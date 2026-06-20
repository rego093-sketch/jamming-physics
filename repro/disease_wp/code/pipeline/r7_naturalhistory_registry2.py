#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R7 stage 2 -- open-source natural-history registry pass (GBD disability weights +
PMC published survival), applied to the burden axes. Cumulative over R5 + R6.

The R6 limitation named two still-open axes with no structured registry source:
DISABILITY magnitude (D) and SEVERITY magnitude (S). R7 closes the open *disability*
axis from the canonical, openly published GBD disability-weights table, and attempts
the open *mortality* path (PMC survival literature). It is the credential-free
counterpart to the OMIM clinical-synopsis pass (which is skipped without a key).

No network: reads the R7 fetch caches (each sha-pinned) and the R6 registry layer.
Imports the FROZEN R3 builder via importlib (tier maps, composite, sensitivity), so
the scoring rules cannot drift from R3.

DECLARED, A-PRIORI RULES (no tuning; recorded in the output + methodology):

 DISABILITY (D) <- GBD 2013 disability weight of the disease's single dominant
   untreated-natural-history functional sequela, via the CITED curation join
   (methodology/gbd_dw_join.csv: one disease -> one named GBD health state, each
   row carrying the clinical evidence basis). The published dw (a [V]-quality
   quantitative value) is binned to the fixed BURDEN_INDEX disability tier by
   cut-points declared a priori:
        dw < 0.10        -> 0.2  (independent)
        0.10 <= dw < 0.30-> 0.5  (partial support)
        0.30 <= dw <= 0.55-> 0.75 (high support)
        dw > 0.55        -> 1.0  (fully dependent)
   GRADE = [L] (not [V]): the dw itself is [V]-grade, but binding a disease to a
   GBD health state is a CURATION join, not a disease-specific measured
   distribution -- the same conservative call R6 made for onset. The raw dw + 95%
   UI are recorded in the basis for provenance. The join is validated at runtime
   against the pinned DW table (a state/weight not reproducible from the pin is a
   hard error). A disease is mapped ONLY when one dominant sequela maps cleanly;
   multi-domain / variable / mortality-dominant diseases are NOT mapped
   (methodology/gbd_dw_excluded.csv records each such decision) and D stays at its
   banked grade -- never guessed.
   Registry [L] SUPERSEDES a prior [H]/[O] D (the definition tier was an a-priori
   guess; the GBD-anchored value is the cited registry value). An existing [L] D is
   CORROBORATED (add-only; value = max, never downgraded).

 MORTALITY (M) <- PMC open-access survival literature, CORROBORATION ONLY. For a
   disease whose entity-verified OA article (r7_litsurvival_fetch.py cache) contains
   a sentence with a QUANTITATIVE survival / age-of-death / explicit-lifespan figure
   whose direction AGREES with the banked M tier band, the published citation (PMCID
   + exact sentence) is added to the M source and an [H] M is promoted to [L]. Model-
   based / treated-cohort / sub-group / comparison-artifact sentences are EXCLUDED by
   a fixed filter (assumption, model, QALY, hazard ratio, transplant, operative,
   interquartile, recipients, follow-up, surgical...). Free text does NOT fill an [O]
   M axis (the over-trigger R5 withheld for); an unmatched [O] M stays open with the
   obstacle recorded. M values are never changed (add-only/no-downgrade).

 SEVERITY (S) / PROGRESSION (P): no structured open source. OMIM clinical synopsis
   (the intended S source) is skipped without a key, and typical-course adjectives are
   too context-dependent to extract safely from free text. S/P are NOT lifted here;
   the obstacle is recorded on each open axis, never guessed.

 ADD-ONLY / ABSENCE-SAFE -- a missing GBD mapping or PMC sentence never downgrades a
   banked value.

The registry layer is CUMULATIVE: R5 + R6 + R7. This stage OVERWRITES the *_registry
artifacts; the R3/R4 BANKED files stay byte-identical (gate-verified). It is self-
healing/idempotent: if the on-disk base already carries R7, the clean r5->r6 base is
regenerated first.

Out (overwrite): data/curated/burden_scores_registry.{json,csv}
                 data/curated/burden_residual_registry.{json,csv}
