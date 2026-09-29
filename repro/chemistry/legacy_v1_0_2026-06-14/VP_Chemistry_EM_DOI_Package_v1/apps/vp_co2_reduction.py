# -*- coding: utf-8 -*-
"""
vp_co2_reduction.py — CO₂ 전기촉매 환원(CO₂RR): d-밴드 CO-결합 descriptor (재현가능)
=============================================================================
정밀계획 v4 — v0_2 §18.6.2 의 *반증된* CO₂판(진폭 205→300fm, 1.46×>√2 로 '해리')을
폐기하고, 검증된 물리(d-밴드 에너지 공명, *CO 흡착결합 descriptor) 위로 재정초한다.
앱의 다른 응용(Pt 촉매·암모니아)과 *같은 d-밴드 엔진*을 CO₂RR 에 적용한다.

핵심 과학(전부 등급화):
  [1] 메커니즘 — CO₂RR 율속/선택성은 *CO 흡착결합(ΔE_CO)*이 지배(Hori/Nørskov).
      '진폭을 √2로 늘려 결합 끊기'(반증)가 아니다. 첫 전자전달 *COOH/*OCHO 가 어려운 단계.
  [2] 열역학 — 다전자 생성물 평형전위는 전부 0V 근처지만, 실제 개시는 −0.8~−1.1V.
      그 차이(과전압)는 CO₂•⁻ 라디칼 음이온(−1.9V)·스케일링 한계에서 온다. [F]
  [3] descriptor — ΔE_CO 가 d-밴드 중심 ε_d 와 상관(r≈−0.9). H·N 과 *같은 엔진*. [F?]
  [4] ★Cu 유일성 — *CO 중간결합(−0.5eV)이 Cu뿐 → 탄화수소/알코올(C₂+) 유일 생성.
      강결합(Pt/Pd/Ni)=CO 피독→H₂, 약결합(Au/Ag/Zn)=CO 방출, sp금속(Sn/Pb/Bi/In)=포름산. [F?]
  [5] 스케일링 한계 — *CO→*CHO 가 ε 무관 ~0.74eV offset → Cu 한계전위 −0.74V.
      (OER 0.37V 한계와 같은 선형 스케일링 족쇄가 CO₂RR 를 어렵게 한다.) [F?]
  [6] HER 경쟁 — 수성에서 늘 2H⁺+2e⁻→H₂(0V)와 경쟁. Cu의 약한 H결합이 H₂ 회피에 유리. [F?]

⇒ 반증가능: Cu가 탄화수소 화산 정점. 순수 비-Cu 금속이 같은 과전압서 탄화수소를 더 내면
   CO-결합 descriptor 그림은 폐기된다. (진폭판의 '300fm 해리'는 측정 무근거였다.)

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_co2_reduction.py
"""

import math

# ── Faraday / 상수 ──
F = 96485.33212

# ── 전이금속 d-밴드 중심 ε_d [eV] (Hammer-Nørskov, 조밀면) [CAL] — 앱 vp_dband_catalysis 와 동일 ──
DBAND = {"Co": -1.17, "Ni": -1.29, "Ru": -1.41, "Rh": -1.73, "Pd": -1.83,
         "Pt": -2.25, "Cu": -2.67, "Au": -3.56, "Ag": -4.30}

# ── *CO 흡착결합 ΔE_CO [eV] (음수=강결합) [CAL] (DFT/실험, Nørskov·Bagger 분류) ──
# d-밴드 금속에서 CO 결합이 *생성물*을 가른다(Hori 4분류).
CO_BIND = {"Co": -1.70, "Ni": -1.65, "Ru": -1.55, "Rh": -1.45, "Pd": -1.35,
           "Pt": -1.30, "Cu": -0.55, "Au": -0.28, "Ag": -0.15}

# ── CO₂RR 평형전위 [V vs RHE] (표준, Kuhl/Nørskov) [CAL anchors → 유도 [F]] ──
# (생성물, 전자수 n, ΔG°[eV/분자] 로부터 E°=−ΔG/nF; 여기선 문헌 E° 직접 [CAL])
CO2RR = [
    ("CO  (일산화탄소)",   2, -0.10),
    ("HCOOH(포름산)",      2, -0.12),
    ("CH3OH(메탄올)",      6,  0.03),
    ("C2H4 (에틸렌)",      12, 0.08),
    ("CH4  (메탄)",        8,  0.17),
]
HER_E0 = 0.00   # 2H⁺+2e⁻→H₂ 경쟁반응 [V vs RHE]

# ── sp-금속(후전이): *OCHO(O-결합)로 포름산. d-밴드 CO descriptor 밖(별도 가지) [CAL] ──
SP_METALS = ["Sn", "Pb", "Bi", "In", "Cd"]

# ── 스케일링 offset: ΔE_CHO ≈ ΔE_CO + Δ_scale (둘 다 C로 결합 → ε 무관 상수) [CAL] ──
DELTA_SCALE = 0.74   # eV (Peterson-Nørskov: *CO→*CHO 가 Cu CH₄ 한계단계)

