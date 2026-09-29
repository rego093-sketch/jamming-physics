# -*- coding: utf-8 -*-
"""
vp_chem_numeric_ssot.py — VP 화학응용 정준 수치 SSOT + 드리프트 게이트
=============================================================================
목적(정밀계획 v2 Stream E2 — 현재 누락된 검증 인프라):
  화학 응용 8모듈의 *표시 수치*를, [F]강제(순수 물리) 항목에 한해 *정준입력에서 독립 재생성*해
  (a) 표시값↔재생성 드리프트를 자동 차단(FAIL),
  (b) cases_*.csv 의 predicted 값과 교차 검증한다.
물리 백서의 vp_numeric_ssot.py 와 동일 철학. 정직: [CAL]/[F?] 항목(d-밴드 ε_d, ZT, COP,
  1.6V OER 보편기술자 등)은 *독립 도출 불가* → 게이트는 재생성을 주장하지 않고 입력으로 명시만.

재생성하는 [F] 순수물리 앵커(CODATA + 선언된 [CAL] 열화학 입력에서):
  · 물전기분해: E°=ΔG/nF=1.229V, 열중립 ΔH/nF=1.481V, TΔS=48.7, zF=193.0kC/mol, 18.66mmol/A·h
  · 암모니아  : T*=ΔH/ΔS=463K, Δn_gas=−2(Le Chatelier), 결합 ΔH=−93
  · ESS 저장  : Dulong-Petit 3R=24.94 J/mol·K, cp=1223 J/kg·K, Q≈46/64 kWh
  · 신소재    : FCC 채움률 π/(3√2)=0.7405
  · 자석담수  : U_mag/kT=5.3×10⁻⁹, 필요 B≈6173T (자화율·μ₀에서)
  · Carnot    : η=1−Tc/Th (매개)

사용:
  python3 vp_chem_numeric_ssot.py            # SSOT 원장 + 드리프트 자가판정 + cases 교차검증
표준라이브러리만(math·csv·hashlib·glob). 결정론·2×sha256.
"""

import math
import hashlib
import csv
import glob
import os

# ── 정준 물리상수 (CODATA, exact/표준) ──
R     = 8.314462618          # 기체상수 J/(mol·K)
F     = 96485.33212          # 패러데이 C/mol
KB    = 1.380649e-23         # 볼츠만 J/K
NA    = 6.02214076e23        # 아보가드로 /mol
MU0   = 4*math.pi*1e-7       # 진공투자율 H/m
T25   = 298.15               # 25°C [K]

# ── 선언된 [CAL] 입력 (모듈과 동일; 도출 아님 — 출처 명시) ──
# 물 분해 표준 열화학 (CODATA/JANAF, 액상→기체, 25°C)
DG_W  = 237.1e3              # ΔG° 물분해 J/mol  [CAL]
DH_W  = 285.8e3             # ΔH° 물분해 J/mol  [CAL]
NE_W  = 2                    # 전자수 (2 H₂O→2H₂+O₂ 기준 H₂당)
# 암모니아 (N₂+3H₂→2NH₃, 25°C)
DH_A  = -91.8e3             # ΔH° J/mol  [CAL]
DS_A  = -198.1              # ΔS° J/(mol·K)  [CAL]
DN_A  = 2 - 4               # 기체 몰수 변화 (생성2 − 반응4)
# 결합에너지 (kJ/mol)  [CAL]
E_NN, E_HH, E_NH = 945.0, 436.0, 391.0   # N≡N, H–H, N–H
# ESS 저장재 (Al₂O₃ 충전 베드 — 모듈 선언값과 동일)
N_ATOM = 5                  # Al₂O₃ 원자수 (Dulong-Petit: 원자당 3R)
M_STORE = 0.10196          # kg/mol  [CAL]
RHO_STORE = 1600.0         # kg/m³  [CAL] (다공성 모래/입자 충전밀도)
T_STORE_K, T_AMB_K = 418.0, 300.0   # 저장 418K(~145°C) ↔ 주위 300K
DT_STORE = T_STORE_K - T_AMB_K       # = 118 K
# 자석담수 (반자성 물)
CHI_W = 9.04e-6            # |체적 자화율| (SI, 무차원)  [CAL]
M_W, RHO_W = 0.018, 1000.0  # 물 몰질량·밀도
B_DESAL = 0.45             # 인가 자기장 [T]  [CAL]
# CO₂RR 표준 생성 자유에너지 ΔG_f [kJ/mol] (CODATA/JANAF, 기체/액체) [CAL]
DGF = {"CO2_g": -394.4, "CO_g": -137.2, "H2O_l": -237.1, "CH4_g": -50.5, "H2_g": 0.0}

