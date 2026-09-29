# -*- coding: utf-8 -*-
"""
vp_iron_magnetism.py — 철의 자성 원리: 왜 Fe인가 (Cu도 Mn도 아닌 이유) (재현가능)
==================================================================================
물리백서 §14(자성=정렬 회전, ∇·B=0, '왜 Fe이고 Cu가 아닌가'는 입력으로 남김) 확장.
본 모듈은 그 *입력으로 남긴 강자성 판정기준*을 두 조건으로 도출한다.

VP 그림: 자기 모멘트 = 짝없는 전자의 *회전*(전하=회전(EM.1)·헬리시티=회전(EM.5)과 동일).
강자성(영구자석)이 되려면 두 조건이 모두 필요:
  조건 1 — 국소 모멘트: 미충전 d껍질의 짝없는 d전자 (Hund 규칙). 회전이 상쇄 안 됨.
  조건 2 — 양의 교환: 이웃 d-회전이 *나란히* 정렬해야(강자성) vs 반대정렬(반강자성).
            Bethe-Slater: 비율 D/d(원자간거리/d궤도지름)가 임계(~1.5) 위면 J>0.

왜 갈리는가:
  • Cu [Ar]3d¹⁰4s¹: 3d 완전충전 → 짝없는 d전자 0 → 모멘트 없음. *조건1 실패* → 자성 없음.
                    (4s¹은 자유전자=전도, 국소모멘트 아님 → 구리는 전도체, vp_copper_conduction)
  • Mn [Ar]3d⁵4s²: 짝없는 5개(Fe보다 많음!)나 D/d<1.5 → J<0 → *조건2 실패* → 반강자성.
  • Fe·Co·Ni: 짝없는 d전자 있고 D/d>1.5 → J>0 → 두 조건 충족 → 강자성.

자체검증(assert)·표준라이브러리·결정론. 실행: python3 vp_iron_magnetism.py
"""
import math

MU_B = 9.2740100783e-24   # 보어 마그네톤 [J/T]
KB   = 1.380649e-23

# 3d 전이금속 (배치·Bethe-Slater 비율·퀴리/네엘온도) — D/d, T는 측정 [CAL]
# d_unpaired: d껍질 짝없는 전자수(Hund). ds_ratio: Bethe-Slater D/d. order: 자성 분류.
ELEMENTS = [
    # Z, 기호, d전자수, 4s,  D/d비,  T_order[K], 실측분류
    (24, "Cr", 5, 1, 1.18,  311, "반강자성"),   # 3d⁵4s¹ 예외
    (25, "Mn", 5, 2, 1.47,  100, "반강자성"),   # 3d⁵4s²
    (26, "Fe", 6, 2, 1.63, 1043, "강자성"),     # 3d⁶4s²
    (27, "Co", 7, 2, 1.82, 1388, "강자성"),     # 3d⁷4s²
    (28, "Ni", 8, 2, 1.98,  627, "강자성"),     # 3d⁸4s²
    (29, "Cu", 10, 1, None, None, "비자성"),    # 3d¹⁰4s¹ 예외
    (30, "Zn", 10, 2, None, None, "비자성"),    # 3d¹⁰4s²
]
DS_CRIT = 1.5   # Bethe-Slater 교환부호 임계 D/d (이상=강자성 J>0)

# 금속 실측 모멘트 [μ_B] (띠/편력 효과로 비정수 — [CAL]/[O])
METALLIC_MOMENT = {"Fe": 2.22, "Co": 1.72, "Ni": 0.62}


def d_unpaired(nd):
    """3d^nd 의 짝없는 d전자수 (Hund 규칙): nd≤5면 nd, 아니면 10−nd."""
    return nd if nd <= 5 else 10 - nd

def spin_only_moment(n_unpaired):
    """스핀전용 자기모멘트 μ = √(n(n+2)) μ_B (국소/이온 그림)."""
    return math.sqrt(n_unpaired*(n_unpaired+2))

def exchange_sign(ds_ratio):
    """Bethe-Slater: D/d > 임계면 교환 J>0 (강자성), 아니면 J<0 (반강자성)."""
    if ds_ratio is None:
        return 0      # 모멘트 없음 → 교환 무의미
    return +1 if ds_ratio > DS_CRIT else -1

