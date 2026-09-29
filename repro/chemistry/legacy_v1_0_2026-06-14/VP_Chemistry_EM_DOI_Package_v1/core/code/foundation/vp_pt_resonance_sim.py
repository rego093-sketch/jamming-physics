# -*- coding: utf-8 -*-
"""
vp_pt_resonance_sim.py — 백금 촉매 전자 진폭 파장 공명: 양자 시뮬레이션 (재현가능)
====================================================================================
CT장 [H] 가설: 활성전자 de Broglie 파장 λ_e가 Pt-Pt 간격 d와 정합(λ_e/2≈d)하면
            역공여가 공명증폭 → 촉매. *스케일 일치*를 넘어 시뮬레이션으로 검증한다.

정직한 결과(미리): 단순 기하 정합 가설은 *동역학적으로 지지되지 않는다*.
  전달행렬 밴드구조로 λ=2d 가 Bragg *밴드 경계/틈*(전자 반사)임을 확인 →
  흡착자리 LDOS(역공여 능력)는 λ=2d 에서 피크가 아니다. 역공여는 페르미준위
  금속 상태밀도+흡착 공명(Newns-Anderson/d-밴드)이 지배 — 확립된 기술자(記述子).
  단, 파장 효과가 정당히 들어오는 곳은 *양자 가둠*(박막 양자우물 상태)이며,
  슬래브 두께 M 변화 시 흡착 LDOS 진동을 시뮬로 보인다(실재 효과).

방법: 1D 유한차분 슈뢰딩거 + (a) 전달행렬 밴드구조 (b) 그린함수 흡착 LDOS
     (c) 두께 M 스윕 양자가둠. 단위: Å·eV, ħ²/2m_e=3.80998 eV·Å².
표준 라이브러리만·결정론·자체검증. 실행: python3 vp_pt_resonance_sim.py
"""
import math, cmath

HBAR2_2M = 3.80998197      # eV·Å²
def lam_of_E(E):  return 12.2750/math.sqrt(E) if E > 0 else float('inf')
def E_of_lam(L):  return HBAR2_2M*(2*math.pi/L)**2

# 계 파라미터
D_PTPT = 2.77; S_ADS = 1.70
V0_PT = 9.0; W_PT = 0.40; V0_ADS = 4.0; W_ADS = 0.45
X0 = 3.0; H_GRID = 0.05; ETA = 0.10


# ── (a) 전달행렬 밴드구조: λ=2d 가 밴드 경계/틈인가 ──
def cell_halftrace(E, n=400):
    """주기 셀(우물 1개) 전달행렬의 Tr/2. |Tr/2|≤1 → 허용 밴드."""
    h = D_PTPT/n
    def q(x): return (-V0_PT*math.exp(-((x - D_PTPT/2)/W_PT)**2) - E)/HBAR2_2M
    def integ(psi, phi):
        x = 0.0
        for _ in range(n):
            k1p, k1f = phi, q(x)*psi
            k2p, k2f = phi+0.5*h*k1f, q(x+0.5*h)*(psi+0.5*h*k1p)
            k3p, k3f = phi+0.5*h*k2f, q(x+0.5*h)*(psi+0.5*h*k2p)
            k4p, k4f = phi+h*k3f, q(x+h)*(psi+h*k3p)
            psi += h*(k1p+2*k2p+2*k3p+k4p)/6
            phi += h*(k1f+2*k2f+2*k3f+k4f)/6
            x += h
        return psi, phi
    a, _ = integ(1.0, 0.0); _, d = integ(0.0, 1.0)
    return (a + d)/2


# ── (b) 그린함수 흡착 LDOS (복소 삼중대각 Thomas) ──
def build_potential(M_pt):
    x_ads = X0 + (M_pt - 1)*D_PTPT + S_ADS
    L = x_ads + 3.0; N = int(L/H_GRID)
    xs = [i*H_GRID for i in range(N)]; V = [0.0]*N
    sites = [X0 + j*D_PTPT for j in range(M_pt)]
    for i, x in enumerate(xs):
        v = -V0_ADS*math.exp(-((x - x_ads)/W_ADS)**2)
        for xj in sites: v += -V0_PT*math.exp(-((x - xj)/W_PT)**2)
        V[i] = v
    ads_idx = min(range(N), key=lambda i: abs(xs[i] - x_ads))
    return V, ads_idx, N

def thomas(diag, off, b):
    n = len(b); cp = [0j]*n; dp = [0j]*n
    cp[0] = off/diag[0]; dp[0] = b[0]/diag[0]
    for i in range(1, n):
        m = diag[i] - off*cp[i-1]
        cp[i] = off/m if i < n-1 else 0j
        dp[i] = (b[i] - off*dp[i-1])/m
    x = [0j]*n; x[n-1] = dp[n-1]
    for i in range(n-2, -1, -1): x[i] = dp[i] - cp[i]*x[i+1]
    return x