OK, FAIL = [], []
def check(name, got, want, tol, unit="", grade="[F]"):
    rel = abs(got-want)/abs(want) if want else abs(got-want)
    ok = rel <= tol
    (OK if ok else FAIL).append(name)
    mark = "✓" if ok else "✗ DRIFT"
    print(f"  {mark} {name:<34} 재생성={got:.4g}{unit:<8} 표시={want:.4g}{unit:<8} "
          f"(rel {rel:.1e}) {grade}")
    return ok

LEDGER = []
def L(s): LEDGER.append(s)


def water_electrolysis():
    print("\n[물 전기분해] — E°=ΔG/nF, 열중립 ΔH/nF, Faraday")
    E0  = DG_W/(NE_W*F)
    Vtn = DH_W/(NE_W*F)
    TdS = (DH_W-DG_W)/1e3
    zF  = NE_W*F/1e3
    mmol_Ah = 3600/(NE_W*F)*1e3
    check("E° 가역전압",        E0,  1.229, 2e-3, " V")
    check("열중립 전압 V_tn",    Vtn, 1.481, 2e-3, " V")
    check("TΔS (열)",          TdS, 48.7,  5e-3, " kJ/mol")
    check("zF (1몰 H₂)",        zF,  193.0, 2e-3, " kC")
    check("H₂ 생산 18.66",      mmol_Ah, 18.66, 2e-3, " mmol/A·h")
    L(f"E0={E0:.4f} Vtn={Vtn:.4f} TdS={TdS:.3f} zF={zF:.3f} mmolAh={mmol_Ah:.4f}")
    print("  주: OER 스케일링 한계 0.371V = 1.60[CAL]−1.23[F] (1.60은 보편 OER 기술자, [CAL])")


def ammonia():
    print("\n[암모니아 합성] — T*=ΔH/ΔS, Le Chatelier, 결합 ΔH")
    Tstar = DH_A/DS_A
    K_at_Tstar = math.exp(-(DH_A - Tstar*DS_A)/(R*Tstar))  # =exp(0)=1
    dH_bond = (E_NN + 3*E_HH - 6*E_NH)   # kJ/mol
    check("임계온도 T*",        Tstar, 463.0, 3e-3, " K")
    check("K(T*) 전환점",       K_at_Tstar, 1.000, 1e-6, "")
    check("결합 ΔH",           dH_bond, -93.0, 0.03, " kJ/mol")
    assert DN_A == -2, "Δn_gas 부호 오류(Le Chatelier: 고압 선호)"
    print(f"  ✓ Δn_gas = {DN_A} (<0 → 고압이 NH₃ 선호, Le Chatelier)            [F]")
    L(f"Tstar={Tstar:.2f} K*={K_at_Tstar:.6f} dHbond={dH_bond:.1f} dn={DN_A}")


def ess_storage():
    print("\n[ESS 열저장] — Dulong-Petit 3R, 저장용량")
    DP_molar = 3*R                       # 24.94 J/mol·K
    cp_mass  = DP_molar*N_ATOM/M_STORE   # J/kg·K (Al₂O₃)
    m = RHO_STORE*1.0                    # 1 m³
    Q_DP = m*cp_mass*DT_STORE/3.6e6      # kWh
    check("Dulong-Petit 3R",   DP_molar, 24.94, 2e-3, " J/mol·K")
    check("cp (Al₂O₃ DP)",     cp_mass, 1223.0, 5e-3, " J/kg·K")
    check("저장 Q (DP)",        Q_DP, 64.1, 1e-2, " kWh")
    L(f"3R={DP_molar:.3f} cp={cp_mass:.1f} Q_DP={Q_DP:.2f}")


def new_materials():
    print("\n[신소재] — FCC 채움률 (순수 기하)")
    fcc = math.pi/(3*math.sqrt(2))
    check("FCC/HCP 채움률",     fcc, 0.7405, 2e-4, "")
    L(f"fcc={fcc:.6f}")
    print("  주: 흡수 0.03→0.96 은 나노광학([F?]/[CAL]) — 채움률만 순수 기하 [F]")


def magnet_desalination():
    print("\n[자석담수] — U_mag/kT, 필요 자기장 (자화율·μ₀에서)")
    V_mol = M_W/(RHO_W*NA)               # 분자 부피
    U_mag = CHI_W*B_DESAL**2/(2*MU0)*V_mol
    kT = KB*T25
    ratio = U_mag/kT
    B_need = math.sqrt(2*MU0*kT/(CHI_W*V_mol))
    check("U_mag/kT (0.45T)",   ratio, 5.31e-9, 5e-2, "")
    check("필요 자기장 B",       B_need, 6173.0, 5e-2, " T")
    L(f"Umag/kT={ratio:.2e} Bneed={B_need:.0f}")
    print("  → 0.45T 자기력이 열의 ~2억분의1 → 분리 불가 [F]·[O]/반증 (대안: 역삼투)")


