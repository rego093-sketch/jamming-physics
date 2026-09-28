#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ch11_grav_waves.py  --  Chapter 11: gravitational waves as a perturbation of the jammed medium.
===============================================================================================
Re-implementation (2026-09-28) of the lost script cited by
  docs/cosmology/axb-reproducibility-map/        (row 11)
  docs/cosmology/11-gravitational-waves-medium-perturbations/  ("Simulation A / B")
  docs/cosmology/16-open-problems-gathered/      (package list)

PAGE CLAIM (axb row 11, verbatim)
  "lattice pulse speed 1.000c; chirp (M_c=28M_odot) 35->250 Hz in 0.19s;
   Hulse-Taylor dot P_b=-2.40x10^-12 (degenerate)"
PAGE CLAIM (ch.11 body)
  "A: transverse pulse on elastic lattice, c=sqrt(K/rho)=1 ... measured pulse speed = 1.000 c"
  "... quadrupole radiation with two transverse polarisations ... A gravitational wave is a
   propagating shear of the same medium"

MECHANISM IMPLEMENTED (author's statement, 2026-09-28)
  "A gravitational wave is the lattice opening and then closing": a propagating
  dilation/compression ("breathing") of the jammed lattice. It rides the same medium as light,
  so its speed must come OUT of the lattice, not be put in.
  NOTE: this is a LONGITUDINAL (compressional) picture. The ch.11 page instead calls the GW a
  "propagating shear" with two transverse-traceless polarisations. The physics volume says that at
  the isostatic point the shear modulus G -> 0 (repro/physics/bundle_v0.4/.../01_stiffness_to_c2,
  02_shear_relaxedG), so a shear wave cannot carry the signal there. This script therefore
  implements the breathing picture and MEASURES the transverse channel instead of assuming it.

PARTS
  A0  1-D chain (K = m = a = 1), the page's "Simulation A": a compression pulse, and a genuinely
      transverse pulse on the same central-force chain at zero tension.
  A   3-D jammed packing (the physics-volume substrate, built here with numpy only):
        * soft frictionless spheres, harmonic contacts (k = 1, diameter sigma = 1, mass m = 1),
          random start (SEED = 19), FIRE-minimised at phi = 0.70, then decompressed to phi = 0.66
          toward the jamming point (phi_J ~ 0.64). Elongated periodic box (Lx = 6 Ly).
        * relaxed (non-affine) moduli by exact linear response on the rigid backbone:
          B (bulk), C11 (x-uniaxial = longitudinal-wave modulus), C55/C66 (x-propagating shear).
        * wave runs, full nonlinear contact forces, velocity Verlet:
            L-small  : plane "opening-then-closing" pulse, u_x = A exp(-((x-x0)/w)^2), strain 3e-5
            L-open   : same, amplitude raised so the dilated half actually OPENS contacts
            T        : transverse pulse u_y of the same shape
          Pulses are launched from rest (d'Alembert split), so no speed is put in; the right-moving
          peak of the slab-averaged displacement is tracked and its speed fitted.
        * compared with c = sqrt(B/rho) (the physics volume's light speed), sqrt(C11/rho)
          (longitudinal elasticity), sqrt(C66/rho) (shear).
  B   Inspiral chirp and Hulse-Taylor decay from the standard quadrupole formula.
      These use G and the GR coefficient 32G/5c^5 as INPUT (the page itself says the 2G/c^4
      coefficient is imported, not derived), so B is a GR arithmetic check, degenerate with GR.

INPUTS (sources)
  CODATA 2018: c. IAU nominal: GM_sun = 1.3271244e20 m^3 s^-2.
  GW150914 chirp mass 28 M_sun (page value; LIGO PRL 116, 061102 gives 28.3 source-frame / ~30 det).
  PSR B1913+16 (Weisberg & Huang 2016, ApJ 829, 55): m_p = 1.4398, m_c = 1.3886 M_sun,
  P_b = 0.322997448918 d, e = 0.6171340; intrinsic dP_b/dt = (-2.398 +- 0.004)e-12.
  Lattice: none fitted. N, box aspect, pulse width, amplitudes are containers/probe choices,
  disclosed below; the conclusions do not depend on them (speed is read from the dynamics).

EXPECTED OUTPUT (what this code gives; see REIMPL_gw_gamma.md for the page comparison)
  A0: longitudinal chain pulse 0.999 c; transverse pulse on a tension-free chain: no propagation.
  A : (run 2026-09-28) breathing-mode speed / sqrt(C11/rho) = 0.97-1.03 at phi = 0.70, 0.66, 0.65;
      / sqrt(B/rho) = 1.11-1.15 (z = 8.1) -> 1.04-1.06 (z = 6.6); opening 5-7% of contacts changes
      the speed by < 3%; transverse c_T = sqrt(C66/rho) within 10%, c_T/c_L = 0.40 -> 0.28.
  B : 35 -> 250 Hz in ~0.19 s for M_c = 28 M_sun; dP_b/dt = -2.40e-12.

DETERMINISM: SEED = 19 (initial positions only); 2 x SHA-256 digest over 6-sig-fig results.
DEPENDENCIES: numpy (matplotlib optional, MPLBACKEND=Agg). Runtime ~2 min.
"""
import json, hashlib, time
import numpy as np

SEED = 19
T0 = time.time()

# ----------------------------------------------------------------------------- utilities
def sig(x, n=6):
    x = float(x)
    if x == 0.0 or not np.isfinite(x):
        return x
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))

def digest(obj):
    blob = json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(hashlib.sha256(blob).digest()).hexdigest()

def fit_speed(t, xpk):
    A = np.vstack([t, np.ones_like(t)]).T
    (v, b), *_ = np.linalg.lstsq(A, xpk, rcond=None)
    res = xpk - (v * t + b)
    return v, float(np.sqrt(np.mean(res ** 2)))

# ============================================================================= PART A0: 1-D chain
def chain_longitudinal(N=6000, w=12.0, steps=1500, dt=0.1):
    """K=m=a=1: u_n'' = u_{n+1} - 2u_n + u_{n-1}.  Launch from rest (no speed input)."""
    n = np.arange(N, dtype=float); x0 = N / 2
    u = 1e-3 * np.exp(-((n - x0) / w) ** 2); v = np.zeros(N)
    acc = lambda u: np.roll(u, 1) - 2 * u + np.roll(u, -1)
    a = acc(u); ts, xs = [], []
    for s in range(steps + 1):
        if s % 50 == 0 and s * dt > 3 * w:
            right = n > x0
            p = u[right] ** 2
            ts.append(s * dt); xs.append((n[right] * p).sum() / p.sum() - x0)
        v += 0.5 * a * dt; u += v * dt; a = acc(u); v += 0.5 * a * dt
    return fit_speed(np.array(ts), np.array(xs))[0]

def chain_transverse(N=2000, w=12.0, steps=1500, dt=0.1, amp=1e-3):
    """Same chain, central springs at rest length (zero tension), transverse displacement y_n.
    Exact force from springs |r_{n+1}-r_n| - 1; returns how far the pulse energy centroid moved."""
    n = np.arange(N, dtype=float); x0 = N / 2
    X = n.copy(); Y = amp * np.exp(-((n - x0) / w) ** 2)
    VX = np.zeros(N); VY = np.zeros(N)
    def force(X, Y):
        dx = np.diff(X); dy = np.diff(Y); r = np.hypot(dx, dy); f = (r - 1.0) / r
        FX = np.zeros(N); FY = np.zeros(N)
        FX[:-1] += f * dx; FX[1:] -= f * dx; FY[:-1] += f * dy; FY[1:] -= f * dy
        return FX, FY
    FX, FY = force(X, Y); y0 = Y.copy()
    for _ in range(steps):
        VX += 0.5 * FX * dt; VY += 0.5 * FY * dt; X += VX * dt; Y += VY * dt
        FX, FY = force(X, Y); VX += 0.5 * FX * dt; VY += 0.5 * FY * dt
    p = Y ** 2
    moved = abs((n * p).sum() / p.sum() - x0)
    return moved, float(np.max(np.abs(Y)) / np.max(np.abs(y0))), steps * dt

# ============================================================================= PART A: 3-D packing
def pairs(x, L, cut):
    """Neighbour pairs within cut; slab binning along the long x axis (numpy only)."""
    nb = max(3, int(L[0] // cut)); wbin = L[0] / nb
    b = np.floor((x[:, 0] % L[0]) / wbin).astype(int) % nb
    idx = [np.nonzero(b == k)[0] for k in range(nb)]
    I, J = [], []
    for k in range(nb):
        A = idx[k]
        for kk, same in ((k, True), ((k + 1) % nb, False)):
            Bi = idx[kk]
            dr = x[A][:, None, :] - x[Bi][None, :, :]; dr -= L * np.rint(dr / L)
            ii, jj = np.nonzero((dr * dr).sum(-1) < cut * cut)
            if same:
                m = jj > ii; ii, jj = ii[m], jj[m]
            I.append(A[ii]); J.append(Bi[jj])
    return np.concatenate(I), np.concatenate(J)

def forces(x, L, I, J):
    dr = x[I] - x[J]; dr -= L * np.rint(dr / L)
    r = np.sqrt((dr * dr).sum(1)); ov = 1.0 - r; m = ov > 0
    I2, J2, dr, r, ov = I[m], J[m], dr[m], r[m], ov[m]
    f = (ov / r)[:, None] * dr
    N = len(x); F = np.empty((N, 3))
    for k in range(3):
        F[:, k] = np.bincount(I2, f[:, k], N) - np.bincount(J2, f[:, k], N)
    return F, (I2, J2, dr, r, ov)

def fire(x, L, ftol=1e-10, skin=0.4, maxit=200000):
    v = np.zeros_like(x); dt, dtmax, al, al0, npc = 0.05, 0.3, 0.1, 0.1, 0
    I, J = pairs(x, L, 1 + skin); xref = x.copy()
    for it in range(maxit):
        if np.max(np.sqrt(((x - xref) ** 2).sum(1))) > 0.5 * skin:
            x %= L; I, J = pairs(x, L, 1 + skin); xref = x.copy()
        F, _ = forces(x, L, I, J)
        if np.abs(F).max() < ftol:
            break
        if (F * v).sum() > 0:
            vn = np.sqrt((v * v).sum()); fn = np.sqrt((F * F).sum())
            v = (1 - al) * v + al * vn * F / fn; npc += 1
            if npc > 5:
                dt = min(dt * 1.1, dtmax); al *= 0.99
        else:
            npc = 0; dt *= 0.5; al = al0; v[:] = 0
        v += dt * F; x = x + dt * v
    return x % L, it

def backbone(N, I, J):
    keep = np.ones(N, bool)
    for _ in range(200):
        m = keep[I] & keep[J]
        c = np.bincount(np.r_[I[m], J[m]], minlength=N)
        new = keep & (c >= 4)
        if new.sum() == keep.sum():
            break
        keep = new
    m = keep[I] & keep[J]
    z = np.bincount(np.r_[I[m], J[m]], minlength=N)[keep].mean()
    return keep, m, float(z)

def moduli(x, L):
    """Relaxed moduli by exact linear response  C = [Born - Xi^T H^+ Xi]/V  (CG solve)."""
    N = len(x); V = float(np.prod(L))
    I0, J0 = pairs(x, L, 1.0)
    _, (I, J, dr, r, ov) = forces(x, L, I0, J0)
    keep, m, z = backbone(N, I, J)
    I, J, dr, r, ov = I[m], J[m], dr[m], r[m], ov[m]
    n = dr / r[:, None]
    # pair stiffness block M = nn - (ov/r)(1-nn)   (U = ov^2/2, U'' = 1, U'/r = -ov/r)
    M = n[:, :, None] * n[:, None, :] - (ov / r)[:, None, None] * (np.eye(3) - n[:, :, None] * n[:, None, :])
    P = float((ov * r).sum()) / (3 * V)        # pressure (virial)
    def Hmv(u):
        g = np.einsum('pab,pb->pa', M, u[I] - u[J])
        y = np.zeros_like(u)
        for k in range(3):
            y[:, k] = np.bincount(I, g[:, k], N) - np.bincount(J, g[:, k], N)
        return y
    def cg(b, tol=1e-9, maxit=30000):
        xk = np.zeros_like(b); rk = b.copy(); pk = rk.copy(); rr = (rk * rk).sum(); b2 = rr
        for it in range(maxit):
            Ap = Hmv(pk); alpha = rr / (pk * Ap).sum()
            xk += alpha * pk; rk -= alpha * Ap; rn = (rk * rk).sum()
            if rn < tol * tol * b2:
                break
            pk = rk + (rn / rr) * pk; rr = rn
        return xk, it, np.sqrt(rn / b2)
    out = {}
    strains = {"B": np.eye(3),
               "C11": np.diag([1.0, 0, 0]),
               "C66": np.array([[0, .5, 0], [.5, 0, 0], [0, 0, 0]]),
               "C55": np.array([[0, 0, .5], [0, 0, 0], [.5, 0, 0]])}
    for name, e in strains.items():
        a = dr @ e.T                                   # affine bond change per unit strain
        Ma = np.einsum('pab,pb->pa', M, a)
        born = float((a * Ma).sum())
        Xi = np.zeros((N, 3))
        for k in range(3):
            Xi[:, k] = np.bincount(I, Ma[:, k], N) - np.bincount(J, Ma[:, k], N)
        Xi[~keep] = 0.0
        w, it, res = cg(Xi)
        relax = float((Xi * w).sum())
        C = (born - relax) / V
        if name == "B":
            C /= 9.0
        out[name] = C; out[name + "_born"] = born / V / (9.0 if name == "B" else 1.0)
        out[name + "_cg"] = (it, res)
    out.update(z=z, P=P, keep=keep, nbb=int(keep.sum()), V=V,
               mean_ov=float(ov.mean()))
    return out

def mode_run(x, L, keep, comp, n, amp, t_end, dt=0.1):
    """Set the lattice into ONE long-wave standing mode, u_comp = amp*cos(k x), k = 2 pi n / Lx,
    from rest (comp=0: the lattice 'opens' where cos<0-slope and 'closes' where >0 -- a breathing
    wave; comp=1: transverse). Record the mode projection q(t) and read its angular frequency by
    least squares; the wave speed c = omega/k comes OUT of the dynamics (no speed is input).
    Full nonlinear contact forces; also returns the largest fraction of contacts that opened."""
    k = 2 * np.pi * n / L[0]
    cx = np.cos(k * x[:, 0]); cx[~keep] = 0.0; norm = (cx * cx).sum()
    X = x.copy(); X[:, comp] += amp * cx
    I, J = pairs(x, L, 1.4)
    _, (Ic, *_ ) = forces(x, L, I, J); n0 = len(Ic); nmin = n0
    V = np.zeros_like(X); F, _ = forces(X, L, I, J)
    nsteps = int(t_end / dt); ts = np.arange(nsteps + 1) * dt; q = np.empty(nsteps + 1)
    for s in range(nsteps + 1):
        q[s] = ((X[:, comp] - x[:, comp]) * cx).sum() / norm
        if s % 50 == 0:
            _, (Ic, *_ ) = forces(X, L, I, J); nmin = min(nmin, len(Ic))
        V += 0.5 * F * dt; X += V * dt; F, _ = forces(X, L, I, J); V += 0.5 * F * dt
    q /= amp
    def resid(om):
        A = np.vstack([np.cos(om * ts), np.ones_like(ts)]).T
        coef, *_ = np.linalg.lstsq(A, q, rcond=None)
        return float(((A @ coef - q) ** 2).mean())
    oms = np.linspace(0.3, 12.0, 1200) * np.pi / t_end     # 0.15 .. 6 periods in the window
    om = oms[np.argmin([resid(o) for o in oms])]
    for span in (oms[1] - oms[0], (oms[1] - oms[0]) / 20):
        grid = np.linspace(om - span, om + span, 41); om = grid[np.argmin([resid(o) for o in grid])]
    periods = om * t_end / (2 * np.pi)
    return om / k, float(np.sqrt(resid(om))), (n0 - nmin) / n0, periods, ts, q

def part_A(phi_list=(0.70, 0.66, 0.65), N=2500, aspect=6.0):
    rng = np.random.default_rng(SEED)
    phi = phi_list[0]
    V = N * (np.pi / 6) / phi; Ly = (V / aspect) ** (1 / 3); L = np.array([aspect * Ly, Ly, Ly])
    x, _ = fire(rng.random((N, 3)) * L, L)
    rows = []; traces = {}
    for phi_t in phi_list:
        if phi_t != phi:
            sc = (phi / phi_t) ** (1 / 3); x = x * sc; L = L * sc; phi = phi_t
            x, _ = fire(x, L)
        mo = moduli(x, L)
        keep = mo["keep"]
        rho_all = N / mo["V"]; rho_bb = mo["nbb"] / mo["V"]
        c_B = np.sqrt(mo["B"] / rho_bb); c_11 = np.sqrt(mo["C11"] / rho_bb)
        c_66 = np.sqrt(max(mo["C66"], 0) / rho_bb); c_55 = np.sqrt(max(mo["C55"], 0) / rho_bb)
        # watch window: ~2 periods at the RELAXED speed estimate (window only; omega is fitted
        # freely over 0.15-6 periods, so the estimate cannot force the answer)
        k1 = 2 * np.pi / L[0]
        tL = 2.0 * 2 * np.pi / (k1 * c_11); tT = 1.5 * 2 * np.pi / (k1 * max(c_66, 0.03))
        strain_small = 1e-5
        vL1, rL1, _, pL1, tsL, qL = mode_run(x, L, keep, 0, 1, strain_small / k1, tL)
        vL2, rL2, _, pL2, _, _ = mode_run(x, L, keep, 0, 2, strain_small / (2 * k1), tL / 2)
        # 'opening' amplitude: peak strain = mean contact overlap, so the dilated half-wave opens contacts
        vO, rO, opO, pO, _, _ = mode_run(x, L, keep, 0, 1, mo["mean_ov"] / k1, tL)
        vT, rT, _, pT, tsT, qT = mode_run(x, L, keep, 1, 1, strain_small / k1, tT)
        rows.append(dict(phi=phi, N=N, nbb=mo["nbb"], z=mo["z"], P=mo["P"], mean_ov=mo["mean_ov"],
                         B=mo["B"], B_born=mo["B_born"], C11=mo["C11"], C11_born=mo["C11_born"],
                         C66=mo["C66"], C55=mo["C55"],
                         rho_all=rho_all, rho_bb=rho_bb, c_B=c_B, c_11=c_11, c_66=c_66, c_55=c_55,
                         vL=vL1, vL_rms=rL1, vL2=vL2, vL2_rms=rL2, vO=vO, vO_rms=rO, open_frac=opO,
                         vT=vT, vT_rms=rT, Lx=L[0], Ly=L[1], k1=k1))
        traces[phi] = (tsL, qL, tsT, qT)
    return rows, traces

# ============================================================================= PART B: chirp + HT
GM_SUN = 1.32712440018e20; C_SI = 2.99792458e8
TSUN = GM_SUN / C_SI ** 3                         # 4.9255e-6 s

def chirp(Mc=28.0, f1=35.0, f2=250.0):
    tau = Mc * TSUN
    k = (96 / 5) * np.pi ** (8 / 3) * tau ** (5 / 3)
    # RK4 integration of df/dt = k f^(11/3)
    f, t, dt = f1, 0.0, 1e-5
    fdot = lambda f: k * f ** (11 / 3)
    while f < f2:
        k1 = fdot(f); k2 = fdot(f + 0.5 * dt * k1); k3 = fdot(f + 0.5 * dt * k2); k4 = fdot(f + dt * k3)
        fn = f + dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        if fn >= f2:
            t += dt * (f2 - f) / (fn - f); break
        f = fn; t += dt
    t_an = (3 / 8) * (f1 ** (-8 / 3) - f2 ** (-8 / 3)) / k
    return t, t_an

def hulse_taylor(mp=1.4398, mc=1.3886, Pb_d=0.322997448918, e=0.6171340):
    Pb = Pb_d * 86400.0
    fe = (1 + 73 / 24 * e ** 2 + 37 / 96 * e ** 4) / (1 - e ** 2) ** 3.5
    return -(192 * np.pi / 5) * (2 * np.pi * TSUN / Pb) ** (5 / 3) * fe * mp * mc / (mp + mc) ** (1 / 3)

# ============================================================================= main
if __name__ == "__main__":
    np.random.seed(SEED)
    print("=" * 92)
    print(" ch11_grav_waves.py -- GW = the jammed lattice opening then closing (breathing pulse)")
    print("=" * 92)

    vL1 = chain_longitudinal()
    moved, ampr, tT = chain_transverse()
    print("\n[A0] 1-D chain, K = m = a = 1 (the page's 'Simulation A'):")
    print(f"     compression (opening/closing) pulse, launched from rest: speed = {vL1:.4f} c")
    print(f"     TRUE transverse pulse on the same central-force chain (zero tension): after t = {tT:.0f}")
    print(f"     the pulse centroid moved {moved:.2f} sites (a c-speed pulse would move {tT:.0f});"
          f" peak kept {ampr:.3f} of its amplitude.")
    print("     => with central springs and no tension there is no linear transverse restoring force:")
    print("        a transverse pulse does not propagate. A '1.000 c transverse pulse' needs a scalar")
    print("        chain (label only) or a pre-tension / shear stiffness that the model must supply.")

    rows, traces = part_A()
    print("\n[A] 3-D jammed packing (harmonic soft spheres, k = sigma = m = 1; SEED = 19; numpy only)")
    print("    wave speed = omega/k of a long-wave standing mode launched from rest (k = 2 pi n/Lx)")
    for r in rows:
        print(f"\n  phi = {r['phi']:.3f}   N = {r['N']}  backbone = {r['nbb']}  z = {r['z']:.3f} "
              f"(isostatic 2d = 6)   box {r['Lx']:.1f} x {r['Ly']:.1f}^2   P = {r['P']:.2e}")
        print(f"    relaxed moduli (linear response):  B = {r['B']:.4f}  C11 = {r['C11']:.4f}  "
              f"C66 = {r['C66']:.4f}  C55 = {r['C55']:.4f}   [Born: B = {r['B_born']:.4f}, C11 = {r['C11_born']:.4f}]")
        G = 0.5 * (r['C55'] + r['C66'])
        print(f"    G/B (x-shear, mean C55,C66) = {G/r['B']:.3f}   C11 - B = {r['C11']-r['B']:.4f}"
              f"  (isotropic 4G/3 = {4/3*G:.4f})")
        print(f"    predicted (rho_backbone = {r['rho_bb']:.3f}):  c = sqrt(B/rho) = {r['c_B']:.4f}   "
              f"sqrt(C11/rho) = {r['c_11']:.4f}   sqrt(C66/rho) = {r['c_66']:.4f}")
        print(f"    MEASURED breathing mode n=1 (kσ={r['k1']:.3f}, strain 1e-5): c_L = {r['vL']:.4f}"
              f"  -> /sqrt(C11/rho) = {r['vL']/r['c_11']:.3f}   /sqrt(B/rho) = {r['vL']/r['c_B']:.3f}"
              f"   (fit rms {r['vL_rms']:.3f})")
        print(f"    MEASURED breathing mode n=2 (kσ={2*r['k1']:.3f}):              c_L = {r['vL2']:.4f}"
              f"  -> /sqrt(C11/rho) = {r['vL2']/r['c_11']:.3f}   /sqrt(B/rho) = {r['vL2']/r['c_B']:.3f}")
        print(f"    MEASURED 'opening' mode (peak strain = mean overlap; {100*r['open_frac']:.1f}% of contacts open):"
              f" c = {r['vO']:.4f}  ({r['vO']/r['vL']:.3f} x linear)")
        print(f"    MEASURED transverse mode n=1:                           c_T = {r['vT']:.4f}"
              f"  -> /sqrt(C66/rho) = {r['vT']/max(r['c_66'],1e-9):.3f}   c_T/c_L = {r['vT']/r['vL']:.3f}"
              f"   (fit rms {r['vT_rms']:.3f})")
    print("\n  Reading: the breathing (opening/closing) wave's speed is an OUTPUT of the lattice dynamics and")
    print("  equals the longitudinal elastic speed sqrt(C11/rho) (C11 = B + 4G/3 for an isotropic solid).")
    print("  It exceeds c = sqrt(B/rho) by the 4G/3 term, a gap that shrinks as z -> 6 (G -> 0; physics")
    print("  volume 01/02). So on this medium the GW-as-breathing wave and 'light' (the c^2 = B/rho wave)")
    print("  are the SAME longitudinal mode: equal speed is automatic, not tuned -- but they are then one")
    print("  mode, not two. The transverse (shear) channel is slower, c_T = sqrt(G/rho), and its share")
    print("  falls toward zero at the isostatic point: the lattice carries ONE scalar/breathing")
    print("  polarisation there, not the two transverse-traceless polarisations the ch.11 page states.")

    t_rk, t_an = chirp()
    Pdot = hulse_taylor()
    print("\n[B] quadrupole chirp and orbital decay (GR coefficient IMPORTED; degenerate with GR):")
    print(f"    M_c = 28 M_sun: 35 -> 250 Hz in {t_rk:.4f} s (RK4)  /  {t_an:.4f} s (closed form)")
    print(f"    Hulse-Taylor (Peters-Mathews, WH2016 masses): dP_b/dt = {Pdot:.4e}"
          f"   (observed intrinsic -2.398e-12)")

    res = {"seed": SEED,
           "A0": {"chain_long_speed": sig(vL1), "chain_trans_moved": sig(moved)},
           "A": [{k: sig(v) for k, v in r.items() if isinstance(v, (float, int, np.floating))} for r in rows],
           "B": {"chirp_s": sig(t_rk), "chirp_an_s": sig(t_an), "HT_Pdot": sig(Pdot)}}
    print(f"\nDETERMINISM-DIGEST (2xSHA-256, 6 sig-fig): {digest(res)}")
    print(f"runtime {time.time()-T0:.0f} s")

    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 3, figsize=(15, 4.3))
        for r in rows:
            tsL, qL, tsT, qT = traces[r["phi"]]
            ax[0].plot(tsL, qL, lw=1, label=f"phi={r['phi']:.2f}")
            ax[1].plot(tsT, qT, lw=1, label=f"phi={r['phi']:.2f}")
        ax[0].set_title("breathing mode (lattice opens/closes): q(t)"); ax[0].set_xlabel("t"); ax[0].legend()
        ax[1].set_title("transverse mode, same packings: q(t)"); ax[1].set_xlabel("t"); ax[1].legend()
        zs = [r["z"] for r in rows]
        ax[2].plot(zs, [r["vL"] / r["c_B"] for r in rows], "o-", label="c_breathing / sqrt(B/rho)")
        ax[2].plot(zs, [r["vT"] / r["vL"] for r in rows], "s-", label="c_T / c_L measured")
        ax[2].axvline(6, color="k", ls=":"); ax[2].set_xlabel("contact number z"); ax[2].legend(); ax[2].grid(alpha=.3)
        ax[2].set_title("toward isostatic z=6")
        plt.tight_layout(); plt.savefig("ch11_grav_waves.png", dpi=110)
        print("[figure written: ch11_grav_waves.png]")
    except Exception as exc:
        print(f"[figure skipped: {exc}]")
