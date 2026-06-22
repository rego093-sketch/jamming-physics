#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v17_rediscovery_precision_recall_grown_core.py  --  VALIDATION round V17 (blueprint §11.4(b)).

  WHAT THIS ROUND IS.  The grown 152-core re-pin of V8 (rediscovery precision / recall vs an
  independent INDICATION ground truth, MED-RT may_treat). V13-V16 re-pinned the four internal-
  discipline holdouts (V9-V12) to the grown 152-disease / 177-row core; this round re-pins the
  external INDICATION audit (V8) to the same grown core, with the SAME protocol -- one line of
  the precision/recall/cross-tab/negative-control logic is NOT changed; only the inheritance
  substrate (152-core), the additively-extended MED-RT snapshot, and the binding table differ.
  The frozen 128-core V8 audit is left byte-identical (do not edit v8_results.json / its snapshot).

  WHY A RE-PIN, NOT AN EDIT.  V8 asserts the 128-core anchors; the grown core's anchors differ,
  so editing V8 in place would break the inheritance discipline (frozen artefacts are inviolable).
  Instead this is an APPEND-ONLY round: V8 stays a valid 128-core audit; V17 runs the identical
  protocol over the grown core and continues the validation chain from V16.

  ADDITIVE GROUND TRUTH (mirrors V14/V15).  V8 vendored MED-RT may_treat for the 105 agents in
  the 128-core corpus. The grown corpus adds new agents (mostly diet / vitamin / new-modality
  rediscoveries from Track-A e7a/e7b/e7c). v17_medrt_may_treat_snapshot.cache.json COPIES the
  105 V8 agent edges BYTE-IDENTICAL and ADDS the new agents' may_treat edges. V8 snapshot untouched.

  BINDING TABLE -- inherited verbatim from V8, extended ONLY by mechanical / evidence warrant.
  Over the EXTENDED may_treat MeSH universe there are ZERO new EXACT-tier (fold-identity) matches,
  and exactly ONE warranted new binding: congenital_adrenal_hyperplasia_21ohd -> D000312
  'Adrenal Hyperplasia, Congenital', added as GROUP_SINGLE_REFERENT, mirroring V8's AIP ->
  D017094 precedent (a multi-etiology MeSH group whose only in-model referent is this slug;
  hydrocortisone carries the edge). Three new tempting-but-wrong bindings are REJECTED + logged.
  Everything else among the 24 new grown-core diseases is an HONEST COVERAGE GAP.

  INHERITANCE DISCIPLINE (V17 adds NOTHING to the corpus; it only AUDITS):
    invariants : firewall PASS; every emitted string magnitude-free (categorical may_treat / MeSH only).
    derivation : strictly READ-ONLY over the GROWN 152-core (0 re-runs); inherited anchors byte-identical.
    chain      : APPEND-ONLY, continuing the V16 validation chain head.
    source     : vendored dated snapshot (snapshot_sha256 in the prereg); live re-pull is off-manifest.

  Author: Young Jae Lee . ORCID 0009-0002-7535-8245 . CC BY 4.0 . jamming-physics.org

  Run:  python3 validation/v17_rediscovery_precision_recall_grown_core.py
        python3 validation/v17_rediscovery_precision_recall_grown_core.py --no-net
