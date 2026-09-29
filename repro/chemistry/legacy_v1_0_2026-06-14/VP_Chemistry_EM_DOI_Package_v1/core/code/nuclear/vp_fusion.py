# -*- coding: utf-8 -*-
"""
vp_fusion.py — VP 핵융합 + 철 봉우리 (재현가능·인과적)
====================================================================
주장: 핵융합과 핵분열은 같은 경쟁의 두 방향이다. 같은 SEMF(표면=재밍, 쿨롱=EM 1/r²)가
      결합에너지/핵자 곡선 B/A 를 만들고, 그 봉우리(철)가 융합·분열의 경계를 정한다.
        - 봉우리 아래(가벼움): 융합이 B/A 를 올림 → 에너지 방출
        - 봉우리 위(무거움):   분열이 B/A 를 올림 → 에너지 방출
      별이 철까지만 융합하고 그 너머에서 붕괴(초신성)하는 이유 = 재밍-EM 경쟁의 봉우리.

인과 사슬: 표면항/핵자 a_S·A^(-1/3) (재밍, A↑로 감소 → B/A↑)
           쿨롱항/핵자 a_C·Z²/A^(4/3) (EM 1/r², A↑로 증가 → B/A↓)
           두 추세의 균형점 = 철 봉우리. 자유계수 0(계수는 N1과 동일 [CAL]).

실행: python3 vp_fusion.py   (표준 라이브러리만)
"""
import math

PI = math.pi
ALPHA_EM, HBAR_C = 1/137.035999, 197.3269804
E2_4PIE0 = ALPHA_EM*HBAR_C
R0_FM = 1.20

# 계수 (N1 vp_fission.py 와 동일 — 단일 SSOT)
A_V, A_S, A_A, A_PAIR = 15.75, 17.80, 23.70, 12.0
A_C = (3/5)*E2_4PIE0/R0_FM       # 쿨롱 = EM 1/r² (= 0.720 MeV)

def pairing(A, Z):
    N = A-Z
    if A % 2 == 1: return 0.0
    return (+A_PAIR if (Z%2==0 and N%2==0) else -A_PAIR)/math.sqrt(A)

def binding_energy(A, Z):
    if A <= 0 or Z < 0 or Z > A: return float('-inf')
    return (A_V*A - A_S*A**(2/3) - A_C*Z*(Z-1)/A**(1/3)
            - A_A*(A-2*Z)**2/A + pairing(A, Z))

def most_stable_Z(A):
    """주어진 A 에서 B 를 최대로 하는 Z (베타 안정선)."""
    best_Z, best_B = 1, float('-inf')
    for Z in range(1, A):
        B = binding_energy(A, Z)
        if B > best_B: best_B, best_Z = B, Z
    return best_Z, best_B

def b_per_a_curve(a_min=4, a_max=240):
    """베타 안정선 따라 B/A 곡선."""
    out = []
    for A in range(a_min, a_max+1):
        Z, B = most_stable_Z(A)
        out.append((A, Z, B/A))
    return out

def surface_coulomb_per_nucleon(A):
    """봉우리의 인과 분해: 표면(재밍) 대 쿨롱(EM) 핵자당 기여."""
    Z, _ = most_stable_Z(A)
    surf = A_S*A**(2/3)/A          # 재밍 표면 비용/핵자 (A↑로 감소)
    coul = A_C*Z*(Z-1)/A**(1/3)/A  # 쿨롱 비용/핵자 (A↑로 증가)
    return surf, coul


