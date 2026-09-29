# -*- coding: utf-8 -*-
"""
vp_water_electrolysis.py — 물정수의 화학: 물 전기분해 전극 (재현가능)
======================================================================
Stream D3a (정밀계획 v2). 촉매(Stream C, d-밴드)를 물정수/청정수소로 잇는다.
물 분해 2H₂O → 2H₂ + O₂ 는 (i) 청정수소 생산과 (ii) 전기화학 수처리의 토대다.
방금 만든 d-밴드 튜닝 레버(vp_dband_catalysis)로 전극을 설계한다 — 촉매→물정수 한 흐름.

이 모듈이 답하는 것:
  [1] 열역학 — 최소 1.23V, 열중립 1.48V, 그 차이(TΔS)는 열로 공급.
  [2] 셀 전압 분해 — 1.23 + η_HER + η_OER + iR. *OER 가 병목*(가장 큰 손실).
  [3] HER 화산 — 정점 Pt(ΔG_H≈0, Stream C 재사용).
  [4] ★OER 스케일링 한계 — 중간체(*OH·*O·*OOH) 결합이 묶여 *근본 과전압 ~0.37V*.
      정점 RuO₂/IrO₂. (왜 OER 가 영원히 비싼가의 정량 근거.)
  [5] d-밴드 전극 설계 — 합금·변형으로 결합을 한계 쪽으로(반증된 기하 공명의 대체).
  [6] Faraday — H₂ 18.66 mmol/A·h, 에너지효율 = 1.48/V_cell.

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_water_electrolysis.py
"""
import math

F = 96485.0          # 패러데이 상수 [C/mol]
E_OER = 1.229        # 산소발생 표준전위 [V] (OER: 2H₂O→O₂+4H⁺+4e⁻) [CAL]
E_HER = 0.0          # 수소발생 표준전위 [V] (정의상 SHE 기준 0)
DH_SPLIT = 285800.0  # 물 분해 ΔH [J/mol H₂] (액체물) [CAL]
G_SCALING = 3.20     # OER 보편 스케일링: ΔG(*OOH)−ΔG(*OH) ≈ 3.2 eV [CAL] (Nørskov/Man)

# HER 검증쌍 (ε_d, ΔG_H) [CAL] — Stream C 와 동일 앵커(정점 Pt)
HER = [("Ni",-1.29,-0.28),("Rh",-1.73,-0.28),("Pd",-1.83,-0.20),("Ir",-2.11,-0.10),
       ("Pt",-2.25,-0.09),("Cu",-2.67,0.30),("Au",-3.56,0.30)]

# OER 촉매 descriptor ΔG(*O)−ΔG(*OH) [eV] [CAL] (Man et al. 2011, rutile/산화물 근사)
OER = [("RuO2",1.60),("IrO2",1.57),("Co3O4",1.42),("MnO2",1.30),("NiO",2.05),
       ("PtO2",2.00),("TiO2",2.40)]


def oer_overpotential(desc):
    """OER 이론 과전압: 4단계 중 큰 자유에너지 갭이 율속.
    두 갭 = (ΔG_O−ΔG_OH)=desc, (ΔG_OOH−ΔG_O)=G_SCALING−desc.
    η = max(두 갭)/e − 1.23 [V]. desc=1.6 에서 최소 0.37V (스케일링 한계)."""
    step_a = desc                       # *OH → *O
    step_b = G_SCALING - desc           # *O  → *OOH
    return max(step_a, step_b) - E_OER


def sabatier(binding, optimum, scale):
    return math.exp(-abs(binding - optimum) / scale)


