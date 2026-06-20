#!/usr/bin/env python3
"""
R6 stage 2 -- natural-history registry pass (Orphanet) applied to the burden axes.

The ONE remaining [L] upgrade named since R3 (BURDEN_INDEX.md "honest limitation"):
an entity-anchored read of a natural-history registry to lift the burden axes from
definition-grade [H] toward registry-grade [L]. R5 (GeneReviews) deliberately
WITHHELD [O]-fill because a full-chapter first-match over-triggers; R6 uses
Orphanet's STRUCTURED, entity-anchored fields, so "entity-anchored" is automatic
(every value is attached to an ORPHAcode, never parsed out of free text) -- the
methodological upgrade R5 deferred to.

No network: reads the r6_orphanet_fetch.py cache (sha-pinned) and the R5 registry
layer. Imports the FROZEN R3 builder via importlib (tier maps, HPO subtrees,
composite, sensitivity) so the scoring rules cannot drift from R3.

DECLARED, A-PRIORI RULES (no tuning; recorded in the output + BURDEN_INDEX.md):
 JOIN -- Exact only. A disease takes a registry [L] lift only from an Orphanet
   concept its OMIM maps to with relation E in en_product1; BTNT/NTBT recorded as
   context but NO lift. Several Exact ORPHAcodes -> their onset/HPO sets unioned.
 ONSET (O) <- en_product9_ages AverageAgeOfOnset, fixed category->tier (same a-priori
   earliness scale as BURDEN_INDEX): Antenatal/Neonatal 1.0 . Infancy 0.85 .
   Childhood 0.7 . Adolescent 0.55 . Adult 0.35 . Elderly 0.2 . ("All ages"/"No data
   available" = not a single tier -> recorded, no lift). O = EARLIEST over usable
   Orphanet categories combined with any existing HPO-[L] onset; registry [L]
   supersedes a prior [H]/[O].
 MORTALITY (M) <- en_product4 HPO terms in HP:0040006 (Mortality/Aging) with an R3
   MORT_VAL tier AND Orphanet frequency >= Frequent. M = most-severe tier; supersedes.
 PROGRESSION (P) <- en_product4 HPO terms in HP:0031797 (Clinical course) with an R3
   PROG_VAL tier AND frequency >= Frequent. P = most-severe tier; supersedes.
 FREQUENCY GATE -- only Obligate/Very frequent/Frequent count. A phenotype at
   Occasional/Very-rare/Excluded does not characterise typical natural history and
   would repeat the over-trigger R5 withheld. Declared a priori.
 SEVERITY (S) / DISABILITY (D) NOT lifted: Orphadata has no structured severity- or
   disability-magnitude tier; left as banked, consultation outcome recorded so the
   obstacle is named. Path for S/D/most P stays OMIM clinical synopsis (licensed) /
   GBD / published survival & functional literature.
 ADD-ONLY / ABSENCE-SAFE -- Orphanet ABSENCE never downgrades/removes a banked value.

The registry layer is CUMULATIVE: R5 + R6. This stage OVERWRITES the *_registry
artifacts; the R3/R4 BANKED files stay byte-identical (gate-verified). Unlike R5
(value frozen), R6 may MOVE raw_burden -- the intended upgrade: a value changes only
when a structured, Exact-mapped Orphanet registry field supports it.

Out (overwrite): data/curated/burden_scores_registry.{json,csv}
                 data/curated/burden_residual_registry.{json,csv}
(treatments_registry.* untouched.)
"""
import os, csv, json, copy, hashlib, importlib.util, collections
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
ORPHA = os.path.join(ROOT, "data", "raw", "orphanet")
P1 = os.path.join(ORPHA, "en_product1.xml")
P9 = os.path.join(ORPHA, "en_product9_ages.xml")
P4 = os.path.join(ORPHA, "en_product4.xml")
RETRIEVED = "2026-06-17"
ORPHA_SRC = ("Orphanet/Orphadata en_product9_ages.xml + en_product4.xml + en_product1.xml, "
             "CC BY 4.0, retrieved " + RETRIEVED)

OUT_SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
OUT_SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
OUT_RESID_J = os.path.join(CUR, "burden_residual_registry.json")
OUT_RESID_C = os.path.join(CUR, "burden_residual_registry.csv")

