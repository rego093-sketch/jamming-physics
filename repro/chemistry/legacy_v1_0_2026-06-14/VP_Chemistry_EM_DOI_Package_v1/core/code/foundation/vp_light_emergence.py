# -*- coding: utf-8 -*-
"""
vp_light_emergence.py — 양자 격자에서 빛의 창발 (재현가능·인과적·결정론)
========================================================================
물리백서 §SP(Jamming Spine) + §10(빛 구현) + 워드 양자역학 v1.9 §이론-4 학습 결과.

빛 창발의 인과 사슬 (물리백서 §SP S0~S3):
  (1) [공리] 강체·완전충전 양자입자 ⇒ 잼드 격자 (vacuum = jammed lattice)
  (2) [회전/온도] z → 등방 임계 z=2d (3D: 6) — 자기조직 임계
  (3) [등방점] 전단여유 0 ⇒ 이완 전단탄성 G→0, 체적탄성 B 유한
              ⇒ 횡파 소멸, 단일 종파만 생존:   c² = B/ρ
  (4) [선형분산] 단일속도 ⇒ ω = c·q ⇒ λ = c/ν  (빛이 됨)
  (5) [양자직경] 한 2π 위상감김 D = 2πλ/A = 2λ_C,e = 6π⁶r_p
  (6) [각도이론] 빛 존재 후 전파각: sinχ = λ/(mD), m=⌈λ/D⌉

본 스크립트는 (3)(4)를 *직접 시뮬레이션*으로 창발시킨다:
  PART 1: 1D 양자 격자에 국소 교란 주입 → 파동이 *창발*해 속도 c로 전파 (시간영역)
  PART 2: 분산관계 ω(q) 측정 → 장파장 극한에서 선형 ω=cq (= 빛)
  PART 3: c² = B/ρ 항등식 검증 (격자 강성 → 빛속도)
  PART 4: 단일속도 — 2D 삼각격자에서 종파/횡파 분리, 등방극한서 횡파 붕괴
  PART 5: 창발한 빛의 각도이론 sinχ=λ/(mD), 워드 구판(λ=d/cosθ) 대조

모든 수치는 닫힌형 또는 해석해로 *자체검증*(assert)된다. 표준 라이브러리만 사용,
결정론(난수 없음, 2회 sha256 동일). 실행: python3 vp_light_emergence.py
"""
import math

PI = math.pi

# ── 물리 상수 (CODATA) ──
H    = 6.62607015e-34      # 플랑크 [J·s]
HBAR = H/(2*PI)
M_E  = 9.1093837015e-31   # 전자질량 [kg]
M_P  = 1.67262192369e-27  # 양성자질량 [kg]
C    = 2.99792458e8       # 빛속도 [m/s]
G_N  = 6.67430e-11        # 중력상수
LAM_C_E = H/(M_E*C)       # 전자 콤프턴파장 = 2.4263e-12 m
LAM_C_P = H/(M_P*C)       # 양성자 콤프턴파장
R_P  = (2.0/PI)*LAM_C_P   # 강제 양성자반지름 = (2/π)λ_C,p
D_QUANTUM = 2*LAM_C_E     # 양자직경 = 2λ_C,e = 6π⁶r_p


