# -*- coding: utf-8 -*-
"""
vp_molecular_color.py — 분자의 색 유도: 물감·염료·착물색 (재현가능)
====================================================================
빛/EM 장(빛=횡파 χ→90°, λ↔E)·결정장 장(d-d 전이, vp_crystal_field) 위에 섭니다.

핵심 원리: 색 = 분자의 전자구조가 *가시광 일부를 선택 흡수*. 흡수된 광자(횡파 빛)는
          전자를 *전자 간극(gap)* 너머로 들뜸. 간극 크기 → 흡수 λ → 관측색.
          (흡수형: 보색이 보임 / 반사형 안료: 반사대가 보임)

색의 네 메커니즘 (모두 '간극을 넘는 전자 들뜸'):
  ① d-d 전이      — 전이금속 착물. 결정장 Δ → λ (vp_crystal_field). 보석·착물색.
  ② 공액 π (FEM)  — 유기염료. HOMO-LUMO 간극 ∝(N+1)/L². 길수록 적색이동(UV→가시).
  ③ 띠틈 band gap — 무기안료(물감!). λ_edge=hc/E_g. 흰색→노랑→빨강→검정 연속.
  ④ 전하이동 CT   — 강렬한 색(과망간산 등). 허용전이라 진함.

자체검증(assert)·표준라이브러리·결정론. 실행: python3 vp_molecular_color.py
"""
import math

H    = 6.62607015e-34
HBAR = H/(2*math.pi)
ME   = 9.1093837015e-31
C    = 2.99792458e8
EV   = 1.602176634e-19

def photon_lambda(E_eV):
    """광자 에너지 → 파장 [nm]. λ = hc/E."""
    return H*C/(E_eV*EV)*1e9

def photon_energy(lam_nm):
    """파장 → 광자 에너지 [eV]."""
    return H*C/(lam_nm*1e-9)/EV


# ── 보색: 흡수 파장 → 관측색 (흡수형: d-d, 염료) ──
def complementary_color(lam_abs_nm):
    """흡수 파장 → 관측색(보색). 가시광 밖이면 무색/검정 판정."""
    if lam_abs_nm < 400:  return "무색(UV흡수, 가시광 통과)"
    if lam_abs_nm > 700:  return "무색(IR흡수, 가시광 통과)"
    table = [
        (400, 430, "보라",   "황록"),
        (430, 490, "파랑",   "주황"),
        (490, 510, "청록",   "빨강"),
        (510, 530, "초록",   "자홍"),
        (530, 560, "황록",   "보라"),
        (560, 580, "노랑",   "남색"),
        (580, 620, "주황",   "파랑"),
        (620, 700, "빨강",   "초록"),
    ]
    for lo, hi, absorbed, perceived in table:
        if lo <= lam_abs_nm < hi:
            return f"{perceived}(흡수={absorbed})"
    return "?"


# ── 띠틈: 밴드갭 에너지 → 안료 반사색 (반사형: 무기안료/물감) ──
def bandgap_color(Eg_eV):
    """밴드갭 → 흡수단 λ_edge=hc/E_g, 반사색(λ>edge). 흰→노랑→빨강→검정."""
    edge = photon_lambda(Eg_eV)   # nm; 이보다 짧은 λ 흡수, 긴 λ 반사
    if edge < 400:   color = "흰색(가시광 전부 반사)"
    elif edge < 430: color = "연노랑(보라만 흡수)"
    elif edge < 490: color = "노랑(보라·파랑 흡수)"
    elif edge < 560: color = "주황(초록까지 흡수)"
    elif edge < 620: color = "빨강(노랑까지 흡수)"
    elif edge < 700: color = "진빨강(주황까지 흡수)"
    else:            color = "검정(가시광 전부 흡수)"
    return edge, color


# ── 공액 π 자유전자모형(FEM): HOMO-LUMO 간극 → λ ──
def fem_polyene(k, d_CC=1.4e-10):
    """
    공액 폴리엔(C=C k개): π전자 N=2k, 상자길이 L=(2k+1)·d_CC (말단 넘침 +1).
    HOMO=준위k, LUMO=k+1. ΔE=(h²/8m_eL²)[(k+1)²−k²]=(h²/8m_eL²)(2k+1)=(N+1)항.
    λ=hc/ΔE. 길수록(k↑) 간극↓ → λ↑ (UV→가시 적색이동).
    """
    N = 2*k
    L = (2*k + 1)*d_CC
    dE = (H*H/(8*ME*L*L))*(N + 1)      # J
    dE_eV = dE/EV
    lam = photon_lambda(dE_eV)
    return N, L, dE_eV, lam


