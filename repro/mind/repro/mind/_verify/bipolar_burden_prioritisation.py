#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bipolar_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420).

A small, transparent ranking that combines three CITED tiers --
  B = burden        (bipolar prevalence x severity / suicide burden; GBD-anchored, indication-level)
  U = unmet need    (how poorly current options serve that mechanistic sub-problem)
  G = genetic/druggability evidence (replicated BD-GWAS support + tractability of the target)
each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.
Burden/unmet-need lead (the stated goal: most suffering, most people); genetic+druggability is
included so the ranking favours replicated, tractable directions but cannot let mechanistic
elegance override need.

HONESTY (binding):
  - B/U/G are CITED Layer-2 tiers; the weights are an explicit editorial choice -> the ranking is
    [F] from cited tiers + declared weights, NOT a [V] engine output.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NOT folded into the priority score (the firewall forbids equating a promoter-stiffness read with
    a clinical magnitude).
  - this ranks READS/TARGETS, not drugs; no molecule, dose, efficacy, or safety is ranked.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 bipolar_burden_prioritisation.py   -> bipolar_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "bipolar_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis. actionable=False for the set-point/scaffold genes
# that are not acute pharmacological targets.
TIERS = {
  "CACNA1C": dict(B=5, U=5, G=5, actionable=True,
      cite="lead BD locus (Ferreira 2008; Sklar 2011; Cross-Disorder 2013); L-type Ca-blocker is a tractable DIRECTION"),
  "ANK3":    dict(B=5, U=5, G=5, actionable=False,
      cite="#2 BD locus (Ferreira 2008; Schulze 2009); AIS excitability set-point, not an acute drug target"),
  "GSK3B":   dict(B=5, U=4, G=4, actionable=True,
      cite="lithium's molecular target (Klein&Melton 1996; Stambolic 1996); mechanism-DIRECTION node, [O] link"),
  "CACNB2":  dict(B=4, U=4, G=5, actionable=True,
      cite="cross-disorder Ca-channel hit (Cross-Disorder 2013); auxiliary subunit of the CACNA1C target"),
  "SCN2A":   dict(B=4, U=4, G=4, actionable=True,
      cite="Na-blocker-stabiliser effector current (lamotrigine/valproate/carbamazepine class); neuropsychiatric Na gene"),
  "ARNTL":   dict(B=4, U=5, G=3, actionable=True,
      cite="core circadian clock; circadian disruption is a cited episode trigger; chronotherapy DIRECTION"),
  "CLOCK":   dict(B=4, U=5, G=3, actionable=True,
      cite="Clock-Delta19 mania-like, lithium-rescued (Roybal 2007); circadian DIRECTION"),
  "CACNA1D": dict(B=4, U=4, G=4, actionable=True,
      cite="L-type Ca family in the cross-disorder Ca signal (Cross-Disorder 2013)"),
  "NR3C1":   dict(B=4, U=4, G=3, actionable=True,
      cite="glucocorticoid receptor / HPA dysregulation; the M18 depressive-pole cortisol drive"),
  "GRIN2A":  dict(B=3, U=5, G=4, actionable=True,
      cite="NMDA subunit; glutamatergic mood axis (ketamine is an NMDA antagonist -- DIRECTION, not efficacy)"),
  "CRHR1":   dict(B=3, U=4, G=3, actionable=True,
      cite="CRF-receptor-1 atop the HPA stress cascade; stress-axis DIRECTION"),
  "PER2":    dict(B=3, U=4, G=3, actionable=True,
      cite="circadian period; lithium lengthens period (a direction-level link)"),
  "CACNA1I": dict(B=3, U=4, G=3, actionable=True,
      cite="T-type Ca_V3.3 in the SCZ/BD overlap (PGC-SCZ 2014)"),
  "KCNQ2":   dict(B=3, U=3, G=2, actionable=True,
      cite="M-current excitability brake; K_V7-opener DIRECTION (ezogabine template, molecule caveats)"),
  "KCNQ3":   dict(B=3, U=3, G=2, actionable=True,
      cite="M-current partner of K_V7.2"),
  "KCNB1":   dict(B=2, U=3, G=2, actionable=True,
      cite="delayed-rectifier excitability brake; broad direction, weaker BD-specific genetic anchor"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["G"]*t["G"], 4)

def build():
    m = json.load(open(MAP))
    by_gene = {e["gene"]: e for e in m["entries"]}
    hsp_rank = {g: i+1 for i, g in enumerate(m["order_by_spinodal_desc"])}
    rows = []
    for gene, t in TIERS.items():
        e = by_gene[gene]
        rows.append({
            "gene": gene, "lever": e["lever"],
            "channel_or_protein": e["channel"] or e.get("protein"),
            "B_burden": t["B"], "U_unmet": t["U"], "G_genetic_druggability": t["G"],
            "priority_score": score(t), "actionable": t["actionable"],
            "structural_context_NOT_in_score": {
                "gamma": e["gamma"], "spinodal_h_sp": e["spinodal_h_sp"],
                "h_sp_rank_stiffest_first": hsp_rank[gene]},
            "cite": t["cite"],
        })
    rows.sort(key=lambda r: (-r["priority_score"], r["gene"]))
    for i, r in enumerate(rows): r["rank"] = i + 1
    actionable = [r for r in rows if r["actionable"]]
    return {
        "title": "Burden-weighted bipolar TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420)",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). efficacy=0; "
                      "no molecule, dose, or patient is ranked."),
        "top_actionable_genes": [r["gene"] for r in actionable[:6]],
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "bipolar_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted bipolar TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  {'rank':4} {'gene':9} {'lev':12} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  context(|h_sp| rank)  basis")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        print(f"  {r['rank']:4} {r['gene']:9} {r['lever']:12} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  (h_sp#{c['h_sp_rank_stiffest_first']:2})  {r['cite'][:46]}")
    print(f"  top actionable: {res['top_actionable_genes']}")
