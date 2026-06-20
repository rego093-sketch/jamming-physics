#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocd_burden_prioritisation.py  —  burden-weighted prioritisation of TARGETS (not drugs).
Inherited from analgesic v2.0 M10 (DOI 10.5281/zenodo.20733420) via the bipolar/epilepsy/depression/
schizophrenia/autism/ADHD/addiction/Alzheimer's T-L prioritisers.

A small, transparent ranking that combines three CITED tiers --
  B = burden        (OCD prevalence x impairment x chronicity; OCD has a ~2% lifetime prevalence, is
                     typically chronic and disabling, and is among the higher-burden psychiatric
                     conditions; GBD-anchored, indication-level)
  U = unmet need    (drug-resistance of the mechanistic sub-problem). THE OCD SIGNATURE: the REACHABLE
                     surface is REACHABLE-BUT-PARTIAL. The serotonergic-drive lever (SLC6A4 via the
                     established SSRI/clomipramine route) carries a MODERATE unmet need where an
                     established route exists -- but that route is only PARTIALLY effective (a large
                     fraction of patients have residual or refractory symptoms even with adequate
                     pharmacotherapy + exposure-response-prevention), so the unmet FLOOR (3) sits ABOVE
                     ADHD's clean-route floor (2). The glutamatergic levers (SLC1A1/GRIN2B/GRIK2) carry a
                     HIGHER unmet need because the glutamate-modulator route (riluzole/memantine/NAC) is
                     INVESTIGATIONAL and unapproved. BUT the dominant fault -- the pathological-
                     stabilisation LOCK axis (DLGAP3/SAPAP3 the corticostriatal scaffold, SLITRK5, PTPRD,
                     BTBD3) -- carries the unmet-need CEILING (the refractory loop-LOCK has NO molecular
                     therapy; deep-brain stimulation of the CSTC loop is the only option for the most
                     refractory) AND is OUT OF REACH of a threshold/drive lever, because that axis is an
                     E0 STABILISATION -- an over-deep basin / hysteresis, a pathological lock, the THIRD
                     distinct E0 mode (after addiction's GAIN and Alzheimer's DECAY), not an instantaneous
                     fold. So the deepest unmet is precisely the unreachable loop-lock.
  G = genetic/druggability evidence (replicated OCD-gene support + tractability; SLC1A1/EAAT3 -- the most
                     replicated OCD candidate/linkage gene and a highly druggable transporter; DRD2 the
                     antipsychotic-augmentation target; the serotonergic SLC6A4/HTR2A/HTR1B nodes; but the
                     loop-LOCK effectors -- the corticostriatal scaffold DLGAP3/SAPAP3, the synaptic-
                     adhesion SLITRK5/PTPRD, the circuit-patterning BTBD3 -- are canonical circuit-model /
                     GWAS genes that are HARD to drug as scaffolds/adhesion molecules).

each on a cited 1..5 scale, under DECLARED weights, to surface the highest-leverage levers.

WEIGHTS ARE DECLARED, NOT TUNED:  w_B=0.40, w_U=0.35, w_G=0.25.  score = w_B*B + w_U*U + w_G*G.

SUBSTANTIVE FINDING (the OCD analogue of the partial-fit signature, expressed through the unmet CEILING):
the DEEPEST-unmet targets (U=5) are ALL non-actionable -- the LOCK loop-fixation genes (DLGAP3/SLITRK5/
PTPRD/BTBD3) carry the unmet CEILING (the refractory loop-lock, no molecular therapy, DBS-only) and are
OUT OF REACH of a threshold/drive lever. The leading ACTIONABLE target is the glutamate transporter
SLC1A1 (the most replicated OCD candidate gene, the glutamate-modulator direction) -- reachable, and the
single highest-leverage molecular handle, but it only PARTIALLY helps because it nudges the instantaneous
operating point and does NOT unstick the loop. So the priority order makes the PARTIAL FIT concrete: the
targets of greatest mechanistic NEED (the loop-LOCK) are exactly the ones the threshold frame cannot reach,
because that axis is a pathological-stabilisation E0-LOCK -- an over-deep basin / hysteresis -- not an
instantaneous fold. This extends the partial-fit signature to a STABILISATION / LOCK, the structural
sibling of (and third distinct mode after) addiction's consolidated GAIN and Alzheimer's degenerative
DECAY.