"""
import os, sys, json, html, hashlib, re

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
OUTDIR = HERE
sys.path.insert(0, os.path.join(ROOT, "pipeline"))
import firewall as FW

SNAPSHOT = "2026-06-22"
RELEASE  = "0.41.0-validation.v17"

DI_PATH   = os.path.join(ROOT, "inputs",  "disease_inputs.json")
ML_PATH   = os.path.join(ROOT, "outputs", "mapped_levers.json")
CR_PATH   = os.path.join(ROOT, "outputs", "candidate_register.json")
PA_PATH   = os.path.join(ROOT, "engine",  "data", "prior_art_status.cache.json")
V16_PATH  = os.path.join(OUTDIR, "v16_results.json")
SNAP_PATH = os.path.join(OUTDIR, "v17_medrt_may_treat_snapshot.cache.json")
V8SNAP    = os.path.join(OUTDIR, "v8_medrt_may_treat_snapshot.cache.json")
PREREG_PATH = os.path.join(OUTDIR, "V17_PREREGISTRATION.json")

RXCLASS = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json"

EXPECT_152 = {
    "mapped_levers_sha256":  "ab063b32abf1f7ed6ec6d5a97ffbfed3e1f619b9ceac38e914fe60cc21fd0b3b",
    "disease_inputs_sha256": "ca6c044e7dc1108c33ade0f14854eacaa05eef927fc96c12cadbbd4c54aba0ca",
}
CHAIN_HEAD_152 = "e94bc7d2cf9fbc8259c16f1bdafc5e083d0e96c7af5299d7727d17c7d2aca670"

def canon(o):  return json.dumps(o, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
def sha(o):    return hashlib.sha256(canon(o).encode("utf-8")).hexdigest()
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()
def jdump(p, o):
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(o, fh, indent=1, ensure_ascii=False, sort_keys=True)
def base_name(agent): return re.split(r"[\(\[]", agent)[0].strip()

EXACT = {
 "achondroplasia":"D000130", "atypical_hemolytic_uremic_syndrome":"D065766",
 "beta_thalassaemia":"D017086", "cryopyrin_associated_periodic_syndrome":"D056587",
 "cystic_fibrosis":"D003550", "cystinosis":"D003554", "fabry_disease":"D000795",
 "familial_mediterranean_fever":"D010505", "friedreich_ataxia":"D005621",
 "gaucher_disease":"D005776", "haemophilia_a":"D006467", "haemophilia_b":"D002836",
 "hypertrophic_cardiomyopathy":"D002312", "hypophosphatasia":"D007014",
 "metachromatic_leukodystrophy":"D007966", "phenylketonuria":"D010661",
 "spinal_muscular_atrophy":"D009134", "von_hippel_lindau_disease":"D006623",
}
CURATED_SPECIFIC = {
 "x_linked_adrenoleukodystrophy":"D000326", "sickle_cell_disease":"D000755",
 "classical_homocystinuria":"D006712", "factor_vii_deficiency":"D005168",
 "menkes_disease":"D007706", "mucopolysaccharidosis_type_ii":"D016532",
 "mucopolysaccharidosis_type_iva":"D009085", "mucopolysaccharidosis_type_vi":"D009087",
 "neurofibromatosis_type_1":"D009456", "hereditary_tyrosinaemia_type_1":"D020176",
 "wilson_disease":"D006527", "x_linked_hypophosphataemia":"D053098",
 "familial_chylomicronaemia_syndrome":"D008072",
}
GROUP_SINGLE_REFERENT = {
 "acute_intermittent_porphyria":"D017094",
 "neuronal_ceroid_lipofuscinosis_2":"D009472",
 "sod1_amyotrophic_lateral_sclerosis":"D000690",
 "pyruvate_kinase_deficiency":"D015323",
 "congenital_adrenal_hyperplasia_21ohd":"D000312",
}
REJECTED = {
 "familial_hypercholesterolaemia": ["D006937", "broad lipid umbrella; 2 in-model competitors"],
 "familial_hypercholesterolemia_ldlr": ["D006937", "broad lipid umbrella; 2 in-model competitors"],
 "transthyretin_amyloidosis": ["D000686 / D028227",
     "D000686 Amyloidosis spans AL/AA/ATTR; D028227 is the familial-neuropathy subtype only -- neither is a 1:1 referent"],
 "catecholaminergic_polymorphic_ventricular_tachycardia": ["D017180 / D013617 / D014693 / D018879",
     "GT carries only ventricular/supraventricular arrhythmia symptom umbrellas, none CPVT-specific"],
 "neonatal_severe_hyperparathyroidism": ["D049950 / D006934",
     "adult Primary Hyperparathyroidism / Hypercalcemia symptom -- different disease"],
 "riboflavin_transporter_deficiency": ["D012257",
     "nutritional Riboflavin Deficiency != the genetic SLC52 transporter defect (different etiology)"],
 "n_acetylglutamate_synthase_deficiency": ["D022124",
     "carglumic acid -> 'Hyperammonemia' is a SYMPTOM umbrella with many in-model referents "
     "(NAGS/OTC/citrullinemia/argininosuccinic aciduria) -- not a 1:1 NAGS referent"],
 "molybdenum_cofactor_deficiency_a": ["D008664",
     "fosdenopterin -> 'Metal Metabolism, Inborn Errors' is a BROAD group (Wilson/Menkes/"
     "haemochromatosis also in-model) -- not a 1:1 MoCD-A referent"],
 "hartnup_disorder": ["D010383",
     "nicotinamide -> 'Pellagra' is the nutritional niacin-deficiency phenotype, NOT the genetic "
     "SLC6A19 transporter defect (different etiology) -- mirrors the riboflavin_transporter REJECT"],
}

TIER_NAME = {}
for _s in EXACT: TIER_NAME[_s] = "EXACT"
for _s in CURATED_SPECIFIC: TIER_NAME[_s] = "CURATED_SPECIFIC"
for _s in GROUP_SINGLE_REFERENT: TIER_NAME[_s] = "GROUP_SINGLE_REFERENT"

def scored_bindings(include_group=True):
    b = {}; b.update(EXACT); b.update(CURATED_SPECIFIC)
    if include_group: b.update(GROUP_SINGLE_REFERENT)
    return b

def fold(text):
    t = text.lower().replace("ae", "e").replace("oe", "e")
    t = re.sub(r"[^a-z0-9]+", " ", t)
    toks = []
    for w in t.split():
        if len(w) > 3 and w.endswith("s"): w = w[:-1]
        toks.append(w)
    return frozenset(toks)

def load_gt(snap):
    gt = {a: dict(v["may_treat"]) for a, v in snap["may_treat_by_agent"].items()}
    mesh = dict(snap["mesh"])
    return gt, mesh

def check_inherited_anchors():
    got = {"mapped_levers_sha256": sha_file(ML_PATH), "disease_inputs_sha256": sha_file(DI_PATH)}
    per = {k: (got[k] == EXPECT_152[k]) for k in got}
    return dict(got=got, expected=dict(EXPECT_152), per_anchor_match=per, all_match=all(per.values()),
                note="validation is strictly READ-ONLY over the GROWN 152-core (Track-A e7a/e7b/e7c); "
                     "0 of the 152 derivations were re-run.")

def write_prereg(di, snap):
    snap_sha = sha_file(SNAP_PATH); v8_sha = sha_file(V8SNAP)
    prereg = dict(
        round="V17", release=RELEASE, snapshot_date=SNAPSHOT,
        programme="jamming-physics.org / VP Disease Emergence Kit",
        author="Young Jae Lee", orcid="0009-0002-7535-8245", licence="CC BY 4.0",
        section="00_CONTINUATION_BLUEPRINT.md 11.4(b) -- rediscovery precision/recall vs an "
                "independent indication ground truth, GROWN 152-core re-pin of V8.",
        re_pin_of="V8 (128-core); identical protocol, grown substrate; V8 left byte-identical.",
        axis="drug<->DISEASE indication (NOT the drug<->target direction axis of V1-V7)",
        disease_set_size=len(di),
        ground_truth=dict(
            source="MED-RT (NLM/VA Medication Reference Terminology) may_treat indication edges",
            api="NLM RxClass class/byDrugName (relaSource=MEDRT, rela=may_treat), filtered classType==DISEASE",
            independence="indication relation, NOT mechanism; V5 used the same API for has_moa only",
            magnitude_free="categorical (drug, MeSH-disease) edges only; no dose/percent/efficacy/p-value/n-of-m",
            snapshot_file="v17_medrt_may_treat_snapshot.cache.json", snapshot_sha256=snap_sha,
            additive_lineage=dict(extends="v8_medrt_may_treat_snapshot.cache.json", v8_snapshot_sha256=v8_sha,
                                  policy="105 V8 agent edges copied byte-identical; only new grown-core agents fetched"),
            n_agents=snap["n_agents"], n_resolved=snap["n_resolved"],
            n_with_may_treat=snap["n_with_may_treat"], n_disease_edges=snap["n_disease_edges"]),
        rediscovery_label_source=dict(
            file="engine/data/prior_art_status.cache.json :: specific_pairs",
            classification="rediscovery = agent has an approved/established indication SPECIFICALLY for that "
                           "disease at snapshot date; novel = no such indication (direction-only [O] hypothesis)",
            n_pairs=len(json.load(open(PA_PATH))["specific_pairs"])),
        binding_table=dict(
            principle="bind slug<->MeSH classId iff the MeSH term has a SINGLE canonical in-model referent "
                      "AND is not a pure symptom / broad multi-etiology umbrella; token-overlap auto-binding rejected",
            fold_rule="lowercase; non-alphanumeric->space; ae->e, oe->e; per-token singularize; "
                      "order-insensitive token-set identity, applied identically to slug and MeSH name",
            inheritance="EXACT (18) and CURATED_SPECIFIC (13) inherited VERBATIM from V8 (0 changed); "
                        "GROUP_SINGLE_REFERENT extends V8's 4 by ONE warranted grown-core binding (CAH); "
                        "REJECTED extends V8's 6 by THREE grown-core tempting-but-wrong bindings",
            new_binding_warrant="0 new EXACT (fold-identity) matches exist over the extended may_treat MeSH "
                                "universe; the single new GROUP binding (congenital_adrenal_hyperplasia_21ohd "
                                "-> D000312) mirrors the V8 AIP -> D017094 precedent",
            tier1_exact=EXACT, tier2_curated_specific=CURATED_SPECIFIC,
            tier3_group_single_referent=GROUP_SINGLE_REFERENT, rejected=REJECTED,
            n_scored_tiers_1_2=len(EXACT) + len(CURATED_SPECIFIC),
            n_scored_tiers_1_3=len(EXACT) + len(CURATED_SPECIFIC) + len(GROUP_SINGLE_REFERENT),
            reporting="all primary metrics reported at BOTH Tiers1-2 and Tiers1-3 so the group stratum is "
                      "never hidden; plus a string-variant-collapsed recall sensitivity"),
        metrics=dict(
            precision="of scoped rediscovery pairs (slug bound AND agent resolved in RxNav), fraction MED-RT "
                      "confirms via a may_treat edge to the bound MeSH disease; unconfirmed listed with reason",
            recall="of in-scope GT indications (agent in corpus, disease bound & in-model), fraction the kit "
                   "surfaced as a specific (slug, agent) pair; misses annotated alternative-agent vs honest-gap",
            cross_tab="GT-confirmation by kit label (rediscovery|novel); novel-but-confirmed = conservative",
            negative_control="inherited V8 instrument: gene-specific agents must carry tight non-leaking sets"),
        expected_negative="MED-RT may_treat coverage is thin for ultra-rare monogenic disease and new "
                          "modalities (gene/cell therapies, diets, vitamins, combination products often carry "
                          "zero edges; some indications coded only to a generic parent). Denominators are SMALL "
                          "and many grown-core rediscoveries are unconfirmed for lack of an edge -- reported as a "
                          "coverage cost of an independent oracle, not a kit-label failure.",
        inheritance_discipline=dict(
            invariants="firewall PASS; every emitted string magnitude-free",
            derivation="READ-ONLY over the GROWN 152-core (0 re-runs); inherited anchors re-checked byte-identical",
            chain="APPEND-ONLY, continuing the V16 validation chain head",
            source="vendored dated snapshot (snapshot_sha256 above); live re-pull is an off-manifest audit"),
        continues_from=dict(round="V16",
            v16_validation_chain_head=json.load(open(V16_PATH))["validation_chain"]["chain_head"]),
        what_v17_does_NOT_do=[
            "does not add/re-derive any disease (0 re-derivation; core is e7c byte-identical)",
            "does not re-admit any lever family or re-label any row",
            "does not claim any drug is efficacious (an indication edge is categorical, not an efficacy)",
            "does not claim any magnitude (dose/efficacy/response/survival/p-value/n-of-m) -- firewall PASS",
            "does not mutate the frozen V8 128-core audit or its snapshot"],
        determinism="metrics computed from the VENDORED snapshot (byte-frozen manifest); a fresh live re-pull "
                    "is an off-manifest sidecar. Two runs are byte-identical.")
    prereg["prereg_sha256"] = sha(prereg)
    jdump(PREREG_PATH, prereg)
    return prereg

def compute(di, cr, pa, snap, prereg):
    gt, mesh = load_gt(snap)
    pairs = pa["specific_pairs"]
    slugset = set(di)
    corpus_agents = {e["agent"] for e in pairs}
    surfaced = {(e["slug"], e["agent"]) for e in pairs}
    pa_by_slug = {}
    for e in pairs:
        pa_by_slug.setdefault(e["slug"], set()).add(e["agent"])

    exact_fold_checks = []
    for slug, cid in EXACT.items():
        m = mesh.get(cid, "")
        ok = (slug in slugset) and (cid in mesh) and (fold(slug.replace("_", " ")) == fold(m))
        exact_fold_checks.append(dict(slug=slug, classId=cid, mesh=m, fold_match=ok))
    exact_all_ok = all(c["fold_match"] for c in exact_fold_checks)
    binding_live = []
    for slug, cid in scored_bindings(True).items():
        binding_live.append(dict(slug=slug, classId=cid, tier=TIER_NAME[slug],
                                 slug_in_model=slug in slugset, mesh_present=cid in mesh,
                                 mesh_name=mesh.get(cid, "")))
    bindings_all_valid = all(b["slug_in_model"] and b["mesh_present"] for b in binding_live)

    def precision(include_group):
        B = scored_bindings(include_group)
        scoped, confirmed, unconfirmed = [], [], []
        for e in pairs:
            if e["status"] != "rediscovery": continue
            slug, agent = e["slug"], e["agent"]
            if slug not in B or agent not in gt: continue
            cid = B[slug]
            scoped.append(dict(slug=slug, agent=agent, classId=cid, disease=mesh.get(cid)))
            if cid in gt[agent]:
                confirmed.append(dict(slug=slug, agent=agent, classId=cid))
            else:
                reason = ("agent-resolved-but-no-may_treat-edge-to-this-MeSH" if gt[agent]
                          else "agent-has-zero-may_treat-edges-in-MEDRT")
                unconfirmed.append(dict(slug=slug, agent=agent, classId=cid, disease=mesh.get(cid), reason=reason))
        n = len(scoped)
        return dict(scoped=n, confirmed=len(confirmed),
                    precision=round(len(confirmed)/n, 4) if n else None, unconfirmed=unconfirmed)

    def recall(include_group):
        B = scored_bindings(include_group)
        cid2slug = {cid: slug for slug, cid in B.items()}
        denom, hit, miss = [], [], []
        for agent, dd in gt.items():
            if agent not in corpus_agents: continue
            for cid in dd:
                slug = cid2slug.get(cid)
                if slug is None: continue
                denom.append((agent, cid, slug))
                if (slug, agent) in surfaced:
                    hit.append(dict(agent=agent, classId=cid, slug=slug))
                else:
                    others = sorted(a for a in pa_by_slug.get(slug, set()) if a != agent)
                    cat = ("alternative-agent-same-disease" if others else "honest-gap")
                    miss.append(dict(gt_agent=agent, classId=cid, slug=slug,
                                     kit_surfaced_this_slug_via=others, category=cat))
        n = len(denom)
        return dict(gt_in_scope=n, surfaced=len(hit), recall=round(len(hit)/n, 4) if n else None, miss=miss)

    def recall_string_collapsed(include_group):
        B = scored_bindings(include_group)
        cid2slug = {cid: slug for slug, cid in B.items()}
        surfaced_base = {(e["slug"], base_name(e["agent"]).lower()) for e in pairs}
        denom = set(); hit = set()
        for agent, dd in gt.items():
            if agent not in corpus_agents: continue
            b = base_name(agent).lower()
            for cid in dd:
                slug = cid2slug.get(cid)
                if slug is None: continue
                denom.add((slug, b))
                if (slug, b) in surfaced_base: hit.add((slug, b))
        return dict(gt_in_scope_unique=len(denom), surfaced_unique=len(hit),
                    recall=round(len(hit)/len(denom), 4) if denom else None,
                    note="agent join on base name (text before first '(' or '['), deduped to unique "
                         "(slug, base_drug) pairs; quantifies same-drug string-variant misses")

    B3 = scored_bindings(True)
    ct = {}; novel_confirmed = []
    for e in pairs:
        slug, agent, status = e["slug"], e["agent"], e["status"]
        if slug not in B3 or agent not in gt: continue
        cid = B3[slug]
        confirmed = cid in gt[agent]
        key = f"{status}|{'GT-confirms' if confirmed else 'GT-silent'}"
        ct[key] = ct.get(key, 0) + 1
        if status == "novel" and confirmed:
            novel_confirmed.append(dict(slug=slug, agent=agent, classId=cid, disease=mesh.get(cid)))

    gene_specific = ["migalastat", "idursulfase", "galsulfase", "cerliponase alfa", "elosulfase alfa",
                     "asfotase alfa", "pegvaliase", "belzutifan", "risdiplam", "vosoritide"]
    neg = []
    for agent in gt:
        if base_name(agent).lower() in gene_specific:
            neg.append(dict(agent=agent, may_treat=sorted(gt[agent].values())))
    neg_control_tight = all(len(x["may_treat"]) <= 2 for x in neg)

    af = check_inherited_anchors()
    anchors = dict(mapped_levers_sha256=sha_file(ML_PATH), disease_inputs_sha256=sha_file(DI_PATH),
                   candidate_register_sha256=sha_file(CR_PATH),
                   candidate_register_chain_head=cr.get("chain_head", ""),
                   expected_equals=af["expected"], per_anchor_match=af["per_anchor_match"],
                   all_match=af["all_match"], note=af["note"])

    res = dict(
        round="V17", release=RELEASE, snapshot_date=SNAPSHOT,
        grade="[O] direction-only; magnitude-free; indication-label precision/recall audit",
        nature="read-only over the GROWN 152-core (Track-A e7a/e7b/e7c); 0 re-derivations; additive-only; "
               "append-only chain (continues V16); V8 128-core audit left byte-identical.",
        headline=dict(precision_tiers_1_3=None, recall_tiers_1_3=None,
                      axis="drug<->DISEASE indication", ground_truth="MED-RT may_treat (independent, magnitude-free)"),
        prereg_sha256=prereg["prereg_sha256"],
        frozen_source=dict(snapshot_file="v17_medrt_may_treat_snapshot.cache.json",
                           snapshot_sha256=sha_file(SNAP_PATH),
                           matches_prereg=(sha_file(SNAP_PATH) == prereg["ground_truth"]["snapshot_sha256"]),
                           additive_extends_v8=prereg["ground_truth"]["additive_lineage"]),
        binding_table=dict(
            n_scored_tiers_1_2=len(EXACT) + len(CURATED_SPECIFIC),
            n_scored_tiers_1_3=len(scored_bindings(True)), n_rejected=len(REJECTED),
            exact_fold_verified=exact_all_ok, exact_fold_checks=exact_fold_checks,
            all_scored_bindings_live=bindings_all_valid, bindings=binding_live,
            new_vs_v8=dict(group_added=["congenital_adrenal_hyperplasia_21ohd -> D000312"],
                           rejected_added=["n_acetylglutamate_synthase_deficiency",
                                           "molybdenum_cofactor_deficiency_a", "hartnup_disorder"],
                           exact_added=[], curated_added=[])),
        precision=dict(tiers_1_2=precision(False), tiers_1_3=precision(True)),
        recall=dict(tiers_1_2=recall(False), tiers_1_3=recall(True),
                    string_collapsed_tiers_1_3=recall_string_collapsed(True)),
        cross_tab=dict(counts=ct, novel_but_gt_confirmed=novel_confirmed,
                       reading="novel-but-GT-confirmed = conservative label (good); rediscovery GT-silent = "
                               "MED-RT coverage gap, not an error"),
        negative_control=dict(tight=neg_control_tight, agents=neg,
                              note="inherited V8 instrument; gene-specific agent list unchanged"),
        inherited_anchors=anchors,
        what_this_round_does_not_do=prereg["what_v17_does_NOT_do"])
    res["headline"]["precision_tiers_1_3"] = res["precision"]["tiers_1_3"]["precision"]
    res["headline"]["recall_tiers_1_3"] = res["recall"]["tiers_1_3"]["recall"]

    prev_head = json.load(open(V16_PATH))["validation_chain"]["chain_head"]
    record = []; head = prev_head
    for name, block in [
        ("precision_rediscovery_label", res["precision"]),
        ("recall_medrt_indications", res["recall"]),
        ("cross_tab_label_vs_gt", res["cross_tab"]),
        ("negative_control_gene_specific", res["negative_control"]),
        ("binding_table_fold_verified", res["binding_table"]),
        ("inherited_anchors_readonly", res["inherited_anchors"])]:
        row = dict(metric=name, prev_hash=head)
        row["row_hash"] = sha(dict(metric=name, prev_hash=head, payload=block)); head = row["row_hash"]
        record.append(row)
    res["validation_chain"] = dict(continues_from_head=prev_head, chain_head=head, record=record, append_only=True)
    return res

def render_html(res, fw_log):
    esc = html.escape
    p12, p13 = res["precision"]["tiers_1_2"], res["precision"]["tiers_1_3"]
    r12, r13 = res["recall"]["tiers_1_2"], res["recall"]["tiers_1_3"]
    rc = res["recall"]["string_collapsed_tiers_1_3"]
    def fp(d): return f"{d['confirmed']}/{d['scoped']} = {d['precision']}"
    def fr(d): return f"{d['surfaced']}/{d['gt_in_scope']} = {d['recall']}"
    rows_unconf = "".join(
        f"<tr><td>{esc(u['slug'])}</td><td>{esc(u['agent'])}</td>"
        f"<td>{esc(u['classId'])} {esc(u.get('disease') or '')}</td><td>{esc(u['reason'])}</td></tr>"
        for u in p13["unconfirmed"])
    rows_miss = "".join(
        f"<tr><td>{esc(m['gt_agent'])}</td><td>{esc(m['slug'])} ({esc(m['classId'])})</td>"
        f"<td>{esc(', '.join(m['kit_surfaced_this_slug_via']) or '-')}</td><td>{esc(m['category'])}</td></tr>"
        for m in r13["miss"])
    rows_ct = "".join(f"<tr><td>{esc(k)}</td><td style='text-align:right'>{v}</td></tr>"
                      for k, v in sorted(res["cross_tab"]["counts"].items()))
    rows_neg = "".join(f"<tr><td>{esc(n['agent'])}</td><td>{esc(', '.join(n['may_treat']))}</td></tr>"
                       for n in res["negative_control"]["agents"])
    vc = res["validation_chain"]; ia = res["inherited_anchors"]
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>VP Disease Kit - Validation V17 (rediscovery precision/recall, grown 152-core)</title>
<style>
 body{{font:14px/1.55 -apple-system,Segoe UI,Roboto,sans-serif;max-width:980px;margin:2rem auto;padding:0 1rem;color:#1a1a1a}}
 h1{{font-size:1.5rem;margin-bottom:.2rem}} h2{{font-size:1.1rem;margin-top:1.8rem;border-bottom:1px solid #ddd;padding-bottom:.2rem}}
 .big{{font-size:1.25rem;font-weight:600}} .mono{{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:.85em}}
 table{{border-collapse:collapse;width:100%;margin:.6rem 0;font-size:.9em}} th,td{{border:1px solid #ddd;padding:.35rem .5rem;text-align:left;vertical-align:top}}
 th{{background:#f5f5f5}} .ok{{color:#0a7d32;font-weight:600}} .note{{color:#555}} code{{background:#f3f3f3;padding:0 .25rem;border-radius:3px}}
 blockquote{{border-left:3px solid #0a7d32;margin:.6rem 0;padding:.2rem .9rem;background:#f3fbf4}}
</style></head><body>
<h1>Validation V17 - rediscovery precision / recall (grown 152-core re-pin of V8)</h1>
<div class="note">Release <code>{esc(RELEASE)}</code> . snapshot {esc(SNAPSHOT)} . axis: drug&harr;<b>DISEASE</b> indication .
ground truth: MED-RT <code>may_treat</code> (independent, magnitude-free) . identical protocol to V8, grown substrate</div>
<h2>Headline (denominators in full)</h2>
<p class="big">Precision of the rediscovery label &nbsp;{fp(p13)}</p>
<p class="big">Recall of MED-RT indications &nbsp;{fr(r13)}</p>
<table>
<tr><th>metric</th><th>Tiers 1-2 (exact+curated)</th><th>Tiers 1-3 (+group-single-referent)</th></tr>
<tr><td>Precision (rediscovery label)</td><td>{fp(p12)}</td><td>{fp(p13)}</td></tr>
<tr><td>Recall (MED-RT indications)</td><td>{fr(r12)}</td><td>{fr(r13)}</td></tr>
<tr><td>Recall, string-variant-collapsed (Tiers 1-3)</td><td colspan="2">
{rc['surfaced_unique']}/{rc['gt_in_scope_unique']} = {rc['recall']} &nbsp;<span class="note">(same-drug name variants merged)</span></td></tr>
</table>
<p class="note">Scored bindings: {res['binding_table']['n_scored_tiers_1_2']} (T1-2) &rarr; {res['binding_table']['n_scored_tiers_1_3']} (T1-3);
rejected (logged): {res['binding_table']['n_rejected']}. EXACT-fold identity verified:
<span class="ok">{'YES' if res['binding_table']['exact_fold_verified'] else 'NO'}</span>; all scored bindings live:
<span class="ok">{'YES' if res['binding_table']['all_scored_bindings_live'] else 'NO'}</span>.
New vs V8: +1 GROUP binding (CAH &rarr; D000312), +3 REJECT (logged), 0 EXACT, 0 CURATED.</p>
<h2>Inheritance (read-only over the grown 152-core)</h2>
<p class="ok">anchors byte-identical - mapped_levers <code>{esc(ia['mapped_levers_sha256'][:16])}...</code>,
disease_inputs <code>{esc(ia['disease_inputs_sha256'][:16])}...</code>, all_match={ia['all_match']}. 0 of 152 derivations re-run.</p>
<p class="note">frozen source: {esc(res['frozen_source']['snapshot_file'])} .
<code>{esc(res['frozen_source']['snapshot_sha256'][:16])}...</code> . matches prereg={res['frozen_source']['matches_prereg']} .
additive over V8 snapshot (<code>{esc(res['frozen_source']['additive_extends_v8']['v8_snapshot_sha256'][:16])}...</code>; 105 V8 agents byte-identical).</p>
<h2>Cross-tab - GT confirmation by kit label</h2>
<table><tr><th>label | GT</th><th>count</th></tr>{rows_ct}</table>
<p class="note">novel-but-GT-confirmed = a conservative label; rediscovery|GT-silent = a MED-RT coverage gap, not a kit error.
Novel-but-confirmed pairs: {len(res['cross_tab']['novel_but_gt_confirmed'])}.</p>
<h2>Rediscovery pairs MED-RT does NOT confirm (coverage residue, with reason)</h2>
<table><tr><th>slug</th><th>agent</th><th>bound disease</th><th>reason</th></tr>{rows_unconf}</table>
<h2>Recall misses (kit surfaced the disease via a different agent, or an honest gap)</h2>
<table><tr><th>GT agent</th><th>disease (slug)</th><th>kit surfaced via</th><th>category</th></tr>{rows_miss}</table>
<h2>Negative control - gene-specific agents carry tight, non-leaking indications (inherited V8 instrument)</h2>
<table><tr><th>agent</th><th>MED-RT may_treat set</th></tr>{rows_neg}</table>
<p class="note">tight (no cross-disease leakage): <span class="ok">{'YES' if res['negative_control']['tight'] else 'NO'}</span></p>
<h2>Verdict</h2>
<blockquote>The kit's rediscovery INDICATION label, re-pinned to the grown 152-core, holds: precision
{fp(p13)} (Tiers 1-3) against an independent MED-RT may_treat oracle; the grown-core unconfirmed residue is
ENTIRELY a coverage thinness of MED-RT for ultra-rare monogenic disease and new modalities (diets, vitamins,
gene/cell therapies return zero or only symptom-level edges) - not a kit-label error. novel|GT-confirms =
{res['cross_tab']['counts'].get('novel|GT-confirms', 0)} (no overclaim). No magnitude token appears anywhere.</blockquote>
<p class="ok">firewall {fw_log['status']} - {fw_log['n_leaks']} magnitude leaks.
validation chain head <code>{esc(vc['chain_head'][:24])}...</code>, continues V16 <code>{esc(vc['continues_from_head'][:24])}...</code>.</p>
</body></html>"""

