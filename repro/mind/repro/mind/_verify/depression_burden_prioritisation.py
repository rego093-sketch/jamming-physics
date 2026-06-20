#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
depression_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420).

A small, transparent ranking that combines three CITED tiers --
  B = burden        (depression prevalence x disability; depression is a leading global cause of
                     years-lived-with-disability; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem; ~30% of depression is treatment-
                     resistant; the up-stream HPA/neurotrophic/glutamate mechanisms address what the
                     first-line monoamine route misses)
  G = genetic/druggability evidence (replicated depression-gene/pharmacology support + tractability)
each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.
Burden/unmet-need lead (the stated goal: most suffering, most people); genetic+druggability is
included so the ranking favours replicated, tractable directions but cannot let mechanistic elegance
override need. Because depression's first-line route (monoamine) leaves a large drug-resistant
remainder, the UNMET-need tier pushes the up-stream HPA / neurotrophic / rapid-glutamate mechanisms
toward the top -- which is the substantive finding of this prioritisation, not a tuning artefact.

HONESTY (binding):
  - B/U/G are CITED Layer-2 tiers; the weights are an explicit editorial choice -> the ranking is
    [F] from cited tiers + declared weights, NOT a [V] engine output.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NOT folded into the priority score (the firewall forbids equating a promoter-stiffness read with
    a clinical magnitude). The decoupling is the firewall made visible: the STIFFEST promoter read
    (KCNQ2, a minor exploratory L2 lever) ranks LOW on priority, and the top-priority gene has a
    MID-RANGE read -- so stiffness cannot be driving the order.
  - actionable=False marks genes whose lever DIRECTION is not a clean tractable antidepressant target:
    KCNQ2/KCNQ3 (exploratory anhedonia direction only) and CACNA1C (cross-disorder set-point).
  - this ranks READS/TARGETS, not drugs; no molecule, dose, efficacy, or safety is ranked.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 depression_burden_prioritisation.py   -> depression_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "depression_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis. actionable=False where the lever DIRECTION is not a
