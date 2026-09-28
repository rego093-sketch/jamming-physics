"""
forced_circle_attractor.py
================================================================================
VP 잼밍 이론 — "강제된 원" 양성자 반경 끌개 (PROTON, not quantum).

물리:  등정적 잼밍 코어(z=2d)는 전단 여유가 0이라, 회전이 임의로 접촉을 깨
       언잼시킨다. 언잼 물질은 단일 C3 노즐로만 빠져나가 *방향성 유입*을 만든다
       (= 백서 6.2 의 r^-4 항, 가정이 아니라 회전의 귀결).  바깥으로는 정류된
       강성 반발(alpha * r^-5).  두 항의 평형이 코어 반경을 '못박는다'.

지배식 (반경 x = r / lambda_Cp, 무차원):

       dx/dt = F(x) = alpha * x^-5  -  x^-4 ,     alpha = 2/pi

  - 고정점:  alpha x^-5 = x^-4  =>  x* = alpha = 2/pi = 0.63662
  - 안정성:  F'(x) = -5 alpha x^-6 + 4 x^-5 ,  F'(x*) = -alpha^-5 = -(pi/2)^5 ~ -9.56 < 0  (안정)
  - 유일성:  양의 고정점은 x* 하나뿐 (F(x)=0 <=> x=alpha)
  - 전역성:  x>0 에서 x<x* 면 F>0(증가), x>x* 면 F<0(감소) => 모든 양의 초기값이 x* 로 수렴

  => r_p = (2/pi) * lambda_Cp = 0.8412 fm  (강제됨, 자유 파라미터 아님)

지수 -5, -4 는 평형 *위치*만 정하고, 평형값 2/pi 는 정류 생존분율 <|cos|>_2D 에서 온다.
(2/pi 의 닫힌 형태 증명은 06_constants_scales_geometry 참조.)

등급: [F]/[V]  (닫힌 형태 + 수치 적분 검증).

실행:  python3 forced_circle_attractor.py
출력:  콘솔 요약 + forced_circle_attractor.png/.pdf (위상선 + 수렴 궤적)
의존:  numpy, matplotlib
"""

import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

ALPHA      = 2/np.pi
LAMBDA_C_P = 1.32140985539e-15   # m (양성자 콤프턴 파장)

def F(x):  return ALPHA * x**-5 - x**-4
def Fp(x): return -5*ALPHA * x**-6 + 4 * x**-5

# ---- 고정점 / 안정성 (해석) -------------------------------------------------
xstar = ALPHA
Fp_star_analytic = -ALPHA**-5            # = -(pi/2)^5
print("="*70)
print("강제된 원 — 양성자 반경 끌개")
print("="*70)
print(f"  고정점       x* = alpha = 2/pi            = {xstar:.6f}")
print(f"  F(x*)                                     = {F(xstar):.3e}  (~0)")
print(f"  F'(x*) 해석  = -(pi/2)^5                   = {Fp_star_analytic:.4f}")
print(f"  F'(x*) 수치                                = {Fp(xstar):.4f}   (<0 => 안정)")
print(f"  => r_p = (2/pi)*lambda_Cp                  = {xstar*LAMBDA_C_P*1e15:.4f} fm")

# ---- 유일성: F(x)=0 의 양의 근 (격자 스캔) ----------------------------------
xs = np.linspace(0.2, 2.0, 400000)
fv = F(xs)
roots = xs[:-1][np.sign(fv[:-1]) != np.sign(fv[1:])]
print(f"  (0.2,2.0) 구간 양의 근 개수                 = {len(roots)}  -> {np.round(roots,5)}")

# ---- 전역 수렴: 여러 초기값에서 적분 ---------------------------------------
def integrate(x0, dt=2e-4, steps=60000):
    x = x0; traj = [x]
    for _ in range(steps):
        x = max(x + dt*F(x), 1e-6)      # 명시적 오일러 + 양수 클립
        traj.append(x)
    return np.array(traj)

x0_list = [0.30, 0.45, 0.6366, 0.85, 1.10, 1.30]
finals  = []
trajs   = {}
for x0 in x0_list:
    tr = integrate(x0); trajs[x0] = tr; finals.append(tr[-1])
print(f"  초기값 {x0_list}")
print(f"  수렴값                                     = {np.round(finals,5)}")
print(f"  모두 x*=2/pi={xstar:.5f} 로 수렴?            -> {np.allclose(finals, xstar, atol=2e-3)}")

# ---- 그림: (좌) 위상선 F(x),  (우) 수렴 궤적 -------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

xx = np.linspace(0.30, 1.6, 600)
ax1.axhline(0, color="0.6", lw=0.8)
ax1.plot(xx, F(xx), color="#1f4e79", lw=2)
ax1.axvline(xstar, color="#c00000", ls="--", lw=1.5)
ax1.plot([xstar], [0], "o", color="#c00000", ms=8, zorder=5)
ax1.annotate(r"$x^\ast=2/\pi$", (xstar, 0), textcoords="offset points",
             xytext=(8, 14), color="#c00000", fontsize=12)
ax1.fill_between(xx, 0, F(xx), where=(F(xx) > 0), color="#1f4e79", alpha=0.12)
ax1.set_xlabel(r"$x=r/\lambda_{C,p}$"); ax1.set_ylabel(r"$F(x)=\alpha x^{-5}-x^{-4}$")
ax1.set_title(r"phase line: unique stable fixed point $x^\ast=\alpha=2/\pi$")
ax1.set_ylim(-1.2, 1.6)

tgrid = np.arange(len(trajs[x0_list[0]])) * 2e-4
for x0 in x0_list:
    ax2.plot(tgrid, trajs[x0], lw=1.6, label=f"$x_0$={x0}")
ax2.axhline(xstar, color="#c00000", ls="--", lw=1.5)
ax2.annotate(r"$2/\pi$", (tgrid[-1], xstar), textcoords="offset points",
             xytext=(-22, 6), color="#c00000", fontsize=11)
ax2.set_xlabel(r"integration time $\tau$"); ax2.set_ylabel(r"$x(\tau)$")
ax2.set_title(r"global convergence: all $x_0>0 \to 2/\pi$")
ax2.legend(fontsize=8, ncol=2)

fig.suptitle(r"Forced proton radius:  $r_p=(2/\pi)\,\lambda_{C,p}=0.8412$ fm", fontsize=13)
fig.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig("forced_circle_attractor.png", dpi=150)
fig.savefig("forced_circle_attractor.pdf")
print("  그림 저장: forced_circle_attractor.png / .pdf")