HONESTY (binding):
  - B/U/G are CITED tiers; the weights are an explicit editorial choice -> the ranking is [F] from cited
    tiers + declared weights, NOT a [V] engine output.
  - efficacy=0: that an established serotonergic route exists is a CITED fact that LOWERS a UNMET-NEED
    tier; it is NOT an efficacy claim about any direction, and no molecule/dose/patient is ranked. The
    serotonergic first-line is only PARTIALLY effective and does NOT unstick the loop-lock. The ranking
    surfaces where unmet MECHANISTIC need is greatest and which of those targets the frame can/cannot
    reach. It does NOT assert that any direction "treats", "cures", or permanently "stops" OCD, claims NO
    cure for the reachable levers, and makes NO miracle-cure claim. OCD is a treatable medical condition
    and intrusive thoughts are a symptom, not a moral failing.
  - the engine read's place (lever, gamma-|h_sp|) is carried ALONGSIDE as structural context; it is NEVER
    folded into the priority score (the firewall forbids equating a promoter-stiffness read with a
    clinical magnitude, a basin depth, a hysteresis width, or the strength of the compulsive lock). The
    decoupling is the firewall made visible: the STIFFEST promoter read (DLGAP3) does NOT sit at the top
    of priority, and the top-priority gene (the actionable SLC1A1) has only a mid-stiffness read -- so
    stiffness cannot be driving the order.
  - actionable=False marks genes the threshold/drive frame cannot cleanly act on: DLGAP3/SLITRK5/PTPRD/
    BTBD3 (OUT OF REACH on the LOCK pathological-stabilisation axis -- the E0-stabilisation / loop-lock
    trace).

No tuning: fixed cited tiers + fixed declared weights + deterministic sort.

Run:  python3 ocd_burden_prioritisation.py  -> ocd_burden_prioritisation.json
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "ocd_threshold_levers_results.json")

WEIGHTS = {"B": 0.40, "U": 0.35, "G": 0.25}

