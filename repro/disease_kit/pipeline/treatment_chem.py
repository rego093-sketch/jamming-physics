#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
treatment_chem.py  --  TREATMENT PATHWAY B: drug development (VP chemistry).

Wraps engine/chem_toolkit.py into the disease pipeline. For a disease whose correction
is a SMALL MOLECULE (enzyme cofactor rescue, substrate reduction, channel potentiator,
metabolic product supply), it builds a VP-chemistry FEASIBILITY card per candidate:

  * equilibrium feasibility  dG = dH - T dS  at body temperature (will it proceed?),
  * the Sabatier binding-window read (firm enough to act, loose enough to release),
  * the parameter-free molecular-geometry primitive (tetrahedral 109.47 deg) for context.

The toolkit consumes EXTERNAL measured thermodynamics (dH, dS, dG_bind) where the author
supplies them, and FLAGS [O] whatever is missing -- the same "no number -> hold it"
discipline used everywhere else. It NEVER invents an affinity.

FIREWALL (binding): feasibility + geometry only. NOT affinity (Kd/IC50), potency, dose,
selectivity, ADMET, efficacy, or safety; NOT a recommendation to treat any individual.

Deterministic: pure arithmetic. stdlib + the in-package engine.
"""
import os, sys, json, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
ENGINE = os.path.join(ROOT, "engine")
if ENGINE not in sys.path: sys.path.insert(0, ENGINE)
import chem_toolkit as CT


def chem_treatment(disease, candidates):
    """candidates: [ {name, modality, dH_kcal?, dS_cal_per_K?, dG_bind_kcal?, rationale, status, src} ]
       Returns one feasibility card per candidate, plus a summary of what is [O]."""
    cards = []
    for c in candidates:
        card = CT.feasibility_card(
            c["name"], dH_kcal=c.get("dH_kcal"), dS_cal_per_K=c.get("dS_cal_per_K"),
            dG_bind_kcal=c.get("dG_bind_kcal"))
        card.update({
            "modality": c.get("modality", ""), "rationale": c.get("rationale", ""),
            "status": c.get("status", "hypothesis"), "src": c.get("src", ""),
        })
        cards.append(card)
    n_open = sum(len(c["open"]) for c in cards)
    out = {
        "disease": disease, "pathway": "B: drug development (VP chemistry feasibility)",
        "geometry_primitive_deg": round(CT.tetrahedral_angle(), 4),
        "body_T_K": CT.body_T(),
        "n_candidates": len(cards),
        "n_open_inputs": n_open,
        "candidates": cards,
        "firewall": ("VP-chemistry feasibility/geometry only; NOT affinity/potency/dose/selectivity/"
                     "ADMET/efficacy/safety; NOT a treatment recommendation."),
    }
    out["determinism_sha"] = hashlib.sha256(
        json.dumps(out, sort_keys=True).encode()).hexdigest()[:12]
    return out


def print_chem(t):
    print("-" * 84)
    print(f"  TREATMENT B (drug development, VP chemistry): {t['disease']}")
    print(f"  geometry primitive {t['geometry_primitive_deg']} deg [F] ; body T {t['body_T_K']} K")
    print("-" * 84)
    for c in t["candidates"]:
        line = f"  {c['candidate']:22} [{c['status']}] {c['modality']}"
        print(line)
        r = c["reads"]
        if "equilibrium" in r:
            eq = r["equilibrium"]
            print(f"      dG = {eq['dG_kcal_per_mol']} kcal/mol  -> "
                  f"{'spontaneous' if eq['spontaneous'] else 'non-spontaneous'}  "
                  f"(Keq={r['Keq']['Keq']})")
        if "binding_window" in r:
            bw = r["binding_window"]
            print(f"      Sabatier {bw['sabatier_score']}  -> {bw['regime']}")
        for o in c["open"]:
            print(f"      [O] {o}")
    print(f"  determinism sha={t['determinism_sha']}")


if __name__ == "__main__":
    # demo: PKU cofactor rescue (sapropterin/BH4) -- direction is supply the missing cofactor
    demo = chem_treatment("Phenylketonuria (demo)", [
        {"name": "sapropterin (BH4)", "modality": "PAH cofactor rescue (supply missing cofactor)",
         "dH_kcal": -8.0, "dS_cal_per_K": -10.0, "dG_bind_kcal": -7.5,
         "rationale": "BH4 stabilises residual PAH; restores partial pathway throughput",
         "status": "approved", "src": "Burton 2007; sapropterin (Kuvan) FDA 2007"},
        {"name": "large-neutral-AA mix", "modality": "substrate competition at the BBB",
         "rationale": "competes phenylalanine transport; thermodynamics not supplied here",
         "status": "clinical", "src": "Matalon 2006"},
    ])
    print_chem(demo)
