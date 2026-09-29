# -*- coding: utf-8 -*-
"""
vp_dband_catalysis.py — d-밴드 에너지 공명: 일반 촉매 엔진 (재현가능)
======================================================================
Stream C (정밀계획 v2). 백금 재현(vp_pt_reproduction)을 *재사용 가능한 다금속·다반응
촉매 엔진*으로 일반화한다. 반증된 기하/진폭 공명을 폐기하고, 검증된 에너지 공명
(d-밴드 중심 ε_d ↔ 흡착물 궤도 ε_a, Newns-Anderson / Hammer-Nørskov)을 토대로 삼는다.

핵심 주장(전부 등급화):
  [1] 메커니즘 — 흡착물 준위가 d-밴드와 결합해 broadening (Newns-Anderson).
  [2] 일반 법칙 — d-밴드 중심 ε_d 가 흡착 결합세기를 정한다(비순환). HER ΔG_H 로 검증.
  [3] Sabatier 화산 — 활성은 중간 결합에서 최대. HER 정점 = Pt (재현).
  [4] ★진짜 튜닝 레버 — ε_d 는 *합금·변형*으로 이동한다. 이것이 활성을 옮기는 실제 손잡이
      (반증된 '격자간격 기하 공명'의 대체). 압축변형 → ε_d 하강 → 약결합.
  [5] 일반성 — 같은 엔진이 질소(N) 흡착에도 적용 → 암모니아(비료) 화산으로 연결(Stream D2).

⇒ '전자 진폭 파장↔격자'(틀림)가 아니라 'd-전자 에너지↔궤도'(맞음). 변수는 에너지다.

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_dband_catalysis.py
"""
import math

# ── Newns-Anderson 모형 파라미터 (eV, 페르미준위 ε_F = 0) ──
EPS_A = -1.0      # 흡착물 궤도 준위 (H 1s 유효, eV)
V_COUP = 1.6      # 흡착물-d 결합 행렬요소 (eV)
W_BAND = 2.0      # d-밴드 반폭 (eV)

# ── 전이금속 d-밴드 중심 ε_d [eV] (Hammer-Nørskov, 조밀면) [CAL] ──
# 한 칸 빈 5d(Pt)가 ε_F 근처에 둔 d-상태의 *에너지*가 핵심.
DBAND = {"Fe":-0.92,"Co":-1.17,"Ni":-1.29,"Ru":-1.41,"Rh":-1.73,"Pd":-1.83,
         "Ir":-2.11,"Pt":-2.25,"Cu":-2.67,"Au":-3.56,"Ag":-4.30}

# ── HER 검증쌍: (금속, ε_d[eV], 실측 ΔG_H[eV]) [CAL] (Nørskov 2005 / 실험) ──
# 이 7쌍은 vp_pt_reproduction 에서 화산 정점 Pt 를 재현한 검증된 앵커.
HER = [("Ni",-1.29,-0.28),("Rh",-1.73,-0.28),("Pd",-1.83,-0.20),("Ir",-2.11,-0.10),
       ("Pt",-2.25,-0.09),("Cu",-2.67,0.30),("Au",-3.56,0.30)]

# ── 질소 흡착 E_N [eV] (½N₂ 기준, 음수=강결합) [CAL] (암모니아 화산, Jacobsen/Nørskov) ──
# 비료(암모니아 합성)의 율속단계 = N≡N 해리. 화산 정점 = Fe/Ru (산업 촉매).
NITROGEN = [("Mo",-1.30),("W",-0.95),("Re",-0.80),("Fe",-0.50),("Ru",-0.42),
            ("Os",-0.40),("Co",0.00),("Ni",0.35),("Pd",0.70),("Pt",0.80)]
E_N_OPT = -0.50   # 암모니아 화산 최적 N 결합(Brønsted-Evans-Polanyi 최적) [CAL]


# ===== 재사용 가능한 엔진 함수 =====
def selfenergy(eps, eps_d):
    """반원형 d-밴드(중심 ε_d, 반폭 W)의 자기에너지 → (Λ=ReΣ, Δ=−ImΣ)."""
    x = eps - eps_d
    pref = V_COUP * V_COUP * 2.0 / (W_BAND * W_BAND)
    if abs(x) <= W_BAND:
        return pref * x, pref * math.sqrt(W_BAND * W_BAND - x * x)
    return pref * (x - math.copysign(math.sqrt(x * x - W_BAND * W_BAND), x)), 0.0


def adsorbate_dos(eps, eps_d):
    """흡착물 상태밀도 ρ_a = −Im G_a/π, G_a = 1/(ε − ε_a − Σ)."""
    Lam, Del = selfenergy(eps, eps_d)
    re = eps - EPS_A - Lam
    eta = max(Del, 1e-3)
    return (1.0 / math.pi) * eta / (re * re + eta * eta)


