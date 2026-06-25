# -*- coding: utf-8 -*-
"""
hierarchy.shape -- the SHAPE projection of a level's STIFFNESS FIELD B(x): the "WHERE STIFF" channel.

Mechanical-scale analogue of the cell-level A4 coordinate and the tissue-level SHAPE. At the cell
level A4 is built by taking the stiffness signal and SUBTRACTING ITS OWN MEDIAN (robust_z) -- i.e.
removing the very number that IS gamma -- so "gamma in A4" is impossible. Here the SHAPE is built
by the IDENTICAL robust_z applied to the stiffness map B(x): it removes the LEVEL (the effective
modulus) and keeps the PATTERN -- where the level is stiffer or softer, and where the stiffness
CLIFFS (the mechanical "anchors") sit. So the LEVEL is not inside the SHAPE: they are the level
and the shape of ONE stiffness field, two orthogonal projections (proven in
hierarchy.orthogonality).

robust_z is byte-identical to key_pipeline_full.robust_z (the cell-level engine) and to
tissue.shape.robust_z (Appendix B):
    z = (x - median(x)) / (1.4826 * max(MAD, eps))
The level/shape split is ONE idea applied at every scale -- molecular, cell, tissue, and now the
mechanical aggregate at every rung of the tower.

The packing-fraction profile phi(x) that gives a non-trivial stiffness pattern is, in real
biology, set by where different cell types / packings sit -- naturally the morphogen TERRITORIES
of Appendix B. Here we use a documented phi(x) profile for the orthogonality DEMONSTRATION; the
orthogonality MATH (LEVEL perp SHAPE) is what is [V] exact, the specific phi(x) is illustrative and
its real form is [O] (named obstacle: a measured packing-density / cell-type territory map).
"""
import numpy as np

from . import lock, jamming
from .level import stiffness_field

_EPS = 1e-9   # identical role to key_pipeline_full.LOCK['eps'] and tissue.shape._EPS


def robust_z(x, eps=_EPS):
    """Median-removed, MAD-scaled signal. Byte-identical to the cell-level and tissue-level
    robust_z. This is the operator that REMOVES the level."""
    x = np.asarray(x, dtype=np.float64)
    m = np.median(x)
    d = np.median(np.abs(x - m))
    return (x - m) / (1.4826 * max(d, eps))


def smoothstep_phi_profile(n=4001, phi_lo=None, phi_hi=None):
    """A documented packing-fraction profile phi(x) rising smoothly from phi_lo to phi_hi across
    the domain (a transparent stand-in for a measured cell-type/packing territory map). Both
    endpoints are above phi_c so the whole level is jammed. Modelling choice [F]; real phi(x) [O]."""
    pc, _, _ = lock.phi_c()
    if phi_lo is None:
        phi_lo = pc + 0.10 * (1.0 - pc)
    if phi_hi is None:
        phi_hi = pc + 0.80 * (1.0 - pc)
    t = np.linspace(0.0, 1.0, n)
    s = t * t * (3.0 - 2.0 * t)              # smoothstep, deterministic
    return phi_lo + (phi_hi - phi_lo) * s


def shape_field(phi_x=None, B_unit=None):
    """The mean-removed SHAPE of the stiffness map: robust_z(B(x)). Carries the pattern; the level
    is gone. Returns the robust-z array."""
    if phi_x is None:
        phi_x = smoothstep_phi_profile()
    return robust_z(stiffness_field(phi_x, B_unit))


def stiffness_anchors(phi_x=None, B_unit=None, z_thresh=0.0):
    """The mechanical 'anchors': indices where the stiffness SHAPE crosses a level (the cliffs
    where soft meets stiff), mirroring A4's shell-boundary anchors. Reported as crossing fractions
    of the domain. Exact crossings of the closed-form field."""
    if phi_x is None:
        phi_x = smoothstep_phi_profile()
    z = shape_field(phi_x, B_unit)
    n = len(z)
    crossings = []
    for i in range(1, n):
        if (z[i - 1] - z_thresh) * (z[i] - z_thresh) <= 0.0 and (z[i - 1] != z[i]):
            # linear interpolation of the crossing position, in domain fraction
            frac = (i - 1 + (z_thresh - z[i - 1]) / (z[i] - z[i - 1])) / (n - 1)
            crossings.append(round(float(frac), 6))
    return crossings


def read_shape(phi_x=None, B_unit=None):
    """The complete SHAPE reading of one structural level: the stiffness pattern's range, its
    anchors (zero-crossings of the mean-removed map), and an explicit statement that the level is
    removed (what makes it SHAPE). All exact on the closed-form field."""
    if phi_x is None:
        phi_x = smoothstep_phi_profile()
    z = shape_field(phi_x, B_unit)
    anchors = stiffness_anchors(phi_x, B_unit)
    return {
        "shape_z_min": round(float(np.min(z)), 6),
        "shape_z_max": round(float(np.max(z)), 6),
        "stiffness_anchor_fracs": anchors,
        "n_anchors": len(anchors),
        "level_removed": True,         # SHAPE = stiffness map with the LEVEL taken out
        "operator": "robust_z = (B - median(B)) / (1.4826*MAD)  [identical to cell-level A4]",
        "grade_form": "[V] exact (precision)",
        "grade_form_vs_real": "[O] needs measured packing-density / cell-type territory map "
                              "(naturally the Appendix B morphogen territories)",
    }