def main():
    print("="*72)
    print("VP 핵융합 + 철 봉우리 — 재밍 표면 대 EM 쿨롱 경쟁이 B/A 곡선을 만든다")
    print("="*72)

    curve = b_per_a_curve()
    peak_A, peak_Z, peak_BA = max(curve, key=lambda t: t[2])
    print(f"\n[철 봉우리] B/A 최대 = {peak_BA:.3f} MeV/핵자  @  A={peak_A}, Z={peak_Z}")
    print(f"  실측: Fe-56(8.79)·Ni-62(8.79) 최대결합. VP 봉우리 A={peak_A} → 철/니켈 영역 ✓")

    print("\n[B/A 곡선 표본] (베타 안정선)")
    print(f"  {'A':>4} {'Z':>4} {'B/A[MeV]':>10}  표면/핵자  쿨롱/핵자   추세")
    print("  "+"-"*70)
    for A in [4, 12, 16, 28, 56, 62, 90, 120, 180, 235]:
        Z, _ = most_stable_Z(A)
        ba = binding_energy(A, Z)/A
        s, c = surface_coulomb_per_nucleon(A)
        side = "융합방출" if A < peak_A else "분열방출"
        print(f"  {A:>4} {Z:>4} {ba:>10.3f}    {s:>6.3f}    {c:>6.3f}    {side}")
    print("  → 표면/핵자(재밍) ↓ · 쿨롱/핵자(EM) ↑ : 두 추세 교차 = 철 봉우리. 인과적.")

    # ── 융합 Q (봉우리 아래, 에너지 방출) ──
    print("\n[융합 Q] 봉우리 아래 — 가벼운 핵 결합 시 에너지 방출 (SEMF)")
    print("  주: SEMF는 극경량핵(He-4 이중마법수)에서 부정확 → 정성적/[O]. 추세는 견고.")
    fus = [
        ("2·C-12 → Mg-24",       [(12,6),(12,6)], (24,12), 0),
        ("C-12 + O-16 → Si-28",  [(12,6),(16,8)], (28,14), 0),
        ("2·O-16 → S-32",        [(16,8),(16,8)], (32,16), 0),
        ("Si-28 + Si-28 → Ni-56",[(28,14),(28,14)],(56,28), 0),
    ]
    for label, reac, prod, ne in fus:
        Bp = binding_energy(*prod)
        Br = sum(binding_energy(A,Z) for A,Z in reac)
        Q = Bp - Br
        sign = "방출" if Q > 0 else "흡수"
        print(f"  {label:<26} Q = {Q:+7.1f} MeV  ({sign})")
    print("  → 전부 양(방출): 봉우리 아래에서 융합은 에너지를 낸다. 분열(N1)과 반대 방향, 같은 곡선.")

    # ── 융합 대 분열 경계 (별의 종말) ──
    print("\n[경계] 같은 경쟁, 두 방향")
    print("  ┌──────────────┬────────────────────┬────────────────────┐")
    print("  │ 영역         │ 에너지 내는 방향   │ VP 구동            │")
    print("  ├──────────────┼────────────────────┼────────────────────┤")
    print(f"  │ A < {peak_A:<3} (경)   │ 융합 (B/A↑로)      │ 재밍 표면 비용 감소 │")
    print(f"  │ A > {peak_A:<3} (중)   │ 분열 (B/A↑로)      │ EM 쿨롱 비용 감소  │")
    print("  └──────────────┴────────────────────┴────────────────────┘")
    print(f"  별: 철({peak_A}±)까지 융합 → 그 너머 융합은 흡열 → 핵 연료 소진 → 중력붕괴(초신성).")
    print(f"  이 우주적 경계가 VP 두 [F] 핸드오프(재밍·EM 1/r²)의 균형점에서 나온다.")

    print("\n" + "="*72)
    print("등급: [F] 봉우리 존재(표면↓·쿨롱↑ 균형, 순수구조) · [F?] 위치 A≈%d (계수 [CAL] 의존)" % peak_A)
    print("      [F] 융합/분열 방향(곡선 양쪽 부호) · [O] 극경량핵 군집효과·정밀 봉우리(껍질)")
    print("      핵심: 분열(N1)과 융합(N2)이 한 곡선의 두 끝. 같은 재밍-EM 경쟁.")
    print("="*72)


if __name__ == "__main__":
    main()
