#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fundamental_therapy.py  --  FUNDAMENTAL (root-directed) treatment, derived from the failure taxonomy.

The framework turns "what is the disease?" into "which part of the loop failed?", and that immediately
yields "what is the FUNDAMENTAL fix?" -- not the symptom, but the failed element. Five principled classes,
each keyed to a failure mode (setpoint_failure.py), each grounded in real (often current) therapeutics,
each graded honestly. Where the framework PREDICTS something beyond current practice, it is flagged [H]
(framework hypothesis), never asserted as established.

  Failure mode (R19)                Fundamental fix                         Established example (cited)
  --------------------------------  --------------------------------------  ----------------------------------
  setpoint DRIFT (comparator)       RESET the set-point (allosteric)        calcimimetic down / calcilytic up
  loop-gain DROP                    RESTORE the limiting arm's gain         active vitamin D; alkali at source
  reservoir DEPLETION               REFILL the reservoir (> slow withdrawal) anabolic (PTH/anti-sclerostin)
  threshold/SPINODAL crossing       STAY BELOW the threshold                hydration/citrate; anti-FGF23
  upstream ROOT driver              remove the driver                       estrogen/SERM; mechanical loading

Two simulations make the framework's distinctive predictions falsifiable:
  T1  setpoint-reset: a calcilytic/calcimimetic (shifting the comparator reference back) restores the
      defended value in a setpoint-drift disease -> treatment IS recalibration. [V]
  T2  reservoir refill vs withdrawal-slow: for a DEPLETED reservoir, raising formation (anabolic) RECOVERS
      the reserve, while only reducing withdrawal (anti-resorptive) merely HALTS the decline -> anabolic is
      the more fundamental fix for depletion (matches the clinical anabolic-first-then-antiresorptive
      sequence). [V] shape; absolute gains [O].

GRADES (C3): mechanism->failure-mode mapping [V]; clinical efficacy of named drugs cited [L]; novel
combination/strategy predictions [H] (framework-derived, flagged).
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_substrate import seed_everything
import importlib
loops = importlib.import_module("vp_loops")

# ---------- T1: set-point reset restores the defended value ----------
def t1_setpoint_reset(disease_shift=0.15, drug_reset=0.15):
    """Setpoint-drift disease (comparator reset by +disease_shift); the drug resets it by -drug_reset.
    The loop's defended value returns toward normal -> treatment = recalibration of the instrument."""
    seed_everything(); m=3.0; g_eff=2.0; pmin=0.1; pmax=1.0; loss=g_eff*(pmin+pmax)/2.0
    def defended(ca_sp):
        ca=1.0; dt=0.02; n=int(400.0/dt)
        for _ in range(n):
            P=loops.pth_curve(ca, ca_sp, m, pmin, pmax); ca+=dt*(g_eff*P-loss)
        return float(ca)
    untreated=defended(1.0+disease_shift)                       # defends pathological value
    treated=defended(1.0+disease_shift-drug_reset)              # drug shifts comparator back
    return dict(disease_setpoint_shift=disease_shift, drug_reset=drug_reset,
                defended_untreated=round(untreated,4), defended_treated=round(treated,4),
                normalized=bool(abs(treated-1.0)<0.05),
                example="calcimimetic (cinacalcet/etelcalcetide) resets CaSR set-point DOWN in hyperPTH; calcilytic (encaleret) resets UP in ADH1",
                grade="[V] recalibration restores the defended value; clinical efficacy cited [L]")

