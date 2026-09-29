# -*- coding: utf-8 -*-
"""
vp_statistical_thermo.py — VP 통계열역학: 회전에너지에서 온도의존 (재현가능·인과적)
====================================================================
사용자 지침: 회전에너지(온도)를 잘 계산하면서. vp_thermal(회전상수 B)을 엄밀히 확장.

핵심: 온도 = 회전에너지 척도. 회전·진동 모드는 kT가 준위간격 넘을 때 깨어난다.
      회전 분배함수에서 열용량 C_v(T)를 엄밀 계산 → H2의 유명한 계단
      (저온 3/2R → 회전 깨어남 5/2R → 진동 깨어남 7/2R).

인과 사슬: 회전준위 E_J=B·hc·J(J+1) (B는 VP 결합기하, vp_thermal) → 분배함수 q_rot →
           열용량 C_v=(⟨E²⟩−⟨E⟩²)/kT² (요동공식, 엄밀). 진동은 아인슈타인.
           활성화온도 T_rot=B·hc/k, T_vib=ν·hc/k.

등급: [F] C_v(T) 회전·진동 활성화(분배함수, 요동공식) · [F] 활성화온도(VP B에서) ·
      [F?] 엔트로피(Sackur-Tetrode+회전+진동) · [O] H2 오르토/파라(핵스핀 통계)
실행: python3 vp_statistical_thermo.py   (표준 라이브러리만)
"""
import math
R = 8.314462; KB = 1.380649e-23; H = 6.62607015e-34; C_CM = 2.99792458e10
NA = 6.02214076e23; HC_K = H*C_CM/KB     # = 1.4388 cm·K (hc/k)

def cv_rot(T, B_cm, sigma):
    """회전 열용량 [J/mol·K] — 준위 합 + 요동공식 (엄밀, 선형분자)."""
    if T <= 0: return 0.0
    Jmax = max(20, int(8*math.sqrt(T/(HC_K*B_cm))+10))
    q=Z1=Z2=0.0
    for J in range(0, Jmax):
        E = B_cm*HC_K*J*(J+1)            # E/k [K]
        g = 2*J+1
        w = g*math.exp(-E/T)
        q += w; Z1 += w*E; Z2 += w*E*E
    Eavg = Z1/q; E2avg = Z2/q
    var = E2avg - Eavg*Eavg              # (ΔE/k)² [K²]
    return R * var/(T*T)                 # C_v,rot/R · R

def cv_vib(T, nu_cm):
    """진동 열용량 [J/mol·K] — 아인슈타인."""
    if T <= 0: return 0.0
    x = nu_cm*HC_K/T                      # θ_v/T
    if x > 50: return 0.0
    ex = math.exp(x)
    return R * x*x*ex/(ex-1)**2

def cv_total(T, B_cm, nu_cm, sigma):
    """총 C_v = 병진(3/2R) + 회전 + 진동."""
    return 1.5*R + cv_rot(T,B_cm,sigma) + cv_vib(T,nu_cm)

# 분자 상수 (B,ν from VP 결합기하; vp_thermal과 일관). g_el=전자바닥 겹침수
MOLS = {
 "H2":  dict(B=60.85, nu=4401, sigma=2, mass=2.016,  g_el=1),
 "N2":  dict(B=2.00,  nu=2359, sigma=2, mass=28.01,  g_el=1),
 "CO":  dict(B=1.93,  nu=2170, sigma=1, mass=28.01,  g_el=1),
 "O2":  dict(B=1.44,  nu=1580, sigma=2, mass=32.00,  g_el=3),  # 삼중항(상자성, 홀전자 2)
}


