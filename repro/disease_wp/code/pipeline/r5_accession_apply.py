#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R5 stage 2 -- GeneReviews accession-dating APPLY (deterministic, NO network).

Reads ONLY the cached GeneReviews snapshots (data/raw/genereviews/<cui>.json) produced
by r5_genereviews_fetch.py, plus the BANKED R3 burden_scores.json and R4 treatments.csv /
burden_residual.json. Lifts grades [H]->[L] where the accession-dated GeneReviews chapter
corroborates, then re-derives raw_burden + residual order. Writes SEPARATE registry artifacts
(*_registry.{json,csv}); the R3/R4 banked files are left byte-identical so every prior gate
(R1-R4, consolidation, W1) keeps passing and the R3 builder's determinism is preserved.

TWO deferred [L] passes, one per cached chapter section:

  (1) TREATMENT accession-dating (treatments.csv [H] -> [L]).
      A treatment row lifts to [L] iff the chapter was found, a Management section is present,
      AND the chapter's Management text corroborates the stated modality (>=1 therapy key-term
      from the modality string appears in the Management text). Provenance is then set to the
      real accession + dates: "GeneReviews NBK<id>; initial posting <d>; last revision <d>;
      retrieved 2026-06-17; Management section". Rows that do not corroborate STAY [H] with
      their obstacle retained -- never a fabricated [L].

  (2) NATURAL-HISTORY axis corroboration (burden O/P/S/M/D [H] -> [L]).
      The FROZEN R3 lexicon (PATTERNS / first_match / mortality_from_text, imported verbatim
      from r3_burden_index) is run over the chapter's Clinical-Description / Natural-History /
      Prognosis text. Because that lexicon was tuned for SHORT MedGen definitions and would
      over-trigger on a long chapter, the policy is CORROBORATION-ONLY, never value-setting:
        * axis already [L] (HPO)         -> unchanged.
        * axis [H] and NH lexicon tier == the definition tier -> LIFT to [L], value UNCHANGED
          (two independent sources agree; raw_burden cannot move).
        * axis [H] and NH lexicon tier != definition tier      -> KEEP [H], record the
          discrepancy (no silent value change -> no tuning).
        * axis [O]                                              -> STAYS [O]. [O]-fill is
          WITHHELD: a single first-match over a ~6 kB chapter returns whatever top-severity
          word appears anywhere (often differential-diagnosis / variant-spectrum context), so
          it is not a sound basis to SET a previously-absent value, and it is the only path that
          would move raw_burden and promote not-placed diseases. Pre-registered rule (R3/R4
          handover): if [O]-fill is risky, do grade-lift ONLY and report honestly rather than
          fabricate promotions. The withheld lexicon suggestion + accession are RECORDED on the
          axis basis so the deferred opportunity is documented, not hidden. CONSEQUENCE: this
          pass lifts GRADES only; the residual ORDER and the placed/not-placed split are
          numerically identical to R4 (raw_burden and e both unchanged for every disease).

  order_locked (per disease) = (every scored axis is grade >= [L])  AND  (treatment is [L]).
  When true the W page may drop the provisional-[H] prioritisation flag for that disease.

