#!/usr/bin/env python3
"""
ch_solar_activity.py -- App E (HYP/SPEC): can a steady inflow clock the 11/22-yr solar cycle?
An HONEST NEGATIVE. RE-IMPLEMENTATION (2026-09-28) of a lost script, rebuilt from the site pages.
No parameter is adjusted to reach a page number.

PAGE CLAIMS
  docs/cosmology/16-open-problems-gathered/: "Checked (v2): ch_solar_activity.py makes the negative
    explicit. The cycle is an 11/22-yr oscillation, which requires a clock -- an intrinsic
    frequency. Reduced to its lowest mode the alpha-Omega dynamo has eigenvalues -1 +/- i sqrt(|D|),
    an intrinsic oscillation of period 2 pi / sqrt(|D|), with no inflow term; a steady inflow (the
    source of unchanging gravity) has no imaginary eigenvalue and cannot supply such a clock."
  docs/cosmology/axi-common-misreadings-reviewer-doubt-trails/ (M7): "the cycle is an oscillation
    needing a clock, and a steady inflow has no imaginary eigenvalue to provide one, so the dynamo
    is favoured (App E, ch_solar_activity.py)."
  axh / axj: "Solar dynamo (honest negative)"; "#13 ... steady inflow cannot clock the cycle".
  The flux-emergence-first observation cited alongside is observational; not computed here.

INPUTS (declared):
  Lowest-mode (two-mode, 'Parker/alpha-Omega') model in diffusion-time units:
     dA/dt = -A + alpha*B ,  dB/dt = Omega'*A - B ,  dynamo number D = alpha*Omega'.
  Steady-inflow representations (VP App E: a sink with converging inflow, flux freezing,
  inflow organises the field -- all time-independent):
     (i)  constant source h (steady forcing);  (ii) steady concentration rate u on B (and A);
     (iii) one-way organisation inflow -> A -> B (no field back-reaction on the inflow).
  Illustrative solar numbers (only for a units check, [L]): convection-zone depth L = 2.0e8 m,
  turbulent diffusivity eta_t = 1e8 m^2/s (literature range ~1e7-1e9 m^2/s); magnetic cycle 22 yr.
  Random matrix scan: numpy default_rng(SEED=19).

ALGORITHM: eigenvalues (numpy.linalg.eigvals) of each linear operator; RK4 integration of the
  alpha-Omega system and period from zero crossings vs 2 pi/sqrt|D|; a 20000-matrix scan showing
  complex eigenvalues of a real 2x2 need opposite-sign cross-couplings (b*c < 0), i.e. a closed
  two-way feedback loop -- which is the dynamo, not a steady one-way inflow.
EXPECTED OUTPUT: dynamo -1 +/- i sqrt|D|, period 2 pi/sqrt|D|; every steady-inflow operator has
  purely real eigenvalues; adding inflow terms to the dynamo shifts the growth rate, not the period.
Deterministic, numpy only.
"""
import numpy as np

SEED = 19

def dyn(D, alpha=None):
    alpha = np.sqrt(abs(D)) if alpha is None else alpha
    Om = D / alpha
    return np.array([[-1.0, alpha], [Om, -1.0]])

def rk4(M, x0, dt, n, h=None):
    h = np.zeros(2) if h is None else h
    x = np.array(x0, float); out = np.empty((n, 2))
    f = lambda y: M @ y + h
    for i in range(n):
        out[i] = x
        k1 = f(x); k2 = f(x + 0.5*dt*k1); k3 = f(x + 0.5*dt*k2); k4 = f(x + dt*k3)
        x = x + dt/6*(k1 + 2*k2 + 2*k3 + k4)
    return out

def period_from_zeros(y, dt):
    s = np.sign(y); z = np.where(s[:-1]*s[1:] < 0)[0]
    tz = (z + y[z]/(y[z] - y[z+1])) * dt     # linear interpolation
    return 2*np.mean(np.diff(tz)) if len(tz) > 2 else np.nan

