#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_hmd_engine.py  --  Hemodynamic Homeostasis engine (deterministic, in-package).

SCOPE (see CHARTER.md): Mean arterial pressure (MAP) is owned by no single organ; this package closes
the CO x SVR x volume loop from the per-system seams and studies its fast (baroreflex) and slow
(RAAS / pressure-natriuresis) defence -- with essential hypertension modeled as a setpoint RESET, the
exact parallel of the lipostat reset in obesity, and chronic heart failure as an R19 basin collapse.

v0.2.0-research adds the FUNDAMENTAL layer the CHARTER asks for, beneath the visible mechanisms:
  * a SENSORY transduction layer (repro/_sensory): the baroreceptor PIEZO1/2 mechanosensor (fast loop)
    and the macula-densa NKCC2 NaCl chemosensor (slow loop) -- the actual molecular transducers that
    read the regulated variables;
  * the closed setpoint LOOPS (repro/_engine/vp_hmd_loops.py, RP1-RP5): MAP from seams, baroreflex
    buffering, the kidney integral controller, the hypertension setpoint reset, the HF basin fold;
  * a literature INTERACTION MAP (sensory cell -> afferent -> integrator/controller -> effector -> MAP
    -> feedback) with per-edge grade + anchor;
  * a FUNDAMENTAL-vs-symptomatic therapy read (repro/_therapy): reference-reset vs operating-point in
    hypertension; load-reduce + cycle-break vs effector-flog in HF, matching the clinical evidence base.

WHAT RUNS: emerge_organs() builds the nodes whose master-gene gamma is vendored (measured), defers the
  to_measure masters honestly, reads developmental order off gamma. circulate() now aggregates the
  nodes, the closed loops, the sensory layer, the interaction map, and the therapy read into ONE
  deterministic object whose hash covers everything.

DETERMINISM (VP-SPEC C1): BLAS pinned before numpy; fixed seed; round-before-hash; sorted keys.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math, hashlib
import numpy as np
_HERE  = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))
sys.path.insert(0, _HERE)                                   # vp_hmd_loops (same dir)
sys.path.insert(0, os.path.join(_HERE, "..", "_sensory"))   # baroreceptor, macula_densa
sys.path.insert(0, os.path.join(_HERE, "..", "_therapy"))   # fundamental_targets
sys.path.insert(0, os.path.join(_HERE, "..", "_pathology")) # hypotension_family
sys.path.insert(0, os.path.join(_HERE, "..", "_comparative")) # setpoint_emergence
sys.path.insert(0, os.path.join(_HERE, "..", "_calibration")) # scale_calibration
sys.path.insert(0, os.path.join(_HERE, "..", "_intervention")) # comfort-logic (analgesic technique)
from vp_substrate import Organ, Neuron, spinodal, barrier, settle, dwell, dominant_freq, seed_everything
import vp_hmd_loops as LOOPS
import baroreceptor as BARO
import macula_densa as MD
import fundamental_targets as RX
import hypotension_family as HYPO
import setpoint_emergence as COMP
import scale_calibration as CAL
import intervention_logic as IV

_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

# ---------------------------------------------------------------------------
#  NODES.  The four control nodes (gamma-emerged where a master gene exists),
#  plus the two SENSORY transducers beneath them, plus the regulated variable.
# ---------------------------------------------------------------------------
ORGAN_ROWS = [{'master': 'SIX2',
  'organ': 'kidney_volume_integrator',
  'role': 'pressure-natriuresis + RAAS volume control (the slow integrator)',
  'dyn_class': 'setpoint-loop',
  'tau_s': None,
  'rate_note': 'Na/volume handling [L]',
  'gamma_state': 'vendored'},
 {'master': 'REN',
  'organ': 'raas_endocrine',
  'role': 'renin-angiotensin-aldosterone slow pressure/volume control',
  'dyn_class': 'slow-loop',
  'tau_s': None,
  'rate_note': 'RAAS setpoint [L]; REN gamma 1.3634 measured [V]',
  'gamma_state': 'vendored'},
 {'master': '(baroreflex_arc)',
  'organ': 'baroreflex',
  'role': 'autonomic fast pressure buffer (cite cardioresp/neuro)',
  'dyn_class': 'fast-buffer',
  'tau_s': None,
  'rate_note': 'baroreflex gain [L]; circuit, cite siblings',
  'gamma_state': 'diffuse'},
 {'master': '(vascular_tone)',
  'organ': 'vascular_resistance',
  'role': 'SVR / Windkessel tone (cite circulatory vessels)',
  'dyn_class': 'effector',
  'tau_s': None,
  'rate_note': 'SVR; cite circulatory',
  'gamma_state': 'diffuse'}]
