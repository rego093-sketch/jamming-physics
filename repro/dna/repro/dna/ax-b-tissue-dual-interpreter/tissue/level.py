# -*- coding: utf-8 -*-
"""
tissue.level -- the LEVEL projection of the tissue field c(x): the "HOW BIG" channel.

Exact tissue analogue of the cell-level  gamma = mean( stiffness signal ).
At the cell level gamma is ONE scalar -- the average height of s(x) -- and it
carries NO position. Here the tissue LEVEL is ONE scalar -- the average height of
the morphogen field c(x) -- the total morphogen budget per unit area. It carries
no territory; territory is the SHAPE channel's job (tissue.shape), exactly as
shells/anchors are A4's job, never gamma's.

The LEVEL is what drives organ SIZE: a larger budget supports a larger structure.
It is computed in CLOSED FORM (planar: lambda*tanh(L/lambda)/L ; Yukawa: the exact
ball integral) -- there is no dwell(gamma, K=0.6, brake=0.5) here. The two inline
magic numbers that made the old size rule rough are gone; SIZE is now the exact
mean of a physically-grounded field.

Developmental growth enters through the ONE universal supply rule (extent ~
devtime^alpha, alpha from the locked DB) -- applied identically to all, never
per-organ. The absolute magnitude vs a real organ mass stays [O] (named obstacle:
a measured per-organ developmental growth-rate atlas).
"""
import math
import numpy as np

from . import lock, field


# ----------------------------------------------------------------------------
# planar LEVEL
# ----------------------------------------------------------------------------
def planar_level(L_um, lam_um=None):
    """Mean of the morphogen profile over [0, L]:
        LEVEL = (1/L) ∫_0^L p(x) dx = (lambda / L) * tanh(L/lambda)   (exact)
    One scalar. The tissue analogue of gamma = mean(s). Grade [V] (exact)."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    return field.planar_integral(L_um, lam_um) / L_um


def planar_budget(L_um, lam_um=None):
    """Total axial budget ∫_0^L p dx = lambda*tanh(L/lambda) (exact). The size-
    supporting quantity before dividing by domain length."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    return field.planar_integral(L_um, lam_um)


# ----------------------------------------------------------------------------
# developmental growth -> emergent SIZE (universal supply rule; no per-organ fit)
# ----------------------------------------------------------------------------
def domain_length_um(devtime, lam_um=None, t0=1.0):
    """Axial extent grows by the SAME universal rule the morphogenesis engine uses:
        L(devtime) = 6*lambda * (devtime/t0)^alpha
    alpha from the locked DB ([F] universal). Base span 6*lambda at t0. Not fitted."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    alpha, _, _ = lock.growth_alpha()
    return 6.0 * lam_um * (devtime / t0) ** alpha


def emergent_size(devtime, lam_um=None):
    """SIZE(devtime) = the morphogen BUDGET on the grown domain
        = ∫_0^{L(devtime)} p dx = lambda * tanh(L(devtime)/lambda)   (exact)
    The LEVEL channel's size readout. As L >> lambda this SATURATES at lambda --
    a fixed physical budget per unit area -- which is itself the mechanism behind
    negative size-allometry (a leading zone of fixed budget in a growing domain).
    Grade: functional form [F] (universal rule); absolute mass vs real organ [O]."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    L = domain_length_um(devtime, lam_um)
    return dict(devtime=devtime, L_um=round(L, 4),
                level_mean=round(planar_level(L, lam_um), 6),
                size_budget=round(planar_budget(L, lam_um), 6))


def size_series(devtimes, lam_um=None):
    """SIZE budget over developmental time -- the LEVEL channel trajectory."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    return [emergent_size(t, lam_um) for t in devtimes]


# ----------------------------------------------------------------------------
# the LEVEL read of a single tissue (one scalar + its grade)
# ----------------------------------------------------------------------------
def read_level(L_um, lam_um=None):
    """The complete LEVEL reading of one tissue domain. Returns the scalar plus an
    explicit statement that it carries no position (the discipline that keeps
    LEVEL and SHAPE from being conflated, mirroring 'gamma carries no position')."""
    if lam_um is None:
        lam_um = lock.lambda_um()
    return {
        "level_mean": round(planar_level(L_um, lam_um), 8),
        "size_budget": round(planar_budget(L_um, lam_um), 8),
        "carries_position": False,   # LEVEL is one scalar; position lives in SHAPE
        "closed_form": "lambda*tanh(L/lambda)/L",
        "grade_value": "[V] exact (precision)",
        "grade_size_vs_real_mass": "[O] needs measured per-organ developmental "
                                   "growth-rate atlas (engine does NOT compare)",
    }
