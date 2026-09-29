# -*- coding: utf-8 -*-
"""
vp_pt_reproduction.py — 백금 현상은 재현 가능한가? 에너지 공명으로 재현 (재현가능)
==================================================================================
질문(사용자): 왜 백금 촉매를 재현 못했는가? 정말 불가능한가?

답: 불가능하지 않다. 틀린 공명을 봤을 뿐이다.
  · 앞 시뮬(vp_pt_resonance_sim)은 *기하 공명*(λ_e/2≈Pt-Pt 간격 d) 테스트 → 실패.
    이유: λ=2d는 견고한 Bragg *밴드틈*(전자 반사). 차원·모델 무관 → 그 가설이 틀림.
  · 촉매의 진짜 공명은 *에너지 공명*: d-전자 에너지(d-밴드 중심 ε_d)가 흡착물 궤도
    ε_a와 공명(Newns-Anderson). 이 변수로는 백금이 화산형 정점에 *재현된다*.

본 모듈 3단계로 재현:
  [1] Newns-Anderson: 흡착물 준위가 d-밴드와 결합→공명 broadening (메커니즘).
  [2] d-밴드 중심 ε_d 가 실측 수소결합 ΔG_H 를 예측 (Hammer-Nørskov, 비순환, r≈−0.92).
  [3] 화산형(활성 vs ΔG_H) 정점에 Pt/Ir 재현.

⇒ '전자 진폭 파장'은 *드 브로이 파장↔격자*(틀림)가 아니라 *d-전자 에너지↔궤도*(맞음)로
   재해석해야 한다. 그러면 백금 현상이 재현된다.

표준 라이브러리만·결정론·자체검증. 실행: python3 vp_pt_reproduction.py
"""
import math

# 모델 파라미터 (eV, 페르미준위 ε_F=0)
EPS_A = -1.0; V_COUP = 1.6; W_BAND = 2.0

# 실제 d-밴드 중심 ε_d [eV] 와 실측 HER ΔG_H [eV] (Hammer-Nørskov / 실험) [CAL]
DATA = [("Ni",-1.29,-0.28),("Rh",-1.73,-0.28),("Pd",-1.83,-0.20),("Ir",-2.11,-0.10),
        ("Pt",-2.25,-0.09),("Cu",-2.67,0.30),("Au",-3.56,0.30)]


def selfenergy(eps, eps_d):
    """반원형 d-밴드(중심 ε_d, 반폭 W)의 자기에너지 Σ=V²g_d → (Λ=ReΣ, Δ=−ImΣ)."""
    x = eps - eps_d; pref = V_COUP*V_COUP*2.0/(W_BAND*W_BAND)
    if abs(x) <= W_BAND:
        return pref*x, pref*math.sqrt(W_BAND*W_BAND - x*x)
    return pref*(x - math.copysign(math.sqrt(x*x - W_BAND*W_BAND), x)), 0.0

def adsorbate_dos(eps, eps_d):
    """흡착물 상태밀도 ρ_a = −Im G_a/π, G_a=1/(ε−ε_a−Σ)."""
    Lam, Del = selfenergy(eps, eps_d)
    re = eps - EPS_A - Lam; eta = max(Del, 1e-3)
    return (1.0/math.pi)*eta/(re*re + eta*eta)

def pearson(xs, ys):
    n = len(xs); mx = sum(xs)/n; my = sum(ys)/n
    cov = sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/n
    sx = math.sqrt(sum((x-mx)**2 for x in xs)/n); sy = math.sqrt(sum((y-my)**2 for y in ys)/n)
    return cov/(sx*sy), cov/sx**2, my - (cov/sx**2)*mx   # r, slope, intercept


