#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schizophrenia_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420).

A small, transparent ranking that combines three CITED tiers --
  B = burden        (schizophrenia prevalence x disability; ~24M people worldwide, among the top causes
                     of years-lived-with-disability per affected person; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem; ~30% of schizophrenia is treatment-
                     resistant, and the established D2-antagonist route leaves the NEGATIVE and COGNITIVE
                     domains largely unaddressed -- the glutamatergic/NMDA mechanisms target what the
                     dopamine route misses)
  G = genetic/druggability evidence (replicated schizophrenia-gene/pharmacology support + tractability;
                     GWAS Trubetskoy 2022 + rare-variant SCHEMA Singh 2022)
each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.
Burden/unmet-need lead (the stated goal: most suffering, most people); genetic+druggability is
included so the ranking favours replicated, tractable directions but cannot let mechanistic elegance
override need. Because schizophrenia's established route (D2 antagonism) is saturated and leaves a large
treatment-resistant + negative/cognitive remainder, the UNMET-need tier pushes the GLUTAMATERGIC (L1/
NMDA) mechanisms ABOVE the established dopamine D2 route -- which is the substantive finding of this
prioritisation, not a tuning artefact.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NOT folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude). The decoupling is the firewall made visible: the STIFFEST promoter read
    (SLC6A3, the dopamine transporter -- NOT a clean antipsychotic direction) ranks LOW on priority,
    and the top-priority gene (GRIN2A) has a MID-RANGE read -- so stiffness cannot be driving the order.
  - actionable=False marks genes whose lever DIRECTION is not a clean tractable direction: CACNA1C and
    CACNB2 (cross-disorder calcium set-point), DRD4 (clozapine-affinity sub-route, exploratory), SLC6A3
    (the transporter -- DAT blockade is the WRONG-direction stimulant target), GABRB3 (exploratory).
  - this ranks READS/TARGETS, not drugs; no molecule, dose, efficacy, or safety is ranked.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 schizophrenia_burden_prioritisation.py  -> schizophrenia_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "schizophrenia_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis. actionable=False where the lever DIRECTION is not a