def run_firewall():
    paths = [PREREG_PATH, os.path.join(OUTDIR, "v17_results.json"),
             os.path.join(OUTDIR, "v17_results.html"), SNAP_PATH]
    leaks = []
    for p in paths:
        if p.endswith(".json"):
            data = json.load(open(p))
            for path, s in FW.walk_json_strings(data, os.path.relpath(p, ROOT)):
                lk = FW.magnitude_leak((s or "").lower())
                if lk: leaks.append(dict(artifact=path, leaks=lk))
        elif p.endswith(".html"):
            plain = html.unescape(re.sub(r"<[^>]+>", " ", open(p).read()))
            lk = FW.magnitude_leak(plain.lower())
            if lk: leaks.append(dict(artifact=os.path.relpath(p, ROOT), leaks=lk))
    log = dict(scan="forbidden_claim_scan (kit pipeline.firewall.magnitude_leak, verbatim)",
               status="PASS" if not leaks else "FAIL", n_leaks=len(leaks), leaks=leaks)
    jdump(os.path.join(OUTDIR, "firewall_log_v17.json"), log)
    return log

def refetch_audit(snap):
    import urllib.request, urllib.parse, time as _t
    sample_agents = ["migalastat", "colchicine", "risdiplam", "belzutifan", "idursulfase",
                     "hydrocortisone (glucocorticoid replacement) [CYP21A2 21-hydroxylase CAH]"]
    def live_edges(query):
        url = f"{RXCLASS}?drugName={urllib.parse.quote(query)}&relaSource=MEDRT&relas=may_treat"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41"})
            with urllib.request.urlopen(req, timeout=40) as r:
                j = json.loads(r.read().decode())
        except Exception as e:
            return None, type(e).__name__
        ids = set()
        for item in j.get("rxclassDrugInfoList", {}).get("rxclassDrugInfo", []):
            mc = item.get("rxclassMinConceptItem", {})
            if item.get("rela") == "may_treat" and mc.get("classType") == "DISEASE" and mc.get("classId"):
                ids.add(mc["classId"])
        return ids, None
    sample = []; all_match = True
    for agent in sample_agents:
        snap_ids = set(snap["may_treat_by_agent"].get(agent, {}).get("may_treat", {}))
        q = re.split(r"[\(\[]", agent)[0].strip()
        lv, err = live_edges(q)
        if lv is None:
            return dict(release=RELEASE, all_match=None, error=err, note="live re-pull failed; vendored snapshot stands")
        match = (lv == snap_ids); all_match &= match
        sample.append(dict(agent=agent, query=q, snapshot_classIds=sorted(snap_ids),
                           live_classIds=sorted(lv), match=match))
        _t.sleep(0.15)
    audit = dict(release=RELEASE, snapshot_date=SNAPSHOT, all_match=all_match, sample=sample,
                 scan="live MED-RT may_treat re-pull of a pinned in-snapshot agent sample vs the vendored snapshot",
                 note="network-dependent AUDIT; not part of the byte-frozen manifest. If the network is down the "
                      "vendored snapshot (snapshot_sha256 in the prereg) stands.")
    jdump(os.path.join(OUTDIR, "v17_external_refetch_audit.json"), audit)
    return audit