# clean tractable antidepressant target (KCNQ exploratory; CACNA1C cross-disorder set-point).
TIERS = {
  "BDNF":    dict(B=5, U=5, G=5, actionable=True,
      cite="neurotrophic hypothesis convergence; the plasticity/un-chronification axis addresses the treatment-resistant mechanism the monoamine route misses (Duman 2006)"),
  "NTRK2":   dict(B=4, U=5, G=4, actionable=True,
      cite="the BDNF-receptor TrkB convergence node where the rapid glutamatergic route and the neurotrophic route meet (Autry 2011; Casarotto 2021)"),
  "FKBP5":   dict(B=4, U=5, G=5, actionable=True,
      cite="the most-replicated stress-axis gene; the HPA sub-axis addresses stress-driven, often treatment-resistant presentations the monoamine route misses (Klengel 2013)"),
  "GRIN2B":  dict(B=4, U=5, G=4, actionable=True,
      cite="the principal rapid-acting NMDA target; the glutamatergic route is the breakthrough direction for treatment-resistant presentations (Berman 2000; Li 2010)"),
  "NR3C1":   dict(B=4, U=5, G=4, actionable=True,
      cite="the glucocorticoid receptor; restoring HPA negative feedback is the up-stream stress-axis route distinct from monoamine reuptake (Pariante 2008)"),
  "CRHR1":   dict(B=4, U=4, G=4, actionable=True,
      cite="the CRH receptor; the up-stream stress-peptide route addressing HPA hyperdrive (Binder 2010)"),
  "SLC6A4":  dict(B=5, U=3, G=4, actionable=True,
      cite="the serotonin transporter; the canonical first-line monoaminergic target -- HIGH burden but LOWER unmet (many respond to the first-line route) (Lesch 1996)"),
  "SLC6A2":  dict(B=4, U=3, G=4, actionable=True,
      cite="the norepinephrine transporter; the noradrenergic monoaminergic target, second-line monoamine route (Ressler 1999)"),
  "MAOA":    dict(B=4, U=3, G=4, actionable=True,
      cite="monoamine oxidase A; the MAOI monoaminergic axis, an established but lower-unmet monoamine route (Shih 1999)"),
  "HTR2A":   dict(B=3, U=4, G=4, actionable=True,
      cite="the 5-HT2A receptor; a serotonergic-receptor route under active study (non-monotone direction) (Carhart-Harris 2021)"),
  "HTR1A":   dict(B=3, U=3, G=4, actionable=True,
      cite="the 5-HT1A receptor; the auto-/post-synaptic serotonergic-receptor adjunct route (Albert 2011)"),
  "GABRA1":  dict(B=3, U=4, G=4, actionable=True,
      cite="GABA-A alpha1; the neurosteroid-PAM route, an approved mechanism for peripartum depression (Meltzer-Brody 2018)"),
  "GRIN2A":  dict(B=3, U=4, G=4, actionable=True,
      cite="the cross-disorder NMDA partner subunit; carried with GluN2B as the glutamatergic route (Lemke 2013)"),
  "TPH2":    dict(B=3, U=3, G=3, actionable=True,
      cite="the brain serotonin-synthesis rate-limiting enzyme; the up-stream synthesis sub-axis (Zill 2004)"),
  "COMT":    dict(B=2, U=3, G=3, actionable=True,
      cite="catecholamine-catabolic enzyme; the prefrontal catecholamine Val158Met set-point modifier (Lachman 1996)"),
  "CACNA1C": dict(B=3, U=3, G=4, actionable=False,
      cite="the most-replicated cross-disorder calcium locus; a set-point gene shared across five disorders, NOT a clean antidepressant target (PGC 2013)"),
  "KCNQ3":   dict(B=2, U=2, G=3, actionable=False,
      cite="M-current partner of K_V7.2; the K_V7-opener anhedonia direction is exploratory only (Costi 2021)"),
  "KCNQ2":   dict(B=2, U=2, G=3, actionable=False,
      cite="the M-current K-channel; the K_V7-opener anhedonia direction is exploratory only -- note: STIFFEST promoter read yet LOW priority (decoupling)"),
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
        "title": "Burden-weighted depression TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420)",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). efficacy=0; "
                      "no molecule, dose, or patient is ranked. SUBSTANTIVE FINDING: because the first-line "
                      "monoamine route leaves a large drug-resistant remainder, the unmet-need tier pushes the "
                      "up-stream HPA / neurotrophic / rapid-glutamate mechanisms ABOVE the high-burden monoamine "
                      "transporters -- the L3-dominant lever map made into a priority order."),
        "decoupling_witness": {
            "stiffest_promoter_gene": stiffest,
            "stiffest_promoter_priority_rank": next(r["rank"] for r in rows if r["gene"] == stiffest),
            "top_priority_gene": top_priority,
            "top_priority_h_sp_rank_stiffest_first": next(
                r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                for r in rows if r["gene"] == top_priority),
            "reading": ("the stiffest promoter read (%s, a minor exploratory L2 lever) sits LOW on priority while the "
                        "top-priority gene (%s) has a MID-RANGE read -- if promoter stiffness drove the ranking neither "
                        "could sit where it does. The decoupling is the firewall made visible." % (stiffest, top_priority)),
        },
        "top_actionable_genes": [r["gene"] for r in actionable[:6]],
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "depression_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted depression TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  {'rank':4} {'gene':9} {'lev':5} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  context(|h_sp| rank)  basis")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (set-point/exploratory)"
        print(f"  {r['rank']:4} {r['gene']:9} {r['lever']:5} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  (h_sp#{c['h_sp_rank_stiffest_first']:2})  {r['cite'][:40]}{act}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
    print(f"  top actionable: {res['top_actionable_genes']}")
