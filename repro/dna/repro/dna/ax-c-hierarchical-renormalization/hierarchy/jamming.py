# -*- coding: utf-8 -*-
"""
hierarchy.jamming -- the rigidity-emergence physics: how a packing of soft units acquires a
modulus. This is the "강성" (stiffness) half of "cells gather and become volume and stiffness."

THE PHYSICAL STATEMENT (grounded, not invented):
  A loose packing of units (phi < phi_c) is a FLUID -- it has zero rigidity; each unit moves
  without impediment. At a sharp critical packing fraction phi_c -- the jamming point, point J
  -- a rigid contact network percolates and the bulk and shear moduli simultaneously become
  non-zero (O'Hern, Silbert, Liu & Nagel 2003, PRE 68:011306). Above phi_c the rigidity grows
  with the EXCESS connectivity above the isostatic (Maxwell) count z_iso = 2d:
        Delta_z = z - z_iso ~ (phi - phi_c)^(1/2)          [O'Hern 2003, universal]
        rigidity (shear modulus G) ~ Delta_z               [Wyart-Nagel-Witten 2005]
  Composing the two CITED universals gives the rigidity that emerges CONTINUOUSLY at the
  transition (vanishing exactly at phi_c):
        rigidity onset ~ (phi - phi_c)^(1/2)

THE RIGIDITY FRACTION J(phi) (the realized fraction of the load-bearing ceiling):
  We carry the dimensionless fraction J(phi) in [0, 1] of the maximum (close-packed) rigidity:
        J(phi) = 0,                                     phi <= phi_c   (unjammed -> Reuss floor)
        J(phi) = sqrt((phi - phi_c) / (1 - phi_c)),     phi >  phi_c
  The SHAPE (square root) is the COMPOSITION of two cited universals above ([L]-grounded, not a
  free choice); the NORMALIZATION (dividing by the value at phi = 1, so J(1) = 1) is a documented
  bounding choice that makes J a fraction of the exact Voigt ceiling. The two EXACT bounds
  (hierarchy.renorm: Reuss floor 0, Voigt ceiling phi*B) are what the gate enforces -- J only
  places the effective modulus continuously between them, and the gate (H1) fails closed if the
  result ever leaves the bracket.

WHY THE BULK MODULUS HAS A FINITE JUMP, AND WHY WE USE THE CONTINUOUS (SHEAR-LIKE) ONSET:
  For harmonic contacts the BULK modulus jumps to a finite value at phi_c (B ~ Delta_phi^0),
  while the SHEAR modulus and the excess coordination vanish continuously (~ Delta_phi^(1/2)).
  "Cells gathering acquire rigidity" is, physically, the CONTINUOUS onset: below jamming there
  is NO rigidity (a fluid), and it turns on at phi_c. So J is built on the continuous (shear /
  coordination) onset -- the quantity that is exactly zero below phi_c. This is stated, not hidden.

Everything here is deterministic, stdlib + numpy only. Constants are inherited from
hierarchy.lock (cited/measured); NOTHING is fitted.
"""
import math
import numpy as np

from . import lock


# ----------------------------------------------------------------------------
# excess coordination above isostaticity
# ----------------------------------------------------------------------------
def excess_coordination(phi):
    """Delta_z(phi) / Delta_z(1)  -- the normalized excess coordination above the isostatic
    count, with the cited onset exponent psi = 1/2. Zero below phi_c. Dimensionless in [0,1]."""
    pc, _, _ = lock.phi_c()
    psi, _, _ = lock.coordination_onset_exponent()
    phi = np.asarray(phi, dtype=np.float64)
    # clamp the base to >=0 BEFORE the fractional power: below phi_c the base
    # (phi-phi_c)/(1-phi_c) is negative and np.where would still evaluate it
    # (raising a negative to ^0.5 -> NaN + warning), even though we select 0.0
    # there. Clamping is mathematically identical (clamped values are only used
    # where phi > phi_c, where the base is already non-negative).
    base = np.maximum((phi - pc) / (1.0 - pc), 0.0)
    excess = np.where(phi > pc, base ** psi, 0.0)
    return excess


def coordination_number(phi):
    """Absolute mean coordination z(phi) at the isostatic anchor plus the (normalized) excess.
    z(phi_c+) = z_iso exactly (marginal); grows above. Reported as a structural read per level.
    NOTE: the prefactor of the excess at phi=1 is packing-dependent; we report z_iso (exact) plus
    the normalized excess fraction, so this is the SHAPE of z(phi), anchored exactly at z_iso."""
    zi, _, _ = lock.z_isostatic()
    return float(zi) + excess_coordination(phi)  # +[0,1] normalized excess above isostatic


# ----------------------------------------------------------------------------
# the rigidity fraction J(phi) in [0,1]
# ----------------------------------------------------------------------------
def rigidity_fraction(phi):
    """J(phi) in [0,1]: the realized fraction of the close-packed (Voigt) rigidity ceiling.
        J = 0                                  for phi <= phi_c   (fluid; Reuss floor)
        J = sqrt((phi-phi_c)/(1-phi_c))        for phi >  phi_c
    Built by composing rigidity ~ Delta_z (Wyart 2005) and Delta_z ~ (phi-phi_c)^(1/2)
    (O'Hern 2003); the sqrt shape is [L]-grounded, the [0,1] normalization is a documented
    bounding choice. ALWAYS in [0,1] -> the effective modulus ALWAYS lies in [Reuss, Voigt]."""
    pc, _, _ = lock.phi_c()
    kappa, _, _ = lock.rigidity_coordination_exponent()   # = 1 (rigidity linear in excess z)
    phi = np.asarray(phi, dtype=np.float64)
    # rigidity ~ Delta_z^kappa with kappa=1 -> J = excess_coordination^kappa, clamped to [0,1]
    J = excess_coordination(phi) ** kappa
    return np.clip(J, 0.0, 1.0)


def is_jammed(phi):
    """True iff the packing is at or above the jamming onset (has non-zero rigidity)."""
    pc, _, _ = lock.phi_c()
    return bool(np.asarray(phi) > pc)


# ----------------------------------------------------------------------------
# a readable jamming-state report for one packing fraction
# ----------------------------------------------------------------------------
def jamming_state(phi):
    """The full jamming read of one packing fraction: threshold, isostatic anchor, excess
    coordination, rigidity fraction, jammed/fluid verdict. All from cited universals."""
    pc, gpc, _ = lock.phi_c()
    zi, gzi, _ = lock.z_isostatic()
    psi, _, _ = lock.coordination_onset_exponent()
    return {
        "phi": float(phi),
        "phi_c": pc,
        "phi_c_grade": gpc,
        "z_isostatic": zi,
        "coordination_onset_exponent": psi,
        "excess_coordination_frac": round(float(excess_coordination(phi)), 8),
        "coordination_number_anchored": round(float(coordination_number(phi)), 6),
        "rigidity_fraction_J": round(float(rigidity_fraction(phi)), 8),
        "state": "jammed (rigid)" if is_jammed(phi) else "unjammed (fluid; zero rigidity)",
        "grade": "[L]-grounded onset (O'Hern 2003 + Wyart 2005); J normalization [F]; "
                 "absolute modulus [O]",
    }
