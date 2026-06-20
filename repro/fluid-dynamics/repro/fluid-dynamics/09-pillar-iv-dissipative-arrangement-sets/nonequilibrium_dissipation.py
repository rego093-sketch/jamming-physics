# -*- coding: utf-8 -*-
"""nonequilibrium_dissipation.py -- the P9 test. In equilibrium turbulence the
dissipation coefficient C_eps = eps L / u'^3 is constant (Taylor's zeroth law);
the framework reads this as the Pi_L RG fixed point (event_rg.py). Out of
equilibrium (e.g. the decay following release from forcing) Vassilicos's
non-equilibrium law gives C_eps ~ Re_M/Re_L, i.e. C_eps * Re_lambda ~ const
(C_eps ∝ Re_lambda^{-1}) -- the framework's non-plateau RG transient. This module
provides the single-snapshot diagnostics; decay.py drives the trajectory and
analyze_ce.py fits C_eps(Re_lambda)."""
import numpy as np
import ns3d as S

def spectrum(uh, vh, wh, g):
    """3D energy spectrum E(k) on integer shells; sum_k E(k) = total energy."""
    N = g['N']
    kmag = np.sqrt(g['k2'])
    kbin = np.minimum(np.round(kmag).astype(int), N // 2)
    Emodal = 0.5 * (np.abs(uh)**2 + np.abs(vh)**2 + np.abs(wh)**2) / (N**6)
    Ek = np.bincount(kbin.ravel(), weights=Emodal.ravel(), minlength=N // 2 + 1)
    k = np.arange(len(Ek))
    return k, Ek

def integral_scale(uh, vh, wh, g):
    """Longitudinal integral scale L = (3 pi/4) * sum(E(k)/k) / sum(E(k))."""
    k, Ek = spectrum(uh, vh, wh, g)
    m = k >= 1
    num = np.sum(Ek[m] / k[m]); den = np.sum(Ek[m])
    return (3 * np.pi / 4) * num / den if den > 0 else np.nan

def diagnostics(uh, vh, wh, g, nu):
    E = S.energy(uh, vh, wh)                 # total KE per mass = (3/2) u'^2
    Z = S.enstrophy(uh, vh, wh, g)
    eps = 2 * nu * Z
    up = np.sqrt(2.0 * E / 3.0)              # rms of one velocity component
    L = integral_scale(uh, vh, wh, g)
    lam = up * np.sqrt(15.0 * nu / eps) if eps > 0 else np.nan   # Taylor microscale
    Re_lam = up * lam / nu
    C_eps = eps * L / up**3
    eta = (nu**3 / eps)**0.25               # Kolmogorov scale
    kmax = (2 / 3) * (g['N'] // 2)
    return dict(E=E, Z=Z, eps=eps, up=up, L=L, lam=lam, Re_lam=Re_lam,
                C_eps=C_eps, eta=eta, kmax_eta=kmax * eta, skew=S.skewness(uh, g))

if __name__ == "__main__":
    nu = 0.008
    for f, N in [("state96.npz", 96), ("state64.npz", 64)]:
        try:
            z = np.load(f); g = S.grid(N)
            d = diagnostics(z['uh'], z['vh'], z['wh'], g, nu)
            print(f"{f}: Re_lam={d['Re_lam']:.1f}  C_eps={d['C_eps']:.3f}  "
                  f"L={d['L']:.3f}  u'={d['up']:.3f}  eps={d['eps']:.3f}  "
                  f"lam={d['lam']:.3f}  kmax*eta={d['kmax_eta']:.2f}  skew={d['skew']:+.2f}")
        except Exception as e:
            print(f"{f}: {e}")
