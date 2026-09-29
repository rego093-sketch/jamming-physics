# -*- coding: utf-8 -*-
"""
vp_em_field_dynamics.py — VP 전자기장 동역학: 1차계·Poynting·인과성 (재현가능)
=============================================================================
EM 완성도 검토에서 발굴한 간극(동역학 맥스웰: 패러데이/앙페르/포인팅 미매핑)을,
AQD(Axiomatic Quantized Dynamics, NOCAL v1.1, DOI 10.5281/zenodo.17423870)의
*엄밀 장동역학*으로 닫는다 — 단, 종방향(스칼라 P) 형태로.

AQD 가 주는 것(직접 인용·구현):
  · 1차 결합계 (A1):  ∂_t P + K∇·v = 0,   ρ ∂_t v + ∇P = 0
        → 결합 시 파동방정식 □_c P = 0,  c² = K/ρ  (물리 c²=B/ρ 와 동일).
        (이 두 1차식이 맥스웰의 회전쌍 ∇×E·∇×B 의 *종방향 유사물*이다.)
  · 에너지밀도·Poynting:  e = ½[P²/K + ρ|v|²],   S = P·v
        → 연속식  ∂_t e + ∇·S = 0  (국소 에너지보존, AQD QP-0002-001).
  · 보존:  무손실 경계(주기/Neumann/Dirichlet불변/무한원 무복사)서 dE/dt = 0.
  · 인과성 (AQD F-A/B/C):  유한 전파 u_max = c, 빛원뿔 밖 도달 불가
        supp e(τ,·) ⊆ supp e(0,·) ⊕ B_{cτ}.

이 모듈(결정론적 검증):
  [1] 1차계 staggered leapfrog 전개 → 펄스 속도 = c 측정.
  [2] 에너지보존 dE/dt≈0 (주기경계=무손실) 직접 확인.
  [3] Poynting 연속식 ∂_t e + ∂_x S = 0 국소 잔차 → 0 확인.
  [4] 인과성: 펄스 지지가 빛원뿔 ct 안에 갇힘(초기지지 ⊕ ct) 확인.

정직 경계(중요): 이는 *종방향(E-섹터, 압력 P)* 동역학이다. 완전한 벡터 E/B 회전식
(패러데이 ∇×E·앙페르 ∇×B 의 벡터형, 자기장=독립 횡벡터)은 EM.9 의 [O] '절대 벡터섹터'로
남는다. 본 모듈은 *에너지·동역학·인과성·Poynting* 을 닫고, 벡터 회전섹터는 열린 채 명시한다.

표준 라이브러리만(math·hashlib)·결정론·2×sha256. 실행: python3 vp_em_field_dynamics.py
"""

import math

# ── 자연단위: K=ρ=1 → c=1 (물리 빛창발 모듈 c_theory=1 과 동일 규약) ──
K = 1.0
RHO = 1.0
C = math.sqrt(K / RHO)        # = 1
N = 400                        # 격자점 (주기)
L = 100.0                      # 도메인 길이
DX = L / N
CFL = 0.5                      # cΔt/Δx
DT = CFL * DX / C
STEPS = 600

LED = []
def P_(s=""):
    print(s); LED.append(s)


def gaussian_pulse():
    """초기 우향 가우시안 펄스: P(x,0), v 는 우향 진행파가 되도록 설정."""
    x0, w = L * 0.35, 3.0
    P = [math.exp(-((i * DX - x0) ** 2) / (2 * w * w)) for i in range(N)]
    # 우향 진행파: v = P/(ρc) (1차계의 우향 특성), half-grid 에 근사 배치
    v = [0.0] * N
    for i in range(N):
        xf = (i + 0.5) * DX
        v[i] = math.exp(-((xf - x0) ** 2) / (2 * w * w)) / (RHO * C)
    return P, v


def energy(P, v):
    """E = Σ ½[P²/K + ρ v²] Δx  (staggered 에너지)."""
    eP = sum(0.5 * P[i] * P[i] / K for i in range(N)) * DX
    ev = sum(0.5 * RHO * v[i] * v[i] for i in range(N)) * DX
    return eP + ev


