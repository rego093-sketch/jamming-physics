# -*- coding: utf-8 -*-
"""
vp_new_materials.py — 신소재: 검은구리 흡수 + 선택흡수체 + d-밴드 소재 설계 (재현가능)
==================================================================
Stream D4 (정밀계획 v2). 사용자 지정 '신소재'. ESS(D5)의 검은구리를 *실제 기전*으로
설명하고(진폭 아님), 소재 설계 규칙을 d-밴드(Stream C)·기하(CH.13)와 잇는다.

이 모듈:
  [1] 왜 광택 금속은 반사하고 검은구리는 흡수하나 — Fresnel 반사율 + 나노구조/산화물
      임피던스 정합. α=1−R 이 0.03→0.96 으로. ('진폭'이 아니라 광학.)
  [2] 선택흡수체 — 높은 태양흡수 α_s + 낮은 적외방사 ε_IR. 재방사 손실(Stefan-Boltzmann)이
      ESS 성능을 좌우 → 왜 '선택성'이 핵심인가(저방사 아니면 데울 수도 없음).
  [3] d-밴드 소재 설계 — 합금이 ε_d 이동 → 표면·촉매·전자 물성 조율(Stream C 연결).
  [4] 결정 기하 — 채움률·밀도(순수 기하 [F], CH.13).

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_new_materials.py
"""
import math

SIGMA = 5.670374e-8          # Stefan-Boltzmann 상수 [W/m²·K⁴]

# 집열·환경 (ESS 와 동일 조건) [CAL]
SOLAR_FLUX = 800.0           # 일사 [W/m²]
AREA = 1.0                   # 면적 [m²]
T_STORE = 418.0              # 저장온도 [K] (~145°C)
T_AMB = 300.0                # 주위 [K]

# 흡수율(=1−반사율) [CAL]
R_POLISHED = 0.97            # 광택 구리 반사율(가시) → α=0.03
ALPHA_BLACK = 0.96           # 검은(나노/산화) 구리 흡수율
EPS_SELECTIVE = 0.05         # 선택흡수체 적외 방사율(낮음)
EPS_BLACKBODY = 0.90         # 비선택(흑체형) 방사율(높음)

# 결정 채움률 (순수 기하) [F]
PACKING = {"FCC/HCP": math.pi / (3 * math.sqrt(2)), "BCC": math.sqrt(3) * math.pi / 8,
           "SC": math.pi / 6}


def rerad_loss(eps):
    """선택흡수체 재방사 손실 (Stefan-Boltzmann): P = ε·σ·A·(T⁴−T_amb⁴) [W]."""
    return eps * SIGMA * AREA * (T_STORE ** 4 - T_AMB ** 4)