if __name__ == "__main__":
    print("=== ch_solar_activity: does a steady inflow supply the solar-cycle clock? ===\n")
    print("(1) lowest-mode alpha-Omega dynamo, time in diffusion units")
    for D in [-1.0, -10.0, -100.0]:
        ev = np.linalg.eigvals(dyn(D))
        y = rk4(dyn(D), [1.0, 0.0], 1e-3, 20000)[:, 1]
        # remove the decay envelope e^{-t} before measuring the period
        t = np.arange(len(y))*1e-3; P = period_from_zeros(y*np.exp(t), 1e-3)
        print(f"  D = {D:6.0f}: eigenvalues {ev[0]:.4f}, {ev[1]:.4f} ; period (ODE) = {P:.4f}"
              f"  vs 2pi/sqrt|D| = {2*np.pi/np.sqrt(abs(D)):.4f}")
    print("  -> -1 +/- i sqrt|D| and period 2 pi/sqrt|D| reproduced; no inflow term appears.\n")

    print("(2) steady-inflow operators (time-independent; VP App E pictures)")
    u = 0.7; k = 2.0
    ops = {
        "(i)   constant source h, no dynamo  [-I]": -np.eye(2),
        "(ii)  steady concentration u on A,B [diag(u-1)]": np.diag([u-1, u-1]),
        "(iii) one-way inflow->A->B          [[-1,0],[k,-1]]": np.array([[-1.0, 0.0], [k, -1.0]]),
        "(ii)+(iii) combined                 ": np.array([[u-1, 0.0], [k, u-1-0.3]]),
    }
    allreal = True
    for name, M in ops.items():
        ev = np.linalg.eigvals(M); im = np.max(np.abs(ev.imag)); allreal &= im == 0
        print(f"  {name}: eigenvalues {np.round(ev, 4)}  max|Im| = {im:.1e}")
    y = rk4(ops["(i)   constant source h, no dynamo  [-I]"], [0.0, 0.0], 1e-2, 3000, h=np.array([1.0, 0.5]))
    print(f"  (i) with steady h: trajectory -> fixed point {np.round(y[-1], 4)} (monotone, no cycle)")
    print(f"  all steady-inflow operators purely real: {allreal}\n")

    print("(3) inflow added to a dynamo: does it set the clock?")
    for uu in [0.0, 0.5, 0.9]:
        ev = np.linalg.eigvals(dyn(-10.0) + uu*np.eye(2))
        print(f"  D=-10, inflow rate u={uu:.1f}: eigenvalues {np.round(ev, 4)} -> period 2pi/|Im| = {2*np.pi/abs(ev[0].imag):.4f}")
    print("  -> inflow shifts only the real part (growth/decay); the frequency is set by D alone.\n")

    print("(4) scan: which real 2x2 operators can oscillate?  (rng seed 19, 20000 matrices)")
    rng = np.random.default_rng(SEED)
    Ms = rng.normal(size=(20000, 2, 2))
    bc = Ms[:, 0, 1]*Ms[:, 1, 0]
    ev = np.linalg.eigvals(Ms); cplx = np.any(np.abs(ev.imag) > 1e-12, axis=1)
    print(f"  complex eigenvalues with b*c >= 0: {np.sum(cplx & (bc >= 0))} of {np.sum(bc >= 0)}")
    print(f"  complex eigenvalues with b*c <  0: {np.sum(cplx & (bc < 0))} of {np.sum(bc < 0)}")
    print("  -> an oscillation needs a closed two-way loop with opposite-sign couplings (the alpha-Omega")
    print("     structure). A steady one-way inflow cannot provide it; if an inflow model were given")
    print("     such a loop it would be re-deriving a dynamo, not replacing it.\n")

    print("(5) units check [L] (not a prediction; eta_t is uncertain by ~2 dex)")
    yr = 3.15576e7; L = 2.0e8; eta = 1e8
    tau = L*L/eta
    Dreq = (2*np.pi*tau/(22*yr))**2
    print(f"  tau_diff = L^2/eta_t = {tau/yr:.1f} yr ; 22-yr magnetic cycle needs |D| = {Dreq:.1f}")
    print("  (for eta_t 1e7..1e9 m^2/s, |D| spans ~0.13..1300: the dynamo accommodates, not predicts, 22 yr)\n")

    print("HONEST VERDICT (as on page): NEGATIVE for the inflow conjecture. A steady inflow has no")
    print("imaginary eigenvalue and cannot clock the cycle; the alpha-Omega dynamo carries the clock.")
    print("Scope: linear lowest-mode caricature; nonlinear saturation (alpha-quenching) not modelled.")
