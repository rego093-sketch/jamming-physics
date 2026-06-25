# -*- coding: utf-8 -*-
"""
tissue.field -- the ONE tissue-level field c(x), solved EXACTLY (closed form).

This is the tissue analogue of the cell-level stiffness signal s(x). Where the
old emergence_trajectory.py solved the screened-Poisson equation with a COARSE
N=32 Jacobi iteration (lambda recovered as 60.55 um vs the exact 60.00 -- a
0.9% coarse-grid artifact; territory boundary 41.92 vs the exact 41.59 -- 0.8%),
this module supplies the EXACT closed form and keeps the Jacobi ONLY as a
convergence witness. We do not patch the rough solver; we supersede it and PROVE
the supersession (handover rule A3: delete rough code, do not patch around it).

Two canonical source geometries, each with an exact closed form:

  PLANAR  (full x=0 face source, Neumann/zero-flux far wall at x=L):
      D c'' - c/tau = 0  ->  c(x) = cosh((L-x)/lambda) / cosh(L/lambda)
      c(0)=1 exactly ; c'(L)=0 exactly. For L>>lambda -> exp(-x/lambda).
      (For a uniform-face source with zero-flux side walls the 3-D field is
       SEPARABLE and depends only on x -- the "collapse to 1-D" the old code did
       approximately is here EXACT, proven by transverse-variance == 0.)

  POINT   (3-D point source, screened-Coulomb / Yukawa Green's function):
      D laplacian(c) - c/tau + S delta^3(r) = 0
      c(r) = (S / 4 pi D) * exp(-r/lambda) / r       (exact)

Everything is deterministic, numpy + stdlib only. lambda is inherited from
tissue.lock (measured D, tau); NOTHING here is fitted.
"""
import math
import numpy as np

from . import lock


# ============================================================================
# PLANAR geometry -- exact closed form
# ============================================================================
def planar_profile(x_um, L_um, lam_um=None):
    """Exact normalized morphogen profile p(x) = cosh((L-x)/lam)/cosh(L/lam).

    x_um may be a scalar or an array. Returns p in (0, 1], p(0)=1, p'(L)=0.
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    x = np.asarray(x_um, dtype=np.float64)
    return np.cosh((L_um - x) / lam_um) / math.cosh(L_um / lam_um)


def planar_integral(L_um, lam_um=None):
    """Exact axial integral  ∫_0^L p(x) dx = lambda * tanh(L/lambda).

    This is the LEVEL channel's analytic backbone -- the total morphogen budget
    per unit transverse area. Closed form; no quadrature, no grid.
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    return lam_um * math.tanh(L_um / lam_um)


def planar_min(L_um, lam_um=None):
    """The profile minimum p(L) = sech(L/lambda). A threshold below this value is
    never reached on the domain (the SHAPE module clamps such boundaries to L)."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    return 1.0 / math.cosh(L_um / lam_um)


def planar_threshold_crossing(level, L_um, lam_um=None):
    """Exact axial position where p(x) == level:
        x_k = L - lambda * acosh(level * cosh(L/lambda))
    valid when level >= sech(L/lambda); else the threshold is never reached and
    the territory extends to the wall (return L). Inverse of the closed form --
    NOT a sub-grid interpolation of a coarse field.
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    arg = level * math.cosh(L_um / lam_um)
    if arg < 1.0:                       # below the profile minimum -> never crossed
        return float(L_um)
    return float(L_um - lam_um * math.acosh(arg))


# ============================================================================
# POINT geometry -- exact Yukawa Green's function
# ============================================================================
def yukawa_profile(r_um, r0_um, lam_um=None):
    """Exact normalized Yukawa profile relative to a reference radius r0:
        p(r) = (r0 / r) * exp(-(r - r0)/lambda)     (p(r0) = 1)
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    r = np.asarray(r_um, dtype=np.float64)
    return (r0_um / r) * np.exp(-(r - r0_um) / lam_um)


def yukawa_ball_integral(R_um, lam_um=None):
    """Exact morphogen budget in a ball of radius R for a unit-strength point
    source with S/D = 1:
        ∫_ball c dV = lambda^2 * [1 - e^{-R/lambda}(1 + R/lambda)]
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    x = R_um / lam_um
    return lam_um * lam_um * (1.0 - math.exp(-x) * (1.0 + x))


