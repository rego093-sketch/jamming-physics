#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
addiction_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420) via the bipolar/epilepsy/depression/
schizophrenia/autism/ADHD T-L prioritisers.

A small, transparent ranking that combines three CITED tiers --
  B = burden        (substance-use-disorder prevalence x impairment; SUDs are among the highest-burden
                     conditions worldwide -- the opioid-overdose crisis, tobacco as the leading
                     preventable cause of death, alcohol-use disorder; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem). THE ADDICTION SIGNATURE is a MIDDLE
                     case between ADHD and autism: addiction HAS established core pharmacology -- the
                     mu-opioid route (naltrexone), the nicotinic route (varenicline), the DAT route
                     (bupropion), the glutamate route (acamprosate), the GABA route (topiramate, off-label)
                     -- so the REACHABLE reward-drive/plasticity/inhibitory levers carry only a MODERATE
                     unmet need; but every one of those routes is only PARTIALLY effective with HIGH
                     RELAPSE, so the unmet FLOOR (3) sits ABOVE ADHD's clean-route floor (2) and below
                     autism's high floor. BUT the dominant SG (consolidated sensitisation-gain) axis
                     (FOSB/BDNF/CREB1/ARC, the learned plastic trace that drives relapse) carries the
                     unmet-need CEILING and is OUT OF REACH -- so the highest-need targets are precisely
                     the unreachable ones (the partial-fit signature).
  G = genetic/druggability evidence (replicated addiction-gene support + tractability; OPRM1 A118G,
                     CHRNA5 rs16969968 (the strongest nicotine-dependence GWAS hit), DRD2/ANKK1 Taq1A,
                     GABRA2 alcohol GWAS, SLC6A3 candidate; receptors/transporters are highly druggable,
                     the transcription/plasticity effectors FOSB/CREB1/ARC far less so).

each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.

