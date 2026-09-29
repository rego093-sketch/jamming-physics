# -*- coding: utf-8 -*-
"""
vp_ess_thermal.py — ESS(검은구리): 태양열 저장 + 정직한 발전 재정초 (재현가능)
==================================================================
Stream D5 (정밀계획 v2). 게이트 G-a(반증/[H] 정직 표기 + 작동 대안) 직접 실행.

구 응용백서(DOI 18043066)의 무배터리 태양열 ESS:
  검은 나노코팅 구리판(흡수≥98%) → 고비열 충전재(Al₂O₃/모래) 저장 → 진공단열 →
  "검은 알루미늄 *회전 진폭 복원* → 전기장 발생" 발전.

정직 분해:
  · 저장부 = 실재. 복사흡수·고비열(Dulong-Petit 3R, CH.7 직결)·진공단열을 정량화.
  · 발전부 = "회전 진폭 복원 → 전기장"은 검증 안 된 [H]. 작동 대안(열전/Stirling/TPV)을
    Carnot 한계와 함께 정량 제시. 작동 안 하는 기구를 작동하는 척하지 않는다.

이 모듈:
  [1] 태양 흡수 — 검은구리 α≥0.98, 흡수전력·하루 집열량.
  [2] 열저장 용량 — Dulong-Petit 비열(CH.7)로 1m³ 저장 에너지[kWh].
  [3] 진공단열 — 열손실·열시정수 τ → 야간 보존 가능성.
  [4] ★발전 — 구 '진폭→전기' 는 [H]; Carnot 한계 + 열전(Seebeck)·Stirling 실효율로 대체.

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_ess_thermal.py
"""
import math

R = 8.314                    # 기체상수 [J/mol·K]

# 검은구리 집열판 [CAL / 구 주장]
ALPHA = 0.98                 # 흡수율 (검은 나노코팅 구리)
SOLAR_FLUX = 800.0           # 일사량 [W/m²] (구 시뮬 조건)
AREA = 1.0                   # 집열면적 [m²] (1m³ 모듈 상면)
SUN_HOURS = 6.0              # 하루 유효 일조 [h]

# 고비열 충전재: Al₂O₃ (알루미나/모래) [CAL]
M_AL2O3 = 0.10196            # 몰질량 [kg/mol] (101.96 g/mol)
ATOMS_PER_FU = 5             # Al₂O₃ 화학식당 원자수 (Dulong-Petit: 원자당 3R)
RHO_PACKED = 1600.0          # 충전 밀도 [kg/m³] (다공성 모래/입자)
VOL = 1.0                    # 저장 부피 [m³]
T_AMB = 300.0                # 주위온도 [K] (~27°C)
T_STORE = 418.0              # 저장 임계온도 [K] (~145°C, 구 주장)
CP_MEASURED = 880.0          # Al₂O₃ 실측 비열 [J/kg·K] (상온, 비교용) [CAL]

# 진공단열 [CAL]
U_INS = 0.5                  # 단열 열관류율 [W/m²·K] (양호한 진공단열)
A_SURF = 6.0                 # 1m³ 정육면체 표면적 [m²]


