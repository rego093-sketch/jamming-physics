#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
chem_toolkit.py  --  the VP-chemistry DRUG-DEVELOPMENT toolkit (pathway B).

Inherited from the VP Chemistry & EM whitepaper (handoff_chemistry v1.8). It does
NOT do docking, QSAR, or ADMET. It provides the parameter-free VP-chemistry
PRIMITIVES that let a medicinal-chemistry hypothesis be DIRECTIONED and sanity-
checked thermodynamically:

  1. delta_G(dH, dS, T)         -- equilibrium feasibility  dG = dH - T dS  (VP CH.2).
                                   Sign decides spontaneity; this is the gate on
                                   "will this binding / reaction proceed at body T?".
  2. sabatier_score(dG, dG_opt) -- the catalyst-as-matchmaker / volcano principle
                                   (VP CH.5, Newns-Anderson d-band picture): a binder
                                   must hold firmly enough to ACT yet loosely enough
                                   to RELEASE. Affinity that is too weak OR too strong
                                   is sub-optimal; the best sits in a window near dG_opt.
  3. tetrahedral_angle()        -- molecular shape from sphere geometry,
                                   arccos(-1/3) = 109.47 deg, zero free parameters (VP CH.2).
  4. body_T()                   -- 310.15 K (37 C), the locked physiological temperature.

HONESTY (binding):
  These are FEASIBILITY / DIRECTION reads, parameter-free where marked [F]. They are
  NOT binding affinities (Kd/IC50), NOT potencies, NOT doses, NOT selectivity, NOT
  efficacy or safety. A real dH/dS for a specific ligand is an EXTERNAL measured input
  [CAL]; absent that, the toolkit reports the STRUCTURE of the feasibility question and
  flags the missing magnitude [O]. No value here is tuned to a target.

Deterministic: pure arithmetic. stdlib only.
"""
import math

R_KCAL = 1.987204258640832e-3   # gas constant, kcal/(mol*K) -- physical constant [CAL]

def body_T():
    """Locked physiological temperature: 37 C = 310.15 K."""
    return 310.15

def tetrahedral_angle():
    """sp3 / maximally-separated-points-on-a-sphere bond angle. [F] zero free parameters."""
    return math.degrees(math.acos(-1.0/3.0))   # 109.4712...

def delta_G(dH_kcal, dS_cal_per_K, T=None):
    """Gibbs free energy  dG = dH - T*dS  (dS given in cal/mol/K, converted to kcal).
       Returns dict(dG_kcal, spontaneous, T). dH/dS are EXTERNAL measured inputs [CAL];
       the FORM is [F]. Spontaneous (favourable) iff dG < 0."""
    if T is None: T = body_T()
    dG = dH_kcal - T * (dS_cal_per_K / 1000.0)
    return {"dG_kcal_per_mol": round(dG, 4), "spontaneous": bool(dG < 0.0), "T_K": T,
            "grade": "[F] form (dG=dH-TdS); dH,dS are [CAL] external measured inputs"}

def keq_from_dG(dG_kcal, T=None):
    """Equilibrium constant from dG:  K = exp(-dG / RT). Feasibility magnitude proxy.
       K>1 (dG<0) favours the bound/product state. [F] form; dG is [CAL]-grounded."""
    if T is None: T = body_T()
    return {"Keq": round(math.exp(-dG_kcal / (R_KCAL * T)), 6),
            "favoured_state": "bound/product (K>1)" if dG_kcal < 0 else "free/reactant (K<1)",
            "grade": "[F] form; dG is [CAL]"}

def sabatier_score(dG_bind_kcal, dG_opt_kcal=-9.0, width=3.0):
    """The matchmaker / volcano principle (VP CH.5). A binder is best when its binding
       free energy sits NEAR the optimum dG_opt (firm enough to act, loose enough to
       release). Returns a 0..1 score = exp(-((dG_bind - dG_opt)/width)^2): 1.0 at the
       apex, falling off for binding that is too WEAK (dG less negative) or too STRONG
       (dG more negative). dG_opt/width are documented modelling choices [F]; the
       per-ligand dG_bind is a [CAL]/[O] external quantity.

       INTERPRETATION ONLY: this scores the DIRECTION of a binding-window hypothesis.
       It is NOT a Kd, IC50, potency, or success probability."""
    z = (dG_bind_kcal - dG_opt_kcal) / width
    score = math.exp(-z * z)
    if dG_bind_kcal > dG_opt_kcal + width:
        regime = "too weak (will not hold/activate the target)"
    elif dG_bind_kcal < dG_opt_kcal - width:
        regime = "too strong (will not release the product / poisons the site)"
    else:
        regime = "near-optimal window (matchmaker balance)"
    return {"sabatier_score": round(score, 4), "regime": regime,
            "dG_opt_kcal": dG_opt_kcal, "width_kcal": width,
            "grade": "[F] window form; dG_bind is [CAL]/[O] external; NOT a Kd/potency"}

def feasibility_card(name, dH_kcal=None, dS_cal_per_K=None, dG_bind_kcal=None, T=None):
    """One drug-feasibility card for a candidate interaction. Whatever EXTERNAL
       measured inputs are supplied get turned into the corresponding VP-chemistry
       feasibility read; whatever is missing is flagged [O] (the author's
       'no number -> hold it' discipline carried into chemistry)."""
    card = {"candidate": name, "T_K": T or body_T(), "reads": {}, "open": []}
    if dH_kcal is not None and dS_cal_per_K is not None:
        dg = delta_G(dH_kcal, dS_cal_per_K, T)
        card["reads"]["equilibrium"] = dg
        card["reads"]["Keq"] = keq_from_dG(dg["dG_kcal_per_mol"], T)
    else:
        card["open"].append("dH/dS not supplied -> equilibrium feasibility [O]")
    if dG_bind_kcal is not None:
        card["reads"]["binding_window"] = sabatier_score(dG_bind_kcal)
    else:
        card["open"].append("measured dG_bind not supplied -> Sabatier window [O]")
    card["firewall"] = ("VP-chemistry feasibility/geometry primitives only; NOT affinity, "
                        "potency, dose, selectivity, ADMET, efficacy, or safety.")
    return card


if __name__ == "__main__":
    print("VP chemistry drug-development toolkit (parameter-free primitives)")
    print(f"  tetrahedral bond angle = {tetrahedral_angle():.4f} deg  [F]")
    print(f"  body temperature       = {body_T()} K")
    # worked feasibility: a hypothetical inhibitor with a measured-style dH/dS and a dG_bind
    demo = feasibility_card("demo_inhibitor", dH_kcal=-12.0, dS_cal_per_K=-20.0, dG_bind_kcal=-9.5)
    import json; print(json.dumps(demo, indent=1))
