#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_failure.py  --  Thermometabolic Homeostasis PATHOLOGY module. Disease here is NOT a local lesion;
it is a FAILURE of a defended setpoint -- a loop-gain drop, a setpoint DRIFT, or an attractor-shift of the
coupled homeostatic loop. Same R19 substrate as the rest of the framework: a healthy setpoint is a regulated
attractor; disease = the loop drifting within / crossing to a pathological basin.

THE DERIVED LAW (R19, no tuning).  A defended setpoint is the upper well at s_set=+sqrt(g). A pathological
loop-gain drop d in [0,1) lowers the EFFECTIVE stiffness g_eff = g*(1-d). Two consequences follow from the
substrate identities, not from fitting:
  * the basin gets SHALLOWER     -- barrier(g_eff)  = g_eff^2 / 4      (less robust to perturbation)
  * the crossing threshold drops  -- spinodal(g_eff) = 2*(g_eff/3)^1.5 (less chronic forcing needed to cross)
A chronic pathological forcing h_path then either DRIFTS the defended state (sub-spinodal) or CROSSES it to
the disease basin (supra-spinodal). That single mechanism -- shallower basin + lower crossing threshold under
a chronic forcing -- is the same Kramers/spinodal kernel the framework uses for carcinogenesis, applied at the
SYSTEM (loop) level instead of the cell level.

GRADES (C3): cited risk/setpoint anchor [L]; reproduced setpoint-drift / attractor-shift SHAPE [V]; ABSOLUTE
incidence/rate [O] with a STATED obstacle (needs external calibration). No silent claims.

Composition with disease_wp: a MONOGENIC lesion (e.g. MODY) is owned by disease_wp as a GENE lesion; here it
enters as a loop PARAMETER (an effective-gain drop) and the systemic trajectory is computed. Polygenic/acquired
disease (T2D, obesity, metabolic syndrome) lives here as loop dysregulation.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import barrier, spinodal, settle

_HERE = os.path.dirname(__file__)
_GAMMA = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")

def _g(sym):
    return json.load(open(_GAMMA, encoding="utf-8"))["genes"][sym]["gamma"]

# Each failure: the node it dysregulates (measured gamma), the loop-gain drop d and chronic forcing h_path
# that NAME the pathology, and the CITED anchor. d and h_path are pathology DESCRIPTORS (declared, cited to a
# clinical axis), never fitted to hit a number; the OUTPUT (drift / crossing) is derived from R19.
FAILURES = [
    {"site": "type 2 diabetes", "node": "INSR (insulin-glucose effector)", "sym": "INSR",
     "loop_gain_drop": 0.45, "chronic_forcing": -0.62,
     "mechanism": "insulin resistance lowers glucose-loop gain (shallower euglycemic basin) while a chronic "
                  "caloric/adiposity forcing pushes disposal down; past the reduced spinodal the state crosses "
                  "to the hyperglycemic basin",
     "anchor": "RR / progression graded vs cited risk axes (BMI, HbA1c cohorts) [L]; attractor-shift shape [V]; "
               "absolute incidence [O]"},
    {"site": "obesity", "node": "lipostat (PPARG storage / LEPR feedback / MC4R setpoint)", "sym": "PPARG",
     "loop_gain_drop": 0.35, "chronic_forcing": 0.30,
     "mechanism": "leptin/melanocortin feedback-gain drop raises the defended adiposity setpoint; a sustained "
                  "positive energy forcing drifts the regulated state UP (defended at higher adiposity) -- "
                  "sub-spinodal drift, not (yet) a basin crossing",
     "anchor": "defended-setpoint drift vs cited energy-balance data [L]; drift shape [V]; absolute kg/BMI [O]"},
    {"site": "metabolic syndrome", "node": "coupled glucose+lipid loops (shared upstream node)", "sym": "INSR",
     "loop_gain_drop": 0.40, "chronic_forcing": -0.58,
     "mechanism": "a shared upstream gain drop co-moves the glucose and lipid loops; the cluster crosses together "
                  "because one substrate node (insulin signalling) gates both basins -- multi-loop co-failure",
     "anchor": "cluster co-movement vs cited prevalence [L]; multi-loop crossing [V]; absolute [O]"},
    {"site": "(MODY / monogenic, via disease_wp)", "node": "GCK/HNF setpoint (gene lesion = parameter)", "sym": "INSR",
     "loop_gain_drop": 0.25, "chronic_forcing": 0.0,
     "mechanism": "a monogenic lesion enters as a fixed loop-PARAMETER perturbation (a glucose-sensing gain "
                  "offset) owned by disease_wp; the systemic trajectory is computed HERE from that parameter",
     "anchor": "parameter imported from disease_wp [cited]; systemic trajectory [V]"},
]

def setpoint_shift(gamma, loop_gain_drop, chronic_forcing):
    """The derived law. A loop-gain drop d lowers effective stiffness g_eff=g*(1-d): shallower basin
    (barrier) and lower crossing threshold (spinodal). A chronic forcing then drifts the defended state
    (sub-spinodal) or crosses it to the pathological basin (supra-spinodal). All from R19, no tuning."""
    d = min(max(float(loop_gain_drop), 0.0), 0.999)
    g_eff = float(gamma) * (1.0 - d)
    b0, b1 = float(barrier(gamma)), float(barrier(g_eff))
    sp0, sp1 = float(spinodal(gamma)), float(spinodal(g_eff))
    s_healthy = settle(gamma, 0.0, s0=math.sqrt(gamma))
    s_path = settle(g_eff, float(chronic_forcing), s0=math.sqrt(g_eff))
    crossed = abs(chronic_forcing) > sp1
    return dict(
        gamma=round(float(gamma), 6), loop_gain_drop=round(d, 6), g_effective=round(g_eff, 6),
        healthy_barrier=round(b0, 6), residual_barrier=round(b1, 6),
        healthy_spinodal=round(sp0, 6), residual_spinodal=round(sp1, 6),
        chronic_forcing=round(float(chronic_forcing), 6),
        healthy_setpoint=round(float(s_healthy), 6), pathological_state=round(float(s_path), 6),
        attractor_crossed=bool(crossed),
        regime=("attractor-shift (crossed to the disease basin)" if crossed
                else "setpoint drift (defended at a shifted value, basin intact)"),
        note="loop-gain loss shrinks the barrier and lowers the crossing threshold; the chronic forcing then "
             "drifts or crosses the setpoint -- the same Kramers/spinodal kernel at the loop level")

def run_failures():
    rows = []
    for f in FAILURES:
        g = _g(f["sym"])
        sh = setpoint_shift(g, f["loop_gain_drop"], f["chronic_forcing"])
        rows.append({"site": f["site"], "node": f["node"], "mechanism": f["mechanism"],
                     "anchor": f["anchor"], "r19": sh,
                     "grade": "anchor [L] / shape [V] / absolute incidence-rate [O] (obstacle: needs external "
                              "calibration of the chronic-forcing axis to clinical units)"})
    return rows

def status():
    return {"model": "R19 setpoint as regulated attractor; disease = loop-gain drop -> shallower basin + lower "
                      "crossing threshold under a chronic forcing -> setpoint drift / attractor-shift",
            "derived_law": "g_eff = g*(1-d); barrier=g_eff^2/4; spinodal=2*(g_eff/3)^1.5; crossed iff |forcing|>spinodal",
            "failures": run_failures(),
            "grades": "anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle)",
            "disease_wp_composition": "monogenic lesion = imported loop parameter (cited); systemic trajectory = "
                                      "computed here. Acquired/polygenic disease = loop dysregulation, owned here."}

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