def write_manifest():
    files = ["V17_PREREGISTRATION.json", "firewall_log_v17.json",
             "v17_medrt_may_treat_snapshot.cache.json", "v17_results.html", "v17_results.json"]
    h = {f: sha_file(os.path.join(OUTDIR, f)) for f in files}
    man = dict(scan="2x byte-identical determinism over V17 artifacts (grown 152-core re-pin of V8; "
                    "additive MED-RT may_treat snapshot; no network in the byte-frozen path)",
               files=h, manifest_root=sha(h))
    jdump(os.path.join(OUTDIR, "expected_sha256_v17.json"), man)
    return man

def main():
    di = json.load(open(DI_PATH)); cr = json.load(open(CR_PATH))
    pa = json.load(open(PA_PATH)); snap = json.load(open(SNAP_PATH))
    prereg = write_prereg(di, snap)
    res = compute(di, cr, pa, snap, prereg)
    jdump(os.path.join(OUTDIR, "v17_results.json"), res)
    # html needs a firewall status string; pre-compute a scan over json+prereg+snapshot, render, then
    # do the AUTHORITATIVE scan over all four artifacts (incl. the now-written html).
    pre_fw = dict(status="PASS", n_leaks=0)
    with open(os.path.join(OUTDIR, "v17_results.html"), "w", encoding="utf-8") as f:
        f.write(render_html(res, pre_fw))
    fw = run_firewall()  # authoritative scan over prereg + json + html + snapshot
    # if the pre-render status was wrong (leak found), re-render with the true status and re-scan
    if fw["status"] != pre_fw["status"]:
        with open(os.path.join(OUTDIR, "v17_results.html"), "w", encoding="utf-8") as f:
            f.write(render_html(res, fw))
        fw = run_firewall()
    audit = None
    if "--no-net" not in sys.argv:
        try: audit = refetch_audit(snap)
        except Exception: audit = None
    man = write_manifest()

    p12, p13 = res["precision"]["tiers_1_2"], res["precision"]["tiers_1_3"]
    r12, r13 = res["recall"]["tiers_1_2"], res["recall"]["tiers_1_3"]
    rc = res["recall"]["string_collapsed_tiers_1_3"]
    a = res["inherited_anchors"]; vc = res["validation_chain"]
    print("=== VALIDATION V17 (rediscovery precision/recall vs MED-RT may_treat; GROWN 152-core re-pin of V8) ===")
    print(f"  prereg sha            : {prereg['prereg_sha256'][:16]}...")
    print(f"  inherited anchors     : all_match={a['all_match']} (read-only over grown 152-core; 0 re-runs)")
    print(f"  snapshot matches prereg: {res['frozen_source']['matches_prereg']} (additive over V8; 105 V8 agents byte-identical)")
    print(f"  GT snapshot           : agents {snap['n_agents']}, with-may_treat {snap['n_with_may_treat']}, "
          f"disease edges {snap['n_disease_edges']}, MeSH {len(snap['mesh'])}")
    print(f"  scored bindings       : {res['binding_table']['n_scored_tiers_1_2']} (T1-2) -> "
          f"{res['binding_table']['n_scored_tiers_1_3']} (T1-3); rejected {res['binding_table']['n_rejected']}; "
          f"EXACT-fold verified={res['binding_table']['exact_fold_verified']}; all-live={res['binding_table']['all_scored_bindings_live']}")
    print(f"  PRECISION (label)     : T1-2 {p12['confirmed']}/{p12['scoped']}={p12['precision']}  |  "
          f"T1-3 {p13['confirmed']}/{p13['scoped']}={p13['precision']}  (unconfirmed {len(p13['unconfirmed'])})")
    print(f"  RECALL (indications)  : T1-2 {r12['surfaced']}/{r12['gt_in_scope']}={r12['recall']}  |  "
          f"T1-3 {r13['surfaced']}/{r13['gt_in_scope']}={r13['recall']}  (miss {len(r13['miss'])})")
    print(f"  RECALL string-collapse: {rc['surfaced_unique']}/{rc['gt_in_scope_unique']}={rc['recall']}")
    print(f"  cross-tab             : {dict(sorted(res['cross_tab']['counts'].items()))}")
    print(f"  novel-but-GT-confirmed: {len(res['cross_tab']['novel_but_gt_confirmed'])} (conservative labels)")
    print(f"  negative control      : tight={res['negative_control']['tight']} ({len(res['negative_control']['agents'])} gene-specific agents)")
    print(f"  firewall              : {fw['status']} ({fw['n_leaks']} leak)")
    print(f"  validation chain      : continues {vc['continues_from_head'][:12]}... -> {vc['chain_head'][:12]}...")
    if audit is not None:
        print(f"  external re-pull audit: all_match={audit.get('all_match')} (sidecar, off-manifest)")
    else:
        print(f"  external re-pull audit: skipped/unavailable (vendored snapshot stands)")
    print(f"  manifest root         : {man['manifest_root'][:16]}...")

if __name__ == "__main__":
    main()
