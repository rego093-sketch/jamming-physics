#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhd_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420) via the bipolar/epilepsy/depression/
schizophrenia/autism T-L prioritisers.

A small, transparent ranking that combines three CITED tiers --
  B = burden        (ADHD prevalence x lifelong impairment; ~5-7% of children, ~2.5% of adults, a
                     lifelong neurodevelopmental condition for a large fraction; GBD/Faraone-anchored,
                     indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem). THE ADHD SIGNATURE is the AUTISM
                     MIRROR: ADHD HAS established core pharmacology -- the DAT route (methylphenidate/
                     amphetamine), the NET route (atomoxetine), the alpha-2A route (guanfacine/clonidine)
                     -- so the REACHABLE drive-tone transporters (SLC6A3/SLC6A2/ADRA2A) have a LOWERED
                     unmet need (the DRD2-analogue ADHD HAS, that autism LACKED). U-floor here is the
                     LOWEST in the series. BUT the dominant GAIN-amplitude axis (TH/DBH/SNAP25, synthesis/
                     release) carries the unmet-need CEILING and is OUT OF REACH -- so the highest-need
                     targets are precisely the unreachable ones (the partial-fit signature).
  G = genetic/druggability evidence (replicated ADHD-gene support + tractability; the classic candidate
                     loci -- DAT1/SLC6A3 VNTR, DRD4 7R -- + Demontis 2019/2023 GWAS; transporters are
                     highly druggable, the synthesis/release enzymes far less so, DRD4 has no selective
                     agent in use).

each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.

