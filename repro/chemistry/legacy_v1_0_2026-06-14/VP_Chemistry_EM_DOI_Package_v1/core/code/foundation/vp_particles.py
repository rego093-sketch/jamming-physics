# -*- coding: utf-8 -*-
"""
vp_particles.py — 입자 기초: 양성자·중성자·전자 정밀 정의 (재현가능·인과적)
====================================================================
목적: 주기율표의 기초가 흔들리지 않도록, p/n/e 를 단일 SSOT 닫힌형으로 정의하고
      측정값(CODATA/PDG)과 대조해 잔차를 명시한다. 통합이론서를 참조하되 의존하지 않고,
      더 정밀한(잔차 명시) 기초로 재구성한다.

구조 (인과):
  전자 = 유일 관찰입력(앵커). m_e 로 절대척도 고정. Re=λ_C/2(최소국소화 증명).
  양성자 = 전자 대비 강제 예측. m_p=6π⁵·m_e, r_p=D/6π⁶, μ_p=(3π+7/4)/4. 구조 89=82+7.
  중성자 = 양성자 대비 경쟁/구조. m_n−m_p=E_config−E_EM, μ_n=(7/4−3π)/4, τ_n=89π². 구조 82.

등급: [F] 강제(<0.5%) · [F?] 강제후보(<1.5% 또는 모델의존) · [CAL] 측정입력 · [O] 열림.
실행: python3 vp_particles.py   (표준 라이브러리만)
"""
import math
PI = math.pi

# ── 측정 상수 (CODATA 2018 / PDG — 검증 기준선, 도출에 미사용) ──
M = dict(
    mp_me   = 1836.15267343,    # m_p/m_e
    mn_me   = 1838.68366173,    # m_n/m_e
    mn_mp   = 1.00137841931,    # m_n/m_p
    mu_p    = 2.79284734463,    # μ_p [μ_N]
    mu_n    = -1.91304273,      # μ_n [μ_N]
    g_e     = 2.00231930436,    # 전자 g-인자
    r_p     = 0.8414,           # 양성자 전하반지름 [fm] (CODATA)
    tau_n   = 878.4,            # 중성자 수명 [s] (bottle/PDG)
    m_e_MeV = 0.51099895,       # 전자질량 [MeV] (앵커, VP에서 정의값)
    mn_mp_MeV = 1.29333236,     # m_n−m_p [MeV]
)
# 물리 입력 (앵커 유도)
HBARC = 197.3269804     # ℏc [MeV·fm]
ALPHA = 1/137.035999    # α_em (측정 외부입력)
DELTA = 1/PI**2         # 정류 δ = 1/π²
R_CORE = 0.84           # 핵자 코어 반경 [fm]


def section(title): print("\n"+"="*72+"\n"+title+"\n"+"="*72)
def chk(name, vp, meas, grade, note=""):
    d = (vp-meas)/meas*100 if meas else 0
    unit = "ppm" if abs(d)<0.01 else "%"
    val = d*1e4 if unit=="ppm" else d
    print(f"  {name:<20} VP={vp:<14.6g} 측정={meas:<14.6g} Δ={val:+.3f}{unit:>4} [{grade}] {note}")


