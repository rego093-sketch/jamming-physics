#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergence_organs.py -- Phase 2: 8 visceral organs + the ALLOMETRIC GROWTH LAW.

Reads ONLY param_db.json (measured gamma + cited allometric exponents); NEVER
the validation targets (measured organ fractions) -- that file is touched only
by validate_organs.py.

Two SEPARATE, honestly-scoped parts:

  PART A  gamma-emergence over the 8 MEASURED organ masters (organ_gamma.json):
            ORDER = argsort(spinodal(gamma))            [V]  intrinsic gamma readout
            rel. dwell = gamma^1.5/(K+brake)            [F]  relative size only
          (gamma is measured; brain is NOT in this set -- no gamma is invented.)

  PART B  allometric GROWTH LAW over organs with a CITED exponent b:
            organ mass-fraction scales with body mass as  f ~ M_body^(b-1)
            b<1 => fraction FALLS as the body grows (negative allometry)
            b~1 => near-isometric                        [L]  cited, gamma-free
          The prediction is the SIGN+MAGNITUDE of (b-1) per organ -- coefficient-
          free, so no per-organ coefficient is ever chosen by us. (brain enters
          here via its exponent only.)
"""
import os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DB = json.load(open(os.path.join(HERE, "param_db.json"), encoding="utf-8"))

# PART A: measured organ-master gamma (read-only [L]; package organ_gamma.json)
ORGAN_GAMMA = {  # organ : (master gene, measured gamma)
    "heart":   ("NKX2-5", 1.513),
    "liver":   ("HHEX",   1.525),
    "stomach": ("BARX1",  1.5609),
    "lung":    ("NKX2-1", 1.5088),
    "pancreas":("PDX1",   1.4732),
    "kidney":  ("SIX2",   1.5556),
    "spleen":  ("TLX1",   1.4228),
    "midgut":  ("CDX2",   1.45),
}
GAMMA_ORGANS = list(ORGAN_GAMMA.keys())

def spinodal(g): return 2.0*(g/3.0)**1.5
def dwell(g, K=0.6, brake=0.5): return (g**1.5)/(K+brake)

# PART B: cited allometric exponents (param_db [L]); the organs that carry one
def allo_table():
    t = dict(DB["allometry"]["organ_scaling_exponent_reference"])
    t.pop("_grade", None); t.pop("_provenance", None)
    return t
ALLO_ORGANS = list(allo_table().keys())

def emerge_gamma():
    feats = {}
    for o in GAMMA_ORGANS:
        gene, g = ORGAN_GAMMA[o]
        feats[o] = dict(gene=gene, gamma=g, spinodal=round(spinodal(g),6),
                        rel_dwell=round(dwell(g),4))
    order = sorted(GAMMA_ORGANS, key=lambda o: spinodal(ORGAN_GAMMA[o][1]))
    for i,o in enumerate(order): feats[o]["order_rank"]=i+1
    return feats

def allometric_law():
    out = {}
    for o, b in allo_table().items():
        out[o] = dict(allo_b=b, frac_scaling_exponent=round(b-1.0,4),
                      direction=("falls" if b<1 else ("isometric" if abs(b-1)<0.02 else "rises")))
    return out

def predicted_fraction_ratio(organ, body_mass_ratio):
    """f_adult/f_neonate predicted = body_mass_ratio^(b-1). body_mass_ratio is a GENERAL
    anthropometric span (neonate->adult), not an organ-specific target."""
    b = allo_table().get(organ)
    return None if b is None else body_mass_ratio**(b-1.0)

def result_hash():
    blob = json.dumps({"a":emerge_gamma(),"b":allometric_law()}, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:12]

if __name__ == "__main__":
    A = emerge_gamma(); B = allometric_law()
    print("="*86)
    print("  ORGAN EMERGENCE (Part A: gamma) + ALLOMETRIC GROWTH LAW (Part B: cited b)")
    print("="*86)
    print("  PART A -- gamma-emergence (8 measured organ masters):")
    print(f"  {'organ':9s} {'gene':8s} {'rank':>4s} {'gamma':>7s} {'rel_dwell':>9s}")
    for o in sorted(GAMMA_ORGANS, key=lambda o: A[o]['order_rank']):
        f=A[o]; print(f"  {o:9s} {f['gene']:8s} {f['order_rank']:>4d} {f['gamma']:>7.3f} {f['rel_dwell']:>9.3f}")
    print("    -> ORDER=[V] (gamma readout) ; rel_dwell=[F]")
    print("\n  PART B -- allometric growth law (f ~ M_body^(b-1), cited b [L]):")
    print(f"  {'organ':9s} {'allo_b':>7s} {'f~M^(b-1)':>10s}  direction")
    for o in sorted(B, key=lambda o: B[o]['allo_b']):
        f=B[o]; print(f"  {o:9s} {f['allo_b']:>7.2f} {f['frac_scaling_exponent']:>10.3f}  {f['direction']}")
    print("    -> PREDICTION: b<1 organs lose body-fraction as body grows; brain (lowest b) most.")
    print(f"\n  determinism: sha={result_hash()}")
    print("="*86)