OSCILLATOR_ORGANS = []

# Sensory transducers (the "fundamental" layer beneath the control nodes).
SENSORY_NODES = [
    {'cell': 'baroreceptor', 'transducer': 'PIEZO1/PIEZO2 (mechanically activated cation channel)',
     'modality': 'arterial-wall stretch (proportional to pressure)', 'loop': 'fast',
     'feeds': 'baroreflex', 'identity_grade': '[L]',
     'anchor': 'Zeng et al., Science 362:464-467 (2018): Piezo1/2 double-KO abolishes baroreflex -> labile hypertension'},
    {'cell': 'macula_densa', 'transducer': 'NKCC2 (apical Na-K-2Cl cotransporter; furosemide-sensitive)',
     'modality': 'luminal NaCl (proportional to distal delivery / GFR)', 'loop': 'slow',
     'feeds': 'raas_endocrine (renin, inverse) + kidney_volume_integrator (TGF)', 'identity_grade': '[L]',
     'anchor': 'macula densa NaCl sensing via NKCC2 -> tubuloglomerular feedback + inverse renin control [L]'},
]

# ---------------------------------------------------------------------------
#  INTERACTION MAP (literature-anchored). Directed edges:
#    sensory cell -> afferent -> integrator/controller -> effector -> MAP -> feedback.
#  sign: '+' excitatory/raising, '-' inhibitory/lowering, '0' read-only sense.
# ---------------------------------------------------------------------------
INTERACTION_EDGES = [
    # afferent sensing
    ('MAP', 'baroreceptor', '0', '[L]', 'arterial wall stretch ~ pressure; PIEZO1/2 transduction (Zeng 2018)'),
    ('MAP', 'macula_densa', '0', '[L]', 'distal NaCl delivery ~ GFR ~ pressure; NKCC2 chemosensing (slow)'),
    # fast loop
    ('baroreceptor', 'baroreflex', '+', '[L]', 'afferent firing -> NTS -> autonomic outflow set'),
    ('baroreflex', 'vascular_resistance', '-', '[V]', 'fast negative feedback: pressure up -> sympathetic withdrawal -> SVR down (RP2)'),
    ('baroreflex', 'MAP', '-', '[V]', 'net fast buffering of a pressure step, residual ~ step/(1+G) (RP2)'),
    # slow loop
    ('macula_densa', 'raas_endocrine', '-', '[L]', 'high luminal NaCl -> renin DOWN (inverse); low NaCl -> renin UP'),
    ('macula_densa', 'kidney_volume_integrator', '+', '[V]', 'tubuloglomerular feedback: high NaCl -> afferent constriction -> GFR down'),
    ('raas_endocrine', 'vascular_resistance', '+', '[L]', 'AngII vasoconstriction raises SVR'),
    ('raas_endocrine', 'kidney_volume_integrator', '+', '[L]', 'aldosterone/AngII raise Na/volume retention -> raises the defended reference'),
    ('kidney_volume_integrator', 'MAP', '+', '[V]', 'integral (pressure-natriuresis) control sets the slow defended MAP reference (RP3, Guyton infinite gain)'),
    # effector -> regulated variable
    ('vascular_resistance', 'MAP', '+', '[V]', 'Ohm hydraulic: MAP = CVP + CO x SVR (RP1)'),
]

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
        if r["dyn_class"] != "oscillator": continue
        taus = r["tau_s"] if r["tau_s"] is not None else 40.0
        n = Neuron(gamma=1.0, tau_f=1.0, tau_s=float(taus), beta=0.5, name=r["organ"])
        S, dt = n.run(drive=0.55, T=8000.0, dt=0.05)
        f = dominant_freq(S, dt); nb = len(Neuron.spikes(S))
        out[r["organ"]] = dict(oscillates=bool(nb >= 3 and f > 0.0), beats=int(nb),
                               relaxation_freq_arb=round(float(f), 8), tau_s=float(taus),
                               rate_anchor=r["rate_note"], mechanism_grade="[V]", rate_grade="[L]")
    return out

def sensory_layer():
    """Run the two sensory transducer modules and return their deterministic reads."""
    return dict(
        baroreceptor=BARO.status(),
        macula_densa=MD.status(),
        note="sensory cells transduce the regulated variables (PIEZO1/2 mechano; NKCC2 NaCl chemo); "
             "afferent firing is a shared-R19 spike train (see baroreceptor.substrate_spikes)")

def closed_loops():
    """Run the five closed-loop discriminants RP1-RP5 (vp_hmd_loops)."""
    return LOOPS.all_loops()

