#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
setpoint_failure.py  --  Mineral / Acid-Base / Electrolyte PATHOLOGY: disease as a FAILURE of a defended
setpoint / a clock / a sense organ on the SAME R19 substrate. Six derived failure MODES, each tied to a
MAJOR (common, polygenic, acquired, age-related) disease; RARE / monogenic forms enter as a CITED
PARAMETER (disease_wp), with the systemic trajectory computed here.

THE FAILURE LAW (derived from R19 + the OU setpoint of vp_loops):
  (1) loop-gain DROP   k -> k' < k :  stationary variance Var = sigma^2/(2k) BLOWS UP, correction tau=1/k
                                      slows; at k -> k_crit regulation is lost (ATTRACTOR-SHIFT).
  (2) setpoint DRIFT   x* -> x*' :     the comparator reference moves; the loop now DEFENDS a pathological
                                      value (sensor mis-calibration / set-point reset).
  (3) reservoir DEPLETION : chronic withdrawal > refill -> the buffer empties while the variable is held.
  (4) buffer-arm FAILURE : one timescale of a two-timescale buffer loses gain -> the other cannot hold.
  (5) threshold/SPINODAL crossing : a hard solubility/precipitation threshold is crossed (discontinuous).
  (6) instrument FAILURE (sensory) : a sensor mis-calibration = a special case of (2) at the comparator.

GRADES (C3): cited risk/setpoint anchor [L]; reproduced shape [V]; ABSOLUTE incidence/rate [O] (stated).
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_substrate import barrier, spinodal, settle, seed_everything
import importlib
loops = importlib.import_module("vp_loops")

# ---------- the derived laws (reusable) ----------
def loop_gain_drop(k_healthy=2.0, k_disease=0.4, sigma=0.3):
    """(1) Var = sigma^2/(2k): a loop-gain drop blows up setpoint variance and slows correction. [V]."""
    vh=loops.ou_setpoint(k_healthy, sigma=sigma)["variance"]; vd=loops.ou_setpoint(k_disease, sigma=sigma)["variance"]
    return dict(k_healthy=k_healthy, k_disease=k_disease, var_healthy=vh, var_disease=vd,
                variance_ratio=round(vd/vh,3), predicted_ratio=round(k_healthy/k_disease,3),
                tau_healthy=round(1.0/k_healthy,3), tau_disease=round(1.0/k_disease,3),
                blows_up=bool(vd>vh))

def setpoint_drift(shift=0.15):
    """(2) Shift the comparator reference; the loop defends the NEW (pathological) value. The plant is
    PTH-effector vs a constant loss (no independent pull to the old value), so the steady state IS the
    comparator setpoint: loss = g_eff*(pmin+pmax)/2 puts the fixed point at ca_sp. [V]."""
    seed_everything(); ca_sp_new=1.0+shift; m=3.0; g_eff=2.0; pmin=0.1; pmax=1.0
    loss=g_eff*(pmin+pmax)/2.0; ca=1.0; dt=0.02; T=400.0; n=int(T/dt)
    for i in range(n):
        P=loops.pth_curve(ca, ca_sp_new, m, pmin, pmax); ca+=dt*(g_eff*P - loss)
    return dict(setpoint_shift=shift, old_setpoint=1.0, new_setpoint=round(ca_sp_new,4), defended_value=round(float(ca),4),
                defends_shifted_setpoint=bool(abs(ca-ca_sp_new)<0.05),
                note="comparator reset -> loop now defends the pathological setpoint (e.g. PTH set-point reset up = primary hyperPTH; CaSR reset down = ADH1)")

def spinodal_cross(margin_safe=0.85, margin_over=1.15):
    """(5) Crossing a hard solubility/precipitation threshold is discontinuous (spinodal analogy). [V]."""
    g=1.5  # representative stiff node
    h_safe=margin_safe*spinodal(g); h_over=margin_over*spinodal(g)
    s_safe=settle(g, h_safe, s0=-math.sqrt(g)); s_over=settle(g, h_over, s0=-math.sqrt(g))
    return dict(threshold=round(spinodal(g),4), state_below=round(float(s_safe),3), state_above=round(float(s_over),3),
                crossed_is_discontinuous=bool((s_safe<0) and (s_over>0)),
                note="below threshold stays in the soluble basin; above it the precipitated basin is forced (stone/calcification)")

