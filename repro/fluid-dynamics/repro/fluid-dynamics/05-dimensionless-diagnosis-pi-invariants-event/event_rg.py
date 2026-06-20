"""
event_rg.py — The event-RG of the axiomatic vortex dynamics (treatise axis 5,
RG1'). Under coarse-graining by a factor lambda,
    L        -> lambda * L
    eps_bind -> lambda^{-chi} * eps_bind
    sigma_eff-> lambda^{psi}  * sigma_eff
    alpha    -> alpha(lambda)        (cascade exponent, may run)
The spatial dimensionless invariant
    Pi_L = L^{1+alpha} * eps_bind / sigma_eff
flows as  d log Pi_L / d log lambda = (1+alpha) - psi - chi.

Hence the SELECTED arrangement is the RG fixed point: Pi_L is scale-independent
(a plateau) exactly when (1+alpha*) - psi - chi = 0. The sign of (1+alpha-psi-chi)
gauges strengthening (>0) vs weakening (<0). The 1/2 length law (Pillar III) is this
plateau read off in real space; departure from the line is the defect delta_ST.
"""
import numpy as np

def rg_flow(alpha, psi, chi, steps=12, lam=1.3, L0=1.0, eb0=1.0, sg0=1.0):
    """Return the Pi_L sequence under repeated coarse-graining."""
    L, eb, sg = L0, eb0, sg0; out = []
    for _ in range(steps):
        out.append(L**(1 + alpha) * eb / sg)
        L *= lam; eb *= lam**(-chi); sg *= lam**(psi)
    return np.array(out)

def selection_gap(alpha, psi, chi):
    """(1+alpha) - psi - chi; zero at the fixed point (Pi_L plateau)."""
    return (1 + alpha) - psi - chi

if __name__ == "__main__":
    print("Event-RG: selected arrangement = fixed point = Pi_L plateau")
    print(f"{'case':>16}{'(1+a)-psi-chi':>15}{'Pi_L first->last':>20}{'verdict':>12}")
    for name, p in [("fixed point", dict(alpha=0.5, psi=1.0, chi=0.5)),
                    ("strengthening", dict(alpha=0.9, psi=0.8, chi=0.4)),
                    ("weakening", dict(alpha=0.2, psi=1.2, chi=0.6))]:
        g = selection_gap(**p); Pi = rg_flow(**p)
        v = "PLATEAU" if abs(g) < 1e-9 else ("grows" if g > 0 else "decays")
        print(f"{name:>16}{g:>15.3f}{f'{Pi[0]:.3f}->{Pi[-1]:.3f}':>20}{v:>12}")
    print("=> (1+alpha*) = psi + chi is the selection condition; the 1/2 law is its real-space face.")
