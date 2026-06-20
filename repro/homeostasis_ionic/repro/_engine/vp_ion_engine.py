#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_ion_engine.py  --  Mineral / Acid-Base Homeostasis engine (deterministic, in-package).

SCOPE (see CHARTER.md): The third homeostasis axis: calcium-phosphate (PTH<->vitamin-D<->bone<->kidney<->gut), acid-base pH (respiratory CO2 + renal HCO3, a two-timescale buffer), and electrolyte (Na/K) setpoints defended as coupled loops. Osteoporosis and acid-base/electrolyte disorders are the disease axis.

WHAT RUNS TODAY: emerge_organs() builds nodes whose master-gene gamma is vendored (measured), defers
  to_measure masters honestly, reads developmental order off gamma. confirm_oscillators() runs the SHARED
  FHN for any oscillator node. 

LOOPS / SENSORS / DISEASE / THERAPY: emerged in repro/_engine/vp_loops.py, vp_sensors.py,
  repro/_pathology/setpoint_failure.py, repro/_therapy/fundamental_therapy.py. Writing unlocks when the
  stress battery (RI1-RI5) is green and research is signed off.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Organ, Neuron, spinodal, barrier, settle, dwell, dominant_freq, seed_everything

_HERE  = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

ORGAN_ROWS = [{'master': 'GCM2',
  'organ': 'parathyroid_pth',
  'role': 'PTH secretion: the fast calcium-raising effector',
  'dyn_class': 'setpoint-loop',
  'tau_s': None,
  'rate_note': 'serum Ca ~2.4 mM setpoint [L]; GCM2 gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'CASR',
  'organ': 'calcium_sensing_receptor',
  'role': 'the calcium SENSOR (setpoint comparator)',
  'dyn_class': 'setpoint-comparator',
  'tau_s': None,
  'rate_note': 'Ca setpoint sensing [L]; CASR gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'VDR',
  'organ': 'vitamin_d_axis',
  'role': 'slow calcium-absorption control (gut/kidney)',
  'dyn_class': 'slow-loop',
  'tau_s': None,
  'rate_note': 'vitamin-D Ca absorption [L]; VDR gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'RUNX2',
  'organ': 'bone_mineral_reservoir',
  'role': 'bone as the calcium/phosphate buffer (remodeling stores/releases)',
  'dyn_class': 'reservoir',
  'tau_s': None,
  'rate_note': 'bone Ca buffer [L]; RUNX2 gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'SIX2',
  'organ': 'kidney_mineral_acidbase',
  'role': 'renal Ca/PO4 handling + HCO3 regeneration (acid-base integrator)',
  'dyn_class': 'setpoint-loop',
  'tau_s': None,
  'rate_note': 'renal HCO3/Ca handling [L]',
  'gamma_state': 'vendored'}]
OSCILLATOR_ORGANS = []

def load_gamma():
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"]

def emerge_organs():
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
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="to_measure",
                              note="master " + r["master"] + ": gamma TO-MEASURE via DNA pipeline (measured input, not fitted)"))
        else:
            built.append(dict(organ=r["organ"], master=r["master"], gamma=None, role=r["role"], dyn_class=r["dyn_class"],
                              gamma_state="diffuse", note="no single master gene (circuit/derived/diffuse)"))
    go = [b for b in built if b.get("gamma") is not None]
    order = [b["organ"] for b in sorted(go, key=lambda b: b["gamma"])]
    return dict(organs=built, gamma_order_ascending=order,
                order_grade="[V] order is a gamma readout over MEASURED nodes; SIGN to validate vs cited timing",
                deferred_gamma=[b["master"] for b in built if b.get("gamma_state") == "to_measure"])

def confirm_oscillators():
    seed_everything(); out = {}
    for r in ORGAN_ROWS:
        if r["dyn_class"] not in ("oscillator", "coupled-oscillator"): continue
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
    out = dict(_what="Mineral / Acid-Base Homeostasis -- emerge nodes from measured gamma, then circulate the dynamics.",
               organs=organs, oscillators=osc,
               dynamics_status="SKELETON: setpoint loops / couplings / disease attractor-shifts NOT yet emerged",
               targets_todo="see CHARTER.md research program and repro/_verify/stress_tests.py")
    pass
    return out

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