def predict_class(nd, ds_ratio):
    """두 조건으로 자성 분류 도출."""
    nu = d_unpaired(nd)
    if nu == 0:
        return "비자성", "조건1 실패(짝없는 d전자 0)"
    j = exchange_sign(ds_ratio)
    if j > 0:
        return "강자성", "조건1·2 충족(모멘트 + J>0)"
    else:
        return "반강자성", "조건2 실패(J<0, D/d<임계)"


def main():
    print("="*72)
    print("철의 자성 원리 — 왜 Fe인가 (Cu도 Mn도 아닌 이유)")
    print("="*72)
    print("자기 모멘트 = 짝없는 전자의 회전 (전하=회전·헬리시티=회전과 동일 회전).")
    print("강자성 두 조건: ① 미충전 d껍질의 짝없는 d전자(국소 모멘트) ② 양의 교환 J>0.")
    print(f"Bethe-Slater 임계: D/d > {DS_CRIT} 이면 J>0(강자성), 미만이면 J<0(반강자성).")

    # ── 1. 조건 1: 짝없는 d전자 (모멘트) ──
    print("\n" + "─"*72)
    print("[조건 1] 미충전 d껍질의 짝없는 d전자 → 국소 모멘트 (Hund 규칙)")
    print("─"*72)
    print(f"  {'원소':<6}{'배치':<14}{'짝없d':>7}{'μ_so[μ_B]':>11}{'모멘트?':>9}")
    print("  "+"-"*47)
    for Z, sym, nd, s4, ds, T, cls in ELEMENTS:
        nu = d_unpaired(nd)
        mu = spin_only_moment(nu)
        cfg = f"3d{nd}4s{s4}"
        has = "있음" if nu > 0 else "없음(0)"
        print(f"  {sym:<6}{cfg:<14}{nu:>7}{mu:>11.2f}{has:>9}")
    print("  → Cu(3d¹⁰): 짝없는 d전자 0 → 모멘트 없음 → 조건1 실패 → 자성 불가.")
    print("    Fe(3d⁶):4, Co(3d⁷):3, Ni(3d⁸):2, Mn(3d⁵):5 → 모멘트 있음(조건1 통과).")
    assert d_unpaired(10) == 0, "Cu 짝없는 d전자 0 실패"
    assert d_unpaired(6) == 4, "Fe 짝없는 d전자 4 실패"
    assert d_unpaired(5) == 5, "Mn 짝없는 d전자 5 실패"

    # ── 2. 조건 2: 교환 부호 (Bethe-Slater) ──
    print("\n" + "─"*72)
    print("[조건 2] 양의 교환 J>0 — 이웃 d-회전이 나란히 정렬 (Bethe-Slater)")
    print("─"*72)
    print(f"  {'원소':<6}{'D/d비':>8}{'J 부호':>9}{'정렬':>12}")
    print("  "+"-"*35)
    for Z, sym, nd, s4, ds, T, cls in ELEMENTS:
        if d_unpaired(nd) == 0:
            print(f"  {sym:<6}{'—':>8}{'무의미':>9}{'(모멘트 없음)':>14}")
            continue
        j = exchange_sign(ds)
        js = "J>0" if j > 0 else "J<0"
        align = "나란히(강자성)" if j > 0 else "반대(반강자성)"
        print(f"  {sym:<6}{ds:>8.2f}{js:>9}{align:>12}")
    print(f"  → Mn(D/d={1.47}<{DS_CRIT}): 짝없는 5개나 J<0 → 반대정렬 → 반강자성(조건2 실패).")
    print(f"    Fe·Co·Ni(D/d>{DS_CRIT}): J>0 → 나란히 → 강자성. Co(D/d=1.82) 교환 최강.")

    # ── 3. 두 조건 종합: 자성 분류 도출 ──
    print("\n" + "─"*72)
    print("[종합] 두 조건 → 자성 분류 (도출 vs 실측)")
    print("─"*72)
    print(f"  {'원소':<6}{'짝없d':>7}{'D/d':>7}{'도출분류':>10}{'실측':>10}{'판정':>6}")
    print("  "+"-"*46)
    n_correct = 0
    for Z, sym, nd, s4, ds, T, cls in ELEMENTS:
        pred, reason = predict_class(nd, ds)
        ok = (pred == cls)
        n_correct += ok
        ds_s = f"{ds:.2f}" if ds else "—"
        print(f"  {sym:<6}{d_unpaired(nd):>7}{ds_s:>7}{pred:>10}{cls:>10}{'✓' if ok else '✗':>6}")
    print(f"  → 도출 {n_correct}/{len(ELEMENTS)} 적중. Cu=비자성(조건1), Mn=반강자성(조건2), Fe·Co·Ni=강자성.")
    assert n_correct == len(ELEMENTS), "자성 분류 도출 불일치"
    print("  ✓ '왜 Fe이고 Cu가 아닌가'(물리백서 입력) = 두 조건으로 도출됨. [F]")

    # ── 4. 퀴리 온도: 교환에너지가 열들뜸에 무너지는 온도 ──
    print("\n" + "─"*72)
    print("[퀴리 온도] 정렬을 무너뜨리는 열 — kT_C ~ 교환에너지 (회전 무질서화)")
    print("─"*72)
    print(f"  {'강자성체':<8}{'T_C[K]':>8}{'kT_C[meV]':>11}{'금속 μ[μ_B]':>12}")
    print("  "+"-"*39)
    for sym in ["Fe", "Co", "Ni"]:
        T = dict((e[1], e[5]) for e in ELEMENTS)[sym]
        kT_meV = KB*T/1.602176634e-19*1000
        mm = METALLIC_MOMENT[sym]
        print(f"  {sym:<8}{T:>8}{kT_meV:>11.1f}{mm:>12.2f}")
    print("  → T_C 위서 열회전이 정렬 무질서화 → 상자성. Co 최고 T_C(교환 최강과 일치).")
    print("    금속 모멘트(Fe 2.22 등)는 비정수 — 띠/편력 효과([O]); 국소 Hund 그림은 *순서*를 줌.")

    # ── 5. ∇·B=0·자구·이력 ──
    print("\n" + "─"*72)
    print("[자구·홀극·이력] 정렬 회전의 거시 발현")
    print("─"*72)
    print("  • 자구(domain): 교환이 국소적으로 모멘트(회전)를 정렬한 영역. 외부장이 자구벽 이동.")
    print("  • ∇·B=0: B는 회전축(양끝 N/S). 축은 분리 불가 → 자기홀극 없음(자석 자르면 N/S 재생).")
    print("  • 이력(hysteresis): 정렬이 일부 '되돌지 않고' 남음(영구자석). 가열>T_C면 소거.")
    print("  → 전자기에서 본 ∇·B=0(EM.4)이 강자성에서 자구·영구자석으로 거시화.")

    # ── 결론 ──
    print("\n" + "="*72)
    print("철의 자성 원리 요약:")
    print("  ① 자기 모멘트 = 짝없는 전자의 회전 (전하·헬리시티와 같은 회전)")
    print("  ② 조건1(국소 모멘트): 미충전 d껍질 짝없는 d전자 — Cu(3d¹⁰)는 0 → 자성 불가")
    print("  ③ 조건2(양의 교환 J>0): Bethe-Slater D/d>임계 — Mn은 J<0 → 반강자성")
    print("  ④ Fe·Co·Ni만 두 조건 충족 → 강자성 ('왜 Fe이고 Cu·Mn 아닌가' 도출)")
    print("  ⑤ 퀴리온도=교환에너지의 열한계, ∇·B=0 → 자구·영구자석·이력")
    print("  → 구리(전도)와 철(자성)의 갈림: 완전충전 d=자유전자=전도 vs 미충전 d=모멘트=자성.")
    print("등급: [F] 짝없는전자(Hund)·두조건 분류·∇·B=0 · [CAL] D/d·T_C·금속모멘트 · [O] 편력 비정수")
    print("="*72)


if __name__ == "__main__":
    main()