"""
import os, re, csv, json, copy, hashlib, importlib.util, collections, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
GBD = os.path.join(ROOT, "data", "raw", "gbd")
LITS = os.path.join(ROOT, "data", "raw", "litsurvival")
OMIM = os.path.join(ROOT, "data", "raw", "omim")
RETRIEVED = "2026-06-18"

OUT_SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
OUT_SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
OUT_RESID_J = os.path.join(CUR, "burden_residual_registry.json")
OUT_RESID_C = os.path.join(CUR, "burden_residual_registry.csv")

# frozen R3 import
_spec = importlib.util.spec_from_file_location("r3b", os.path.join(HERE, "r3_burden_index.py"))
r3 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(r3)
W = r3.W
GRADE_RANK = r3.GRADE_RANK
floor_grade = r3.floor_grade
weighted_burden = r3.weighted_burden
spearman = r3.spearman
RANK_MIN = r3.RANK_MIN_AXES

GBD_SRC = ("Salomon JA, Haagsma JA, Davis A, et al. Disability weights for the Global Burden "
           "of Disease 2013 study. Lancet Glob Health 2015;3(11):e712-23 (GBD 2013 estimate); "
           "open access (CC BY), retrieved " + RETRIEVED)

# a-priori dw -> disability tier cut-points (declared; not fitted)
def dw_to_tier(dw):
    if dw < 0.10:
        return 0.2
    if dw < 0.30:
        return 0.5
    if dw <= 0.55:
        return 0.75
    return 1.0

# --- PMC mortality-sentence extraction (corroboration only) ---
DOT = "\u2024"
ABBR = ["e.g.", "i.e.", "vs.", "cf.", "al.", "Dr.", "approx.", "no.", "Fig.", "ca."]
SIG = re.compile(r"\b(median survival|life expectanc|lifespan|life span|survival rate|"
                 r"\d+-year survival|age of death|die[ds]? (?:at|by|in|before|during)|"
                 r"fatal|lethal|premature death|reduced (?:life|surviv)|"
                 r"normal (?:life|lifespan|survival)|shortened (?:life|surviv))\b", re.I)
NUM = re.compile(r"\b\d{1,3}(?:\.\d+)?\s*(?:year|yr|month|week|day|decade)s?\b", re.I)
AGEWORD = re.compile(r"\b(in utero|neonat|perinat|infancy|early infancy|childhood)\b", re.I)
# sentences that are about a MODEL/TREATED/SUBGROUP/COMPARISON artifact, not disease-typical
# untreated natural history -> excluded from corroboration.
EXCLUDE = re.compile(r"\b(assum|model|qaly|hazard ratio|transplant|operative|interquartile|"
                     r"recipient|post-?operative|follow-up|surgical|surgery|stimulation test|"
                     r"growth hormone|parkinson|cohort of hospitalised|cohort of hospitalized|"
                     r"recruited|participants (?:were|between)|underwent)\b", re.I)


def sentences(t):
    s = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + DOT + m.group(2), t)
    for a in ABBR:
        s = s.replace(a, a.replace(".", DOT))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\u2022])", s)
    return [p.replace(DOT, ".").strip() for p in parts]


def mortality_direction(sent):
    """Fixed keyword map -> ('early_lethal'|'reduced'|'qualified'|'normal', tier) or None."""
    s = sent.lower()
    if re.search(r"normal life ?expectanc|not reduced|does not (?:affect|reduce) (?:life|lifespan)|"
                 r"normal lifespan|normal survival", s):
        return ("normal", 0.0)
    # explicit early-childhood lethality
    if (re.search(r"\b(in utero|neonat|perinat)\b", s) and re.search(r"fatal|lethal|death|die", s)) \
       or re.search(r"fatal .*(?:infancy|childhood)|death .*(?:infancy|childhood)", s) \
       or re.search(r"(?:lifespan|survival) .*under (?:5|6|7|8|9|10) years", s) \
       or re.search(r"under (?:5|6|7|8|9|10) years\b.*(?:lifespan|survival|life)", s):
        return ("early_lethal", 1.0)
    if re.search(r"slightly reduced|mildly reduced|marginally reduced", s):
        return ("qualified", 0.4)
    if re.search(r"reduced (?:life ?expectanc|lifespan|survival)|premature death|shortened (?:life|lifespan)|"
                 r"median survival", s):
        return ("reduced", 0.7)
    return None


# tier bands that count as AGREEING with a banked M value (corroboration permitted)
def m_band_agrees(banked_v, cand_tier):
    if banked_v is None:
        return False
    bands = {0.0: {0.0}, 0.4: {0.0, 0.4, 0.7}, 0.7: {0.4, 0.7, 1.0}, 1.0: {0.7, 1.0}}
    return cand_tier in bands.get(banked_v, set())


def corroborate_mortality(cui, banked_v):
    """Return (pmcid, sentence, cand_tier) for a clean agreeing mortality statement, else None."""
    path = os.path.join(LITS, f"{cui}.json")
    if not os.path.exists(path):
        return None
    art = json.load(open(path))
    if not art.get("found"):
        return None
    best = None
    for s in sentences(art.get("text", "")):
        if not (25 <= len(s) <= 320):
            continue
        if EXCLUDE.search(s):
            continue
        if not SIG.search(s):
            continue
        if not (NUM.search(s) or AGEWORD.search(s)):
            continue
        d = mortality_direction(s)
        if d and m_band_agrees(banked_v, d[1]):
            # prefer the shortest clean agreeing sentence (least incidental text)
            if best is None or len(s) < len(best[1]):
                best = (art["pmcid"], s, d[1])
    return best


def _append_once(s, frag, sep=" | "):
    s = s or ""
    return s if frag in s else (s + sep + frag if s else frag)


def load_join():
    rows = {}
    with open(os.path.join(METH, "gbd_dw_join.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            rows[r["cui"]] = r
    return rows


def load_excluded():
    rows = {}
    with open(os.path.join(METH, "gbd_dw_excluded.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            rows[r["cui"]] = r
    return rows


def main():
    dw_table = json.load(open(os.path.join(GBD, "gbd_disability_weights.json")))["weights"]
    join = load_join()
    excluded = load_excluded()
    omim_log = json.load(open(os.path.join(OMIM, "_fetch_log.json")))
    gbd_log = json.load(open(os.path.join(GBD, "_fetch_log.json")))
    lits_log = json.load(open(os.path.join(LITS, "_fetch_log.json")))

    base = json.load(open(OUT_SCORES_J))
    if "R7_open_naturalhistory" in base.get("registry_passes", []):
        subprocess.run([sys.executable, os.path.join(HERE, "r5_accession_apply.py")],
                       check=True, stdout=subprocess.DEVNULL)
        subprocess.run([sys.executable, os.path.join(HERE, "r6_naturalhistory_registry.py")],
                       check=True, stdout=subprocess.DEVNULL)
        base = json.load(open(OUT_SCORES_J))
    recs = copy.deepcopy(base["records"])

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = {"e": float(r["efficacy_offset_e"]), "R_treat": float(r["R_treat"]),
                               "grade": r["grade"], "evidence_status": r["evidence_status"]}

    lift = collections.Counter()
    promotions, locked, per_axis_changes = [], [], []
    gbd_join_audit, m_corroborations = [], []

    for r in recs:
        comp = r["components"]; cui = r["cui"]

        # ---------- DISABILITY via GBD ----------
        d = comp["D"]
        if cui in join:
            state = join[cui]["gbd_health_state"]
            if state not in dw_table:
                print(f"  ERROR: GBD state {state!r} for {r['entity']} not in pinned DW table")
                sys.exit(4)
            dw = dw_table[state]["dw2013"]; lo = dw_table[state]["ui_lo"]; hi = dw_table[state]["ui_hi"]
            tier = dw_to_tier(dw)
            old_v, old_g = d["value"], d["grade"]
            cite = (f"GBD health state '{state}' dw={dw:.3f} (95% UI {lo}-{hi}) -> disability tier "
                    f"{tier:.2f} [cut-points dw<.10:.2/.10-.30:.5/.30-.55:.75/>.55:1.0]; "
                    f"sequela: {join[cui]['dominant_untreated_sequela']}; {GBD_SRC}")
            gbd_join_audit.append({"entity": r["entity"], "cui": cui, "gbd_health_state": state,
                                   "dw2013": dw, "ui": [lo, hi], "disability_tier": tier,
                                   "prior_value": old_v, "prior_grade": old_g,
                                   "evidence_basis": join[cui]["evidence_basis"]})
            if old_g == "[L]" and old_v is not None:
                new_v = max(old_v, tier)
                tag = "corroborated" if new_v == old_v else "raised"
                d["value"] = new_v; d["grade"] = "[L]"
                d["basis"] = _append_once(d.get("basis", ""), f"GBD dw {dw:.3f} ({state}) {tag}")
                d["source"] = _append_once(d.get("source", ""), cite, sep=" + ")
                lift["D_L_corroborated" if new_v == old_v else "D_L_raised"] += 1
                if new_v != old_v:
                    per_axis_changes.append((r["entity"], "D", old_v, new_v, old_g, "[L]"))
            else:
                d["value"] = tier; d["grade"] = "[L]"
                d["basis"] = f"GBD disability weight: {state} (dw={dw:.3f}) -> tier {tier:.2f}"
                d.pop("obstacle", None); d["source"] = cite
                lift["D_H_to_L" if old_g == "[H]" else "D_O_to_L"] += 1
                per_axis_changes.append((r["entity"], "D", old_v, tier, old_g, "[L]"))
        elif cui in excluded:
            note = (f"GBD disability-weight mapping considered and declined: {excluded[cui]['exclusion_reason']} "
                    f"({GBD_SRC})")
            if d["grade"] == "[O]":
                d["obstacle"] = _append_once(d.get("obstacle", ""), note)
            else:
                d.setdefault("gbd_note", note)
            lift["D_excluded_recorded"] += 1
        else:
            if d["grade"] == "[O]":
                note = ("no single dominant GBD health state maps to the untreated natural history "
                        "(multi-domain or no characteristic disabling sequela); D not lifted, not guessed; "
                        "OMIM clinical synopsis (the licensed alternative) unavailable")
                d["obstacle"] = _append_once(d.get("obstacle", ""), note)
                lift["D_O_kept_no_state"] += 1
            else:
                lift[f"D_kept_{d['grade'].strip('[]')}"] += 1

        # ---------- MORTALITY corroboration via PMC ----------
        m = comp["M"]
        corr = corroborate_mortality(cui, m["value"])
        if corr is not None:
            pmcid, sent, cand_tier = corr
            short = (sent[:200] + "...") if len(sent) > 200 else sent
            cite = f"PMC {pmcid}: \"{short}\" (open access, retrieved {RETRIEVED})"
            m_corroborations.append({"entity": r["entity"], "cui": cui, "pmcid": pmcid,
                                     "banked_value": m["value"], "candidate_tier": cand_tier,
                                     "sentence": sent})
            if m["grade"] == "[H]":
                m["grade"] = "[L]"
                m["basis"] = _append_once(m.get("basis", ""), f"independently corroborated by PMC {pmcid}")
                m["source"] = _append_once(m.get("source", ""), cite, sep=" + ")
                lift["M_H_to_L_pmc"] += 1
                per_axis_changes.append((r["entity"], "M", m["value"], m["value"], "[H]", "[L]"))
            else:
                m["basis"] = _append_once(m.get("basis", ""), f"corroborated by PMC {pmcid}")
                m["source"] = _append_once(m.get("source", ""), cite, sep=" + ")
                lift["M_L_corroborated_pmc"] += 1
        elif m["grade"] == "[O]":
            note = ("no quantitative disease-typical survival figure in the open PMC literature "
                    "(model/treated/subgroup sentences excluded); mortality not lifted from free text "
                    "(over-trigger risk); OMIM clinical synopsis unavailable; obstacle recorded, not guessed")
            m["obstacle"] = _append_once(m.get("obstacle", ""), note)
            lift["M_O_kept_no_figure"] += 1

        # ---------- SEVERITY / PROGRESSION: obstacle (no open structured source) ----------
        s_ax = comp["S"]
        if s_ax["grade"] == "[O]":
            note = ("no open structured disease-level severity-magnitude source: Orphadata carries no "
                    "severity tier (R6); HPO severity modifiers (phenotype.hpoa) cover only 4/35 cohort "
                    "diseases and are feature-level, not a disease-level tier; GeneReviews/PMC clinical "
                    "descriptions give spectrum/range language ('ranges from mild to severe'), from which a "
                    "single tier cannot be read without inference; OMIM clinical synopsis (the only "
                    "disease-level source) is API-key-gated and the key is unobtainable here. Severity left "
                    "open, not guessed")
            s_ax["obstacle"] = _append_once(s_ax.get("obstacle", ""), note)
            lift["S_O_kept_no_source"] += 1
        else:
            lift[f"S_kept_{s_ax['grade'].strip('[]')}"] += 1
        p_ax = comp["P"]
        if p_ax["grade"] == "[O]":
            note = ("no structured open typical-course source: Orphadata supplies no frequent-enough course "
                    "term for this cohort (R6); OMIM clinical synopsis (intended source) skipped (no API key); "
                    "free-text course descriptors not extracted (ambiguous); axis left open, not guessed")
            p_ax["obstacle"] = _append_once(p_ax.get("obstacle", ""), note)
            lift["P_O_kept_no_source"] += 1
        else:
            lift[f"P_kept_{p_ax['grade'].strip('[]')}"] += 1

        # ---------- recompute composite / coverage / rankability ----------
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
        "phase": "R7 (open-source natural history: GBD disability weights + PMC survival; cumulative over R5+R6)",
        "investigation_only": base.get("investigation_only", True),
        "generated": RETRIEVED,
        "method": "methodology/BURDEN_INDEX.md + GBD2013 disability-weights pass + PMC mortality corroboration (R7)",
        "derived_from": ("burden_scores_registry.json (R5+R6) + data/raw/gbd/ (Salomon 2015 dw, pinned) + "
                         "data/raw/litsurvival/ (PMC OA, pinned) + data/raw/omim/_fetch_log.json"),
        "registry_passes": ["R5_genereviews_accession_dating", "R6_orphanet_natural_history",
                            "R7_open_naturalhistory"],
        "weights_default": W,
        "composite_rule": base.get("composite_rule"),
        "floor_rule": base.get("floor_rule"),
        "ranking_basis": base.get("ranking_basis"),
        "rankability": base.get("rankability"),
        "cohort_size": len(ordered),
        "lift_policy": (
            "D <- GBD 2013 disability weight of the disease's single dominant untreated functional sequela "
            "(methodology/gbd_dw_join.csv, cited), binned by a-priori cut-points to the BURDEN_INDEX "
            "disability tier; grade [L] (curation join, not a disease-specific measured distribution); "
            "registry [L] supersedes [H]/[O], existing [L] corroborated (max, add-only). Multi-domain/"
            "variable/mortality-dominant diseases NOT mapped (methodology/gbd_dw_excluded.csv), D kept. "
            "M <- PMC open-access survival literature, CORROBORATION ONLY: an entity-verified quantitative "
            "disease-typical survival figure agreeing with the banked M band adds a published citation and "
            "promotes [H]->[L]; model/treated/subgroup sentences excluded; free text never fills [O] M. "
            "S/P not lifted (no open structured source; OMIM synopsis skipped without a key); obstacle "
            "recorded on each open axis, never guessed."),
        "disability_tier_cutpoints": {"dw<0.10": 0.2, "0.10<=dw<0.30": 0.5,
                                      "0.30<=dw<=0.55": 0.75, "dw>0.55": 1.0},
        "omim_status": omim_log,
        "gbd_source": gbd_log,
        "litsurvival_source": {"found": lits_log.get("found"), "cohort": lits_log.get("cohort")},
        "gbd_disability_join": gbd_join_audit,
        "gbd_excluded": [{"entity": excluded[c]["entity"], "cui": c,
                          "reason": excluded[c]["exclusion_reason"]} for c in excluded],
        "pmc_mortality_corroborations": m_corroborations,
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
        "phase": "R7 (open-source natural history; cumulative over R5+R6)",
        "derived_from": "burden_scores_registry.json (R5+R6+R7) + treatments_registry.csv (R4/R5 offset)",
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
                        cell(r["burden_score"]), r["burden_score_grade"], r["treatment_grade"],
                        "yes" if r["order_locked"] else "no"])

    # ----- report -----
    print("--- R7 open-source natural-history pass (GBD disability weights + PMC survival) ---")
    print(f"  GBD disability join: {len(gbd_join_audit)} diseases mapped to a GBD health state")
    print(f"  GBD mappings declined (recorded): {len(excluded)}")
    print(f"  PMC mortality corroborations: {len(m_corroborations)}")
    print("\n  lift events:")
    for k in sorted(lift):
        print(f"    {k:26s} {lift[k]}")
    print("\n  axis grade coverage AFTER R7 (over 35):")
    for k in W:
        print(f"    {k}: {cov[k]}")
    print(f"\n  promotions (not-placed -> placed): {len(promotions)}"
          + ("".join(f"\n      + {p['entity']} ({p['axes_scored']}/5)" for p in promotions) if promotions else " (none)"))
    print(f"  order_locked diseases (all scored axes [L]/[V], >=3 axes): {len(locked)}"
          + ("".join(f"\n      * {x['entity']}" for x in locked) if locked else ""))
    if per_axis_changes:
        print("\n  axis VALUE/GRADE changes:")
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