def main():
    print("="*72)
    print("VP 통계열역학 — 회전에너지에서 온도의존 (온도=회전에너지 척도)")
    print("="*72)
    print(f"\nhc/k = {HC_K:.4f} cm·K. 활성화온도 T_rot=B·hc/k, T_vib=ν·hc/k.")

    # ── 활성화 온도 ──
    print("\n[활성화 온도] 모드는 kT > 준위간격일 때 깨어난다")
    print(f"  {'분자':<5}{'B[cm⁻¹]':>9}{'T_rot[K]':>9}{'ν[cm⁻¹]':>9}{'T_vib[K]':>9}")
    print("  "+"-"*42)
    for name,d in MOLS.items():
        Trot=d['B']*HC_K; Tvib=d['nu']*HC_K
        print(f"  {name:<5}{d['B']:>9.2f}{Trot:>9.1f}{d['nu']:>9}{Tvib:>9.0f}")
    print("  → H2: 회전 88K·진동 6332K. N2: 회전 2.9K·진동 3394K (회전은 극저온서도 활성).")

    # ── H2 열용량 계단 (엄밀 계산) ──
    print("\n[H2 열용량 C_v(T)] 회전·진동 활성화 계단 (분배함수 엄밀)")
    d = MOLS["H2"]
    print(f"  {'T[K]':>7}{'C_v/R':>8}{'C_v[J/molK]':>13}  상태")
    print("  "+"-"*44)
    for T in [20, 50, 88, 150, 298, 1000, 3000, 6332, 10000]:
        cv = cv_total(T, d['B'], d['nu'], d['sigma'])
        state = ("병진만" if cv<1.7*R else "병진+회전" if cv<3.2*R else "병진+회전+진동")
        print(f"  {T:>7}{cv/R:>8.2f}{cv:>13.2f}  {state}")
    print("  → 20K(3/2R 병진만) → 298K(5/2R +회전) → 10000K(7/2R +진동). 계단 재현. [F]")
    print("    회전 활성화(~88K)·진동 활성화(~6332K)가 VP 결합기하의 B·ν에서 직접.")

    # ── 검증: 298K 열용량 ──
    print("\n[검증] 상온(298K) C_v 예측 vs 실측 [J/mol·K]")
    meas = {"H2":20.4,"N2":20.8,"CO":20.8,"O2":21.0}
    for name,d in MOLS.items():
        cv = cv_total(298, d['B'], d['nu'], d['sigma'])
        print(f"  {name:<5} 예측 {cv:.2f} / 실측 {meas[name]:.1f}  Δ={(cv-meas[name])/meas[name]*100:+.1f}%")
    print("  → 상온서 이원자분자 C_v≈5/2R=20.8 (회전 활성, 진동 동결). 일치.")

    # ── 엔트로피 (Sackur-Tetrode + 회전 + 진동) ──
    print("\n[엔트로피] S = S_병진(Sackur-Tetrode) + S_회전 + S_진동  (298K, 1bar)")
    print(f"  {'분자':<5}{'S예측':>9}{'S실측':>9}{'[J/molK]':>10}")
    print("  "+"-"*34)
    Smeas = {"H2":130.7,"N2":191.6,"CO":197.7,"O2":205.2}
    for name,d in MOLS.items():
        m = d['mass']/1000/NA; T=298.15; P=1e5
        # 병진 (Sackur-Tetrode)
        S_tr = R*(math.log((2*math.pi*m*KB*T/H**2)**1.5 * KB*T/P) + 2.5)
        # 회전 (선형, 고온)
        Trot = d['B']*HC_K
        S_rot = R*(math.log(T/(d['sigma']*Trot)) + 1)
        # 진동 (대개 작음)
        x = d['nu']*HC_K/T
        S_vib = R*(x/(math.exp(x)-1) - math.log(1-math.exp(-x))) if x<50 else 0.0
        # 전자 겹침 (O2 삼중항 등)
        S_el = R*math.log(d['g_el'])
        S = S_tr + S_rot + S_vib + S_el
        note = " (전자겹침 Rln3)" if d['g_el']>1 else ""
        print(f"  {name:<5}{S:>9.1f}{Smeas[name]:>9.1f}  Δ={(S-Smeas[name])/Smeas[name]*100:+.1f}%{note}")
    print("  → 표준 몰엔트로피가 회전·진동·병진·전자 분배함수에서. O2 삼중항(상자성) 반영. [F?]")

    # ── VP 통일 ──
    print("\n[VP 통일] 온도 = 회전에너지 척도, 엄밀히")
    print("  • 온도 T가 회전준위 간격(B) 넘으면 회전 활성, 진동준위(ν) 넘으면 진동 활성.")
    print("  • C_v(T) 계단 = 회전·진동 자유도가 온도 따라 깨어남. 모두 회전에너지(vp_thermal).")
    print("  • 엔트로피·자유에너지도 회전·진동 분배함수에서 → 화학평형의 통계적 기초.")
    print("  • 빛(회전양자 횡파, vp_light_angle)·열(회전 들뜸)·온도가 하나의 회전 위에.")

    print("\n" + "="*72)
    print("등급: [F] C_v(T) 회전·진동 활성화 계단(분배함수 요동공식, 엄밀)")
    print("      [F] 활성화온도(VP B·ν에서) · [F?] 표준 엔트로피(Sackur-Tetrode+회전+진동)")
    print("      [O] H2 오르토/파라(핵스핀 통계) · 핵심: 온도=회전에너지 척도, 엄밀 계산.")
    print("="*72)


if __name__ == "__main__":
    main()