def main():
    print("="*72)
    print("분자의 색 유도 — 물감·염료·착물색 (색 = 전자가 간극을 넘는 들뜸)")
    print("="*72)
    print("원리: 가시광(횡파 빛, 400~700nm)의 일부를 전자구조가 흡수 → 전자를 간극 너머 들뜸.")
    print("      간극 크기 → 흡수 λ → 관측색. 흡수형=보색 보임, 반사형 안료=반사대 보임.")
    print(f"  광자: λ[nm]=1240/E[eV].  가시광 E: {photon_energy(700):.2f}eV(빨강)~{photon_energy(400):.2f}eV(보라)")

    # ── ① d-d 전이 (결정장) ──
    print("\n" + "─"*72)
    print("[① d-d 전이] 전이금속 착물 — 결정장 Δ → 흡수 λ → 보색 (vp_crystal_field)")
    print("─"*72)
    print(f"  메커니즘: λ_흡수[nm]=10⁷/Δ[cm⁻¹]. d-궤도가 리간드 EM 1/r²장에 갈라짐(Δ).")
    print(f"  {'착물':<18}{'Δ[cm⁻¹]':>9}{'λ흡수[nm]':>10}{'관측색(모형)':>16}{'실제':>8}")
    print("  "+"-"*61)
    dd = [("[Ti(H2O)6]³⁺ d¹",20300,"적자"),("[Cr(H2O)6]³⁺ d³",17400,"청자"),
          ("[Co(H2O)6]²⁺ d⁷",19400,"분홍"),("[Cu(H2O)6]²⁺ d⁹",12600,"청"),
          ("[Ni(H2O)6]²⁺ d⁸",8500,"녹")]
    for name, delta, real in dd:
        lam = 1e7/delta
        col = complementary_color(lam)
        if lam > 700:
            col = f"(단일Δ한계)"   # d⁹·d⁸ 다중띠 → 단일점 모형 불충분
        print(f"  {name:<18}{delta:>9}{lam:>10.0f}{col:>16}{real:>8}")
    print("  → d¹(Ti)은 단일전이라 모형 정확. d⁹·d⁸(Cu·Ni)는 넓은 다중띠가")
    print("    가시 적색까지 꼬리 → 실제 청·녹. 단일 Δ점 모형의 한계(정밀색 [O]).")
    print("    메커니즘 [F](VP 기하, Δ가 가시광이면 색), 분광화학계열 [CAL].")
    assert 480 < 1e7/20300 < 500, "Ti 착물 흡수파장 오류"

    # ── ② 공액 π (FEM) ──
    print("\n" + "─"*72)
    print("[② 공액 π계] 유기염료 — HOMO-LUMO 간극 ∝(N+1)/L², 길수록 적색이동")
    print("─"*72)
    print(f"  자유전자모형: ΔE=(h²/8m_eL²)(N+1), N=2k π전자, L∝공액길이. 길수록 간극↓.")
    print(f"  {'폴리엔(C=C수 k)':<16}{'N':>4}{'FEM λ[nm]':>10}{'실측 λ[nm]':>11}{'영역(실측)':>12}")
    print("  "+"-"*54)
    # 실측 흡수 최대 (UV-vis), [CAL]
    obs = {1:165, 2:217, 3:258, 4:304, 5:334, 11:450}
    prev_lam = 0
    for k, name in [(1,"에텐 k=1"),(2,"부타디엔 k=2"),(3,"헥사트리엔 k=3"),
                    (4,"옥타테트라엔 k=4"),(5,"k=5"),(11,"β-카로틴 k=11")]:
        N, L, dE, lam = fem_polyene(k)
        o = obs[k]
        region = "자외선(무색)" if o < 400 else "가시광(유색)"
        print(f"  {name:<16}{N:>4}{lam:>10.0f}{o:>11}{region:>12}")
        assert lam > prev_lam, "FEM: 공액 길수록 λ 증가 위배"
        prev_lam = lam
    print("  → 실측: 짧은 공액(에텐~옥타테트라엔)=자외선=무색, 긴 공액(β-카로틴)=가시=유색.")
    print("    FEM은 *추세*(간극∝(N+1)/L² → 적색이동, UV→가시)를 옳게 줌. [F] 스케일.")
    print("    절대값은 긴 사슬서 과대(결합교대가 간극을 가둠) → FEM λ는 추세용 [F?].")
    print("    당근(β-카로틴 k=11)·토마토(리코펜 k=11)=긴 공액 → 청색흡수 → 주황·빨강. [F?]")

    # ── ③ 띠틈 (무기안료 = 물감) ──
    print("\n" + "─"*72)
    print("[③ 띠틈 band gap] 무기안료(물감!) — λ_edge=hc/E_g, 흰→노랑→빨강→검정 연속")
    print("─"*72)
    print(f"  반도체 안료: 광자E>E_g(λ<edge) 흡수, E<E_g(λ>edge) 반사. 반사대가 색.")
    print(f"  {'안료':<22}{'E_g[eV]':>8}{'흡수단[nm]':>11}{'반사색(관측)':>18}")
    print("  "+"-"*59)
    pigments = [
        ("TiO₂ 티탄백",        3.05),
        ("ZnO 아연백",         3.20),
        ("As₂S₃ 웅황(orpiment)",2.70),
        ("CdS 카드뮴옐로",      2.42),
        ("PbCrO₄ 크롬옐로",     2.30),
        ("CdS·Se 카드뮴오렌지", 2.10),
        ("HgS 주색(버밀리언)",  2.00),
        ("Fe₂O₃ 적철석(적황토)",2.10),
        ("CdSe 카드뮴레드",     1.73),
        ("탄소 카본블랙",       0.50),
    ]
    for name, Eg in pigments:
        edge, col = bandgap_color(Eg)
        print(f"  {name:<22}{Eg:>8.2f}{edge:>11.0f}{col:>18}")
    print("  → E_g 큰(>3.1eV) 안료=흰색(가시 전부 반사). 작은(<1.8eV)=검정. 사이=유색.")
    print("    E_g 줄이면 흰→노랑→주황→빨강→검정 *연속 이동* — 카드뮴 안료 계열이 실증.")
    print("    역사적 안료(버밀리언·웅황·적철석)도 같은 띠틈 규칙. [F] 규칙, E_g는 [CAL].")
    # 검증: 카드뮴 계열 단조 이동
    e_ti,_ = bandgap_color(3.05); e_cds,_ = bandgap_color(2.42); e_cdse,_ = bandgap_color(1.73)
    assert e_ti < e_cds < e_cdse, "띠틈 작을수록 흡수단 길어짐 위배"
    assert e_ti < 410 and e_cdse > 700, "TiO2 흰색·CdSe 빨강 경계 오류"

    # ── ④ 전하이동 (CT) ──
    print("\n" + "─"*72)
    print("[④ 전하이동 CT] 강렬한 색 — 금속↔리간드 전자이동(허용전이라 진함)")
    print("─"*72)
    print("  과망간산 MnO₄⁻: O→Mn 전하이동 ~525nm 흡수 → 진보라. (d-d보다 100~1000배 진함)")
    print("  중크롬산 Cr₂O₇²⁻: O→Cr CT → 주황. 프러시안블루: Fe²⁺↔Fe³⁺ CT → 진청.")
    print("  → CT는 허용전이라 흡광계수 큼 → 소량으로도 진한 색. 메커니즘=전자가 간극 넘음.")
    mno4 = complementary_color(525)
    print(f"  검증: 525nm 흡수 → {mno4} (과망간산 진보라와 일치).")

    # ── VP 통일 ──
    print("\n" + "─"*72)
    print("[VP 통일] 색 = 횡파 광자가 전자 간극에서 흡수")
    print("─"*72)
    print("  • 흡수하는 빛 = 횡파 EM(χ→90°, 가시광). 간극에 맞는 광자만 흡수(공명).")
    print("  • 간극의 기원: d-d=결정장(EM 1/r²)·π계=공액길이·안료=띠틈·CT=금속↔리간드.")
    print("  • 모두 '전자가 간극(gap)을 넘는 들뜸'. 간극→λ→색. 하나의 원리, 네 발현.")
    print("  • 흰색=간극>가시(흡수없음·전부반사), 검정=간극<가시(전부흡수). 색=그 사이.")

    print("\n" + "="*72)
    print("분자의 색 유도 요약:")
    print("  ① d-d 전이: 결정장 Δ → λ → 보색 (착물·보석)")
    print("  ② 공액 π: 간극∝(N+1)/L², 길수록 적색이동 (UV→가시) = 유기염료·카로틴")
    print("  ③ 띠틈: λ_edge=hc/E_g, 흰→노랑→빨강→검정 (무기안료=물감)")
    print("  ④ 전하이동: 허용전이 진한 색 (과망간산 등)")
    print("  → 색 = 횡파 광자가 전자 간극에서 흡수. 간극 크기가 색을 정한다.")
    print("등급: [F] 색=간극들뜸·보색·띠틈규칙·d-d기하 · [CAL] Δ,E_g,분광계열 · [F?] FEM값 · [O] 다중전자 정밀색")
    print("="*72)


if __name__ == "__main__":
    main()