# frozen R3 import (tier maps, HPO loaders/subtree, composite, sensitivity)
_spec = importlib.util.spec_from_file_location("r3b", os.path.join(HERE, "r3_burden_index.py"))
r3 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(r3)
NAME, PARENTS, CHILDREN = r3.load_obo()
MORT_SUB = set(r3.subtree("HP:0040006", CHILDREN))
COURSE_SUB = set(r3.subtree("HP:0031797", CHILDREN))
W = r3.W
GRADE_RANK = r3.GRADE_RANK
floor_grade = r3.floor_grade
weighted_burden = r3.weighted_burden
spearman = r3.spearman
RANK_MIN = r3.RANK_MIN_AXES

ONSET_TIER = {"Antenatal": 1.0, "Neonatal": 1.0, "Infancy": 0.85, "Childhood": 0.7,
              "Adolescent": 0.55, "Adult": 0.35, "Elderly": 0.2}
ONSET_SKIP = {"All ages", "No data available"}
FREQ_OK = {"Obligate (100%)", "Very frequent (99-80%)", "Frequent (79-30%)"}


def load_omim_to_orpha():
    root = ET.parse(P1).getroot(); m = {}
    for d in root.iter("Disorder"):
        oc = d.findtext("OrphaCode"); nm = d.findtext("Name")
        for e in d.findall(".//ExternalReference"):
            if e.findtext("Source") == "OMIM":
                rel = (e.findtext(".//DisorderMappingRelation/Name") or "").split(" ")[0]
                m.setdefault(e.findtext("Reference"), []).append((oc, rel, nm))
    return m


def load_onset():
    root = ET.parse(P9).getroot(); o = {}
    for d in root.iter("Disorder"):
        cats = sorted({x.text for x in d.findall(".//AverageAgeOfOnset/Name")})
        if cats:
            o[d.findtext("OrphaCode")] = cats
    return o


def load_hpo():
    root = ET.parse(P4).getroot(); h = {}
    for d in root.iter("Disorder"):
        rows = [(a.findtext(".//HPOId"), a.findtext(".//HPOFrequency/Name"))
                for a in d.findall(".//HPODisorderAssociation")]
        if rows:
            h[d.findtext("OrphaCode")] = rows
    return h


def onset_lift(cats):
    usable = [(ONSET_TIER[c], c) for c in cats if c in ONSET_TIER]
    if not usable:
        return None, []
    return max(v for v, _ in usable), [c for _, c in usable]


def hpo_axis_lift(hpo_rows, subtree, val_map):
    hits = [(NAME.get(hid, hid), fr, val_map[hid])
            for hid, fr in hpo_rows if fr in FREQ_OK and hid in subtree and hid in val_map]
    if not hits:
        return None, []
    return max(t for _, _, t in hits), hits


def freq_short(f):
    return f.split(" (")[0] if f else f


def _append_once(s, frag, sep=" | "):
    """append frag iff not already present (idempotent across re-runs)."""
    s = s or ""
    return s if frag in s else (s + sep + frag if s else frag)


def _orphanet_basis(b, frag):
    """set the ' | Orphanet ...' suffix idempotently, preserving any earlier
    (e.g. R5 GeneReviews) ' | ...' note that precedes the Orphanet suffix. frag
    must begin with 'Orphanet'."""
    b = b or ""
    i = b.find(" | Orphanet")
    base = b[:i] if i != -1 else b
    return base + " | " + frag


