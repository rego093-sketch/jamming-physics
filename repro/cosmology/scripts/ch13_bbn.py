#!/usr/bin/env python3
"""
ch13_bbn.py -- Ch 13 "Light elements without a hot Big Bang": make the target explicit and show
why the naive static route fails for deuterium. RE-IMPLEMENTATION (2026-09-28) of a lost script;
rebuilt from the site pages. No parameter is adjusted to reach a page number.

PAGE CLAIMS (docs/cosmology/13-light-elements-without-hot-big/, axb-reproducibility-map/):
  Eq. (bbn-yp): Y_p = 2(n/p)/(1+n/p) ~ (2/7)/(8/7) = 0.25
  Sim A printout: "n/p at freeze-out = 0.167 -> after decay 0.143 -> Y_p = 0.250 (observed 0.247)"
  Sim B printout: "D/H after N stellar generations: 2.5e-05 -> 1.0e-05 -> 4.0e-06 ... (DESTROYED,
                   wrong way)"
  axb: "freeze-out n/p ~1/6 -> 1/7, Y_p = 0.250 (target met); stellar D/H 2.5 -> 1.0 -> 0.4 x1e-5
        destroyed, wrong way (conflicting)"
  Status on the page: out-of-scope origin gap (NOT a VP prediction). Nothing here is a VP result;
  it is the standard-model TARGET plus a negative for the naive static route.

INPUTS (declared, literature):
  Q = m_n - m_p = 1.29333 MeV (PDG); tau_n = 878.4 s (PDG 2024 average)
  M_Pl = 1.22091e22 MeV; g* = 10.75 above e+e- annihilation, 3.36 below (standard values)
  Weak n<->p rates: Bernstein, Brown & Feinberg (1989) closed form
        lambda_np(T) = (255/tau_n) (12 + 6x + x^2)/x^5,  x = Q/T,  lambda_pn = lambda_np e^{-x}
  Deuterium bottleneck T_D = 0.07 MeV (textbook range 0.06-0.08 MeV; e.g. Kolb & Turner)
  Observed Y_p = 0.247, D/H = 2.5e-5 (Cooke+2018 2.53e-5), Li7/H = 1.6e-10 (as quoted on page)

ALGORITHM:
  (A1) Page's textbook arithmetic: n/p = 1/6 at freeze-out -> neutron decay to 1/7 -> Eq. (bbn-yp).
  (A2) Independent cross-check (not on the page): integrate dX_n/dt = -l_np X_n + l_pn (1-X_n)
       with the BBF rates plus free decay 1/tau_n on the n->p side, radiation-dominated t(T), g* stepped 10.75 -> 3.36 at T = 0.5 MeV
       (crude; declared), from T = 10 MeV down to T_D; Y_p = 2 X_n(T_D).
  (B)  Astration: each stellar generation cycles a fraction f of the gas through stars; D burns
       at ~1e6 K so returned gas carries no D; stars have NO net D source. Survival per
       generation s = 1 - f. The page's printed sequence (x0.4 per step) corresponds to f = 0.6;
       f is NOT fixed by any input, so a grid of f is shown. The claim tested is the DIRECTION
       (D/H monotonically decreases for every f > 0), not the step size.
EXPECTED OUTPUT: Y_p = 0.250 (A1); crude A2 gives Y_p ~ 0.19 (known-deficient, see printout); D/H falls for every f (B).
Deterministic, numpy only.
"""
import numpy as np

Q = 1.29333; tau_n = 878.4; MPl = 1.22091e22; hbar = 6.582119569e-22   # MeV, s, MeV, MeV s
T_D = 0.07

def Yp_from_np(r):
    return 2 * r / (1 + r)

def lam_np(T):
    x = Q / T
    return 255.0 / tau_n * (12 + 6 * x + x * x) / x**5

def gstar(T):
    return 10.75 if T > 0.5 else 3.36

def H(T):  # s^-1, radiation dominated
    return 1.66 * np.sqrt(gstar(T)) * T * T / MPl / hbar