def main():
    print("="*72)
    print("입자 기초 — p/n/e 정밀 정의 + 측정 대조 (주기율표의 토대)")
    print("="*72)

    # ════════════════ 전자 (앵커 = 유일 관찰입력) ════════════════
    section("전자 e⁻ — 유일 관찰입력 (절대척도 고정)")
    lam_C_reduced = HBARC/M["m_e_MeV"]      # 환산 콤프턴 λ_C = ħc/(m_e c²) [fm]
    Re = lam_C_reduced/2                      # 코어반경 = λ_C/2 (최소국소화 증명)
    D_pm = 2*(HBARC/M["m_e_MeV"])*1e-3 * (2*PI)  # placeholder, 아래서 정정
    # D = 2·λ_C(비환산) = 2·h/(m_e c); r_vac = D/2π²
    lam_C_full = 2*PI*lam_C_reduced          # 비환산 콤프턴 = 2π·환산
    D_fm = 2*lam_C_full                       # 양자지름 D = 2λ_C(비환산)
    r_vac = D_fm/(2*PI**2)                     # 회전진폭 r_e = D/2π²
    print(f"  m_e = {M['m_e_MeV']} MeV  [앵커/CAL] — 이 한 값이 모든 절대척도를 정함")
    print(f"  코어반경 Re = λ_C/2 = ħc/(2 m_e c²) = {Re:.3f} fm   [F, v=c 포화 최소국소화 증명]")
    print(f"  회전진폭 r_e = D/2π² = {r_vac:.1f} fm   (D=2λ_C(비환산)={D_fm:.1f} fm)   [F]")
    chk("g_e (g-인자)", 2.0, M["g_e"], "F?", "Dirac=2; 변칙 a_e=α/2π는 [O](QED)")
    print(f"  전하 = −e  [F, EM 캘리브레이션 q_eff=e 정확 — 단일상수 q_ref*로]")
    print(f"  → 전자는 기준. 양성자·중성자는 이 전자 대비 *강제 예측*(아래).")

    # ════════════════ 양성자 (강제 예측) ════════════════
    section("양성자 p⁺ — 전자 대비 강제 예측")
    mp_me_vp = 6*PI**5                         # m_p/m_e = 6π⁵ = 2π·3π⁴
    r_p_vp = D_fm/(6*PI**6)                    # r_p = D/6π⁶
    mu_p_vp = (3*PI + 7/4)/4                   # μ_p = (3π+7/4)/4
    print(f"  구조: N_p = 89 = 82(코어) + 7(껍질).  3섹터 분배 (30,30,29) [정수 최소분산 유일]")
    print(f"        7 = 1(노즐→전하 +1) + 6(균형링 = 6π⁵의 6)")
    chk("m_p/m_e = 6π⁵", mp_me_vp, M["mp_me"], "F", "= 2π·3π⁴ (n겹 법칙)")
    chk("r_p = D/6π⁶ [fm]", r_p_vp, M["r_p"], "F", "vs CODATA; vs locked 0.8412 +61ppm")
    chk("μ_p = (3π+7/4)/4", mu_p_vp, M["mu_p"], "F", "g_p=(3π+7/4)/2")
    print(f"  전하 = +e  [F]  ·  사건율 ν_p = 3π⁴ = {3*PI**4:.3f} Hz (정준; 길이경로 294 교차검증)")

    # ════════════════ 중성자 (경쟁 + 구조) ════════════════
    section("중성자 n⁰ — 양성자 대비 경쟁/구조")
    E_config = (4 + 2*DELTA)*M["m_e_MeV"]      # 미충전코어 초과 [MeV]
    E_EM = ALPHA*HBARC/(2*R_CORE)              # 양성자 노즐 자체에너지 [MeV]
    mn_mp_vp = E_config - E_EM                 # m_n − m_p [MeV] (경쟁)
    mu_n_vp = (7/4 - 3*PI)/4                   # μ_n = (7/4−3π)/4
    tau_n_vp = 89*PI**2                        # τ_n = 89π² = N_p/δ
    print(f"  구조: N_n = 82 = 82(코어, 7껍질 비움).  3섹터 분배 (28,27,27).")
    print(f"        노즐 없음 → EM-mute(q_eff=0), 순전하 0. 단 내부비틀림 누출 → μ_n≠0.")
    print(f"  질량차 [경쟁]: m_n−m_p = E_config − E_EM")
    print(f"    E_config=(4+2δ)m_e={E_config:.3f} MeV − E_EM=α_em ℏc/(2r_core)={E_EM:.3f} MeV")
    chk("m_n−m_p [MeV]", mn_mp_vp, M["mn_mp_MeV"], "F?", "두 큰 양의 미세차(경쟁)")
    chk("μ_n = (7/4−3π)/4", mu_n_vp, M["mu_n"], "F?", "g_n=(7/4−3π)/2")
    chk("τ_n = 89π² [s]", tau_n_vp, M["tau_n"], "F", "= N_p/δ; bottle법 지지(beam 888 갈림)")
    print(f"  전하 = 0  [F]  ·  붕괴 n→p+e⁻+ν̄ (S_align<임계 트리거)")

    # ════════════════ 등벡터/등스칼라 (자기 통로 닫힘) ════════════════
    section("자기 통로 — 등벡터/등스칼라 (NMR 기초)")
    chk("g_p−g_n = 3π", 3*PI, 2*M["mu_p"]-2*M["mu_n"], "F", "3섹터×π회전 (등벡터)")
    chk("g_p+g_n = 7/4", 7/4, 2*M["mu_p"]+2*M["mu_n"], "F?", "7껍질/4 (등스칼라)")

    # ════════════════ 종합 ════════════════
    section("종합 — 기초 검증표")
    print("  양        VP 닫힌형          측정          잔차      등급")
    print("  "+"-"*64)
    rows = [
        ("m_p/m_e",  "6π⁵",        mp_me_vp, M["mp_me"], "F"),
        ("r_p [fm]", "D/6π⁶",      r_p_vp, M["r_p"], "F"),
        ("μ_p [μ_N]","(3π+7/4)/4", mu_p_vp, M["mu_p"], "F"),
        ("μ_n [μ_N]","(7/4−3π)/4", mu_n_vp, M["mu_n"], "F?"),
        ("τ_n [s]",  "89π²",       tau_n_vp, M["tau_n"], "F"),
        ("m_n−m_p",  "E_cfg−E_EM", mn_mp_vp, M["mn_mp_MeV"], "F?"),
        ("g_p−g_n",  "3π",         3*PI, 2*(M["mu_p"]-M["mu_n"]), "F"),
    ]
    for name, cf, vp, meas, gr in rows:
        d = (vp-meas)/meas*100
        print(f"  {name:<9} {cf:<13} {vp:>11.5g} {meas:>11.5g}  {d:>+7.3f}%  [{gr}]")
    print("\n  핵심: 전자(1개 입력) → 양성자(6π⁵·D/6π⁶, 전부 <0.5%) → 중성자(경쟁/구조, <0.3%).")
    print("        이 기초가 주기율표의 토대다. 다음: 이 p/n/e 로 원소별 질량·반지름 예측·검증.")


if __name__ == "__main__":
    main()