SUBSTANTIVE FINDING (the addiction analogue of ADHD's "highest need is out of reach", here for a DEEPER
reason): the highest-need targets are ALL non-actionable -- the SG sensitisation-gain genes
(FOSB/BDNF/CREB1/ARC) carry the unmet CEILING (no route addresses the consolidated learned trace) and are
OUT OF REACH of a threshold/drive lever. The cleanest ACTIONABLE directions (the mu-opioid receptor OPRM1,
the nicotinic CHRNA5, the dopamine transporter SLC6A3/DAT) rank just below the top because their unmet
need is LOWERED by an established -- though only partially effective -- route. So the priority order makes
the PARTIAL FIT concrete: the targets of greatest mechanistic need (the SG consolidated-gain axis) are
exactly the ones the threshold frame cannot reach, because that axis is a LEARNED/plastic (E0-layer)
variable, not an instantaneous fold. This extends the ADHD partial-fit signature (highest need out of
reach) to a CONSOLIDATED gain -- the convergence point with the E0 dynamics layer.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - efficacy=0: that an established APPROVED route exists is a CITED fact that LOWERS a UNMET-NEED tier;
    it is NOT an efficacy claim about any direction, and no molecule/dose/patient is ranked. Addiction is
    a TREATABLE MEDICAL CONDITION, not a moral failing; the ranking surfaces where unmet MECHANISTIC need
    is greatest and which of those targets the frame can/cannot reach. It does NOT assert that any
    direction "treats", "cures", or "ends" addiction, grants NO route to obtain or use any substance, and
    makes NO miracle-cure claim.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NEVER folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude). The decoupling is the firewall made visible: the STIFFEST promoter read
    (SLC6A3/DAT) sits MID-table on priority (its established bupropion route lowers its unmet need),
    while the top-priority gene (the out-of-reach FOSB/deltaFosB sensitisation switch) has only a
    mid-stiffness read -- so stiffness cannot be driving the order.
  - actionable=False marks genes the threshold/drive frame cannot cleanly act on: FOSB/BDNF/CREB1/ARC
    (OUT OF REACH on the SG consolidated-sensitisation-gain axis -- the learned plastic trace).

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 addiction_burden_prioritisation.py  -> addiction_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "addiction_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis + reach_status. actionable=False where the frame cannot
# cleanly act: OUT OF REACH (SG consolidated-sensitisation-gain axis -- the learned plastic trace).
# NOTE the addiction U-signature (a MIDDLE case): the REACHABLE reward-drive/plasticity/inhibitory levers
# carry a MODERATE unmet need because an established -- but only PARTIALLY effective, high-relapse -- route
# exists; the OUT-OF-REACH SG genes carry the unmet-need CEILING (no route reaches the consolidated trace).
TIERS = {
  # ---- reachable reward-drive LEVERS (L3) ----
  "OPRM1":  dict(B=5, U=3, G=5, actionable=True, reach="reached (L3 reward drive)",
      cite="the mu-opioid receptor (OPRM1, the A118G functional variant); the molecular target of the established naltrexone/naloxone route in opioid- and alcohol-use disorder -- its UNMET-need tier is LOWERED by an established route, but the route is only PARTIALLY effective with high relapse and poor adherence, so unmet stays MODERATE (Bond 1998; Volkow 2016)"),
  "CHRNA5": dict(B=5, U=3, G=4, actionable=True, reach="reached (L3 reward drive)",
      cite="the alpha-5 nicotinic acetylcholine receptor subunit (CHRNA5, rs16969968 -- the strongest replicated nicotine-dependence GWAS locus); the nicotinic-reward arm reachable via the established varenicline/cytisine route -- UNMET LOWERED by an established but partially effective, relapse-prone route (the smoking-cessation arm) (Bierut 2008; Volkow 2016)"),
  "SLC6A3": dict(B=4, U=3, G=5, actionable=True, reach="reached (L3 reward drive)",
      cite="the dopamine transporter (DAT/SLC6A3); the reuptake node that sets ambient dopamine tone and the target of bupropion in smoking cessation -- UNMET LOWERED by the established (partial) bupropion route; highly druggable transporter (Volkow 2016)"),
  "DRD2":   dict(B=4, U=4, G=4, actionable=True, reach="reached (L3 reward drive) but no clean agonist route",
      cite="the dopamine D2 receptor (DRD2/ANKK1 Taq1A, among the most-replicated addiction candidate variants); D2 availability is REDUCED in addiction, so a clean D2-direction is mechanistically subtle (agonism is reinforcing, antagonism blunts all reward) -- reachable as a drive-tone read but with NO established clean route, so unmet stays HIGH (Blum 1990; Volkow 2016)"),
  "OPRK1":  dict(B=3, U=4, G=4, actionable=True, reach="reached (L3 anti-reward arm) but route experimental",
      cite="the kappa-opioid receptor (OPRK1); the ANTI-reward/dysphoria-drive arm (nalmefene partial-antagonism, experimental kappa antagonists) -- a mechanistically distinct direction with NO established clean route in addiction, so its UNMET need stays HIGH (Chavkin 2011; Volkow 2016)"),
  # ---- reachable glutamate-plasticity SUBSTRATE LEVERS (L1) ----
  "GRIN2A": dict(B=4, U=4, G=3, actionable=True, reach="reached (L1 glutamate-plasticity substrate)",
      cite="the NMDA NR2A subunit (GRIN2A); the glutamatergic plasticity substrate reachable via the acamprosate/N-acetylcysteine direction -- the established acamprosate route is only WEAKLY/partially effective in alcohol-use disorder, so unmet stays HIGH (Mason 2006; Volkow 2016)"),
  "GRIN2B": dict(B=4, U=4, G=3, actionable=True, reach="reached (L1 glutamate-plasticity substrate)",
      cite="the NMDA NR2B subunit (GRIN2B); the glutamatergic plasticity substrate of the same acamprosate/NAC direction -- partially effective at best, unmet stays HIGH (Mason 2006; Volkow 2016)"),
  # ---- reachable inhibitory-RESTORE LEVERS (L2) ----
  "GABRA2": dict(B=4, U=4, G=4, actionable=True, reach="reached (L2 inhibitory restore)",
      cite="the GABA-A alpha-2 subunit (GABRA2, a replicated alcohol-dependence GWAS locus); the inhibitory-restore arm reachable via the topiramate direction -- topiramate is OFF-LABEL and partially effective in alcohol-use disorder with no clean approved GABA-A route, so unmet stays HIGH (Edenberg 2004; Volkow 2016)"),
  "GABRG3": dict(B=3, U=4, G=3, actionable=True, reach="reached (L2 inhibitory restore)",
      cite="the GABA-A gamma-3 subunit (GABRG3, an alcohol-dependence-linked locus); the inhibitory-restore arm of the same topiramate direction -- off-label, partial, no clean approved route, unmet stays HIGH (Dick 2004; Volkow 2016)"),
  # ---- OUT-OF-REACH sensitisation-gain genes (SG) -- highest unmet, NOT reachable by a threshold/drive lever ----
  "FOSB":   dict(B=5, U=5, G=3, actionable=False, reach="OUT-OF-REACH (SG sensitisation-gain axis)",
      cite="deltaFosB (FOSB), the MASTER sensitisation transcription factor that accumulates with repeated exposure and drives the consolidated low-threshold reward state -- the sec.26 E0 GAIN axis (the DOMINANT addiction fault, the relapse driver). No route addresses the consolidated trace (UNMET at the ceiling) and a threshold/drive lever has NO handle on a learned plastic gain -- OUT OF REACH, the partial-fit signature (Nestler 2008; sec.26)"),
  "BDNF":   dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (SG sensitisation-gain axis)",
      cite="brain-derived neurotrophic factor (BDNF); the activity-dependent remodelling factor that consolidates sensitised reward circuitry -- a sec.26 E0 GAIN-axis effector; no route addresses the remodelled trace (UNMET at the ceiling) and the threshold frame cannot reach learned plasticity -- OUT OF REACH (Russo 2009; sec.26)"),
  "CREB1":  dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (SG sensitisation-gain axis)",
      cite="CREB (CREB1), the cAMP-response-element binding transcription factor that runs the tolerance/dependence programme -- a sec.26 E0 GAIN-axis effector; the consolidated programme is not addressed by any route (UNMET at the ceiling) and a fold lever cannot set a learned gain -- OUT OF REACH (Nestler 2008; sec.26)"),
  "ARC":    dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (SG sensitisation-gain axis)",
      cite="ARC/Arg3.1 (ARC), the activity-regulated effector of synaptic consolidation and AMPA trafficking that stabilises plastic change -- a sec.26 E0 GAIN-axis effector; consolidation is not addressed by any route (UNMET at the ceiling) and the threshold frame has no handle on it -- OUT OF REACH (Shepherd 2011; sec.26)"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["G"]*t["G"], 4)

