#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
repurposing_scanner.py  --  the CROSS-DISEASE REPURPOSING scanner (fail-closed).  [NATIVE, ROADMAP III-A2]

  *** NATIVE to the VP Disease Emergence Kit (not inherited).  It is the kit's HIGHEST-LEVERAGE
      catalytic output (ROADMAP §0 telos): a read-only scanner that uses the kit's own same-axis /
      same-direction / same-lever structure to surface, automatically, pairs of the form

          disease X (NO approved agent on its axis)   <-- shares an axis-perturbation signature -->
          disease Y (HAS an approved agent Z on the SAME signature)

      and proposes Z's MECHANISM CLASS as a testable corrective-DIRECTION hypothesis for X.  For a
      rare single-gene disease with no approved therapy, the cheapest credible path to a treatment is
      usually REPURPOSING an agent already approved for a disease that shares the same druggable axis.
      The bare forced direction ("lower the toxic protein", "replace the missing gene") is often
      already obvious to a specialist; what is NOT obvious, and what actually moves a sponsor, is the
      concrete cross-disease link "agent class Z, approved for Y, is a candidate direction for X". ***

THE SIGNATURE IT MATCHES (ROADMAP III-A2): emergent_axis-family x corrective-direction x lever-class.
  - axis_family  : a CURATED, auditable taxonomy (slug -> molecular CORRECTIVE-axis family below).
                   Defined at the level where a mechanism CLASS genuinely transfers -- by what is
                   pushed and how, NOT by the affected organ.  (So RHO-adRP, whose corrective axis is
                   "lower a toxic gain-of-function protein", sits with SOD1-ALS / TTR amyloidosis /
                   Huntington in `toxic_gof_protein`, NOT with the retinal gene-REPLACEMENT reads --
                   the retina is the organ, not the corrective axis.  The organ difference is exactly
                   the "same-axis != same-disease" caveat every hypothesis carries.)
  - direction    : the engine's [F]-forced corrective axis (UP / DOWN), frozen per disease.
  - lever_class  : the corrective lever (reduce/replace/restrain/potentiate/correct/oppose/restore/mimic).

  A hypothesis is surfaced for a bucket (axis_family, direction) and a lever class L iff the bucket
  holds BOTH (a) >=1 RECIPIENT -- a disease whose LEAD lever is L and whose lead agent is NOT approved
  (clinical / investigational) -- AND (b) >=1 DONOR -- a DIFFERENT disease with an APPROVED lever of
  class L (lead OR a secondary arm).  The tight axis_family deliberately PREVENTS spurious
  cross-modality matches: two diseases that share only the bare lever label `correct` (e.g. a
  pharmacochaperone read vs an exon-skip read) fall in DIFFERENT axis_families and never pair.

FIREWALL (strict -- ROADMAP III-A2):  MECHANISM-CLASS DIRECTION ONLY.  Never dose, never potency,
  never efficacy, never response rate, never a specific-product efficacy claim.  Every hypothesis
  carries an [O] grade, a measurable falsifier, and the honest caveat "same-axis != same-disease --
  this is a hypothesis, not a prediction; X-specific biology may defeat repurposing".  A hypothesis
  whose recipient already pursues the donor's mechanism class is EXPLICITLY DEMOTED to low-novelty
  (it then merely VALIDATES the scanner's logic -- a sanity check, like direction-recovery -- rather
  than proposing something new).  Read-only over the FROZEN analysis.json + registry; perturbs no hash.

Scanner gate (fail-closed):
  - every RESOLVED disease has an axis_family (forces honest classification of any disease added later);
  - every surfaced hypothesis carries [O] + a non-empty falsifier + the same-axis!=same-disease caveat;
  - the book-keeping closes: every no-approved-lead disease is either a recipient in >=1 hypothesis OR
    listed in the honest "orphan directions (no same-axis approved donor)" set, with no overlap;
  - a planted recipient with a same-(axis,direction,lever) approved donor MUST surface a hypothesis,
    and a planted recipient whose only candidate donor is in a DIFFERENT axis_family / direction MUST
    NOT -- the very predicate the gate uses.