SUBSTANTIVE FINDING (the ADHD analogue of autism's "inhibitory-restore above excitatory", here INVERTED
by reachability): the highest-need targets are ALL non-actionable -- the GA gain-amplitude genes
(TH/DBH/SNAP25) are OUT OF REACH of a drive-tone lever, and DRD4 (the most-replicated receptor variant)
has NO selective tractable agent. The cleanest ACTIONABLE direction, the dopamine transporter SLC6A3/DAT,
ranks only mid-table because its unmet need is LOWERED by the established methylphenidate/amphetamine
route. So the priority order makes the PARTIAL FIT concrete: the targets of greatest mechanistic need (the
GA synthesis/release axis) are exactly the ones the threshold frame cannot reach, while the reachable
transporters already carry established routes. This is the autism prioritiser INVERTED: autism had high
unmet everywhere and the actionable set was the inhibitory-restore L2 genes; ADHD has LOW unmet on the
reachable transporters and the highest-unmet set is the OUT-OF-REACH gain axis.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - efficacy=0: that an established APPROVED route exists is a CITED fact that LOWERS a UNMET-NEED tier;
    it is NOT an efficacy claim about any direction, and no molecule/dose/patient is ranked. ADHD is a
    neurodevelopmental DIFFERENCE, not only a deficit; the ranking surfaces where unmet MECHANISTIC need
    is greatest and which of those targets the frame can/cannot reach. It does NOT assert that any
    direction "treats", "normalises", or "cures" ADHD, and grants NO stimulant-misuse or cognitive-
    enhancement licence.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is
    NEVER folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude). The decoupling is the firewall made visible: the STIFFEST promoter read
    (SLC6A3/DAT) sits MID-table on priority (its established route lowers its unmet need), while the
    top-priority gene (the out-of-reach synthesis enzyme) has only a mid-stiffness read -- so stiffness
    cannot be driving the order. (This is the ADHD inverse of autism, where the stiffest read sat
    LOWEST.)
  - actionable=False marks genes the threshold/drive-tone frame cannot cleanly act on: TH/DBH/SNAP25/COMT
    (OUT OF REACH on the GA gain-amplitude axis) and DRD4 (replicated genetics but no selective agent).

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 adhd_burden_prioritisation.py  -> adhd_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "adhd_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis + reach_status. actionable=False where the frame cannot
# cleanly act: OUT OF REACH (GA gain-amplitude axis) or no selective tractable agent (DRD4).
# NOTE the ADHD U-signature (autism MIRROR): the REACHABLE catecholamine transporters carry a LOWERED
# unmet need because an established approved route exists (the DRD2-analogue ADHD HAS); the OUT-OF-REACH
# gain genes carry the unmet-need CEILING.
TIERS = {
  # ---- reachable drive-tone LEVERS (L3) ----
  "SLC6A3": dict(B=4, U=2, G=5, actionable=True, reach="reached (DT lever)",
      cite="the dopamine transporter (DAT1/SLC6A3); the primary molecular target of the established methylphenidate/amphetamine route and one of the most-studied ADHD candidate loci (the 3'-UTR VNTR) -- its UNMET-need tier is LOWERED by an established approved route (the DRD2-analogue ADHD HAS) (Cook 1995; Faraone 2021)"),
  "SLC6A2": dict(B=4, U=2, G=4, actionable=True, reach="reached (DT lever)",
      cite="the noradrenaline transporter (NET/SLC6A2); the molecular target of the established atomoxetine route (the non-stimulant arm) -- UNMET-need tier LOWERED by an approved route (Bymaster 2002; Faraone 2021)"),
  "ADRA2A": dict(B=3, U=2, G=4, actionable=True, reach="reached (DT lever)",
      cite="the alpha-2A adrenergic receptor (ADRA2A); the molecular target of the established guanfacine/clonidine route -- UNMET-need tier LOWERED by an approved route (Arnsten 2010; Faraone 2021)"),
  "SLC6A4": dict(B=3, U=4, G=3, actionable=True, reach="reached (DT lever)",
      cite="the serotonin transporter (5-HTT/SLC6A4); the arousal-tone arm reachable as drive-tone, but serotonergic agents are NOT an established ADHD-core route, so its UNMET-need tier stays HIGHER than the catecholamine transporters (the secondary monoaminergic arm) (Faraone 2021)"),
  "DRD4":   dict(B=4, U=4, G=3, actionable=False, reach="reached (DT lever) but no selective agent",
      cite="the dopamine D4 receptor (DRD4); the 7-repeat exon-3 VNTR is among the most-replicated ADHD candidate variants, but there is NO selective D4 agent in ADHD use -- strong genetics WITHOUT a clean tractable direction, so NOT actionable despite high replication (LaHoste 1996; Faraone 2021)"),
  # ---- OUT-OF-REACH gain-amplitude genes (GA) -- highest unmet, NOT reachable by a drive-tone lever ----
  "TH":     dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (GA gain axis)",
      cite="tyrosine hydroxylase (TH), rate-limiting catecholamine SYNTHESIS -- the sec.22 GAIN axis (the DOMINANT ADHD fault). No established route addresses synthesis (UNMET at the ceiling) and a drive-tone lever has NO handle on it -- OUT OF REACH, the partial-fit signature (Faraone 2021; sec.22)"),
  "DBH":    dict(B=3, U=5, G=3, actionable=False, reach="OUT-OF-REACH (GA gain axis)",
      cite="dopamine beta-hydroxylase (DBH), the DA->NA SYNTHESIS step -- a sec.22 GAIN-axis gene; no established route addresses it (UNMET at the ceiling) and the drive-tone frame cannot reach synthesis -- OUT OF REACH (Cubells 2000; sec.22)"),
  "SNAP25": dict(B=3, U=5, G=3, actionable=False, reach="OUT-OF-REACH (GA gain axis)",
      cite="SNAP-25, the SNARE vesicle-RELEASE protein (the coloboma-mouse ADHD model) -- a sec.22 GAIN-axis gene; release machinery is not addressed by any established route (UNMET at the ceiling) and a drive-tone lever cannot reach RELEASE -- OUT OF REACH (Hess 1992; sec.22)"),
  "COMT":   dict(B=3, U=4, G=3, actionable=False, reach="OUT-OF-REACH (GA gain axis, boundary)",
      cite="catechol-O-methyltransferase (COMT), prefrontal dopamine CATABOLIC clearance (the Val158Met polymorphism) -- a sec.22 GAIN-axis BOUNDARY gene; clearance is an amplitude term a drive-tone lever cannot set -- OUT OF REACH (Egan 2001; sec.22)"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["G"]*t["G"], 4)