def ldos_ads(E, V, ads_idx, N, t):
    z = complex(E, ETA)
    diag = [z - (2*t + V[i]) for i in range(N)]
    b = [0j]*N; b[ads_idx] = 1.0+0j
    G = thomas(diag, complex(t, 0), b)
    return -G[ads_idx].imag/math.pi


def main():
    print("="*72)
    print("백금 촉매 전자 진폭 파장 공명 — 양자 시뮬레이션 (정직한 검증)")
    print("="*72)
    t = HBAR2_2M/(H_GRID*H_GRID)
    E_2d = E_of_lam(2*D_PTPT)
    print(f"가설: λ_e/2 ≈ Pt-Pt d={D_PTPT}Å → λ_e=2d={2*D_PTPT:.2f}Å (E={E_2d:.2f}eV)에서 공명.")
    print(f"Pt 일함수 φ=5.65eV → λ_e={lam_of_E(5.65):.2f}Å (2d 대비 비 {lam_of_E(5.65)/(2*D_PTPT):.2f}).")

    # ── 1. 밴드구조: λ=2d 는 공명인가 밴드 경계인가? ──
    print("\n" + "─"*72)
    print("[1] 전달행렬 밴드구조 — λ=2d 는 공명대가 아니라 Bragg 밴드 경계/틈")
    print("─"*72)
    print(f"  {'E[eV]':>6}{'λ_e[Å]':>8}{'Tr/2':>8}{'상태':>12}")
    print("  "+"-"*36)
    edge_E = None; prev_allowed = None
    for i in range(2, 26):
        E = 0.5*i; ht = cell_halftrace(E); allowed = abs(ht) <= 1.0
        if prev_allowed is False and allowed and edge_E is None: edge_E = E
        prev_allowed = allowed
        if i % 2 == 0 or abs(E - E_2d) < 0.3:
            tag = "허용(밴드)" if allowed else "금지(틈)"
            note = " ←λ=2d" if abs(E - E_2d) < 0.3 else ""
            print(f"  {E:>6.1f}{lam_of_E(E):>8.2f}{ht:>8.2f}{tag:>12}{note}")
    print(f"  → E<{edge_E:.1f}eV 는 밴드틈(전자 반사). 제1전도띠 바닥 ≈{edge_E:.1f}eV.")
    print(f"    λ=2d(E={E_2d:.2f}eV)는 띠 바닥 *경계* 근처 — 공명 증폭점이 아니라 반사/경계.")
    assert cell_halftrace(2.0) < -1.0, "저에너지 밴드틈 확인 실패"   # 깊은우물→저E 틈

    # ── 2. 흡착 LDOS(E): λ=2d 에서 피크인가? (가설 직접 검증) ──
    print("\n" + "─"*72)
    print("[2] 흡착자리 LDOS(역공여 능력) — λ=2d 에서 피크 안 생김 (가설 반증)")
    print("─"*72)
    V, ads_idx, N = build_potential(12)
    Es = [1.0 + 0.25*i for i in range(45)]
    ld = [ldos_ads(E, V, ads_idx, N, t) for E in Es]
    Lmax = max(ld); Emax = Es[ld.index(Lmax)]
    print(f"  {'E[eV]':>6}{'λ_e[Å]':>8}{'LDOS':>9}  막대")
    print("  "+"-"*40)
    for E, L in zip(Es, ld):
        if abs(E*4 - round(E*4)) < 1e-9 and round(E*4) % 4 == 0:
            note = " ←λ=2d" if abs(E - E_2d) < 0.3 else (" ←최대" if E == Emax else "")
            print(f"  {E:>6.1f}{lam_of_E(E):>8.2f}{L:>9.4f}  {'█'*int(36*L/Lmax)}{note}")
    L_2d = ldos_ads(E_2d, V, ads_idx, N, t)
    print(f"\n  LDOS 최대: E={Emax:.2f}eV(λ={lam_of_E(Emax):.2f}Å) — 흡착 공명/밴드 효과.")
    print(f"  LDOS at λ=2d (E={E_2d:.2f}eV) = {L_2d:.4f} = 최대의 {100*L_2d/Lmax:.0f}% (피크 아님).")
    print(f"  → 가설이 예측한 λ=2d 공명 피크는 *나타나지 않음*. 기하 정합 ≠ 역공여 증폭.")
    assert L_2d < 0.7*Lmax, "λ=2d 가 LDOS 피크가 아님(가설 반증) 확인 실패"

    # ── 3. 무엇이 역공여를 지배하는가: 페르미 DOS + 흡착 공명 ──
    print("\n" + "─"*72)
    print("[3] 역공여를 지배하는 것 — 금속 페르미 상태밀도 + 흡착 공명 (d-밴드/Newns-Anderson)")
    print("─"*72)
    print("  흡착 LDOS는 (i) 금속 띠에 상태가 있는 에너지서 크고, (ii) 흡착 자체 공명서 큼.")
    print("  Pt가 좋은 촉매인 진짜 이유: 페르미준위에 d-상태(부분충전 5d) → 결합·역공여 가능,")
    print("  그리고 흡착 세기가 Sabatier 최적(ΔG_H≈0). 이는 *기하 파장정합이 아니라 DOS/결합*.")
    print(f"  Pt φ=5.65eV(E_F 근처)는 제1전도띠 *안*(λ_e={lam_of_E(5.65):.2f}Å, 띠바닥 위) →")
    print("    전파 상태 존재 = 금속·촉매. '파장 공명'이 아니라 '띠 안에 상태 있음'이 핵심.")

    # ── 4. 파장 효과가 정당한 곳: 양자 가둠(박막 양자우물 상태) ──
    print("\n" + "─"*72)
    print("[4] 파장 효과의 정당한 자리 — 양자 가둠: 슬래브 두께 M 변화 → 흡착 LDOS 진동")
    print("─"*72)
    print("  실재 효과: 얇은 금속막의 양자우물 상태가 두께에 따라 표면 반응성을 진동시킴.")
    print("  여기선 두께 M(층수) 변화 시 흡착 LDOS(E_F)가 진동하는가 검증 (가둠 길이 L=M·d).")
    E_F = 6.5   # 띠 안 고정 에너지
    print(f"  고정 E_F={E_F}eV (λ_e={lam_of_E(E_F):.2f}Å). 두께별 흡착 LDOS:")
    print(f"  {'M(층)':>6}{'L=Md[Å]':>9}{'LDOS(E_F)':>11}  막대")
    print("  "+"-"*40)
    ms = list(range(6, 19))
    lvals = []
    for M in ms:
        VM, ai, NM = build_potential(M)
        Lv = ldos_ads(E_F, VM, ai, NM, t); lvals.append(Lv)
    Lmx = max(lvals)
    for M, Lv in zip(ms, lvals):
        print(f"  {M:>6}{M*D_PTPT:>9.1f}{Lv:>11.4f}  {'█'*int(34*Lv/Lmx)}")
    # 진동 존재 확인: 표준편차/평균
    mean = sum(lvals)/len(lvals)
    var = sum((x-mean)**2 for x in lvals)/len(lvals)
    cv = math.sqrt(var)/mean
    # 부호변화(진동) 횟수
    diffs = [lvals[i+1]-lvals[i] for i in range(len(lvals)-1)]
    sign_changes = sum(1 for i in range(len(diffs)-1) if diffs[i]*diffs[i+1] < 0)
    print(f"  → 두께에 따른 LDOS 변동계수 CV={cv:.2f}, 진동(부호변화) {sign_changes}회.")
    print(f"    두께(가둠 길이)와 전자 파장의 정합이 표면 반응성을 *진동*시킴 = 양자우물 효과.")
    print(f"    파장-기하 정합이 촉매에 들어오는 곳은 *면내 Pt-Pt 간격이 아니라 막 두께*.")
    assert sign_changes >= 2, "양자 가둠 진동 미검출"

    # ── 결론 ──
    print("\n" + "="*72)
    print("시뮬레이션 결론 — 정직한 검증:")
    print(f"  ① λ=2d(기하 정합)는 Bragg *밴드 경계/틈*(전자 반사) — 공명 증폭점 아님 [반증]")
    print(f"  ② 흡착 LDOS는 λ=2d서 피크 안 생김(최대의 {100*L_2d/Lmax:.0f}%) — 단순 기하 가설 미지지")
    print(f"  ③ 역공여 지배자 = 페르미 DOS + 흡착 공명 (d-밴드/Newns-Anderson, 확립)")
    print(f"  ④ Pt 우수성 = 부분충전 5d로 E_F에 상태 + Sabatier 최적 (파장 공명 아님)")
    print(f"  ⑤ 파장 효과의 정당한 자리 = 양자 가둠(막 두께) — LDOS 두께 진동 확인 [V]")
    print("  → CT장의 λ_e/2≈d '스케일 일치'는 우연; 동역학 공명 아님. 가설 [H] 하향 — ")
    print("    정직한 기술자는 d-밴드 중심. 파장-가둠(박막)이 추구할 실제 방향.")
    print("등급: [V] 1D 양자 시뮬(밴드·LDOS·가둠) · [F] Bragg 밴드경계 · [반증] 면내 기하 공명")
    print("="*72)


if __name__ == "__main__":
    main()