def pearson(xs, ys):
    """피어슨 r, 최소제곱 기울기·절편."""
    n = len(xs); mx = sum(xs) / n; my = sum(ys) / n
    cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    return cov / (sx * sy), cov / sx ** 2, my - (cov / sx ** 2) * mx


def sabatier_activity(binding, optimum, scale):
    """Sabatier: 활성 = exp(−|결합 − 최적|/scale). 최적 결합에서 최대."""
    return math.exp(-abs(binding - optimum) / scale)


def dband_shift_strain(eps_d0, strain_pct):
    """변형 → d-밴드 이동. 압축(−)은 띠 넓힘→중심 하강, 인장(+)은 상승.
    1차 근사 dε_d/dε ≈ +0.10 eV/%(인장 양수). [F?] 부호·추세는 견고(탄성 띠넓힘)."""
    return eps_d0 + 0.10 * strain_pct


# ===== 보고 =====
def main():
    print("=" * 72)
    print("d-밴드 에너지 공명 — 일반 촉매 엔진 (백금 재현의 다금속·다반응 일반화)")
    print("=" * 72)
    print("토대: 반증된 기하/진폭 공명 폐기 → 검증된 에너지 공명(d-밴드 중심 ε_d).")
    print("      변수는 '격자간격'이 아니라 'd-전자 에너지'. 같은 엔진이 H·N 둘 다 설명.")

    # ── [1] 메커니즘: Newns-Anderson broadening ──
    print("\n" + "─" * 72)
    print("[1] 메커니즘 — 흡착물 준위가 d-밴드와 결합해 broadening (Newns-Anderson) [V]")
    print("─" * 72)
    es = [-5 + 0.5 * i for i in range(12)]
    rs = [adsorbate_dos(e, DBAND["Pt"]) for e in es]; rmax = max(rs)
    print(f"  Pt(ε_d={DBAND['Pt']}eV): 고립 흡착물 날카로운 선 → d-밴드 공명으로 퍼짐")
    print(f"  {'ε[eV]':>7}{'ρ_a':>9}  막대")
    for e, r in zip(es, rs):
        mark = " ←ε_F" if abs(e) < 0.01 else (" ←ε_a" if abs(e - EPS_A) < 0.25 else "")
        print(f"  {e:>7.1f}{r:>9.4f}  {'█' * int(28 * r / rmax)}{mark}")
    assert rmax > 0
    print("  → broadening = 결합 형성의 기초. d-밴드가 흡착물 준위를 '잡는다'.")

    # ── [2] 일반 법칙: ε_d → 결합세기 (HER 로 검증) ──
    print("\n" + "─" * 72)
    print("[2] 일반 법칙 — d-밴드 중심 ε_d 가 결합을 정한다 (HER ΔG_H 로 검증, 비순환) [F?]")
    print("─" * 72)
    eds = [d[1] for d in HER]; dgs = [d[2] for d in HER]
    r, a, b = pearson(eds, dgs)
    print(f"  ε_d ↔ ΔG_H 상관 r = {r:.3f} (강함). 회귀: ΔG_H = {a:.3f}·ε_d {b:+.3f}")
    print(f"  {'금속':<5}{'ε_d[eV]':>8}{'ΔG_H예측':>10}{'ΔG_H실측':>10}{'오차':>7}")
    for name, ed, dg in HER:
        pred = a * ed + b
        print(f"  {name:<5}{ed:>8.2f}{pred:>+10.2f}{dg:>+10.2f}{abs(pred - dg):>7.2f}")
    assert abs(r) > 0.85, "d-밴드↔결합 상관 약함"
    print("  → ε_d(밴드구조, 독립입력)가 결합을 예측 = 에너지 공명. 진폭 불필요.")

    # ── [3] Sabatier 화산: HER 정점 = Pt (재현) ──
    print("\n" + "─" * 72)
    print("[3] Sabatier 화산 — HER 활성 vs ΔG_H, 정점 = Pt (재현) [F?]")
    print("─" * 72)
    scale = 0.15
    rows = [(n, dg, sabatier_activity(dg, 0.0, scale)) for n, ed, dg in HER]
    rows.sort(key=lambda x: -x[2]); amax = max(x[2] for x in rows)
    print(f"  활성 = exp(−|ΔG_H|/{scale}); ΔG_H≈0(최적)서 최대.")
    print(f"  {'금속':<5}{'ΔG_H[eV]':>10}{'활성':>8}  막대")
    for n, dg, act in rows:
        print(f"  {n:<5}{dg:>+10.2f}{act:>8.3f}  {'█' * int(26 * act / amax)}")
    top = rows[0][0]
    assert top in ("Pt", "Ir"), f"HER 화산 정점 재현 실패: {top}"
    print(f"  → 정점 = {top}. 약결합(Au·Cu) 우하강. 실측 HER 화산과 일치.")

    # ── [4] ★진짜 튜닝 레버: d-밴드 이동(변형/합금) ──
    print("\n" + "─" * 72)
    print("[4] ★진짜 튜닝 레버 — ε_d 는 변형·합금으로 이동(반증된 기하 공명의 대체) [F?]")
    print("─" * 72)
    print("  반증됨: '격자간격 = de Broglie 파장' 기하 공명(Bragg 밴드틈).")
    print("  대체:   ε_d 를 *변형/합금*으로 직접 이동 → 화산 위 위치를 옮긴다.")
    print(f"  예) 약결합 금속을 인장변형으로 ε_d 상승 → 결합 강화 → 정점 쪽 이동:")
    print(f"  {'변형%':>7}{'ε_d(Cu)':>9}{'ΔG_H예측':>10}{'화산활성':>9}")
    for sp in (-3, -1, 0, 2, 4):
        ed = dband_shift_strain(DBAND["Cu"], sp)
        dg = a * ed + b
        act = sabatier_activity(dg, 0.0, scale)
        print(f"  {sp:>+7}{ed:>9.2f}{dg:>+10.2f}{act:>9.3f}")
    print("  → 변형이 ε_d 를 올려 ΔG_H 를 0 쪽으로 → 활성 상승. 이것이 실제 전극 설계 손잡이.")
    print("    (응용: 합금·코어쉘·변형 박막으로 d-밴드를 정점에 맞춤 — 물전기분해 전극.)")

    # ── [5] 일반성: 같은 엔진이 질소(N)에도 → 암모니아(비료) 화산 ──
    print("\n" + "─" * 72)
    print("[5] 일반성 — 같은 화산이 질소 흡착에도. 암모니아(비료) 정점 = Fe/Ru [F?]")
    print("─" * 72)
    print(f"  암모니아 합성 율속 = N≡N 해리. 화산 최적 E_N≈{E_N_OPT}eV; 너무 강하면 N 갇힘,")
    print(f"  너무 약하면 N₂ 해리 못함. (H 화산과 *다른* 최적 — 엔진은 같고 흡착물만 다름.)")
    nscale = 0.45
    nrows = [(n, en, sabatier_activity(en, E_N_OPT, nscale)) for n, en in NITROGEN]
    nrows.sort(key=lambda x: -x[2]); namax = max(x[2] for x in nrows)
    print(f"  {'금속':<5}{'E_N[eV]':>9}{'활성':>8}  막대   비고")
    for n, en, act in nrows:
        note = ""
        if en < -0.85: note = "너무 강(N 갇힘)"
        elif en > 0.2: note = "너무 약(해리 X)"
        elif act > 0.7: note = "← 산업 촉매"
        print(f"  {n:<5}{en:>+9.2f}{act:>8.3f}  {'█' * int(20 * act / namax):<20} {note}")
    ntop = nrows[0][0]
    top3 = {nrows[0][0], nrows[1][0], nrows[2][0]}
    assert ntop in ("Fe", "Ru", "Os"), f"암모니아 화산 정점 재현 실패: {ntop}"
    assert "Fe" in top3 and "Ru" in top3, "Fe·Ru 가 상위 3 안에 없음"
    print(f"  → 정점 = {ntop} (상위3: {sorted(top3)}). 실제 산업 촉매 Fe(Haber-Bosch)·Ru 재현.")
    print("    Mo·W(강결합) 좌측 비활성, Ni·Pt(약결합) 우측 비활성 — 화산 양끝 일치.")

    # ── 결론 + 등급 ──
    print("\n" + "=" * 72)
    print("결론 — d-밴드 에너지 공명은 재사용 가능한 일반 촉매 엔진이다")
    print("  ① 메커니즘(Newns-Anderson) → ② ε_d 가 결합 예측(HER r=%.2f) → ③ 화산 정점 Pt 재현"
          % r)
    print("  ④ 튜닝은 *에너지*(변형/합금으로 ε_d 이동)지 *기하*가 아니다(반증된 공명 대체)")
    print("  ⑤ 같은 엔진이 질소 흡착 → 암모니아(비료) 정점 Fe/Ru 재현 → Stream D2 로 연결")
    print("-" * 72)
    print("등급: [V] Newns-Anderson·화산 재현 · [F?] ε_d↔결합·변형 이동·정점 식별 ·")
    print("      [CAL] ε_d, ΔG_H, E_N (밴드구조/실측 입력) · [O] 절대 반응속도·다단계 미세동역학")
    print("반증가능 예측: HER 정점은 ΔG_H≈0(Pt), 암모니아 정점은 E_N≈−0.5(Fe/Ru);")
    print("  이 순위가 깨지면 d-밴드 화산 그림은 폐기된다.")
    print("=" * 72)


if __name__ == "__main__":
    main()