def yukawa_threshold_radius(level, r0_um, lam_um=None):
    """Exact radius where the Yukawa profile p(r) == level, via the Lambert W
    function (principal branch):  p(r)=level  ->  r = lambda * W(arg),
    arg = (r0 / (level*lambda)) * exp(r0/lambda).  Closed form (special fn).
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    arg = (r0_um / (level * lam_um)) * math.exp(r0_um / lam_um)
    return float(lam_um * _lambert_w0(arg))


def _lambert_w0(z, tol=1e-15, maxit=100):
    """Principal branch Lambert W (W0) for z >= 0, Halley's method, machine-exact.
    No SciPy dependency (the kit is numpy + stdlib only)."""
    if z < 0:
        raise ValueError("tissue.field._lambert_w0: domain is z >= 0")
    if z == 0.0:
        return 0.0
    # initial guess: good for both small and large z
    w = math.log(z) - math.log(math.log(z)) if z > math.e else z / (1.0 + z)
    for _ in range(maxit):
        ew = math.exp(w)
        f = w * ew - z
        denom = ew * (w + 1.0) - (w + 2.0) * f / (2.0 * w + 2.0)
        dw = f / denom
        w -= dw
        if abs(dw) <= tol * (1.0 + abs(w)):
            break
    return w


# ============================================================================
# CONVERGENCE WITNESS -- the deterministic Jacobi solver, kept ONLY to prove the
# closed form is the truth and the old N=32 grid was the rough approximation.
# ============================================================================
def jacobi_planar_field(N, L_um, lam_um=None, tol=1e-12, maxit=200000):
    """Steady-state morphogen field on an N^3 box (x=0 face Dirichlet=1; other
    faces zero-flux Neumann). Jacobi to a fixed residual. Returns (c, h).

    This is the SAME scheme the old emergence_trajectory used -- reproduced here
    so the gate can show its discretization error SHRINKS toward the closed form
    as N grows (i.e. it was a grid artifact, never the physics).
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    D, _, _ = lock.diffusion_um2_per_s()
    decay_min, _, _ = lock.morphogen_decay_min()
    tau_s = decay_min * 60.0
    h = L_um / (N - 1)
    a = D / h ** 2
    m = 1.0 / tau_s
    denom = 6.0 * a + m
    c = np.zeros((N, N, N))
    src = np.zeros((N, N, N), bool)
    src[0, :, :] = True
    c[src] = 1.0
    for _ in range(maxit):
        cp = np.pad(c, 1, mode="edge")
        s = (cp[2:, 1:-1, 1:-1] + cp[:-2, 1:-1, 1:-1]
             + cp[1:-1, 2:, 1:-1] + cp[1:-1, :-2, 1:-1]
             + cp[1:-1, 1:-1, 2:] + cp[1:-1, 1:-1, :-2])
        cn = a * s / denom
        cn[src] = 1.0
        if np.max(np.abs(cn - c)) < tol:
            c = cn
            break
        c = cn
    return c, h


def jacobi_axis_profile(c):
    """Central-axis profile of a solved 3-D field, normalized to its source value."""
    N = c.shape[0]
    ax = (N - 1) // 2
    p = c[:, ax, ax].copy()
    return p / p[0]


def transverse_variance(c):
    """Max variance across the transverse (y,z) plane at each x-slice. For the
    separable full-face geometry this is 0 to machine epsilon -- the EXACT proof
    that the field depends only on x (so the 1-D closed form is the 3-D truth)."""
    return float(np.max(np.var(c.reshape(c.shape[0], -1), axis=1)))


def convergence_to_closed_form(L_um, Ns=(16, 24, 32, 48), lam_um=None):
    """For each grid N, recover lambda from the Jacobi field's far-field axial
    slope and compare to the exact lambda. Returns the shrinking error table --
    the witness that the old coarse solver was rough, not the physics.
    """
    if lam_um is None:
        lam_um = lock.lambda_um()
    rows = []
    for N in Ns:
        c, h = jacobi_planar_field(N, L_um, lam_um)
        p = jacobi_axis_profile(c)
        xs = np.arange(c.shape[0]) * h
        sel = (xs >= 1.0 * lam_um) & (xs <= 4.5 * lam_um) & (p > 1e-9)
        slope = np.polyfit(xs[sel], np.log(p[sel]), 1)[0]
        lam_meas = -1.0 / slope
        rows.append(dict(N=N,
                         lambda_jacobi=round(float(lam_meas), 5),
                         lambda_exact=round(lam_um, 5),
                         rel_err_pct=round(abs(lam_meas - lam_um) / lam_um * 100.0, 4),
                         transverse_var=round(transverse_variance(c), 3)))
    return rows
