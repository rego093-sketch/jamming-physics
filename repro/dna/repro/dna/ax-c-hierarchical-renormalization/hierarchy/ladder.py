# -*- coding: utf-8 -*-
"""
hierarchy.ladder -- the explicit BIOLOGICAL LADDER and the climb up it.

Appendix B dualized exactly TWO scales (cell gamma/A4; tissue morphogen LEVEL/SHAPE) and treated
them as unconnected -- the tissue constants were looked up, never DERIVED from the cell. That was
the over-simplification: real biology is a TOWER of structural levels, and each level is built by
PACKING the level below. This module makes the tower explicit and climbs it with the
renormalization operator R (hierarchy.renorm), so each level's stiffness and density are DERIVED
from the level below, not assumed.

THE LADDER (characteristic length scales, [F] generic central values from hierarchy.lock):
    L0  molecular / chromatin   ~ 11 nm   (nucleosome; where gamma lives)
    L1  cell                    ~ 10 um
    L2  tissue (functional unit)~ 100 um  (where morphogen LEVEL/SHAPE lives -- Appendix B)
    L3  organ                   ~ 1 cm
    L4  organ system / body     ~ 0.1-1 m

UNITS PER RUNG (counting, exact given the lengths):
    a level of size ell_{k+1} built from units of size ell_k holds, at packing fraction phi,
        N_k = phi * (ell_{k+1} / ell_k)^d         (d = 3)
    units. (N is reported for scale; the FLOW of B, rho, c does not depend on N -- it depends on
    phi through J only. So the ladder's mechanical content is phi-controlled, length-independent.)

THE CLIMB:
    start at the BASE unit (cell) with (B0, rho0) from the DB ([O] absolute), c0 = sqrt(B0/rho0).
    at each rung apply R with that rung's packing fraction phi_k:
        B_{k+1} = phi_k B_k J(phi_k);  rho_{k+1} = phi_k rho_k;  c_{k+1} = c_k sqrt(J(phi_k))
    and record the exact Voigt/Reuss bracket and the softening ratio.

WHAT IS EXACT AND WHAT IS OPEN (precision != accuracy):
    * the softening ratio c_{k+1}/c_k = sqrt(J(phi_k)), the density law rho_{k+1}=phi_k rho_k,
      and the composition over rungs are EXACT [V].
    * for UNIFORM phi the wave speed decreases MONOTONICALLY up the tower -- an exact RG theorem
      of the idealized ladder.
    * the ABSOLUTE moduli per real level need a measured elastography/AFM atlas [O]; real per-rung
      phi needs measured stereology [O]; and ECM stiffening (cartilage/bone) can RAISE the unit
      modulus and break monotonicity -- so the real biological flow is [O], stated plainly.

Deterministic; constants from hierarchy.lock; nothing fitted.
"""
import math

from . import lock, jamming, renorm


def units_per_rung(phi, ell_lo_um, ell_hi_um):
    """N = phi * (ell_hi/ell_lo)^d -- how many lower units pack into one upper unit. Reported
    for scale; the mechanical flow does not depend on N."""
    d, _, _ = lock.dimension_d()
    return phi * (ell_hi_um / ell_lo_um) ** d


def default_phi_profile():
    """A documented per-rung packing-fraction profile used for the demonstration climb.
    All values are ABOVE phi_c (so every rung is jammed/rigid) but BELOW 1; they are a modelling
    choice [F] standing in for measured per-rung stereology [O]. The operator is general in phi --
    swapping these for measured fractions changes only the numbers, not the machinery."""
    pc, _, _ = lock.phi_c()
    n_steps = len(lock.ladder_rungs()) - 2   # climb from the cell (idx 1) up to the top
    # evenly spaced jammed fractions in (phi_c, 1): a transparent, non-tuned set
    return [round(pc + (i + 1) * (1.0 - pc) / (n_steps + 1), 6) for i in range(n_steps)]


