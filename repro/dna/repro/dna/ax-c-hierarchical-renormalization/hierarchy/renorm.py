# -*- coding: utf-8 -*-
"""
hierarchy.renorm -- the RENORMALIZATION OPERATOR R: the map that takes the units of one level
and produces the aggregate one level up. This is the formal statement of "세포들이 모이면
그자체로 부피이자 강성이 될것이다" -- when units pack, they become, by that act, both a
VOLUME (density rho) and a STIFFNESS (bulk modulus B).

THE OPERATOR R, on (B, rho) of the units packed at fraction phi:

  DENSITY (the "부피/volume" half) -- EXACT, no modelling choice:
      rho' = phi * rho                      (void contributes no mass; mass/volume conservation)
      V'(N units) = N * v / phi             (the aggregate volume holding N units)

  STIFFNESS (the "강성/stiffness" half) -- bracketed by EXACT theorems, placed by jamming:
      Reuss (isostress) lower bound : B_Reuss = 0          (a packing with void in series:
                                                            unjammed -> zero rigidity) [V]
      Voigt (isostrain) upper bound : B_Voigt = phi * B    (volume-weighted, void B=0) [V]
      effective modulus             : B' = phi * B * J(phi)
                                      with J(phi) in [0,1] the jamming rigidity fraction
                                      (hierarchy.jamming). Therefore  0 <= B' <= phi*B  ALWAYS,
                                      i.e. B' is GUARANTEED inside the exact bracket (gate H1).

  VP MASTER (the through-line) -- the wave speed at every level:
      c  = sqrt(B  / rho)        (units)
      c' = sqrt(B' / rho') = sqrt( (phi*B*J) / (phi*rho) ) = sqrt(B/rho) * sqrt(J) = c * sqrt(J)
  so the RENORMALIZATION SOFTENING RATIO per rung is EXACTLY  c'/c = sqrt(J(phi)).
  Because J in [0,1], the mechanical signal speed DECREASES (or, at the Voigt limit J=1, is
  preserved) under coarse-graining -- a clean, exact, falsifiable renormalization-group flow.

GRADES (the precision != accuracy discipline, enforced in hierarchy.grading):
  * rho' = phi*rho, V' = N*v/phi, and the softening ratio c'/c = sqrt(J)   -> [V] EXACT (precision)
  * Reuss=0, Voigt=phi*B bounds                                            -> [V] EXACT theorems
  * the placement B' = phi*B*J inside the bracket via the cited jamming onset -> [L]-grounded form
  * the ABSOLUTE moduli at each biological level (B0 in Pa, per-rung phi)   -> [O] named obstacles
  * monotone softening assumes uniform phi and no ECM stiffening           -> stated; real flow [O]

Deterministic; stdlib + numpy only; constants inherited from hierarchy.lock; nothing fitted.
"""
import math

from . import lock, jamming


# ----------------------------------------------------------------------------
# exact composite bounds (theorems) -- the bracket the effective modulus must lie in
# ----------------------------------------------------------------------------
def voigt_ceiling(B_unit, phi):
    """Voigt (isostrain) UPPER bound with a void phase (B_void=0): B_Voigt = phi * B_unit.
    Exact theorem. [V]."""
    return phi * B_unit


def reuss_floor(B_unit, phi):
    """Reuss (isostress) LOWER bound with a void phase (B_void=0): B_Reuss = 0.
    A packing with any void in series carries no load -> an UNJAMMED packing has zero rigidity.
    Exact theorem. [V]. (B_unit, phi accepted for signature symmetry; result is identically 0.)"""
    return 0.0


# ----------------------------------------------------------------------------
# the renormalization operator R -- one rung up
# ----------------------------------------------------------------------------
def renormalize(B, rho, phi, c=None):
    """One application of R: units (B, rho) packed at fraction phi -> aggregate (B', rho', c').

    Returns a dict with the aggregate moduli, the exact bracket, the rigidity fraction, and the
    wave-speed softening ratio. Every field carries the relation it came from.
    """
    J = float(jamming.rigidity_fraction(phi))
    B_voigt = voigt_ceiling(B, phi)
    B_reuss = reuss_floor(B, phi)

    B_eff = phi * B * J                 # placed inside [B_reuss, B_voigt] by construction
    rho_eff = phi * rho                 # exact

    if c is None:
        c = math.sqrt(B / rho) if (B > 0 and rho > 0) else 0.0
    c_eff = (c * math.sqrt(J)) if J > 0 else 0.0     # = sqrt(B_eff/rho_eff), exact

    # the bracket must contain B_eff -- this is what the gate (H1) asserts, here for the record
    within_bracket = (B_reuss - 1e-15) <= B_eff <= (B_voigt + 1e-15)

    return {
        "phi": float(phi),
        "rigidity_fraction_J": round(J, 10),
        "B_unit": B,
        "B_reuss_floor": B_reuss,             # exact lower theorem
        "B_voigt_ceiling": round(B_voigt, 10),  # exact upper theorem
        "B_eff": round(B_eff, 10),            # placed inside the bracket
        "B_eff_within_bracket": bool(within_bracket),
        "rho_unit": rho,
        "rho_eff": round(rho_eff, 10),        # exact: phi * rho
        "c_unit": round(c, 10),
        "c_eff": round(c_eff, 10),            # exact: c * sqrt(J)
        "softening_ratio_c_eff_over_c": round(math.sqrt(J), 10),  # exact = sqrt(J)
        "grades": {
            "rho_eff": "[V] exact (phi*rho; mass/volume conservation)",
            "bounds": "[V] exact theorems (Reuss=0, Voigt=phi*B)",
            "B_eff_placement": "[L]-grounded (jamming onset sqrt((phi-phi_c)/(1-phi_c)))",
            "softening_ratio": "[V] exact (= sqrt(J); the VP master c^2=B/rho applied twice)",
            "absolute_modulus": "[O] needs measured per-scale modulus atlas",
        },
    }


# ----------------------------------------------------------------------------
# composition / associativity -- climbing two rungs == climbing one combined rung
# ----------------------------------------------------------------------------
def compose_two(B, rho, phi1, phi2, c=None):
    """Apply R twice (phi1 then phi2) and ALSO compute the single-step product, to witness
    that R composes exactly (the renormalization-group semigroup property). Returns both and
    their max discrepancy (must be ~0 -> gate H4)."""
    if c is None:
        c = math.sqrt(B / rho) if (B > 0 and rho > 0) else 0.0
    # two explicit rungs
    r1 = renormalize(B, rho, phi1, c)
    r2 = renormalize(r1["B_eff"], r1["rho_eff"], phi2, r1["c_eff"])
    # direct product form
    J1 = float(jamming.rigidity_fraction(phi1))
    J2 = float(jamming.rigidity_fraction(phi2))
    B_direct = phi2 * (phi1 * B * J1) * J2
    rho_direct = phi2 * phi1 * rho
    c_direct = c * math.sqrt(J1 * J2) if (J1 > 0 and J2 > 0) else 0.0
    disc = max(abs(r2["B_eff"] - B_direct),
               abs(r2["rho_eff"] - rho_direct),
               abs(r2["c_eff"] - c_direct))
    return {
        "stepwise": {"B_eff": r2["B_eff"], "rho_eff": r2["rho_eff"], "c_eff": r2["c_eff"]},
        "direct_product": {"B_eff": round(B_direct, 10), "rho_eff": round(rho_direct, 10),
                           "c_eff": round(c_direct, 10)},
        "max_discrepancy": disc,
        "composes_exactly": disc < 1e-9,
        "grade": "[V] exact: R composes (renormalization-group semigroup)",
    }
