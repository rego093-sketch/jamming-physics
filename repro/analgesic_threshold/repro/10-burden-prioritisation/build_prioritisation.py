#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_prioritisation.py  —  M10 (v2): burden-weighted prioritisation of TARGETS (not drugs).

The user's goal is to reduce the MAXIMUM suffering for the GREATEST number of people, via targets.
So this is a small, transparent ranking that combines three CITED tiers —
  B = burden        (prevalence x severity of the indication the target serves; GBD-anchored)
  U = unmet need    (how poorly current therapy serves that indication)
  D = druggability  (clinical validation / tractability evidence for the target)
each on a cited 1..5 scale, under DECLARED weights, to surface the Tier-1 burden leaders.

THE WEIGHTS ARE DECLARED, NOT TUNED TO A DESIRED ANSWER:
  w_B=0.40, w_U=0.35, w_D=0.25  — burden and unmet-need lead (that is the stated goal: most
  suffering, most people); druggability is included so the ranking favours tractable directions
  but cannot let mechanistic elegance override need. score = w_B*B + w_U*U + w_D*D  (range 1..5).

HONESTY (binding):
  - B/U/D are CITED Layer-2 tiers; the weights are an explicit editorial choice. The ranking is
    therefore [F] from cited tiers + declared weights — NOT a [V] engine output.
  - The engine read's place in the map (lever, gamma-|h_sp|) is carried ALONGSIDE each target as
    structural context. It is NOT folded into the clinical priority score: gamma-|h_sp| is a
    promoter-stiffness read, not a clinical magnitude, and the firewall forbids equating them.
  - This ranks READS/TARGETS, not drugs. No molecule, dose, efficacy, or safety is ranked here.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 build_prioritisation.py   -> expected/priority_ranking.json
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.normpath(os.path.join(HERE, "..", "03-threshold-map", "expected", "threshold_map.json"))

# DECLARED weights (explicit; sum = 1.0). Burden- and unmet-need-leading, per the stated goal.
WEIGHTS = {"B": 0.40, "U": 0.35, "D": 0.25}