# ---------- T2: reservoir REFILL vs withdrawal-slowing ----------
def _bone_trajectory(formation, kappa_withdraw, B0=0.5, demand=0.3, B_max=1.0, T=600.0, dt=0.05):
    """Run the RI3 reservoir from a DEPLETED start B0 under a fixed demand, with given formation and
    withdrawal coefficients. Bone mass is capped at a peak ceiling B_max (cannot exceed healthy peak).
    Ca dynamics are independent of B here (the loop holds Ca); B records the reservoir balance."""
    seed_everything(); m=3.0; g_eff=6.0; beta=2.0; clr=4.0; P0=loops.pth_curve(1.0,1.0,m)
    ca=1.0; B=B0; tr=[]
    for i in range(int(T/dt)):
        Pex=loops.pth_curve(ca,1.0,m)-P0
        ca+=dt*(g_eff*Pex+beta*Pex-clr*(ca-1.0)-demand)
        B=min(max(B+dt*(formation - kappa_withdraw*max(Pex,0.0)),0.0), B_max); tr.append(B)
    return float(tr[-1]), tr

def t2_reservoir_refill():
    """For a DEPLETED reservoir (B0=0.5 of peak): anabolic (raise formation) REFILLS decisively; anti-
    resorptive (cut withdrawal) prevents further loss and rebuilds slowly; untreated keeps declining.
    Anabolic is the more fundamental fix for depletion (and refills fastest under ongoing demand)."""
    base_f=0.0008; base_k=0.05; B0=0.5
    untreated,_=_bone_trajectory(base_f, base_k, B0=B0)                 # keeps falling
    antiresorptive,_=_bone_trajectory(base_f, base_k*0.2, B0=B0)        # withdrawal slowed
    anabolic,_=_bone_trajectory(base_f*15.0, base_k, B0=B0)             # formation raised (refill)
    return dict(start_reserve=B0, peak_ceiling=1.0, untreated_final=round(untreated,4),
                antiresorptive_final=round(antiresorptive,4), anabolic_final=round(anabolic,4),
                anabolic_recovers=bool(anabolic>B0+0.02),
                antiresorptive_better_than_untreated=bool(antiresorptive>untreated),
                anabolic_beats_antiresorptive=bool(anabolic>antiresorptive),
                example="anti-resorptive (bisphosphonate/denosumab) slows withdrawal; anabolic (teriparatide/abaloparatide intermittent-PTH, romosozumab anti-sclerostin) refills",
                grade="[V] refill > withdrawal-slow for a depleted reservoir; absolute gains [O]; clinical sequence cited [L]")

# ---------- the principled taxonomy + frontier hypotheses ----------
THERAPY_CLASSES = [
 {"failure_mode":"setpoint drift (comparator reset)", "fundamental_fix":"reset the set-point (allosteric sensor modulator)",
  "established":"calcimimetic (cinacalcet, etelcalcetide) for 2deg/1deg hyperPTH; calcilytic (encaleret) for ADH1 (Phase 3 CALIBRATE positive 2025)",
  "diseases":["primary hyperparathyroidism","ADH1"], "grade":"[V] mapping; [L] efficacy"},
 {"failure_mode":"loop-gain drop (limiting arm)", "fundamental_fix":"restore the failed arm's gain at its source",
  "established":"active vitamin D / calcitriol (VDR slow arm); alkali / restore renal HCO3 transport in RTA; thiazide raises renal Ca-reabsorption gain",
  "diseases":["metabolic acidosis","hypocalcemia","hypercalciuria"], "grade":"[V] mapping; [L] efficacy"},
 {"failure_mode":"reservoir depletion", "fundamental_fix":"REFILL the reservoir (anabolic) > slow withdrawal (anti-resorptive)",
  "established":"anabolic: teriparatide/abaloparatide (intermittent PTH), romosozumab (anti-sclerostin, dual action); anti-resorptive: bisphosphonates, denosumab",
  "diseases":["osteoporosis"], "grade":"[V] mapping + T2 sim; [L] efficacy/sequence"},
 {"failure_mode":"threshold/spinodal crossing", "fundamental_fix":"stay below the solubility/precipitation threshold",
  "established":"hydration + citrate (raise Ca-oxalate solubility) for stones; phosphate binders / anti-FGF23 (burosumab) to control the Ca*PO4 product",
  "diseases":["nephrolithiasis","vascular calcification","hyperphosphatemia"], "grade":"[V] mapping; [L] efficacy"},
 {"failure_mode":"upstream root driver", "fundamental_fix":"remove the driver",
  "established":"estrogen/SERM for post-menopausal bone loss; mechanical loading lowers sclerostin (non-drug anabolic input); parathyroidectomy removes the PTH source",
  "diseases":["post-menopausal osteoporosis","primary hyperparathyroidism"], "grade":"[V] mapping; [L] efficacy"},
]