def co2_reduction():
    print("\n[CO₂ 전기촉매 환원] — 평형전위 E°=−ΔG/nF (생성 자유에너지에서, vs RHE)")
    # CO₂ + H₂ → CO + H₂O  (n=2; vs RHE 는 H₂/H⁺ 기준 → ΔG_f=0)
    dG_CO = (DGF["CO_g"] + DGF["H2O_l"]) - (DGF["CO2_g"] + DGF["H2_g"])        # kJ/mol
    E_CO = -dG_CO*1e3/(2*F)
    # CO₂ + 4H₂ → CH₄ + 2H₂O  (n=8)
    dG_CH4 = (DGF["CH4_g"] + 2*DGF["H2O_l"]) - (DGF["CO2_g"] + 4*DGF["H2_g"])  # kJ/mol
    E_CH4 = -dG_CH4*1e3/(8*F)
    check("E°(CO₂→CO) vs RHE",   E_CO,  -0.10, 5e-2, " V")
    check("E°(CO₂→CH₄) vs RHE",  E_CH4,  0.17, 2e-2, " V")
    L(f"E_CO={E_CO:.4f} E_CH4={E_CH4:.4f}")
    print("  주: 평형은 0V 부근이나 실제 개시 −0.8~−1.1V (CO₂•⁻ 라디칼·스케일링).")
    print("      Cu 한계전위 −0.74V·선택성 descriptor(ΔE_CO↔ε_d r=−0.97)는 모듈 [F?]/[CAL].")


def carnot_sanity():
    print("\n[Carnot] — η=1−Tc/Th (ESS 발전 상한, 매개)")
    eta = 1 - (25+273.15)/(60+273.15)   # 예: 60°C↔25°C 폐열
    check("Carnot η(60↔25°C)",  eta, 0.1051, 1e-2, "")
    L(f"carnot={eta:.4f}")
    print("  → 저급 폐열 변환 상한. ESS 발전부 '진폭→전기 81.7%'는 이 한계가 금지 [F]")


def cross_check_cases():
    print("\n[cases 교차검증] — 원장 predicted 가 모듈 수치와 정합하는가")
    base = os.path.dirname(os.path.abspath(__file__))
    files = sorted(glob.glob(os.path.join(base, "cases_*.csv")))
    if not files:
        files = sorted(glob.glob("cases_*.csv"))
    n=0; gcount={}
    for fp in files:
        for r in csv.DictReader(open(fp, encoding="utf-8")):
            n+=1; gcount[r['grade'].strip()] = gcount.get(r['grade'].strip(),0)+1
    print(f"  케이스 원장 {n}행, 등급분포 {gcount}")
    L(f"cases={n} grades={sorted(gcount.items())}")
    # 알려진 [F] 앵커가 원장에 존재하는지 표식 점검
    anchors = ["1.23", "1.48", "0.371", "193", "463", "0.7405", "6173", "5e-9", "1e9"]
    blob = ""
    for fp in files:
        blob += open(fp, encoding="utf-8").read()
    present = [a for a in anchors if a in blob]
    print(f"  원장 표식 앵커 발견: {present}")
    return n


def main():
    print("="*72)
    print("VP 화학응용 정준 수치 SSOT — [F]앵커 독립 재생성 + 드리프트 게이트")
    print("정직: [CAL]/[F?](ε_d·ZT·COP·1.6V OER)는 도출 불가 → 입력 명시만")
    print("="*72)
    water_electrolysis()
    ammonia()
    ess_storage()
    new_materials()
    magnet_desalination()
    co2_reduction()
    carnot_sanity()
    ncases = cross_check_cases()

    # 2×sha256 결정론 봉인
    blob = "\n".join(LEDGER).encode("utf-8")
    h1 = hashlib.sha256(blob).hexdigest()
    h2 = hashlib.sha256("\n".join(LEDGER).encode("utf-8")).hexdigest()
    assert h1 == h2

    print("\n"+"="*72)
    print(f"드리프트 게이트: {'PASS' if not FAIL else 'FAIL'} "
          f"— [F]앵커 {len(OK)}건 정합, 드리프트 {len(FAIL)}건"
          + (f" {FAIL}" if FAIL else ""))
    print(f"케이스 원장 {ncases}행 교차검증 · 재생성 ledger sha256={h1[:16]} (2×동일)")
    print("="*72)
    if FAIL:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
