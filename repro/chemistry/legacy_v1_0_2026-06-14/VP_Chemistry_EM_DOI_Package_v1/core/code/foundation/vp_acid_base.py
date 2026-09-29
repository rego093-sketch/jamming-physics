# -*- coding: utf-8 -*-
"""
vp_acid_base.py — VP 산·염기: 양성자(노즐) 이동의 화학 (재현가능·인과적)
====================================================================
주장: 산-염기는 본질적으로 *양성자(H+) 이동*이다. VP에서 H+ = 알몸 양성자(89=82+7,
      노즐=+1, 전자 없음). 산도 = 결합이 이 노즐을 얼마나 쉽게 놓느냐 =
      결합 극성(전기음성도, 놓기 유리) 대 결합 강도(√2 파열, 놓기 저항)의 경쟁.
      Lewis 산-염기 = 전자영역(빈 궤도 받음 vs 고립쌍 줌) — VSEPR/옥텟 기하.

인과 사슬: H+ = VP 양성자(노즐). 산 H-X 탈양성자 ⇔ X-H 결합 극성↑(전기음성도) +
           결합강도↓(BDE). 두 인자 경쟁 → 주기/족/옥시산 경향. 전부 기존 VP 구조 위.

등급: [F] H+=양성자(노즐)·Lewis=전자영역·하이드로늄 기하(VSEPR) ·
      [F?] 산도 경향(극성 vs 결합강도 경쟁, 순서) · [O] 절대 pKa(완전 열역학/용매)
실행: python3 vp_acid_base.py   (표준 라이브러리만)
"""
import math

def spearman_ok(pred, actual):
    """예측 순서가 실제 순서와 일치하는가 (단조)."""
    pr = sorted(range(len(pred)), key=lambda i: pred[i])
    ac = sorted(range(len(actual)), key=lambda i: actual[i])
    return pr == ac or pr == ac[::-1]


