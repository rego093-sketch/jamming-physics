# -*- coding: utf-8 -*-
"""
vp_ammonia_synthesis.py — 비료의 화학: 암모니아 합성 (재현가능)
==================================================================
Stream D2 (정밀계획 v2). 질소 고정 N₂ + 3H₂ ⇌ 2NH₃ — 인류 식량의 절반을 떠받치는
반응(Haber-Bosch)을 VP 화학의 두 기둥으로 완성한다:
  · 평형(CH.8): ΔG=ΔH−TΔS 와 Le Chatelier 가 *왜* 고압·중온·촉매를 강제하는가.
  · 촉매(Stream C, d-밴드): *왜* Fe/Ru 인가 — N≡N 해리 화산의 정점.

이 모듈이 답하는 것:
  [1] 평형 — 저온은 수율↑이나 속도≈0; 고온은 속도↑이나 수율↓ → 절충 + 고압(Δn=−2).
  [2] 임계온도 — ΔG=0 넘으면 평형이 역전(왜 무한정 가열 못함).
  [3] 율속 장벽 — N≡N(945 kJ/mol)이 가장 강한 결합 → 촉매 필수.
  [4] 촉매 화산 — N 결합세기 descriptor → 정점 Fe/Ru (산업 촉매 재현, d-밴드와 연결).

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_ammonia_synthesis.py
"""
import math

R = 8.314            # 기체상수 [J/mol·K]
# 표준 반응량 (298 K) [CAL] — N₂+3H₂⇌2NH₃
DH = -91800.0        # ΔH° [J/mol] (발열; 2·ΔHf(NH₃)=2·(−45.9 kJ))
DS = -198.1          # ΔS° [J/mol·K] (음수; 기체 4몰→2몰)
BOND_NN = 945.0      # N≡N 삼중결합 해리에너지 [kJ/mol] (가장 강한 등핵 결합 중 하나)
BOND_HH = 436.0      # H–H [kJ/mol]
BOND_NH = 391.0      # N–H (평균) [kJ/mol]

# 질소 흡착 E_N [eV] (½N₂ 기준, 음수=강결합) [CAL] — 암모니아 화산 (Jacobsen/Nørskov)
NITROGEN = [("Mo",-1.30),("W",-0.95),("Re",-0.80),("Fe",-0.50),("Ru",-0.42),
            ("Os",-0.40),("Co",0.00),("Ni",0.35),("Pd",0.70),("Pt",0.80)]
E_N_OPT = -0.50      # 화산 최적 N 결합 [CAL]


def K_eq(T):
    """평형상수 K(T) = exp(−ΔG°/RT), ΔG°=ΔH−TΔS (van 't Hoff, ΔH·ΔS 근사 일정) [F?]."""
    dG = DH - T * DS
    return math.exp(-dG / (R * T)), dG


def equil_NH3_fraction(T, P):
    """N₂+3H₂⇌2NH₃ 화학량론 공급(1:3)에서 평형 NH₃ 몰분율. P[atm].
    진행도 x∈(0,1): n_N2=1−x, n_H2=3−3x, n_NH3=2x, 총=4−2x.
    K = [y_NH3²/(y_N2·y_H2³)]·P^(−2) → 이분법으로 x 해."""
    K, _ = K_eq(T)

    def Qy(x):
        n = 4.0 - 2.0 * x
        yN2 = (1.0 - x) / n; yH2 = (3.0 - 3.0 * x) / n; yNH3 = 2.0 * x / n
        if yN2 <= 0 or yH2 <= 0:
            return float('inf')
        return yNH3 * yNH3 / (yN2 * yH2 ** 3)

    target = K * P * P                      # Qy(x) 가 맞춰야 할 값
    lo, hi = 1e-12, 1.0 - 1e-9
    for _ in range(200):                    # 결정론적 이분법
        mid = 0.5 * (lo + hi)
        if Qy(mid) < target:
            lo = mid
        else:
            hi = mid
    x = 0.5 * (lo + hi)
    return 2.0 * x / (4.0 - 2.0 * x), x


