#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergence_trajectory.py -- Phase 3: the reduced-order REACTION-DIFFUSION
trajectory layer (positional information on a GROWING 3-D domain).

Where Phase 1 turned the measured protein half-life into an absolute *time*
scale (onset in hours), Phase 3 turns the measured morphogen biophysics into an
absolute *length* scale and a reproducible spatial partition. Same discipline:

  * Reads ONLY param_db.json (measured/universal morphogen constants); NEVER the
    validation targets and NEVER any real anatomy -- that separation is what makes
    every constant a locked input [L] rather than a back-fit.
  * Produces a COARSE, reproducible realized FORM (an ordered territory partition
    of a 3-D domain), not an exact anatomy. The mechanism is what is recovered.

The physics (linear, steady-state, screened Poisson)
----------------------------------------------------
A morphogen produced at a source diffuses (D) and decays (1/tau):

        D * laplacian(c)  -  c/tau  +  source  =  0

Its intrinsic length scale is the diffusion-decay length

        lambda = sqrt(D * tau)                                  [L]-grounded

set ENTIRELY by the two measured constants -- nothing chosen by us. A source on
one face gives c(x) ~ exp(-x/lambda) along the axis; thresholds theta_k carve the
domain into nested territories with boundaries at x_k = lambda * ln(1/theta_k).
This is Wolpert's positional information / "French-flag" partition -- the
textbook reduced-order morphogenesis mechanism.

Growth (allometric, source-sink)
--------------------------------
The domain ELONGATES along the morphogen axis over developmental time via the
SAME single universal supply rule used in Phases 1-2 (extent ~ devtime^alpha,
alpha from the DB). Because lambda is a FIXED physical length while the domain
grows, the apical (leading) territory -- width lambda*ln(1/theta), fixed in um --
occupies a SHRINKING fraction of the whole as the domain grows. That is a
negative-allometry MECHANISM, recovered here from first principles, qualitatively
echoing the negative allometry Phase 2 measured -- WITHOUT fitting any fraction.

Grades (grade == evidence)
--------------------------
  * intrinsic length  lambda = sqrt(D*tau) ........ [L]-grounded (measured D, tau)
  * positional partition / realized coarse FORM ... [F]  (threshold + supply rule)
  * apical negative-allometry of fixed-lambda zone . [F]  (mechanism, not a fit)
  * EXACT validated 3-D anatomy .................... [O]  (needs measured tissue
                                                          mechanics + HPC; not done)

