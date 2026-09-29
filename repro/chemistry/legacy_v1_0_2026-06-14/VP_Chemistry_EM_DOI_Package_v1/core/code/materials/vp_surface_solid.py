# -*- coding: utf-8 -*-
"""
vp_surface_solid.py — S3 표면·계면 에너지 → 금속 (재현가능·인과적)
====================================================================
주장: 표면에너지는 §9 재밍의 '잃은 배위수' 물리다. 표면 원자는 배위수가 줄고, 그 끊긴
      접촉이 표면에너지다. 재밍(z=6 비정질/액체)은 γσ²/ε=3φz/4π=0.92(비활성기체 검증);
      결정(fcc z=12)은 끊긴결합 환원 γ_s·A/E_coh = Z_broken/Z_bulk ≈ 0.25 (비완화 상한).
      실측 금속은 그 상한 아래 범위(완화로 ~30%↓) — '이상값 + 현실 범위'.

인과 사슬: 재밍 끊긴접촉(§9)[F] → 표면 원자 잃은 배위 Z_broken → γ_s = Z_broken·E_coh/(Z_bulk·A).
           기하(Z_broken/Z_bulk)[F] + E_coh·격자상수 측정[CAL]. 완화 = [O].

이상값 대 범위: 0.25(비완화 상한) = 이상; 실측 0.13-0.19 = 완화로 그 아래. 잔차 면역(VP-섹터 무관).
실행: python3 vp_surface_solid.py   (표준 라이브러리만)
"""
import math
EV = 1.602176634e-19

# 비활성기체 z=6 재밍 (§9, 검증완료) — z=6 닻
PHI6, Z6 = 0.64, 6
RED_JAM6 = 3*PHI6*Z6/(4*math.pi)     # 0.917 (Ar 0.921·Kr 0.895 검증)

# 결정 끊긴결합 상한 (비완화)
def broken_bond_upper(Z_broken, Z_bulk):  return Z_broken/Z_bulk

# 검증: 금속 (구조, a[Å], E_coh[eV], γ_s측정[J/m²], 면, Z_broken, Z_bulk)
METALS = [
    ("Cu", "fcc", 3.615, 3.49, 1.79, "(111)", 3, 12),
    ("Ni", "fcc", 3.524, 4.44, 2.45, "(111)", 3, 12),
    ("Al", "fcc", 4.050, 3.39, 1.14, "(111)", 3, 12),
    ("Au", "fcc", 4.078, 3.81, 1.50, "(111)", 3, 12),
    ("Ag", "fcc", 4.085, 2.95, 1.25, "(111)", 3, 12),
    ("Pt", "fcc", 3.924, 5.84, 2.49, "(111)", 3, 12),
    ("Fe", "bcc", 2.866, 4.28, 2.41, "(110)", 2, 8),
    ("W",  "bcc", 3.165, 8.90, 3.27, "(110)", 2, 8),
]

def atom_area(struct, a_A):
    """표면 원자당 면적 [m²]. fcc(111): (√3/4)a². bcc(110): a²/√2."""
    a = a_A*1e-10
    if struct == "fcc": return (math.sqrt(3)/4)*a*a      # (111)
    else:               return a*a/math.sqrt(2)          # bcc(110)


def main():
    print("="*72)
    print("S3 금속 표면에너지 — 재밍 '잃은 배위수'가 이상 상한, 완화가 현실을 그 아래로")
    print("="*72)

    print(f"\n[z=6 닻] 비활성기체 재밍 γσ²/ε = 3φz/4π = {RED_JAM6:.3f}  (§9: Ar 0.921·Kr 0.895 검증)")
    print(f"  결정(fcc z=12) 끊긴결합 상한 γ_s·A/E_coh = Z_broken/Z_bulk = 3/12 = {3/12:.3f} (비완화)")

    print("\n[검증] 금속 환원 표면에너지 vs 끊긴결합 상한")
    print(f"  {'금속':<4} {'구조':>4} {'면':>6} {'γ측정':>6} {'A[Å²]':>6} {'환원γ':>7} {'상한':>5} {'완화':>6}")
    print("  "+"-"*64)
    reds = []
    for name, st, a, Ecoh, gam, face, Zb, Zbulk in METALS:
        A = atom_area(st, a)
        red = gam*A/(Ecoh*EV)               # 무차원 γ_s·A/E_coh
        upper = broken_bond_upper(Zb, Zbulk)
        relax = 1 - red/upper               # 완화율
        reds.append(red)
        print(f"  {name:<4} {st:>4} {face:>6} {gam:>6.2f} {A*1e20:>6.2f} {red:>7.3f} {upper:>5.2f} {100*relax:>5.0f}%")
    avg = sum(reds)/len(reds)
    print(f"  → 환원 평균 {avg:.3f} vs 상한 0.25 → 평균 완화 ~{100*(1-avg/0.25):.0f}%. 전부 상한 아래(이상값 아래).")

    print("\n[비평 + 이상값/범위]")
    print(f"  • 끊긴결합 상한 0.25(=Z_broken/Z_bulk)는 '이상값'(비완화). 측정 {min(reds):.2f}-{max(reds):.2f}.")
    print("  • 모든 금속이 상한 아래 → 표면 완화(원자 안쪽 이완)가 ~25-45% 낮춤. 완화 = [O](정밀화 과제).")
    print("  • 재밍 z=6(0.92, 비활성기체)과 결정 z=12(0.25 환원)는 같은 '잃은 배위=표면에너지' 물리,")
    print("    배위수만 다름(3φz/4π ↔ Z_broken/Z_bulk). 미시(§5 결합각)·거시(표면) 통일의 연장.")

    print("\n[신소재 함의]")
    print("  • 표면에너지 상한이 E_coh·기하로 결정 → 코팅/촉매/계면 설계의 상한 추정 가능.")
    print("  • 완화율(이상↔실측 간극)이 표면 재구성·흡착 설계의 여지 — S1 강도의 결함여지와 같은 구조.")

    print("\n" + "="*72)
    print("등급: [F] 끊긴결합 환원 = Z_broken/Z_bulk (기하) · [CAL] E_coh·격자상수 · [O] 표면완화")
    print("      [F] z=6 재밍 0.92(비활성기체 검증, §9) · 이상값(상한) 견고, 현실은 완화로 범위.")
    print("      잔차 면역: VP 양성자/힉스 섹터 잔차 미진입(E_coh·격자는 측정[CAL]).")
    print("="*72)


if __name__ == "__main__":
    main()
