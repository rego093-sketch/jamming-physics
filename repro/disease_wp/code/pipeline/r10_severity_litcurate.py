#!/usr/bin/env python3
# =============================================================================
# R10 - curated SEVERITY / PROGRESSION literature pass, ROUND 2
#        (cumulative over R5..R9)
# -----------------------------------------------------------------------------
# R9 lifted S/P for the cohort diseases whose dominant untreated sequela had a
# citeable DISEASE-LEVEL magnitude in a PMC open-access source, recorded every
# declined statement, and left the asymmetric discipline in place: lift only
# where defensible, decline transparently, never fish for an order-lock.
# R10 is a SECOND curation round over the SAME a-priori inclusion criterion and
# the SAME FROZEN R3 tier function -- it does NOT touch R9's recorded artifacts
# (methodology/severity_litcurate_join.csv, *_excluded.csv) or R9's recorded
# registry-set sha; it adds a fresh, separately-auditable join/excluded set
# (methodology/severity_litcurate2_join.csv, *_excluded.csv) on top of the R9
# registry, exactly as R7 was a separate cumulative stage over R6.
#
# THE INCLUSION CRITERION IS UNCHANGED (declared, not fitted):
#   A disease's S or P lifts to registry-grade [L] IFF a cited PMC OPEN-ACCESS
#   source states a DISEASE-LEVEL magnitude for its DOMINANT untreated sequela
#   (not a sub-phenotype, not a treated cohort, not spectrum/continuum language,
#   not a comparative reference to other forms), and the FROZEN R3 tier function
#   applied to the verbatim cited sentence yields the declared tier. The tier is
#   DERIVED (imported r3.first_match over PATTERNS['P_progression']/['S_severity'];
#   no new cut-points), the sentence is re-found verbatim in the pinned OA cache
#   at build time or the build fails, and the R3 spectrum override is enforced.
#   All of derive_tier / is_spectrum / the cut-point tables / the decline
#   vocabulary are IMPORTED from r9_severity_litcurate so they cannot drift.
#
# add-only: registry [L] supersedes [H]/[O]; an existing [L] is corroborated
#   (max). A missing/declined source NEVER downgrades a value. R10 touches ONLY
#   S and P; O/M/D stay byte-identical to R9.
#
# Self-healing / idempotent: if its own pass-tag is already present, R10 re-runs
# r5..r9 to rebuild a clean R9 base, then re-applies. Writes the payload back to
# burden_scores_registry.json (+ burden_residual_registry.{json,csv}) and prints
# the registry-set sha256[:12] over the four emitted artifacts.
# The R10 pipeline is LIVING CODE and is intentionally NOT in MANIFEST_governed.
# =============================================================================
import os, csv, json, copy, hashlib, importlib.util, collections, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
LITC = os.path.join(ROOT, "data", "raw", "litcurate")
RETRIEVED = "2026-06-18"

OUT_SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
OUT_SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
OUT_RESID_J = os.path.join(CUR, "burden_residual_registry.json")
OUT_RESID_C = os.path.join(CUR, "burden_residual_registry.csv")

# ---- import R9's PURE helpers so the frozen tier / spectrum / decline logic
#      is literally the same object (cannot drift); r9.main is __main__-guarded ----
_s9 = importlib.util.spec_from_file_location("r9_litc", os.path.join(HERE, "r9_severity_litcurate.py"))
r9 = importlib.util.module_from_spec(_s9); _s9.loader.exec_module(r9)
W = r9.W
GRADE_RANK = r9.GRADE_RANK
floor_grade = r9.floor_grade
weighted_burden = r9.weighted_burden
spearman = r9.spearman
RANK_MIN = r9.RANK_MIN
AXIS_PATTERN = r9.AXIS_PATTERN
P_CUTPOINTS = r9.P_CUTPOINTS
S_CUTPOINTS = r9.S_CUTPOINTS
DECLINE_VOCAB = r9.DECLINE_VOCAB
LIT_SRC_TMPL = r9.LIT_SRC_TMPL
derive_tier = r9.derive_tier          # frozen R3 first_match + spectrum guard
load_pinned = r9.load_pinned          # verifies pinned OA cache + its own sha
_append_once = r9._append_once


def load_join2():
    p = os.path.join(METH, "severity_litcurate2_join.csv")
    if not os.path.exists(p):
        return []
    with open(p, newline="") as fh:
        return list(csv.DictReader(fh))


