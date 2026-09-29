# -*- coding: utf-8 -*-
"""
vp_solution_chemistry.py — VP 용액화학: 양성자 전달 평형 (재현가능·인과적)
====================================================================
사용자 흐름: 평형·속도 → 용액화학. 산염기 = 양성자 전달 평형. H⁺=맨 VP 양성자(노즐).
      전달평형이 ΔG=ΔH−TΔS(회전엔트로피, vp_equilibrium)로 지배 → pH·완충·적정.

핵심: HA ⇌ H⁺ + A⁻. H⁺=맨 양성자(vp_acid_base). 평형상수 Ka=[H⁺][A⁻]/[HA].
      물 자체이온화 Kw=[H⁺][OH⁻]=10⁻¹⁴ → pH+pOH=14. pH=−log[H⁺].

인과 사슬: 양성자 전달평형(ΔG=ΔH−TΔS) → Ka → 약산 pH=½(pKa−logC),
      완충 Henderson-Hasselbalch pH=pKa+log([A⁻]/[HA]), 적정 당량점 도약.

등급: [F] pH 척도·Kw·약산 pH·Henderson-Hasselbalch·적정곡선·완충 (평형 틀)
      [CAL] 개별 pKa(산 고유 결합·용매화) · [O] 절대 pKa 예측(용매화 정밀)
실행: python3 vp_solution_chemistry.py   (표준 라이브러리만)
"""
import math
KW = 1.0e-14    # 물 이온곱 (25°C)

def pH_strong_acid(C):  return -math.log10(C)
def pH_strong_base(C):  return 14 + math.log10(C)

def pH_weak_acid(C, Ka):
    """약산 정확해: Ka=x²/(C−x) → x. pH=−log x."""
    x = (-Ka + math.sqrt(Ka*Ka + 4*Ka*C))/2
    return -math.log10(x)

def pH_weak_base(C, Kb):
    x = (-Kb + math.sqrt(Kb*Kb + 4*Kb*C))/2
    return 14 + math.log10(x)

def henderson(pKa, ratio):
    """완충 pH = pKa + log([A⁻]/[HA])."""
    return pKa + math.log10(ratio)

def titration_pH(Va_mL, Ca, Vb_mL, Cb):
    """강산(Va,Ca)에 강염기(Vb,Cb) 적정 시 pH."""
    mol_a = Ca*Va_mL/1000; mol_b = Cb*Vb_mL/1000
    Vtot = (Va_mL+Vb_mL)/1000
    if mol_b < mol_a:
        return -math.log10((mol_a-mol_b)/Vtot)
    elif mol_b > mol_a:
        return 14 + math.log10((mol_b-mol_a)/Vtot)
    return 7.0   # 당량점

# 약산/염기 (pKa or pKb)
ACIDS = [("아세트산 CH3COOH",1.8e-5,4.74),("폼산 HCOOH",1.8e-4,3.75),
         ("플루오린화수소 HF",6.6e-4,3.18),("탄산 H2CO3",4.3e-7,6.37),
         ("시안화수소 HCN",6.2e-10,9.21)]