def build():
    m = json.load(open(MAP))
    lever_by_gene = {e["gene"]: e for e in m["entries"]}
    oor_by_gene   = {e["gene"]: e for e in m["out_of_reach_targets"]["entries"]}
    all_by_gene   = {**lever_by_gene, **oor_by_gene}
    # combined stiffest-first |h_sp| rank across ALL thirteen genes (levers + out-of-reach)
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

    # the addiction U-signature: the LOWEST unmet-need tier present (the established-but-partial routes)
    u_floor = min(t["U"] for t in TIERS.values())
    top_priority = rows[0]["gene"]

    # substantive finding: the leading ACTIONABLE (reachable) gene vs the highest-scoring NON-actionable
    # gene (the out-of-reach SG sensitisation-gain effector)
    lead_act = next(r for r in rows if r["actionable"])
    blocked_top = next((r for r in rows if not r["actionable"]), None)
    act_top = [r["gene"] for r in actionable]
    return {
        "title": "Burden-weighted addiction TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD T-L",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "addiction_unmet_need_signature": {
            "u_floor": u_floor,
            "reading": ("the addiction signature -- a MIDDLE case between ADHD and autism: addiction HAS "
                        "established core pharmacology (the mu-opioid/naltrexone route, the "
                        "nicotinic/varenicline route, the DAT/bupropion route, the glutamate/acamprosate "
                        "route, the GABA/topiramate off-label route), so the REACHABLE reward-drive, "
                        "glutamate-plasticity and inhibitory-restore levers carry only a MODERATE unmet "
                        "need. The unmet-need FLOOR here is %d -- ABOVE ADHD's clean-route floor of 2 "
                        "(because every addiction route is only PARTIALLY effective with HIGH RELAPSE) and "
                        "below autism's high floor. BUT the dominant SG (consolidated sensitisation-gain) "
                        "axis (FOSB/BDNF/CREB1/ARC, the learned plastic trace that drives relapse) carries "
                        "the unmet-need CEILING (5) AND is out-of-reach -- so the highest-need targets are "
                        "precisely the unreachable ones, the partial-fit signature, for a DEEPER reason "
                        "than ADHD (a consolidated/LEARNED gain, not just a gain)." % u_floor),
        },
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "efficacy=0: that an established APPROVED route exists is a CITED fact that LOWERS a "
                      "UNMET-NEED tier, NOT an efficacy claim about any direction; no molecule, dose, or "
                      "patient is ranked; addiction is a TREATABLE MEDICAL CONDITION, not a moral failing; "
                      "the ranking grants NO route to obtain or use any substance and makes NO miracle-cure "
                      "claim; and it does NOT assert that any direction treats, cures, or ends addiction. "
                      "gamma-|h_sp| is carried ALONGSIDE as structural context and is NEVER folded into the "
                      "score (firewall: a promoter-stiffness read is not a clinical magnitude). SUBSTANTIVE "
                      "FINDING: the highest-need targets are ALL non-actionable -- the SG sensitisation-gain "
                      "genes (FOSB/BDNF/CREB1/ARC) carry the unmet CEILING and are OUT OF REACH of the "
                      "threshold/drive frame -- while the cleanest ACTIONABLE directions (OPRM1/CHRNA5/"
                      "SLC6A3) rank just below the top because their unmet need is LOWERED by an "
                      "established (though partial) route. The priority order makes the PARTIAL FIT "
                      "concrete: the targets of greatest mechanistic need are exactly the ones the frame "
                      "cannot reach, because the SG axis is a learned/plastic (E0-layer) variable -- the "
                      "convergence point with the dynamics route."),
        "substantive_finding": {
            "leading_actionable_gene": lead_act["gene"],
            "leading_actionable_lever": lead_act["lever"],
            "leading_actionable_rank": lead_act["rank"],
            "highest_scoring_nonactionable_gene": (blocked_top["gene"] if blocked_top else None),
            "highest_scoring_nonactionable_rank": (blocked_top["rank"] if blocked_top else None),
            "highest_scoring_nonactionable_reach": (blocked_top["reach_status"] if blocked_top else None),
            "top_actionable_genes": act_top,
            "reading": ("the highest-need targets are ALL non-actionable: the SG sensitisation-gain genes "
                        "(FOSB/BDNF/CREB1/ARC) carry the unmet CEILING (no route reaches the consolidated "
                        "learned trace) and are OUT OF REACH of the threshold/drive frame. The "
                        "highest-scoring target %s (#%d) is %s. The cleanest ACTIONABLE direction, %s (%s), "
                        "ranks #%d because its UNMET need is LOWERED by an established -- though only "
                        "partially effective, relapse-prone -- route. So the priority order makes the "
                        "PARTIAL FIT concrete: the targets of greatest mechanistic need (the SG "
                        "consolidated-gain axis) are exactly the ones the threshold frame cannot reach, "
                        "while the reachable levers already carry established (partial) routes. This ranks "
                        "unmet MECHANISTIC need; it makes NO efficacy claim (see the firewall: no direction "
                        "is asserted to treat, cure, or end the disorder)."
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
            "reading": ("the stiffest promoter read (%s, a REACHABLE reward-drive transporter) sits at "
                        "priority #%d -- NOT the top -- because its established (partial) bupropion route "
                        "LOWERS its unmet need; while the top-priority gene (%s, on the out-of-reach SG "
                        "sensitisation-gain axis) has only the #%d-stiffest promoter. If promoter stiffness "
                        "drove the ranking neither could sit where it does. The decoupling is the firewall "
                        "made visible: a promoter-stiffness read is carried alongside but never folded into "
                        "the clinical priority."
                        % (stiffest, next(r["rank"] for r in rows if r["gene"] == stiffest),
                           top_priority, next(r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                                              for r in rows if r["gene"] == top_priority))),
        },
        "top_actionable_genes": act_top,
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "addiction_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted addiction TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  U-floor: {res['addiction_unmet_need_signature']['u_floor']}  (established but PARTIAL routes LOWER unmet on reachable levers; above ADHD's clean-route floor)")
    print(f"  {'rank':4} {'gene':9} {'lev':4} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  reach                                      (|h_sp|#)")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (non-actionable)"
        print(f"  {r['rank']:4} {r['gene']:9} {str(r['lever']):4} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  {r['reach_status']:41} (h_sp#{c['h_sp_rank_stiffest_first']:2}){act}")
    sf = res["substantive_finding"]
    print(f"  finding: leading ACTIONABLE {sf['leading_actionable_gene']} ({sf['leading_actionable_lever']}) #{sf['leading_actionable_rank']}; "
          f"highest-need {sf['highest_scoring_nonactionable_gene']} #{sf['highest_scoring_nonactionable_rank']} is {sf['highest_scoring_nonactionable_reach']}")
    print(f"  top actionable (reachable levers): {sf['top_actionable_genes']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
