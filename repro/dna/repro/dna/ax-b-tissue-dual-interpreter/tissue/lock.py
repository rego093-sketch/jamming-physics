# -*- coding: utf-8 -*-
"""
tissue.lock -- the LOCKED constant surface for the tissue-level dual interpreter.

DISCIPLINE (no compromise):
  * EVERY physical constant is read from the package's locked param_db.json
    (the SAME file the morphogenesis engine reads). There is NOT ONE inline
    magic number in this whole module set. The roughness we are removing
    INCLUDED `dwell(g, K=0.6, brake=0.5)` -- two constants that lived inline in
    emergence_engine.py / emergence_organs.py and appeared in NO database. Here,
    any constant that is a modelling choice is named, graded, and sourced -- never
    buried in a default argument.
  * Grades carried verbatim from the DB:
        [L] locked: independently measured / universal law, cited
        [F] fixed modelling choice (functional form / generic central value)
        [O] open: the entity-specific measured value does not exist here
  * This module READS the DB; it never writes it. Changing any value defines a
    new version (mirrors key_pipeline_full.LOCK at the cell level).

WHAT THE TISSUE FIELD IS (the one field we project twice):
  the morphogen concentration c(x) on a tissue domain, obeying the linear,
  steady-state SCREENED-POISSON equation
        D * laplacian(c)  -  c / tau  +  source  =  0
  whose intrinsic length is  lambda = sqrt(D * tau)  -- set ENTIRELY by two
  measured constants. This is the tissue-level analogue of the cell-level
  stiffness signal s(x) = w_gc*GC + w_cpg*CpG + w_at*AT6.
"""
import os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_DB_CANDIDATES = [
    os.path.join(_HERE, "..", "param_db.json"),
    os.path.join(_HERE, "..", "..", "ax-a-universal-morphogenesis-gene-clock",
                 "code", "emergence_v2", "param_db.json"),
]


def _load_db():
    for p in _DB_CANDIDATES:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                return json.load(fh), os.path.relpath(p, _HERE)
    raise FileNotFoundError(
        "param_db.json not found. The tissue interpreter refuses to invent "
        "constants; place the locked DB next to it (no compromise)."
    )


DB, DB_PATH = _load_db()


def _entry(*path):
    """Fetch a DB entry by key path and return (value, grade, provenance)."""
    node = DB
    for k in path:
        node = node[k]
    return node["value"], node.get("grade", "[?]"), node.get("provenance", "")


# ----------------------------------------------------------------------------
# the LOCKED tissue constants -- every one sourced, none inline
# ----------------------------------------------------------------------------
def diffusion_um2_per_s():
    """Morphogen effective diffusion D. [L] measured (Kicheva 2007)."""
    return _entry("morphogen", "diffusion_um2_per_s")


def morphogen_decay_min():
    """Morphogen clearance time. [L] measured (Kicheva 2007)."""
    return _entry("morphogen", "morphogen_decay_min")


def territory_theta():
    """Positional-information threshold theta (French-flag). [F] modelling choice;
    the interpreter is required to be theta-robust over [0.3, 0.7]."""
    return _entry("kinetics", "relay_threshold_theta")


def growth_alpha():
    """Universal developmental supply exponent alpha (extent ~ devtime^alpha).
    [F] single universal rule applied identically to all -- never per-target."""
    return _entry("allometry", "growth_supply_exponent_alpha")


def diffusion_range_um2_per_s():
    """The DB's own measured D-range -- used ONLY for a grounded consistency band
    (bracketing real morphogen gradients), never to fit anything."""
    return DB["morphogen"]["diffusion_um2_per_s"]["range"]


# ----------------------------------------------------------------------------
# derived locked length scale -- the ONE number both projections inherit
# ----------------------------------------------------------------------------
import math


def lambda_um():
    """Intrinsic morphogen length lambda = sqrt(D * tau), from MEASURED D, tau ONLY.
    Grade is [L]-grounded: it is a composition of two locked measured constants,
    with NO modelling choice. This is the tissue-level invariant -- the analogue of
    the cell-level locked NN dG table that fixes gamma."""
    D, _, _ = diffusion_um2_per_s()
    decay_min, _, _ = morphogen_decay_min()
    tau_s = decay_min * 60.0           # min -> s : a UNIT conversion, not a choice
    return math.sqrt(D * tau_s)


def lambda_band_um():
    """Length band implied by the DB's measured D-range (grounded sanity bracket)."""
    lo, hi = diffusion_range_um2_per_s()
    decay_min, _, _ = morphogen_decay_min()
    tau_s = decay_min * 60.0
    return math.sqrt(lo * tau_s), math.sqrt(hi * tau_s)


def lock_manifest():
    """A flat, auditable dump of every constant this interpreter stands on,
    with its grade and provenance. Printed in the gate so a hostile reviewer can
    confirm no constant is unsourced."""
    D, gD, pD = diffusion_um2_per_s()
    dec, gdec, pdec = morphogen_decay_min()
    th, gth, pth = territory_theta()
    al, gal, pal = growth_alpha()
    return {
        "db_path": DB_PATH,
        "constants": {
            "diffusion_D_um2_per_s": {"value": D, "grade": gD, "provenance": pD},
            "morphogen_decay_min": {"value": dec, "grade": gdec, "provenance": pdec},
            "territory_theta": {"value": th, "grade": gth, "provenance": pth},
            "growth_alpha": {"value": al, "grade": gal, "provenance": pal},
        },
        "derived": {
            "lambda_um": {"value": round(lambda_um(), 10),
                          "grade": "[L]-grounded",
                          "provenance": "lambda = sqrt(D*tau); composed of two "
                                        "measured locked constants, no fit"},
        },
        "inline_magic_numbers": 0,   # asserted by tissue.gate
    }