def main():
    print("=" * 72)
    print("신소재 — 검은구리 흡수 + 선택흡수체 + d-밴드 소재 설계")
    print("=" * 72)
    print("검은구리 고흡수는 *광학(나노구조·임피던스)*이지 '진폭'이 아니다. ESS·촉매와 연결.")

    # ── [1] 광택 금속 vs 검은구리 ──
    print("\n" + "─" * 72)
    print("[1] 왜 광택 금속은 반사하고 검은구리는 흡수하나 — Fresnel + 나노구조 [F?]")
    print("─" * 72)
    alpha_polished = 1 - R_POLISHED
    print(f"  광택 구리: 자유전자 플라즈마가 가시광 반사(R≈{R_POLISHED}) → 흡수 α=1−R={alpha_polished:.2f}.")
    print(f"  검은(나노/CuO) 구리: 표면 나노구조가 (a) 점진 굴절률로 반사 억제(임피던스 정합),")
    print(f"    (b) 빛 가둠(다중산란), (c) CuO 본질 흡수 → α≈{ALPHA_BLACK:.2f}.")
    print(f"  흡수 향상: α {alpha_polished:.2f} → {ALPHA_BLACK:.2f} (약 {ALPHA_BLACK/alpha_polished:.0f}배).")
    print(f"  → 기전은 *광학*(구리편 플라즈마/표피와 같은 EM): 진폭 fm 수치가 아니라.")
    assert ALPHA_BLACK > alpha_polished, "검은구리 흡수가 광택보다 작음(모순)"

    # ── [2] 선택흡수체: 재방사 손실이 ESS 를 좌우 ──
    print("\n" + "─" * 72)
    print("[2] 선택흡수체 — 높은 α_s + 낮은 ε_IR. 재방사 손실이 핵심 [F]")
    print("─" * 72)
    P_abs = ALPHA_BLACK * SOLAR_FLUX * AREA
    P_sel = rerad_loss(EPS_SELECTIVE)
    P_bb = rerad_loss(EPS_BLACKBODY)
    print(f"  흡수 태양전력 = α_s·flux·A = {P_abs:.0f} W")
    print(f"  재방사 손실 P = ε·σ·A·(T⁴−T_amb⁴):")
    print(f"  {'표면':<24}{'ε_IR':>6}{'재방사[W]':>11}{'순흡수[W]':>11}")
    print(f"  {'선택흡수체(저방사)':<22}{EPS_SELECTIVE:>6.2f}{P_sel:>11.0f}{P_abs-P_sel:>11.0f}")
    print(f"  {'비선택(흑체형)':<23}{EPS_BLACKBODY:>6.2f}{P_bb:>11.0f}{P_abs-P_bb:>11.0f}")
    print(f"  → 선택흡수체는 순흡수 +{P_abs-P_sel:.0f}W(저장 가능). 흑체형은 {P_abs-P_bb:+.0f}W —")
    print(f"    재방사가 흡수를 초과해 *데울 수조차 없다*. 검은구리에 '저적외방사'가 필수.")
    print(f"  선택성 α/ε = {ALPHA_BLACK/EPS_SELECTIVE:.0f} (선택흡수체) vs {ALPHA_BLACK/EPS_BLACKBODY:.1f}(흑체형).")
    assert (P_abs - P_bb) < 0 < (P_abs - P_sel), "선택성 임계 판정 모순"

    # ── [3] d-밴드 소재 설계 ──
    print("\n" + "─" * 72)
    print("[3] d-밴드 소재 설계 — 합금이 ε_d 이동 → 물성 조율 (Stream C 연결) [F?]")
    print("─" * 72)
    print("  같은 d-밴드 원리(Stream C)가 소재 설계 규칙을 준다:")
    print("  · 촉매: ε_d 이동으로 흡착 결합 최적화(합금/변형/코어쉘) — 물분해 전극(D3a).")
    print("  · 전자/자성: d-채움이 전도(구리)·자성(철)·촉매(백금)를 가른다(금속 3부작, CM/CT).")
    print("  · 설계 손잡이는 *d-전자 에너지*(조성·변형)지 격자기하 공명(반증)이 아니다.")

    # ── [4] 결정 기하 (순수 기하 [F]) ──
    print("\n" + "─" * 72)
    print("[4] 결정 기하 — 채움률(순수 기하, CH.13) [F]")
    print("─" * 72)
    print(f"  {'구조':<10}{'채움률':>10}  (자유계수 0, 닫힌형)")
    for name, pf in PACKING.items():
        print(f"  {name:<10}{pf:>10.4f}")
    assert abs(PACKING["FCC/HCP"] - 0.7405) < 1e-3, "FCC 채움률 불일치"
    print(f"  → FCC/HCP π/(3√2)={PACKING['FCC/HCP']:.4f}. 소재 밀도·구조의 기하 토대(튜닝 불가).")

    # ── 결론 + 등급 ──
    print("\n" + "=" * 72)
    print("결론 — 신소재는 광학·d-밴드·기하로 설명된다 (진폭 아님)")
    print(f"  ① 검은구리 흡수 α {alpha_polished:.2f}→{ALPHA_BLACK:.2f} = 나노구조 광학(EM, 구리편 계승)")
    print(f"  ② 선택흡수체: 저적외방사 필수 — 아니면 순흡수 음수(데울 수 없음)")
    print(f"  ③ d-밴드(조성/변형)가 촉매·전자·자성 설계 손잡이 (Stream C)")
    print(f"  ④ 결정 채움률은 순수 기하 [F] (CH.13)")
    print("-" * 72)
    print("등급: [F] 재방사 Stefan-Boltzmann·채움률 기하 · [F?] 흡수 향상·선택성·d-밴드 설계 ·")
    print("      [CAL] 반사율·방사율·일사 · (진폭 기반 설명은 폐기 — 광학/에너지로 대체)")
    print("반증가능 예측: 비선택 흑체형 검은구리는 저장온도서 순흡수 음수 → 작동 불가.")
    print("=" * 72)


if __name__ == "__main__":
    main()