# CITED tiers (B,U,G in 1..5) + one-line basis + reach_status. actionable=False where the frame cannot
# cleanly act: OUT OF REACH (LOCK pathological-stabilisation axis -- the loop-lock E0-stabilisation trace).
# NOTE the OCD U-signature: the REACHABLE surface is REACHABLE-BUT-PARTIAL. The serotonergic route (SLC6A4)
# carries a MODERATE unmet; the glutamate levers a HIGHER unmet (investigational); the OUT-OF-REACH LOCK
# genes carry the unmet CEILING (the refractory loop-lock, no molecular therapy -- DBS only).
TIERS = {
  # ---- reachable glutamatergic-excitatory LEVERS (L1; REDUCE the hyperactive loop drive) ----
  "SLC1A1": dict(B=5, U=4, G=5, actionable=True, reach="reached (L1 glutamatergic excitatory; investigational route)",
      cite="the neuronal glutamate transporter EAAT3 (SLC1A1, 9p24); the MOST replicated OCD candidate / linkage gene and a highly druggable transporter -- the single highest-leverage molecular handle. The glutamate-modulator direction (riluzole / N-acetylcysteine) is INVESTIGATIONAL and unapproved, so unmet stays HIGH; reachable but only PARTIALLY helps (it nudges the operating point, not the loop-lock) (Arnold 2006; Pittenger 2011)"),
  "GRIN2B": dict(B=4, U=4, G=3, actionable=True, reach="reached (L1 glutamatergic excitatory)",
      cite="the NMDA NR2B subunit (GRIN2B); the NMDA arm of the glutamate-modulator (memantine-class) direction, with OCD candidate-gene support. The route is investigational/modest, so unmet stays MODERATE-HIGH (Arnold 2004; Pittenger 2011)"),
  "GRIK2": dict(B=3, U=4, G=3, actionable=True, reach="reached (L1 glutamatergic excitatory)",
      cite="the kainate GluK2 subunit (GRIK2); a secondary glutamatergic-excitatory node with OCD candidate-gene support -- no approved route, unmet stays MODERATE-HIGH (Delorme 2004; Sampaio 2011)"),
  # ---- reachable serotonergic/dopaminergic-drive LEVERS (L3, the DOMINANT lever) ----
  "SLC6A4": dict(B=5, U=3, G=5, actionable=True, reach="reached (L3 serotonergic drive; established route)",
      cite="the serotonin transporter SERT (SLC6A4); the molecular target of the established SSRI / clomipramine first-line for OCD. Its UNMET-need tier is LOWERED by an established route, but that route is only PARTIALLY effective (large residual / refractory fraction even with adequate pharmacotherapy + ERP), so unmet stays MODERATE; a highly druggable transporter (Soomro 2008; Fineberg 2012)"),
  "DRD2": dict(B=4, U=4, G=4, actionable=True, reach="reached (L3 dopaminergic drive; augmentation route)",
      cite="the D2 dopamine receptor (DRD2); the target of antipsychotic augmentation for SSRI-refractory / tic-related OCD -- an augmentation route exists but is partial and for refractory cases only, so the reachable lever carries a HIGH unmet need (Bloch 2006; Dougherty 2004)"),
  "HTR2A": dict(B=4, U=4, G=3, actionable=True, reach="reached (L3 serotonergic drive)",
      cite="the 5-HT2A serotonin receptor (HTR2A); a serotonergic-drive node with OCD candidate-gene support, modulated by the serotonergic first-line as a receptor-level direction -- no clean receptor-specific approved OCD route, so unmet stays HIGH (Saiz 2008)"),
  "HTR1B": dict(B=4, U=4, G=3, actionable=True, reach="reached (L3 serotonergic drive)",
      cite="the 5-HT1B serotonin autoreceptor (HTR1B); a terminal-release autoreceptor with OCD candidate-gene / provocation support -- no clean receptor-specific approved route, so unmet stays HIGH (Mundo 2002)"),
  # ---- reachable inhibitory-RESTORE LEVER (L2; SPARSE) ----
  "GABRA1": dict(B=3, U=4, G=2, actionable=True, reach="reached (L2 inhibitory restore; SPARSE)",
      cite="the GABA-A alpha-1 subunit (GABRA1); the single, sparse inhibitory-restore node (reduced cortical GABA is reported in OCD; benzodiazepine is an adjunct). No approved GABAergic OCD route and a thin evidence base, so the sparse reachable lever carries a HIGH unmet need but modest druggability evidence (Simpson 2012)"),
  # ---- OUT-OF-REACH loop-LOCK genes (LOCK) -- DEEPEST unmet (U=5), NOT reachable by a threshold/drive lever ----
  "DLGAP3": dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (LOCK pathological-stabilisation axis; E0 stabilisation)",
      cite="DLGAP3 / SAPAP3; the corticostriatal postsynaptic-density scaffold whose knockout produces compulsive overgrooming -- the canonical mouse model of the OCD loop-LOCK. The refractory loop-lock is the DOMINANT OCD fault and has NO molecular therapy (deep-brain stimulation of the CSTC loop is the only option for the most refractory), so unmet is at the CEILING. A scaffold is HARD to drug, and a threshold/drive lever has NO handle on a pathological-stabilisation E0-LOCK (an over-deep basin / hysteresis, not a fold) -- OUT OF REACH, the partial-fit signature (Welch 2007)"),
  "SLITRK5": dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (LOCK pathological-stabilisation axis; E0 stabilisation)",
      cite="SLITRK5; a corticostriatal synaptic-adhesion molecule whose knockout also produces OCD-like overgrooming -- a circuit-fixation arm of the loop-lock. Disease-modification of the loop-lock is at the unmet ceiling and a synaptic-adhesion molecule is hard to drug; the pathological-stabilisation E0-LOCK axis is OUT OF REACH of a threshold lever (Shmelkov 2010)"),
  "PTPRD": dict(B=4, U=5, G=3, actionable=False, reach="OUT-OF-REACH (LOCK pathological-stabilisation axis; E0 stabilisation)",
      cite="PTPRD; a presynaptic synaptic-adhesion receptor-phosphatase implicated by OCD GWAS that organises synapse formation -- a circuit-fixation arm of the loop-lock. The loop-lock has no molecular therapy (unmet ceiling) and the pathological-stabilisation E0-LOCK axis is OUT OF REACH of a threshold lever (IOCDF-GC 2018)"),
  "BTBD3": dict(B=3, U=5, G=3, actionable=False, reach="OUT-OF-REACH (LOCK pathological-stabilisation axis; E0 stabilisation)",
      cite="BTBD3; a regulator of dendritic orientation and activity-dependent circuit patterning implicated by OCD GWAS -- a circuit-fixation arm of the loop-lock. Circuit-architecture disease-modification is unproven (unmet ceiling) and the pathological-stabilisation E0-LOCK axis is OUT OF REACH of a threshold lever (Stewart 2013)"),
}

