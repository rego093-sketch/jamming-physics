# -*- coding: utf-8 -*-
"""
hierarchy.lock -- the LOCKED constant surface for the hierarchical scale-renormalization interpreter.

DISCIPLINE (no compromise), inherited verbatim from the cell-level (key_pipeline_full.LOCK)
and tissue-level (tissue.lock) modules:

  * EVERY physical constant is read from this package's locked param_db.json. There is NOT
    ONE inline magic number in this whole module set. The roughness Appendix B removed
    INCLUDED `dwell(g, K=0.6, brake=0.5)` -- two constants that lived inline and appeared in
    NO database. Here, any constant that is a modelling choice is named, graded, and sourced.
  * Grades carried verbatim from the DB:
        [L] locked: independently measured / universal law / exact theorem, cited
        [V] verified: an exact closed form/theorem evaluated to machine precision
        [F] fixed modelling choice (functional form / generic central value)
        [O] open: the entity-specific MEASURED value does not exist here
  * This module READS the DB; it never writes it. Changing any value defines a new version.

WHAT THE HIERARCHY OPERATES ON (the one quantity it flows up the ladder):
  a structural level carries an effective bulk modulus B (stiffness) and a mean density rho
  (volume/mass). When the units of one level PACK at fraction phi, the aggregate acquires its
  OWN B and rho -- "cells gather and become, by that act, both volume and stiffness." The VP
  master relation c^2 = B/rho holds at EVERY level; the renormalization is the map that takes
  (B, rho) of the units to (B, rho) of the aggregate. This is the SAME jamming physics the VP
  core thesis applies to the vacuum (vacuum as a jammed elastic solid, c^2 = B/rho), applied
  one structural level up.
"""
import os
import json
import math

_HERE = os.path.dirname(os.path.abspath(__file__))
_DB_PATH = os.path.join(_HERE, "..", "param_db.json")


def _load_db():
    if not os.path.exists(_DB_PATH):
        raise FileNotFoundError(
            "param_db.json not found. The hierarchy interpreter refuses to invent "
            "constants; place the locked DB next to it (no compromise)."
        )
    with open(_DB_PATH, encoding="utf-8") as fh:
        return json.load(fh), os.path.relpath(_DB_PATH, _HERE)


DB, DB_PATH = _load_db()


def _entry(*path):
    """Fetch a DB entry by key path -> (value, grade, provenance)."""
    node = DB
    for k in path:
        node = node[k]
    return node["value"], node.get("grade", "[?]"), node.get("provenance", "")


# ----------------------------------------------------------------------------
# JAMMING constants -- the rigidity-emergence physics ("cells gather -> stiffness")
# ----------------------------------------------------------------------------
def phi_c():
    """Onset-of-jamming packing fraction phi_c (3D frictionless ~0.639 = RCP).
    [L] cited (O'Hern et al. 2003). Friction/polydispersity shift it -> absolute [O]."""
    return _entry("jamming", "phi_c_3d_frictionless")


def dimension_d():
    """Spatial dimension d = 3. [L]."""
    return _entry("jamming", "spatial_dimension_d")


def z_isostatic():
    """Maxwell isostatic coordination z_iso = 2d = 6 (3D). [L] exact counting."""
    return _entry("jamming", "z_isostatic_3d")


def coordination_onset_exponent():
    """Excess coordination exponent: Delta_z ~ (phi-phi_c)^psi, psi = 1/2. [L] (O'Hern 2003)."""
    return _entry("jamming", "coordination_onset_exponent")


def rigidity_coordination_exponent():
    """Rigidity-to-coordination linearity: shear modulus G ~ Delta_z^1. [L] (Wyart 2005)."""
    return _entry("jamming", "rigidity_coordination_linearity")


# ----------------------------------------------------------------------------
# HIERARCHY ladder -- characteristic length scales of the structural levels
# ----------------------------------------------------------------------------
def ladder_rungs():
    """The biological ladder: list of {level, name, length_um, grade, provenance}.
    [F] generic central values, used ONLY to count units-per-rung (volume ratio)."""
    return DB["hierarchy_scales"]["rungs"]


# ----------------------------------------------------------------------------
# UNIT mechanics -- the [O] absolute anchor (single base unit B, rho)
# ----------------------------------------------------------------------------
def unit_bulk_modulus_pa():
    """Single base-unit (cell) bulk modulus, generic placeholder. [O] -- per-cell-type
    MEASURED modulus is the named obstacle; sets ABSOLUTE magnitude only."""
    return _entry("unit_mechanics", "single_cell_bulk_modulus_pa")


def unit_density_kg_per_m3():
    """Single base-unit (cell) mass density. [L] generic central; the dimensionless
    softening ratio does NOT depend on it."""
    return _entry("unit_mechanics", "single_cell_density_kg_per_m3")


# ----------------------------------------------------------------------------
# derived: isostatic anchor for the wave-speed at the base of the ladder
# ----------------------------------------------------------------------------
def unit_wave_speed_m_per_s():
    """Base-level VP wave speed c0 = sqrt(B0/rho0) (the master relation at the unit scale).
    Grade follows its inputs: [O] in absolute magnitude (B0 is [O]); the FORM is exact."""
    B0, _, _ = unit_bulk_modulus_pa()
    rho0, _, _ = unit_density_kg_per_m3()
    return math.sqrt(B0 / rho0)


def lock_manifest():
    """A flat, auditable dump of every constant this interpreter stands on, with grade and
    provenance. Printed in the gate so a hostile reviewer can confirm no constant is unsourced."""
    pc, gpc, ppc = phi_c()
    d, gd, pd = dimension_d()
    zi, gzi, pzi = z_isostatic()
    psi, gpsi, ppsi = coordination_onset_exponent()
    kappa, gk, pk = rigidity_coordination_exponent()
    B0, gB0, pB0 = unit_bulk_modulus_pa()
    rho0, grho, prho = unit_density_kg_per_m3()
    return {
        "db_path": DB_PATH,
        "constants": {
            "phi_c": {"value": pc, "grade": gpc, "provenance": ppc},
            "dimension_d": {"value": d, "grade": gd, "provenance": pd},
            "z_isostatic": {"value": zi, "grade": gzi, "provenance": pzi},
            "coordination_onset_exponent": {"value": psi, "grade": gpsi, "provenance": ppsi},
            "rigidity_coordination_exponent": {"value": kappa, "grade": gk, "provenance": pk},
            "unit_bulk_modulus_pa": {"value": B0, "grade": gB0, "provenance": pB0},
            "unit_density_kg_per_m3": {"value": rho0, "grade": grho, "provenance": prho},
        },
        "derived": {
            "z_iso_equals_2d": {"value": (zi == 2 * d), "grade": "[L]",
                                "provenance": "isostatic identity z_iso = 2d checked against the DB"},
            "unit_wave_speed_m_per_s": {"value": round(unit_wave_speed_m_per_s(), 6),
                                        "grade": "[O]-absolute / [V]-form",
                                        "provenance": "c0 = sqrt(B0/rho0); FORM exact (VP master), "
                                                      "absolute [O] because B0 is [O]"},
        },
        "ladder_rungs": ladder_rungs(),
        "inline_magic_numbers": 0,   # asserted by hierarchy.gate
    }
