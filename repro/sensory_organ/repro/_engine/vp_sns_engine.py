#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_sns_engine.py  --  Special-Sense Organs engine (deterministic, in-package).

SCOPE (see CHARTER.md): The special-sense ORGANS as physical instruments: ocular optics/accommodation, the cochlear basilar-membrane frequency map, vestibular inertial sensing, and taste/olfaction chemodetection. Organ optics/acoustics are CLASSICAL physics (documented, linked); the R19 substrate handles the cellular transduction switch. neuro owns transduction->spike. Cataract, glaucoma, AMD, presbycusis are the disease axis.

WHAT RUNS TODAY: emerge_organs() builds nodes whose master-gene gamma is vendored (measured), defers
  to_measure masters honestly, reads developmental order off gamma. confirm_oscillators() runs the SHARED
  FHN for any oscillator node. 

WHAT IS A SKELETON: the setpoint LOOPS / oscillator couplings / disease attractor-shifts (see CHARTER
  research program). Writing is locked until the stress battery is green.

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

ORGAN_ROWS = [{'master': 'PAX6',
  'organ': 'eye_retina_optics',
  'role': 'retinal photoreceptor mosaic + the ocular dioptric system (optics classical; switch R19)',
  'dyn_class': 'sensor',
  'tau_s': None,
  'rate_note': 'refraction / accommodation [L]; PAX6 measured',
  'gamma_state': 'vendored'},
 {'master': 'RAX',
  'organ': 'eye_photoreceptor',
  'role': 'photoreceptor phototransduction switch (R19 cellular)',
  'dyn_class': 'sensor-switch',
  'tau_s': None,
  'rate_note': 'phototransduction threshold [L]',
  'gamma_state': 'vendored'},
 {'master': 'EYA1',
  'organ': 'cochlea_frequency_map',
  'role': 'basilar-membrane tonotopic frequency analysis (mechanics classical; switch R19)',
  'dyn_class': 'sensor',
  'tau_s': None,
  'rate_note': 'tonotopic place-frequency map [L]; EYA1 measured',
  'gamma_state': 'vendored'},
 {'master': 'SOX2',
  'organ': 'inner_ear_haircell',
  'role': 'cochlear/vestibular hair-cell mechanotransduction (R19 switch)',
  'dyn_class': 'sensor-switch',
  'tau_s': None,
  'rate_note': 'mechanotransduction threshold [L]',
  'gamma_state': 'vendored'},
 {'master': '(vestibular_system)',
  'organ': 'vestibular_balance',
  'role': 'semicircular-canal + otolith inertial sensing (balance)',
  'dyn_class': 'sensor',
  'tau_s': None,
  'rate_note': 'vestibulo-ocular reflex gain [L]; circuit',
  'gamma_state': 'diffuse'},
 {'master': 'TAS1R3',
  'organ': 'taste_chemodetection',
  'role': 'taste receptor chemodetection (sweet/umami; bitter via TAS2R)',
  'dyn_class': 'sensor',
  'tau_s': None,
  'rate_note': 'taste detection threshold [L]; TAS1R3 measured',
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


def validate_developmental_order(organs):
    """SIGN-validate the gamma-derived order against CITED developmental timing. Broad signal: taste latest.
    Fine ordering among the early sensory organs is NOT robustly validated -> honest partial."""
    order = organs["gamma_order_ascending"]
    # cited early-vs-late developmental specification (mouse/human): eye field (PAX6/RAX) & otic placode
    # (EYA1/SOX2) are EARLY (wk 3-4); taste buds are LATE (wk 8+). Refs: standard developmental biology.
    cited_late = "taste_chemodetection"
    broad_ok = bool(order and order[-1] == cited_late)
    return dict(gamma_order_ascending=order,
                broad_prediction="taste organ specified latest", broad_validated=broad_ok,
                fine_ordering_status="[L]-pending: fine order among early eye/ear nodes not robustly validated vs cited timing (PAX6/RAX eye-field and EYA1/SOX2 otic placode co-occur early); honest partial",
                grade="[V] broad signal (taste latest) ; [O]->[L] fine ordering needs cited stage timing")


def circulate():
    """Emerge nodes from measured gamma, then run the full sensory research program:
    organ optics/acoustics (classical), the molecular transducer switches (R19), the cochlear Hopf
    amplifier (criticality), and the developmental-order validation. Deterministic; HTML is never built."""
    import transduction, cochlear_amplifier, organ_optics
    organs = emerge_organs(); osc = confirm_oscillators()
    G = load_gamma()
    out = dict(_what="Special-Sense Organs -- emerge nodes from measured gamma, then circulate the dynamics.",
               organs=organs, oscillators=osc,
               developmental_order=validate_developmental_order(organs),
               organ_optics_acoustics=organ_optics.verify_optics_acoustics(),     # RS1, RS3-map, RS4 (classical)
               transduction=transduction.verify_transducers(G),                    # RS2, RS3-switch, RS5 (R19)
               cochlear_amplifier=cochlear_amplifier.verify_amplifier(),           # RS3-amplifier (Hopf criticality)
               dynamics_status="RESEARCH: organ instruments (classical) + transducer switches (R19) + Hopf amplifier emerged and circulated",
               targets_todo="see CHARTER.md research program and repro/_verify/stress_tests.py")
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
