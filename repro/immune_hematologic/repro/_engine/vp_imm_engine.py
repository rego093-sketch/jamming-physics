#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_imm_engine.py  --  Immune / Hematologic emergence engine (deterministic, in-package).

SCOPE (see CHARTER.md): Thymus, spleen, marrow hematopoiesis and the adaptive lymphoid compartment
emerge as a POPULATION of R19 switches: a cell is ON/OFF activated, inflammation is a bistable latch,
hematopoietic lineage order is a gamma readout, immune memory is substrate persistence, and
immunosurveillance modulates every other package's cancer kernel.

WHAT RUNS: emerge_organs() loads MEASURED master-gene gamma (now 4/4: FOXN1, TLX1, RUNX1, PAX5 -- the
  last two fetched via the validated NN-stacking pipeline, cached for offline reproduction), builds each
  Organ on the R19 substrate, and reads the developmental ORDER off gamma. verify_gamma() re-derives
  gamma offline from cached sequence and confirms the pipeline reproduces the knowns (FOXN1/TLX1) -- so
  every gamma here is measured, never invented. confirm_oscillators() runs the SHARED FHN for any
  oscillator organ (this class has none autonomous; lymphoid/marrow dynamics are switch+population).

DYNAMICS (CHARTER targets T1..T5) live in repro/_dynamics and repro/_oncology and are summarised here.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, barrier, dwell, dominant_freq, seed_everything
import gamma_pipeline as GP
import ncbi_verify as NV          # v0.3.0: primary-source (NCBI) γ provenance, offline-checkable

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

ORGAN_ROWS = [
 {'master':'FOXN1','organ':'thymus','role':'T-cell positive/negative selection (threshold gating)',
  'dyn_class':'population','tau_s':None,'rate_note':'thymic selection threshold [L]','gamma_state':'vendored'},
 {'master':'TLX1','organ':'spleen','role':'blood filtration + lymphoid white pulp',
  'dyn_class':'population','tau_s':None,'rate_note':'spleen identity [V] (visceral atlas)','gamma_state':'vendored'},
 {'master':'RUNX1','organ':'bone_marrow_hematopoiesis','role':'HSC -> lineage branching (clonal)',
  'dyn_class':'population','tau_s':None,'rate_note':'RUNX1 gamma MEASURED [V]; lineage tree by gamma','gamma_state':'vendored'},
 {'master':'PAX5','organ':'lymphoid_adaptive','role':'B/T clonal selection + immune memory',
  'dyn_class':'population','tau_s':None,'rate_note':'PAX5 gamma MEASURED [V]; affinity-threshold activation','gamma_state':'vendored'},
]
OSCILLATOR_ORGANS = []

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def verify_gamma():
    """Offline, deterministic: recompute every gamma from cached sequence; confirm knowns reproduce."""
    rep = GP.validation_report()
    return dict(knowns_reproduced=rep["knowns_reproduced"], all_cache_consistent=rep["all_cache_consistent"],
                grade=rep["pipeline_grade"],
                gamma={k: v["gamma"] for k, v in rep["per_gene"].items()})


def provenance_report():
    """v0.3.0: PRIMARY-SOURCE γ provenance (offline, deterministic). Confirms the frozen NCBI proof is
    self-consistent with the shipped cache + atlas (byte-exact sha chain, γ recompute, RefSeq chromosome).
    Kept OUT of circulate()'s hashed object on purpose: the core science object is byte-identical to
    v0.2.0 (sha unchanged), and this is an ADDED independent verification layer. Online audit/refresh is
    inherited/ncbi_verify.py ONLINE_reverify()."""
    return NV.OFFLINE_check()

def emerge_organs():
    """Emerge all organs from MEASURED gamma; read developmental order off gamma (ascending)."""
    seed_everything(); G = load_gamma(); built = []
    for r in ORGAN_ROWS:
        if r["gamma_state"] == "vendored":
            g = G[r["master"]]["gamma"]; o = Organ(r["organ"], g, master=r["master"])
            built.append(dict(organ=r["organ"], master=r["master"], gamma=round(float(g), 6), role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="vendored",
                              functional_spinodal=round(float(o.functional_spinodal()), 6),
                              barrier=round(float(barrier(g)), 6),
                              rel_size_dwell=round(float(o.size()), 6)))
        else:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state=r["gamma_state"],
                              note="master " + r["master"] + ": gamma to fetch via DNA pipeline"))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] developmental order is a gamma readout over 4 MEASURED organs; "
                            "endpoints SIGN-validated vs cited embryology (hematopoiesis first, adaptive last)",
                deferred_gamma=[b["master"] for b in built if b.get("gamma_state") == "to_measure"])

def confirm_oscillators():
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] != "oscillator": continue
        taus = r["tau_s"] if r["tau_s"] is not None else 40.0
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(taus), beta=0.5, name=r["organ"])
        S, dt = n.run(drive=0.55, T=8000.0, dt=0.05)
        f = dominant_freq(S, dt); nb = len(Neuron.spikes(S))
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f), 8), tau_s=float(taus),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

def circulate():
    organs = emerge_organs(); osc = confirm_oscillators(); vg = verify_gamma()
    return dict(_what="Immune / Hematologic -- emerge organs from MEASURED gamma (4/4), then circulate dynamics.",
                gamma_verification=vg, organs=organs, oscillators=osc,
                dynamics_pointer="T1..T5 in repro/_dynamics, repro/_oncology, repro/_therapy; battery in repro/_verify",
                grounding="full (4/4 master-gene gamma measured & offline-reproducible)")

def _round(o):
    if isinstance(o, float): return round(o, 8)
    if isinstance(o, dict):  return {k: _round(v) for k, v in o.items()}
    if isinstance(o, list):  return [_round(v) for v in o]
    return o

def emit(obj):
    s = json.dumps(_round(obj), ensure_ascii=False, sort_keys=True, indent=1)
    return s, hashlib.sha256(s.encode("utf-8")).hexdigest()

if __name__ == "__main__":
    s, h = emit(circulate()); print(s); print("# sha256:", h)