def therapy_layer():
    """Fundamental-vs-symptomatic therapy read for the two major diseases."""
    return RX.status()

def hypotension_layer():
    """Low-pressure failure as a node decomposition (RP6-RP9 + cardiogenic + node-specific therapy)."""
    return HYPO.all_hypotension()

def comparative_layer():
    """Universality: defended-pressure setpoint emergence by loop accretion across organism grade."""
    return COMP.setpoint_emergence()

def calibration_layer():
    """[CAL] absolute-scale track: cited anchors propagated through the locked [V] relations and
    cross-checked against independent references (CAL1-CAL7). Closes the declared [O] absolute scales
    by EXPLICIT calibration -- first-principles derivation stays [O]. No new substrate math (C1)."""
    return CAL.all_calibration()

def build_interaction_map():
    """Assemble the literature-anchored node/edge interaction graph."""
    nodes = []
    for s in SENSORY_NODES:
        nodes.append(dict(id=s["cell"], kind="sensory", transducer=s["transducer"],
                          modality=s["modality"], loop=s["loop"], grade=s["identity_grade"]))
    for r in ORGAN_ROWS:
        nodes.append(dict(id=r["organ"], kind="control", role=r["role"], dyn_class=r["dyn_class"],
                          gamma_state=r["gamma_state"]))
    nodes.append(dict(id="MAP", kind="regulated_variable",
                      role="mean arterial pressure -- the defended output, owned by no single organ"))
    edges = [dict(src=a, dst=b, sign=sgn, grade=gr, mechanism=note)
             for (a, b, sgn, gr, note) in INTERACTION_EDGES]
    # close the loops explicitly: every sensory node senses MAP and feeds a controller
    fast = [e for e in edges if e["src"] in ("baroreceptor", "baroreflex")]
    slow = [e for e in edges if e["src"] in ("macula_densa", "raas_endocrine", "kidney_volume_integrator")]
    return dict(
        nodes=sorted(nodes, key=lambda n: (n["kind"], n["id"])),
        edges=edges,
        fast_loop="MAP -> baroreceptor(PIEZO) -> baroreflex -(-)-> SVR/HR -> MAP  (seconds; RP2)",
        slow_loop="MAP -> macula_densa(NKCC2) -> renin(-)/TGF(+) -> RAAS/kidney integrator -> volume -> MAP  (hours-days; RP3)",
        reset_axis="essential hypertension = rightward reset of the kidney integral reference (RP4); "
                   "chronic heart failure = collapse of the cardiac high-output basin (RP5)",
        cited_seams_not_re_emerged="carotid-body chemoreceptors (O2/CO2/pH) and cardiopulmonary volume "
                                   "receptors are cited afferent seams owned by the cardioresp sibling; "
                                   "SSOT -> referenced, not re-emerged here",
        n_fast_edges=len(fast), n_slow_edges=len(slow), grade="edges [L] identity / [V] reproduced loop shape")

def circulate():
    organs = emerge_organs(); osc = confirm_oscillators()
    out = dict(_what="Hemodynamic Homeostasis -- emerge nodes from measured gamma, transduce via the "
                     "sensory layer, circulate the fast/slow setpoint loops, map the interactions, and "
                     "read fundamental-vs-symptomatic therapy. MAP is owned by no single organ.",
               organs=organs,
               oscillators=osc,
               sensory=sensory_layer(),
               loops=closed_loops(),
               interaction_map=build_interaction_map(),
               therapy=therapy_layer(),
               hypotension=hypotension_layer(),
               comparative=comparative_layer(),
               calibration=calibration_layer(),
               intervention=IV.all_intervention(),
               dynamics_status="EMERGED: sensory transduction + RP1-RP5 closed loops + interaction map + "
                               "fundamental therapy read + hypotension node-decomposition (RP6-RP9) + "
                               "cross-organism setpoint emergence + the comfort-logic intervention layer "
                               "(analgesic three-lever technique, ported) all run deterministically under "
                               "one hash.",
               deferred="absolute scales now CALIBRATED [O]->[CAL] (CAL1-CAL7: pressure mmHg / baroreflex "
                        "gain / firing Hz / macula-densa NaCl+GFR / hypertension reset in clinical SBP / "
                        "therapy effect sizes / perfusion-floor+orthostatic) by explicit cited anchors -- "
                        "first-principles derivation stays [O]; residual-open: absolute disease incidence, "
                        "single-nephron GFR / NKCC2 K_m, trial HR/NNT, per-taxon pressures, the exact "
                        "phylogenetic transition clade. No master-gene gamma remains to measure (REN [V]).")
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
