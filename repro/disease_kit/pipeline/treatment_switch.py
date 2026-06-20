#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
treatment_switch.py  --  TREATMENT PATHWAY A: switch adjustment.

Generalises the analgesic three-lever logic to ANY emerged disease switch. Given the
emergence reading (which fixes the PATHOLOGICAL direction on the emergent axis) and the
disease's CITED therapeutic axes, it:

  1. derives the CORRECTIVE direction = oppose the pathology (push the axis back toward
     normal),
  2. for each candidate lever (a gene + how intervening on it moves the emergent axis),
     checks whether it CORRECTS (opposes pathology) or WORSENS it -- a consistency gate,
  3. anchors each corrective lever to a real validated/approved AGENT CLASS where one
     exists, and grades the mechanism link honestly,
  4. EMERGES the switch state concretely: healthy vs disease vs treated DWELL, so the
     "adjust the switch" claim is shown, not just asserted. The DIRECTION and the
     ORDERING (treated sits between disease and healthy) are forced [F]; the absolute
     MAGNITUDE of each shift is [O] (a runtime/Layer-2 quantity).

Lever vocabulary (the unifying frame -- raise/restore the emergent axis):
   reduce      : turn DOWN an over-active element (the GOF brake / runaway channel)
   potentiate  : open a gate stuck in the OFF basin (LOF channel)
   correct     : rescue a mis-folded/mis-trafficked protein toward function
   oppose      : boost an OPPOSING element that pushes the axis the healthy way
   replace     : supply a missing enzyme / cofactor / product (metabolic LOF)
   mimic       : supply a DIFFERENT molecule that does the missing element's FUNCTION
                 (not the element itself) -- e.g. emicizumab bridging FIXa/FX for absent FVIIIa
   restrain    : turn DOWN an over-driven accelerator (GOF accelerator)

FIREWALL (binding): a lever names a DIRECTION + a cited agent CLASS. It is NOT a dose, a
potency, an efficacy or safety claim, nor a recommendation to treat any individual.