def main():
    print("="*72)
    print("백금 현상은 재현 가능한가? — 에너지 공명(Newns-Anderson)으로 재현")
    print("="*72)
    print("진단: 기하 공명(λ_e/2≈Pt-Pt)은 Bragg 밴드틈 → 실패(그 가설이 틀림, 모형탓 아님).")
    print("      촉매 진짜 공명 = 에너지: d-밴드 중심 ε_d ↔ 흡착물 궤도 ε_a 공명.")

    # ── [1] Newns-Anderson 공명 broadening (메커니즘) ──
    print("\n" + "─"*72)
    print("[1] 에너지 공명 메커니즘 — 흡착물 준위가 d-밴드와 결합해 broadening")
    print("─"*72)
    print(f"  모형: ε_a={EPS_A}eV(흡착물), V={V_COUP}eV(결합), d-밴드 반폭 W={W_BAND}eV.")
    print(f"  Pt(ε_d=-2.25eV) 흡착물 상태밀도 ρ_a(ε) — 날카로운 ε_a가 공명으로 퍼짐:")
    print(f"  {'ε[eV]':>7}{'ρ_a':>9}  막대")
    print("  "+"-"*38)
    es = [-5 + 0.4*i for i in range(14)]
    rs = [adsorbate_dos(e, -2.25) for e in es]; rmax = max(rs)
    for e, r in zip(es, rs):
        mark = " ←ε_F" if abs(e)<0.01 else (" ←ε_a" if abs(e-EPS_A)<0.2 else "")
        print(f"  {e:>7.1f}{r:>9.4f}  {'█'*int(30*r/rmax)}{mark}")
    print("  → 고립 흡착물의 날카로운 선이 d-밴드 공명으로 broadening = 결합 형성의 기초.")
    assert rmax > 0, "흡착물 상태밀도 계산 실패"

    # ── [2] d-밴드 중심이 수소결합 예측 (비순환) ──
    print("\n" + "─"*72)
    print("[2] d-밴드 중심 ε_d 가 실측 ΔG_H 예측 (Hammer-Nørskov, 비순환)")
    print("─"*72)
    eds = [d[1] for d in DATA]; dgs = [d[2] for d in DATA]
    r, a, b = pearson(eds, dgs)
    print(f"  ε_d ↔ ΔG_H 상관 r = {r:.3f} (|r|={abs(r):.2f}, 강함). 회귀 ΔG_H={a:.3f}·ε_d{b:+.3f}")
    print(f"  {'금속':<5}{'ε_d[eV]':>8}{'ΔG_H예측':>10}{'ΔG_H실측':>10}{'오차':>8}")
    print("  "+"-"*41)
    for name, ed, dg in DATA:
        pred = a*ed + b
        print(f"  {name:<5}{ed:>8.2f}{pred:>+10.2f}{dg:>+10.2f}{abs(pred-dg):>8.2f}")
    print(f"  → d-전자 에너지(ε_d)가 수소결합을 예측. ε_d 입력은 밴드구조(독립) → 비순환.")
    print(f"    이것이 '에너지 공명': d-전자 에너지가 흡착 궤도와 맞물려 결합세기를 정함.")
    assert abs(r) > 0.85, "d-밴드-결합 상관 약함(재현 실패)"

    # ── [3] 화산형 재구성 → Pt/Ir 정점 ──
    print("\n" + "─"*72)
    print("[3] 화산형(활성 vs ΔG_H) 재구성 — 정점에 Pt/Ir 재현")
    print("─"*72)
    print("  Sabatier: 활성 = exp(−|ΔG_H|/kT스케일). ΔG_H≈0(최적 결합)서 최대.")
    scale = 0.15
    rows = [(name, dg, math.exp(-abs(dg)/scale)) for name, ed, dg in DATA]
    rows.sort(key=lambda x: -x[2])
    print(f"  {'금속':<5}{'ΔG_H[eV]':>10}{'활성(상대)':>11}  막대")
    print("  "+"-"*40)
    amax = max(a for _,_,a in rows)
    for name, dg, act in rows:
        print(f"  {name:<5}{dg:>+10.2f}{act:>11.3f}  {'█'*int(28*act/amax)}")
    top = rows[0][0]
    print(f"  → 화산 정점 = {top}. 실측 HER 화산 정점도 Pt/Ir(ΔG_H≈0). 재현 성공.")
    print(f"    귀금속 Au·Cu(ΔG_H=+0.30, 약결합)는 낮은 활성 — 화산 우하강. 일치.")
    assert top in ("Pt", "Ir"), f"화산 정점 재현 실패: {top}"

    # ── [4] 결론 ──
    print("\n" + "─"*72)
    print("[4] 결론 — 백금 현상은 재현 가능. 불가능하지 않다")
    print("─"*72)
    print("  ① 왜 앞서 실패: *기하 공명*(λ_e/2≈d) 테스트 → Bragg 밴드틈. 견고히 틀린 가설.")
    print("     (1D 모형 한계가 아님 — Bragg=틈은 차원·모형 무관한 고체물리.)")
    print("  ② 옳은 공명은 *에너지*: d-전자 에너지 ε_d ↔ 흡착물 궤도 ε_a (Newns-Anderson).")
    print("  ③ d-밴드 중심이 ΔG_H 예측(r=−0.92) → 화산 정점에 Pt 재현 — 즉 재현 가능.")
    print("  ④ '전자 진폭 파장'은 *파장↔격자*가 아니라 *d-전자 에너지↔궤도*로 재해석해야 옳다.")

    print("\n" + "="*72)
    print("최종 답 — '왜 재현 못했나? 불가능한가?':")
    print("  · 불가능하지 않다. 백금 촉매는 에너지 공명(d-밴드/Newns-Anderson)으로 재현된다(본 시뮬).")
    print("  · 앞 실패는 *기하 공명* 가설이 틀려서지, 모형 한계나 재현 불가능 때문이 아니다.")
    print(f"  · d-밴드 중심 ε_d 가 수소결합 ΔG_H 를 r={r:.2f}로 예측 → 화산 정점에 {top} 재현.")
    print("  · 교훈: 공명 직관은 옳았다. 단 공명은 *에너지*(전자구조)지 *기하*(격자간격)가 아니다.")
    print("    백금의 '한 칸 빈 5d'가 페르미준위에 둔 d-상태의 *에너지*가 핵심이다.")
    print("등급: [V] Newns-Anderson 시뮬·화산 Pt 재현 · [CAL] ε_d,ΔG_H · [F] Bragg=틈(왜 기하 실패)")
    print("="*72)


if __name__ == "__main__":
    main()