def main():
    print("="*72)
    print("VP 용액화학 — 양성자 전달 평형 (H⁺=맨 VP 양성자)")
    print("="*72)
    print("\n원리: HA⇌H⁺+A⁻. H⁺=노즐(맨 양성자). Ka가 전달평형(ΔG=ΔH−TΔS) 지배. Kw=10⁻¹⁴.")

    # ── pH 척도 ──
    print("\n[pH 척도] Kw=[H⁺][OH⁻]=10⁻¹⁴ → pH+pOH=14")
    print(f"  순수한 물: [H⁺]=[OH⁻]=√Kw={math.sqrt(KW):.1e} M → pH={-math.log10(math.sqrt(KW)):.1f} (중성)")
    print(f"  {'용액':<18}{'농도M':>8}{'pH':>7}  성격")
    print("  "+"-"*40)
    for name,C in [("강산 HCl",0.1),("강산 HCl",0.001),("강염기 NaOH",0.1),("강염기 NaOH",0.001)]:
        if "산" in name: pH=pH_strong_acid(C); s="산성"
        else: pH=pH_strong_base(C); s="염기성"
        print(f"  {name:<18}{C:>8}{pH:>7.1f}  {s}")
    print("  → 강산/강염기 완전해리. pH=−log[H⁺]. 회석하면 7로 접근. [F]")

    # ── 약산 pH ──
    print("\n[약산 pH] 부분해리: Ka=x²/(C−x). 0.1M 기준")
    print(f"  {'약산':<22}{'Ka':>10}{'pKa':>6}{'pH(0.1M)':>10}")
    print("  "+"-"*48)
    for name,Ka,pKa in ACIDS:
        pH = pH_weak_acid(0.1, Ka)
        print(f"  {name:<22}{Ka:>10.1e}{pKa:>6.2f}{pH:>10.2f}")
    print("  → 약산일수록(Ka작을수록) 덜 해리 → pH 높음(덜 산성). 아세트산 0.1M pH=2.87 일치. [F]")
    print("    HCN(pKa9.2)은 거의 해리 안함 → pH 5.1. 양성자 거의 안 내놓음. [CAL](pKa)")

    # ── 약염기 ──
    print("\n[약염기 pH] 암모니아 NH3 (Kb=1.8e-5)")
    print(f"  0.1M NH3: pH = {pH_weak_base(0.1, 1.8e-5):.2f} (약염기, OH⁻ 부분생성)")
    print("  → NH3+H2O⇌NH4⁺+OH⁻. 약염기는 pH<14(부분). [F]")

    # ── 완충 (Henderson-Hasselbalch) ──
    print("\n[완충] Henderson-Hasselbalch: pH = pKa + log([A⁻]/[HA])")
    print(f"  아세트산 완충(pKa 4.74):")
    print(f"  {'[A⁻]/[HA]':>10}{'pH':>8}  비고")
    print("  "+"-"*30)
    for ratio,note in [(0.1,"산 많음"),(1.0,"같음(pH=pKa)"),(10,"염기 많음")]:
        print(f"  {ratio:>10.1f}{henderson(4.74,ratio):>8.2f}  {note}")
    print("  → [A⁻]=[HA]일 때 pH=pKa (반당량점). 완충은 pKa±1 범위서 pH 안정. [F]")
    print("    완충작용: 산/염기 가해도 비율만 조금 변해 pH 거의 불변(생체 pH 유지).")

    # ── 적정곡선 ──
    print("\n[적정곡선] 0.1M HCl 25mL에 0.1M NaOH 적정")
    print(f"  {'NaOH[mL]':>9}{'pH':>7}  단계")
    print("  "+"-"*28)
    for Vb in [0, 10, 20, 24, 25, 26, 30, 40]:
        pH = titration_pH(25, 0.1, Vb, 0.1)
        stage = ("당량점" if Vb==25 else "산성영역" if Vb<25 else "염기영역")
        print(f"  {Vb:>9}{pH:>7.2f}  {stage}")
    print("  → 당량점(25mL)서 pH 급도약(2.x→11.x). 강산+강염기 당량점 pH=7. [F]")
    print("    도약 폭이 지시약 선택 근거. 양성자 전달의 완결점.")

    # ── 용해도 (간단) ──
    print("\n[용해도곱] Ksp = 이온농도곱 (포화)")
    print("  • AgCl: Ksp=1.8e-10 → 용해도 √Ksp=1.3e-5 M (난용성).")
    print("  • 용해 ΔG=ΔH(격자−용매화)−TΔS: 격자에너지 vs 수화에너지 경쟁(vp_equilibrium 틀).")
    print("  → 이온결정 용해도 평형도 ΔG=ΔH−TΔS. 회전엔트로피(수화) 기여. [CAL]")

    # ── VP 통일 ──
    print("\n[VP 통일] 양성자 전달 평형")
    print("  • H⁺ = 맨 VP 양성자(노즐, vp_acid_base). 산도=결합극성 vs 결합세기(√2).")
    print("  • 전달평형 Ka = ΔG=ΔH−TΔS(회전엔트로피, vp_equilibrium)에서.")
    print("  • pH·완충·적정 = 양성자 전달평형의 정량. 용액화학이 평형 틀 위에.")

    print("\n" + "="*72)
    print("등급: [F] pH 척도·Kw·약산 pH·Henderson-Hasselbalch·적정·완충 (평형 틀)")
    print("      [CAL] 개별 pKa(산 고유) · [O] 절대 pKa 예측(용매화 정밀)")
    print("      핵심: 산염기=양성자 전달평형. H⁺=맨 양성자, ΔG=ΔH−TΔS가 지배.")
    print("="*72)


if __name__ == "__main__":
    main()