Deterministic: pure arithmetic. stdlib + the in-package engine.
"""
import os, sys, json, math, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
ENGINE = os.path.join(ROOT, "engine")
for p in (ENGINE, os.path.join(ENGINE, "organism")):
    if p not in sys.path: sys.path.insert(0, p)
import vp_neuro_engine as VN

DIRINT = {"DOWN": -1, "UP": +1, "unchanged": 0}

# how each lever moves the emergent axis (sign), and whether it acts by lowering or
# raising the brake on the dwell engine (used for the concrete emergence below).
LEVER_AXIS_SIGN = {
    "reduce": +1,      # reduce an over-active brake -> axis UP
    "oppose": +1,      # boost an opposing accelerator -> axis UP
    "potentiate": +1,  # open a closed channel -> restore (axis UP toward function)
    "correct": +1,     # rescue protein -> restore function (axis UP)
    "replace": +1,     # supply missing product/enzyme -> restore (axis UP)
    "mimic": +1,       # supply a DIFFERENT molecule that performs the missing element's
                       #   FUNCTION (not the element itself) -> restore (axis UP). v0.13.0:
                       #   the cofactor-mimic class (emicizumab bridges FIXa-FX, doing FVIIIa's
                       #   job without being factor VIII -> works even past an anti-FVIII inhibitor).
                       #   Distinct from 'replace' (same molecule) and 'correct' (rescue the native
                       #   protein). Purely additive: no prior disease uses it -> all frozen hashes
                       #   stay drift 0 (the v0.4.0 axis-UP-branch deepening convention).
    "restrain": -1,    # restrain an over-driven accelerator -> axis DOWN
}


def corrective_direction(emergence):
    """The therapeutic goal: oppose the pathological direction on the emergent axis."""
    ps = emergence.get("primary_switch")
    if ps is None:
        return 0
    return -DIRINT.get(ps["emergent_axis_direction"], 0)


def evaluate_levers(emergence, therapeutic_axes):
    """therapeutic_axes: [ {lever, target_gene, push, agent_class, status, mechanism_grade, src} ]
       Returns each lever tagged CORRECTS / WORSENS / NEUTRAL against the pathology."""
    want = corrective_direction(emergence)        # +1 means we want the axis UP, etc.
    out = []
    for ax in therapeutic_axes:
        sign = LEVER_AXIS_SIGN.get(ax["lever"], 0)
        if want == 0 or sign == 0:
            verdict = "NEUTRAL"
        elif sign == want:
            verdict = "CORRECTS"
        else:
            verdict = "WORSENS"
        out.append({
            "lever": ax["lever"], "target_gene": ax["target_gene"],
            "push_direction": ax["push"], "axis_effect": "UP" if sign > 0 else ("DOWN" if sign < 0 else "none"),
            "verdict_vs_pathology": verdict,
            "agent_class": ax.get("agent_class"), "status": ax.get("status", "hypothesis"),
            "mechanism_grade": ax.get("mechanism_grade", "[O] mechanism link not derived"),
            "src": ax.get("src", ""),
        })
    # corrective levers first, then by approval status
    rank = {"approved": 0, "clinical": 1, "preclinical": 2, "hypothesis": 3}
    out.sort(key=lambda l: (0 if l["verdict_vs_pathology"] == "CORRECTS" else 1,
                            rank.get(l["status"], 9)))
    return out, want


def emerge_switch_states(primary_gamma, mechanism, delta=0.6, treat_frac=0.6, axis_dir="DOWN"):
    """Concrete DWELL emergence: healthy vs disease vs treated, on the SAME engine.

    The growth/output engine is dwell(gamma, brake)=gamma^1.5/(K+brake). The disease is a
    SHIFT of the effective brake; a treatment removes a fraction 'treat_frac' of that shift.
    The ORDERING is forced (treated sits strictly between disease and healthy); the magnitudes
    delta / treat_frac are documented modelling choices and the realised values are [O].

    axis_dir tells the model WHICH WAY the disease pushes the emergent axis:
      * "DOWN" (deficiency / loss-of-output / over-active brake) -> disease RAISES the effective
        brake (+delta) -> disease dwell BELOW healthy; treatment relaxes a fraction back up.
        This is the v0.2.0 model and is returned byte-for-byte unchanged (loss-of-function and
        over-active-brake diseases: CF, PKU, Gaucher, SMA, DMD, achondroplasia, HD-as-brake, ...).
      * "UP"   (gain-of-toxicity / dosage-excess / over-drive) -> disease LOWERS the effective
        brake (fractional) -> disease dwell ABOVE healthy (the axis OVER-shoots); the corrective
        lever RESTRAINS it back down a fraction toward normal. Used for toxic-accumulation and
        dosage-excess diseases (tyrosinaemia, Wilson, MECP2-duplication) whose approved/lead
        therapy removes or restrains the excess rather than restoring a lost function.

    The (γ^1.5)/(K+brake) form itself is the LOCKED dwell engine and is never altered; only the
    choice of effective brake for disease/treated differs by axis direction. Returns the three
    emergent dwell values + an axis-appropriate ordering check.
    """
    K = 0.6; brake0 = 0.5

    if axis_dir == "UP":
        # over-shoot model: disease relaxes the brake (more output/burden); treatment restrains
        # a fraction back toward normal. Multiplicative so the brake stays strictly positive
        # without a clamp (brake0*(1-delta) with delta<1). Ordering healthy < treated < disease
        # is forced [F]; the realised magnitudes are [O] (documented modelling choice).
        brake_disease = brake0 * (1.0 - delta)
        brake_treated = brake0 * (1.0 - delta * (1.0 - treat_frac))
        d_health  = VN.dwell(primary_gamma, brake0, K)
        d_disease = VN.dwell(primary_gamma, brake_disease, K)
        d_treated = VN.dwell(primary_gamma, brake_treated, K)
        ordered = (d_health < d_treated < d_disease)
        return {
            "dwell_healthy":  round(d_health, 5),
            "dwell_disease":  round(d_disease, 5),
            "dwell_treated":  round(d_treated, 5),
            "axis_direction": "UP",
            "ordering_healthy_lt_treated_lt_disease": bool(ordered),
            "restraint_fraction_of_excess": round(
                (d_disease - d_treated) / max(1e-9, (d_disease - d_health)), 4),
            "modelling": {"delta": delta, "treat_frac": treat_frac, "axis": "UP",
                          "grade": "[F] ordering forced (over-shoot) ; delta/treat_frac documented choices ; realised magnitude [O]"},
        }

    # ---- axis-DOWN (unchanged from v0.2.0; output is byte-identical to the frozen artifacts) ----
    if mechanism == "GOF":          # over-active brake -> higher effective brake -> less dwell
        brake_disease = brake0 + delta
        brake_treated = brake0 + delta * (1.0 - treat_frac)
    else:                            # LOF (accelerator/channel/enzyme) -> output deficit modelled as raised brake
        brake_disease = brake0 + delta
        brake_treated = brake0 + delta * (1.0 - treat_frac)
    d_health  = VN.dwell(primary_gamma, brake0, K)
    d_disease = VN.dwell(primary_gamma, brake_disease, K)
    d_treated = VN.dwell(primary_gamma, brake_treated, K)
    ordered = (d_disease < d_treated < d_health)
    return {
        "dwell_healthy":  round(d_health, 5),
        "dwell_disease":  round(d_disease, 5),
        "dwell_treated":  round(d_treated, 5),
        "ordering_disease_lt_treated_lt_healthy": bool(ordered),
        "recovery_fraction_of_deficit": round(
            (d_treated - d_disease) / max(1e-9, (d_health - d_disease)), 4),
        "modelling": {"delta": delta, "treat_frac": treat_frac,
                      "grade": "[F] ordering forced ; delta/treat_frac documented choices ; realised magnitude [O]"},
    }


def switch_treatment(emergence, therapeutic_axes):
    """Full pathway-A reading for one disease."""
    levers, want = evaluate_levers(emergence, therapeutic_axes)
    ps = emergence.get("primary_switch")
    states = None
    if ps is not None:
        pg = next((g["gamma"] for g in emergence["per_gene"] if g["gene"] == ps["gene"]), None)
        if pg is not None:
            states = emerge_switch_states(pg, ps["mechanism"], axis_dir=ps["emergent_axis_direction"])
    corrective = [l for l in levers if l["verdict_vs_pathology"] == "CORRECTS"]
    out = {
        "disease": emergence["disease"],
        "pathway": "A: switch adjustment",
        "pathology_axis_direction": None if ps is None else ps["emergent_axis_direction"],
        "corrective_axis_direction": {1: "UP", -1: "DOWN", 0: "n/a"}[want],
        "levers": levers,
        "n_corrective": len(corrective),
        "n_worsening": sum(1 for l in levers if l["verdict_vs_pathology"] == "WORSENS"),
        "lead_corrective_lever": corrective[0] if corrective else None,
        "switch_state_emergence": states,
        "firewall": ("levers are DIRECTION + cited agent CLASS; not dose/potency/efficacy/safety, "
                     "not a recommendation to treat any individual."),
    }
    out["determinism_sha"] = hashlib.sha256(
        json.dumps(out, sort_keys=True).encode()).hexdigest()[:12]
    return out


def print_treatment(t):
    print("-" * 84)
    print(f"  TREATMENT A (switch adjustment): {t['disease']}")
    print(f"  pathology axis = {t['pathology_axis_direction']}  ->  corrective axis = {t['corrective_axis_direction']}")
    print("-" * 84)
    print(f"  {'lever':11} {'target':8} {'axis':5} {'verdict':9} {'status':11} agent class")
    for l in t["levers"]:
        print(f"  {l['lever']:11} {l['target_gene']:8} {l['axis_effect']:5} "
              f"{l['verdict_vs_pathology']:9} {l['status']:11} {l['agent_class'] or '-'}")
    if t["switch_state_emergence"]:
        s = t["switch_state_emergence"]
        print(f"\n  DWELL emergence (relative size):  disease {s['dwell_disease']}  <  "
              f"treated {s['dwell_treated']}  <  healthy {s['dwell_healthy']}   "
              f"[ordered={s['ordering_disease_lt_treated_lt_healthy']}]")
        print(f"    recovers {int(100*s['recovery_fraction_of_deficit'])}% of the deficit "
              f"(direction forced; magnitude [O])")
    if t["lead_corrective_lever"]:
        L = t["lead_corrective_lever"]
        print(f"\n  LEAD CORRECTIVE LEVER: {L['lever']} {L['target_gene']} "
              f"via {L['agent_class']} ({L['status']})  {L['mechanism_grade']}")
    print(f"  determinism sha={t['determinism_sha']}")


if __name__ == "__main__":
    # standalone demo wiring (achondroplasia) -- requires the emergence first
    sys.path.insert(0, HERE)
    import emerge_disease as ED
    spec = {
        "disease": "Achondroplasia", "omim": "100800",
        "summary": "FGFR3 GOF over-activates the growth-plate brake.",
        "emergent_axis": "endochondral bone elongation",
        "causal_genes": [{"gene": "FGFR3", "role": "brake", "mechanism": "GOF",
                          "note": "G380R", "src": "Shiang 1994 Cell 78:335"}],
    }
    em = ED.emerge_disease(spec, offline=True)
    axes = [
        {"lever": "oppose", "target_gene": "NPR2", "push": "boost CNP/NPR2-cGMP, opposes the FGFR3/MAPK brake",
         "agent_class": "CNP analogue (vosoritide)", "status": "approved",
         "mechanism_grade": "[O] downstream brake-suppression link not derived from sequence",
         "src": "Savarirayan 2020 Lancet 396:684; vosoritide FDA/EMA 2021"},
        {"lever": "reduce", "target_gene": "FGFR3", "push": "reduce FGFR3 tyrosine-kinase signalling",
         "agent_class": "FGFR3-TKI / soluble FGFR3 decoy (infigratinib, recifercept — investigational)",
         "status": "clinical",
         "mechanism_grade": "[O] potency/selectivity not asserted",
         "src": "Legeai-Mallet lineage; infigratinib paediatric program"},
    ]
    t = ED.print_reading(em) or __import__("builtins")
    tt = switch_treatment(em, axes)
    print_treatment(tt)