Everything is deterministic (no RNG in the engine) and offline. numpy only.
"""

import os, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DB   = json.load(open(os.path.join(HERE, "param_db.json"), encoding="utf-8"))

# ----------------------------------------------------------------------------
# parameters pulled from the locked DB (NEVER inline magic numbers)
# ----------------------------------------------------------------------------
def morphogen_params():
    m = DB["morphogen"]
    D_um2_s   = m["diffusion_um2_per_s"]["value"]     # [L] measured (Kicheva 2007)
    decay_min = m["morphogen_decay_min"]["value"]     # [L] measured clearance time
    tau_s     = decay_min * 60.0                       # min -> s (unit handling only)
    return D_um2_s, tau_s, decay_min

def territory_theta():
    return DB["kinetics"]["relay_threshold_theta"]["value"]   # [F] threshold

def growth_alpha():
    return DB["allometry"]["growth_supply_exponent_alpha"]["value"]   # [F] universal

def decay_length_um():
    """The intrinsic morphogen length scale, from MEASURED constants only. [L]."""
    D, tau_s, _ = morphogen_params()
    return math.sqrt(D * tau_s)

def lambda_range_um():
    """Length band implied by the DB's own measured D-range (a grounded
    consistency check, not a fit): brackets real morphogen gradients."""
    m = DB["morphogen"]["diffusion_um2_per_s"]
    lo, hi = m["range"]; _, tau_s, _ = morphogen_params()
    return math.sqrt(lo*tau_s), math.sqrt(hi*tau_s)

# ----------------------------------------------------------------------------
# deterministic 3-D screened-Poisson solver (full-face source; Neumann walls)
# ----------------------------------------------------------------------------
def solve_field(N, L_um, tol=1e-7, maxit=60000):
    """Steady-state morphogen field on an N^3 grid spanning a box of axial length
    L_um. Source = whole x=0 face held at c=1 (Dirichlet); other faces zero-flux
    (Neumann). Jacobi iteration to a fixed residual tolerance -> deterministic."""
    D, tau_s, _ = morphogen_params()
    h = L_um / (N - 1)
    a = D / h**2
    m = 1.0 / tau_s
    denom = 6.0*a + m
    c = np.zeros((N, N, N))
    src = np.zeros((N, N, N), bool); src[0, :, :] = True
    c[src] = 1.0
    for _ in range(maxit):
        cp = np.pad(c, 1, mode="edge")           # edge-pad == zero-flux Neumann
        s = (cp[2:,1:-1,1:-1] + cp[:-2,1:-1,1:-1]
           + cp[1:-1,2:,1:-1] + cp[1:-1,:-2,1:-1]
           + cp[1:-1,1:-1,2:] + cp[1:-1,1:-1,:-2])
        cn = a*s/denom
        cn[src] = 1.0
        if np.max(np.abs(cn - c)) < tol:
            c = cn; break
        c = cn
    return c, h

def axis_profile(c):
    """Normalized morphogen profile along the central source-normal axis."""
    N = c.shape[0]; cax = (N-1)//2
    p = c[:, cax, cax].copy()
    return p / p[0]

def extract_lambda(c, h):
    """Recover the decay length from the SOLVED field (far-field axial ln-fit).
    Proves lambda is a property of the physics: this -> sqrt(D*tau)."""
    lam = decay_length_um()
    p = axis_profile(c)
    xs = np.arange(c.shape[0]) * h
    sel = (xs >= 1.0*lam) & (xs <= 4.5*lam) & (p > 1e-9)
    slope = np.polyfit(xs[sel], np.log(p[sel]), 1)[0]
    return -1.0 / slope

def crossing_um(c, h, level):
    """Sub-grid axial position where the normalized profile p(x) first drops to
    `level` (linear interpolation between the bracketing grid points). Removes
    grid quantisation so a boundary lands at its physical value lambda*ln(1/level)."""
    p = axis_profile(c); xs = np.arange(c.shape[0]) * h
    idx = np.where(p < level)[0]
    if idx.size == 0:
        return float(xs[-1])
    j = idx[0]
    if j == 0:
        return 0.0
    x0, x1, p0, p1 = xs[j-1], xs[j], p[j-1], p[j]
    return float(x0 + (x1 - x0) * (p0 - level) / (p0 - p1))

# ----------------------------------------------------------------------------
# positional information -> nested territories (French-flag partition)
# ----------------------------------------------------------------------------
def territory_thresholds(theta, k=4):
    """A geometric ladder theta, theta^2, ... -> EQUAL-width territories of width
    lambda*ln(1/theta). theta is the single modelling choice; widths are physics."""
    return [theta**(i+1) for i in range(k)]

def territories(c, h, theta=None, k=4):
    """Carve the 3-D domain into nested territories along the morphogen axis.
    Boundaries via sub-grid threshold crossings (physics-clean); per-territory
    3-D VOLUME fractions counted from the actual solved field."""
    if theta is None: theta = territory_theta()
    thr = territory_thresholds(theta, k)
    xs = np.arange(c.shape[0]) * h; L = xs[-1]
    bnds = [crossing_um(c, h, t) for t in thr]              # sub-grid crossings
    # 3-D volume fractions of each band {t_k <= c < t_{k-1}} from the actual field
    edges = [1.0] + thr
    fr = []
    for hi, lo in zip(edges[:-1], edges[1:]):
        vol = np.count_nonzero((c < hi) & (c >= lo))
        fr.append(vol / c.size)
    # apical AXIAL fraction: fixed physical width lambda*ln(1/theta) over growing L
    apical_axial_frac = crossing_um(c, h, theta) / L
    return dict(thresholds=thr, boundaries_um=bnds,
                band_volume_fracs=fr, apical_axial_frac=apical_axial_frac, L_um=L)

# ----------------------------------------------------------------------------
# growing domain -> realized coarse FORM + emergent negative allometry
# ----------------------------------------------------------------------------
def domain_length_um(devtime, t0=1.0):
    """Axial extent grows by the SAME universal supply rule as Phases 1-2:
    extent ~ devtime^alpha (alpha from DB). Base span = 6*lambda at devtime=t0.
    Not fitted to any size."""
    lam = decay_length_um(); a = growth_alpha()
    return 6.0*lam * (devtime/t0)**a

def realized_form(devtime, N=32):
    """Coarse realized form at a developmental time: solve on the grown domain,
    return territory count / boundaries / apical fraction. Shape, not anatomy."""
    L = domain_length_um(devtime)
    c, h = solve_field(N, L)
    lam = decay_length_um()
    T = territories(c, h)
    width = lam * math.log(1.0/territory_theta())        # fixed apical width [L]xtheta
    n_terr = int(L // width)
    return dict(devtime=devtime, L_um=round(L,2), n_territories=n_terr,
                apical_width_um=round(width,2),
                apical_axial_frac=round(T["apical_axial_frac"],4),
                boundaries_um=[round(b,2) for b in T["boundaries_um"]])

def growing_domain_allometry(devtimes):
    """Apical-territory axial-fraction vs domain length over developmental time.
    A fixed lambda in a growing domain => fraction FALLS (negative allometry).
    Returns the fitted scaling exponent (expected ~ -1). Mechanism [F]; no fit."""
    Ls, fr = [], []
    for t in devtimes:
        f = realized_form(t)
        Ls.append(f["L_um"]); fr.append(f["apical_axial_frac"])
    e = np.polyfit(np.log(Ls), np.log(fr), 1)[0]          # frac ~ L^e
    return dict(L_um=Ls, apical_axial_frac=fr, frac_vs_L_exponent=round(float(e),3))

# ----------------------------------------------------------------------------
def result_hash():
    forms = [realized_form(t) for t in (1.0, 1.5, 2.0, 3.0)]
    allo  = growing_domain_allometry([1.0, 1.5, 2.0, 3.0])
    blob = json.dumps({"forms": forms, "allo": allo}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:12]

if __name__ == "__main__":
    D, tau_s, decay_min = morphogen_params()
    lam = decay_length_um(); lo, hi = lambda_range_um()
    print("="*86)
    print("  REDUCED-ORDER REACTION-DIFFUSION TRAJECTORY LAYER  (Phase 3)")
    print("  positional information on a growing 3-D domain; targets never read")
    print("="*86)
    print(f"  morphogen biophysics (param_db, measured [L]):  D={D} um^2/s , "
          f"decay={decay_min} min (tau={tau_s:.0f}s)")
    print(f"  INTRINSIC LENGTH SCALE  lambda = sqrt(D*tau) = {lam:.2f} um   [L]-grounded")
    print(f"    -> from the DB's measured D-range, lambda in [{lo:.0f}, {hi:.0f}] um "
          f"(brackets real morphogen gradients; not fitted)\n")

    # recover lambda from a solved 3-D field (it is physics, not mesh)
    c, h = solve_field(32, 6*lam)
    print(f"  recovered from a solved 3-D field (N=32): lambda_measured = "
          f"{extract_lambda(c,h):.2f} um  (== sqrt(D*tau))")

    theta = territory_theta()
    T = territories(c, h)
    print(f"\n  POSITIONAL PARTITION (French-flag; theta={theta} [F]):  "
          f"territory width = lambda*ln(1/theta) = {lam*math.log(1/theta):.1f} um")
    print(f"  {'territory':>9s} {'outer bound (um)':>16s} {'~n*lambda*ln(1/th)':>18s} {'3-D vol frac':>13s}")
    for i,(b,fv) in enumerate(zip(T['boundaries_um'], T['band_volume_fracs'])):
        print(f"  {'#'+str(i+1):>9s} {b:>16.2f} {(i+1)*lam*math.log(1/theta):>18.2f} {fv:>13.4f}")
    print("    -> ordered, reproducible spatial partition EMERGES (grade [F])")

    print(f"\n  REALIZED COARSE FORM over developmental growth "
          f"(domain elongates ~ devtime^alpha, alpha={growth_alpha()} [F]):")
    print(f"  {'devtime':>7s} {'L (um)':>9s} {'#territories':>12s} {'apical axial-frac':>17s}")
    for t in (1.0, 1.5, 2.0, 3.0):
        f = realized_form(t)
        print(f"  {t:>7.1f} {f['L_um']:>9.1f} {f['n_territories']:>12d} {f['apical_axial_frac']:>17.4f}")

    allo = growing_domain_allometry([1.0,1.5,2.0,3.0])
    print(f"\n  EMERGENT NEGATIVE ALLOMETRY (mechanism, [F]): apical fraction ~ L^"
          f"{allo['frac_vs_L_exponent']}")
    print( "    fixed lambda in a growing domain -> leading territory loses body-fraction")
    print( "    as the domain grows -- the SAME sign Phase 2 measured, here from first")
    print( "    principles, with NO fraction fitted.")

    print(f"\n  GRADES: lambda-scale=[L]-grounded (measured D,tau) ; partition/form=[F] ;")
    print(f"          apical negative-allometry=[F] (mechanism) ; exact 3-D anatomy=[O].")
    print(f"  determinism: result sha={result_hash()}")
    print("="*86)
