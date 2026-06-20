#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_age_engine.py  --  Aging / Senescence engine (deterministic, in-package).

SCOPE (see CHARTER.md): The capstone temporal layer: aging is the slow drift and loss of gain of EVERY homeostatic setpoint, plus the accumulation of cells stuck in pathological R19 attractors (senescence). It is the dominant RISK MULTIPLIER for the oncology/pathology kernels across the whole framework. Sarcopenia, frailty, and multimorbidity are the disease axis.

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

ORGAN_ROWS = [{'master': 'TP53',
  'organ': 'cellular_senescence',
  'role': 'cells stuck in a pathological R19 attractor (irreversible arrest + SASP)',
  'dyn_class': 'stuck-attractor',
  'tau_s': None,
  'rate_note': 'senescent-cell accumulation rate [L]; TP53 gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'CDKN2A',
  'organ': 'senescence_arrest_switch',
  'role': 'the p16INK4a senescence arrest program (the switch)',
  'dyn_class': 'stuck-attractor',
  'tau_s': None,
  'rate_note': 'p16 accumulation with age [L]; CDKN2A gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'FOXO3',
  'organ': 'longevity_signaling',
  'role': 'the insulin/IGF-mTOR-FOXO longevity axis (loop-gain maintenance)',
  'dyn_class': 'maintenance',
  'tau_s': None,
  'rate_note': 'longevity-pathway tone [L]; FOXO3 gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': 'TERT',
  'organ': 'telomere_maintenance',
  'role': 'telomere attrition -> the replicative limit (reservoir clock)',
  'dyn_class': 'reservoir-depletion',
  'tau_s': None,
  'rate_note': 'telomere shortening rate [L]; TERT gamma TO-MEASURE',
  'gamma_state': 'vendored'},
 {'master': '(systemic_setpoint_drift)',
  'organ': 'homeostatic_setpoint_drift',
  'role': 'the slow drift of ALL imported setpoints (cross-package)',
  'dyn_class': 'integrative-decline',
  'tau_s': None,
  'rate_note': 'multi-setpoint drift; imports siblings',
  'gamma_state': 'diffuse'}]
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
    """Emerge nodes from MEASURED gamma, then circulate the aging dynamics (RA1..RA6) and the
    cross-species longevity discriminant (RA7). Deterministic; the result hashes bit-for-bit."""
    seed_everything()
    organs = emerge_organs(); osc = confirm_oscillators()
    sys.path.insert(0, os.path.dirname(__file__))
    import importlib
    ad = importlib.import_module("aging_dynamics")
    xd = importlib.import_module("xspecies_discriminant")
    arc = importlib.import_module("archaic_discriminant")
    tk = importlib.import_module("telomere_keystone")
    dynamics = dict(
        RA1_setpoint_drift      = ad.ra1_setpoint_drift(),
        RA2_senescence_stuck    = ad.ra2_senescence_stuck(),
        RA3_reservoir_depletion = ad.ra3_reservoir_depletion(),
        RA4_hallmarks_map       = ad.ra4_hallmarks_map(),
        RA5_risk_multiplier     = ad.ra5_risk_multiplier(),
        RA6_rate_of_aging       = ad.ra6_rate_of_aging(),
    )
    xspecies = xd.discriminant()
    archaic = arc.discriminant()
    telomere = tk.keystone()
    out = dict(_what="Aging / Senescence -- nodes emerge from measured gamma; the dynamics circulate.",
               organs=organs, oscillators=osc, dynamics=dynamics,
               cross_species_RA7=xspecies,
               archaic_observation_RA8=archaic,
               telomere_keystone_RA9=telomere,
               dynamics_status=("LIVE: RA1..RA6 simulated on the vendored R19 substrate; RA7 cross-species "
                                "discriminant; RA8 archaic<->present-day observation (OBSERVATION ONLY); "
                                "RA9 telomere keystone"),
               offline_reproduce=dict(cross_species=xd.verify_offline_reproduces(),
                                      archaic=arc.verify_offline_reproduces()))
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