# clean tractable direction (calcium set-point; D4 exploratory; DAT wrong-direction; GABRB3 exploratory).
TIERS = {
  "GRIN2A":  dict(B=4, U=5, G=5, actionable=True,
      cite="one of the few genes with BOTH genome-wide common-variant and exome rare-variant evidence (Trubetskoy 2022; Singh 2022 SCHEMA); the glutamatergic/NMDA route addresses the treatment-resistant + negative/cognitive remainder the dopamine route misses"),
  "GRIN2B":  dict(B=4, U=5, G=4, actionable=True,
      cite="the principal NMDA-modulator subunit; the NMDA-hypofunction route is the leading non-dopaminergic mechanism for the remainder (Olney 1995; Trubetskoy 2022)"),
  "DRD2":    dict(B=5, U=2, G=5, actionable=True,
      cite="the dopamine D2 receptor; the single most established target (every licensed agent is a D2 antagonist/partial agonist) and a GWAS locus -- HIGHEST burden but LOW unmet (the established route already addresses it) (Seeman 1976; Howes 2009; Trubetskoy 2022)"),
  "GRIN1":   dict(B=3, U=5, G=4, actionable=True,
      cite="the obligate NMDA subunit and the glycine-site node; the NMDA-hypofunction direction (sign-subtle: PV-interneuron hypofunction -> downstream disinhibition) (Javitt 1991; Olney 1995)"),
  "CACNA1C": dict(B=4, U=3, G=4, actionable=False,
      cite="the most-replicated cross-disorder calcium locus; a set-point gene shared across five disorders, NOT a clean schizophrenia-selective direction (Cross-Disorder PGC 2013; Ripke 2014)"),
  "GRIA3":   dict(B=3, U=4, G=3, actionable=True,
      cite="an AMPA-receptor subunit downstream of the NMDA node; the fast-excitatory sub-route of the glutamatergic axis (Trubetskoy 2022)"),
  "TH":      dict(B=3, U=4, G=3, actionable=True,
      cite="tyrosine hydroxylase; the elevated presynaptic striatal dopamine-SYNTHESIS capacity is the most-replicated imaging abnormality, distinct from the post-synaptic D2 route (Howes 2012)"),
  "HTR2A":   dict(B=3, U=3, G=4, actionable=True,
      cite="the 5-HT2A receptor; the serotonin-dopamine atypical axis (non-monotone direction) (Meltzer 1989)"),
  "CACNB2":  dict(B=3, U=3, G=3, actionable=False,
      cite="the Ca_V beta-2 auxiliary subunit; a GWAS calcium-channel locus but a set-point modifier, not a clean direction (Cross-Disorder PGC 2013)"),
  "GABRA1":  dict(B=3, U=3, G=3, actionable=True,
      cite="GABA-A alpha1; the parvalbumin-interneuron restore route addressing the cortical disinhibition mechanism (Lewis 2005)"),
  "COMT":    dict(B=2, U=3, G=3, actionable=True,
      cite="catechol-O-methyltransferase; the prefrontal catecholamine Val158Met set-point modifier (Egan 2001)"),
  "SLC6A3":  dict(B=3, U=2, G=2, actionable=False,
      cite="the dopamine transporter (DAT); NOT a clean direction -- DAT blockade RAISES dopamine (the amphetamine/stimulant direction that worsens psychosis) -- note: STIFFEST promoter read yet LOW priority (decoupling) (Laruelle 1996)"),
  "GABRB3":  dict(B=2, U=3, G=2, actionable=False,
      cite="GABA-A beta3 (15q11-13); the interneuron-restore sub-route, exploratory (Lewis 2005)"),
  "DRD4":    dict(B=2, U=2, G=2, actionable=False,
      cite="the dopamine D4 receptor; high clozapine affinity made it a candidate, but a clean D4-selective direction is exploratory (Van Tol 1991)"),
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
    # substantive finding: the leading glutamatergic L1 gene vs the established D2 gene
    glut_rank = next(r["rank"] for r in rows if r["gene"] == "GRIN2A")
    d2_rank   = next(r["rank"] for r in rows if r["gene"] == "DRD2")
    return {
        "title": "Burden-weighted schizophrenia TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420)",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). efficacy=0; "
                      "no molecule, dose, or patient is ranked. SUBSTANTIVE FINDING: because the established "
                      "D2-antagonist route is saturated and leaves a large treatment-resistant + negative/"
                      "cognitive remainder, the unmet-need tier pushes the GLUTAMATERGIC (L1/NMDA) mechanisms "
                      "ABOVE the established dopamine D2 route -- the L1+L3 co-dominant lever map made into a "
                      "priority order, with the unmet-need axis breaking the L1/L3 symmetry in L1's favour."),
        "substantive_finding": {
            "leading_glutamatergic_gene": "GRIN2A", "glutamatergic_rank": glut_rank,
            "established_dopamine_gene": "DRD2", "dopamine_rank": d2_rank,
            "reading": ("the leading glutamatergic L1 gene GRIN2A ranks #%d, ABOVE the established dopamine "
                        "D2 gene DRD2 at #%d -- the unmet-need tier surfaces the NMDA route as the higher-"
                        "leverage direction precisely because the D2 route is already the established one and "
                        "leaves the negative/cognitive remainder. This does NOT assert efficacy; it ranks where "
                        "the unmet mechanistic need is greatest." % (glut_rank, d2_rank)),
        },
        "decoupling_witness": {
            "stiffest_promoter_gene": stiffest,
            "stiffest_promoter_priority_rank": next(r["rank"] for r in rows if r["gene"] == stiffest),
            "top_priority_gene": top_priority,
            "top_priority_h_sp_rank_stiffest_first": next(
                r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                for r in rows if r["gene"] == top_priority),
            "reading": ("the stiffest promoter read (%s, the dopamine transporter -- not a clean direction) sits "
                        "LOW on priority while the top-priority gene (%s) has a MID-RANGE read -- if promoter "
                        "stiffness drove the ranking neither could sit where it does. The decoupling is the "
                        "firewall made visible." % (stiffest, top_priority)),
        },
        "top_actionable_genes": [r["gene"] for r in actionable[:6]],
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "schizophrenia_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted schizophrenia TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  {'rank':4} {'gene':9} {'lev':5} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  context(|h_sp| rank)  basis")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (set-point/exploratory/wrong-dir)"
        print(f"  {r['rank']:4} {r['gene']:9} {r['lever']:5} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  (h_sp#{c['h_sp_rank_stiffest_first']:2})  {r['cite'][:40]}{act}")
    sf = res["substantive_finding"]
    print(f"  finding: glutamatergic {sf['leading_glutamatergic_gene']} #{sf['glutamatergic_rank']} ABOVE established dopamine {sf['established_dopamine_gene']} #{sf['dopamine_rank']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
    print(f"  top actionable: {res['top_actionable_genes']}")
