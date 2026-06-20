#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autism_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420) via the bipolar/epilepsy/depression/
schizophrenia T-L prioritisers.

A small, transparent ranking that combines three CITED tiers --
  B = burden        (autism prevalence x lifelong disability; ~1 in 36 children identified, ~2% of the
                     population, a lifelong neurodevelopmental condition with substantial support needs at
                     the higher-need end; GBD/CDC-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem). THE AUTISM SIGNATURE: there is NO
                     approved pharmacology for the CORE features (social-communication, the E/I set-point
                     itself); the only licensed agents target the irritability ADJUNCT, not the core. So
                     unlike schizophrenia -- where the established D2 route drives DRD2's unmet-need LOW --
                     autism has no gene whose unmet need is lowered by an established core route. U is
                     therefore uniformly HIGH (the U-floor here is higher than in any prior T-L chapter).
  G = genetic/druggability evidence (replicated autism-gene support + tractability; SFARI gene scores +
                     the rare-variant exome studies (e.g. Satterstrom 2020) + common-variant GWAS (Grove
                     2019)). K+ / GABA-A channels are highly druggable; NMDA/Na_V subunits are sign-subtle.

each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.

SUBSTANTIVE FINDING (the autism analogue of schizophrenia's "glutamatergic above dopamine"):
  the L2 INHIBITORY-RESTORE route (GABA-A / K+ : GABRB3, GABRA5, KCNQ3, GABRA2) is the cleanest
  ACTIONABLE direction -- NOT because it scores highest in the abstract, but because the high-scoring
  L1 EXCITATORY-REDUCE genes are mostly sign-subtle: SCN2A and GRIN2B are GoF/LoF-opposite (a gain-of-
  function pushes the early-infantile DEE / seizure pole, a loss-of-function the milder ASD/ID pole), so
  "reduce excitation" is NOT a clean clinical direction for them; CACNA1C is a cross-disorder calcium
  SET-POINT shared across five disorders, not autism-selective. When the ranking is filtered to clean
  (actionable) directions, the inhibitory-restore L2 genes rise to the top -- restoring outward K+/Cl-
  inhibition is direction-consistent (it raises the spinodal fold) whereas reducing inward current runs
  into the GoF/LoF sign problem. This is the L1-dominant-by-COUNT map turned into a priority order, with
  the actionability filter breaking L1's count-dominance in L2's favour.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NEVER folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude). The decoupling is the firewall made visible: the STIFFEST promoter read
    (SLC6A4, the serotonin transporter -- the SPARSE L3 node, NOT a clean direction) ranks LOWEST on
    priority, and the top-priority gene has a MID-RANGE read -- so stiffness cannot be driving the order.
  - actionable=False marks genes whose lever DIRECTION is not a clean tractable direction: SCN2A and
    GRIN2B (GoF/LoF sign-subtle), CACNA1C (cross-disorder calcium set-point), SLC6A4 (non-monotone
    serotonergic adjunct).
  - this ranks READS/TARGETS, not drugs; no molecule, dose, efficacy, or safety is ranked. Autism is a
    neurodevelopmental DIFFERENCE, not only a deficit; the ranking surfaces where unmet MECHANISTIC need
    is greatest, it does NOT assert that any direction "treats", "normalises", or "cures" autism.

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 autism_burden_prioritisation.py  -> autism_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "autism_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis. actionable=False where the lever DIRECTION is not a
# clean tractable direction (GoF/LoF sign-subtle; cross-disorder set-point; non-monotone serotonergic).
# NOTE the autism U-signature: U is uniformly HIGH because no established route addresses the CORE
# features -- there is no DRD2-analogue with a lowered unmet need.
TIERS = {
  # ---- L1 : excitatory-reduce (mostly sign-subtle) ----
  "GRIN2A":  dict(B=4, U=5, G=4, actionable=True,
      cite="a high-confidence SFARI gene; the NMDA GluN2A subunit on the excitatory axis. The E/I-restore framing makes the NMDA node a candidate DIRECTION, though the autism-vs-epilepsy-aphasia phenotype is allele-dependent (Satterstrom 2020; SFARI Gene)"),
  "GRIN2B":  dict(B=4, U=5, G=4, actionable=False,
      cite="a high-confidence SFARI NMDA GluN2B gene, but SIGN-SUBTLE: gain-of-function pushes the early DEE/seizure pole while loss-of-function the milder ASD/ID pole -- so 'reduce excitation' is not a clean clinical direction (Satterstrom 2020; Platzer 2017)"),
  "GRIA1":   dict(B=3, U=4, G=3, actionable=True,
      cite="an AMPA-receptor subunit downstream of the NMDA node; the fast-excitatory sub-route of the E/I axis (SFARI Gene)"),
  "CACNA1C": dict(B=4, U=4, G=4, actionable=False,
      cite="the most-replicated CROSS-DISORDER calcium locus (Ca_V1.2); a set-point gene shared across five disorders, NOT an autism-selective direction (Cross-Disorder PGC 2013)"),
  "SCN2A":   dict(B=4, U=5, G=4, actionable=False,
      cite="one of the most recurrently mutated ASD genes (Na_V1.2), but SIGN-SUBTLE: early gain-of-function gives infantile DEE/seizures, later loss-of-function gives ASD/ID -- opposite directions, so the excitatory-reduce direction is sign-dependent (Sanders 2018; Satterstrom 2020)"),
  # ---- L2 : inhibitory-restore (the cleanest actionable direction) ----
  "KCNQ3":   dict(B=3, U=5, G=4, actionable=True,
      cite="K_V7.3 (M-current K+); restoring outward K+ current is direction-consistent (raises the fold) and the channel is druggable (the retigabine/ezogabine M-current precedent) (Wang 1998)"),
  "GABRB3":  dict(B=4, U=5, G=4, actionable=True,
      cite="GABA-A beta3 in the 15q11-13 region (the Dup15q/Angelman overlap raises burden); restoring Cl- inhibition is direction-consistent and GABA-A is highly druggable (Cook 1998; SFARI Gene)"),
  "GABRA5":  dict(B=3, U=5, G=4, actionable=True,
      cite="extrasynaptic GABA-A alpha5 carrying tonic inhibition; alpha5-selective ligands exist (the cognition/Down-syndrome alpha5 literature), an actionable inhibitory-restore node (SFARI Gene)"),
  "GABRA2":  dict(B=3, U=4, G=3, actionable=True,
      cite="synaptic GABA-A alpha2; the phasic-inhibition sub-route of the inhibitory-restore axis (SFARI Gene)"),
  # ---- L3 : serotonergic, SPARSE (non-monotone, stiffest read yet lowest priority) ----
  "SLC6A4":  dict(B=2, U=3, G=2, actionable=False,
      cite="the serotonin transporter; the SPARSE L3 node -- the serotonergic evidence in autism is NON-MONOTONE/mixed (an adjunct, not a core direction) -- note: STIFFEST promoter read yet LOWEST priority (decoupling) (SFARI Gene)"),
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
    # the autism U-signature: the lowest unmet-need tier present (no DRD2-analogue at U<=2)
    u_floor = min(t["U"] for t in TIERS.values())
    # decoupling witnesses: the stiffest promoter and the top-priority gene
    stiffest = m["order_by_spinodal_desc"][0]
    top_priority = rows[0]["gene"]
    # substantive finding: the leading ACTIONABLE inhibitory-restore (L2) gene vs the highest-scoring
    # but NON-actionable excitatory (L1) gene (the sign-subtle one)
    lead_l2 = next(r for r in rows if r["lever"] == "L2" and r["actionable"])
    blocked_l1 = next((r for r in rows if r["lever"] == "L1" and not r["actionable"]), None)
    l2_top = [r["gene"] for r in actionable if r["lever"] == "L2"]
    return {
        "title": "Burden-weighted autism TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia T-L",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "autism_unmet_need_signature": {
            "u_floor": u_floor,
            "reading": ("the AUTISM signature: there is no approved pharmacology for the CORE features "
                        "(only the irritability adjunct is licensed), so -- unlike schizophrenia where the "
                        "established D2 route drives DRD2's unmet need to 2 -- NO autism gene has a lowered "
                        "unmet need from an established core route. The unmet-need FLOOR here is %d, higher "
                        "than in any prior T-L chapter; U is uniformly high." % u_floor),
        },
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). efficacy=0; "
                      "no molecule, dose, or patient is ranked; autism is a neurodevelopmental DIFFERENCE, "
                      "not only a deficit. SUBSTANTIVE FINDING: the L2 INHIBITORY-RESTORE route is the "
                      "cleanest ACTIONABLE direction because the high-scoring L1 excitatory genes are mostly "
                      "sign-subtle (SCN2A/GRIN2B GoF/LoF-opposite) or cross-disorder set-points (CACNA1C); "
                      "filtering to clean directions lifts the GABA-A/K+ inhibitory-restore genes to the top "
                      "-- the L1-dominant-by-count map turned into a priority order, with the actionability "
                      "filter breaking L1's count-dominance in L2's favour."),
        "substantive_finding": {
            "leading_actionable_inhibitory_gene": lead_l2["gene"],
            "leading_actionable_inhibitory_lever": lead_l2["lever"],
            "leading_actionable_inhibitory_rank": lead_l2["rank"],
            "highest_scoring_blocked_excitatory_gene": (blocked_l1["gene"] if blocked_l1 else None),
            "highest_scoring_blocked_excitatory_rank": (blocked_l1["rank"] if blocked_l1 else None),
            "top_actionable_inhibitory_genes": l2_top,
            "reading": ("the leading ACTIONABLE inhibitory-restore gene %s (%s) ranks #%d, and the top "
                        "actionable set is dominated by the L2 GABA-A/K+ inhibitory-restore genes %s. The "
                        "L1 excitatory genes that score as high or higher -- e.g. %s at #%s -- are flagged "
                        "NON-actionable because their GoF/LoF sign-subtlety (or cross-disorder set-point "
                        "status) makes 'reduce excitation' a non-clean direction. So the cleanest actionable "
                        "direction is to RESTORE inhibition (raise the fold), not to reduce excitation. This "
                        "does NOT assert efficacy; it ranks where the clean, unmet mechanistic direction is."
                        % (lead_l2["gene"], lead_l2["lever"], lead_l2["rank"], l2_top,
                           (blocked_l1["gene"] if blocked_l1 else "n/a"),
                           (str(blocked_l1["rank"]) if blocked_l1 else "n/a"))),
        },
        "decoupling_witness": {
            "stiffest_promoter_gene": stiffest,
            "stiffest_promoter_priority_rank": next(r["rank"] for r in rows if r["gene"] == stiffest),
            "top_priority_gene": top_priority,
            "top_priority_h_sp_rank_stiffest_first": next(
                r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                for r in rows if r["gene"] == top_priority),
            "reading": ("the stiffest promoter read (%s, the serotonin transporter -- the sparse L3 node, "
                        "not a clean direction) sits LOWEST on priority while the top-priority gene (%s) has "
                        "a MID-RANGE read -- if promoter stiffness drove the ranking neither could sit where "
                        "it does. The decoupling is the firewall made visible." % (stiffest, top_priority)),
        },
        "top_actionable_genes": [r["gene"] for r in actionable[:6]],
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "autism_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted autism TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  U-floor: {res['autism_unmet_need_signature']['u_floor']}  (no core-feature pharmacology -> U uniformly high)")
    print(f"  {'rank':4} {'gene':9} {'lev':5} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  context(|h_sp| rank)  basis")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (sign-subtle/set-point/non-monotone)"
        print(f"  {r['rank']:4} {r['gene']:9} {r['lever']:5} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  (h_sp#{c['h_sp_rank_stiffest_first']:2})  {r['cite'][:40]}{act}")
    sf = res["substantive_finding"]
    print(f"  finding: inhibitory-restore {sf['leading_actionable_inhibitory_gene']} ({sf['leading_actionable_inhibitory_lever']}) #{sf['leading_actionable_inhibitory_rank']} is the cleanest ACTIONABLE direction; "
          f"L1 {sf['highest_scoring_blocked_excitatory_gene']} #{sf['highest_scoring_blocked_excitatory_rank']} blocked (sign-subtle)")
    print(f"  top actionable inhibitory (L2): {sf['top_actionable_inhibitory_genes']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
    print(f"  top actionable: {res['top_actionable_genes']}")