def load_excluded2():
    p = os.path.join(METH, "severity_litcurate2_excluded.csv")
    if not os.path.exists(p):
        return collections.defaultdict(list)
    rows = collections.defaultdict(list)
    with open(p, newline="") as fh:
        for r in csv.DictReader(fh):
            rows[r["cui"]].append(r)
    return rows


def main():
    join = load_join2()
    excluded = load_excluded2()

    base = json.load(open(OUT_SCORES_J))
    # self-healing: if R10 already applied, rebuild a clean R9 base from r5..r9
    if "R10_litcurate2" in base.get("registry_passes", []):
        for stage in ("r5_accession_apply.py", "r6_naturalhistory_registry.py",
                      "r7_naturalhistory_registry2.py", "r8_severity_registry.py",
                      "r9_severity_litcurate.py"):
            subprocess.run([sys.executable, os.path.join(HERE, stage)],
                           check=True, stdout=subprocess.DEVNULL)
        base = json.load(open(OUT_SCORES_J))
    if "R9_litcurate_severity_progression" not in base.get("registry_passes", []):
        print("  ERROR: R10 expects an R9 base (registry_passes missing "
              "R9_litcurate_severity_progression)", file=sys.stderr)
        sys.exit(3)

    recs = copy.deepcopy(base["records"])
    rec_by_cui = {r["cui"]: r for r in recs}

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = {"e": float(r["efficacy_offset_e"]), "R_treat": float(r["R_treat"]),
                               "grade": r["grade"], "evidence_status": r["evidence_status"]}

    lift = collections.Counter()
    promotions, locked, per_axis_changes = [], [], []
    join_audit, excluded_audit = [], []

    # ---------------- LIFTS (curation join, round 2) ----------------
    for jr in join:
        cui, axis, entity = jr["cui"], jr["axis"], jr["entity"]
        if cui not in rec_by_cui:
            print(f"  ERROR: join cui {cui} ({entity}) not in cohort", file=sys.stderr); sys.exit(4)
        if axis not in AXIS_PATTERN:
            print(f"  ERROR: join axis {axis!r} for {entity} not S/P", file=sys.stderr); sys.exit(4)
        art = load_pinned(jr["pmcid"])
        if not art.get("open_access"):
            print(f"  ERROR: cited source {jr['pmcid']} for {entity} is not open-access", file=sys.stderr); sys.exit(4)
        sentence = jr["exact_sentence"]
        if sentence not in art["text"]:
            print(f"  ERROR: curated sentence for {entity} NOT re-found verbatim in pinned {jr['pmcid']}",
                  file=sys.stderr); sys.exit(4)
        tier_val, tier_label, tier_phrase = derive_tier(axis, sentence, entity)
        if abs(float(jr["tier"]) - tier_val) > 1e-9:
            print(f"  ERROR: declared tier {jr['tier']} for {entity} ({axis}) != frozen-R3-derived {tier_val}",
                  file=sys.stderr); sys.exit(4)
        if not (jr.get("dominant_sequela_basis") or "").strip():
            print(f"  ERROR: {entity} join row missing dominant_sequela_basis", file=sys.stderr); sys.exit(4)

        ax = rec_by_cui[cui]["components"][axis]
        old_v, old_g = ax["value"], ax["grade"]
        sha = art["text_sha256"][:12]
        cite = (LIT_SRC_TMPL.format(pmcid=jr["pmcid"], pmid=jr["pmid"], sha=sha, ret=RETRIEVED,
                                    axis_fn=AXIS_PATTERN[axis])
                + f" -> tier {tier_val:.2f} ({tier_label}); curated sentence: \"{sentence}\"; "
                + f"dominant-sequela basis: {jr['dominant_sequela_basis']}")
        join_audit.append({"entity": entity, "cui": cui, "axis": axis, "pmcid": jr["pmcid"],
                           "pmid": jr["pmid"], "tier": tier_val, "tier_label": tier_label,
                           "exact_sentence": sentence, "prior_value": old_v, "prior_grade": old_g,
                           "open_access": True})

        if old_g == "[L]" and old_v is not None:
            new_v = max(old_v, tier_val)
            tag = "corroborated" if new_v == old_v else "raised"
            ax["value"] = new_v; ax["grade"] = "[L]"
            ax["basis"] = _append_once(ax.get("basis", ""), f"curated literature {tier_label} {tag}")
            ax["source"] = _append_once(ax.get("source", ""), cite, sep=" + ")
            lift[f"{axis}_L_corroborated" if new_v == old_v else f"{axis}_L_raised"] += 1
            if new_v != old_v:
                per_axis_changes.append((entity, axis, old_v, new_v, old_g, "[L]"))
        else:
            ax["value"] = tier_val; ax["grade"] = "[L]"
            ax["basis"] = f"curated literature: {tier_label} (frozen R3 {AXIS_PATTERN[axis]} tier {tier_val:.2f})"
            ax.pop("obstacle", None); ax["source"] = cite
            lift[f"{axis}_H_to_L" if old_g == "[H]" else f"{axis}_O_to_L"] += 1
            per_axis_changes.append((entity, axis, old_v, tier_val, old_g, "[L]"))

    # ---------------- DECLINES (recorded, never lifted) ----------------
    for cui, rows in excluded.items():
        if cui not in rec_by_cui:
            print(f"  ERROR: excluded cui {cui} not in cohort", file=sys.stderr); sys.exit(4)
        for x in rows:
            axis = x["axis"]
            art = load_pinned(x["considered_pmcid"])
            if x["considered_statement"] not in art["text"]:
                print(f"  ERROR: considered statement for {x['entity']} ({axis}) NOT in pinned "
                      f"{x['considered_pmcid']}", file=sys.stderr); sys.exit(4)
            if x.get("decline_class") not in DECLINE_VOCAB:
                print(f"  ERROR: decline_class {x.get('decline_class')!r} for {x['entity']} not in vocabulary",
                      file=sys.stderr); sys.exit(4)
            if not (x.get("exclusion_reason") or "").strip():
                print(f"  ERROR: {x['entity']} decline missing exclusion_reason", file=sys.stderr); sys.exit(4)
            ax = rec_by_cui[cui]["components"][axis]
            note = (f"curated-literature {axis}-magnitude statement (round 2) considered and declined "
                    f"({x['decline_class']}): {x['exclusion_reason']} "
                    f"[{x['considered_pmcid']} PMID:{x['considered_pmid']}]")
            if ax["grade"] == "[O]":
                ax["obstacle"] = _append_once(ax.get("obstacle", ""), note)
            else:
                ax.setdefault("litcurate_note", "")
                ax["litcurate_note"] = _append_once(ax["litcurate_note"], note)
            excluded_audit.append({"entity": x["entity"], "cui": cui, "axis": axis,
                                   "considered_pmcid": x["considered_pmcid"], "considered_pmid": x["considered_pmid"],
                                   "decline_class": x["decline_class"], "considered_statement": x["considered_statement"],
                                   "exclusion_reason": x["exclusion_reason"]})
            lift[f"{axis}_excluded_recorded"] += 1

    # ---------------- recompute composite / coverage / rankability (identical to R8/R9) ----------------
    for r in recs:
        comp = r["components"]
        present = [k for k in W if comp[k]["value"] is not None]
        r["axes_scored"] = len(present)
        r["axes_missing"] = [k for k in W if k not in present]
        r["rankable"] = len(present) >= RANK_MIN
        r["raw_burden"] = weighted_burden(comp, W)
        r["raw_burden_grade_floor"] = floor_grade([comp[k]["grade"] for k in W])
        r["raw_burden_grade_present"] = floor_grade([comp[k]["grade"] for k in present]) if present else "[O]"

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
        "phase": "R10 (curated severity/progression literature, round 2; cumulative over R5+R6+R7+R8+R9)",
        "investigation_only": base.get("investigation_only", True),
        "generated": RETRIEVED,
        "method": (base.get("method", "")
                   + " + curated PMC-OA severity/progression literature join, round 2 (R10)"),
        "derived_from": ("burden_scores_registry.json (R5..R9) + data/raw/litcurate/ (PMC-OA, pinned) + "
                         "methodology/severity_litcurate2_join.csv + methodology/severity_litcurate2_excluded.csv"),
        "registry_passes": list(base.get("registry_passes", [])) + ["R10_litcurate2"],
        "weights_default": W,
        "composite_rule": base.get("composite_rule"),
        "floor_rule": base.get("floor_rule"),
        "ranking_basis": base.get("ranking_basis"),
        "rankability": base.get("rankability"),
        "cohort_size": len(ordered),
        "lift_policy": (
            base.get("lift_policy", "") + "  ||  R10: SECOND curated PMC OPEN-ACCESS S/P round over the SAME "
            "a-priori inclusion criterion and the SAME frozen R3 tier function as R9, applied through a fresh, "
            "separately-auditable curation join (methodology/severity_litcurate2_join.csv) plus a recorded decline "
            "set (methodology/severity_litcurate2_excluded.csv). R10 does NOT modify R9's recorded join/excluded "
            "CSVs or R9's recorded registry-set sha; it is a separate cumulative stage over the R9 registry, exactly "
            "as R7 was a separate cumulative stage over R6. derive_tier / is_spectrum / the cut-point tables / the "
            "decline vocabulary are IMPORTED from r9_severity_litcurate so they cannot drift. Registry [L] supersedes "
            "[H]/[O], existing [L] corroborated (max, add-only). No inference; no new cut-points."),
        "disability_tier_cutpoints": base.get("disability_tier_cutpoints"),
        "severity_modifier_cutpoints": base.get("severity_modifier_cutpoints"),
        "litcurate_progression_cutpoints": P_CUTPOINTS,
        "litcurate_severity_cutpoints": S_CUTPOINTS,
        "litcurate_inclusion_criterion": base.get("litcurate_inclusion_criterion"),
        "omim_status": base.get("omim_status"),
        "gbd_source": base.get("gbd_source"),
        "litsurvival_source": base.get("litsurvival_source"),
        "hpo_severity_source": base.get("hpo_severity_source"),
        "litcurate_source": base.get("litcurate_source"),
        "litcurate2_source": {"dir": "data/raw/litcurate/", "class": "PubMed Central open-access full text",
                              "retrieved": RETRIEVED,
                              "cited_articles": sorted({a["pmcid"] for a in join_audit}
                                                       | {e["considered_pmcid"] for e in excluded_audit})},
        "gbd_disability_join": base.get("gbd_disability_join", []),
        "gbd_excluded": base.get("gbd_excluded", []),
        "pmc_mortality_corroborations": base.get("pmc_mortality_corroborations", []),
        "severity_hpo_join": base.get("severity_hpo_join", []),
        "severity_hpo_excluded": base.get("severity_hpo_excluded", []),
        "litcurate_join": base.get("litcurate_join", []),
        "litcurate_excluded": base.get("litcurate_excluded", []),
        "litcurate2_join": join_audit,
        "litcurate2_excluded": excluded_audit,
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
            axc = r["components"]
            def cell(v):
                return "" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)
            w.writerow([cell(r["rank"]), "yes" if r["rankable"] else "no", r["entity"], r["cui"],
                        r["tier"], r["system_class"],
                        cell(axc["O"]["value"]), axc["O"]["grade"], cell(axc["P"]["value"]), axc["P"]["grade"],
                        cell(axc["S"]["value"]), axc["S"]["grade"], cell(axc["M"]["value"]), axc["M"]["grade"],
                        cell(axc["D"]["value"]), axc["D"]["grade"],
                        r["axes_scored"], cell(r["raw_burden"]),
                        r["raw_burden_grade_floor"], r["raw_burden_grade_present"],
                        cell(r["treatability"]["value"]), r["treatability"]["grade"],
                        cell(r["burden_score"]), r["burden_score_grade"],
                        "yes" if r["order_locked"] else "no",
                        "yes" if r.get("emergence_link") else ""])

    rj = {
        "schema": "disease_wp.burden_residual/v1",
        "phase": "R10 (curated severity/progression literature, round 2; cumulative over R5..R9)",
        "derived_from": "burden_scores_registry.json (R5..R10) + treatments_registry.csv (R4/R5 offset)",
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
    print("--- R10 curated severity/progression literature pass, ROUND 2 (PMC-OA dominant-sequela join) ---")
    print(f"  curation lifts:  {len(join_audit)}   declines recorded: {len(excluded_audit)}")
    print("\n  lift events:")
    for k in sorted(lift):
        print(f"    {k:34s} {lift[k]}")
    print("\n  S/P axis grade coverage AFTER R10 (over 35):")
    print(f"    S: {cov['S']}")
    print(f"    P: {cov['P']}")
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