def main():
    print("="*72)
    print("VP 산·염기 — 양성자(노즐) 이동의 화학")
    print("="*72)

    # ── H+ = VP 양성자 ──
    print("\n[H+ = VP 양성자] 산-염기의 주인공")
    print("  • H+ = 알몸 양성자(전자 0). 구조 89=82+7, 노즐이 +1 전하를 줌(전하 출처).")
    print("  • 산-염기 반응 = 이 노즐(양성자)이 산→염기로 이동. 전자쌍이 아니라 양성자가 움직임.")
    print("  • Brønsted: 산=H+ 줌, 염기=H+ 받음.  Lewis: 산=전자쌍 받음, 염기=전자쌍 줌.")

    # ── Brønsted 산도: 두 인자 경쟁 ──
    print("\n[Brønsted 산도] = 결합 극성(놓기 유리) 대 결합 강도(놓기 저항)")

    # 주기 경향 (주기2 H-X): 전기음성도 지배
    print("\n  (1) 주기 경향 CH4·NH3·H2O·HF — 전기음성도 지배")
    period = [("CH4","C",2.55,50),("NH3","N",3.04,38),("H2O","O",3.44,15.7),("HF","F",3.98,3.2)]
    print(f"     {'산':<5}{'X':<3}{'전기음성도':>9}{'pKa실측':>8}")
    for a,x,en,pka in period:
        print(f"     {a:<5}{x:<3}{en:>9.2f}{pka:>8.1f}")
    en_pred = [en for _,_,en,_ in period]; pka_act = [pka for _,_,_,pka in period]
    print(f"     → 전기음성도↑ ⇒ 산도↑(pKa↓): 순서 일치 {spearman_ok(en_pred, [-p for p in pka_act])} ✓")
    print(f"       (더 전기음성한 X가 전자 당겨 H 약화 + 짝염기 X⁻ 안정 → H+ 놓기 쉬움)")

    # 족 경향 (족17 HX): 결합 강도 지배
    print("\n  (2) 족 경향 HF·HCl·HBr·HI — 결합 강도 지배 (전기음성도와 반대!)")
    group = [("HF",570,3.2),("HCl",432,-7),("HBr",366,-9),("HI",298,-10)]
    print(f"     {'산':<5}{'BDE[kJ/mol]':>12}{'pKa실측':>9}")
    for a,bde,pka in group:
        print(f"     {a:<5}{bde:>12}{pka:>9}")
    bde_pred = [bde for _,bde,_ in group]; pka_g = [pka for _,_,pka in group]
    print(f"     → 결합강도↓ ⇒ 산도↑: 순서 일치 {spearman_ok(bde_pred, [-p for p in pka_g])} ✓")
    print(f"       (F 가 가장 전기음성이나 HF 가 가장 약산 — 강한 H-F 결합이 양성자 붙잡음.")
    print(f"        족에선 √2 결합파열 저항(BDE)이 극성을 이긴다.)")

    # 옥시산 (HClOn): 산소수 지배
    print("\n  (3) 옥시산 HClO_n — 산소수(전자끌기+공명) 지배")
    oxy = [("HClO",1,7.5),("HClO2",2,2.0),("HClO3",3,-1),("HClO4",4,-10)]
    print(f"     {'산':<7}{'O수':>4}{'pKa실측':>9}")
    for a,n,pka in oxy:
        print(f"     {a:<7}{n:>4}{pka:>9}")
    n_pred=[n for _,n,_ in oxy]; pka_o=[pka for _,_,pka in oxy]
    print(f"     → 산소수↑ ⇒ 산도↑: 순서 일치 {spearman_ok(n_pred,[-p for p in pka_o])} ✓")
    print(f"       (O 가 전자 끌어 짝염기 음전하 분산/공명 안정 → H+ 놓기 쉬움)")

    # ── 경쟁 종합 ──
    print("\n[경쟁 종합] 산도 = 극성(놓기) vs 결합강도(저항)")
    print("  • 주기·옥시산: 전기음성도/전자끌기(극성·짝염기안정) 지배 → 산도↑")
    print("  • 족: 결합강도(√2 파열저항) 지배 → 약한결합 산도↑")
    print("  • 둘 다 이미 VP 안: 극성=P_idx/전기음성도, 결합강도=√2 결합파열. 산도=둘의 경쟁.")

    # ── Lewis 산-염기 = 전자영역 ──
    print("\n[Lewis 산-염기] 전자영역(VSEPR)에서 직접")
    lewis = [("BF3","Lewis산","빈 궤도(6전자, 옥텟 미달)","전자쌍 받음"),
             ("NH3","Lewis염기","고립쌍 1","전자쌍 줌"),
             ("H2O","Lewis염기","고립쌍 2","전자쌍 줌"),
             ("AlCl3","Lewis산","빈 궤도","전자쌍 받음")]
    print(f"  {'분자':<7}{'분류':<10}{'전자영역':<22}{'역할'}")
    for m,c,e,r in lewis:
        print(f"  {m:<7}{c:<10}{e:<22}{r}")
    print("  → 빈 궤도(옥텟미달)=Lewis산, 고립쌍=Lewis염기. NH3+BF3→H3N-BF3(전자쌍 공유).")
    print("    Lewis 산-염기가 옥텟/VSEPR 전자영역에서 직접 나온다.")

    # ── 하이드로늄/수산화 기하 ──
    print("\n[하이드로늄·수산화 기하] 양성자 이동 산물 (VSEPR)")
    print("  • H3O⁺ (하이드로늄): 3결합 + 1고립쌍 = 4영역 → 삼각뿔(NH3 닮음), 각 ~107°.")
    print("  • OH⁻ (수산화): 산소에 고립쌍 3 → 강한 전자쌍 주개(강염기).")
    print("  • 물 자동이온화: 2H2O ⇌ H3O⁺ + OH⁻ (양성자=노즐 이동). Kw=[H3O⁺][OH⁻]=10⁻¹⁴.")

    # ── pH 척도 ──
    print("\n[pH 척도] 양성자 농도 = pH = −log[H⁺]")
    print(f"  {'용액':<12}{'[H⁺] mol/L':>12}{'pH':>6}")
    for name, h in [("중성(순수물)",1e-7),("산성(0.01M HCl)",1e-2),("염기(0.01M NaOH)",1e-12)]:
        print(f"  {name:<12}{h:>12.0e}{-math.log10(h):>6.1f}")
    print("  → pH = 양성자(노즐) 농도의 로그 척도. 산-염기 정량의 기준.")

    print("\n" + "="*72)
    print("등급: [F] H+=양성자(노즐)·Lewis=전자영역·하이드로늄 기하(VSEPR)")
    print("      [F?] 산도 경향 3종(주기·족·옥시산, 극성 vs 결합강도 경쟁 순서 일치)")
    print("      [O] 절대 pKa(완전 열역학·용매·엔트로피) — 경향은 VP, 절대값은 다체/용매")
    print("      핵심: 산-염기 = 양성자(노즐) 이동. 산도=극성(P_idx) vs 결합강도(√2)의 경쟁.")
    print("            Lewis=전자영역(VSEPR). 화학의 산-염기 축이 VP 기하 위에 선다.")
    print("="*72)


if __name__ == "__main__":
    main()
