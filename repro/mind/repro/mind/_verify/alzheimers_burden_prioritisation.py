#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alzheimers_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420) via the bipolar/epilepsy/depression/
schizophrenia/autism/ADHD/addiction T-L prioritisers.

A small, transparent ranking that combines three CITED tiers --
  B = burden        (Alzheimer's disease prevalence x impairment x caregiver burden; AD is the leading
                     cause of dementia and among the very highest-burden conditions worldwide, with
                     prevalence rising steeply in ageing populations and an enormous informal-care
                     burden; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem). THE ALZHEIMER'S SIGNATURE is the
                     DEEPEST partial-fit case in the series. The REACHABLE surface is PURELY
                     SYMPTOMATIC: the cholinergic-drive levers (ACHE/BCHE via the donepezil/rivastigmine/
                     galantamine route), the glutamatergic-excitotoxicity lever (GRIN2B via the memantine
                     route) and the inhibitory-restore arm carry only a MODERATE unmet need where an
                     established symptomatic route exists -- but those routes give only TEMPORARY, MODEST
                     benefit and DO NOT slow neurodegeneration, so the unmet FLOOR (3) sits ABOVE ADHD's
                     clean-route floor (2). BUT the dominant fault -- the neurodegenerative PROGRESSION
                     axis (APP/PSEN1/PSEN2 amyloid/gamma-secretase, MAPT tau, APOE clearance, TREM2
                     microglial) -- carries the unmet-need CEILING (disease-MODIFICATION is the single
                     greatest unmet need in the field; even the anti-amyloid antibodies lecanemab/
                     donanemab only MODESTLY slow decline, with serious caveats) AND is OUT OF REACH of
                     a threshold/drive lever, because that axis is an E0 DECAY -- a cumulative,
                     irreversible LOSS over time, the structural INVERSE of addiction's E0 GAIN, not an
                     instantaneous fold. So the highest-need targets are precisely the unreachable ones,
                     for the DEEPEST reason in the series.
  G = genetic/druggability evidence (replicated AD-gene support + tractability; APOE e4 -- the strongest
                     common genetic risk factor for late-onset AD; APP/PSEN1/PSEN2 -- the autosomal-
                     dominant early-onset familial-AD genes (Mendelian); MAPT tau; TREM2 R47H rare
                     variant. The cholinesterases ACHE/BCHE are highly druggable enzymes (the donepezil/
                     rivastigmine target); receptors CHRM1/CHRNA7/GRIN/GABR are druggable; but the
                     progression effectors -- APOE clearance, tau, gamma-secretase modulation -- have
                     historically been the hardest targets in CNS drug development).

each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.

