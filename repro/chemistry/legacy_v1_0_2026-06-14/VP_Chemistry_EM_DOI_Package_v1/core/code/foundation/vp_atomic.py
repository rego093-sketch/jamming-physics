# -*- coding: utf-8 -*-
"""
vp_atomic.py — VP 전자 구조: 원자 척도·이온화·껍질 (재현가능·인과적)
====================================================================
목적: 주기율표의 *전자 쪽* 토대. 원자 척도(Bohr 반지름·Rydberg)가 전자 앵커 + EM 1/r²에서
      나오고(통합이론서 e-p 결합 E(r;L) 최소점), 각운동량 껍질구조가 주기(period)를 만든다.

인과 사슬:
  전자 앵커 λ_C + EM 1/r² → e-p 쿨롱 결합 E(r)=L²/2μr² − κ/r (κ=αℏc)
    → 최소점 r* = a₀ = λ_C/α (Bohr 반지름),  E(r*) = −α²m_e c²/2 = −Ry (Rydberg)
  각운동량 (2l+1) 상태 × 2(스핀) → 부껍질 용량 2,6,10,14 → 주기 2,8,8,18,18,32.

등급: [F] 원자 척도 a₀·Ry (앵커+EM, <0.01%) · [F] 수소형 이온 (정확) ·
      [F?] 껍질 용량/주기 (각운동량; VP 회전 정합) · [O] 다전자 절대 IE/반지름(완전 다체).
실행: python3 vp_atomic.py   (표준 라이브러리만)
"""
import math
PI = math.pi

# ── 전자 앵커 + EM (vp_particles.py 와 동일 SSOT) ──
M_E_MEV = 0.51099895                 # 전자질량 [MeV] (앵커)
HBARC   = 197.3269804                # ℏc [MeV·fm]
ALPHA   = 1/137.035999               # α_em (EM 결합)
LAM_C   = HBARC/M_E_MEV              # 환산 콤프턴 λ_C = ħc/(m_e c²) [fm] = 386.16

# ── VP 원자 척도 (e-p 쿨롱 결합 최소점에서) ──
A0_FM = LAM_C/ALPHA                  # Bohr 반지름 a₀ = λ_C/α  [fm]
A0_A  = A0_FM*1e-5                   # → Å
RY_EV = ALPHA**2 * M_E_MEV*1e6 / 2   # Rydberg = α²m_e c²/2  [eV]


def hydrogenic(Z, n=1):
    """수소형 이온(전자 1개): 이온화에너지 [eV], 반지름 [Å]."""
    IE = RY_EV * Z**2 / n**2
    r  = A0_A * n**2 / Z
    return IE, r

# 부껍질 용량 = 2(2l+1):  s,p,d,f
SUBSHELL = {"s":2, "p":6, "d":10, "f":14}
# Aufbau 채움 순서 (n+l 규칙)
AUFBAU = ["1s","2s","2p","3s","3p","4s","3d","4p","5s","4d","5p",
          "6s","4f","5d","6p","7s","5f","6d","7p"]


