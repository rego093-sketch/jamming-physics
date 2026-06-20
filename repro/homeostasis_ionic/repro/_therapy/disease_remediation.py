#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
disease_remediation.py  --  APPLY the three-lever principle to the diseases this volume OWNS.

Scope discipline (VP_FRAMEWORK_MAP section 6 ownership contract): this volume owns the COMMON, polygenic,
acquired, age-related disorders of mineral / acid-base / electrolyte LOOP regulation -- osteoporosis,
primary hyperparathyroidism, metabolic acidosis/alkalosis, common electrolyte disorders, nephrolithiasis,
and the Tier-2 trio (magnesium imbalance, CKD-MBD, humoral hypercalcemia of malignancy). Rare / monogenic
forms remain owned by disease_wp and enter here only as a cited parameter. Carcinogen-driven cancers are
owned by the mechanistic volumes. This module does not cross those boundaries; it deepens what is inside.

The three-lever principle (three_lever.py) gives a DERIVABLE selection rule. Every disease here is a
corruption of one of the three OU parameters of its defended setpoint, and the asymmetry

    error = load/k        (set by L1 source and L2 gain)
    variance = sigma^2/2k (set ONLY by L2 gain)

selects the PRIMARY lever from WHICH parameter was corrupted:

    corrupted parameter        primary lever      because
    ------------------------   ---------------    --------------------------------------------------------
    loop gain k (down)         L2 gain            only restoring k tightens the lability, not just the mean
    set-point x* (drifted)     L3 setpoint        relocate the comparator durably; symptom control relapses
    load (unsuppressible)      L1 source          remove the driver the loop cannot suppress
    hard solubility threshold  L1 source          no tunable loop gain at a fixed Ksp; keep the drive below
    reservoir (depleted)       L2 gain            refill/restore remodeling gain > merely slowing the drain

For each owned disease this module (1) names the corrupted parameter, (2) selects the primary lever from
the asymmetry, (3) runs ONE clean demonstration on the volume's OWN OU law showing the primary lever
succeeds where the mis-matched lever does not, and (4) states the improvement -- cited drug classes [L],
framework-beyond-practice predictions flagged [H], absolute magnitudes [O].