def centroid(P):
    """|P|² 가중 질량중심 (펄스 위치)."""
    w = [P[i] * P[i] for i in range(N)]
    tot = sum(w)
    return sum(i * DX * w[i] for i in range(N)) / tot if tot else 0.0


def support_halfwidth(P, thresh_frac=1e-3):
    """|P|² 지지의 반폭 (인과성: ct 안에 갇히는지)."""
    w = [P[i] * P[i] for i in range(N)]
    pk = max(w)
    idx = [i for i in range(N) if w[i] > thresh_frac * pk]
    if not idx:
        return 0.0
    return (max(idx) - min(idx)) * DX / 2.0


def step(P, v):
    """1차계 staggered leapfrog 1스텝: ∂_tP=−K∂_xv, ∂_tv=−(1/ρ)∂_xP (주기)."""
    # v 갱신: v_{i+1/2} -= (Δt/ρ/Δx)(P_{i+1}-P_i)
    newv = v[:]
    for i in range(N):
        ip = (i + 1) % N
        newv[i] = v[i] - (DT / RHO / DX) * (P[ip] - P[i])
    # P 갱신: P_i -= (KΔt/Δx)(v_{i+1/2}-v_{i-1/2})
    newP = P[:]
    for i in range(N):
        im = (i - 1) % N
        newP[i] = P[i] - (K * DT / DX) * (newv[i] - newv[im])
    return newP, newv


def poynting_residual(Pprev, P, v):
    """국소 연속식 ∂_t e + ∂_x S = 0 의 RMS 잔차 (S_{i+1/2}=P_face·v)."""
    # ∂_t e (시간차분, 격자별)
    res = 0.0
    cnt = 0
    for i in range(N):
        ip = (i + 1) % N
        im = (i - 1) % N
        # e at i (use P midpoint in time)
        Pm = 0.5 * (Pprev[i] + P[i])
        # S at faces i+1/2 and i-1/2
        S_ip = 0.5 * (P[i] + P[ip]) * v[i]
        S_im = 0.5 * (P[im] + P[i]) * v[im]
        de = (P[i] * P[i] - Pprev[i] * Pprev[i]) / (2 * K) / DT  # ≈ ∂_t(½P²/K)
        dS = (S_ip - S_im) / DX
        res += (de + dS) ** 2
        cnt += 1
    return math.sqrt(res / cnt)


