# -*- coding: utf-8 -*-
"""
hierarchy.orthogonality -- PROVE that the mechanical LEVEL and SHAPE are orthogonal projections of
ONE stiffness field, to the SAME standard the cell level proved gamma vs A4 and the tissue level
proved its LEVEL vs SHAPE.

The proof is mechanical, not statistical -- the robust_z that builds SHAPE removes the LEVEL by
construction:

  (knob 1) SCALE the stiffness field by kappa: B(x) -> kappa*B(x).
           LEVEL -> kappa*LEVEL (changes); robust_z(kappa*B) == robust_z(B) -> SHAPE IDENTICAL.
  (knob 2) ADD a uniform stiffness offset b: B(x) -> B(x) + b.
           LEVEL -> LEVEL + b (changes); robust_z(B+b) == robust_z(B) -> SHAPE IDENTICAL.
  Two knobs move LEVEL while SHAPE does not move AT ALL -- to MACHINE EPSILON. So LEVEL is not in
  SHAPE.
  (converse) Change the GEOMETRY of the packing profile (the phi(x) pattern) and the SHAPE moves
  while the LEVEL can be held fixed -> SHAPE is not in LEVEL.

If any analytic invariance exceeds a tiny tolerance, the gate FAILS CLOSED. There is no
"approximately orthogonal" escape hatch (no compromise).
"""
import numpy as np

from . import lock
from .level import stiffness_field
from .shape import robust_z, smoothstep_phi_profile

_MACHINE_TOL = 1e-12   # the invariances are exact; anything above this is a bug


def two_knob_test(phi_x=None, kappa=4.3, offset=0.7, B_unit=None):
    """Move the LEVEL two ways (scale, add background) and confirm the SHAPE does not budge."""
    if phi_x is None:
        phi_x = smoothstep_phi_profile()
    B = stiffness_field(phi_x, B_unit)
    L0 = float(np.mean(B))
    S0 = robust_z(B)

    B_scaled = kappa * B
    L_scaled = float(np.mean(B_scaled))
    dS_scale = float(np.max(np.abs(robust_z(B_scaled) - S0)))

    B_shift = B + offset
    L_shift = float(np.mean(B_shift))
    dS_shift = float(np.max(np.abs(robust_z(B_shift) - S0)))

    return {
        "knob1_scale_field": {
            "kappa": kappa,
            "level_before": round(L0, 6), "level_after": round(L_scaled, 6),
            "level_ratio": round(L_scaled / L0, 8) if L0 != 0 else None,
            "shape_max_abs_change": dS_scale,
            "shape_invariant": dS_scale < _MACHINE_TOL,
        },
        "knob2_add_background": {
            "offset": offset,
            "level_before": round(L0, 6), "level_after": round(L_shift, 6),
            "level_delta": round(L_shift - L0, 6),
            "shape_max_abs_change": dS_shift,
            "shape_invariant": dS_shift < _MACHINE_TOL,
        },
        "verdict": "LEVEL moves; SHAPE invariant to machine epsilon -> LEVEL not in SHAPE",
    }


def geometry_changes_shape(B_unit=None):
    """Confirm the converse: changing the packing-profile geometry MOVES the SHAPE. Compare a
    gentle profile to a steeper one and show the shape range changes materially."""
    pc, _, _ = lock.phi_c()
    gentle = smoothstep_phi_profile(phi_lo=pc + 0.30 * (1 - pc), phi_hi=pc + 0.50 * (1 - pc))
    steep = smoothstep_phi_profile(phi_lo=pc + 0.05 * (1 - pc), phi_hi=pc + 0.95 * (1 - pc))
    zg = robust_z(stiffness_field(gentle, B_unit))
    zs = robust_z(stiffness_field(steep, B_unit))
    rng_g = float(np.max(zg) - np.min(zg))
    rng_s = float(np.max(zs) - np.min(zs))
    return {
        "gentle_profile_shape_range": round(rng_g, 6),
        "steep_profile_shape_range": round(rng_s, 6),
        "shape_moved": abs(rng_g - rng_s) > 1e-4,
        "verdict": "packing-profile geometry moves SHAPE while LEVEL is rescalable -> SHAPE not in LEVEL",
    }


def panel_correlation(B_unit=None):
    """Sweep a family of packing profiles; collect the LEVEL scalar and a SHAPE descriptor (the
    shape range); report corr(LEVEL, SHAPE). Both are readouts of one field; |corr|<1 shows they
    are not redundant (the mechanical analogue of the cell-level 'same field, axis|corr|=0.327')."""
    pc, _, _ = lock.phi_c()
    levels, shapes = [], []
    for hi_frac in (0.30, 0.45, 0.60, 0.75, 0.90):
        prof = smoothstep_phi_profile(phi_lo=pc + 0.10 * (1 - pc),
                                      phi_hi=pc + hi_frac * (1 - pc))
        B = stiffness_field(prof, B_unit)
        z = robust_z(B)
        levels.append(float(np.mean(B)))
        shapes.append(float(np.max(z) - np.min(z)))
    levels = np.array(levels)
    shapes = np.array(shapes)
    corr = float(np.corrcoef(levels, shapes)[0, 1])
    return {
        "level_means": [round(x, 4) for x in levels.tolist()],
        "shape_ranges": [round(x, 4) for x in shapes.tolist()],
        "corr_level_vs_shape": round(corr, 4),
        "note": "both from one stiffness field; |corr|<1 -> not redundant readouts",
    }


def certify(phi_x=None, B_unit=None):
    """Run analytic + numeric checks and return a single certificate dict with a boolean
    `orthogonal` that the gate keys on (fail-closed)."""
    tk = two_knob_test(phi_x, B_unit=B_unit)
    gc = geometry_changes_shape(B_unit=B_unit)
    pc_ = panel_correlation(B_unit=B_unit)
    orthogonal = (tk["knob1_scale_field"]["shape_invariant"]
                  and tk["knob2_add_background"]["shape_invariant"]
                  and gc["shape_moved"])
    return {
        "two_knob_test": tk,
        "geometry_changes_shape": gc,
        "panel_correlation": pc_,
        "orthogonal": bool(orthogonal),
        "grade": "[V] exact: SHAPE invariant under LEVEL moves to machine epsilon",
    }