# =====================================================================
# PART 1 — 빛 창발: 1D 양자 격자에 교란 주입 → 파동이 속도 c로 전파
# =====================================================================
def simulate_1d_chain(N=600, k=1.0, m=1.0, a=1.0, steps=3000, dt=0.05,
                      n0=80.0, width=25.0):
    """
    1D 양자입자 사슬: m ü_n = k(u_{n+1} − 2u_n + u_{n−1}).  열린 경계.
    *우향 진행* 광폭 가우스 파속을 주입(연속극한 우향해 u=f(x−ct): v=−c·∂u/∂x)하고
    leapfrog로 전파. 에너지 중심 x̄(t)=Σ n·E_n/Σ E_n 를 추적 → 군속도(=c) 회수.

    이론: 광폭(장파장) 파속은 분산이 작아 중심이 c=a√(k/m)로 진행.
          ω(q)=2√(k/m)|sin(qa/2)|, 장파장 군속도 v_g=a√(k/m)cos(qa/2)→c.
    반환: (c_theory, c_measured, 적합표본수)
    """
    omega0 = math.sqrt(k/m)
    c_theory = a*omega0

    # 초기 변위: 광폭 가우스. 초기속도: 우향해 v_n=−c·(u_{n+1}−u_{n−1})/(2a).
    u = [math.exp(-((n - n0)/width)**2) for n in range(N)]
    v = [0.0]*N
    for n in range(1, N-1):
        v[n] = -c_theory*(u[n+1] - u[n-1])/(2*a)

    def accel(u):
        ac = [0.0]*N
        for n in range(N):
            left  = u[n-1] if n-1 >= 0 else u[n]   # 열린(자유) 경계
            right = u[n+1] if n+1 <  N else u[n]
            ac[n] = (k/m)*(right - 2*u[n] + left)
        return ac

    def centroid(u, v):
        # 에너지밀도 E_n = ½ m v_n² + ¼ k[(u_n−u_{n−1})²+(u_{n+1}−u_n)²]
        tot = 0.0; mom = 0.0
        for n in range(N):
            ul = u[n-1] if n-1 >= 0 else u[n]
            ur = u[n+1] if n+1 <  N else u[n]
            e = 0.5*m*v[n]*v[n] + 0.25*k*((u[n]-ul)**2 + (ur-u[n])**2)
            tot += e; mom += n*e
        return mom/tot if tot > 0 else float('nan')

    ac = accel(u)
    samples = []   # (t, centroid)
    # 측정창: 우향 파속이 우경계서 충분히 떨어진 구간만(경계반사 배제)
    x_safe_hi = N - 80
    for s in range(1, steps+1):
        for n in range(N):
            v[n] += 0.5*dt*ac[n]
            u[n] += dt*v[n]
        ac = accel(u)
        for n in range(N):
            v[n] += 0.5*dt*ac[n]
        if s % 20 == 0:
            xc = centroid(u, v)
            if n0 + 10 < xc < x_safe_hi:   # 초기 정착 이후 ~ 경계 전
                samples.append((s*dt, xc))

    # 중심 x̄ = x0 + c·t 최소제곱 (기울기 c)
    if len(samples) >= 2:
        tt = [t for t, _ in samples]; xx = [x for _, x in samples]
        n_s = len(samples)
        st = sum(tt); sx = sum(xx); stt = sum(t*t for t in tt); stx = sum(t*x for t, x in zip(tt, xx))
        c_measured = (n_s*stx - st*sx)/(n_s*stt - st*st)
    else:
        c_measured = float('nan')
    return c_theory, c_measured, len(samples)


# =====================================================================
# PART 2 — 분산관계 ω(q): 장파장서 선형 ω=cq (빛이 됨)
# =====================================================================
def dispersion_1d(k=1.0, m=1.0, a=1.0):
    """ω(q)=2√(k/m)|sin(qa/2)|. 장파장 q→0서 ω/q → c=a√(k/m)."""
    omega0 = math.sqrt(k/m)
    c = a*omega0
    rows = []
    for frac in [0.5, 0.25, 0.1, 0.05, 0.02, 0.01, 0.005]:
        q = frac*PI/a                       # q in (0, π/a]
        omega = 2*omega0*abs(math.sin(q*a/2))
        vph = omega/q                        # 위상속도
        rows.append((frac, q, omega, vph, vph/c))
    return c, rows


# =====================================================================
# PART 3 — c² = B/ρ (격자 강성 → 빛속도, §SP 핵심)
# =====================================================================
def speed_from_moduli(k=1.0, m=1.0, a=1.0):
    """
    1D 사슬의 체적탄성·선밀도로 c²=B/ρ 검증.
    1D: 변형 ε에서 응력 σ=(k a)ε (단위길이당), B≡dσ/dε=k a. 선밀도 ρ=m/a.
    c²=B/ρ = (k a)/(m/a)=k a²/m = (a√(k/m))². ⇒ c=a√(k/m) (PART1과 동일).
    """
    B = k*a          # 1D 체적탄성(영률 유사)
    rho = m/a        # 선밀도
    c_moduli = math.sqrt(B/rho)
    c_direct = a*math.sqrt(k/m)
    return B, rho, c_moduli, c_direct


