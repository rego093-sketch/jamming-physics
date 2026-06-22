#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_substrate.py  --  shared loader for the inheritance kit.

Imports the VENDORED substrate primitive (inherited/vp_substrate.py: the R19 jamming switch
ds/dt = g*s - s^3 + h, spinodal(g)=2(g/3)^1.5, barrier(g)=g^2/4) and exposes the three MEASURED
gamma atlases (germline, immune, RNA-carrier) read-only. Nothing here re-derives the math or the
gamma -- single source, measured input. Grades: [F] forced / [V] simulation-verified / [O] open / [L] calibration.
"""
import os, sys, json
import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
_INH  = os.path.join(_HERE, "..", "inherited")
sys.path.insert(0, _INH)
import vp_substrate as S  # vendored: sdot, spinodal, barrier, settle, is_on, dwell, Organ, Neuron
import vp_a4 as A4        # vendored: A4 coordinate/structure channel (run_key, locate_in_A4, helix_coord, material reads)

SEED = S.SEED  # 19 -- the inherited substrate seed

def _load(name):
    return json.load(open(os.path.join(_INH, name), encoding="utf-8"))

def germline_gamma():
    d = _load("germline_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def immune_gamma():
    d = _load("immune_gamma.json")
    g = d.get("genes", d)
    return {k: v["gamma"] for k, v in g.items() if isinstance(v, dict) and "gamma" in v}

def rna_gamma():
    d = _load("rna_carrier_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def rna_roles():
    d = _load("rna_carrier_gamma.json")["genes"]
    return {k: v["role"] for k, v in d.items()}

def neuro_gamma():
    """MEASURED neurodevelopmental / autism-spectrum master-gene gamma (v0.7.0, anchor-gated)."""
    d = _load("neuro_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def neuro_roles():
    d = _load("neuro_gamma.json")["genes"]
    return {k: v["role"] for k, v in d.items()}

def onco_gamma():
    """MEASURED cancer-driver master-gene gamma (v0.8.0, anchor-gated). Suppressors + oncogenes."""
    d = _load("onco_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def onco_meta():
    d = _load("onco_gamma.json")["genes"]
    return {k: {"gamma": v["gamma"], "role": v["role"], "mechanism": v["mechanism"],
                "corr_sign": v["corr_sign"], "therapy": v.get("therapy", ""), "note": v.get("note", "")}
            for k, v in d.items()}

def neurodegen_gamma():
    """MEASURED Parkinson's/neurodegeneration master-gene gamma (v0.8.0, anchor-gated)."""
    d = _load("neurodegen_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def neurodegen_meta():
    d = _load("neurodegen_gamma.json")["genes"]
    return {k: {"gamma": v["gamma"], "role": v["role"], "mechanism": v["mechanism"],
                "corr_sign": v["corr_sign"], "therapy": v.get("therapy", ""), "note": v.get("note", "")}
            for k, v in d.items()}

def disease_meta():
    """Merged disease master-gene meta across classes: oncology + neurodegeneration.
    Each gene carries gamma, role, mechanism (GOF/LOF), corr_sign (+/-), therapy, note, and class."""
    out = {}
    for cls, fn in (("oncology", onco_meta), ("neurodegeneration", neurodegen_meta)):
        for k, v in fn().items():
            vv = dict(v); vv["disease_class"] = cls
            out[k] = vv
    return out

def imprint_gamma():
    d = _load("imprint_gamma.json")["genes"]
    return {k: v["gamma"] for k, v in d.items()}

def imprint_meta():
    d = _load("imprint_gamma.json")["genes"]
    return {k: {"gamma": v["gamma"], "parent_of_origin": v.get("parent_of_origin", "complex"),
               "role": v.get("role", "")} for k, v in d.items()}

def a4_coords():
    """A4 coordinate reads (structure channel) for the RNA carriers, measured from wide NCBI windows."""
    d = _load("a4_coordinates.json")["genes"]
    return {k: v for k, v in d.items() if "gamma_canonical" in v}  # carriers (drop the SOX9 reference)

def a4_coords_set(name):
    """A4 coordinate reads for a named gene set: 'imprint' | 'germline' | 'immune' (carriers via a4_coords)."""
    d = _load("a4_%s_coordinates.json" % name)["genes"]
    return {k: v for k, v in d.items() if "gamma_canonical" in v}

def a4_read(seq, offset=None):
    """Read the A4 coordinate of an element at `offset` within `seq` via the vendored A4 engine.
    If offset is None, place it at the window centre."""
    A = A4.run_key(seq)
    off = (len(seq) // 2) if offset is None else offset
    return A4.locate_in_A4(A, off)

# convenience re-exports
sdot     = S.sdot
spinodal = S.spinodal
barrier  = S.barrier
settle   = S.settle
is_on    = S.is_on
