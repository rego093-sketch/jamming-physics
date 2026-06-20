#!/usr/bin/env python3
# =============================================================================
# R8 - open-source SEVERITY pass  (cumulative over R5+R6+R7)
# -----------------------------------------------------------------------------
# Lifts the BURDEN_INDEX severity axis (S) from an OPEN, citeable, NCBI-grade
# structured source: the HPO clinical-modifier *Severity* subtree
# (HP:0012824 -> Mild/Moderate/Severe/Profound) carried in the pinned
# phenotype.hpoa, applied through a DECLARED, CITED, dominant-sequela curation
# join -- exactly the discipline R7 used for disability against the GBD weights.
#
# Honesty rails (enforced by code/pipeline/r8_gate.py):
#   * the handover claim "HPO has no severity branch" is FALSE: HP:0012824 exists
#     and maps 1:1 to the S tiers; severity is wired like O/P/M are (HPO subtree).
#   * BUT for this cohort the severity annotations are FEATURE-level, so a naive
#     "take any feature's modifier" gives category errors (Mild tall stature,
#     Mild DMD, Severe achondroplasia). A disease tier is therefore taken ONLY
#     via a cited DOMINANT-sequela join (methodology/severity_hpo_join.csv);
#     every other considered annotation is declined with a per-disease reason
#     (methodology/severity_hpo_excluded.csv). NO inference; OMIM synopsis is
#     API-key-gated and the key is unobtainable for an individual researcher,
#     so that path is removed (not "deferred").
#   * add-only: registry [L] supersedes [H]/[O]; an existing [L] is corroborated
#     (max). A missing/declined source NEVER downgrades a value.
#   * each join row is VALIDATED at runtime against the pinned phenotype.hpoa
#     (phenotype, modifier, frequency, reference must all be re-found) or the
#     build exits nonzero -- the lift cannot drift from the cited source.
#   * a-priori modifier -> tier cut-points (Mild .25 / Moderate .5 / Severe .75
#     / Profound 1.0; Borderline -> no tier), declared, not fitted.
#
# Self-healing / idempotent: if its own pass-tag is already present, R8 re-runs
# r5 -> r6 -> r7 to rebuild a clean R7 base, then re-applies. Writes the payload
# back to burden_scores_registry.json (+ burden_residual_registry.{json,csv})
# and prints the registry-set sha256[:12] over the four emitted artifacts.
# The R8 pipeline is LIVING CODE and is intentionally NOT in MANIFEST_governed.
# =============================================================================
import os, re, csv, json, copy, gzip, hashlib, importlib.util, collections, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
HPO = os.path.join(ROOT, "data", "raw", "hpo")
HPOA = os.path.join(HPO, "phenotype.hpoa.gz")
RETRIEVED = "2026-06-18"
HPOA_VER = "v2026-06-06"

OUT_SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
OUT_SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
OUT_RESID_J = os.path.join(CUR, "burden_residual_registry.json")
OUT_RESID_C = os.path.join(CUR, "burden_residual_registry.csv")

# frozen R3 import (same helpers R7 uses)
_spec = importlib.util.spec_from_file_location("r3b", os.path.join(HERE, "r3_burden_index.py"))
r3 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(r3)
W = r3.W
GRADE_RANK = r3.GRADE_RANK
floor_grade = r3.floor_grade
weighted_burden = r3.weighted_burden
spearman = r3.spearman
RANK_MIN = r3.RANK_MIN_AXES

# HPO clinical-modifier Severity subtree HP:0012824 -> S tier (a-priori; declared)
SEV_SUBTREE = "HP:0012824"
SEV_MODIFIER_TIER = {
    "HP:0012825": ("Mild", 0.25),
    "HP:0012826": ("Moderate", 0.5),
    "HP:0012827": ("Borderline", None),   # between Mild/Moderate; no S tier -> does not lift
    "HP:0012828": ("Severe", 0.75),
    "HP:0012829": ("Profound", 1.0),
}
HPO_SRC_TMPL = ("HPO clinical-modifier Severity subtree {sub} in phenotype.hpoa {ver} "
                "(pinned sha256[:12]={sha}, retrieved {ret}); Human Phenotype Ontology, "
                "CC BY 4.0")