SUBSTANTIVE FINDING (the Alzheimer's analogue of ADHD's "highest need is out of reach", here for the
DEEPEST reason in the series): the highest-need targets are ALL non-actionable -- the PROG
progression genes (APP/APOE/MAPT/PSEN/TREM2) carry the unmet CEILING (disease-modification, the
greatest unmet need, only modestly touched even now) and are OUT OF REACH of a threshold/drive lever.
The cleanest ACTIONABLE direction (the cholinesterase ACHE, the donepezil/rivastigmine target) ranks
just below the top because its unmet need is LOWERED by an established -- though purely symptomatic,
temporary -- route. So the priority order makes the PARTIAL FIT concrete: the targets of greatest
mechanistic need (the PROG progression axis) are exactly the ones the threshold frame cannot reach,
because that axis is a degenerative E0-DECAY variable -- a cumulative loss over time -- not an
instantaneous fold. This extends the partial-fit signature (highest need out of reach) to a
DEGENERATIVE decay, the structural inverse of addiction's consolidated gain.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - efficacy=0: that an established APPROVED symptomatic route exists is a CITED fact that LOWERS a
    UNMET-NEED tier; it is NOT an efficacy claim about any direction, and no molecule/dose/patient is
    ranked. The cholinesterase-inhibitor and memantine routes are SYMPTOMATIC ONLY and do NOT slow
    progression. The ranking surfaces where unmet MECHANISTIC need is greatest and which of those targets
    the frame can/cannot reach. It does NOT assert that any direction "treats", "cures", "reverses", or
    "prevents" Alzheimer's, claims NO disease-modification for the reachable levers, and makes NO
    miracle-cure claim. A person living with dementia remains a person.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NEVER folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude, a neurodegeneration rate, or an amyloid/tau burden). The decoupling is the
    firewall made visible: the STIFFEST promoter read (CHRM1) sits MID-table on priority (it is a
    reachable symptomatic lever with no clean approved AD route), while the top-priority gene (the
    out-of-reach APP/amyloid driver) has only a mid-stiffness read -- so stiffness cannot be driving
    the order.
  - actionable=False marks genes the threshold/drive frame cannot cleanly act on: APP/PSEN1/PSEN2/MAPT/
    APOE/TREM2 (OUT OF REACH on the PROG neurodegenerative-progression axis -- the E0-decay trace).

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 alzheimers_burden_prioritisation.py  -> alzheimers_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "alzheimers_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis + reach_status. actionable=False where the frame cannot
# cleanly act: OUT OF REACH (PROG neurodegenerative-progression axis -- the E0-decay trace).
# NOTE the Alzheimer's U-signature (the DEEPEST partial fit): the REACHABLE surface is PURELY SYMPTOMATIC.
# Cholinergic-drive levers with an established (donepezil/rivastigmine/galantamine) route carry a MODERATE
# unmet need; the OUT-OF-REACH PROG genes carry the unmet CEILING (disease-modification, only modestly
# touched even by lecanemab/donanemab) because no threshold lever reaches a degenerative E0-decay axis.
TIERS = {
  # ---- reachable cholinergic-drive LEVERS (L3, the DOMINANT lever; RESTORE deficient tone) ----
  "ACHE":   dict(B=5, U=3, G=5, actionable=True, reach="reached (L3 cholinergic drive; symptomatic only)",
      cite="acetylcholinesterase (ACHE); the molecular target of the established donepezil/rivastigmine/galantamine route -- the cholinergic-deficit hypothesis of AD. Its UNMET-need tier is LOWERED by an established route, but the route is SYMPTOMATIC ONLY, gives temporary/modest benefit and does NOT slow progression, so unmet stays MODERATE; a highly druggable enzyme (Davies 1976; Birks 2006)"),
  "BCHE":   dict(B=4, U=3, G=4, actionable=True, reach="reached (L3 cholinergic drive; symptomatic only)",
      cite="butyrylcholinesterase (BCHE); the co-target of rivastigmine (a dual AChE/BuChE inhibitor) whose relative role rises as AChE falls in advancing AD -- UNMET LOWERED by the established (symptomatic, temporary) rivastigmine route; a druggable enzyme (Greig 2005; Birks 2006)"),
  "CHRM1":  dict(B=4, U=4, G=4, actionable=True, reach="reached (L3 cholinergic drive) but no clean approved AD route",
      cite="the M1 muscarinic acetylcholine receptor (CHRM1); the post-synaptic cholinergic-drive node. Selective M1 agonism has been pursued for AD cognition but has historically been hard to drug cleanly (no approved AD-specific muscarinic route), so the reachable lever carries a HIGHER unmet need than the cholinesterases (Bodick 1997; Volkow-equivalent AD reviews)"),
  "CHRNA7": dict(B=4, U=4, G=4, actionable=True, reach="reached (L3 cholinergic drive) but route failed in trials",
      cite="the alpha-7 nicotinic acetylcholine receptor (CHRNA7); a pre/post-synaptic cholinergic-drive node. Alpha-7 agonists (e.g. encenicline) were trialled for AD cognition but FAILED, so no clean approved route exists and the reachable lever carries a HIGH unmet need (Hurst 2013)"),
  # ---- reachable glutamatergic-excitotoxicity LEVERS (L1; REDUCE excitotoxic drive) ----
  "GRIN2B": dict(B=4, U=4, G=3, actionable=True, reach="reached (L1 glutamatergic excitotoxicity)",
      cite="the NMDA NR2B subunit (GRIN2B); the preferential target of the memantine route that dampens tonic excitotoxic NMDA drive in moderate-severe AD. The established memantine route is only WEAKLY/modestly effective and symptomatic, so unmet stays MODERATE-HIGH (Reisberg 2003)"),
  "GRIN2A": dict(B=4, U=4, G=3, actionable=True, reach="reached (L1 glutamatergic excitotoxicity)",
      cite="the NMDA NR2A subunit (GRIN2A); the glutamatergic-excitotoxicity substrate of the same memantine direction (low-affinity, use-dependent NMDA channel block) -- symptomatic and modest at best, unmet stays MODERATE-HIGH (Reisberg 2003)"),
  # ---- reachable inhibitory-RESTORE / network LEVERS (L2; RESTORE inhibitory tone against AD hyperexcitability) ----
  "GABRA1": dict(B=3, U=4, G=3, actionable=True, reach="reached (L2 inhibitory restore / network)",
      cite="the GABA-A alpha-1 subunit (GABRA1); the synaptic inhibitory-restore arm against AD network HYPEREXCITABILITY (subclinical epileptiform activity is common in AD and worsens cognition). No approved GABAergic AD route exists, so the reachable inhibitory-restore lever carries a HIGH unmet need (Palop 2007; Vossel 2013)"),
  "GABRA5": dict(B=3, U=4, G=3, actionable=True, reach="reached (L2 inhibitory restore / network)",
      cite="the GABA-A alpha-5 subunit (GABRA5, extrasynaptic/tonic inhibition, hippocampus-enriched); the tonic inhibitory-restore arm of the AD network-hyperexcitability direction -- experimental, no approved route, unmet stays HIGH (Palop 2007)"),
  "GABRB3": dict(B=3, U=4, G=3, actionable=True, reach="reached (L2 inhibitory restore / network)",
      cite="the GABA-A beta-3 subunit (GABRB3); the inhibitory-restore arm of the same AD network-hyperexcitability direction -- experimental, no approved route, unmet stays HIGH (Palop 2007)"),
  # ---- OUT-OF-REACH neurodegenerative-progression genes (PROG) -- highest unmet, NOT reachable by a threshold/drive lever ----
  "APP":    dict(B=5, U=5, G=4, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="amyloid precursor protein (APP); the source of the amyloid-beta peptide and an autosomal-dominant EARLY-ONSET familial-AD gene (Mendelian). The PROG progression axis is the DOMINANT AD fault and disease-MODIFICATION is the single greatest unmet need in the field; the anti-amyloid antibodies lecanemab/donanemab target this axis but only MODESTLY reduce the rate of clinical decline, with serious caveats -- UNMET at the ceiling. A threshold/drive lever has NO handle on a degenerative E0-DECAY axis (a cumulative, irreversible loss over time, not a fold) -- OUT OF REACH, the deepest partial-fit signature (Goate 1991; van Dyck 2023)"),
  "APOE":   dict(B=5, U=5, G=3, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="apolipoprotein E (APOE); the e4 allele is the STRONGEST COMMON genetic risk factor for late-onset AD, acting on amyloid clearance and lipid/microglial handling. APOE has historically been among the hardest CNS targets to drug; disease-modification via clearance is at the unmet ceiling and the degenerative E0-DECAY axis is OUT OF REACH of a threshold lever (Corder 1993)"),
  "MAPT":   dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="microtubule-associated protein tau (MAPT); neurofibrillary tau tangles track AD severity and spread, and MAPT mutations cause frontotemporal degeneration. There is NO approved tau therapy (tau antisense/aggregation approaches are emerging), so disease-modification is at the unmet ceiling and the degenerative E0-DECAY axis is OUT OF REACH (Goedert 1988; Spillantini 1998)"),
  "PSEN1":  dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="presenilin-1 (PSEN1); the gamma-secretase catalytic subunit and the most common autosomal-dominant EARLY-ONSET familial-AD gene. Gamma-secretase MODULATION has repeatedly failed in trials, so disease-modification stays at the unmet ceiling and the degenerative E0-DECAY axis is OUT OF REACH (Sherrington 1995)"),
  "PSEN2":  dict(B=3, U=5, G=3, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="presenilin-2 (PSEN2); the second gamma-secretase catalytic subunit and a rarer autosomal-dominant early-onset familial-AD gene -- the same out-of-reach gamma-secretase/amyloid PROG axis; disease-modification at the unmet ceiling, OUT OF REACH of a threshold lever (Levy-Lahad 1995)"),
  "TREM2":  dict(B=3, U=5, G=3, actionable=False, reach="OUT-OF-REACH (PROG neurodegenerative-progression axis; E0 decay)",
      cite="the microglial receptor TREM2; the R47H rare variant roughly triples late-onset AD risk via impaired microglial response to amyloid/neurodegeneration. Microglial/neuroinflammatory disease-modification is emerging but unproven, so unmet stays at the ceiling and the degenerative E0-DECAY axis is OUT OF REACH of a threshold lever (Guerreiro 2013)"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["G"]*t["G"], 4)