def main():
    print("=" * 72)
    print("ESS(검은구리) — 태양열 저장 + 정직한 발전 재정초")
    print("=" * 72)
    print("정직 분해: 저장부=실재(정량화) · 발전부 '진폭→전기'=검증 안 됨([H], 대안 제시).")

    # ── [1] 태양 흡수 ──
    print("\n" + "─" * 72)
    print("[1] 태양 흡수 — 검은구리 α≥0.98 [F?]/[CAL]")
    print("─" * 72)
    P_abs = ALPHA * SOLAR_FLUX * AREA
    E_day = P_abs * SUN_HOURS * 3600.0                  # [J]
    print(f"  흡수전력 P = α·flux·A = {ALPHA}·{SOLAR_FLUX}·{AREA} = {P_abs:.0f} W")
    print(f"  하루 집열량 = P·{SUN_HOURS}h = {E_day/3.6e6:.1f} kWh/일 (1m² 집열, 6시간 일조)")
    print(f"  → 검은구리 고흡수는 나노구조 광대역 흡수(표면 임피던스 정합)지 '진폭' 아님(D4 참조).")
    assert P_abs > 0

    # ── [2] 열저장 용량 (Dulong-Petit, CH.7 직결) ──
    print("\n" + "─" * 72)
    print("[2] 열저장 용량 — Dulong-Petit 비열(CH.7 열역학)로 1m³ 저장 [F?]")
    print("─" * 72)
    # Dulong-Petit: 몰열용량(원자당) 3R → 화학식당 3R·atoms; 질량당 cp = 3R·atoms/M
    cp_DP = 3 * R * ATOMS_PER_FU / M_AL2O3              # [J/kg·K]
    m = RHO_PACKED * VOL                                 # [kg]
    dT = T_STORE - T_AMB
    Q = m * CP_MEASURED * dT                             # 실측 비열로 저장에너지
    Q_DP = m * cp_DP * dT
    print(f"  Dulong-Petit 비열 cp = 3R·{ATOMS_PER_FU}/M = {cp_DP:.0f} J/kg·K")
    print(f"    (실측 상온 {CP_MEASURED:.0f} J/kg·K — 고온서 Dulong-Petit 극한으로 접근, CH.7 계단과 동일 원리)")
    print(f"  질량 m = ρ·V = {m:.0f} kg · ΔT = {dT:.0f} K")
    print(f"  저장에너지 Q = m·cp·ΔT = {Q/3.6e6:.1f} kWh (실측비열) / {Q_DP/3.6e6:.1f} kWh (Dulong-Petit)")
    print(f"  → 1m³ 가 ~{Q/3.6e6:.0f} kWh 열 저장. 집열 {E_day/3.6e6:.1f}kWh/일 → 충전 ~{Q/E_day:.1f}일분 용량.")
    assert cp_DP > CP_MEASURED, "Dulong-Petit 상한이 실측보다 작음(모순)"

    # ── [3] 진공단열: 열시정수 ──
    print("\n" + "─" * 72)
    print("[3] 진공단열 — 열손실·열시정수 τ → 야간 보존 [F?]")
    print("─" * 72)
    P_loss = U_INS * A_SURF * dT                         # 초기 열손실률 [W]
    tau = (m * CP_MEASURED) / (U_INS * A_SURF)           # 열시정수 [s]
    print(f"  초기 열손실 P_loss = U·A·ΔT = {U_INS}·{A_SURF}·{dT:.0f} = {P_loss:.0f} W")
    print(f"  열시정수 τ = m·cp/(U·A) = {tau/3600:.0f} h = {tau/86400:.1f} 일")
    print(f"  → τ ≈ {tau/86400:.1f}일 이면 야간(~12h) 보존은 충분. 단열이 핵심 설계요소.")
    assert tau > 12 * 3600, "열시정수가 야간보다 짧음(보존 불가)"

    # ── [4] ★발전: 구 '진폭→전기'는 [H], 작동 대안 정량 ──
    print("\n" + "─" * 72)
    print("[4] ★발전 — '회전 진폭→전기장'은 [H]; Carnot 한계 + 작동 대안 [H]→대안 [F]")
    print("─" * 72)
    eta_carnot = 1 - T_AMB / T_STORE
    print(f"  구 주장 '진폭 복원→전기장': 검증된 기전 없음 → [H]. 열→전기는 Carnot 가 상한.")
    print(f"  Carnot 한계 η = 1 − T_c/T_h = 1 − {T_AMB:.0f}/{T_STORE:.0f} = {eta_carnot*100:.1f}%")
    # 열전(Seebeck): η = η_carnot · (√(1+ZT)−1)/(√(1+ZT)+T_c/T_h)
    ZT = 1.0
    s = math.sqrt(1 + ZT)
    eta_TE = eta_carnot * (s - 1) / (s + T_AMB / T_STORE)
    # Stirling: 실효율 ~ Carnot 의 50%
    eta_stirling = 0.5 * eta_carnot
    Q_kWh = Q / 3.6e6
    print(f"  작동 대안(저장열 {Q_kWh:.0f}kWh, ΔT={dT:.0f}K 기준 전기 산출):")
    print(f"  {'기술':<22}{'효율':>8}{'전기[kWh]':>11}")
    print(f"  {'Carnot 한계(이상)':<21}{eta_carnot*100:>7.1f}%{Q_kWh*eta_carnot:>11.1f}")
    print(f"  {'열전 Seebeck (ZT=1)':<21}{eta_TE*100:>7.1f}%{Q_kWh*eta_TE:>11.1f}")
    print(f"  {'Stirling 엔진(~½Carnot)':<20}{eta_stirling*100:>7.1f}%{Q_kWh*eta_stirling:>11.1f}")
    print(f"  → 발전은 검증된 열기관/열전으로 해야 하며, ΔT={dT:.0f}K 는 효율을 근본 제한.")
    print(f"    '진폭 복원 전기장'은 작동 증거가 없으므로 [H]로 명시 — 저장부의 실재성과 분리.")
    assert eta_TE < eta_carnot, "열전 효율이 Carnot 초과(물리 위반)"

    # ── 결론 + 등급 ──
    print("\n" + "=" * 72)
    print("결론 — ESS 저장부는 실재·정량화, 발전부는 정직히 [H] + 대안")
    print(f"  ① 검은구리 흡수 {P_abs:.0f}W → 하루 {E_day/3.6e6:.1f}kWh 집열")
    print(f"  ② 1m³ 고비열 저장 ~{Q_kWh:.0f}kWh (Dulong-Petit, CH.7 직결)")
    print(f"  ③ 진공단열 τ≈{tau/86400:.1f}일 → 야간 보존 가능")
    print(f"  ④ 발전: '진폭→전기'[H]; Carnot {eta_carnot*100:.0f}% 한계 내 열전/Stirling 로 대체")
    print("-" * 72)
    print("등급: [F] Dulong-Petit·열시정수·Carnot/Seebeck/Stirling 효율 ·")
    print("      [F?] 흡수·저장 용량 · [CAL] α·일사·비열·단열계수 ·")
    print("      [H]→대안 구 '회전 진폭→전기장' 발전 기구(작동 증거 없음 → 열기관으로 대체)")
    print("정직 고지: 저장(열역학, 실재)과 발전(기전, 미검증)을 분리. Pt·자석담수와 같은 패턴.")
    print("=" * 72)


if __name__ == "__main__":
    main()