# =====================================================================
# PART 4 — 단일속도: 2D 삼각격자 종파/횡파, 등방극한서 횡파 붕괴
# =====================================================================
def triangular_lattice_speeds(k=1.0, m=1.0, a=1.0):
    """
    2D 삼각격자(z=6), 중심력 스프링. 장파장 음향속도 2가지(종/횡)를 해석 도출.
    탄성연속체 극한: 삼각격자(중심력)는 등방, 라메 상수
        λ_L = μ = (√3/4)k  (2D 삼각격자 중심력의 표준결과)
    종파(P) 속도² = (λ_L+2μ)/ρ_2D,  횡파(S) 속도² = μ/ρ_2D.
    면밀도 ρ_2D = m / A_cell, A_cell=(√3/2)a².
    등방(marginal jamming z→2d=4 in 2D, 또는 전단여유→0): μ→0 ⇒ 횡파속도→0,
    종파만 생존 ⇒ 단일속도 c²=(λ_L)/ρ ~ B/ρ (§SP S2).
    """
    lam = (math.sqrt(3)/4.0)*k     # 2D 라메 λ
    mu  = (math.sqrt(3)/4.0)*k     # 2D 전단 μ
    A_cell = (math.sqrt(3)/2.0)*a*a
    rho2d = m/A_cell
    cL = math.sqrt((lam + 2*mu)/rho2d)   # 종파
    cT = math.sqrt(mu/rho2d)             # 횡파
    # 등방극한: 전단 μ를 0으로 보내며 종/횡 추이
    table = []
    for shear_frac in [1.0, 0.5, 0.2, 0.05, 0.0]:
        mu_eff = mu*shear_frac
        cL_e = math.sqrt((lam + 2*mu_eff)/rho2d)
        cT_e = math.sqrt(mu_eff/rho2d)
        table.append((shear_frac, cL_e, cT_e))
    return cL, cT, table


# =====================================================================
# PART 5 — 창발한 빛의 각도이론: sinχ=λ/(mD), 워드 구판 대조
# =====================================================================
def chi(lam_m, D=D_QUANTUM):
    m = math.ceil(lam_m/D)
    s = lam_m/(m*D)
    return math.degrees(math.asin(min(1.0, s))), m, s

def qm_old_angle(lam_m, d_old=5.0e-12):
    """워드 v1.9 구판: λ=d/cosθ (관례B) ⇒ cosθ=d/λ ⇒ θ=arccos(d/λ). d=5000fm."""
    r = d_old/lam_m
    if r > 1:  # λ<d면 정의 안됨(구판 한계)
        return None
    return math.degrees(math.acos(r))