def build():
    m = json.load(open(MAP))
    lever_by_gene = {e["gene"]: e for e in m["entries"]}
    oor_by_gene   = {e["gene"]: e for e in m["out_of_reach_targets"]["entries"]}
    all_by_gene   = {**lever_by_gene, **oor_by_gene}
    # combined stiffest-first |h_sp| rank across ALL fifteen genes (levers + out-of-reach)
    hsp_order = sorted(all_by_gene.values(), key=lambda e: -e["spinodal_h_sp"])
    hsp_rank  = {e["gene"]: i+1 for i, e in enumerate(hsp_order)}
    stiffest  = hsp_order[0]["gene"]

    rows = []
    for gene, t in TIERS.items():
        e = all_by_gene[gene]
        rows.append({
            "gene": gene, "lever": e.get("lever"),
            "reach_status": t["reach"],
            "channel_or_protein": e.get("channel") or e.get("protein") or e.get("role"),
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

    # the Alzheimer's U-signature: the LOWEST unmet-need tier present (the established-but-symptomatic routes)
    u_floor = min(t["U"] for t in TIERS.values())
    top_priority = rows[0]["gene"]

    # substantive finding: the leading ACTIONABLE (reachable) gene vs the highest-scoring NON-actionable
    # gene (the out-of-reach PROG neurodegenerative-progression effector)
    lead_act = next(r for r in rows if r["actionable"])
    blocked_top = next((r for r in rows if not r["actionable"]), None)
    act_top = [r["gene"] for r in actionable]
    return {
        "title": "Burden-weighted Alzheimer's TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction T-L",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "alzheimers_unmet_need_signature": {
            "u_floor": u_floor,
            "reading": ("the Alzheimer's signature -- the DEEPEST partial-fit case in the series: the "
                        "REACHABLE surface is PURELY SYMPTOMATIC. The cholinergic-drive levers carry only "
                        "a MODERATE unmet need where an established symptomatic route exists (the "
                        "donepezil/rivastigmine/galantamine route on ACHE/BCHE), but that route gives only "
                        "temporary/modest benefit and does NOT slow neurodegeneration. The unmet-need "
                        "FLOOR here is %d -- ABOVE ADHD's clean-route floor of 2 (because the AD symptomatic "
                        "routes are only modestly effective and do not touch the disease) and the muscarinic/"
                        "nicotinic/glutamate/inhibitory levers sit higher still (no clean approved route, or "
                        "a failed one). BUT the dominant fault -- the neurodegenerative PROGRESSION axis "
                        "(APP/PSEN1/PSEN2 amyloid/gamma-secretase, MAPT tau, APOE clearance, TREM2 microglial) "
                        "-- carries the unmet-need CEILING (5): disease-MODIFICATION is the single greatest "
                        "unmet need in the field, only MODESTLY touched even by the anti-amyloid antibodies "
                        "lecanemab/donanemab (which only modestly reduce the rate of clinical decline). That "
                        "axis is OUT OF REACH of a threshold/drive lever because it "
                        "is an E0 DECAY -- a cumulative, irreversible loss over time, the structural INVERSE "
                        "of addiction's E0 GAIN, not an instantaneous fold. So the highest-need targets are "
                        "precisely the unreachable ones, for the DEEPEST reason in the series." % u_floor),
        },
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "efficacy=0: that an established APPROVED symptomatic route exists is a CITED fact "
                      "that LOWERS a UNMET-NEED tier, NOT an efficacy claim about any direction; no "
                      "molecule, dose, or patient is ranked; the cholinesterase-inhibitor and memantine "
                      "routes are SYMPTOMATIC ONLY and do NOT slow progression; the ranking claims NO "
                      "disease-modification for the reachable levers, grants NO miracle cure, and does NOT "
                      "assert that any direction treats, cures, reverses, or prevents Alzheimer's; a person "
                      "living with dementia remains a person. gamma-|h_sp| is carried ALONGSIDE as "
                      "structural context and is NEVER folded into the score (firewall: a promoter-stiffness "
                      "read is not a clinical magnitude, a neurodegeneration rate, or an amyloid/tau "
                      "burden). SUBSTANTIVE FINDING: the highest-need targets are ALL non-actionable -- the "
                      "PROG progression genes (APP/APOE/MAPT/PSEN/TREM2) carry the unmet CEILING and are "
                      "OUT OF REACH of the threshold/drive frame -- while the cleanest ACTIONABLE direction "
                      "(the cholinesterase ACHE) ranks just below the top because its unmet need is LOWERED "
                      "by an established (symptomatic, temporary) route. The priority order makes the "
                      "PARTIAL FIT concrete: the targets of greatest mechanistic need are exactly the ones "
                      "the frame cannot reach, because the PROG axis is a degenerative E0-DECAY variable -- "
                      "a cumulative loss over time, the structural inverse of addiction's consolidated "
                      "gain."),
        "substantive_finding": {
            "leading_actionable_gene": lead_act["gene"],
            "leading_actionable_lever": lead_act["lever"],
            "leading_actionable_rank": lead_act["rank"],
            "highest_scoring_nonactionable_gene": (blocked_top["gene"] if blocked_top else None),
            "highest_scoring_nonactionable_rank": (blocked_top["rank"] if blocked_top else None),
            "highest_scoring_nonactionable_reach": (blocked_top["reach_status"] if blocked_top else None),
            "top_actionable_genes": act_top,
            "reading": ("the highest-need targets are ALL non-actionable: the PROG neurodegenerative-"
                        "progression genes (APP/APOE/MAPT/PSEN/TREM2) carry the unmet CEILING (disease-"
                        "modification, the greatest unmet need, only modestly touched even now) and are OUT "
                        "OF REACH of the threshold/drive frame. The highest-scoring target %s (#%d) is %s. "
                        "The cleanest ACTIONABLE direction, %s (%s), ranks #%d because its UNMET need is "
                        "LOWERED by an established -- though purely symptomatic, temporary -- route. So the "
                        "priority order makes the PARTIAL FIT concrete: the targets of greatest mechanistic "
                        "need (the PROG progression axis) are exactly the ones the threshold frame cannot "
                        "reach, while the reachable levers already carry established (symptomatic) routes. "
                        "This ranks unmet MECHANISTIC need; it makes NO efficacy claim (see the firewall: "
                        "no direction is asserted to treat, cure, reverse, or prevent the disorder, and the "
                        "reachable levers do not slow progression)."
                        % ((blocked_top["gene"] if blocked_top else "n/a"),
                           (blocked_top["rank"] if blocked_top else 0),
                           (blocked_top["reach_status"] if blocked_top else "n/a"),
                           lead_act["gene"], lead_act["lever"], lead_act["rank"])),
        },
        "decoupling_witness": {
            "stiffest_promoter_gene": stiffest,
            "stiffest_promoter_priority_rank": next(r["rank"] for r in rows if r["gene"] == stiffest),
            "top_priority_gene": top_priority,
            "top_priority_h_sp_rank_stiffest_first": next(
                r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                for r in rows if r["gene"] == top_priority),
            "reading": ("the stiffest promoter read (%s, a REACHABLE symptomatic cholinergic-drive node "
                        "with no clean approved AD route) sits at priority #%d -- NOT the top; while the "
                        "top-priority gene (%s, on the out-of-reach PROG neurodegenerative-progression "
                        "axis) has only the #%d-stiffest promoter. If promoter stiffness drove the ranking "
                        "neither could sit where it does. The decoupling is the firewall made visible: a "
                        "promoter-stiffness read is carried alongside but never folded into the clinical "
                        "priority, and it is not a neurodegeneration rate or an amyloid/tau burden."
                        % (stiffest, next(r["rank"] for r in rows if r["gene"] == stiffest),
                           top_priority, next(r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                                              for r in rows if r["gene"] == top_priority))),
        },
        "top_actionable_genes": act_top,
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "alzheimers_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted Alzheimer's TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0; symptomatic levers do NOT slow progression)")
    print(f"  U-floor: {res['alzheimers_unmet_need_signature']['u_floor']}  (established but SYMPTOMATIC/temporary routes LOWER unmet on the cholinergic levers; above ADHD's clean-route floor)")
    print(f"  {'rank':4} {'gene':9} {'lev':4} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  reach                                                          (|h_sp|#)")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (non-actionable)"
        print(f"  {r['rank']:4} {r['gene']:9} {str(r['lever']):4} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  {r['reach_status']:61} (h_sp#{c['h_sp_rank_stiffest_first']:2}){act}")
    sf = res["substantive_finding"]
    print(f"  finding: leading ACTIONABLE {sf['leading_actionable_gene']} ({sf['leading_actionable_lever']}) #{sf['leading_actionable_rank']}; "
          f"highest-need {sf['highest_scoring_nonactionable_gene']} #{sf['highest_scoring_nonactionable_rank']} is {sf['highest_scoring_nonactionable_reach']}")
    print(f"  top actionable (reachable symptomatic levers): {sf['top_actionable_genes']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