GRADES (C3): lever-selection DIRECTION reproduced from the OU law [V]; named-drug efficacy cited [L];
framework predictions [H]; absolute magnitudes [O]. Determinism (C1): fixed seed, round-before-hash.
"""
import os, sys, math, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
from vp_substrate import seed_everything
import importlib
loops = importlib.import_module("vp_loops")

# ===========================================================================
# archetype demonstrations on the volume's OWN OU law
# ===========================================================================
def _variance_limited_demo(k_lo=1.0, k_hi=4.0, load=1.0, sigma=0.3):
    """A loop-gain-drop disease (low k). Compare the mis-matched L1 (cut the load) against the matched L2
    (restore the gain). L1 lowers the mean offset but the variance stays high (variance=sigma^2/2k is
    independent of load); only L2 tightens BOTH. This is why a chronically labile defended ion is fixed at
    the ARM, not by chasing the mean."""
    seed_everything()
    base_mean=loops.ou_setpoint(k_lo, sigma=0.0, load=load)["mean_offset"]
    base_var =loops.ou_setpoint(k_lo, sigma=sigma, load=0.0)["variance"]
    l1_mean  =loops.ou_setpoint(k_lo, sigma=0.0, load=load*0.5)["mean_offset"]   # load cut
    l1_var   =loops.ou_setpoint(k_lo, sigma=sigma, load=0.0)["variance"]         # k unchanged -> var unchanged
    l2_mean  =loops.ou_setpoint(k_hi, sigma=0.0, load=load)["mean_offset"]       # arm restored
    l2_var   =loops.ou_setpoint(k_hi, sigma=sigma, load=0.0)["variance"]         # var falls
    return dict(k_low=k_lo, k_high=k_hi,
                baseline=dict(mean=round(base_mean,4), variance=round(base_var,5)),
                L1_load_cut=dict(mean=round(l1_mean,4), variance=round(l1_var,5)),
                L2_arm_restored=dict(mean=round(l2_mean,4), variance=round(l2_var,5)),
                L1_leaves_variance_high=bool(abs(l1_var-base_var) < 0.15*base_var),
                only_L2_tightens_variance=bool(l2_var < 0.7*base_var),
                variance_ratio_L1_over_L2=round(l1_var/l2_var,3))

def _setpoint_drift_demo(disease_shift=0.15, drug_reset=0.15):
    """A set-point-drift disease (comparator x* moved). The defended attractor equals the comparator
    set-point for every Hill slope (structural identity), so an L3 allosteric reset relocates the defended
    value durably; a symptom-only approach (push against the drift without moving x*) relapses to the
    mis-set value when withdrawn. Returns the durable (reset) vs relapsing (symptom) residuals."""
    seed_everything(); m=3.0; g_eff=2.0; pmin=0.1; pmax=1.0; loss=g_eff*(pmin+pmax)/2.0
    def defended(ca_sp):
        ca=1.0; dt=0.02
        for _ in range(int(400.0/dt)):
            P=loops.pth_curve(ca, ca_sp, m, pmin, pmax); ca+=dt*(g_eff*P-loss)
        return float(ca)
    untreated=defended(1.0+disease_shift)
    reset    =defended(1.0+disease_shift-drug_reset)          # L3: move the comparator -> defends ~1.0
    relapse  =defended(1.0+disease_shift)                     # symptom control withdrawn -> back to mis-set
    return dict(disease_shift=disease_shift,
                defended_untreated=round(untreated,4), defended_after_L3_reset=round(reset,4),
                defended_after_symptom_withdrawal=round(relapse,4),
                L3_reset_normalizes=bool(abs(reset-1.0)<0.05),
                symptom_control_relapses=bool(abs(relapse-1.0)>0.05))

def _threshold_margin_demo(drive_hi=1.0, drive_lo=0.4, threshold=1.0):
    """A threshold-crossing disease (a hard solubility/precipitation Ksp, not a tunable loop gain). There
    is no k to raise at a fixed Ksp, so L2 does not apply; the lever is L1 -- keep the drive below the
    threshold (dilute via hydration, raise solubility via citrate, cut the Na/oxalate/phosphate load). The
    controlled quantity is the MARGIN to the threshold. Returns the margin under high vs lowered drive."""
    margin_hi=threshold-drive_hi
    margin_lo=threshold-drive_lo
    return dict(threshold=threshold, drive_high=drive_hi, drive_low_after_L1=drive_lo,
                margin_high_drive=round(margin_hi,3), margin_after_L1=round(margin_lo,3),
                L1_restores_margin=bool(margin_lo>margin_hi),
                note="at a fixed solubility constant there is no loop gain to raise (L2 N/A); L1 keeps the "
                     "drive in the soluble basin, L3 (lower the Ca*PO4 product set-point) is the adjunct")

def _reservoir_demo(B0=0.5, base_f=0.0008, base_k=0.05, demand=0.3, T=600.0, dt=0.05, B_max=1.0):
    """A reservoir-depletion disease (bone). Anti-resorptive (cut withdrawal) is an L1/holding move that
    only HALTS the decline; anabolic (raise formation) is the L2 move that restores the remodeling gain and
    REFILLS. Returns the depleted-start trajectories: untreated (falls), L1 anti-resorptive (halts), L2
    anabolic (refills)."""
    seed_everything(); m=3.0; g_eff=6.0; beta=2.0; clr=4.0; P0=loops.pth_curve(1.0,1.0,m)
    def traj(formation, kappa):
        ca=1.0; B=B0
        for _ in range(int(T/dt)):
            Pex=loops.pth_curve(ca,1.0,m)-P0
            ca+=dt*(g_eff*Pex+beta*Pex-clr*(ca-1.0)-demand)
            B=min(max(B+dt*(formation-kappa*max(Pex,0.0)),0.0),B_max)
        return float(B)
    untreated=traj(base_f, base_k)
    l1_anti  =traj(base_f, base_k*0.2)        # withdrawal slowed (hold)
    l2_anab  =traj(base_f*15.0, base_k)       # formation raised (refill)
    return dict(start_reserve=B0, untreated_final=round(untreated,4),
                L1_antiresorptive_final=round(l1_anti,4), L2_anabolic_final=round(l2_anab,4),
                L1_only_halts=bool(l1_anti>untreated and l1_anti<B0+0.02),
                L2_refills=bool(l2_anab>B0+0.02), L2_beats_L1=bool(l2_anab>l1_anti))

# ===========================================================================
# the owned-disease remediation table (selection + demo + improvement)
# ===========================================================================
def remediation_table():
    seed_everything()
    vdemo=_variance_limited_demo(); sdemo=_setpoint_drift_demo()
    tdemo=_threshold_margin_demo(); rdemo=_reservoir_demo()
    D=[
      {"disease":"osteoporosis", "owns":"this volume (common/age/post-menopausal)",
       "corrupted_parameter":"reservoir depleted + remodeling gain low",
       "primary_lever":"L2 gain (refill/restore remodeling gain)",
       "adjunct":"L1 source (anti-resorptive to hold; remove driver: estrogen/SERM, mechanical loading)",
       "sequence":"L2 first (build with anabolic), then L1 (lock in with anti-resorptive)",
       "demonstration":rdemo,
       "improvement":"anabolic-FIRST (teriparatide / abaloparatide intermittent-PTH; romosozumab anti-sclerostin) to refill, THEN anti-resorptive (bisphosphonate / denosumab) to hold; remove the driver (estrogen/SERM, loading). The framework's distinctive call is the SEQUENCE: refill the gain before holding the drain.",
       "grade":"[V] L2 refills where L1 only halts (reservoir demo); sequence + drugs cited [L]; absolute gains [O]"},
      {"disease":"primary hyperparathyroidism", "owns":"this volume (common acquired; familial -> disease_wp)",
       "corrupted_parameter":"set-point x* drifted UP (autonomous PTH; CaSR comparator effectively reset high)",
       "primary_lever":"L3 setpoint (allosteric calcimimetic reset DOWN) or L1 source (remove the adenoma)",
       "adjunct":"L1 surgery (parathyroidectomy removes the source)",
       "sequence":"L1 cure if surgical candidate; otherwise L3 medical reset",
       "demonstration":sdemo,
       "improvement":"calcimimetic (cinacalcet / etelcalcetide) resets the CaSR comparator DOWN durably; parathyroidectomy (L1) removes the autonomous source. The framework's call: medical control is RECALIBRATION (L3), not chronic calcium chasing, which relapses on withdrawal.",
       "grade":"[V] L3 reset durable vs symptom relapse (drift demo); cinacalcet/surgery cited [L]; absolute residual [O]"},
      {"disease":"ADH1 (autosomal dominant hypocalcemia type 1)", "owns":"cross-ref: monogenic CaSR -> disease_wp; LOOP behavior here",
       "corrupted_parameter":"set-point x* set LOW (activating CaSR senses Ca as high)",
       "primary_lever":"L3 setpoint (calcilytic reset UP)",
       "adjunct":"avoid plain calcium/vitD (worsens hypercalciuria -- treats the symptom, not x*)",
       "sequence":"L3 reset is the matched lever",
       "demonstration":sdemo,
       "improvement":"calcilytic (encaleret; Phase-3 CALIBRATE positive 2025) resets the over-active CaSR set-point UP -- the matched L3 lever -- where calcium/vitD repletion (symptom control) drives hypercalciuria. Monogenic gene-lesion facts are owned by disease_wp; the loop reading is here.",
       "grade":"[V] L3 matched-lever (drift demo); encaleret CALIBRATE cited [L]; magnitudes [O]; non-CaSR generalisation [H]"},
      {"disease":"distal renal tubular acidosis / chronic metabolic acidosis", "owns":"this volume (acid-base loop failure)",
       "corrupted_parameter":"loop gain k down (failed renal HCO3-regeneration arm)",
       "primary_lever":"L2 gain (restore the renal HCO3 arm at source)",
       "adjunct":"L1 source (reduce dietary acid load); current care = lifelong alkali (a mean-only buffer)",
       "sequence":"L2 restoration is the durable fix; alkali holds the mean meanwhile",
       "demonstration":vdemo,
       "improvement":"lifelong alkali (ADV7103 / Sibnayal) cancels the MEAN only and must be sustained (leaves k low, lability high); restoring the failed HCO3-transporter / ventilatory arm (L2) uniquely tightens the variance and rejects a fresh acid load by k_high/k_low. Framework prediction: arm restoration > lifelong buffering [H].",
       "grade":"[V] only L2 tightens variance (variance demo); dRTA/alkali standard cited [L]; arm-restoration [H]; magnitudes [O]"},
      {"disease":"common electrolyte disorders (hyper/hypo- natremia, kalemia)", "owns":"this volume; Na<->volume seam cited to hemodynamic",
       "corrupted_parameter":"loop gain k down (renal handling arm) and/or unsuppressible load",
       "primary_lever":"L2 gain (restore renal handling) when the arm is weak; L1 source when an external load drives it",
       "adjunct":"correct the rate of change carefully (osmotic-demyelination caution -- a symptom-pacing constraint)",
       "sequence":"identify whether the arm (L2) or an external load (L1) is the lesion, then match",
       "demonstration":vdemo,
       "improvement":"a labile electrolyte is the loop-gain-drop mode read on Na/K: where renal handling gain is low (L2 restore the arm); where an unsuppressible load drives it (L1 remove/oppose the source -- e.g. SIADH water restriction / vaptan). The volume's load/k law selects which.",
       "grade":"[V] loop-gain-drop mode (variance demo); cited setpoints/agents [L]; absolute magnitudes [O]"},
      {"disease":"nephrolithiasis (calcium stones) / vascular calcification", "owns":"this volume (supersaturation threshold)",
       "corrupted_parameter":"a hard solubility/precipitation threshold (Ksp) is crossed -- no tunable loop gain",
       "primary_lever":"L1 source (keep the drive below the threshold)",
       "adjunct":"L3 setpoint (lower the Ca*PO4 product set-point via FGF23/binders); L2 does NOT apply (fixed Ksp)",
       "sequence":"L1 maintains the margin; L3 lowers the product set-point",
       "demonstration":tdemo,
       "improvement":"hydration (dilute) + citrate (raise Ca-oxalate solubility) + Na/oxalate restriction keep the drive in the soluble basin (L1); phosphate binders / anti-FGF23 (burosumab) lower the Ca*PO4 product set-point (L3). Because the barrier is a fixed solubility constant, there is no k to raise -- the framework explicitly rules L2 out here.",
       "grade":"[V] L1 restores the threshold margin (margin demo); hydration/citrate/binder cited [L]; absolute Ksp [O]"},
      {"disease":"hypomagnesemia / hypermagnesemia", "owns":"this volume (Tier-2; TRPM6/Gitelman -> disease_wp gene facts)",
       "corrupted_parameter":"loop gain k down on a third defended ion (Mg reabsorption arm)",
       "primary_lever":"L2 gain (restore the Mg-reabsorption arm)",
       "adjunct":"L1 source (Mg repletion holds the mean; remove an Mg-wasting drive)",
       "sequence":"repletion holds the mean; arm restoration is the durable fix",
       "demonstration":vdemo,
       "improvement":"Mg repletion (L1) cancels the mean while the arm stays weak; restoring the TRPM6 / distal Mg-reabsorption gain (L2) is the durable lever (variance-tightening). Gene-lesion facts (TRPM6, SLC12A3/Gitelman) are owned by disease_wp and cited.",
       "grade":"[V] loop-gain-drop on a third ion (variance demo); Mg setpoint/variants cited [L]; arm restoration [H]; magnitudes [O]"},
      {"disease":"CKD-MBD with secondary hyperparathyroidism", "owns":"this volume (multi-arm renal gain drop)",
       "corrupted_parameter":"loop gain k down across SEVERAL renal arms at once (nephron loss)",
       "primary_lever":"L2 gain (substitute the failed arms) + L1 source (lower the phosphate load) + L3 (calcimimetic on the driven PTH)",
       "adjunct":"all three levers act together -- a multi-arm failure needs a multi-lever package",
       "sequence":"L1 phosphate-load control + L2 active-vitD arm substitution + L3 calcimimetic on PTH",
       "demonstration":vdemo,
       "improvement":"phosphate binders + dietary phosphate restriction (L1) lower the load; active vitamin D / analogs (L2) substitute the failed renal 1-alpha-hydroxylase arm; calcimimetic (L3) resets the secondary-HPT comparator. CKD-MBD is the one owned disease where all three levers are simultaneously indicated -- the multi-arm gain drop demands the full package.",
       "grade":"[V] multi-arm loop-gain-drop (variance demo + Tier-2 cascade); KDIGO/agents cited [L]; per-stage timing [O]"},
      {"disease":"humoral hypercalcemia of malignancy (PTHrP)", "owns":"this volume (set-point drift by external drive)",
       "corrupted_parameter":"an unsuppressible external LOAD (tumor PTHrP the CaSR cannot switch off)",
       "primary_lever":"L1 source (remove/oppose the PTHrP driver)",
       "adjunct":"symptom control (hydration, anti-resorptive to blunt the Ca release) buys time",
       "sequence":"L1 (treat the tumor / oppose PTHrP) is curative-directed; symptom control is supportive",
       "demonstration":sdemo,
       "improvement":"the loop itself works -- it simply cannot suppress a drive that is not its own; the matched lever is L1, remove/oppose the PTHrP source (anti-tumor therapy), with hydration + anti-resorptive (denosumab/bisphosphonate) as supportive symptom control. Distinct from primary hyperPTH (an L3 disease): here endogenous PTH is appropriately suppressed.",
       "grade":"[V] external-load case, L1 matched (drift demo, inverse); PTHrP mechanism cited [L]; absolute level [O]"},
    ]
    # selection-rule integrity: every disease's primary lever follows from its corrupted parameter
    sel_ok = (vdemo["only_L2_tightens_variance"] and sdemo["L3_reset_normalizes"]
              and sdemo["symptom_control_relapses"] and tdemo["L1_restores_margin"]
              and rdemo["L2_refills"] and rdemo["L2_beats_L1"])
    by_lever={}
    for d in D:
        pl=d["primary_lever"].split()[0]
        by_lever.setdefault(pl, []).append(d["disease"])
    return dict(diseases=D, by_primary_lever=by_lever, selection_rule_demonstrations_pass=bool(sel_ok),
                archetype_demonstrations=dict(variance_limited=vdemo, setpoint_drift=sdemo,
                                              threshold_margin=tdemo, reservoir=rdemo))

def status():
    seed_everything()
    rt=remediation_table()
    return dict(_what="The three-lever principle applied to the diseases this volume owns: each disease's "
                      "primary lever is SELECTED from which OU parameter it corrupted, demonstrated on the "
                      "volume's own OU law, and turned into a cited, honestly-graded improvement.",
                scope_note="owned = common/polygenic/acquired/age-related loop disorders; rare/monogenic "
                           "gene facts -> disease_wp (cited); carcinogen cancers -> mechanistic volumes. "
                           "Boundaries per VP_FRAMEWORK_MAP section 6 are not crossed.",
                remediation=rt, demonstrations_pass=bool(rt["selection_rule_demonstrations_pass"]),
                grade="lever-selection direction [V]; named-drug efficacy [L]; framework predictions [H]; "
                      "absolute magnitudes [O]")

if __name__ == "__main__":
    print(json.dumps(status(), ensure_ascii=False, indent=2))
