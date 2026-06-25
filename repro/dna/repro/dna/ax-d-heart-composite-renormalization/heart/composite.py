# -*- coding: utf-8 -*-
"""
heart.composite -- the TWO-PHASE composite renormalization for myocardium.

Appendix C renormalized ONE phase (cells) packed in VOID: density rho' = phi*rho,
stiffness bracketed by Reuss = 0 (void in series carries no load) and Voigt = phi*B, with
the effective modulus placed inside by the jamming rigidity fraction. That is the right
operator when the second phase is empty space. Myocardium is NOT cells-in-void: it is
cells embedded in a STIFF extracellular collagen matrix. So the second phase is not void
(B = 0) but the ECM (B = B_ECM > 0), and the bounds change accordingly.

THE EXACT TWO-PHASE ELASTIC-MIXTURE BOUNDS (Voigt 1889 / Reuss 1929 -- exact theorems):
  for a composite of a CELL phase (modulus B_c, volume fraction phi_c) and an ECM phase
  (modulus B_e, volume fraction phi_e = 1 - phi_c):

      Voigt (isostrain, UPPER)  B_V = phi_c * B_c + phi_e * B_e            [V] exact
      Reuss (isostress, LOWER)  1/B_R = phi_c / B_c + phi_e / B_e          [V] exact

  Any real isotropic composite modulus B_eff is GUARANTEED to satisfy B_R <= B_eff <= B_V
  (Hill 1952). These bounds carry NO free parameter; they are evaluated exactly here.

WHY THIS MATTERS FOR THE HEART (the discovery):
  * The CELL phase alone (Appendix C, ECM = void) gives B_eff <= phi_c * B_c <= B_c. For
    the EMBRYONIC heart the cell is soft (B_c ~ 1 kPa), so cells-in-void can reach AT MOST
    ~1 kPa -- yet the tissue stiffens to ~10-18 kPa. The stiff ECM phase is NECESSARY; the
    pure-jamming tower is FALSIFIED for the trajectory (heart.decomposition proves it).
  * Because the bounds are a VOLUME-WEIGHTED combination, raising the ECM fraction phi_e
    (collagen deposition, measured to rise over development) raises BOTH bounds -- a
    COMPOSITION flow. The stiffening is in the changing composition, not in the fixed
    sequence material gamma.

VP MASTER (the through-line): c = sqrt(B_eff / rho). Carried so the heart connects to the
same c^2 = B/rho relation as the vacuum core and the Appendix C tower; here B_eff is the
composite modulus and the passive elastic wave speed scales as sqrt(B_eff).

Deterministic; stdlib + numpy; constants from heart.lock; nothing fitted.
"""
import math
import numpy as np

from . import lock


# ----------------------------------------------------------------------------
# the exact two-phase bounds
# ----------------------------------------------------------------------------
def voigt_upper(B_cell, B_ecm, phi_cell):
    """Voigt (isostrain) UPPER bound: B_V = phi_c*B_c + phi_e*B_e. Exact. [V]."""
    phi_ecm = 1.0 - phi_cell
    return phi_cell * B_cell + phi_ecm * B_ecm


def reuss_lower(B_cell, B_ecm, phi_cell):
    """Reuss (isostress) LOWER bound: 1/B_R = phi_c/B_c + phi_e/B_e. Exact. [V].
    (Both phases have B > 0 here -- unlike the cells-in-void case where B_e=0 -> B_R=0.)"""
    phi_ecm = 1.0 - phi_cell
    inv = phi_cell / B_cell + phi_ecm / B_ecm
    return 1.0 / inv if inv > 0 else 0.0


def bracket(B_cell, B_ecm, phi_cell):
    """The exact [Reuss, Voigt] bracket the composite modulus must lie in, plus the
    geometric-mean midpoint (a common isotropic estimate) for reference."""
    B_R = reuss_lower(B_cell, B_ecm, phi_cell)
    B_V = voigt_upper(B_cell, B_ecm, phi_cell)
    mid = math.sqrt(B_R * B_V) if (B_R > 0 and B_V > 0) else 0.5 * (B_R + B_V)
    return {
        "B_reuss_lower_kpa": round(B_R, 6),
        "B_voigt_upper_kpa": round(B_V, 6),
        "B_geomean_mid_kpa": round(mid, 6),
        "phi_cell": phi_cell,
        "phi_ecm": round(1.0 - phi_cell, 6),
        "ordered": bool(B_R <= B_V + 1e-12),
        "grade": "[V] exact elastic-mixture theorems (Voigt 1889 / Reuss 1929; Hill 1952)",
    }


def contains(B_cell, B_ecm, phi_cell, B_measured):
    """Does the exact bracket CONTAIN a measured tissue modulus? Parameter-free given the
    measured phase moduli and fraction. This is the accuracy-CONSISTENCY check (gate D2)."""
    br = bracket(B_cell, B_ecm, phi_cell)
    inside = (br["B_reuss_lower_kpa"] - 1e-9) <= B_measured <= (br["B_voigt_upper_kpa"] + 1e-9)
    return {
        "B_measured_kpa": B_measured,
        "bracket_kpa": [br["B_reuss_lower_kpa"], br["B_voigt_upper_kpa"]],
        "contained": bool(inside),
        "where_in_bracket": (round((B_measured - br["B_reuss_lower_kpa"]) /
                                   max(br["B_voigt_upper_kpa"] - br["B_reuss_lower_kpa"], 1e-9), 4)
                             if br["B_voigt_upper_kpa"] > br["B_reuss_lower_kpa"] else None),
    }


# ----------------------------------------------------------------------------
# the cells-in-VOID (Appendix C pure-jamming) ceiling, for the falsification
# ----------------------------------------------------------------------------
def cell_jamming_ceiling(B_cell):
    """The MAXIMUM modulus a packing of cells in VOID (no ECM) can reach: the Voigt
    ceiling at full packing phi->1 is exactly B_cell (and the realized value, with the
    jamming fraction J<=1, is at most B_cell). So cells-in-void can never exceed the
    single-cell modulus. This is the ceiling the embryonic-cell trajectory must break,
    proving the ECM phase is necessary."""
    return B_cell


# ----------------------------------------------------------------------------
# VP master wave speed (the through-line)
# ----------------------------------------------------------------------------
def wave_speed_m_per_s(B_eff_kpa, rho=None):
    """Passive elastic wave speed c = sqrt(B/rho) (B in kPa -> Pa). The SAME relation the
    VP core applies to the vacuum; here for the composite myocardium. Distinct from the
    ACTIVE contraction wave (Majkut: linear in E_t), which is a separate phenomenon."""
    if rho is None:
        rho, _, _ = lock.cell_density_kg_per_m3()
    B_pa = B_eff_kpa * 1.0e3
    return math.sqrt(B_pa / rho) if (B_pa > 0 and rho > 0) else 0.0