def sabatier(binding, optimum, scale):
    return math.exp(-abs(binding - optimum) / scale)


def main():
    print("=" * 72)
    print("비료의 화학 — 암모니아 합성 N₂ + 3H₂ ⇌ 2NH₃ (Haber-Bosch)")
    print("=" * 72)
    print("VP 두 기둥: 평형(ΔG=ΔH−TΔS, CH.8) + 촉매(d-밴드 화산, Stream C).")
    print(f"  ΔH°={DH/1000:.1f} kJ/mol(발열) · ΔS°={DS:.1f} J/mol·K(기체 4→2몰, 음수)")

    # ── [1] 평형: 왜 고압·중온인가 (Le Chatelier 정량) ──
    print("\n" + "─" * 72)
    print("[1] 평형 — 저온은 수율↑·속도0, 고온은 수율↓ → 절충 + 고압(Δn=−2) [F]")
    print("─" * 72)
    print(f"  {'T[K]':>6}{'T[°C]':>7}{'K(T)':>12}  평형 NH₃ 몰분율 @ 압력")
    print(f"  {'':>13}{'':>12}{'1 atm':>9}{'100 atm':>10}{'200 atm':>10}{'400 atm':>10}")
    for T in (298, 500, 600, 700, 800):
        K, _ = K_eq(T)
        y1, _ = equil_NH3_fraction(T, 1.0)
        y100, _ = equil_NH3_fraction(T, 100.0)
        y200, _ = equil_NH3_fraction(T, 200.0)
        y400, _ = equil_NH3_fraction(T, 400.0)
        print(f"  {T:>6}{T-273:>7}{K:>12.2e}{y1*100:>8.1f}%{y100*100:>9.1f}%"
              f"{y200*100:>9.1f}%{y400*100:>9.1f}%")
    print("  → 저온(298K): 평형은 거의 완전(수율 높음)이나 N₂ 불활성 → 속도≈0(촉매로도 너무 느림).")
    print("    고온(800K): 속도는 충분하나 평형 수율 급락. 압력↑이 Δn=−2 로 수율 회복.")
    print("    ⇒ 산업 조건 ≈ 450°C / 150–300 atm / Fe 촉매 — 셋의 강제된 절충.")
    # 검증: 발열+Δn<0 → 온도↑면 수율↓, 압력↑면 수율↑
    yA, _ = equil_NH3_fraction(700, 200.0); yB, _ = equil_NH3_fraction(800, 200.0)
    yC, _ = equil_NH3_fraction(700, 400.0)
    assert yA > yB, "Le Chatelier 위반: 발열인데 고온서 수율↑"
    assert yC > yA, "Le Chatelier 위반: Δn<0 인데 고압서 수율↓"

    # ── [2] 임계온도: 평형 역전 ──
    print("\n" + "─" * 72)
    print("[2] 임계온도 — ΔG=0 넘으면 평형이 생성물에서 멀어진다 [F]")
    print("─" * 72)
    T_flip = DH / DS                        # ΔG=ΔH−TΔS=0 → T=ΔH/ΔS
    K_flip, _ = K_eq(T_flip)
    print(f"  ΔG°(T) = ΔH − TΔS = 0  ⇒  T* = ΔH/ΔS = {T_flip:.0f} K ({T_flip-273:.0f}°C)")
    print(f"  T<{T_flip:.0f}K: ΔG<0 (정반응 선호) · T>{T_flip:.0f}K: ΔG>0 (역반응 선호, K<1)")
    print(f"  검증: K({T_flip:.0f}K)={K_flip:.3f} ≈ 1.0 (전환점).")
    assert abs(K_flip - 1.0) < 0.05, "임계온도서 K≈1 아님"
    print("  → 무한정 가열 불가. 이 상한이 '고압·촉매' 조합을 강제하는 근본 이유.")

    # ── [3] 율속 장벽: N≡N 해리 ──
    print("\n" + "─" * 72)
    print("[3] 율속 장벽 — N≡N(가장 강한 결합)의 해리가 율속 → 촉매 필수 [F]")
    print("─" * 72)
    dH_check = (BOND_NN + 3 * BOND_HH) - 6 * BOND_NH   # 결합에너지로 ΔH 점검
    print(f"  결합: N≡N={BOND_NN} · H–H={BOND_HH} · N–H={BOND_NH} kJ/mol")
    print(f"  결합기준 ΔH ≈ (N≡N + 3·H–H) − 6·N–H = {dH_check:+.0f} kJ/mol (발열, 실측 −92 와 부호·규모 일치)")
    print(f"  N≡N {BOND_NN}kJ/mol = 해리 최대 장벽. 비촉매 균일해리는 사실상 불가 →")
    print(f"  촉매 표면이 N₂를 흡착·해리(Ea 낮춤)해야만 반응 진행. 촉매 선택이 핵심.")
    assert dH_check < 0, "결합 기준 ΔH 가 발열이 아님"

    # ── [4] 촉매 화산: 왜 Fe/Ru 인가 ──
    print("\n" + "─" * 72)
    print("[4] 촉매 화산 — N 결합세기 descriptor, 정점 Fe/Ru (d-밴드/Stream C 연결) [F?]")
    print("─" * 72)
    print(f"  Sabatier: 너무 강(Mo·W)하면 N 갇혀 NH₃ 못 떼고, 너무 약(Ni·Pt)하면 N₂ 해리 못함.")
    print(f"  최적 E_N≈{E_N_OPT}eV 에서 정점.")
    scale = 0.45
    rows = [(n, en, sabatier(en, E_N_OPT, scale)) for n, en in NITROGEN]
    rows.sort(key=lambda x: -x[2]); amax = max(x[2] for x in rows)
    print(f"  {'금속':<5}{'E_N[eV]':>9}{'상대활성':>9}  막대   비고")
    for n, en, act in rows:
        note = "너무 강" if en < -0.85 else ("너무 약" if en > 0.2 else
               ("← 산업 촉매" if act > 0.78 else ""))
        print(f"  {n:<5}{en:>+9.2f}{act:>9.3f}  {'█'*int(20*act/amax):<20} {note}")
    top3 = [rows[i][0] for i in range(3)]
    assert rows[0][0] in ("Fe", "Ru", "Os"), f"정점 재현 실패: {rows[0][0]}"
    assert "Fe" in top3 and "Ru" in top3, "Fe·Ru 상위3 아님"
    print(f"  → 정점권 = {top3}. Fe(Haber-Bosch, 저렴)·Ru(2세대, 고활성) 산업 촉매 재현.")
    print("    이 화산은 격자기하가 아니라 *d-밴드 에너지*가 N 결합을 정함에서 나온다(Stream C).")

    # ── 결론 + 등급 ──
    print("\n" + "=" * 72)
    print("결론 — 비료(암모니아)는 평형 + d-밴드 촉매로 완성된다")
    print(f"  ① 평형: 발열+Δn=−2 → 저온수율↑/고온속도↑ 상충 → 고압 절충(정량 재현)")
    print(f"  ② 임계 T*={T_flip:.0f}K 가 가열 상한을 강제 → 촉매 필수")
    print(f"  ③ N≡N {BOND_NN}kJ/mol 해리가 율속 → 촉매 표면이 장벽 낮춤")
    print(f"  ④ N 결합 화산 정점 Fe/Ru 재현 — d-밴드 에너지 공명(Stream C)과 한 줄기")
    print("-" * 72)
    print("등급: [F] 평형 방향·Le Chatelier·임계온도·결합에너지 ΔH 부호 ·")
    print("      [F?] 촉매 화산 정점 식별 · [CAL] ΔH,ΔS,E_N,결합에너지 ·")
    print("      [O] 절대 반응속도·촉진제(K₂O·Al₂O₃) 효과·표면 미세동역학")
    print("반증가능 예측: 발열 평형은 고온서 수율↓·고압서 수율↑; 촉매 정점은 E_N≈−0.5(Fe/Ru).")
    print("  이 추세가 깨지면 평형/화산 그림은 폐기된다.")
    print("=" * 72)


if __name__ == "__main__":
    main()
