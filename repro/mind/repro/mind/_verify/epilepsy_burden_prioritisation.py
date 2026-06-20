#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
epilepsy_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420).

A small, transparent ranking that combines three CITED tiers --
  B = burden        (epilepsy prevalence x severity / SUDEP mortality; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem; ~30% of epilepsy is drug-resistant)
  G = genetic/druggability evidence (replicated epilepsy-gene support + tractability of the target)
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
    a clinical magnitude). The decoupling is the firewall made visible: the stiffest promoter
    (CACNA1H) ranks LOW on priority, and the top-priority burden gene (SCN1A) has nearly the SOFTEST
    promoter read -- so stiffness cannot be driving the order.
  - actionable=False marks genes whose lever DIRECTION is not a clean tractable target: SCN1A
    (the L1 Na-block direction is CONTRAINDICATED in Dravet) and KCNA1 (rarer, weak direct target).
  - this ranks READS/TARGETS, not drugs; no molecule, dose, efficacy, or safety is ranked.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 epilepsy_burden_prioritisation.py   -> epilepsy_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "epilepsy_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis. actionable=False where the lever DIRECTION is not a
# clean tractable target (SCN1A Dravet contraindication; KCNA1 rarer/weaker direct handle).
TIERS = {
  "SCN1A":   dict(B=5, U=5, G=5, actionable=False,
      cite="Dravet syndrome, high SUDEP; the most-replicated monogenic epilepsy gene (Claes 2001) -- but the L1 Na-block direction is CONTRAINDICATED in Dravet"),
  "TSC2":    dict(B=5, U=4, G=5, actionable=True,
      cite="tuberous sclerosis (severe, often drug-resistant epilepsy); tuberin is the Rheb-GAP; everolimus is an approved mTOR-inhibition DIRECTION (French 2016)"),
  "KCNQ2":   dict(B=5, U=4, G=5, actionable=True,
      cite="KCNQ2 encephalopathy + benign familial neonatal epilepsy; the M-current brake with the clearest mechanism and the retigabine K_V7-opener precedent (Weckhuysen 2012)"),
  "KCNT1":   dict(B=4, U=5, G=4, actionable=True,
      cite="malignant migrating partial seizures of infancy (EIMFS), extremely drug-resistant; quinidine is a KCNT1-GOF channel-block DIRECTION (Barcia 2012; Bearden 2014)"),
  "DEPDC5":  dict(B=4, U=4, G=5, actionable=True,
      cite="leading cause of familial focal epilepsy incl. focal cortical dysplasia; GATOR1/mTOR repressor -> mTOR-inhibition precision DIRECTION (Dibbens 2013)"),
  "TSC1":    dict(B=4, U=4, G=5, actionable=True,
      cite="tuberous sclerosis (hamartin); mTOR-inhibition DIRECTION (van Slegtenhorst 1997; French 2016)"),
  "SCN8A":   dict(B=4, U=4, G=4, actionable=True,
      cite="SCN8A gain-of-function epileptic encephalopathy (EIEE13); persistent-Na+ GOF is the Na-blocker-responsive case (Veeramah 2012)"),
  "SCN2A":   dict(B=4, U=4, G=4, actionable=True,
      cite="SCN2A gain-of-function early-infantile epileptic encephalopathy, Na-blocker responsive (Wolff 2017); shared neuropsychiatric Na gene"),
  "KCNB1":   dict(B=3, U=4, G=4, actionable=True,
      cite="KCNB1 developmental and epileptic encephalopathy; the major somatic delayed-rectifier brake (Torkamani 2014)"),
  "GRIN2A":  dict(B=3, U=4, G=4, actionable=True,
      cite="GRIN2A epilepsy-aphasia spectrum (Landau-Kleffner/CSWS); glutamatergic NMDA DIRECTION (Lemke 2013; Lesca 2013)"),
  "GABRA1":  dict(B=3, U=3, G=4, actionable=True,
      cite="GABA-A alpha1 in juvenile myoclonic epilepsy and DEE; the inhibitory GABAergic restoring current (Cossette 2002)"),
  "GABRG2":  dict(B=3, U=3, G=4, actionable=True,
      cite="GABA-A gamma2 in GEFS+/febrile seizures; the benzodiazepine-site inhibitory brake (Baulac 2001; Wallace 2001)"),
  "KCNQ3":   dict(B=3, U=3, G=4, actionable=True,
      cite="KCNQ3 benign familial neonatal epilepsy; M-current partner of K_V7.2 (Charlier 1998)"),
  "CACNA1A": dict(B=3, U=3, G=3, actionable=True,
      cite="P/Q-type Ca-channel in absence epilepsy + episodic-ataxia overlap (Jouvenceau 2001)"),
  "CACNA1H": dict(B=3, U=2, G=3, actionable=True,
      cite="T-type Ca_V3.2 in childhood absence epilepsy; ethosuximide T-type DIRECTION is established/low unmet (Chen 2003) -- note: STIFFEST promoter read yet LOW priority (decoupling)"),
  "KCNA1":   dict(B=2, U=3, G=3, actionable=False,
      cite="K_V1.1 episodic ataxia type 1 with epilepsy; rarer, weaker direct pharmacological handle (Browne 1994)"),
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
    # decoupling witnesses: the stiffest promoter and the top-priority gene
    stiffest = m["order_by_spinodal_desc"][0]
    top_priority = rows[0]["gene"]
    return {
        "title": "Burden-weighted epilepsy TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420)",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). efficacy=0; "
                      "no molecule, dose, or patient is ranked."),
        "decoupling_witness": {
            "stiffest_promoter_gene": stiffest,
            "stiffest_promoter_priority_rank": next(r["rank"] for r in rows if r["gene"] == stiffest),
            "top_priority_gene": top_priority,
            "top_priority_h_sp_rank_stiffest_first": next(
                r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                for r in rows if r["gene"] == top_priority),
            "reading": ("the stiffest promoter read (%s) sits LOW on priority while the top-priority burden gene "
                        "(%s) has one of the SOFTEST reads -- if promoter stiffness drove the ranking neither could "
                        "sit where it does. The decoupling is the firewall made visible." % (stiffest, top_priority)),
        },
        "top_actionable_genes": [r["gene"] for r in actionable[:6]],
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "epilepsy_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted epilepsy TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  {'rank':4} {'gene':9} {'lev':12} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  context(|h_sp| rank)  basis")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (set-point/contra)"
        print(f"  {r['rank']:4} {r['gene']:9} {r['lever']:12} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  (h_sp#{c['h_sp_rank_stiffest_first']:2})  {r['cite'][:42]}{act}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
    print(f"  top actionable: {res['top_actionable_genes']}")