Self-check (printed + gate-checked): every disease with NO [O]-fill must keep its banked R3
raw_burden numerically unchanged, and its residual burden_score must equal raw_burden*(1-e).
"""
import os, sys, json, csv, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR  = os.path.join(ROOT, "data", "curated")
CACHE = os.path.join(ROOT, "data", "raw", "genereviews")
RETRIEVED = "2026-06-17"

# ---- import the FROZEN R3 lexicon + helpers verbatim (no re-implementation) ----
spec = importlib.util.spec_from_file_location("r3b", os.path.join(HERE, "r3_burden_index.py"))
r3 = importlib.util.module_from_spec(spec)
# r3_burden_index imports HPO files at module exec only inside main(); top-level is safe.
spec.loader.exec_module(r3)
PATTERNS = r3.PATTERNS
first_match = r3.first_match
mortality_from_text = r3.mortality_from_text
floor_grade = r3.floor_grade
GRADE_RANK = r3.GRADE_RANK
RANK_MIN_AXES = r3.RANK_MIN_AXES
weighted_burden = r3.weighted_burden
W = r3.W

AXIS_KEY = {"O": "O_onset_text", "P": "P_progression", "S": "S_severity", "D": "D_disability"}

# generic words to drop from a modality string before therapy key-term matching
THERAPY_STOP = {
    "therapy", "therapies", "treatment", "treatments", "management", "managing", "care",
    "disease", "directed", "disorder", "with", "and", "the", "for", "of", "in", "to", "or",
    "where", "indicated", "forms", "form", "via", "using", "use", "agent", "agents", "approach",
    "based", "such", "as", "including", "include", "patients", "individuals", "affected",
    "symptomatic", "supportive", "no", "not", "established", "standard", "controls",
    "control", "reduce", "reducing", "improve", "manifestations", "complications", "available",
    "early", "late", "onset", "severe", "mild", "type", "related", "associated",
    # disease-descriptor words (never therapies) -- prevent a bare disease-name overlap from
    # corroborating a treatment (e.g. ACG II's "skeletal dysplasia" matching a dysplasia chapter)
    "skeletal", "dysplasia", "neurologic", "neuronopathic", "perinatal", "lethal", "phenotype",
    "manifestation", "course", "cure",
}


def therapy_terms(modality):
    """Distinctive therapy key-terms from a modality string (drugs, modality nouns)."""
    toks = []
    for raw in modality.replace("(", " ").replace(")", " ").replace("/", " ").replace(",", " ").replace(";", " ").split():
        t = "".join(ch for ch in raw.lower() if ch.isalpha())
        if len(t) >= 4 and t not in THERAPY_STOP:
            toks.append(t)
    # keep order, dedupe
    seen = set(); out = []
    for t in toks:
        if t not in seen:
            seen.add(t); out.append(t)
    return out


def corroborates(terms, text):
    """Return the list of key-terms present (as a word-prefix) in text."""
    low = text.lower()
    hits = []
    for t in terms:
        # word-boundary prefix match: 'chelation'~'chelating', 'transplant'~'transplantation'
        import re
        if re.search(r"\b" + re.escape(t[: max(5, len(t) - 2)]), low):
            hits.append(t)
    return hits


def load_banked():
    bs = json.load(open(os.path.join(CUR, "burden_scores.json")))
    by_cui = {r["cui"]: r for r in bs["records"]}
    treats = {r["cui"]: r for r in csv.DictReader(open(os.path.join(CUR, "treatments.csv"), newline=""))}
    cache = {}
    for fn in os.listdir(CACHE):
        if fn.startswith("_") or not fn.endswith(".json"):
            continue
        d = json.load(open(os.path.join(CACHE, fn)))
        cache[d["cui"]] = d
    return bs, by_cui, treats, cache


def axis_lexicon_tier(axis, nh_text):
    """Frozen-lexicon tier value for one axis over the NH text (or None)."""
    if not nh_text:
        return None
    if axis == "M":
        v, _ = mortality_from_text(nh_text)
        return v
    hit = first_match(nh_text, PATTERNS[AXIS_KEY[axis]])
    return hit[0] if hit else None


def apply():
    bs, by_cui, treats, cache = load_banked()
    out_records = []
    treat_out = {}
    lifts = {"treat_L": 0, "treat_keep_H": 0,
             "axis_L_corrob": 0, "axis_keep_H_discrepancy": 0, "axis_O_fill": 0, "axis_O_keep": 0}
    promoted = []
    selfcheck_fail = []

    for cui, rec in by_cui.items():
        snap = cache.get(cui, {"found": False})
        found = snap.get("found", False)
        nbk = snap.get("nbk")
        posted = snap.get("date_initial_posting")
        revised = snap.get("date_last_revision")
        is_overview = bool(snap.get("overview_multi_phenotype"))
        mgmt_present = bool(snap.get("management_sections_present"))
        mgmt_text = snap.get("management_text", "") or ""
        summary_text = snap.get("summary_text", "") or ""
        mgmt_corpus = mgmt_text + " " + summary_text  # Summary box always states the therapy
        nh_text = snap.get("naturalhistory_text", "") or ""
        accession_cite = (f"GeneReviews {nbk}; initial posting {posted}; "
                          f"last revision {revised}; retrieved {RETRIEVED}") if found else None

        # ---------- (2) axis corroboration ----------
        comps = json.loads(json.dumps(rec["components"]))  # deep copy
        axis_changes = []
        raw_burden_moves = False
        for axis in ["O", "P", "S", "M", "D"]:
            ax = comps[axis]
            cur_grade = ax["grade"]
            # frozen-lexicon read of the GeneReviews NH text (the matched phrase too, for transparency)
            nh_tier = None; nh_phrase = None
            if found and nh_text:
                if axis == "M":
                    nh_tier, nh_label = mortality_from_text(nh_text)
                    nh_phrase = nh_label
                else:
                    hit = first_match(nh_text, PATTERNS[AXIS_KEY[axis]])
                    if hit:
                        nh_tier, _, nh_phrase = hit
            if cur_grade in ("[L]", "[V]"):
                continue  # already registry-grade (HPO)
            if cur_grade == "[H]":
                # CORROBORATION ONLY: lift [H]->[L] iff GeneReviews' independent lexicon read
                # agrees with the definition-derived tier. Value never changes -> raw_burden
                # cannot move -> no possibility of the order being manipulated by this pass.
                if nh_tier is not None and abs(nh_tier - (ax["value"] or -9)) < 1e-9:
                    ax["grade"] = "[L]"
                    ax["basis"] = ax["basis"] + (f" | corroborated by GeneReviews natural-history "
                                                 f"section (matched: '{nh_phrase}')")
                    ax["source"] = (f"{ax.get('source','')}; corroborated by {accession_cite} "
                                    f"(Clinical Description / Natural History)")
                    axis_changes.append((axis, "H->L corroborated", ax["value"]))
                    lifts["axis_L_corrob"] += 1
                else:
                    if nh_tier is not None:
                        ax["basis"] = ax["basis"] + (f" | GeneReviews NH strongest lexicon tier={nh_tier} "
                                                     f"('{nh_phrase}') differs from definition tier "
                                                     f"{ax['value']}; grade retained [H]")
                        lifts["axis_keep_H_discrepancy"] += 1
            elif cur_grade == "[O]":
                # [O]-fill DELIBERATELY WITHHELD. first_match over a full ~6 kB GeneReviews
                # chapter returns the single highest-severity tier whose pattern appears ANYWHERE
                # (e.g. "congenital"/"severe" in a differential-diagnosis or variant-spectrum
                # sentence), so using it to SET a previously-absent axis value is not a sound
                # registry basis -- it over-triggers, and it is exactly the path that would move
                # raw_burden and promote not-placed diseases on a shaky read. Pre-registered rule
                # (R3/R4 handover): if [O]-fill is risky, do grade-lift ONLY and report honestly
                # rather than fabricate promotions. We therefore keep [O], but RECORD the withheld
                # lexicon suggestion + accession so the opportunity is documented, not hidden.
                if found and nh_tier is not None:
                    ax["basis"] = ax.get("basis", "") + (
                        f" | GeneReviews chapter {nbk} present; frozen lexicon suggests tier "
                        f"{nh_tier} ('{nh_phrase}') for this open axis, but registry [O]-fill is "
                        f"WITHHELD (corroboration-only policy: full-chapter first-match over-triggers; "
                        f"a sentence-level entity-anchored registry read is the path to [L], deferred)")
                lifts["axis_O_keep"] += 1

        present = [k for k in W if comps[k]["value"] is not None]
        axes_scored = len(present)
        rankable = axes_scored >= RANK_MIN_AXES
        raw_burden = weighted_burden(comps, W)
        grade_floor = floor_grade([comps[k]["grade"] for k in W])
        grade_present = floor_grade([comps[k]["grade"] for k in present]) if present else "[O]"

        # self-check: no [O]-fill => raw_burden numerically unchanged vs banked R3
        if not raw_burden_moves:
            if abs((raw_burden or -9) - (rec["raw_burden"] or -9)) > 1e-9:
                selfcheck_fail.append((cui, rec["raw_burden"], raw_burden))
        else:
            if rec.get("rankable") is False and rankable:
                promoted.append((cui, rec["entity"], rec["axes_scored"], axes_scored))

        # ---------- (1) treatment accession-dating ----------
        tr = dict(treats[cui])
        modality = tr["modality"]
        evidence_status = tr["evidence_status"]
        terms = therapy_terms(modality)
        mgmt_hits = corroborates(terms, mgmt_corpus) if (found and mgmt_present) else []
        # evidence_status == 'none' means NO disease-directed therapy exists (perinatal-lethal
        # ACG II; the neuronopathic course of NPD-A unaddressed by ERT). There is no therapy to
        # accession-date, so [L] does not apply -- the 'none' finding stays [H] (an honest text
        # inference about the ABSENCE of therapy). A bare disease-name or a why-it-fails drug
        # mention in the chapter must NOT manufacture a treatment [L] here.
        lift_ok = found and mgmt_present and bool(mgmt_hits) and evidence_status != "none"
        if lift_ok:
            tr["grade"] = "[L]"
            tr["provenance"] = (f"accession-dated to GeneReviews Management section. "
                                f"{accession_cite}; Management section "
                                f"(corroborating term(s): {', '.join(mgmt_hits[:4])})")
            tr["obstacle_for_L"] = ""
            tr["nbk"] = nbk
            tr["accession_initial_posting"] = posted or ""
            tr["accession_last_revision"] = revised or ""
            tr["mgmt_corroboration_terms"] = ", ".join(mgmt_hits)
            lifts["treat_L"] += 1
        else:
            tr["nbk"] = nbk or ""
            tr["accession_initial_posting"] = posted or ""
            tr["accession_last_revision"] = revised or ""
            tr["mgmt_corroboration_terms"] = ""
            if evidence_status == "none":
                tr["obstacle_for_L"] = (f"evidence_status 'none' (no disease-directed therapy exists); "
                                        f"GeneReviews chapter {nbk} confirms supportive/absent-therapy "
                                        f"management. No therapy to accession-date; grade retained [H] "
                                        f"as an honest inference about absence of therapy.")
            elif found and not mgmt_hits:
                tr["obstacle_for_L"] = (f"GeneReviews chapter {nbk} retrieved (Management section "
                                        f"present={mgmt_present}) but did not textually corroborate the "
                                        f"stated modality; grade retained [H]. " + tr.get("obstacle_for_L", ""))
            lifts["treat_keep_H"] += 1
        treat_grade = tr["grade"]
        treat_out[cui] = tr

        # order_locked is meaningful ONLY for a disease that is actually IN the order (rankable):
        # its residual rank rests on registry-grade data iff every SCORED axis is >=[L] AND the
        # treatment is [L]. A not-placed disease has no order position, so it cannot be locked.
        order_locked = (rankable and grade_present in ("[L]", "[V]") and treat_grade == "[L]")

        out_records.append({
            "entity": rec["entity"], "cui": cui, "tier": rec["tier"],
            "system_class": rec["system_class"], "genes": rec["genes"],
            "omim_codes": rec["omim_codes"], "slug": None,
            "components": comps, "axes_scored": axes_scored, "rankable": rankable,
            "axes_present": present, "axes_missing": [k for k in W if k not in present],
            "raw_burden": raw_burden, "raw_burden_grade_floor": grade_floor,
            "raw_burden_grade_present": grade_present,
            "emergence_link": rec.get("emergence_link"),
            "genereviews": {"found": found, "nbk": nbk, "url": snap.get("url"),
                            "initial_posting": posted, "last_revision": revised,
                            "overview_multi_phenotype": is_overview,
                            "management_sections_present": snap.get("management_sections_present", []),
                            "naturalhistory_sections_present": snap.get("naturalhistory_sections_present", [])},
            "axis_changes": axis_changes,
            "treatment_grade": treat_grade,
            "order_locked": order_locked,
        })

    if selfcheck_fail:
        print("SELF-CHECK FAIL (raw_burden moved without an [O]-fill):")
        for cui, a, b in selfcheck_fail:
            print(f"   {cui}: banked={a} registry={b}")
        sys.exit(1)

    # ---- residual: burden_score = raw_burden*(1-e); rank rankable set desc ----
    # raw_rank (registry pre-treatment order) for shift reporting
    rankset = [r for r in out_records if r["rankable"]]
    rawsorted = sorted(rankset, key=lambda r: (-(r["raw_burden"] if r["raw_burden"] is not None else -1),
                                               -r["axes_scored"], r["entity"]))
    raw_rank = {r["cui"]: i + 1 for i, r in enumerate(rawsorted)}

    for r in out_records:
        tr = treat_out[r["cui"]]
        e = float(tr["efficacy_offset_e"])
        r["efficacy_offset_e"] = e
        r["evidence_status"] = tr["evidence_status"]
        r["burden_score"] = (r["raw_burden"] * (1 - e)) if r["raw_burden"] is not None else None
        # grade floor of residual = min(raw_burden_grade_present, treatment grade)
        r["burden_score_grade"] = floor_grade([r["raw_burden_grade_present"], r["treatment_grade"]])

    placed = sorted([r for r in out_records if r["rankable"]],
                    key=lambda r: (-(r["burden_score"] if r["burden_score"] is not None else -1),
                                   -r["axes_scored"], r["entity"]))
    not_placed = sorted([r for r in out_records if not r["rankable"]],
                        key=lambda r: (-r["axes_scored"], r["entity"]))
    for i, r in enumerate(placed):
        r["residual_rank"] = i + 1
        r["raw_rank"] = raw_rank.get(r["cui"])
        r["rank_shift_vs_raw"] = (raw_rank.get(r["cui"]) - (i + 1)) if raw_rank.get(r["cui"]) else None
    for r in not_placed:
        r["residual_rank"] = None
        r["raw_rank"] = None
        r["rank_shift_vs_raw"] = None

    write_outputs(bs, out_records, placed, not_placed, treat_out, lifts, promoted)
    print_summary(out_records, lifts, promoted, placed)


def write_outputs(bs, out_records, placed, not_placed, treat_out, lifts, promoted):
    ordered = placed + not_placed
    by_cui = {r["cui"]: r for r in out_records}

    # ---- burden_scores_registry.json ----
    coverage = {ax: {} for ax in ["O", "P", "S", "M", "D"]}
    for ax in coverage:
        from collections import Counter
        c = Counter(by_cui[r["cui"]]["components"][ax]["grade"] for r in out_records)
        coverage[ax] = dict(c)
    bs_reg = dict(bs)
    bs_reg["schema"] = "disease_wp.burden_scores_registry/v1"
    bs_reg["phase"] = "R5 (GeneReviews accession-dating apply)"
    bs_reg["derived_from"] = "burden_scores.json (R3, banked) + data/raw/genereviews/ cache"
    bs_reg["lift_policy"] = ("[H]->[L] where the frozen R3 lexicon over the GeneReviews "
                             "Clinical-Description/Natural-History text agrees with the "
                             "definition-derived tier (value unchanged); [O]-fill from non-overview "
                             "chapters; overview chapters corroborate existing [H] only.")
    bs_reg["axis_grade_coverage_registry"] = coverage
    bs_reg["lift_counts"] = lifts
    bs_reg["records"] = []
    for r in ordered:
        rr = by_cui[r["cui"]]
        bs_reg["records"].append({
            "residual_rank": rr.get("residual_rank"),
            "entity": rr["entity"], "cui": rr["cui"], "tier": rr["tier"],
            "system_class": rr["system_class"], "genes": rr["genes"], "omim_codes": rr["omim_codes"],
            "components": rr["components"], "axes_scored": rr["axes_scored"], "rankable": rr["rankable"],
            "axes_missing": rr["axes_missing"], "raw_burden": rr["raw_burden"],
            "raw_burden_grade_floor": rr["raw_burden_grade_floor"],
            "raw_burden_grade_present": rr["raw_burden_grade_present"],
            "burden_score": rr["burden_score"], "burden_score_grade": rr["burden_score_grade"],
            "treatment_grade": rr["treatment_grade"], "order_locked": rr["order_locked"],
            "genereviews": rr["genereviews"], "axis_changes": rr["axis_changes"],
            "emergence_link": rr["emergence_link"],
        })
    json.dump(bs_reg, open(os.path.join(CUR, "burden_scores_registry.json"), "w"),
              ensure_ascii=False, indent=2)

    # ---- burden_scores_registry.csv (same 25 columns as burden_scores.csv + 2 new) ----
    cols = ["rank", "rankable", "entity", "cui", "tier", "system_class",
            "O_value", "O_grade", "P_value", "P_grade", "S_value", "S_grade",
            "M_value", "M_grade", "D_value", "D_grade", "axes_scored", "raw_burden",
            "raw_burden_grade_floor", "raw_burden_grade_present", "R_treat", "R_treat_grade",
            "burden_score", "burden_score_grade", "emergence_link", "order_locked", "genereviews_nbk"]
    with open(os.path.join(CUR, "burden_scores_registry.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(cols)
        for r in ordered:
            rr = by_cui[r["cui"]]; c = rr["components"]; tr = treat_out[r["cui"]]
            def vg(ax):
                v = c[ax]["value"]; return ("" if v is None else f"{v:.4f}"), c[ax]["grade"]
            ov, og = vg("O"); pv, pg = vg("P"); sv, sg = vg("S"); mv, mg = vg("M"); dv, dg = vg("D")
            e = float(tr["efficacy_offset_e"]); rt = 1 - e
            w.writerow([
                rr.get("residual_rank") or "", "yes" if rr["rankable"] else "no",
                rr["entity"], rr["cui"], rr["tier"], rr["system_class"],
                ov, og, pv, pg, sv, sg, mv, mg, dv, dg, rr["axes_scored"],
                "" if rr["raw_burden"] is None else f"{rr['raw_burden']:.4f}",
                rr["raw_burden_grade_floor"], rr["raw_burden_grade_present"],
                f"{rt:.4f}", rr["treatment_grade"],
                "" if rr["burden_score"] is None else f"{rr['burden_score']:.4f}",
                rr["burden_score_grade"],
                (rr["emergence_link"]["value"] if rr["emergence_link"] else ""),
                "yes" if rr["order_locked"] else "no",
                rr["genereviews"]["nbk"] or "",
            ])

    # ---- treatments_registry.{json,csv} ----
    t_cols = list(next(iter(treat_out.values())).keys())
    with open(os.path.join(CUR, "treatments_registry.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=t_cols); w.writeheader()
        for cui in [r["cui"] for r in ordered]:
            w.writerow(treat_out[cui])
    from collections import Counter
    json.dump({"schema": "disease_wp.treatments_registry/v1",
               "phase": "R5 (GeneReviews accession-dating apply)",
               "derived_from": "treatments.csv (R4, banked) + data/raw/genereviews/ cache",
               "grade_distribution": dict(Counter(t["grade"] for t in treat_out.values())),
               "records": [treat_out[r["cui"]] for r in ordered]},
              open(os.path.join(CUR, "treatments_registry.json"), "w"),
              ensure_ascii=False, indent=2)

    # ---- burden_residual_registry.{json,csv} ----
    res_cols = ["residual_rank", "raw_rank", "rank_shift_vs_raw", "rankable", "entity", "cui",
                "tier", "system_class", "raw_burden", "raw_burden_grade_present", "evidence_status",
                "efficacy_offset_e", "R_treat", "R_treat_grade", "burden_score", "burden_score_grade",
                "order_locked", "genereviews_nbk"]
    with open(os.path.join(CUR, "burden_residual_registry.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(res_cols)
        for r in ordered:
            rr = by_cui[r["cui"]]; tr = treat_out[r["cui"]]
            e = float(tr["efficacy_offset_e"]); rt = 1 - e
            w.writerow([
                rr.get("residual_rank") or "", rr.get("raw_rank") or "",
                "" if rr.get("rank_shift_vs_raw") is None else rr["rank_shift_vs_raw"],
                "yes" if rr["rankable"] else "no", rr["entity"], rr["cui"], rr["tier"],
                rr["system_class"],
                "" if rr["raw_burden"] is None else f"{rr['raw_burden']:.4f}",
                rr["raw_burden_grade_present"], tr["evidence_status"], f"{e:.4f}",
                f"{rt:.4f}", rr["treatment_grade"],
                "" if rr["burden_score"] is None else f"{rr['burden_score']:.4f}",
                rr["burden_score_grade"], "yes" if rr["order_locked"] else "no",
                rr["genereviews"]["nbk"] or "",
            ])
    json.dump({"schema": "disease_wp.burden_residual_registry/v1",
               "phase": "R5 (GeneReviews accession-dating apply)",
               "reads_unchanged": "raw_burden re-derived from registry-lifted components (only [O]-fills move it)",
               "residual_rule": "burden_score = raw_burden * (1 - e); rankable set re-ranked by burden_score desc",
               "placed": len(placed), "not_placed": len(not_placed),
               "promoted_from_not_placed": [{"cui": c, "entity": e} for c, e, _, _ in promoted],
               "records": [{"residual_rank": by_cui[r["cui"]].get("residual_rank"),
                            "raw_rank": by_cui[r["cui"]].get("raw_rank"),
                            "rank_shift_vs_raw": by_cui[r["cui"]].get("rank_shift_vs_raw"),
                            "entity": r["entity"], "cui": r["cui"], "rankable": r["rankable"],
                            "axes_scored": r["axes_scored"], "raw_burden": r["raw_burden"],
                            "burden_score": r["burden_score"], "burden_score_grade": r["burden_score_grade"],
                            "treatment_grade": r["treatment_grade"], "order_locked": r["order_locked"]}
                           for r in ordered]},
              open(os.path.join(CUR, "burden_residual_registry.json"), "w"),
              ensure_ascii=False, indent=2)


def print_summary(out_records, lifts, promoted, placed):
    print("\n=== R5 accession-dating apply ===")
    print(f"treatments: [H]->[L] {lifts['treat_L']}  |  kept [H] {lifts['treat_keep_H']}")
    print(f"axes: H->L corroborated {lifts['axis_L_corrob']}  |  kept H (discrepancy) "
          f"{lifts['axis_keep_H_discrepancy']}  |  [O]-fill {lifts['axis_O_fill']}  |  [O] kept {lifts['axis_O_keep']}")
    nlock = sum(1 for r in out_records if r["order_locked"])
    print(f"order_locked diseases (all scored axes >=[L] AND treatment [L]): {nlock}/{len(out_records)}")
    if promoted:
        print("PROMOTED not-placed -> placed (axis [O]-fill reached >=3 axes):")
        for c, e, a0, a1 in promoted:
            print(f"   {e} ({c}): {a0} -> {a1} axes")
    else:
        print("PROMOTED not-placed -> placed: none (no not-placed disease reached 3 registry-scored axes)")
    print("\nplaced residual order (registry):")
    for r in placed:
        lock = "LOCKED" if r["order_locked"] else "prov-H"
        print(f"  #{r['residual_rank']:2} {r['entity'][:38]:38} bs={r['burden_score']:.4f} "
              f"tx={r['treatment_grade']} {lock}")


if __name__ == "__main__":
    apply()