def main():
    print("=" * 72)
    print("물정수의 화학 — 물 전기분해 전극 2H₂O → 2H₂ + O₂ (청정수소 + 수처리)")
    print("=" * 72)
    print("촉매(Stream C, d-밴드) → 물정수 한 흐름. 같은 튜닝 레버로 전극 설계.")

    # ── [1] 열역학 ──
    print("\n" + "─" * 72)
    print("[1] 열역학 — 최소 1.23V, 열중립 1.48V, 차이는 TΔS(열) [F]")
    print("─" * 72)
    Ecell = E_OER - E_HER
    dG = 2 * F * Ecell                  # n=2 (H₂ 1몰당 2전자)
    V_tn = DH_SPLIT / (2 * F)           # 열중립 전압 = ΔH/(nF)
    TdS = DH_SPLIT - dG
    print(f"  E°cell = E°(OER) − E°(HER) = {E_OER} − {E_HER} = {Ecell:.3f} V (가역 최소)")
    print(f"  ΔG = nFE = 2·{F:.0f}·{Ecell:.3f} = {dG/1000:.1f} kJ/mol H₂")
    print(f"  열중립 전압 V_tn = ΔH/(nF) = {DH_SPLIT/1000:.1f}/(2·{F:.0f}) = {V_tn:.3f} V")
    print(f"  TΔS = ΔH − ΔG = {TdS/1000:.1f} kJ/mol (이 열을 전기로도 주면 1.48V, 환경열이면 1.23V)")
    assert abs(Ecell - 1.229) < 1e-3 and abs(V_tn - 1.481) < 2e-3, "열역학 상수 불일치"
    print("  → 1.23V 미만은 분해 불가(열역학 금지). 실제는 과전압 때문에 1.8–2.0V.")

    # ── [2] 셀 전압 분해: OER 병목 ──
    print("\n" + "─" * 72)
    print("[2] 셀 전압 분해 — V_cell = 1.23 + η_HER + η_OER + iR (OER 가 병목) [F?]")
    print("─" * 72)
    eta_her, eta_oer, iR = 0.03, 0.37, 0.20   # Pt HER ~30mV, 최선 OER ~0.37V, 옴손실
    Vcell = E_OER + eta_her + eta_oer + iR
    print(f"  {'기여':<22}{'전압[V]':>9}  비고")
    print(f"  {'가역 (열역학 최소)':<20}{E_OER:>9.3f}  넘을 수 없는 바닥")
    print(f"  {'η_HER (수소, Pt)':<21}{eta_her:>9.3f}  작음 — d-밴드 정점 Pt")
    print(f"  {'η_OER (산소)':<22}{eta_oer:>9.3f}  ★최대 손실 — 스케일링 한계")
    print(f"  {'iR (옴/막/기포)':<21}{iR:>9.3f}  공학적 최소화 대상")
    print(f"  {'합계 V_cell':<22}{Vcell:>9.3f}  실제 운전 전압")
    print(f"  → 전압효율 = 1.48/{Vcell:.2f} = {V_tn/Vcell*100:.0f}% (열중립 기준).")
    print(f"    OER η 가 단일 최대 손실 → 전극 개선의 1순위.")
    assert eta_oer > eta_her, "OER 가 병목이 아님(모순)"

    # ── [3] HER 화산: 정점 Pt (Stream C 재사용) ──
    print("\n" + "─" * 72)
    print("[3] HER 화산 — 정점 Pt (ΔG_H≈0, d-밴드 에너지 공명) [F?]")
    print("─" * 72)
    scale = 0.15
    rows = sorted([(n, dg, sabatier(dg, 0.0, scale)) for n, ed, dg in HER],
                  key=lambda x: -x[2]); amax = max(x[2] for x in rows)
    print(f"  {'금속':<6}{'ΔG_H[eV]':>10}{'활성':>8}  막대")
    for n, dg, act in rows:
        print(f"  {n:<6}{dg:>+10.2f}{act:>8.3f}  {'█'*int(22*act/amax)}")
    assert rows[0][0] in ("Pt", "Ir"), "HER 정점 재현 실패"
    print(f"  → 정점 {rows[0][0]}. 음극(수소) 쪽은 거의 해결됨 — 손실은 양극(OER).")

    # ── [4] ★OER 스케일링 한계 ──
    print("\n" + "─" * 72)
    print("[4] ★OER 스케일링 한계 — 중간체 결합이 묶여 근본 과전압 ~0.37V [F?]")
    print("─" * 72)
    print(f"  4단계 OER 의 *OH·*O·*OOH 결합이 보편 관계 ΔG(*OOH)−ΔG(*OH)≈{G_SCALING}eV 로 묶임.")
    print(f"  → 두 중간 갭을 1.23/1.23 으로 못 가르고 최선이 1.6/1.6 → η_min = 1.6−1.23 = 0.37V.")
    orows = sorted([(n, d, oer_overpotential(d)) for n, d in OER], key=lambda x: x[2])
    print(f"  {'촉매':<7}{'ΔG_O−ΔG_OH':>12}{'η_OER[V]':>10}  막대(낮을수록 좋음)")
    omax = max(x[2] for x in orows)
    for n, d, eta in orows:
        bar = '█' * int(22 * eta / omax)
        tag = " ← 정점(산업 OER)" if n in ("RuO2", "IrO2") else ""
        print(f"  {n:<7}{d:>12.2f}{eta:>10.3f}  {bar}{tag}")
    eta_min = oer_overpotential(1.60)
    assert abs(eta_min - 0.37) < 0.01, f"스케일링 한계 0.37V 재현 실패: {eta_min}"
    assert orows[0][0] in ("RuO2", "IrO2"), "OER 정점 재현 실패"
    print(f"  → 한계 η_min={eta_min:.2f}V (desc=1.6). 정점 {orows[0][0]}. RuO₂/IrO₂ 가 산업 OER 촉매.")
    print(f"    이 0.37V 가 물분해를 영원히 비싸게 하는 근본 한계 — 스케일링을 깨야(3D/이중자리) 넘는다.")

    # ── [5] d-밴드 전극 설계 레버 ──
    print("\n" + "─" * 72)
    print("[5] d-밴드 전극 설계 — 합금·변형으로 결합을 한계 쪽으로 (기하 공명 대체) [F?]")
    print("─" * 72)
    print("  반증된 '격자간격 기하 공명' 대신, ε_d 이동(합금/변형/코어쉘)으로 중간체 결합을")
    print("  최적(HER: ΔG_H→0, OER: desc→1.6)에 맞춘다. 예) OER 촉매 결합 desc 를 1.6 으로:")
    print(f"  {'desc[eV]':>9}{'η_OER[V]':>10}  방향")
    for d in (2.0, 1.8, 1.6, 1.4):
        eta = oer_overpotential(d)
        arrow = " ← 한계(목표)" if abs(d - 1.6) < 1e-6 else (" (강결합 쪽)" if d < 1.6 else " (약결합 쪽)")
        print(f"  {d:>9.2f}{eta:>10.3f} {arrow}")
    print("  → 설계 규칙: 결합을 약→강(또는 역)으로 *에너지* 이동해 정점 정렬. 격자맞춤 아님.")

    # ── [6] Faraday: 생산량·효율 ──
    print("\n" + "─" * 72)
    print("[6] Faraday — H₂ 생산량과 에너지효율 [F]")
    print("─" * 72)
    n_H2_per_Ah = 3600.0 / (2 * F)          # 1 A·h 당 H₂ 몰수 (z=2)
    print(f"  n(H₂) = It/(zF); 1 A·h → {n_H2_per_Ah*1000:.2f} mmol H₂ = {n_H2_per_Ah*22.4*1000:.1f} mL(STP)")
    print(f"  1몰 H₂(=22.4L STP) 생산에 필요한 전하 = zF = {2*F/1000:.1f} kC = {2*F/3600:.1f} A·h")
    print(f"  에너지효율 = V_tn/V_cell = {V_tn:.2f}/{Vcell:.2f} = {V_tn/Vcell*100:.0f}% (열중립 기준)")
    assert abs(n_H2_per_Ah*1000 - 18.66) < 0.05, "Faraday H₂ 생산량 불일치"
    print("  → 청정수소: 불순수에서도 H₂(음극)·O₂(양극)는 순수하게 분리 생산.")

    # ── [7] 물정수 연결 ──
    print("\n" + "─" * 72)
    print("[7] 물정수 연결 — 전기화학 수처리 [F?]/[CAL]")
    print("─" * 72)
    print("  · 청정수소/산소: 오염수에서도 H₂·O₂ 가스만 순수 추출(가스상 분리).")
    print("  · 전기응집(electrocoagulation): 양극 용해 금속이온이 오염물 응집·침전.")
    print("  · 전기투석/축전식 탈이온(CDI): 전위로 이온 이동·흡착 → 담수화(전력 사용).")
    print("  · 같은 전극 과학(과전압·d-밴드) 위에 선다 → 자석 담수(D3b)와 정직 비교 예정.")

    # ── 결론 + 등급 ──
    print("\n" + "=" * 72)
    print("결론 — 물 전기분해는 d-밴드 촉매 위에서 정량 완성된다")
    print(f"  ① 열역학 바닥 1.23V/열중립 1.48V (TΔS={TdS/1000:.0f}kJ 열) ② OER 가 병목")
    print(f"  ③ HER 정점 Pt ④ ★OER 스케일링 근본 한계 η_min={eta_min:.2f}V(RuO₂/IrO₂)")
    print(f"  ⑤ 전극 설계는 d-밴드 *에너지* 이동(기하 공명 대체) ⑥ Faraday 18.66 mmol/A·h")
    print("-" * 72)
    print("등급: [F] 열역학(1.23/1.48V)·Faraday · [F?] OER 스케일링 한계·HER/OER 정점·d-밴드 설계 ·")
    print("      [CAL] E°·ΔH·스케일링 3.2eV·OER descriptor · [O] 절대 과전압·이중자리 스케일링 회피")
    print("반증가능 예측: OER 단일자리 근본 한계 η≈0.37V; HER 정점 Pt, OER 정점 RuO₂/IrO₂.")
    print("  단일자리 촉매가 η<0.3V 를 안정적으로 보이면 스케일링 그림은 보정 필요.")
    print("=" * 72)


if __name__ == "__main__":
    main()
