#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergence_morphogen_validation.py -- Phase 7: the morphogen LENGTH-SCALE band,
derived from first principles from the locked generic biophysics.

ADD-ONLY extension of the Phase-3 reduced-order reaction-diffusion layer
(emergence_trajectory.py). Phase 3 established the intrinsic length
lambda = sqrt(D*tau) and recovered it from the solved 3-D field to <1%; the
Phase-3 LEDGER asserted, QUALITATIVELY, that the DB's D-range maps to
lambda in [19,190] um, "bracketing real morphogen gradients (Bicoid/FGF/Nodal/Shh)".
This module turns that qualitative aside into a quantitative, gated object: it emits
the model's first-principles lambda BAND and CENTRAL value, computed PURELY from
param_db.json (the same locked D-range and clearance tau the trajectory engine uses).

Reads ONLY:
    param_db.json   -- morphogen.diffusion_um2_per_s (value + range) and
                       morphogen.morphogen_decay_min                         [L]
NEVER reads any validation-target / measured-gradient file (NON-FIT, asserted by
the Phase-7 gate via source scan + output-invariance). The band is a pure function
of two measured biophysical constants; it does not know that any real morphogen
exists. The gate (verify_emergence_morphogen.py) supplies the independently-measured
gradient lengths POST HOC and tests whether this band brackets them.

This is the screened-Poisson positional-information length (Wolpert / French-flag):
for a steady linear gradient D*nabla^2 c - c/tau + source = 0, the intrinsic decay
length is lambda = sqrt(D*tau). No length here is fitted to any anatomy or to any
measured morphogen; lambda is a derived consequence of D and tau alone.
"""
import os, json, math, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = json.load(open(os.path.join(HERE, "param_db.json"), encoding="utf-8"))


def _morphogen_constants():
    """The two locked biophysical constants the band is built from."""
    m = DB["morphogen"]
    D_val = m["diffusion_um2_per_s"]["value"]          # central effective diffusion (um^2/s)
    D_lo, D_hi = m["diffusion_um2_per_s"]["range"]      # cited measured range (um^2/s)
    tau_min = m["morphogen_decay_min"]["value"]         # clearance timescale (min)
    return D_val, D_lo, D_hi, tau_min


def length_scale_um(D_um2_per_s, tau_min):
    """Intrinsic screened-Poisson length lambda = sqrt(D*tau), in um.
    tau is converted from minutes to seconds so D[um^2/s]*tau[s] -> um^2."""
    tau_s = tau_min * 60.0
    return math.sqrt(D_um2_per_s * tau_s)


def model_band():
    """The model's first-principles lambda band + central value, from param_db only.
    Returns a dict with lambda_min_um, lambda_central_um, lambda_max_um and the
    constants they derive from. Target-independent by construction."""
    D_val, D_lo, D_hi, tau_min = _morphogen_constants()
    return {
        "D_central_um2_per_s": D_val,
        "D_range_um2_per_s": [D_lo, D_hi],
        "tau_min": tau_min,
        "tau_s": tau_min * 60.0,
        "lambda_central_um": length_scale_um(D_val, tau_min),
        "lambda_min_um": length_scale_um(D_lo, tau_min),
        "lambda_max_um": length_scale_um(D_hi, tau_min),
        "law": "lambda = sqrt(D*tau)  (screened-Poisson positional-information length)",
    }


def contains(lambda_um, band=None, tol_rel=0.0):
    """True iff lambda_um lies within [lambda_min, lambda_max]. tol_rel optionally
    widens the band by a relative fraction on each edge (used only to flag
    boundary-adjacent values; the headline membership uses tol_rel=0)."""
    b = band or model_band()
    lo = b["lambda_min_um"] * (1.0 - tol_rel)
    hi = b["lambda_max_um"] * (1.0 + tol_rel)
    return lo <= lambda_um <= hi


def result_hash():
    """Deterministic 12-hex fingerprint of the model band (a pure function of the
    two locked constants). Changes iff D, tau, or the law change -- i.e. iff the
    measured biophysics or the physics changes. Independent of any real morphogen."""
    b = model_band()
    blob = json.dumps({k: (round(v, 9) if isinstance(v, float) else v)
                       for k, v in b.items()}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:12]


if __name__ == "__main__":
    b = model_band()
    print("=" * 86)
    print("  MORPHOGEN LENGTH-SCALE BAND (lambda = sqrt(D*tau), from locked biophysics [L])")
    print("=" * 86)
    print(f"  measured constants (param_db.json):")
    print(f"    D (effective diffusion)  central {b['D_central_um2_per_s']} um^2/s   "
          f"range {b['D_range_um2_per_s']} um^2/s")
    print(f"    tau (clearance)          {b['tau_min']} min = {b['tau_s']:.0f} s")
    print(f"\n  derived intrinsic length lambda = sqrt(D*tau):")
    print(f"    lambda_central = {b['lambda_central_um']:.2f} um   (from D={b['D_central_um2_per_s']})")
    print(f"    lambda_min     = {b['lambda_min_um']:.2f} um   (from D={b['D_range_um2_per_s'][0]})")
    print(f"    lambda_max     = {b['lambda_max_um']:.2f} um   (from D={b['D_range_um2_per_s'][1]})")
    print(f"\n  -> first-principles BAND lambda in [{b['lambda_min_um']:.2f}, {b['lambda_max_um']:.2f}] um")
    print(f"     no length fitted to any anatomy or to any real morphogen (NON-FIT).")
    print(f"\n  determinism: sha={result_hash()}")
    print("=" * 86)