# CITED tiers per target (B,U,D in 1..5) with a one-line basis. actionable=False for the
# developmental master and the context/comparator arm (read for contrast, not recommended).
TIERS = {
  # --- Tier-1 burden leaders: musculoskeletal (NGF / Na_V / alpha2delta) ---
  "NGF":     dict(B=5, U=4, D=4, actionable=True,
                  cite="GBD: musculoskeletal is the #1 YLD burden (LBP ~619M 2020, OA ~500M); anti-NGF Phase-III, RPOA caveat (Lane 2010 NEJM)"),
  "NTRK1":   dict(B=5, U=4, D=3, actionable=True,
                  cite="Same NGF->TrkA axis; TrkA inhibition carries CNS/oncology selectivity caveats (Indo 1996)"),
  "SCN9A":   dict(B=4, U=5, D=4, actionable=True,
                  cite="Neuropathic + channelopathy; opioid-resistant, poorly served; Na_V1.7 genetically validated (Cox 2006)"),
  "SCN10A":  dict(B=4, U=5, D=5, actionable=True,
                  cite="Acute/peripheral; first new non-opioid class in 25y, FDA-approved (suzetrigine 2025-01-30)"),
  "CACNA2D1":dict(B=4, U=4, D=5, actionable=True,
                  cite="Neuropathic + very broad adjuvant use; gabapentinoids approved but modest efficacy + misuse (Field 2006)"),
  # --- Tier-1: migraine (CGRP axis) ---
  "CALCA":   dict(B=5, U=3, D=5, actionable=True,
                  cite="Migraine ~1B people; gepants + anti-CGRP mAbs approved (de-risked); non-responders remain (Edvinsson 2018)"),
  "CALCRL":  dict(B=5, U=3, D=5, actionable=True,
                  cite="CGRP receptor; erenumab/gepant target, approved class (McLatchie 1998)"),
  "RAMP1":   dict(B=5, U=3, D=4, actionable=True,
                  cite="CGRP receptor specificity component; small-molecule tractable (McLatchie 1998)"),
  "CALCB":   dict(B=4, U=3, D=3, actionable=True,
                  cite="beta-CGRP minor isoform of the validated migraine axis (Russell 2014)"),
  # --- Tier-1: neuropathic (Na_V1.3 / Ca_V3.2 / K_V7) ---
  "SCN3A":   dict(B=4, U=5, D=3, actionable=True,
                  cite="Neuropathic; Na_V1.3 re-expressed after nerve injury; preclinical (Hains 2003)"),
  "CACNA1H": dict(B=4, U=5, D=3, actionable=True,
                  cite="Neuropathic T-type Ca_V3.2; early-stage (Bourinet 2005)"),
  "KCNQ2":   dict(B=4, U=4, D=3, actionable=True,
                  cite="Neuropathic/excitability; retigabine withdrawn so direction valid but molecule caveats (Wang 1998)"),
  "KCNQ3":   dict(B=4, U=4, D=3, actionable=True,
                  cite="M-current partner of K_V7.2 (Wang 1998)"),
  "KCNQ5":   dict(B=3, U=4, D=2, actionable=True,
                  cite="Peripheral M-current component; early-stage (Lerche 2000)"),
  # --- Tier-2: visceral / inflammatory / cold ---
  "P2RX3":   dict(B=3, U=4, D=4, actionable=True,
                  cite="Visceral/cough/endometriosis; gefapixant approved for chronic cough (Cockayne 2000)"),
  "TRPV1":   dict(B=3, U=3, D=4, actionable=True,
                  cite="Inflammatory; capsaicin 8% patch approved; antagonist hyperthermia caveat (Caterina 1997)"),
  "TRPA1":   dict(B=3, U=3, D=3, actionable=True,
                  cite="Inflammatory/irritant transducer; clinical programmes (Story 2003)"),
  "CACNA1B": dict(B=3, U=4, D=4, actionable=True,
                  cite="Severe/refractory; ziconotide approved but intrathecal-only limits reach (Snutch 2005)"),
  "ASIC3":   dict(B=3, U=3, D=2, actionable=True,
                  cite="Muscle/inflammatory acid sensing; preclinical (Sutherland 2001)"),
  "TRPM8":   dict(B=2, U=3, D=3, actionable=True,
                  cite="Cold allodynia (narrower); human cold-pain trial (Bautista 2007)"),
  "ASIC1":   dict(B=2, U=3, D=2, actionable=True,
                  cite="Broader CNS expression (less peripheral-selective); preclinical (Waldmann 1997)"),
  "SCN11A":  dict(B=3, U=4, D=2, actionable=True,
                  cite="Channelopathy/neuropathic (narrower); hard to express in vitro (Dib-Hajj 1998)"),
  # --- developmental master (not an acute target) ---
  "PRDM12":  dict(B=5, U=4, D=1, actionable=False,
                  cite="Nociceptor master TF; developmental, not an acute drug target (Chen 2015)"),
  # --- context / comparators (read for contrast; the logic routes AWAY from reward) ---
  "OPRM1":   dict(B=4, U=4, D=5, actionable=False,
                  cite="COMPARATOR: mu-opioid — the reward-engaging axis this design routes AWAY from (Matthes 1996)"),
  "OPRK1":   dict(B=3, U=4, D=3, actionable=False,
                  cite="COMPARATOR: peripheral kappa, non-reward direction (dysphoria caveat) (Stein 2013)"),
  "OPRD1":   dict(B=3, U=3, D=3, actionable=False,
                  cite="COMPARATOR: delta-opioid (Gaveriaux-Ruff 2011)"),
  "CNR2":    dict(B=3, U=3, D=3, actionable=False,
                  cite="COMPARATOR: peripheral CB2, non-psychoactive direction (Guindon 2008)"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["D"]*t["D"], 4)

def build():
    m = json.load(open(MAP))
    by_gene = {e["gene"]: e for e in m["entries"]}
    hsp_rank = {g: i+1 for i, g in enumerate(m["order_by_spinodal_desc"])}  # 1 = stiffest read

    rows = []
    for gene, t in TIERS.items():
        e = by_gene[gene]
        rows.append({
            "gene": gene,
            "lever": e["lever"],
            "channel_or_protein": e["channel"] or e.get("protein"),
            "B_burden": t["B"], "U_unmet": t["U"], "D_druggability": t["D"],
            "priority_score": score(t),
            "actionable": t["actionable"],
            # the read's place in the map, carried as STRUCTURAL context (NOT in the score):
            "map_place": {"gamma_h_sp": e["spinodal_h_sp"], "h_sp_rank": hsp_rank[gene]},
            "burden_tier_cited": e["burden_tier"],
            "tier_basis_cited": t["cite"],
            "grade": "[F] from cited B/U/D tiers + declared weights (Layer-2 ranking, not a [V] engine output)",
        })

    actionable = sorted([r for r in rows if r["actionable"]],
                        key=lambda r: (-r["priority_score"], -r["map_place"]["gamma_h_sp"], r["gene"]))
    for i, r in enumerate(actionable):
        r["rank"] = i + 1
    comparators = sorted([r for r in rows if not r["actionable"]],
                         key=lambda r: (-r["priority_score"], r["gene"]))

    # informational: which declared burden-leader clusters surface near the top
    top_quartile = {r["gene"] for r in actionable[:max(1, len(actionable)//4)]}
    clusters = {
        "musculoskeletal (NGF/Na_V/alpha2delta)": ["NGF", "NTRK1", "SCN9A", "SCN10A", "CACNA2D1"],
        "migraine (CGRP axis)":                   ["CALCA", "CALCRL", "RAMP1", "CALCB"],
        "neuropathic (Na_V1.3/Ca_V3.2/K_V7)":     ["SCN3A", "CACNA1H", "KCNQ2", "KCNQ3"],
    }
    surfaced = {name: sorted(set(genes) & top_quartile) for name, genes in clusters.items()}

    return {
        "title": "Burden-weighted prioritisation of READS/TARGETS (not drugs)",
        "method": "score = w_B*B + w_U*U + w_D*D over cited 1..5 tiers; deterministic sort by score, "
                  "tie-break by gamma-|h_sp| then gene name.",
        "weights_declared": WEIGHTS,
        "weights_sum": round(sum(WEIGHTS.values()), 6),
        "label": "This is a prioritisation of TARGETS/READS, NOT a ranking of drugs, doses, or efficacy.",
        "firewall_note": ("gamma-|h_sp| is shown as the structural read's place in the map and is NOT folded "
                          "into the clinical priority score (it is a promoter-stiffness read, not a clinical magnitude)."),
        "n_actionable": len(actionable), "n_comparators": len(comparators),
        "ranking_actionable": actionable,
        "comparators_context": comparators,
        "tier1_clusters_surfaced_in_top_quartile": surfaced,
    }

if __name__ == "__main__":
    out = build()
    json.dump(out, open(os.path.join(HERE, "expected", "priority_ranking.json"), "w"), indent=1)
    print("M10 burden-weighted prioritisation (TARGETS, not drugs)")
    print(f"  weights (declared): {out['weights_declared']}  sum={out['weights_sum']}")
    print(f"  {'#':>2} {'gene':9} {'lev':10} {'B':>1} {'U':>1} {'D':>1} {'score':>5}  {'|h_sp|rank':>9}  basis")
    for r in out["ranking_actionable"]:
        print(f"  {r['rank']:>2} {r['gene']:9} {r['lever']:10} {r['B_burden']} {r['U_unmet']} {r['D_druggability']} "
              f"{r['priority_score']:5.2f}  {r['map_place']['h_sp_rank']:>9}  {r['tier_basis_cited'][:54]}")
    print("  comparators (read for contrast, routed away from):",
          ", ".join(r["gene"] for r in out["comparators_context"]))
    print("  Tier-1 clusters surfaced in top quartile:")
    for name, genes in out["tier1_clusters_surfaced_in_top_quartile"].items():
        print(f"    - {name}: {genes}")
    print("wrote expected/priority_ranking.json")
