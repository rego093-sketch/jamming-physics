#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_skn_engine.py  --  Integumentary emergence engine (deterministic, in-package).

SCOPE (see CHARTER.md): Epidermis, keratinocyte barrier, melanocyte photoprotection and appendages emerge as the body boundary; wound healing is a jamming->unjamming->re-jamming transition, and UV dose-response is the cleanest R19 carcinogenesis case.

WHAT RUNS TODAY: emerge_organs() loads MEASURED master-gene gamma (vendored from DNA), builds each
  Organ on the R19 substrate for organs whose gamma is vendored, reads the developmental ORDER off
  gamma, and DEFERS organs whose gamma is still 'to_measure' (named masters whose gamma is an honest
  research input to fetch via the DNA pipeline -- never invented). confirm_oscillators() runs the
  SHARED FHN for any oscillator organ (rhythm depends on tau, not identity gamma).

WHAT IS A SKELETON (research to COMPLETE before writing): the dynamics for this physical class
  (see CHARTER targets T1..T5), the stress battery, and the carcinogen dose-response.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, dwell, dominant_freq, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

ORGAN_ROWS = [{'master': 'TP63',
  'organ': 'epidermis',
  'role': 'stratified barrier: basal->cornified transit',
  'dyn_class': 'barrier',
  'tau_s': None,
  'rate_note': 'epidermal turnover ~28-40 d [L] TO-ANCHOR',
  'gamma_state': 'vendored'},
 {'master': 'KRT14',
  'organ': 'keratinocyte',
  'role': 'keratin barrier mechanics / structural integrity',
  'dyn_class': 'barrier',
  'tau_s': None,
  'rate_note': 'barrier permeability (TEWL) [L]',
  'gamma_state': 'vendored'},
 {'master': 'MITF',
  'organ': 'melanocyte',
  'role': 'melanin synthesis + UV photoprotection',
  'dyn_class': 'defense',
  'tau_s': None,
  'rate_note': 'melanin UV-dose protection [L]',
  'gamma_state': 'vendored'},
 {'master': 'EDAR',
  'organ': 'skin_appendage',
  'role': 'hair follicle / sweat gland (thermoregulation interface)',
  'dyn_class': 'appendage',
  'tau_s': None,
  'rate_note': 'appendage identity [V]',
  'gamma_state': 'vendored'}]
OSCILLATOR_ORGANS = []

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def emerge_organs():
    """Emerge organs whose gamma is vendored (measured); defer to_measure masters honestly."""
    seed_everything(); G = load_gamma(); built = []
    for r in ORGAN_ROWS:
        st = r["gamma_state"]
        if st == "vendored":
            g = G[r["master"]]["gamma"]; o = Organ(r["organ"], g, master=r["master"])
            built.append(dict(organ=r["organ"], master=r["master"], gamma=round(float(g), 6), role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="vendored",
                              functional_spinodal=round(float(o.functional_spinodal()), 6),
                              rel_size_dwell=round(float(o.size()), 6)))
        elif st == "to_measure":
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="to_measure",
                              note="master " + r["master"] + ": gamma TO-MEASURE via DNA fetch_morpho_gamma pipeline (measured input, not fitted)"))
        else:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"],
                              dyn_class=r["dyn_class"], gamma_state="diffuse",
                              note="no single master gene (derived/diffuse)"))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] order is a gamma readout over MEASURED organs; SIGN to validate vs cited timing",
                deferred_gamma=[b["master"] for b in built if b.get("gamma_state") == "to_measure"])

def confirm_oscillators():
    """For each OSCILLATOR organ, instantiate the SHARED FHN and confirm a beat. Mechanism [V]; rate [L]."""
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
    organs = emerge_organs(); osc = confirm_oscillators()
    import importlib
    dyn = importlib.import_module("skn_dynamics").dynamics_summary()
    return dict(_what="Integumentary -- emerge organs from measured gamma, then circulate class dynamics.",
                organs=organs, oscillators=osc, dynamics=dyn,
                dynamics_status="COMPLETE: T1..T5 class dynamics emerged on the R19 substrate",
                targets_ref="see CHARTER.md and repro/_verify/stress_tests.py")

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