def score(t):
    return round(WEIGHTS["B"]*t["B"] + WEIGHTS["U"]*t["U"] + WEIGHTS["G"]*t["G"], 4)

def build():
    m = json.load(open(MAP))
    lever_by_gene = {e["gene"]: e for e in m["entries"]}
    oor_by_gene   = {e["gene"]: e for e in m["out_of_reach_targets"]["entries"]}
    all_by_gene   = {**lever_by_gene, **oor_by_gene}
    # combined stiffest-first |h_sp| rank across ALL twelve genes (levers + out-of-reach)
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

    # the OCD U-signature: the LOWEST unmet-need tier present (the established-but-partial serotonergic route)
    u_floor = min(t["U"] for t in TIERS.values())
    u_ceiling = max(t["U"] for t in TIERS.values())
    top_priority = rows[0]["gene"]

    # substantive finding: the leading ACTIONABLE (reachable) gene vs the highest-scoring NON-actionable
    # gene (the out-of-reach LOCK loop-fixation effector); also the deepest-unmet (U=5) set
    lead_act = next(r for r in rows if r["actionable"])
    blocked_top = next((r for r in rows if not r["actionable"]), None)
    act_top = [r["gene"] for r in actionable]
    deepest_unmet_genes = sorted([g for g, t in TIERS.items() if t["U"] == u_ceiling])
    deepest_unmet_all_oor = all(not TIERS[g]["actionable"] for g in deepest_unmet_genes)
    return {
        "title": "Burden-weighted OCD TARGET prioritisation (cited tiers + declared weights)",
        "inherited_from": "analgesic_threshold_logic v2.0 M10 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction/Alzheimer's T-L",
        "weights_declared": WEIGHTS,
        "scale": "B/U/G cited on 1..5; score = 0.40*B + 0.35*U + 0.25*G (range 1..5)",
        "ocd_unmet_need_signature": {
            "u_floor": u_floor,
            "deepest_unmet_genes": deepest_unmet_genes,
            "deepest_unmet_all_out_of_reach": deepest_unmet_all_oor,
            "reading": ("the OCD signature: the REACHABLE surface is REACHABLE-BUT-PARTIAL. The serotonergic-"
                        "drive lever (SLC6A4) carries only a MODERATE unmet need where an established route "
                        "exists (the SSRI / clomipramine first-line), but that route is only "
                        "PARTIALLY effective (a large residual / refractory fraction even with adequate "
                        "pharmacotherapy + exposure-response-prevention), so the unmet-need FLOOR here is %d "
                        "-- ABOVE ADHD's clean-route floor of 2; the glutamate levers (SLC1A1/GRIN2B/GRIK2) "
                        "sit higher (the glutamate-modulator route is investigational/unapproved) and the "
                        "dopaminergic/serotonergic-receptor and sparse inhibitory levers higher still. BUT "
                        "the dominant fault -- the pathological-stabilisation LOCK axis (DLGAP3/SAPAP3 the "
                        "corticostriatal scaffold, SLITRK5, PTPRD, BTBD3) -- carries the unmet-need CEILING "
                        "(%d): the refractory loop-LOCK has NO molecular therapy (deep-brain stimulation of "
                        "the CSTC loop is the only option for the most refractory). That axis is OUT OF "
                        "REACH of a threshold/drive lever because it is an E0 STABILISATION -- an over-deep "
                        "basin / hysteresis, a pathological lock, the THIRD distinct E0 mode (after "
                        "addiction's GAIN and Alzheimer's DECAY), not an instantaneous fold. So the deepest "
                        "unmet (U=%d) is carried ENTIRELY by the out-of-reach loop-lock genes (%s), the "
                        "partial-fit signature." % (u_floor, u_ceiling, u_ceiling, ", ".join(deepest_unmet_genes))),
        },
        "principle": ("ranks READS/TARGETS, not drugs. B/U/G are CITED tiers; the weights are a declared "
                      "editorial choice -> the ranking is [F] from tiers+weights, NOT a [V] engine output. "
                      "efficacy=0: that an established serotonergic route exists is a CITED fact that LOWERS "
                      "a UNMET-NEED tier, NOT an efficacy claim about any direction; no molecule, dose, or "
                      "patient is ranked; the serotonergic first-line is only PARTIALLY effective and does "
                      "NOT unstick the loop-lock; the ranking claims NO cure for the reachable levers, "
                      "grants NO miracle cure, and does NOT assert that any direction treats, cures, or "
                      "permanently stops OCD; OCD is a treatable medical condition and intrusive thoughts "
                      "are a symptom, not a moral failing. gamma-|h_sp| is carried ALONGSIDE as structural "
                      "context and is NEVER folded into the score (firewall: a promoter-stiffness read is "
                      "not a clinical magnitude, a basin depth, a hysteresis width, or the strength of the "
                      "compulsive lock). SUBSTANTIVE FINDING: the DEEPEST-unmet targets (U=5) are ALL "
                      "non-actionable -- the LOCK loop-fixation genes (DLGAP3/SLITRK5/PTPRD/BTBD3) carry "
                      "the unmet CEILING (the refractory loop-lock, no molecular therapy) and are OUT OF "
                      "REACH of the threshold/drive frame -- while the leading ACTIONABLE target (the "
                      "glutamate transporter SLC1A1, the most replicated OCD gene) is reachable and the "
                      "single highest-leverage molecular handle, yet only PARTIALLY helps because it nudges "
                      "the operating point and does not unstick the loop. The priority order makes the "
                      "PARTIAL FIT concrete: the targets of greatest mechanistic need (the loop-LOCK) are "
                      "exactly the ones the frame cannot reach, because the LOCK axis is a pathological-"
                      "stabilisation E0-LOCK -- an over-deep basin / hysteresis, a STABILISATION (the third "
                      "distinct E0 mode after addiction's GAIN and Alzheimer's DECAY)."),
        "substantive_finding": {
            "leading_actionable_gene": lead_act["gene"],
            "leading_actionable_lever": lead_act["lever"],
            "leading_actionable_rank": lead_act["rank"],
            "highest_scoring_nonactionable_gene": (blocked_top["gene"] if blocked_top else None),
            "highest_scoring_nonactionable_rank": (blocked_top["rank"] if blocked_top else None),
            "highest_scoring_nonactionable_reach": (blocked_top["reach_status"] if blocked_top else None),
            "deepest_unmet_genes_all_out_of_reach": deepest_unmet_all_oor,
            "top_actionable_genes": act_top,
            "reading": ("the deepest-unmet targets (U=%d) are ALL non-actionable -- the LOCK loop-fixation "
                        "genes (%s) carry the unmet CEILING (the refractory loop-lock, no molecular "
                        "therapy) and are OUT OF REACH of the threshold/drive frame. The highest-scoring "
                        "NON-actionable target %s (#%d) is %s. The leading ACTIONABLE direction, %s (%s), "
                        "ranks #%d -- it is the strongest OCD candidate gene and the single highest-leverage "
                        "molecular handle, yet it is REACHABLE-BUT-PARTIAL (it nudges the operating point, "
                        "not the loop-lock). So the priority order makes the PARTIAL FIT concrete: the "
                        "targets of greatest mechanistic need (the loop-LOCK) are exactly the ones the "
                        "threshold frame cannot reach, while even the strongest reachable lever leaves the "
                        "loop untouched. This ranks unmet MECHANISTIC need; it makes NO efficacy claim (see "
                        "the firewall: no direction is asserted to treat, cure, or permanently stop the "
                        "disorder, and the reachable levers do not unstick the loop)."
                        % (u_ceiling, ", ".join(deepest_unmet_genes),
                           (blocked_top["gene"] if blocked_top else "n/a"),
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
            "reading": ("the stiffest promoter read (%s, an OUT-OF-REACH loop-lock scaffold) sits at "
                        "priority #%d -- NOT the top; while the top-priority gene (%s, the reachable "
                        "glutamate transporter) has only the #%d-stiffest promoter. If promoter stiffness "
                        "drove the ranking neither could sit where it does. The decoupling is the firewall "
                        "made visible: a promoter-stiffness read is carried alongside but never folded into "
                        "the clinical priority, and it is not a basin depth, a hysteresis width, or the "
                        "strength of the compulsive lock."
                        % (stiffest, next(r["rank"] for r in rows if r["gene"] == stiffest),
                           top_priority, next(r["structural_context_NOT_in_score"]["h_sp_rank_stiffest_first"]
                                              for r in rows if r["gene"] == top_priority))),
        },
        "top_actionable_genes": act_top,
        "ranking": rows,
    }

if __name__ == "__main__":
    res = build()
    json.dump(res, open(os.path.join(HERE, "ocd_burden_prioritisation.json"), "w"), indent=1)
    print("burden-weighted OCD TARGET prioritisation  (declared weights, cited tiers)")
    print(f"  weights: {res['weights_declared']}   (ranks TARGETS, never drugs/doses; efficacy=0; reachable levers do NOT unstick the loop-lock)")
    print(f"  U-floor: {res['ocd_unmet_need_signature']['u_floor']}  (established but PARTIAL serotonergic route LOWERS unmet on SLC6A4; above ADHD's floor)")
    print(f"  deepest-unmet genes (U=ceiling) all out-of-reach: {res['ocd_unmet_need_signature']['deepest_unmet_all_out_of_reach']}  {res['ocd_unmet_need_signature']['deepest_unmet_genes']}")
    print(f"  {'rank':4} {'gene':9} {'lev':4} {'B':>2} {'U':>2} {'G':>2} {'score':>6}  reach                                                          (|h_sp|#)")
    for r in res["ranking"]:
        c = r["structural_context_NOT_in_score"]
        act = "" if r["actionable"] else "  (non-actionable)"
        print(f"  {r['rank']:4} {r['gene']:9} {str(r['lever']):4} {r['B_burden']:2} {r['U_unmet']:2} "
              f"{r['G_genetic_druggability']:2} {r['priority_score']:6.3f}  {r['reach_status']:61} (h_sp#{c['h_sp_rank_stiffest_first']:2}){act}")
    sf = res["substantive_finding"]
    print(f"  finding: leading ACTIONABLE {sf['leading_actionable_gene']} ({sf['leading_actionable_lever']}) #{sf['leading_actionable_rank']}; "
          f"highest-need non-actionable {sf['highest_scoring_nonactionable_gene']} #{sf['highest_scoring_nonactionable_rank']} is {sf['highest_scoring_nonactionable_reach']}")
    print(f"  top actionable (reachable levers): {sf['top_actionable_genes']}")
    dw = res["decoupling_witness"]
    print(f"  decoupling: stiffest promoter {dw['stiffest_promoter_gene']} -> priority #{dw['stiffest_promoter_priority_rank']}; "
          f"top priority {dw['top_priority_gene']} -> promoter stiffness #{dw['top_priority_h_sp_rank_stiffest_first']}")