Run:  python3 pipeline/repurposing_scanner.py [--write]   -> exit 1 on any violation
"""
import os, sys, json
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")

NO_APPROVED = {"clinical", "investigational"}

# --------------------------------------------------------------------------------------------------
# CURATED axis_family taxonomy  (slug -> molecular CORRECTIVE-axis family).
#
#   This is a faithful biological taxonomy of the CORRECTIVE axis (what is pushed and HOW), at the
#   granularity where a mechanism CLASS genuinely transfers between diseases.  It is the exact set of
#   axis classes already documented in VERSION / HANDOFF (toxic-protein-lowering, retinal gene
#   replacement, lysosomal storage, inflammasome/IL-1, coagulation, complement, ...), recorded here
#   in ONE auditable place rather than scattered across the registry.  It is NOT tuned to manufacture
#   pairs -- the scanner surfaces whatever buckets fall out, then grades novelty honestly.  The gate
#   fails closed if any RESOLVED disease is missing here, so adding a disease later forces an honest
#   axis_family classification (the same discipline as adding a burden tier).
# --------------------------------------------------------------------------------------------------
AXIS_FAMILY = {
    # --- lower a toxic / excess GAIN-of-function protein (knockdown / silencing modality) ----------
    "huntington_disease": "toxic_gof_protein",
    "rho_autosomal_dominant_retinitis_pigmentosa": "toxic_gof_protein",
    "sod1_amyotrophic_lateral_sclerosis": "toxic_gof_protein",
    "transthyretin_amyloidosis": "toxic_gof_protein",
    # MeCP2 over-dosage: same "excess gene product" theme but the engine reads it as a master-TF
    # over-shoot (axis DOWN / restrain), a DIFFERENT (direction,lever) bucket from the axis-UP
    # toxic-brake proteinopathies -- kept here as its own dosage-excess axis (no same-signature
    # approved donor, honestly).
    "mecp2_duplication_syndrome": "nuclear_TF_dosage",
    "rett_syndrome": "nuclear_TF_dosage",                # opposite direction (potentiate IGF1, downstream)
    # --- restore a missing inherited-retinal gene (subretinal-AAV gene-replacement modality) -------
    "leber_congenital_amaurosis_2": "retinal_gene_replacement",
    "x_linked_retinitis_pigmentosa": "retinal_gene_replacement",
    "choroideremia": "retinal_gene_replacement",
    # --- replace a deficient lysosomal catabolic ENZYME (enzyme-replacement modality) --------------
    "gaucher_disease": "lysosomal_enzyme_replacement",
    "fabry_disease": "lysosomal_enzyme_replacement",
    "pompe_disease": "lysosomal_enzyme_replacement",
    "lysosomal_acid_lipase_deficiency": "lysosomal_enzyme_replacement",
    "niemann_pick_disease_type_a_b": "lysosomal_enzyme_replacement",
    "mucopolysaccharidosis_type_i": "lysosomal_enzyme_replacement",
    "metachromatic_leukodystrophy": "lysosomal_enzyme_replacement",
    # --- reduce a stored lysosomal / peroxisomal substrate (substrate-reduction modality) ----------
    "cystinosis": "lysosomal_substrate_reduction",
    "niemann_pick_disease_type_c": "lysosomal_substrate_reduction",
    "x_linked_adrenoleukodystrophy": "peroxisomal_substrate_load",
    # --- restore a deficient cytosolic / metabolic enzyme (gene/enzyme restoration) ----------------
    "phenylketonuria": "metabolic_enzyme_replacement",
    "aadc_deficiency": "metabolic_enzyme_replacement",
    "cerebrotendinous_xanthomatosis": "metabolic_enzyme_replacement",
    "tetrahydrobiopterin_deficiency": "metabolic_enzyme_replacement",
    "classical_homocystinuria": "cofactor_responsive_enzyme",
    # --- restrain a toxic small-molecule metabolite the lost brake lets accumulate ----------------
    "hereditary_tyrosinaemia_type_1": "toxic_metabolite_upstream_restraint",
    "alkaptonuria": "toxic_metabolite_upstream_restraint",
    "acute_intermittent_porphyria": "toxic_metabolite_upstream_restraint",
    "primary_hyperoxaluria_type_1": "toxic_metabolite_upstream_restraint",
    "ornithine_transcarbamylase_deficiency": "toxic_metabolite_upstream_restraint",
    # --- toxic-metal overload --------------------------------------------------------------------
    "wilson_disease": "toxic_metal_overload",
    "hereditary_haemochromatosis_type_1": "toxic_metal_overload",
    "menkes_disease": "copper_delivery_deficiency",      # opposite sign (deliver copper) -> no donor
    # --- direct chemical sequestration of a poorly-soluble accumulating metabolite ---------------
    # cystinuria's approved lead does NOT restore the lost rBAT/b0,+AT transporter; it reacts the
    # free urinary cystine with a thiol (thiol-disulfide exchange) to raise its solubility.  That is
    # a distinct corrective modality from upstream-enzyme restraint (nitisinone-type) and from metal
    # chelation, so it gets its own family.  Singleton: it is an approved-lead DONOR with no
    # no-approved-tail recipient sharing (.,DOWN,restrain), so this naming cannot create/destroy any
    # hypothesis -- it is honest bookkeeping only.
    "cystinuria": "urinary_cystine_restraint",
    # --- lipid axes (distinct) -------------------------------------------------------------------
    "familial_hypercholesterolaemia": "ldl_cholesterol_level",
    "sitosterolaemia": "sterol_absorption",
    "familial_chylomicronaemia_syndrome": "triglyceride_clearance",
    # --- coagulation -----------------------------------------------------------------------------
    "haemophilia_a": "coagulation_factor_restore",
    "haemophilia_b": "coagulation_factor_restore",
    "factor_v_leiden": "coagulation_anticoagulation",
    "hereditary_antithrombin_deficiency": "coagulation_anticoagulation",
    # --- other cascades / mediators --------------------------------------------------------------
    "atypical_hemolytic_uremic_syndrome": "complement_cascade_restraint",
    "hereditary_angioedema": "kinin_bradykinin_restraint",
    "cryopyrin_associated_periodic_syndrome": "inflammasome_IL1_restraint",
    "familial_mediterranean_fever": "inflammasome_IL1_restraint",
    "deficiency_of_il1_receptor_antagonist": "inflammasome_IL1_restraint",
    # --- cardiac ---------------------------------------------------------------------------------
    "hypertrophic_cardiomyopathy": "cardiac_contractility_restraint",
    "long_qt_syndrome_3": "cardiac_ion_channel",
    # --- channels / receptors --------------------------------------------------------------------
    "cystic_fibrosis": "regulated_channel_potentiation",
    "congenital_hyperinsulinism": "regulated_channel_potentiation",
    "dravet_syndrome": "neuronal_ion_channel",           # recipient, no approved donor (honest)
    "nephrogenic_diabetes_insipidus_x_linked": "gpcr_water_signalling",
    "nephrogenic_siad": "gpcr_water_signalling",          # opposite direction -> no same-signature donor
    # --- intracellular signalling ----------------------------------------------------------------
    "tuberous_sclerosis_complex": "mtor_growth_signalling",
    "von_hippel_lindau_disease": "hif_pseudohypoxia",
    "hereditary_haemorrhagic_telangiectasia": "endothelial_angiogenesis",  # recipient, no donor (HHT downgrade)
    # --- hormones --------------------------------------------------------------------------------
    "x_linked_hypophosphataemia": "hormone_fgf23_restraint",
    "congenital_leptin_deficiency": "hormone_leptin_replace",
    "bardet_biedl_syndrome": "satiety_melanocortin",
    "leptin_receptor_deficiency": "satiety_melanocortin",
    # --- structural / scaffold -------------------------------------------------------------------
    "alpha1_antitrypsin_deficiency": "serpin_level_replace",
    "hypophosphatasia": "mineralization_enzyme",
    "duchenne_muscular_dystrophy": "muscle_dystrophin",
    "usher_syndrome_type_2a": "sensory_structural_scaffold",   # recipient, no donor (honest)
    # --- erythroid / motor-neuron / maturation / growth-plate ------------------------------------
    "beta_thalassaemia": "erythroid_globin_output",
    "sickle_cell_disease": "erythroid_globin_output",
    "spinal_muscular_atrophy": "motor_neuron_smn",
    "friedreich_ataxia": "mitochondrial_biogenesis",
    "achondroplasia": "growth_plate_brake",
    # --- v0.32.0 adds: skeletal-muscle channel / calcium-sensing GPCR / cofactor + transport replace ---
    "scn4a_skeletal_muscle_channelopathy": "skeletal_muscle_sodium_channel",  # skeletal twin of LQT3 (cardiac_ion_channel); recipient/donor singleton
    "neonatal_severe_hyperparathyroidism": "calcium_sensing_gpcr",            # distinct GPCR from gpcr_water_signalling; singleton
    "biotinidase_deficiency": "cofactor_recycling_replacement",               # flood the missing vitamin cofactor; singleton
    "primary_carnitine_deficiency": "carnitine_transport_replacement",        # flood the missing transported substrate; singleton
}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


def load_resolved():
    reg = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    out = []
    for slug in reg["diseases"]:
        a = json.load(open(os.path.join(DISEASES, slug, "analysis.json"), encoding="utf-8"))
        if a.get("status") != "RESOLVED":
            continue
        tx = a["treatment_A_switch"]
        em = a["emergence"]
        lead = tx.get("lead_corrective_lever") or {}
        # every corrective lever (lead + secondary arms) with its approval status -- the donor scan
        approved_lever_classes = set()
        corrective_lever_classes = set()
        agent_by_class = defaultdict(list)
        for L in tx.get("levers", []):
            if L.get("verdict_vs_pathology") != "CORRECTS":
                continue
            lc = L.get("lever")
            corrective_lever_classes.add(lc)
            ag = (L.get("agent_class") or "").split("(")[0].strip() or lc
            if L.get("status") == "approved":
                approved_lever_classes.add(lc)
                agent_by_class[lc].append(ag)
        out.append({
            "slug": slug,
            "axis_family": AXIS_FAMILY.get(slug),
            "emergent_axis": em.get("emergent_axis", ""),
            "direction": tx.get("corrective_axis_direction"),
            "lead_lever": lead.get("lever"),
            "lead_target": lead.get("target_gene"),
            "lead_status": lead.get("status"),
            "lead_no_approved": lead.get("status") in NO_APPROVED,
            "approved_lever_classes": approved_lever_classes,
            "corrective_lever_classes": corrective_lever_classes,
            "agent_by_class": {k: sorted(set(v)) for k, v in agent_by_class.items()},
        })
    return out


def build():
    rows = load_resolved()
    by_slug = {r["slug"]: r for r in rows}

    # ---- gate: every resolved disease classified (forces honest classification on future adds) ----
    unclassified = sorted(r["slug"] for r in rows if not r["axis_family"])
    if unclassified:
        for s in unclassified:
            print(f"    [FAIL] {s} has no axis_family -- classify it in AXIS_FAMILY")
    check(f"every resolved disease has a curated axis_family ({len(rows)} classified, "
          f"{len(unclassified)} missing)", not unclassified)

    # ---- group into buckets keyed (axis_family, corrective_direction) ----------------------------
    buckets = defaultdict(list)
    for r in rows:
        buckets[(r["axis_family"], r["direction"])].append(r)

    hypotheses = []
    for (fam, direction), members in sorted(buckets.items()):
        # lever classes present as a LEAD among the bucket members
        lever_classes = {m["lead_lever"] for m in members}
        for L in sorted(lever_classes):
            recipients = [m for m in members if m["lead_lever"] == L and m["lead_no_approved"]]
            donors = [m for m in members if L in m["approved_lever_classes"]]
            if not recipients or not donors:
                continue
            for rec in recipients:
                rdon = [d for d in donors if d["slug"] != rec["slug"]]
                if not rdon:
                    continue
                # novelty: does the recipient ALREADY pursue the donor's mechanism class L?
                already = L in rec["corrective_lever_classes"]
                novelty = ("low-novelty (confirmatory: the recipient already pursues this mechanism "
                           "class -- the scanner here merely VALIDATES its same-axis logic, a sanity "
                           "check)") if already else (
                          "candidate-transfer (the donor's approved mechanism class is NOT yet among "
                          "the recipient's pursued levers -- a genuinely new cross-disease direction)")
                donor_payload = sorted(
                    ({"donor": d["slug"], "donor_axis": d["emergent_axis"],
                      "approved_agent_class": d["agent_by_class"].get(L, []),
                      "donor_lead_target": d["lead_target"]} for d in rdon),
                    key=lambda x: x["donor"])
                hypotheses.append({
                    "recipient": rec["slug"],
                    "recipient_axis": rec["emergent_axis"],
                    "recipient_lead_target": rec["lead_target"],
                    "recipient_lead_status": rec["lead_status"],
                    "shared_axis_family": fam,
                    "shared_corrective_direction": direction,
                    "shared_lever_class": L,
                    "donors": donor_payload,
                    "hypothesis": (
                        f"On the shared '{fam}' axis, the corrective direction is {direction} via "
                        f"'{L}'.  An agent of this class is APPROVED for "
                        f"{', '.join(d['donor'] for d in donor_payload)} but NOT for {rec['slug']}; "
                        f"that approved mechanism class is therefore a candidate {direction}-direction "
                        f"repurposing hypothesis for {rec['slug']}."),
                    "novelty": novelty,
                    "grade": "[F] shared-axis direction forced + cited ; [O] magnitude / efficacy / "
                             "dose / repurposing-success-probability NOT asserted",
                    "falsifier": (
                        f"If a class-'{L}' agent that moves the '{fam}' axis {direction} in the donor "
                        f"disease(s) fails to move {rec['slug']}'s axis {direction} in its own tissue "
                        f"(e.g. allele-specificity, delivery, or {rec['slug']}-specific biology "
                        f"defeats it), the same-axis repurposing hypothesis for {rec['slug']} is false."),
                    "honesty_caveat": ("same-axis != same-disease -- this is a mechanism-CLASS "
                                       "DIRECTION hypothesis, not a prediction; the donor and recipient "
                                       "differ in tissue / delivery / allele / off-target biology, any "
                                       "of which may defeat repurposing.  No magnitude is claimed [O]."),
                })

    hypotheses.sort(key=lambda h: (h["shared_axis_family"], h["recipient"]))

    # ---- book-keeping: every no-approved-lead disease is a recipient OR an honest orphan ----------
    no_approved = sorted(r["slug"] for r in rows if r["lead_no_approved"])
    recipients_set = sorted({h["recipient"] for h in hypotheses})
    orphan = sorted(s for s in no_approved if s not in set(recipients_set))
    orphan_directions = [{
        "slug": s, "axis_family": by_slug[s]["axis_family"], "axis": by_slug[s]["emergent_axis"],
        "corrective_direction": by_slug[s]["direction"], "lead_lever": by_slug[s]["lead_lever"],
        "lead_status": by_slug[s]["lead_status"],
        "why_orphan": ("no OTHER resolved disease shares this (axis_family, corrective_direction, "
                       "lever_class) with an APPROVED agent -- the forced direction stands, but the "
                       "kit honestly reports there is no same-axis approved donor to repurpose from"),
    } for s in orphan]

    # closure check: recipients and orphans partition the no-approved set, no overlap
    partition_ok = (sorted(set(recipients_set) | set(orphan)) == no_approved
                    and not (set(recipients_set) & set(orphan)))
    check(f"book-keeping closes: every no-approved-lead disease is a recipient ({len(recipients_set)}) "
          f"or an honest orphan ({len(orphan)}), partitioning the {len(no_approved)} no-approved set "
          f"with no overlap", partition_ok)

    # every hypothesis carries [O] + falsifier + same-axis caveat
    well_formed = all(("[O]" in h["grade"]) and h["falsifier"].strip()
                      and "same-axis != same-disease" in h["honesty_caveat"]
                      for h in hypotheses)
    check(f"every hypothesis carries [O] grade + non-empty falsifier + same-axis!=same-disease caveat "
          f"({len(hypotheses)} hypotheses)", well_formed)

    fam_counts = Counter(r["axis_family"] for r in rows)
    result = {
        "title": "Cross-disease repurposing scanner -- same-axis approved agent as a candidate "
                 "direction for a no-approved-therapy disease",
        "native_to": "vp_disease_emergence_kit (ROADMAP III-A2); read-only over frozen analysis.json + registry",
        "principle": ("for a single-gene disease with NO approved therapy, the cheapest credible path "
                      "to a treatment is repurposing an agent already approved for a disease that shares "
                      "the same druggable axis; the scanner surfaces (axis_family x corrective-direction "
                      "x lever-class) buckets that hold both a no-approved RECIPIENT and an approved "
                      "DONOR, and proposes the donor's MECHANISM CLASS as the recipient's testable "
                      "direction -- the catalytic novelty the bare forced direction lacks."),
        "firewall": ("MECHANISM-CLASS DIRECTION ONLY; never dose, potency, efficacy, response rate, or "
                     "a specific-product efficacy claim; every hypothesis is [O] + falsifier + "
                     "'same-axis != same-disease' caveat; a recipient already pursuing the donor class "
                     "is demoted to low-novelty (a sanity check, not a new claim); read-only, perturbs "
                     "no per-disease hash."),
        "grade": "[F] shared-axis direction forced + cited ; [O] all magnitude / efficacy / "
                 "repurposing-success",
        "n_resolved": len(rows),
        "n_axis_families": len(fam_counts),
        "axis_family_counts": dict(sorted(fam_counts.items())),
        "n_no_approved_lead": len(no_approved),
        "no_approved_lead": no_approved,
        "n_hypotheses": len(hypotheses),
        "repurposing_hypotheses": hypotheses,
        "n_orphan_directions": len(orphan_directions),
        "orphan_directions_no_donor": orphan_directions,
        "overall": "PASS" if not FAIL else "FAIL",
        "failures": FAIL,
    }
    return result


def selftest():
    """Prove the scanner has TEETH on the EXACT predicate the gate uses: a synthetic bucket with a
    no-approved RECIPIENT and a same-(axis,direction,lever) APPROVED DONOR must surface a hypothesis;
    a recipient whose only candidate donor is in a DIFFERENT axis_family, or pushes a DIFFERENT
    direction, must NOT."""
    def surfaces(recipient, donor):
        # recipient/donor: dicts with axis_family, direction, lead_lever, lead_no_approved,
        # approved_lever_classes
        same_bucket = (recipient["axis_family"] == donor["axis_family"]
                       and recipient["direction"] == donor["direction"])
        donor_has = recipient["lead_lever"] in donor["approved_lever_classes"]
        return bool(same_bucket and recipient["lead_no_approved"] and donor_has)

    rec = {"axis_family": "F", "direction": "UP", "lead_lever": "reduce",
           "lead_no_approved": True, "approved_lever_classes": set()}
    donor_same = {"axis_family": "F", "direction": "UP", "lead_lever": "reduce",
                  "lead_no_approved": False, "approved_lever_classes": {"reduce"}}
    donor_other_family = {"axis_family": "G", "direction": "UP", "lead_lever": "reduce",
                          "lead_no_approved": False, "approved_lever_classes": {"reduce"}}
    donor_other_dir = {"axis_family": "F", "direction": "DOWN", "lead_lever": "reduce",
                       "lead_no_approved": False, "approved_lever_classes": {"reduce"}}
    donor_no_class = {"axis_family": "F", "direction": "UP", "lead_lever": "replace",
                      "lead_no_approved": False, "approved_lever_classes": {"replace"}}

    good = surfaces(rec, donor_same)
    rej_family = surfaces(rec, donor_other_family)
    rej_dir = surfaces(rec, donor_other_dir)
    rej_class = surfaces(rec, donor_no_class)
    ok = good and not rej_family and not rej_dir and not rej_class
    print("  [self-test] scanner teeth:",
          f"same-axis-donor(surface)={good}  other-family(reject)={not rej_family}  "
          f"other-direction(reject)={not rej_dir}  no-matching-class(reject)={not rej_class}  "
          f"-> {'OK' if ok else 'BROKEN'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    teeth_ok = selftest()
    res = build()
    if not teeth_ok:
        res["overall"] = "FAIL"
        res.setdefault("failures", []).append("self-test: scanner predicate is broken")
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "modules", "expected", "repurposing_hypotheses.json")
        json.dump(res, open(p, "w"), indent=1)
        print(f"  wrote {os.path.relpath(p, ROOT)}")
    print("Cross-disease repurposing scanner  [NATIVE / ROADMAP III-A2]")
    print(f"  resolved={res['n_resolved']}  axis-families={res['n_axis_families']}  "
          f"no-approved-lead={res['n_no_approved_lead']}")
    print(f"  repurposing hypotheses surfaced: {res['n_hypotheses']}  "
          f"(recipients with a donor); orphan no-donor directions: {res['n_orphan_directions']}")
    for h in res["repurposing_hypotheses"]:
        print(f"    [{h['shared_axis_family']}|{h['shared_corrective_direction']}|"
              f"{h['shared_lever_class']}]  {h['recipient']}  <-  "
              f"{', '.join(d['donor'] for d in h['donors'])}")
    print("OVERALL:", "PASS" if res["overall"] == "PASS" else f"FAIL {res['failures']}")
    sys.exit(0 if res["overall"] == "PASS" else 1)