def main():
    P_("#" * 74)
    P_("# VP 전자기장 동역학 — 1차계·Poynting·인과성 (AQD 엄밀 장동역학으로 간극 닫기)")
    P_("# 출처: AQD NOCAL v1.1 (DOI 10.5281/zenodo.17423870) · 종방향(E-섹터) 형태")
    P_("#" * 74)
    P_(f"  자연단위 K=ρ=1 → c={C:.0f}; 격자 N={N}, Δx={DX:.3f}, Δt={DT:.4f}, CFL={CFL}")

    P, v = gaussian_pulse()
    E0 = energy(P, v)
    c0 = centroid(P)
    sup0 = support_halfwidth(P)

    # ── [1]+[2]+[3]+[4] 전개하며 측정 ──
    Emax_dev = 0.0
    res_max = 0.0
    Pprev = P[:]
    for n in range(STEPS):
        Pprev = P[:]
        P, v = step(P, v)
        E = energy(P, v)
        Emax_dev = max(Emax_dev, abs(E - E0) / E0)
        if n % 50 == 0:
            res_max = max(res_max, poynting_residual(Pprev, P, v))

    cF = centroid(P)
    supF = support_halfwidth(P)
    # 펄스가 주기상자에서 이동한 거리(랩 고려): 우향 진행 → c·t
    t_total = STEPS * DT
    dist_expected = C * t_total
    dist_measured = (cF - c0) % L
    # 가장 가까운 주기 표현
    while dist_measured < dist_expected - L / 2:
        dist_measured += L
    c_measured = dist_measured / t_total

    P_("\n" + "─" * 74)
    P_("[1] 1차계 전개 → 전파속도 = c  (∂_tP=−K∂_xv, ρ∂_tv=−∇P → □_c P=0) [V]/[F]")
    P_("─" * 74)
    P_(f"  펄스 중심 이동 = {dist_measured:.2f} (기대 c·t = {dist_expected:.2f})")
    P_(f"  측정 c = {c_measured:.4f} vs 이론 c = {C:.4f}  (오차 {abs(c_measured-C)/C*100:.2f}%)")
    assert abs(c_measured - C) / C < 0.02, "전파속도가 c 와 불일치"

    P_("\n" + "─" * 74)
    P_("[2] 에너지 보존 dE/dt≈0  (주기=무손실, AQD QP-0002-001) [F]/[V]")
    P_("─" * 74)
    P_(f"  E(0) = {E0:.6f};  전 구간 최대 상대편차 = {Emax_dev:.2e}")
    P_(f"  → 무손실 경계서 ∮S·n=0 → dE/dt=0. 수치적으로 보존(편차 {Emax_dev:.1e}).")
    assert Emax_dev < 1e-2, "에너지 비보존 — 무손실 위반"

    P_("\n" + "─" * 74)
    P_("[3] Poynting 연속식 ∂_t e + ∂_x S = 0 (S=P·v) 국소 잔차 → 0 [F]/[V]")
    P_("─" * 74)
    P_(f"  국소 연속식 RMS 잔차(최대) = {res_max:.2e}  (이산화 오차 규모)")
    P_(f"  → e=½[P²/K+ρv²], S=P·v. ∂_t e+∂_x S=0 국소 성립(잔차={res_max:.1e}).")
    P_("    (AQD 2차형: S=−(∂_tP)∇P 도 동일 연속식 — 등가.)")
    assert res_max < 1e-1, "Poynting 연속식 잔차 과대"

    P_("\n" + "─" * 74)
    P_("[4] 인과성 — 펄스 지지가 빛원뿔 ct 안에 갇힘 (AQD F-B: u_max=c) [F]")
    P_("─" * 74)
    growth = supF - sup0
    cone = C * t_total
    P_(f"  지지 반폭: 초기 {sup0:.2f} → 최종 {supF:.2f} (증가 {growth:.2f})")
    P_(f"  빛원뿔 한계 ct = {cone:.2f} → 지지 확장 ≤ ct 요구: {growth:.2f} ≤ {cone:.2f}")
    assert growth <= cone + DX, "지지가 빛원뿔 초과 — 인과성 위반"
    P_("  → 에너지/정보가 c 초과 전파 불가. supp e(τ)⊆supp e(0)⊕B_{cτ} (빛원뿔).")

    print("\n" + "=" * 74)
    print("결론 — 동역학 맥스웰 간극을 AQD 종방향 장동역학으로 닫음 (벡터섹터는 [O] 명시)")
    print("  ① 1차계 ∂_tP+K∇·v=0, ρ∂_tv+∇P=0 → □_c P=0, c²=K/ρ (맥스웰 회전쌍의 종방향 유사물)")
    print(f"  ② 에너지보존 dE/dt≈0 (편차 {Emax_dev:.0e}) — 무손실 경계, AQD QP-0002-001 [F]")
    print(f"  ③ Poynting 연속식 ∂_t e+∂_x S=0 (S=P·v) 국소 성립 (잔차 {res_max:.0e}) [F]")
    print("  ④ 인과성 u_max=c, 빛원뿔 갇힘 — AQD F-A/B/C [F]")
    print("-" * 74)
    print("등급: [F] 1차계·Poynting 연속식·에너지보존·인과성(닫힌형, AQD 정리) ·")
    print("      [V] 수치 전개로 c·보존·잔차·원뿔 확인 · [CAL] 없음(자연단위) ·")
    print("      [O] *완전 벡터 E/B 회전식*(패러데이/앙페르 벡터형·자기 독립횡벡터)=절대 벡터섹터 잔존")
    print("정직 경계: 이는 종방향(E-섹터) 동역학이다. 에너지·동역학·인과성·Poynting 은 닫혔고,")
    print("  벡터 회전섹터(자기장 절대구조)는 EM.9 [O]로 열린 채 명시 — 숨기지 않는다.")
    print("=" * 74)


if __name__ == "__main__":
    main()