def climb(phis=None):
    """Climb the ladder from the base unit (cell) to the top, applying R at each rung.

    Returns the per-level trajectory of (B, rho, c), the exact bracket and softening ratio at
    each rung, and the monotonicity verdict for the wave speed. phis defaults to a documented
    jammed profile; pass a measured per-rung phi list to get the real flow (still graded [O] in
    absolute magnitude)."""
    rungs = lock.ladder_rungs()
    if phis is None:
        phis = default_phi_profile()

    B0, gB0, _ = lock.unit_bulk_modulus_pa()
    rho0, _, _ = lock.unit_density_kg_per_m3()
    c0 = math.sqrt(B0 / rho0)

    # base level = the CELL (rung index 1 in the ladder; L0 is the molecular substrate that
    # sets the cell's own gamma, read at the cell level by the existing engine).
    levels = [{
        "level": rungs[1]["level"],
        "name": rungs[1]["name"],
        "length_um": rungs[1]["length_um"],
        "B_pa": round(B0, 6),
        "rho_kg_per_m3": round(rho0, 6),
        "c_m_per_s": round(c0, 6),
        "role": "BASE unit (cell): (B,rho) from DB; absolute [O], c0=sqrt(B0/rho0)",
    }]

    B, rho, c = B0, rho0, c0
    rung_reports = []
    speeds = [c0]
    # climb from the cell (ladder index 1) upward; never index past the top rung
    n_steps = min(len(phis), len(rungs) - 2)
    for k in range(n_steps):
        phi = phis[k]
        ell_lo = rungs[1 + k]["length_um"]
        ell_hi = rungs[2 + k]["length_um"]
        N = units_per_rung(phi, ell_lo, ell_hi)
        step = renorm.renormalize(B, rho, phi, c)
        B, rho, c = step["B_eff"], step["rho_eff"], step["c_eff"]
        speeds.append(c)
        levels.append({
            "level": rungs[2 + k]["level"],
            "name": rungs[2 + k]["name"],
            "length_um": ell_hi,
            "phi_used": phi,
            "units_packed_from_below": round(N, 3),
            "B_pa": round(B, 6),
            "rho_kg_per_m3": round(rho, 6),
            "c_m_per_s": round(c, 6),
            "rigidity_fraction_J": step["rigidity_fraction_J"],
            "softening_ratio_c_over_prev": step["softening_ratio_c_eff_over_c"],
            "B_within_bracket": step["B_eff_within_bracket"],
        })
        rung_reports.append({
            "from_level": rungs[1 + k]["name"], "to_level": rungs[2 + k]["name"],
            "phi": phi,
            "B_reuss_floor": step["B_reuss_floor"],
            "B_voigt_ceiling": step["B_voigt_ceiling"],
            "B_eff": step["B_eff"],
            "softening_ratio": step["softening_ratio_c_eff_over_c"],
        })

    # monotone-softening verdict (exact for uniform phi; here phis vary but each J<1 -> each rung
    # softens, so the sequence is still strictly decreasing as long as every phi<1)
    monotone_soft = all(speeds[i] >= speeds[i + 1] - 1e-12 for i in range(len(speeds) - 1))

    return {
        "_what": "renormalization climb up the biological ladder: each level's (B,rho,c) DERIVED "
                 "from the level below by R (jamming), not assumed",
        "phi_profile_used": phis,
        "phi_profile_grade": "[F] documented jammed profile standing in for measured per-rung "
                             "stereology [O]",
        "levels": levels,
        "rung_brackets": rung_reports,
        "wave_speed_trajectory_m_per_s": [round(s, 6) for s in speeds],
        "wave_speed_monotone_decreasing": bool(monotone_soft),
        "note": "softening ratio per rung = sqrt(J(phi)) is EXACT [V]; monotone decrease holds for "
                "any phi<1 (idealized, no ECM stiffening). ABSOLUTE moduli per real level are [O].",
    }