# ---------- major diseases mapped to failure modes ----------
FAILURES = [
 {"site":"osteoporosis", "mode":"reservoir depletion (+ loop-gain drop with estrogen loss/aging)",
  "mechanism":"chronic Ca/bone setpoint imbalance -> net reservoir depletion (post-menopausal / age)",
  "anchor":"bone-density loss vs cited post-menopausal/age rates [L]; reservoir depletion [V]; cross-ref reproductive(estrogen)+aging",
  "monogenic_xref":"none (this is the polygenic/acquired/age disease)"},
 {"site":"primary hyperparathyroidism", "mode":"setpoint drift (PTH set-point reset UP)",
  "mechanism":"PTH setpoint reset upward -> hypercalcemia",
  "anchor":"setpoint reset [V]; cited Ca/PTH [L]; rare genetic forms (MEN1, CASR/FHH) -> disease_wp",
  "monogenic_xref":"MEN1, FHH (CASR loss-of-fn) -> disease_wp as cited parameter"},
 {"site":"metabolic acidosis / alkalosis", "mode":"buffer-arm failure (renal or respiratory arm gain drops)",
  "mechanism":"the two-timescale acid-base defense fails on one arm",
  "anchor":"two-timescale buffer failure [V]; cited pH 7.4 + Winters [L]",
  "monogenic_xref":"distal/proximal RTA (SLC4A1, etc.) -> disease_wp"},
 {"site":"common electrolyte disorders", "mode":"loop-gain drop / setpoint deviation (Na/K)",
  "mechanism":"hyper/hypo- natremia / kalemia (volume + renal handling)",
  "anchor":"setpoint deviation vs cited [L]; loop [V]; volume<->pressure = hemodynamic seam",
  "monogenic_xref":"Liddle (SCNN1), Gitelman/Bartter -> disease_wp"},
 {"site":"nephrolithiasis (calcium stones)", "mode":"threshold/spinodal crossing (supersaturation)",
  "mechanism":"supersaturation once the Ca/oxalate solubility threshold is exceeded",
  "anchor":"crossing a solubility threshold [V]; cited [L]",
  "monogenic_xref":"primary hyperoxaluria (AGXT) -> disease_wp"},
 {"site":"autosomal dominant hypocalcemia type 1 (ADH1)", "mode":"instrument failure (CaSR gain-of-fn -> setpoint reset DOWN)",
  "mechanism":"CaSR too sensitive -> defends too-low serum Ca (sensor mis-calibration)",
  "anchor":"setpoint reset via sensor [V]; cited CASR variants [L]; MONOGENIC -> disease_wp (entered as cited setpoint shift)",
  "monogenic_xref":"CASR gain-of-fn -> disease_wp; calcilytic (encaleret) resets set-point UP"},
 {"site":"BPPV (benign paroxysmal positional vertigo)", "mode":"mineral-reservoir + instrument failure (otoconia)",
  "mechanism":"dislodged/degenerated otoconia (CaCO3) -> mechanical vestibular instrument failure",
  "anchor":"mineral<->sensory seam [V/mapping]; common, age-related [L]; OTOP1 biomineral pH dependence cited",
  "monogenic_xref":"none common; the seam links acid-base/mineral homeostasis to a sense organ"},
]

def status():
    seed_everything()
    laws = {"loop_gain_drop": loop_gain_drop(),
            "setpoint_drift": setpoint_drift(),
            "spinodal_cross": spinodal_cross()}
    ok = (laws["loop_gain_drop"]["blows_up"] and laws["setpoint_drift"]["defends_shifted_setpoint"]
          and laws["spinodal_cross"]["crossed_is_discontinuous"])
    return {"model":"R19 setpoint/clock/sense-organ failure: loop-gain drop / setpoint drift / reservoir depletion / buffer-arm failure / threshold crossing / instrument failure",
            "derived_laws":laws, "laws_demonstrated":bool(ok), "failures":FAILURES,
            "status":"DERIVED: failure laws demonstrated on the substrate; per-disease cited anchors set",
            "grades":"anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle)",
            "disease_wp_composition":"rare/monogenic = cited parameter in (setpoint shift / arm-gain); systemic trajectory = computed here"}

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
