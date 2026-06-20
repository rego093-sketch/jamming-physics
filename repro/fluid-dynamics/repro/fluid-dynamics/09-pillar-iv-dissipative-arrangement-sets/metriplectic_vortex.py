"""
metriplectic_vortex.py — Energy-consistent reduced metriplectic model for the
VP fluid whitepaper Onsager-anomaly diagnostic (Sec. 5.2-5.4, GATE-level claim).

What is rigorously demonstrated (the BUDGET, a bookkeeping theorem):
  Forced steady-state energy balance with two sinks,
        dE/dt = I - eps_nu - eps_bind,   eps_nu = a*nu*E,  eps_bind = b*E,
  has steady state E* = I/(a*nu + b), giving EXACTLY
        eps_nu + eps_bind = I            (budget closure, all nu)
        eps_nu  = I * a*nu/(a*nu+b)  -> 0      as nu -> 0
        eps_bind= I * b   /(a*nu+b)  -> I      as nu -> 0   (saturation plateau = I)
  Re_eff = U_rms*L/nu with U_rms = sqrt(2 E*/rho0), rho0 = 1.

What is NOT claimed here: that a microscopic vortex event rule actually carries the
inertial flux down to r_c. That support-localization statement is the GATE item of
Sec. 5.2/5.3 and is left open. This module demonstrates the steady-state budget and
its nu-independent plateau; the plateau value equals the injection rate I by
construction. Finite vortex number N_v enters only through the ENSEMBLE SCATTER of
the stochastic event channel (CLT: relative spread ~ 1/sqrt(events) ~ 1/sqrt(N_v)).
Everything is fixed by (N_v, nu, seed, I, a, b).
"""
import numpy as np

L = 2.0 * np.pi
AREA = L * L

def steady(nu, I=0.21, a=2.0, b=0.55):
    """Analytic steady-state budget (mean-field, N_v -> inf)."""
    Estar = I / (a * nu + b)
    eps_nu = a * nu * Estar
    eps_bind = b * Estar
    Urms = np.sqrt(2.0 * Estar / 1.0) / L     # normalize so Urms ~ O(0.5)
    Re_eff = Urms * L / nu
    return dict(eps_nu=eps_nu, eps_bind=eps_bind, eps_tot=eps_nu + eps_bind,
                eps_inj=I, Estar=Estar, Urms=Urms, Re_eff=Re_eff)

def run(N_v=1000, nu=0.005, seed=0, I=0.21, a=2.0, b=0.55,
        T=400.0, dt=0.05, t0_window=100.0):
    """Stochastic realization: each of N_v vortices undergoes binding events as an
    independent Poisson process; per-event energy release is set so the MEAN event
    dissipation equals b*E (energy-consistent). Finite N_v -> ensemble scatter."""
    rng = np.random.default_rng(seed)
    Estar0 = I / (a * nu + b)
    E = Estar0
    nsteps = int(round(T / dt))
    # per-vortex Poisson rate lam (events/time); per-event release de so that
    # N_v * lam * de = b * E  (mean event sink). Choose lam fixed, de = b*E/(N_v*lam).
    lam = 0.5
    cum_bind = 0.0
    cum_visc = 0.0
    cum_inj = 0.0
    Es = []
    for n in range(nsteps):
        cum_inj += I * dt
        E += I * dt
        # viscous sink (smooth)
        dvis = a * nu * E * dt
        E -= dvis
        cum_visc += dvis
        # event sink: number of binding events this step ~ Poisson(N_v*lam*dt)
        n_ev = rng.poisson(N_v * lam * dt)
        de = (b * E) / (N_v * lam) if (N_v * lam) > 0 else 0.0
        dbind = min(n_ev * de, max(E - 1e-9, 0.0))
        E -= dbind
        cum_bind += dbind
        t = (n + 1) * dt
        if t >= t0_window:
            Es.append(E)
    Tw = T - t0_window
    eps_bind = cum_bind / (AREA * Tw)
    eps_visc = cum_visc / (AREA * Tw)
    eps_inj = cum_inj / (AREA * T)
    Ew = float(np.mean(Es))
    Urms = np.sqrt(2.0 * Ew) / L
    Re_eff = Urms * L / nu
    # rescale dissipations to per-area-rate consistent with steady() normalization:
    # steady() returns eps already as a rate; here cum/(AREA*Tw) double-divides AREA,
    # so multiply back by AREA to compare on the same footing as steady().
    eps_bind *= AREA; eps_visc *= AREA; eps_inj *= AREA
    return dict(N_v=N_v, nu=nu, seed=seed,
                eps_bind=eps_bind, eps_visc=eps_visc, eps_inj=eps_inj,
                eps_tot=eps_bind + eps_visc, Urms=Urms, Re_eff=Re_eff,
                budget_residual=abs(eps_inj - (eps_bind + eps_visc)) / max(eps_inj, 1e-9))

if __name__ == "__main__":
    print("=== mean-field steady-state budget + saturation (analytic) ===")
    for nu in (0.05, 0.02, 0.01, 0.005, 0.002, 0.001, 0.0005):
        s = steady(nu)
        print(f"  nu={nu:<6}: Re_eff={s['Re_eff']:8.1f}  eps_nu={s['eps_nu']:.4f}  "
              f"eps_bind={s['eps_bind']:.4f}  eps_tot={s['eps_tot']:.4f}  (I={s['eps_inj']})")
    print("\n=== stochastic realization (budget closure check) ===")
    o = run(N_v=1000, nu=0.005, seed=0)
    print({k: round(v, 5) if isinstance(v, float) else v for k, v in o.items()})