def main():
    omim2orpha = load_omim_to_orpha()
    onset_by = load_onset()
    hpo_by = load_hpo()

    # R6 reads the R5 registry as its base and OVERWRITES it (cumulative registry layer).
    # If the on-disk base already carries R6 (an accidental re-run), regenerate the clean
    # R5 base first so the pass stays idempotent. The canonical pipeline is r5 -> r6; the
    # gate runs that chain. r5_accession_apply is no-network (banked + GeneReviews cache).
    base = json.load(open(OUT_SCORES_J))
    if "R6_orphanet_natural_history" in base.get("registry_passes", []):
        import subprocess, sys
        subprocess.run([sys.executable, os.path.join(HERE, "r5_accession_apply.py")],
                       check=True, stdout=subprocess.DEVNULL)
        base = json.load(open(OUT_SCORES_J))
    recs = copy.deepcopy(base["records"])

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = {"e": float(r["efficacy_offset_e"]), "R_treat": float(r["R_treat"]),
                               "grade": r["grade"], "evidence_status": r["evidence_status"]}

    lift = collections.Counter()
    promotions, demotions, locked, per_axis_changes = [], [], [], []

    for r in recs:
        comp = r["components"]; omims = r["omim_codes"]
        exact, nonexact = [], []
        for om in omims:
            for (oc, rel, onm) in omim2orpha.get(om, []):
                (exact if rel == "E" else nonexact).append((om, oc, rel, onm))
        exact_oc = sorted({oc for _, oc, _, _ in exact})
        nonexact_oc = sorted({f"{oc}({rel})" for _, oc, rel, _ in nonexact})
        meta = {"exact_orphacodes": exact_oc, "nonexact_mappings": nonexact_oc, "source": ORPHA_SRC}
        r["orphanet"] = meta

        if not exact_oc:
            note = (f"no exact Orphanet mapping (only broader/narrower {nonexact_oc or 'none'}); "
                    "Orphanet natural history not applied")
            meta["applied"] = False; meta["reason"] = note
            for ax in ("S", "D"):
                if comp[ax]["grade"] == "[O]":
                    comp[ax]["obstacle"] = _append_once(comp[ax]["obstacle"], note)
            lift["disease_no_exact_mapping"] += 1
        else:
            meta["applied"] = True
            onset_cats = sorted({c for oc in exact_oc for c in onset_by.get(oc, [])})
            hpo_rows = [row for oc in exact_oc for row in hpo_by.get(oc, [])]
            meta["onset_categories"] = onset_cats
            ocs = ",".join(exact_oc)

            # ONSET
            o_tier, o_used = onset_lift(onset_cats)
            if o_tier is not None:
                o = comp["O"]; old_v, old_g = o["value"], o["grade"]
                src = f"Orphanet en_product9 AverageAgeOfOnset {o_used} (ORPHA:{ocs}); {ORPHA_SRC}"
                if old_g == "[L]" and old_v is not None:
                    new_v = max(old_v, o_tier)
                    tag = "corroborated" if new_v == old_v else "extended earlier"
                    o["value"] = new_v; o["grade"] = "[L]"
                    o["basis"] = _orphanet_basis(o["basis"], f"Orphanet onset {o_used} {tag} (ORPHA:{ocs})")
                    o["source"] = _append_once(o.get("source", ""), src, sep=" + ")
                    lift["O_L_corroborated" if new_v == old_v else "O_L_extended"] += 1
                    if new_v != old_v:
                        per_axis_changes.append((r["entity"], "O", old_v, new_v, old_g, "[L]"))
                else:
                    o["value"] = o_tier; o["grade"] = "[L]"
                    o["basis"] = f"earliest Orphanet AverageAgeOfOnset tier from {o_used} (ORPHA:{ocs})"
                    o.pop("obstacle", None); o["source"] = src
                    lift["O_H_to_L" if old_g == "[H]" else "O_O_to_L"] += 1
                    per_axis_changes.append((r["entity"], "O", old_v, o_tier, old_g, "[L]"))
            elif onset_cats:
                comp["O"].setdefault("orphanet_note",
                    f"Orphanet onset = {onset_cats} (non-specific / 'All ages'); not mapped to a tier; axis unchanged")

            # MORTALITY
            m_tier, m_hits = hpo_axis_lift(hpo_rows, MORT_SUB, r3.MORT_VAL)
            if m_tier is not None:
                m = comp["M"]; old_v, old_g = m["value"], m["grade"]
                terms = "; ".join(f"{n} ({freq_short(fr)})" for n, fr, _ in m_hits)
                src = f"Orphanet en_product4 HPO Mortality/Aging: {terms} (ORPHA:{ocs}); {ORPHA_SRC}"
                if old_g == "[L]" and old_v is not None:
                    new_v = max(old_v, m_tier)
                    m["value"] = new_v; m["grade"] = "[L]"
                    m["basis"] = _orphanet_basis(m["basis"], f"Orphanet corroborates: {terms}")
                    m["source"] = _append_once(m.get("source", ""), src, sep=" + ")
                    lift["M_L_corroborated"] += 1
                    if new_v != old_v:
                        per_axis_changes.append((r["entity"], "M", old_v, new_v, old_g, "[L]"))
                else:
                    m["value"] = m_tier; m["grade"] = "[L]"
                    m["basis"] = f"Orphanet HPO Mortality/Aging (freq>=Frequent): {terms}"
                    m.pop("obstacle", None); m["source"] = src
                    lift["M_H_to_L" if old_g == "[H]" else "M_O_to_L"] += 1
                    per_axis_changes.append((r["entity"], "M", old_v, m_tier, old_g, "[L]"))

            # PROGRESSION
            p_tier, p_hits = hpo_axis_lift(hpo_rows, COURSE_SUB, r3.PROG_VAL)
            if p_tier is not None:
                p = comp["P"]; old_v, old_g = p["value"], p["grade"]
                terms = "; ".join(f"{n} ({freq_short(fr)})" for n, fr, _ in p_hits)
                src = f"Orphanet en_product4 HPO Clinical-course: {terms} (ORPHA:{ocs}); {ORPHA_SRC}"
                if old_g == "[L]" and old_v is not None:
                    new_v = max(old_v, p_tier)
                    p["value"] = new_v; p["grade"] = "[L]"
                    p["basis"] = _orphanet_basis(p["basis"], f"Orphanet corroborates: {terms}")
                    p["source"] = _append_once(p.get("source", ""), src, sep=" + ")
                    lift["P_L_corroborated"] += 1
                    if new_v != old_v:
                        per_axis_changes.append((r["entity"], "P", old_v, new_v, old_g, "[L]"))
                else:
                    p["value"] = p_tier; p["grade"] = "[L]"
                    p["basis"] = f"Orphanet HPO Clinical-course (freq>=Frequent): {terms}"
                    p.pop("obstacle", None); p["source"] = src
                    lift["P_H_to_L" if old_g == "[H]" else "P_O_to_L"] += 1
                    per_axis_changes.append((r["entity"], "P", old_v, p_tier, old_g, "[L]"))

            # SEVERITY / DISABILITY: no Orphanet tier -> record outcome
            for ax, label in (("S", "severity-magnitude"), ("D", "disability-magnitude")):
                note = (f"Orphanet en_product4 (ORPHA:{ocs}) consulted: Orphadata carries no structured "
                        f"{label} tier (frequency-annotated phenotypes only); axis unchanged, deferred to "
                        f"OMIM clinical synopsis (licensed) / published functional literature, not guessed")
                if comp[ax]["grade"] == "[O]":
                    comp[ax]["obstacle"] = _append_once(comp[ax]["obstacle"], note)
                    lift[f"{ax}_O_kept_no_tier"] += 1
                else:
                    comp[ax].setdefault("orphanet_note", note)
                    lift[f"{ax}_kept_{comp[ax]['grade'].strip('[]')}"] += 1

        # recompute composite / coverage / rankability
        present = [k for k in W if comp[k]["value"] is not None]
        r["axes_scored"] = len(present)
        r["axes_missing"] = [k for k in W if k not in present]
        r["rankable"] = len(present) >= RANK_MIN
        r["raw_burden"] = weighted_burden(comp, W)
        r["raw_burden_grade_floor"] = floor_grade([comp[k]["grade"] for k in W])
        r["raw_burden_grade_present"] = floor_grade([comp[k]["grade"] for k in present]) if present else "[O]"

    # promotions/demotions vs banked R4
    banked = {x["cui"]: x for x in json.load(open(os.path.join(CUR, "burden_scores.json")))["records"]}
    for r in recs:
        was = banked[r["cui"]]["rankable"]
        if r["rankable"] and not was:
            promotions.append({"entity": r["entity"], "cui": r["cui"],
                               "axes_scored": r["axes_scored"], "raw_burden": r["raw_burden"]})
        elif not r["rankable"] and was:
            demotions.append({"entity": r["entity"], "cui": r["cui"]})

    placed = sorted([r for r in recs if r["rankable"]],
                    key=lambda r: (-(r["raw_burden"] if r["raw_burden"] is not None else -1),
                                   -r["axes_scored"], r["entity"]))
    not_placed = sorted([r for r in recs if not r["rankable"]],
                        key=lambda r: (-r["axes_scored"], r["entity"]))
    raw_rank = {}
    for i, r in enumerate(placed, 1):
        r["rank"] = i; raw_rank[r["cui"]] = i
    for r in not_placed:
        r["rank"] = None
    ordered = placed + not_placed

    for r in ordered:
        t = treat.get(r["cui"], {"e": 0.0, "R_treat": 1.0, "grade": "[O]", "evidence_status": "unknown"})
        raw = r["raw_burden"]; Rt = round(t["R_treat"], 12)
        r["burden_score"] = round(raw * Rt, 12) if raw is not None else None
        r["burden_score_grade"] = floor_grade([r["raw_burden_grade_present"], t["grade"]]) if raw is not None else "[O]"
        r["treatment_grade"] = t["grade"]
        present = [k for k in W if r["components"][k]["value"] is not None]
        scored_grades = [r["components"][k]["grade"] for k in present]
        r["order_locked"] = bool(r["rankable"] and present and
                                 all(GRADE_RANK.get(g, 0) >= GRADE_RANK["[L]"] for g in scored_grades))
        r["treatability"] = {"value": Rt, "grade": t["grade"],
                             "basis": f"R_treat = 1 - e = {Rt:.2f}; e = {t['e']:.2f} for evidence_status '{t['evidence_status']}'"}
        if r["order_locked"]:
            locked.append({"entity": r["entity"], "cui": r["cui"], "axes_scored": r["axes_scored"]})

    residual_sorted = sorted([r for r in ordered if r["rankable"]],
                             key=lambda r: (-(r["burden_score"] if r["burden_score"] is not None else -1),
                                            -(r["raw_burden"] if r["raw_burden"] is not None else -1),
                                            -r["axes_scored"], r["entity"]))
    for i, r in enumerate(residual_sorted, 1):
        r["residual_rank"] = i; r["raw_rank"] = raw_rank.get(r["cui"])
        r["rank_shift_vs_raw"] = (r["raw_rank"] - i) if r["raw_rank"] else None
    for r in not_placed:
        r["residual_rank"] = None; r["raw_rank"] = None; r["rank_shift_vs_raw"] = None

    alt = {"equal_default": W,
           "onset_heavy": {"O": .40, "P": .15, "S": .15, "M": .15, "D": .15},
           "mortality_heavy": {"O": .15, "P": .15, "S": .15, "M": .40, "D": .15},
           "severity_heavy": {"O": .15, "P": .15, "S": .40, "M": .15, "D": .15},
           "drop_disability_core4": {"O": .25, "P": .25, "S": .25, "M": .25, "D": 0.0}}
    default_vals = [r["raw_burden"] or 0.0 for r in placed]
    sensitivity = {lbl: {"weights": ww,
                         "spearman_vs_default": spearman(default_vals,
                             [weighted_burden(r["components"], ww) or 0.0 for r in placed])}
                   for lbl, ww in alt.items()}
    cov = {k: dict(collections.Counter(r["components"][k]["grade"] for r in ordered)) for k in W}

    # ----- write burden_scores_registry.{json,csv} -----
    payload = {
        "schema": "disease_wp.burden_scores/v1",
        "phase": "R6 (natural-history registry; cumulative over R5)",
        "investigation_only": base.get("investigation_only", True),
        "generated": RETRIEVED,
        "method": "methodology/BURDEN_INDEX.md + Orphanet natural-history registry pass (R6)",
        "derived_from": "burden_scores_registry.json (R5 GeneReviews) + data/raw/orphanet/ cache (Orphadata CC BY 4.0)",
        "registry_passes": ["R5_genereviews_accession_dating", "R6_orphanet_natural_history"],
        "weights_default": W,
        "composite_rule": base.get("composite_rule"),
        "floor_rule": base.get("floor_rule"),
        "ranking_basis": base.get("ranking_basis"),
        "rankability": base.get("rankability"),
        "cohort_size": len(ordered),
        "lift_policy": ("Orphanet structured fields, ENTITY-ANCHORED per ORPHAcode, EXACT OMIM<->ORPHA only. "
                        "O<-en_product9 AverageAgeOfOnset (fixed earliness tier map). M<-en_product4 HPO "
                        "Mortality/Aging (HP:0040006), P<-en_product4 HPO Clinical-course (HP:0031797), each "
                        "with an R3 tier AND Orphanet frequency>=Frequent. Registry [L] supersedes [H]/[O]. "
                        "S and D not lifted (Orphadata has no severity/disability magnitude tier). Add-only: "
                        "Orphanet absence never downgrades a banked value."),
        "join_rule": "OMIM<->ORPHA relation E only (en_product1); BTNT/NTBT recorded as context, no lift",
        "onset_tier_map": ONSET_TIER,
        "onset_skip_categories": sorted(ONSET_SKIP),
        "frequency_gate": sorted(FREQ_OK),
        "orphanet_sources": json.load(open(os.path.join(ORPHA, "_fetch_log.json"))),
        "lift_counts": dict(lift),
        "axis_value_changes": [{"entity": e, "axis": a, "old": ov, "new": nv,
                                "old_grade": og, "new_grade": ng}
                               for (e, a, ov, nv, og, ng) in per_axis_changes],
        "promotions_from_not_placed": promotions,
        "demotions_to_not_placed": demotions,
        "order_locked_diseases": locked,
        "order_lock_rule": "order_locked = rankable (>=3 axes) AND every scored axis grade in {[L],[V]}",
        "sensitivity": sensitivity,
        "axis_grade_coverage_registry": cov,
        "records": [{
            "rank": r["rank"], "entity": r["entity"], "cui": r["cui"], "tier": r["tier"],
            "system_class": r["system_class"], "genes": r["genes"], "omim_codes": r["omim_codes"],
            "components": r["components"], "axes_scored": r["axes_scored"], "rankable": r["rankable"],
            "axes_missing": r["axes_missing"], "raw_burden": r["raw_burden"],
            "raw_burden_grade_floor": r["raw_burden_grade_floor"],
            "raw_burden_grade_present": r["raw_burden_grade_present"],
            "treatability": r["treatability"], "burden_score": r["burden_score"],
            "burden_score_grade": r["burden_score_grade"], "treatment_grade": r["treatment_grade"],
            "order_locked": r["order_locked"], "orphanet": r["orphanet"],
            "emergence_link": r.get("emergence_link"),
        } for r in ordered],
        "grade_vocabulary": base.get("grade_vocabulary"),
    }
    json.dump(payload, open(OUT_SCORES_J, "w"), indent=2, ensure_ascii=False)

    cols = ["rank", "rankable", "entity", "cui", "tier", "system_class",
            "O_value", "O_grade", "P_value", "P_grade", "S_value", "S_grade",
            "M_value", "M_grade", "D_value", "D_grade",
            "axes_scored", "raw_burden", "raw_burden_grade_floor", "raw_burden_grade_present",
            "R_treat", "R_treat_grade", "burden_score", "burden_score_grade",
            "order_locked", "exact_orphacodes", "emergence_link"]
    with open(OUT_SCORES_C, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for r in ordered:
            ax = r["components"]
            def cell(v):
                return "" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)
            w.writerow([cell(r["rank"]), "yes" if r["rankable"] else "no", r["entity"], r["cui"],
                        r["tier"], r["system_class"],
                        cell(ax["O"]["value"]), ax["O"]["grade"], cell(ax["P"]["value"]), ax["P"]["grade"],
                        cell(ax["S"]["value"]), ax["S"]["grade"], cell(ax["M"]["value"]), ax["M"]["grade"],
                        cell(ax["D"]["value"]), ax["D"]["grade"],
                        r["axes_scored"], cell(r["raw_burden"]),
                        r["raw_burden_grade_floor"], r["raw_burden_grade_present"],
                        cell(r["treatability"]["value"]), r["treatability"]["grade"],
                        cell(r["burden_score"]), r["burden_score_grade"],
                        "yes" if r["order_locked"] else "no",
                        ";".join(r["orphanet"].get("exact_orphacodes", [])),
                        "yes" if r.get("emergence_link") else ""])

    # ----- write burden_residual_registry.{json,csv} -----
    rj = {
        "schema": "disease_wp.burden_residual/v1",
        "phase": "R6 (natural-history registry; cumulative over R5)",
        "derived_from": "burden_scores_registry.json (R5+R6) + treatments_registry.csv (R4/R5 offset)",
        "residual_rule": "burden_score = raw_burden * (1 - e); placed = rankability cut (axes>=3) re-ranked by residual burden_score desc, then raw_burden desc, axes desc, entity",
        "order_lock_rule": payload["order_lock_rule"],
        "placed": len(residual_sorted),
        "not_placed": len(not_placed),
        "promoted_from_not_placed": promotions,
        "order_locked_count": len(locked),
        "records": [{
            "residual_rank": r["residual_rank"], "raw_rank": r["raw_rank"],
            "rank_shift_vs_raw": r["rank_shift_vs_raw"], "entity": r["entity"], "cui": r["cui"],
            "rankable": r["rankable"], "axes_scored": r["axes_scored"], "raw_burden": r["raw_burden"],
            "burden_score": r["burden_score"], "burden_score_grade": r["burden_score_grade"],
            "treatment_grade": r["treatment_grade"], "order_locked": r["order_locked"],
        } for r in (residual_sorted + not_placed)],
    }
    json.dump(rj, open(OUT_RESID_J, "w"), indent=2, ensure_ascii=False)

    rcols = ["residual_rank", "raw_rank", "rank_shift_vs_raw", "rankable", "entity", "cui",
             "tier", "system_class", "axes_scored", "raw_burden", "raw_burden_grade_present",
             "evidence_status", "efficacy_offset_e", "R_treat", "R_treat_grade",
             "burden_score", "burden_score_grade", "treatment_grade", "order_locked",
             "exact_orphacodes"]
    with open(OUT_RESID_C, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(rcols)
        for r in (residual_sorted + not_placed):
            def cell(v):
                return "" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)
            t = treat.get(r["cui"], {"e": 0.0, "R_treat": 1.0, "grade": "[O]", "evidence_status": "unknown"})
            w.writerow([cell(r["residual_rank"]), cell(r["raw_rank"]), cell(r["rank_shift_vs_raw"]),
                        "yes" if r["rankable"] else "no", r["entity"], r["cui"],
                        r["tier"], r["system_class"], r["axes_scored"],
                        cell(r["raw_burden"]), r["raw_burden_grade_present"],
                        t["evidence_status"], f"{t['e']:.4f}", f"{t['R_treat']:.4f}", t["grade"],
                        cell(r["burden_score"]), r["burden_score_grade"], r["treatment_grade"],
                        "yes" if r["order_locked"] else "no",
                        ";".join(r["orphanet"].get("exact_orphacodes", []))])

    # ----- report -----
    print("--- R6 natural-history registry pass (Orphanet) ---")
    print(f"  exact-mapped diseases: {sum(1 for r in recs if r['orphanet'].get('applied'))}/{len(recs)}"
          f"  (no exact mapping: {lift['disease_no_exact_mapping']})")
    print("\n  lift events:")
    for k in sorted(lift):
        print(f"    {k:24s} {lift[k]}")
    print("\n  axis grade coverage AFTER R6 (over 35):")
    for k in W:
        print(f"    {k}: {cov[k]}")
    print(f"\n  promotions (not-placed -> placed): {len(promotions)}"
          + ("".join(f"\n      + {p['entity']} ({p['axes_scored']}/5)" for p in promotions) if promotions else " (none)"))
    print(f"  demotions: {len(demotions)}")
    print(f"  order_locked diseases (all scored axes [L]/[V], >=3 axes): {len(locked)}"
          + ("".join(f"\n      * {x['entity']}" for x in locked) if locked else " (none -> order stays provisional [H])"))
    if per_axis_changes:
        print("\n  axis VALUE changes (registry supersedes prior grade):")
        for e, a, ov, nv, og, ng in per_axis_changes:
            print(f"      {e[:38]:38s} {a}: {ov}{og} -> {nv}{ng}")
    print("\n  sensitivity (Spearman rho of raw order vs equal-weight default):")
    for lbl, sd in sensitivity.items():
        print(f"    {lbl:24s} rho = {sd['spearman_vs_default']}")

    h = hashlib.sha256()
    for p in (OUT_SCORES_C, OUT_SCORES_J, OUT_RESID_C, OUT_RESID_J):
        h.update(open(p, "rb").read())
    print(f"\n  registry-set sha256[:12]: {h.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