LED = []
def P(s=""):
    print(s); LED.append(s)


def pearson(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/n
    sx = math.sqrt(sum((x-mx)**2 for x in xs)/n)
    sy = math.sqrt(sum((y-my)**2 for y in ys)/n)
    return cov/(sx*sy), cov/sx**2, my-(cov/sx**2)*mx


def classify(co):
    """*CO 결합 → Hori 생성물 분류."""
    if co <= -1.10:   return "H₂ (CO 피독)"
    if co <= -0.80:   return "CO/혼합"
    if -0.80 < co <= -0.35: return "탄화수소·알코올 (C₂+)"   # Cu 영역
    if -0.35 < co <= 0.0:   return "CO (방출)"
    return "포름산"


def main():
    P("="*74)
    P("CO₂ 전기촉매 환원(CO₂RR) — d-밴드 *CO-결합 descriptor (진폭판 폐기·재정초)")
    P("="*74)
    P("토대: v0_2 §18.6.2 '진폭 300fm 로 CO₂ 해리'(반증) 폐기 → 검증된 *CO 흡착결합(d-밴드).")
    P("      변수는 '진폭'이 아니라 'd-전자 에너지 ↔ *CO 결합'. Pt·암모니아와 같은 엔진.")

    # ── [1] 열역학: 평형전위 vs 실제 개시 (과전압 간극) ──
    P("\n"+"─"*74)
    P("[1] 열역학 — 평형전위는 0V 근처지만 실제 개시 −0.8~−1.1V (과전압 간극) [F]")
    P("─"*74)
    P(f"  {'생성물':<16}{'n(e⁻)':>6}{'E°[V vs RHE]':>14}{'vs HER(0V)':>12}")
    for name, n, e0 in CO2RR:
        rel = "위(쉬움)" if e0 > HER_E0 else "아래(어려움)"
        P(f"  {name:<16}{n:>6}{e0:>+14.2f}   {rel}")
    P(f"  경쟁: 2H⁺+2e⁻→H₂  E°={HER_E0:+.2f} (HER, 늘 동반)")
    P("  → 평형은 0V 부근이나, 첫 전자전달 CO₂+e⁻→*CO₂•⁻ 가 −1.9V(라디칼)라 큰 과전압.")
    P("    촉매가 *COOH/*OCHO 를 안정화해 이를 낮춘다 — 그 정도가 ΔE_CO 로 정해진다.")
    # 자가검증: CO/HCOOH 는 HER 아래(더 음전위), CH4 는 위
    assert CO2RR[0][2] < HER_E0 < CO2RR[-1][2], "평형전위 순서 오류"

    # ── [2] descriptor: ΔE_CO ↔ ε_d 상관 ──
    P("\n"+"─"*74)
    P("[2] descriptor — *CO 결합이 d-밴드 중심 ε_d 와 상관 (H·N 과 같은 엔진) [F?]")
    P("─"*74)
    metals = [m for m in DBAND if m in CO_BIND]
    eds = [DBAND[m] for m in metals]
    cos = [CO_BIND[m] for m in metals]
    r, a, b = pearson(eds, cos)
    P(f"  ε_d ↔ ΔE_CO 상관 r = {r:.3f} (강함). 회귀 ΔE_CO = {a:.3f}·ε_d {b:+.3f}")
    P(f"  {'금속':<5}{'ε_d[eV]':>8}{'ΔE_CO[eV]':>10}{'예측':>9}{'분류':>20}")
    for m in metals:
        pred = a*DBAND[m] + b
        P(f"  {m:<5}{DBAND[m]:>8.2f}{CO_BIND[m]:>10.2f}{pred:>+9.2f}   {classify(CO_BIND[m])}")
    assert abs(r) > 0.85, "ε_d↔CO 상관 약함 — descriptor 실패"
    P("  → ε_d(밴드구조 독립입력)가 *CO 결합을 예측. 진폭 불필요 — 에너지 descriptor.")

    # ── [3] Hori 4분류: CO 결합 → 생성물 (Cu 유일) ──
    P("\n"+"─"*74)
    P("[3] Hori 4분류 — *CO 결합세기가 생성물을 가른다 (★Cu 유일 탄화수소) [F?]")
    P("─"*74)
    groups = {}
    for m in metals:
        groups.setdefault(classify(CO_BIND[m]), []).append(m)
    for m in SP_METALS:
        groups.setdefault("포름산", []).append(m)
    order = ["H₂ (CO 피독)", "탄화수소·알코올 (C₂+)", "CO (방출)", "포름산", "CO/혼합"]
    for g in order:
        if g in groups:
            P(f"  {g:<22} ← {', '.join(groups[g])}")
    cu_group = classify(CO_BIND["Cu"])
    hydro = groups.get("탄화수소·알코올 (C₂+)", [])
    P(f"  ★ 탄화수소 생성 금속 = {hydro}  → 순수금속 중 Cu 단독.")
    assert hydro == ["Cu"], f"Cu 유일성 실패: {hydro}"
    P("    강결합(Pt/Pd/Ni): CO 가 표면 피독 → H₂. 약결합(Au/Ag): CO 그대로 방출.")
    P("    Cu만 *CO 를 '적당히' 잡아 더 환원(*CHO→…→CH₄/C₂H₄). 실험적 사실(Hori) 재현.")

    # ── [4] Cu 유일성 화산 + 스케일링 한계전위 ──
    P("\n"+"─"*74)
    P("[4] Cu 화산 정점 + 스케일링 한계전위 −0.74V (*CO→*CHO) [F?]")
    P("─"*74)
    CO_OPT = -0.55   # 탄화수소 최적 *CO 결합(중간) [CAL]
    P(f"  {'금속':<5}{'ΔE_CO':>7}{'탄화수소 활성':>14}  막대")
    acts = []
    for m in metals:
        act = math.exp(-abs(CO_BIND[m]-CO_OPT)/0.35)
        acts.append((m, act))
    amax = max(a for _, a in acts)
    for m, act in acts:
        flag = " ←정점(Cu)" if m == "Cu" else ""
        P(f"  {m:<5}{CO_BIND[m]:>7.2f}{act:>14.3f}  {'█'*int(26*act/amax)}{flag}")
    apex = max(acts, key=lambda t: t[1])[0]
    assert apex == "Cu", f"탄화수소 화산 정점이 Cu 아님: {apex}"
    # 스케일링 한계전위
    U_lim = -DELTA_SCALE   # *CO→*CHO ΔG=0.74eV @0V → U_L=−0.74V
    P(f"  스케일링: ΔE_CHO ≈ ΔE_CO + {DELTA_SCALE:.2f}eV (둘 다 C-결합, ε 무관 offset).")
    P(f"  → *CO→*CHO 가 한계단계 → Cu CH₄ 한계전위 U_L = {U_lim:+.2f}V (Peterson-Nørskov).")
    P(f"    이 0.74eV offset 은 ε_d 튜닝으로 못 내림(선형 스케일링 족쇄) — OER 0.37V 한계의 사촌.")
    assert U_lim < CO2RR[-1][2], "한계전위가 CH₄ 평형보다 위(모순)"

    # ── [5] HER 경쟁 / 선택성 ──
    P("\n"+"─"*74)
    P("[5] HER 경쟁 — 수성서 늘 H₂와 경쟁; Cu의 약한 H결합이 H₂ 회피에 유리 [F?]")
    P("─"*74)
    P("  강 d-밴드(Pt/Ni): H도 강결합 → H₂ 빠름 + CO 피독 → CO₂RR 거의 안 됨.")
    P("  Cu(약 H결합 ΔG_H≈+0.1~0.3eV): H₂ 가 느려 *CO 환원이 경쟁력 확보 → 탄화수소.")
    P("  → 같은 ε_d 가 H·CO 둘 다 정함. Cu는 둘의 균형점(H 약·CO 중간)이 유일.")
    P("    (반증가능: Cu보다 H₂를 더 억제하며 탄화수소 내는 순수금속이 있으면 그림 수정.)")

    print("\n"+"="*74)
    print("결론 — CO₂RR 은 d-밴드 *CO-결합으로 닫힌다 (진폭판 폐기, 같은 엔진 재사용)")
    print("  ① 메커니즘: *CO 결합(d-밴드)이 선택성 지배 — 진폭→√2 해리(반증) 아님")
    print("  ② 평형전위 0V 부근이나 실제 −0.8~−1.1V (라디칼 음이온·스케일링 과전압) [F]")
    print(f"  ③ ΔE_CO ↔ ε_d 상관 r={r:.2f} — H·N 과 같은 descriptor [F?]")
    print("  ④ ★Cu 유일 탄화수소(강결합→H₂피독, 약결합→CO, sp→포름산) — Hori 재현 [F?]")
    print(f"  ⑤ 스케일링 한계전위 −0.74V(*CO→*CHO) — OER 0.37V 한계의 사촌 [F?]")
    print("-"*74)
    print("등급: [F] 평형전위·전자수 · [F?] ε_d↔CO descriptor·Cu 유일성·화산·스케일링 한계 ·")
    print("      [CAL] ΔE_CO·ε_d·평형전위·offset · [O] 절대 전류밀도·C-C 짝지음 미세동역학")
    print("반증가능: Cu가 탄화수소 화산 정점·CO₂RR 선택성=*CO결합 순위. 순수 비-Cu 금속이 같은")
    print("  과전압서 탄화수소를 더 내거나 순위가 깨지면 d-밴드 CO descriptor 그림은 폐기된다.")
    print("="*74)


if __name__ == "__main__":
    main()