# a-priori inclusion criterion (declared, not fitted): the annotated Severity modifier must sit
# on a feature that is OBLIGATE for the disease, so it represents the whole disease rather than a
# sub-phenotype. Obligate = HPO frequency 100% (n/m with n==m) or the HPO term "Obligate".
OBLIGATE_TERM = "HP:0040280"


def _is_obligate(freq):
    f = (freq or "").strip()
    if OBLIGATE_TERM in f or f in ("100%", "1/1"):
        return True
    m = re.fullmatch(r"(\d+)\s*/\s*(\d+)", f)
    if m and int(m.group(1)) == int(m.group(2)) and int(m.group(2)) > 0:
        return True
    m = re.fullmatch(r"(\d+(?:\.\d+)?)%", f)
    return bool(m and abs(float(m.group(1)) - 100.0) < 1e-9)



def _append_once(s, frag, sep=" | "):
    s = s or ""
    return s if frag in s else (s + sep + frag if s else frag)


def load_join():
    with open(os.path.join(METH, "severity_hpo_join.csv"), newline="") as fh:
        return {r["cui"]: r for r in csv.DictReader(fh)}


def load_excluded():
    rows = collections.defaultdict(list)
    with open(os.path.join(METH, "severity_hpo_excluded.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            rows[r["cui"]].append(r)
    return rows


def load_hpoa_index():
    """index: (OMIM_id, hpo_id) -> list of {modifier,frequency,reference,aspect}; plus file sha."""
    idx = collections.defaultdict(list)
    h = hashlib.sha256()
    with open(HPOA, "rb") as fb:
        h.update(fb.read())
    sha = h.hexdigest()
    with gzip.open(HPOA, "rt") as f:
        header = None
        for line in f:
            if line.startswith("#"):
                continue
            if header is None:
                header = line.rstrip("\n").split("\t")
                ci = {c: i for i, c in enumerate(header)}
                continue
            p = line.rstrip("\n").split("\t")
            dbid = p[ci["database_id"]]
            if not dbid.startswith("OMIM:"):
                continue
            mim = dbid.split(":")[1]
            idx[(mim, p[ci["hpo_id"]])].append({
                "modifier": p[ci["modifier"]], "frequency": p[ci["frequency"]],
                "reference": p[ci["reference"]], "aspect": p[ci["aspect"]],
            })
    return idx, sha


def validate_join_row(jr, rec_omims, hpoa_idx):
    """Re-find the cited (phenotype, modifier, frequency, reference) in the pinned hpoa
    under one of the record's OMIM phenotype MIMs. Returns the matched MIM or exits."""
    pheno = jr["hpo_phenotype"]; modi = jr["severity_modifier"]
    freq = jr["frequency"].strip(); ref = jr["reference"].strip()
    for mim in rec_omims:
        for row in hpoa_idx.get((mim, pheno), []):
            if modi in row["modifier"] and row["frequency"].strip() == freq and row["reference"].strip() == ref:
                return mim
    print(f"  ERROR: severity-join row for {jr['entity']} ({jr['cui']}) NOT re-found in pinned "
          f"phenotype.hpoa: expected {pheno} modifier {modi} freq {freq} ref {ref} under OMIM "
          f"{sorted(rec_omims)}", file=sys.stderr)
    sys.exit(4)


def main():
    join = load_join()
    excluded = load_excluded()
    hpoa_idx, hpoa_sha = load_hpoa_index()
    hpo_src = HPO_SRC_TMPL.format(sub=SEV_SUBTREE, ver=HPOA_VER, sha=hpoa_sha[:12], ret=RETRIEVED)

    base = json.load(open(OUT_SCORES_J))
    # self-healing: if R8 already applied, rebuild a clean R7 base from r5 -> r6 -> r7
    if "R8_open_severity" in base.get("registry_passes", []):
        for stage in ("r5_accession_apply.py", "r6_naturalhistory_registry.py",
                      "r7_naturalhistory_registry2.py"):
            subprocess.run([sys.executable, os.path.join(HERE, stage)],
                           check=True, stdout=subprocess.DEVNULL)
        base = json.load(open(OUT_SCORES_J))
    if "R7_open_naturalhistory" not in base.get("registry_passes", []):
        print("  ERROR: R8 expects an R7 base (registry_passes missing R7_open_naturalhistory)",
              file=sys.stderr)
        sys.exit(3)

    recs = copy.deepcopy(base["records"])

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = {"e": float(r["efficacy_offset_e"]), "R_treat": float(r["R_treat"]),
                               "grade": r["grade"], "evidence_status": r["evidence_status"]}

    lift = collections.Counter()
    promotions, locked, per_axis_changes = [], [], []
    sev_join_audit, sev_excluded_audit = [], []

    for r in recs:
        comp = r["components"]; cui = r["cui"]
        rec_omims = set(str(x) for x in (r.get("omim_codes") or []))
        s_ax = comp["S"]

        if cui in join:
            jr = join[cui]
            mim = validate_join_row(jr, rec_omims, hpoa_idx)
            modi = jr["severity_modifier"]
            if modi not in SEV_MODIFIER_TIER:
                print(f"  ERROR: modifier {modi} not in declared Severity subtree map", file=sys.stderr)
                sys.exit(4)
            mod_name, tier = SEV_MODIFIER_TIER[modi]
            if tier is None:
                print(f"  ERROR: modifier {modi} ({mod_name}) carries no S tier; cannot lift "
                      f"{jr['entity']}", file=sys.stderr)
                sys.exit(4)
            # declared cut-point consistency: the CSV tier must equal the a-priori map
            if abs(float(jr["severity_tier"]) - tier) > 1e-9:
                print(f"  ERROR: severity_tier {jr['severity_tier']} for {jr['entity']} disagrees "
                      f"with a-priori map {modi}->{tier}", file=sys.stderr)
                sys.exit(4)
            # a-priori INCLUSION criterion: the severity-graded feature must be OBLIGATE for the
            # disease (HPO frequency 100% / "Obligate"), so the modifier reflects the whole disease
            # rather than a sub-phenotype. Non-obligate -> declined, never lifted.
            if not _is_obligate(jr["frequency"]):
                print(f"  ERROR: severity annotation for {jr['entity']} is not obligate "
                      f"(frequency {jr['frequency']!r}); inclusion criterion not met", file=sys.stderr)
                sys.exit(4)

            old_v, old_g = s_ax["value"], s_ax["grade"]
            cite = (f"HPO Severity modifier {modi} ({mod_name}) on {jr['hpo_phenotype']} "
                    f"({jr['hpo_phenotype_name']}), frequency {jr['frequency']}, ref {jr['reference']} "
                    f"-> severity tier {tier:.2f} [cut-points Mild .25/Moderate .5/Severe .75/Profound 1.0]; "
                    f"dominant-sequela basis: {jr['dominant_sequela_basis']}; {hpo_src}")
            sev_join_audit.append({"entity": r["entity"], "cui": cui, "omim": mim,
                                   "hpo_phenotype": jr["hpo_phenotype"],
                                   "hpo_phenotype_name": jr["hpo_phenotype_name"],
                                   "severity_modifier": modi, "severity_modifier_name": mod_name,
                                   "frequency": jr["frequency"], "reference": jr["reference"],
                                   "severity_tier": tier, "prior_value": old_v, "prior_grade": old_g})
            if old_g == "[L]" and old_v is not None:
                new_v = max(old_v, tier)
                tag = "corroborated" if new_v == old_v else "raised"
                s_ax["value"] = new_v; s_ax["grade"] = "[L]"
                s_ax["basis"] = _append_once(s_ax.get("basis", ""),
                                             f"HPO Severity modifier {mod_name} ({jr['hpo_phenotype_name']}) {tag}")
                s_ax["source"] = _append_once(s_ax.get("source", ""), cite, sep=" + ")
                lift["S_L_corroborated" if new_v == old_v else "S_L_raised"] += 1
                if new_v != old_v:
                    per_axis_changes.append((r["entity"], "S", old_v, new_v, old_g, "[L]"))
            else:
                s_ax["value"] = tier; s_ax["grade"] = "[L]"
                s_ax["basis"] = (f"HPO Severity modifier {mod_name} on {jr['hpo_phenotype_name']} "
                                 f"({jr['hpo_phenotype']}) -> tier {tier:.2f}")
                s_ax.pop("obstacle", None); s_ax["source"] = cite
                lift["S_H_to_L" if old_g == "[H]" else "S_O_to_L"] += 1
                per_axis_changes.append((r["entity"], "S", old_v, tier, old_g, "[L]"))

        elif cui in excluded:
            reasons = "; ".join(f"{x['considered_phenotype_name']} flagged "
                                f"{x['considered_modifier_name']}: {x['exclusion_reason']}"
                                for x in excluded[cui])
            note = ("HPO Severity-subtree annotation(s) considered and declined (feature-level, not a "
                    f"disease tier): {reasons}")
            if s_ax["grade"] == "[O]":
                s_ax["obstacle"] = _append_once(s_ax.get("obstacle", ""), note)
            else:
                s_ax["severity_hpo_note"] = note
            for x in excluded[cui]:
                sev_excluded_audit.append({"entity": r["entity"], "cui": cui,
                                           "considered_phenotype": x["considered_phenotype"],
                                           "considered_phenotype_name": x["considered_phenotype_name"],
                                           "considered_modifier": x["considered_modifier"],
                                           "considered_modifier_name": x["considered_modifier_name"],
                                           "exclusion_reason": x["exclusion_reason"]})
            lift["S_excluded_recorded"] += 1

        else:
            if s_ax["grade"] == "[O]":
                note = ("HPO clinical-modifier Severity subtree (HP:0012824) checked: this disease carries "
                        "no severity annotation on its dominant sequela in the pinned phenotype.hpoa; "
                        "Orphadata carries no severity tier; OMIM clinical synopsis (the disease-level "
                        "alternative) is API-key-gated and the key is unobtainable for an individual "
                        "researcher; spectrum/range text would require inference. S left open, not guessed")
                s_ax["obstacle"] = _append_once(s_ax.get("obstacle", ""), note)
                lift["S_O_kept_no_dominant_annotation"] += 1
            else:
                lift[f"S_kept_{s_ax['grade'].strip('[]')}"] += 1

        # ---------- recompute composite / coverage / rankability (identical to R7) ----------
        present = [k for k in W if comp[k]["value"] is not None]
        r["axes_scored"] = len(present)
        r["axes_missing"] = [k for k in W if k not in present]
        r["rankable"] = len(present) >= RANK_MIN
        r["raw_burden"] = weighted_burden(comp, W)
        r["raw_burden_grade_floor"] = floor_grade([comp[k]["grade"] for k in W])
        r["raw_burden_grade_present"] = floor_grade([comp[k]["grade"] for k in present]) if present else "[O]"

    # promotions vs banked R4
    banked = {x["cui"]: x for x in json.load(open(os.path.join(CUR, "burden_scores.json")))["records"]}
    for r in recs:
        if r["rankable"] and not banked[r["cui"]]["rankable"]:
            promotions.append({"entity": r["entity"], "cui": r["cui"],
                               "axes_scored": r["axes_scored"], "raw_burden": r["raw_burden"]})

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
           "disability_heavy": {"O": .15, "P": .15, "S": .15, "M": .15, "D": .40},
           "drop_disability_core4": {"O": .25, "P": .25, "S": .25, "M": .25, "D": 0.0}}
    default_vals = [r["raw_burden"] or 0.0 for r in placed]
    sensitivity = {lbl: {"weights": ww,
                         "spearman_vs_default": spearman(default_vals,
                             [weighted_burden(r["components"], ww) or 0.0 for r in placed])}
                   for lbl, ww in alt.items()}
    cov = {k: dict(collections.Counter(r["components"][k]["grade"] for r in ordered)) for k in W}

    payload = {
        "schema": "disease_wp.burden_scores/v1",
        "phase": "R8 (open-source severity: HPO Severity-modifier dominant-sequela join; cumulative over R5+R6+R7)",
        "investigation_only": base.get("investigation_only", True),
        "generated": RETRIEVED,
        "method": ("methodology/BURDEN_INDEX.md + GBD2013 disability weights (R7) + PMC mortality "
                   "corroboration (R7) + HPO Severity-modifier curation join (R8)"),
        "derived_from": ("burden_scores_registry.json (R5+R6+R7) + data/raw/hpo/phenotype.hpoa.gz "
                         f"(HPO {HPOA_VER}, pinned sha256[:12]={hpoa_sha[:12]}) + "
                         "methodology/severity_hpo_join.csv + methodology/severity_hpo_excluded.csv"),
        "registry_passes": list(base.get("registry_passes", [])) + ["R8_open_severity"],
        "weights_default": W,
        "composite_rule": base.get("composite_rule"),
        "floor_rule": base.get("floor_rule"),
        "ranking_basis": base.get("ranking_basis"),
        "rankability": base.get("rankability"),
        "cohort_size": len(ordered),
        "lift_policy": (
            base.get("lift_policy", "") + "  ||  R8: S <- HPO clinical-modifier Severity subtree "
            "(HP:0012824 -> Mild .25/Moderate .5/Severe .75/Profound 1.0) carried in the pinned "
            "phenotype.hpoa, applied ONLY through a cited DOMINANT-sequela curation join "
            "(methodology/severity_hpo_join.csv); grade [L] (curation join, like R7 disability). "
            "A disease's S lifts iff its severity-graded feature is OBLIGATE (HPO frequency 100% / "
            "'Obligate') -- so the modifier reflects the whole disease, not a sub-phenotype -- AND that "
            "feature is its cited dominant sequela AND the disease is non-spectrum. Each join row is "
            "re-validated against the pinned hpoa (phenotype+modifier+frequency+reference) at build time "
            "or the build fails. Every other cohort severity annotation is FEATURE-level and is declined "
            "with a per-disease reason (methodology/severity_hpo_excluded.csv) -- naive use would be a "
            "category error (e.g. Mild tall stature, Mild DMD, Severe achondroplasia). Registry [L] "
            "supersedes [H]/[O], existing [L] corroborated (max, add-only). OMIM clinical synopsis path "
            "REMOVED (API key unobtainable for an individual researcher), not deferred; no inference used."),
        "severity_inclusion_criterion": (
            "S -> [L] for a cohort disease IFF, in the pinned open HPO phenotype.hpoa, it carries a "
            "Severity-modifier annotation (HP:0012824 subtree) that is (i) OBLIGATE -- HPO frequency "
            "100% / term HP:0040280 -- on the annotated feature, (ii) on the disease's cited dominant "
            "sequela, and (iii) for a non-spectrum (non-umbrella) entity. (i) is checked programmatically "
            "against the open source at build and gate time; (ii)-(iii) are cited curatorial inputs "
            "recorded in methodology/severity_hpo_join.csv (dominant_sequela_basis) and "
            "methodology/severity_hpo_excluded.csv. A-priori, not fitted to any target order."),
        "disability_tier_cutpoints": base.get("disability_tier_cutpoints"),
        "severity_modifier_cutpoints": {"HP:0012825 Mild": 0.25, "HP:0012826 Moderate": 0.5,
                                        "HP:0012828 Severe": 0.75, "HP:0012829 Profound": 1.0,
                                        "HP:0012827 Borderline": None},
        "omim_status": base.get("omim_status"),
        "gbd_source": base.get("gbd_source"),
        "litsurvival_source": base.get("litsurvival_source"),
        "hpo_severity_source": {"file": "data/raw/hpo/phenotype.hpoa.gz", "version": HPOA_VER,
                                "sha256": hpoa_sha, "subtree": SEV_SUBTREE,
                                "retrieved": RETRIEVED, "license": "CC BY 4.0"},
        "gbd_disability_join": base.get("gbd_disability_join", []),
        "gbd_excluded": base.get("gbd_excluded", []),
        "pmc_mortality_corroborations": base.get("pmc_mortality_corroborations", []),
        "severity_hpo_join": sev_join_audit,
        "severity_hpo_excluded": sev_excluded_audit,
        "lift_counts": dict(lift),
        "axis_value_changes": [{"entity": e, "axis": a, "old": ov, "new": nv,
                                "old_grade": og, "new_grade": ng}
                               for (e, a, ov, nv, og, ng) in per_axis_changes],
        "promotions_from_not_placed": promotions,
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
            "order_locked": r["order_locked"], "orphanet": r.get("orphanet"),
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
            "order_locked", "emergence_link"]
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
                        "yes" if r.get("emergence_link") else ""])

    rj = {
        "schema": "disease_wp.burden_residual/v1",
        "phase": "R8 (open-source severity; cumulative over R5+R6+R7)",
        "derived_from": "burden_scores_registry.json (R5+R6+R7+R8) + treatments_registry.csv (R4/R5 offset)",
        "residual_rule": ("burden_score = raw_burden * (1 - e); placed = rankability cut (axes>=3) re-ranked "
                          "by residual burden_score desc, then raw_burden desc, axes desc, entity"),
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
             "burden_score", "burden_score_grade", "treatment_grade", "order_locked"]
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
                        cell(r["burden_score"]), r["burden_score_grade"], t["grade"],
                        "yes" if r["order_locked"] else "no"])

    # ----- report -----
    print("--- R8 open-source severity pass (HPO Severity-modifier dominant-sequela join) ---")
    print(f"  HPO phenotype.hpoa {HPOA_VER} sha256[:12] = {hpoa_sha[:12]}")
    print(f"  severity join: {len(sev_join_audit)} disease(s) lifted to [L]")
    print(f"  severity annotations declined (recorded): {len(sev_excluded_audit)}")
    print("\n  lift events:")
    for k in sorted(lift):
        print(f"    {k:34s} {lift[k]}")
    print("\n  S axis grade coverage AFTER R8 (over 35):")
    print(f"    S: {cov['S']}")
    if per_axis_changes:
        print("\n  axis VALUE/GRADE changes:")
        for e, a, ov, nv, og, ng in per_axis_changes:
            print(f"      {e[:38]:38s} {a}: {ov}{og} -> {nv}{ng}")
    print(f"\n  order_locked diseases (all scored axes [L]/[V], >=3 axes): {len(locked)}"
          + ("".join(f"\n      * {x['entity']} ({x['axes_scored']}/5)" for x in locked) if locked else ""))
    print("\n  sensitivity (Spearman rho of raw order vs equal-weight default):")
    for lbl, sd in sensitivity.items():
        print(f"    {lbl:24s} rho = {sd['spearman_vs_default']}")

    h = hashlib.sha256()
    for p in (OUT_SCORES_C, OUT_SCORES_J, OUT_RESID_C, OUT_RESID_J):
        h.update(open(p, "rb").read())
    print(f"\n  registry-set sha256[:12]: {h.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