def main():
    print("="*72)
    print("VP 전자 구조 — 원자 척도(앵커+EM)와 껍질구조(각운동량)가 주기율표를 만든다")
    print("="*72)

    # ── 원자 척도 유도 ──
    print("\n[원자 척도] e-p 쿨롱 결합(EM 1/r²) 최소점에서 (통합이론서 E(r;L))")
    print(f"  Bohr 반지름  a₀ = λ_C/α = {A0_A:.6f} Å    측정 0.529177 Å   Δ={(A0_A-0.529177)/0.529177*100:+.4f}%  [F]")
    print(f"  Rydberg      Ry = α²m_e c²/2 = {RY_EV:.4f} eV   측정 13.6057 eV  Δ={(RY_EV-13.6057)/13.6057*100:+.4f}%  [F]")
    print(f"  → 둘 다 전자 앵커(λ_C) + EM 결합(α)만으로. 핵·재료와 같은 단일입력+EM 구조.")

    # ── 수소형 이온 (정확) ──
    print("\n[수소형 이온] 전자 1개 — IE=Ry·Z², r=a₀/Z (정확)")
    print(f"  {'이온':<8}{'Z':>3} {'IE예측[eV]':>11} {'IE측정[eV]':>11} {'r[Å]':>8}")
    print("  "+"-"*48)
    hion = [("H",1,13.598),("He⁺",2,54.418),("Li²⁺",3,122.45),
            ("Be³⁺",4,217.72),("B⁴⁺",5,340.23),("C⁵⁺",6,489.99)]
    for name, Z, IE_meas in hion:
        IE, r = hydrogenic(Z)
        d = (IE-IE_meas)/IE_meas*100
        print(f"  {name:<8}{Z:>3} {IE:>11.2f} {IE_meas:>11.2f} {r:>8.4f}   Δ={d:+.2f}%")
    print("  → 수소형(단일전자)은 정확. Z² 법칙은 순수 EM 1/r². [F]")

    # ── 껍질 구조 → 주기 ──
    print("\n[껍질 구조] 각운동량 (2l+1)×2 → 부껍질 용량 → 주기율표 구조")
    print(f"  부껍질 용량 2(2l+1):  s={SUBSHELL['s']} p={SUBSHELL['p']} d={SUBSHELL['d']} f={SUBSHELL['f']}")
    cum = 0; nobles = []; period_ends = []
    print(f"  Aufbau 채움 순서 (n+l 규칙):")
    line = "    "
    for orb in AUFBAU:
        cap = SUBSHELL[orb[1]]
        cum += cap
        line += f"{orb}({cap}) "
        if orb[1] == "p" or orb == "1s":   # 주기 끝 = np (또는 1s)
            nobles.append(cum); period_ends.append(orb)
    print(line)
    print(f"\n  비활성기체 Z(주기 끝): {nobles}")
    print(f"  측정 비활성기체:       [2, 10, 18, 36, 54, 86, 118]")
    match = nobles == [2,10,18,36,54,86,118]
    print(f"  → {'완전 일치 ✓' if match else '불일치'}. 주기 길이 2,8,8,18,18,32,32 가 부껍질 채움에서 나온다. [F?]")

    # ── 주기 길이 ──
    print("\n[주기 길이] = 비활성기체 간격")
    plens = [nobles[0]] + [nobles[i]-nobles[i-1] for i in range(1,len(nobles))]
    print(f"  예측 주기 길이: {plens}")
    print(f"  측정:          [2, 8, 8, 18, 18, 32, 32]")
    print(f"  → 2·⌈(n+1)/2⌉² 패턴. s→p→d→f 채움이 2,8,18,32 용량을 단계적으로 연다.")

    # ── 다전자 절대값은 [O] ──
    print("\n[한계 — 정직] 다전자 중성원자 절대 IE/반지름")
    print("  • 단순 Z_eff(슬레이터)로 다전자 IE 예측 시 외곽전자 차폐 과소→절대값 크게 빗나감(Ne 116 vs 22).")
    print("  • 절대 IE/반지름은 완전 다체 문제 → [O]. 단, 주기 구조·수소형은 [F].")
    print("  • 즉 주기율표의 '뼈대'(주기·껍질·척도)는 VP, '살'(다전자 미세값)은 추가 다체물리.")

    print("\n" + "="*72)
    print("등급: [F] a₀=λ_C/α·Ry=α²m_ec²/2 (앵커+EM, <0.01%) · [F] 수소형 Z² (정확)")
    print("      [F?] 껍질용량/주기 (각운동량 (2l+1)×2; VP 구면회전 정합) · [O] 다전자 절대값")
    print("      핵심: 전자쪽 토대(척도+주기)가 핵쪽 토대(p/n/e)와 같은 전자앵커+EM에서 선다.")
    print("="*72)


if __name__ == "__main__":
    main()