def build():
    m = json.load(open(MAP))
    lever_by_gene = {e["gene"]: e for e in m["entries"]}
    oor_by_gene   = {e["gene"]: e for e in m["out_of_reach_targets"]["entries"]}
    all_by_gene   = {**lever_by_gene, **oor_by_gene}
    # combined stiffest-first |h_sp| rank across ALL nine genes (levers + out-of-reach)
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

    # the ADHD U-signature: the LOWEST unmet-need tier present (the established-route transporters)
    u_floor = min(t["U"] for t in TIERS.values())
    top_priority = rows[0]["gene"]

    # substantive finding: the leading ACTIONABLE (reachable drive-tone) gene vs the highest-scoring
    # NON-actionable gene (the out-of-reach gain enzyme)
    lead_act = next(r for r in rows if r["actionable"])
    blocked_top = next((r for r in rows if not r["actionable"]), None)
    act_top = [r["gene"] for r in actionable]
    return {
        "title": "Burden-weighted ADHD TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism T-L",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "adhd_unmet_need_signature": {
            "u_floor": u_floor,
            "reading": ("the ADHD signature -- the AUTISM MIRROR: ADHD HAS established core pharmacology "
                        "(the DAT/methylphenidate-amphetamine route, the NET/atomoxetine route, the "
                        "alpha-2A/guanfacine route), so the REACHABLE drive-tone transporters "
                        "(SLC6A3/SLC6A2/ADRA2A) have a LOWERED unmet-need tier (the DRD2-analogue ADHD "
                        "HAS, that autism LACKED). The unmet-need FLOOR here is %d -- the LOWEST in the "
                        "series, the inverse of autism's high floor. BUT the dominant GAIN-amplitude axis "
                        "(TH/DBH/SNAP25, synthesis/release) carries the unmet-need CEILING (5) AND is "
                        "out-of-reach -- so the highest-need targets are precisely the unreachable ones, "
                        "the partial-fit signature." % u_floor),
        },
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "efficacy=0: that an established APPROVED route exists is a CITED fact that LOWERS a "
                      "UNMET-NEED tier, NOT an efficacy claim about any direction; no molecule, dose, or "
                      "patient is ranked; ADHD is a neurodevelopmental DIFFERENCE, not only a deficit; the "
                      "ranking grants NO stimulant-misuse or cognitive-enhancement licence; and it does NOT "
                      "assert that any direction treats, normalises, or cures ADHD. gamma-|h_sp| "
                      "is carried ALONGSIDE as structural context and is NEVER folded into the score "
                      "(firewall: a promoter-stiffness read is not a clinical magnitude). SUBSTANTIVE "
                      "FINDING: the highest-need targets are ALL non-actionable -- the GA gain-amplitude "
                      "genes are OUT OF REACH of the drive-tone frame and DRD4 has no selective agent -- "
                      "while the cleanest ACTIONABLE direction (the dopamine transporter SLC6A3/DAT) ranks "
                      "mid-table because its unmet need is LOWERED by the established route. The priority "
                      "order makes the PARTIAL FIT concrete: the targets of greatest mechanistic need are "
                      "exactly the ones the frame cannot reach. This is the autism prioritiser INVERTED."),
        "substantive_finding": {
            "leading_actionable_gene": lead_act["gene"],
            "leading_actionable_lever": lead_act["lever"],
            "leading_actionable_rank": lead_act["rank"],
            "highest_scoring_nonactionable_gene": (blocked_top["gene"] if blocked_top else None),
            "highest_scoring_nonactionable_rank": (blocked_top["rank"] if blocked_top else None),
            "highest_scoring_nonactionable_reach": (blocked_top["reach_status"] if blocked_top else None),
            "top_actionable_genes": act_top,
            "reading": ("the highest-need targets are ALL non-actionable: the GA gain-amplitude genes "
                        "(TH/DBH/SNAP25) are OUT OF REACH of the drive-tone frame and DRD4 (the most-"
                        "replicated receptor variant) has no selective agent. The highest-scoring target "
                        "%s (#%d) is %s. The cleanest ACTIONABLE direction, %s (%s), ranks only #%d because "
                        "its UNMET need is LOWERED by the established route (the DRD2-analogue ADHD HAS). "
                        "So the priority order makes the PARTIAL FIT concrete -- the targets of greatest "
                        "mechanistic need (the GA synthesis/release axis) are exactly the ones the "
                        "threshold frame cannot reach, while the reachable transporters already carry "
                        "established routes. This ranks unmet MECHANISTIC need; it makes NO efficacy claim "
                        "(see the firewall: no direction is asserted to treat, normalise, or cure)."
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
            "reading": ("the stiffest promoter read (%s, a REACHABLE drive-tone transporter) sits at "
                        "priority #%d -- NOT the top -- because its established approved route LOWERS its "
                        "unmet need; while the top-priority gene (%s, on the out-of-reach gain axis) has "
                        "only the #%d-stiffest promoter. If promoter stiffness drove the ranking neither "
                        "could sit where it does. This is the ADHD inverse of autism (where the stiffest "
                        "read sat LOWEST); the decoupling is the firewall made visible."
                        % (stiffest, next(r["rank"] for r in rows if r["gene"] == stiffest),
                           top_priority, next(r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                                              for r in rows if r["gene"] == top_priority))),
        },
        "top_actionable_genes": act_top,
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "adhd_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted ADHD TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0)")
    print(f"  U-floor: {res['adhd_unmet_need_signature']['u_floor']}  (established core routes LOWER unmet on reachable transporters -- autism mirror)")
    print(f"  {'rank':4} {'gene':9} {'lev':4} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  reach                       (|h_sp|#)")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (non-actionable)"
        print(f"  {r['rank']:4} {r['gene']:9} {str(r['lever']):4} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  {r['reach_status']:26} (h_sp#{c['h_sp_rank_stiffest_first']:2}){act}")
    sf = res["substantive_finding"]
    print(f"  finding: leading ACTIONABLE {sf['leading_actionable_gene']} ({sf['leading_actionable_lever']}) #{sf['leading_actionable_rank']}; "
          f"highest-need {sf['highest_scoring_nonactionable_gene']} #{sf['highest_scoring_nonactionable_rank']} is {sf['highest_scoring_nonactionable_reach']}")
    print(f"  top actionable (reachable drive-tone): {sf['top_actionable_genes']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