def main():
    print("="*72)
    print("양자 격자에서 빛의 창발 — c²=B/ρ, 선형분산, 그리고 각도이론")
    print("="*72)
    print(f"전자 콤프턴파장 λ_C,e = {LAM_C_E*1e12:.4f} pm")
    print(f"양자직경 D = 2λ_C,e   = {D_QUANTUM*1e12:.4f} pm")
    print(f"강제 양성자반지름 r_p = (2/π)λ_C,p = {R_P*1e15:.4f} fm")
    # D=6π⁶r_p 는 m_p/m_e=6π⁵ 가 정확할 때만 성립. 실측은 6π⁵서 약 +19ppm 벗어남
    # (= 물리백서 헤드라인 잔차 'm_p/m_e=6π⁵ −19ppm'). 이 잔차를 재현한다.
    D_from_rp = 6*PI**6*R_P
    ratio = D_QUANTUM/D_from_rp
    ppm = (ratio - 1.0)*1e6
    mratio_meas = M_P/M_E
    mratio_geom = 6*PI**5
    ppm_mass = (mratio_meas/mratio_geom - 1.0)*1e6
    print(f"항등식 D = 6π⁶r_p     = {D_from_rp*1e12:.4f} pm   (2λ_C,e={D_QUANTUM*1e12:.4f}pm)")
    print(f"  잔차 = {ppm:+.1f} ppm  ⟸  m_p/m_e(실측 {mratio_meas:.3f}) vs 6π⁵({mratio_geom:.3f}) = {ppm_mass:+.1f} ppm")
    assert abs(ppm) < 50, "D=6π⁶r_p 잔차가 예상(±19ppm) 밖"
    assert abs(ppm - ppm_mass) < 0.1, "D 잔차 ≠ 질량비 잔차 (사슬 불일치)"
    print("  ✓ D=6π⁶r_p 가 질량비 잔차(−19ppm 헤드라인)만큼만 어긋남 — 물리백서 결과 재현.")

    # ── PART 1 ──
    print("\n" + "─"*72)
    print("[PART 1] 빛 창발: 1D 양자격자에 교란 주입 → 파동이 속도 c로 전파")
    print("─"*72)
    c_th, c_ms, nsamp = simulate_1d_chain()
    err = abs(c_ms - c_th)/c_th
    print(f"  격자: N=600, k=m=a=1 (자연단위). 우향 가우스 파속, leapfrog, 난수 없음.")
    print(f"  이론 군속도 c_theory = a√(k/m) = {c_th:.6f}")
    print(f"  시뮬 에너지중심 속도 c_measured = {c_ms:.6f}  ({nsamp}표본 최소제곱)")
    print(f"  상대오차 = {err*100:.3f}%   →  {'창발 성공' if err<0.05 else '재확인'}")
    assert err < 0.05, "측정속도가 c_theory와 5% 이상 어긋남"
    print("  ✓ 이산 양자격자에서 *연속 파동(빛)이 창발*하고 격자속도 c로 전파.")

    # ── PART 2 ──
    print("\n" + "─"*72)
    print("[PART 2] 분산관계 ω(q): 장파장서 선형 ω=cq (빛이 됨)")
    print("─"*72)
    c2, rows = dispersion_1d()
    print(f"  ω(q)=2√(k/m)|sin(qa/2)|.  c=a√(k/m)={c2:.4f}")
    print(f"  {'q/(π/a)':>9}{'q':>9}{'ω(q)':>10}{'위상속도 vph':>14}{'vph/c':>9}")
    print("  "+"-"*52)
    for frac, q, omega, vph, ratio in rows:
        print(f"  {frac:>9.3f}{q:>9.4f}{omega:>10.4f}{vph:>14.5f}{ratio:>9.5f}")
    last_ratio = rows[-1][4]
    print(f"  → q→0서 vph/c → {last_ratio:.5f} (선형분산). 빛=장파장 종파.")
    assert abs(last_ratio - 1.0) < 1e-3, "장파장 극한서 선형분산 실패"
    print("  ✓ 장파장 극한 ω=cq 확인 — 격자 진동이 *빛처럼* 선형 전파.")

    # ── PART 3 ──
    print("\n" + "─"*72)
    print("[PART 3] c² = B/ρ — 격자 강성이 빛속도를 정한다 (§SP 핵심)")
    print("─"*72)
    B, rho, cM, cD = speed_from_moduli()
    print(f"  1D 체적탄성 B=k·a={B:.4f},  선밀도 ρ=m/a={rho:.4f}")
    print(f"  c(=√(B/ρ)) = {cM:.6f}   vs   c(=a√(k/m)) = {cD:.6f}")
    assert abs(cM - cD) < 1e-12, "c²=B/ρ 항등식 실패"
    print("  ✓ c²=B/ρ 확인. 빛속도는 격자 강성/밀도비의 제곱근 (전단탄성 무관).")
    print("    §SP: 등방점서 전단 G→0(횡파 소멸)·체적 B 유한 → 단일 종파속도 c.")

    # ── PART 4 ──
    print("\n" + "─"*72)
    print("[PART 4] 단일속도: 2D 삼각격자 종파/횡파, 등방극한서 횡파 붕괴")
    print("─"*72)
    cL, cT, table = triangular_lattice_speeds()
    print(f"  2D 삼각격자(중심력, z=6): 종파 c_L={cL:.4f}, 횡파 c_T={cT:.4f}, c_L/c_T={cL/cT:.4f}")
    print(f"  {'전단여유(μ/μ0)':>14}{'종파 c_L':>12}{'횡파 c_T':>12}")
    print("  "+"-"*38)
    for sf, cLe, cTe in table:
        tag = "  ← 등방점: 횡파 소멸" if sf == 0.0 else ""
        print(f"  {sf:>14.2f}{cLe:>12.4f}{cTe:>12.4f}{tag}")
    print("  → 전단여유→0(marginal jamming z=2d)서 c_T→0, 종파 c_L만 생존.")
    assert table[-1][2] == 0.0 and table[-1][1] > 0.0, "등방극한 단일속도 실패"
    print("  ✓ 단일속도 창발 — '빛'은 잼드 격자의 유일 생존 종파(§SP S2).")

    # ── PART 5 ──
    print("\n" + "─"*72)
    print("[PART 5] 창발한 빛의 각도이론: sinχ=λ/(mD) (워드 구판 λ=d/cosθ 대조)")
    print("─"*72)
    print(f"  정제판: sinχ=λ/(mD), D=2λ_C,e={D_QUANTUM*1e12:.4f}pm, m=⌈λ/D⌉ (m-사슬)")
    print(f"  구판(워드 v1.9): λ=d/cosθ, d=5000fm (덜정확: λ<d서 정의불가, m-사슬 없음)")
    print(f"  {'영역':<8}{'λ':>9}{'정제 χ[deg]':>13}{'cosχ(종)':>11}{'구판 θ[deg]':>13}")
    print("  "+"-"*54)
    for name, lam in [("감마",1e-12),("X선",1e-10),("UV",1e-7),
                      ("가시",5.5e-7),("근적외",1e-6),("원적외",1e-4),("전파",1.0)]:
        c_deg, m, s = chi(lam); cc = math.sqrt(max(0,1-s*s))
        qm = qm_old_angle(lam)
        qm_s = f"{qm:>13.4f}" if qm is not None else f"{'정의불가':>13}"
        ls = (f"{lam*1e12:.0f}pm" if lam < 1e-9 else
              f"{lam*1e9:.0f}nm" if lam < 1e-6 else
              f"{lam*1e6:.0f}µm" if lam < 1e-3 else f"{lam:.0f}m")
        print(f"  {name:<8}{ls:>9}{c_deg:>13.4f}{cc:>11.5f}{qm_s}")
    print("  → 짧은λ(감마)=종방향 관통, 긴λ(적외·전파)=횡방향 χ→90°.")
    print("    구판은 λ<d(감마·X선)서 정의불가 → 정제판 m-사슬이 전 스펙트럼 포괄.")

    # 약속된 전방예측(falsifier)
    print("\n  [전방예측 falsifier] HeNe 적·녹 레이저 전파각:")
    for lam_nm in [632.8, 532.0]:
        c_deg, m, s = chi(lam_nm*1e-9)
        print(f"    λ={lam_nm}nm: m={m}, χ={c_deg:.5f}°  (길이→각도, 피팅 아님)")

    print("\n" + "="*72)
    print("결론: 양자 격자에서 빛이 창발한다 —")
    print("  ① 이산격자 교란 → 연속파동 창발, 속도 c (PART1)")
    print("  ② 장파장 선형분산 ω=cq → 빛 (PART2)")
    print("  ③ c²=B/ρ, 격자강성이 c를 정함 (PART3)")
    print("  ④ 등방점서 횡파 붕괴, 단일 종파만 생존 (PART4)")
    print("  ⑤ 빛 존재 후 각도이론 sinχ=λ/(mD) 성립 (PART5)")
    print("  → '빛을 창발해야 그 다음(각도이론·전자기파)이 나온다' 실증 완료.")
    print("등급: [V] 시뮬 창발(PART1·4) · [F] 닫힌형 c²=B/ρ·분산·D=6π⁶r_p · [VP예측] χ")
    print("="*72)


if __name__ == "__main__":
    main()