FRONTIER_HYPOTHESES = [
 {"id":"H-RESET", "hypothesis":"any mis-calibrated IONIC SENSOR is a set-point-reset target -- the encaleret/CaSR paradigm "
  "generalizes to OTOP1/ASIC/ENaC sensor diseases (allosteric recalibration over symptom control).",
  "grade":"[V] generalization direction reproduced -- the defended attractor equals the comparator set-point for every Hill slope, "
  "so allosteric reset is the unique DURABLE fix across the sensor family while symptom control relapses (frontier_quant.h_reset_generalization); "
  "CaSR proof-of-concept cited [L] (encaleret Ph3 CALIBRATE, cinacalcet); non-CaSR allosteric recalibrators [H]; absolute residuals [O]"},
 {"id":"H-DUAL", "hypothesis":"sustained reservoir refill needs to remove the FORMATION BRAKE, not just push formation: "
  "romosozumab's anabolic window closes as DKK1 rises (cited), so DUAL anti-sclerostin + anti-DKK1 should sustain "
  "refilling longer than either alone.", "grade":"[V] ordering (dual>single>untreated) reproduced (frontier_quant.h_dual_window); "
  "premise + preclinical synergy cited [L] (Florio 2016); absolute window size [O]; human clinical efficacy [H]"},
 {"id":"H-ARM", "hypothesis":"chronic acid-base disease is better fixed by restoring the FAILED ARM at source (renal HCO3 "
  "transporter / ventilatory drive) than by lifelong exogenous buffering (which leaves loop gain low).",
  "grade":"[V] direction reproduced from the OU loop-gain law -- at matched mean correction, arm restoration (raising k) uniquely "
  "tightens variance and rejects a fresh acid load by the factor k_high/k_low, while buffering cancels the mean only and is non-durable "
  "(frontier_quant.h_arm_restoration); current lifelong-alkali care cited [L] (dRTA / ADV7103); absolute gains [O]; clinical arm-restoration [H]"},
 {"id":"H-OTOC", "hypothesis":"BPPV recurrence reflects otoconial CaCO3 instability; a fundamental approach targets the "
  "otoconial micro-pH/Ca environment (OTOP1-dependent) to stabilize/repair biomineral, beyond repositioning.",
  "grade":"[V] saturation DIRECTION reproduced -- acidosis & hypocalcemia lower calcite Omega (frontier_quant.h_otoc_saturation); "
  "OTOP1<->pH + ion-chemistry BPPV model cited [L] (Frontiers 2025); absolute Omega=1 threshold [O]; clinical OTOP1/pH targeting [H]"},
]

def status():
    seed_everything()
    t1=t1_setpoint_reset(); t2=t2_reservoir_refill()
    demos_ok = t1["normalized"] and t2["anabolic_recovers"] and t2["anabolic_beats_antiresorptive"]
    return dict(_what="Fundamental (root-directed) therapy keyed to the R19 failure mode; established drugs cited, "
                      "framework predictions flagged [H].",
                simulations={"T1_setpoint_reset":t1, "T2_reservoir_refill":t2}, demonstrations_pass=bool(demos_ok),
                therapy_classes=THERAPY_CLASSES, frontier_hypotheses=FRONTIER_HYPOTHESES,
                grade="mechanism->failure mapping [V]; named-drug efficacy cited [L]; novel strategies [H]")

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