def integrate_Xn(T0=10.0, T1=T_D, n=200000):
    # integrate in lnT: dX/dlnT = -(dX/dt)/H   (dT/dt = -H T)
    lnT = np.linspace(np.log(T0), np.log(T1), n)
    X = 1.0 / (1.0 + np.exp(Q / T0))         # equilibrium start
    Xf = None
    for i in range(n - 1):
        T = np.exp(lnT[i]); h = lnT[i + 1] - lnT[i]
        def f(X, T):
            l = lam_np(T); lp = l * np.exp(-Q / T)
            return -(-(l + 1.0 / tau_n) * X + lp * (1 - X)) / H(T)   # + free n decay
        k1 = f(X, T); k2 = f(X + 0.5 * h * k1, T * np.exp(0.5 * h))
        k3 = f(X + 0.5 * h * k2, T * np.exp(0.5 * h)); k4 = f(X + h * k3, T * np.exp(h))
        X = X + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        if Xf is None and lam_np(T) < H(T):
            Xf = (T, X)
    return X, Xf

if __name__ == "__main__":
    print("=== ch13_bbn: the light-element target and the deuterium negative ===\n")
    print("(A1) page arithmetic (textbook inputs n/p = 1/6 -> 1/7)")
    r_f = 1 / 6
    f_surv = 7 / 8                       # X_n 1/7 -> 1/8 <=> n/p 1/6 -> 1/7
    t_dec = -tau_n * np.log(f_surv)
    r_d = r_f * f_surv / (1 + r_f * (1 - f_surv))
    print(f"  n/p at freeze-out = {r_f:.3f} -> after decay {r_d:.3f} -> Y_p = {Yp_from_np(r_d):.3f} (observed 0.247)")
    print(f"  (the 1/6 -> 1/7 step implies {t_dec:.0f} s of free decay with tau_n = {tau_n} s)")
    print("  MATCH to the page printout; note this is the standard hot-BBN number, not a VP output.\n")

    print("(A2) independent cross-check: BBF weak rates + radiation-dominated clock (crude)")
    X, Xf = integrate_Xn()
    print(f"  weak freeze-out (lambda = H) at T_f = {Xf[0]:.3f} MeV, X_n = {Xf[1]:.4f} (n/p = {Xf[1]/(1-Xf[1]):.3f})")
    print(f"  at T_D = {T_D} MeV: X_n = {X:.4f} (n/p = {X/(1-X):.3f}) -> Y_p = 2 X_n = {2*X:.3f}")
    print("  Precision codes (PArthENoPE/PRIMAT) give 0.247. This crude integration does NOT reach it:")
    print("  it neglects m_e in the rates, the T_nu < T_gamma split and the smooth e+e- annihilation,")
    print("  all of which keep weak rates overestimated below ~0.5 MeV and drain neutrons too long.")
    print("  Reported as-is (no knob turned). It does not bear on the page claim, which is (A1).\n")

    print("(B) astration: stellar processing of primordial gas (the naive static route)")
    DH0 = 2.5e-5
    for f in [0.1, 0.3, 0.6, 0.9]:
        seq = DH0 * (1 - f) ** np.arange(4)
        print(f"  f = {f:.1f}: D/H " + " -> ".join(f"{v:.1e}" for v in seq) + "  (DESTROYED, wrong way)")
    print("  page sequence 2.5e-05 -> 1.0e-05 -> 4.0e-06 is the f = 0.6 row (survival 0.4/step).")
    print("  f is illustrative (no input fixes it); the robust result is the SIGN: with no stellar D")
    print("  source, d(D/H)/dN = -f D/H < 0 for every f > 0, so stars cannot raise D/H to 2.5e-5.\n")
    print("VERDICT (as on page): target Y_p ~ 0.25 made explicit; naive static route drives D/H down.")
    print("Light elements stay an out-of-scope origin gap; this script supplies no VP mechanism.")
