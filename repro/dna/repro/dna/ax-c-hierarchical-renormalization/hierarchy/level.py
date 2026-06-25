# -*- coding: utf-8 -*-
"""
hierarchy.level -- the LEVEL projection of a level's STIFFNESS FIELD B(x): the "HOW STIFF" channel.

This is the mechanical-scale analogue of the cell-level gamma = mean(stiffness signal) and the
tissue-level LEVEL = mean(morphogen field). Here the field is the spatial bulk-modulus map of a
structural level, B(x) = B_unit * phi(x) * J(phi(x)) -- the local stiffness wherever the local
packing is phi(x). The LEVEL is its spatial mean:

    LEVEL = mean(B(x))          -> the effective modulus of the level (the size/quantity of stiffness)

It carries NO position -- position is the SHAPE channel's job (hierarchy.shape), exactly as
gamma carries no position and shells/anchors are A4's job. The LEVEL is the scalar that the
renormalization operator flows up the ladder.

Closed form for a uniform level: B(x) = const = B_unit*phi*J(phi) -> LEVEL = B_unit*phi*J(phi),
which is exactly the renorm operator's B_eff. For a structured level (phi varying across the
domain) the LEVEL is the exact mean of the closed-form stiffness map. No grid, no magic numbers.

Absolute magnitude vs a real level's MEASURED modulus stays [O] (named obstacle: a per-scale
elastography/AFM modulus atlas). The FORM of the mean is exact [V].
"""
import numpy as np

from . import lock, jamming


def stiffness_field(phi_x, B_unit=None):
    """The local bulk-modulus map B(x) = B_unit * phi(x) * J(phi(x)) over a packing-fraction
    profile phi(x). Exact, pointwise. phi_x may be scalar or array."""
    if B_unit is None:
        B_unit, _, _ = lock.unit_bulk_modulus_pa()
    phi_x = np.asarray(phi_x, dtype=np.float64)
    J = jamming.rigidity_fraction(phi_x)
    return B_unit * phi_x * J


def level_mean(phi_x, B_unit=None):
    """LEVEL = mean(B(x)) -- the effective modulus of the level (the gamma-mirror scalar).
    One number; carries no position. [V] exact (mean of a closed-form map)."""
    return float(np.mean(stiffness_field(phi_x, B_unit)))


def read_level(phi_x, B_unit=None):
    """The complete LEVEL reading of one structural level: the effective-modulus scalar plus an
    explicit statement that it carries no position (keeping LEVEL and SHAPE from being conflated,
    mirroring 'gamma carries no position')."""
    if B_unit is None:
        B_unit, gB, _ = lock.unit_bulk_modulus_pa()
    else:
        gB = "[F]"
    return {
        "level_effective_modulus_pa": round(level_mean(phi_x, B_unit), 6),
        "carries_position": False,     # LEVEL is one scalar; position lives in SHAPE
        "closed_form": "mean( B_unit * phi(x) * J(phi(x)) )",
        "grade_value": "[V] exact mean (precision)",
        "grade_modulus_vs_real": "[O] needs measured per-scale modulus atlas "
                                 "(elastography/AFM); engine does NOT compare (would be back-fit)",
    }
