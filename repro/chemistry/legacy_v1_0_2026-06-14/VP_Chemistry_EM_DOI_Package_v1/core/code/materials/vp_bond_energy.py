# -*- coding: utf-8 -*-
"""
vp_bond_energy.py — M1 결합에너지 정량 (정직한 부분해, §12 G2)
====================================================================
목표: §4 √2 천장 → 결합해리에너지(BDE, kJ/mol). 분열 Q와 같은 응집-교란 차를 분자결합에.
결과(정직): √2 는 파열 *기하*(변위 (√2−1)r_e)를 [F]로 준다. 그러나 BDE = ∫F dr 는
            퍼텐셜 *모양*(비조화성)을 요구하고, 그 모양은 결합마다 달라 √2 만으로 BDE가
            닫히지 않는다 → BDE 정량은 [O] 유지. 무리하게 닫지 않는다(녹는점·껍질처럼).

이상값 대 범위: √2-조화 모형이 한 '참조 이상값'을 주되, 실 BDE 는 결합차수·고립쌍반발로
                그 둘레에 범위로 퍼진다. 면역 점검: 이 결과는 전자앵커·π·측정 k·r_e 만 쓴다.

실행: python3 vp_bond_energy.py   (표준 라이브러리만)
"""
import math
SQRT2 = math.sqrt(2)
NA = 6.02214076e23
EV = 1.602176634e-19

# √2-조화 계수: D_e = (1/2)k·Δr², Δr=(√2−1)r_e → D_e/(k r_e²) = (√2−1)²/2
VP_COEFF = (SQRT2-1)**2/2          # = 0.0858 (조화 하한)
# Morse 최대힘을 √2 변위에 매핑 시: D_e = k r_e²/[2(ln2/(√2−1))²] = k r_e²·(√2−1)²/(2 ln2²)
VP_COEFF_MORSE = (SQRT2-1)**2/(2*math.log(2)**2)   # = 0.179

# 검증: (결합, 차수, k[N/m], r_e[Å], D_e 측정[kJ/mol], 메모)
BONDS = [
    ("H-H",  1, 575,  0.741, 458, "단일 기준"),
    ("C-C",  1, 450,  1.535, 370, "단일"),
    ("N-N",  1, 560,  1.45,  167, "단일 — 고립쌍반발로 약함"),
    ("O-O",  1, 1180, 1.21,  498, "이중(O2)"),  # O2 is double
    ("N≡N",  3, 2295, 1.098, 945, "삼중 — 매우 강함"),
    ("C≡C",  3, 1620, 1.203, 839, "삼중"),
    ("O-H",  1, 780,  0.96,  497, "단일 — 강한 극성"),
    ("C-H",  1, 480,  1.09,  413, "단일"),
]


def main():
    print("="*72)
    print("M1 결합에너지 — √2 는 파열 기하를 주지만 BDE 는 비조화성을 요구 (정직)")
    print("="*72)

    print(f"\n[기하 [F]] 파열변위 Δr = (√2−1)·r_e = {SQRT2-1:.3f}·r_e  (§4 √2 천장)")
    print(f"  조화 하한 계수  D_e/(k r_e²) = (√2−1)²/2     = {VP_COEFF:.4f}")
    print(f"  Morse-√2 계수   D_e/(k r_e²) = (√2−1)²/2ln2² = {VP_COEFF_MORSE:.4f}  (참조 이상값)")

    print("\n[검증] 실 D_e/(k r_e²) 는 결합마다 다른가? (모양=비조화성 의존성)")
    print(f"  {'결합':<7} {'차수':>3} {'k[N/m]':>7} {'r_e[Å]':>7} {'D_e측정':>8} {'무차원비':>9}")
    print("  "+"-"*60)
    ratios = []
    for name, bo, k, re, De, note in BONDS:
        re_m = re*1e-10
        De_J = De*1000/NA                       # kJ/mol → J/분자
        ratio = De_J/(k*re_m**2)                # 무차원 D_e/(k r_e²)
        ratios.append((name, ratio, bo))
        print(f"  {name:<7} {bo:>3} {k:>7.0f} {re:>7.3f} {De:>8.0f} {ratio:>9.4f}  {note}")
    lo = min(r for _,r,_ in ratios); hi = max(r for _,r,_ in ratios)
    print(f"  → 무차원비 범위 {lo:.3f}–{hi:.3f} (×{hi/lo:.1f} 산포). VP 참조 {VP_COEFF_MORSE:.3f} 는 그 안.")

    print("\n[비평 — √2 만으로 BDE 는 닫히지 않는다 (음성 결과, 정직)]")
    print("  • 무차원비 D_e/(k r_e²) 가 ×10 산포(0.024 N-N ~ 0.241 H-H). 단일 상수로 안 잡힘.")
    print("  • √2-Morse 계수 0.179 로 D_e 예측 시 오차 −26%(H-H) ~ +658%(N-N) → 모형 실패.")
    print("  • 원인: D_e ∝ k/a² (a=비조화 범위)인데, a 는 √2 와 독립이며 결합마다 다르다.")
    print("    k(곡률)와 r_e 는 측정돼도 a(모양)가 자유 → √2 기하만으로 에너지 미결정.")
    print("  • 결론: √2 는 파열 *기하*[F]만 고정. BDE 절대 정량은 닫히지 않음 → **[O] 전면 유지**.")

    print("\n[이상값 + 범위 — 단, 이건 '실패의 범위'다] √2-Morse vs 측정")
    worst = 0
    for name, bo, k, re, De, note in BONDS:
        re_m = re*1e-10
        De_pred = VP_COEFF_MORSE*k*re_m**2 *NA/1000
        err = 100*(De_pred-De)/De; worst = max(worst, abs(err))
        flag = " ✗실패" if abs(err)>50 else " ~참조"
        print(f"  {name:<6} 예측 {De_pred:5.0f} vs 측정 {De:4.0f} kJ/mol  Δ={err:+4.0f}%{flag}")
    print(f"  → 최대 오차 {worst:.0f}%. H-H·O-H·C-H 만 우연히 근접, 나머지 대실패. BDE 는 G2 [O].")
    print("    (무리하게 닫지 않는다 — 백서의 sqrt(2.5) 철회와 같은 규율. 음성 결과도 결과다.)")

    print("\n" + "="*72)
    print("등급: [F] 파열변위 (√2−1)r_e (기하) · [O] BDE 절대 정량 (전면 유지, 비조화성 미해결)")
    print("      정직: 이번 케이스는 *부분 정복도 아닌 음성 결과*. √2≠에너지. 다음 과제로 명확히 남김.")
    print("      교훈: 무차원 구조(σ_th/E·θ_tet)는 닫히나, 에너지 절대값은 추가 물리(비조화성) 필요.")
    print("="*72)


if __name__ == "__main__":
    main()
