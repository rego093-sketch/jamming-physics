#!/usr/bin/env python3
"""
R4 stage 2 -- residual burden over the R3 ordering.

Reads the BANKED R3 deliverable data/curated/burden_scores.json (raw_burden is read
UNCHANGED; R4 does not mutate R3) and the R4 survey data/curated/treatments.csv. Applies
the treatability offset from TREATMENT_INDEX.md:

    R_treat = 1 - e ;   burden_score = raw_burden * R_treat

and RE-RANKS the placed diseases by residual burden_score (the clinically relevant order:
what is left after best available therapy). The placed set is exactly the R3 rankability
cut (axes_scored >= 3) -- therapy adds no burden axes -- and the 18 not-placed diseases
stay not-placed (rank = null). A sensitivity pass recomputes the residual order under the
five R3 axis weightings.

INVESTIGATION ONLY (no whitepaper prose). Deterministic, no network.

Grade of the residual burden_score: floor over (raw_burden grade_present, R_treat grade).
In R3, burden_score floored to [O] because treatability was deferred ([O]); in R4 R_treat is
[H] (TREATMENT_INDEX.md two-tier evidence), so the residual burden_score grade is the honest
floor of the burden-axis confidence and the [H] treatability confidence.

Out: data/curated/burden_residual.csv   (flat, gate- and human-readable)
     data/curated/burden_residual.json  (schema disease_wp.burden_residual/v1)
"""
import csv, os, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BURDEN = os.path.join(ROOT, "data", "curated", "burden_scores.json")
TREAT = os.path.join(ROOT, "data", "curated", "treatments.csv")
OUT_CSV = os.path.join(ROOT, "data", "curated", "burden_residual.csv")
OUT_JSON = os.path.join(ROOT, "data", "curated", "burden_residual.json")
RETRIEVED = "2026-06-17"

GRADE_RANK = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3}
AXES = ["O", "P", "S", "M", "D"]
W = {"O": 0.20, "P": 0.20, "S": 0.20, "M": 0.20, "D": 0.20}


def floor_grade(grades):
    gs = [g for g in grades if g in GRADE_RANK]
    return min(gs, key=lambda g: GRADE_RANK[g]) if gs else "[O]"


def weighted_burden(components, weights):
    """renormalised mean of present axis values under given weights (R3-identical)."""
    num = den = 0.0
    for k, w in weights.items():
        ax = components[k]
        if ax["value"] is not None:
            num += w * ax["value"]
            den += w
    return (num / den) if den else None


# ---- Spearman (R3-identical, no scipy) ---- #
def rank_vec(vals):
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j + 1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            r[order[k]] = avg
        i = j + 1
    return r


def spearman(a, b):
    ra, rb = rank_vec(a), rank_vec(b)
    n = len(a)
    if n < 2:
        return 1.0
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((ra[i] - ma) * (rb[i] - mb) for i in range(n))
    va = sum((x - ma) ** 2 for x in ra) ** 0.5
    vb = sum((x - mb) ** 2 for x in rb) ** 0.5
    return round(cov / (va * vb), 4) if va and vb else 1.0


def read_treatments():
    """cui -> {e, R_treat, evidence_status, evidence_tier, grade, modality}."""
    out = {}
    with open(TREAT, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[r["cui"]] = {
                "e": float(r["efficacy_offset_e"]),
                "R_treat": float(r["R_treat"]),
                "evidence_status": r["evidence_status"],
                "evidence_tier": r["evidence_tier"],
                "grade": r["grade"],
                "modality": r["modality"],
            }
    return out


def main():
    payload = json.load(open(BURDEN, encoding="utf-8"))
    treat = read_treatments()

    base = payload["records"]
    base_cuis = {r["cui"] for r in base}
    missing = base_cuis - set(treat)
    if missing:
        raise SystemExit(f"treatments.csv missing {len(missing)} cohort CUIs: {sorted(missing)[:5]}")

    recs = []
    for r in base:
        cui = r["cui"]
        t = treat[cui]
        raw = r["raw_burden"]                       # UNCHANGED from R3
        e = t["e"]
        R_treat = round(t["R_treat"], 12)
        burden_score = round(raw * R_treat, 12) if raw is not None else None
        # residual grade: floor of burden-axis present-grade and the [H] treatability grade
        bs_grade = floor_grade([r["raw_burden_grade_present"], t["grade"]]) if raw is not None else "[O]"

        recs.append({
            "entity": r["entity"], "cui": cui, "tier": r["tier"],
            "system_class": r["system_class"], "genes": r["genes"], "omim_codes": r["omim_codes"],
            "components": r["components"],
            "axes_scored": r["axes_scored"], "rankable": r["rankable"],
            "raw_rank": r["rank"],
            "raw_burden": raw,
            "raw_burden_grade_present": r["raw_burden_grade_present"],
            "evidence_status": t["evidence_status"], "evidence_tier": t["evidence_tier"],
            "efficacy_offset_e": e,
            "treatability": {
                "value": R_treat, "grade": t["grade"],
                "basis": f"R_treat = 1 - e = {R_treat:.2f}; e = {e:.2f} for evidence_status '{t['evidence_status']}' (TREATMENT_INDEX.md offset map)",
                "source": f"data/curated/treatments.csv (modality: {t['modality'][:60]}...)" if len(t["modality"]) > 60
                          else f"data/curated/treatments.csv (modality: {t['modality']})",
            },
            "burden_score": burden_score,
            "burden_score_grade": bs_grade,
        })

    # ---- residual re-ranking: placed set only (R3 rankability cut, unchanged) ----
    placed = sorted([r for r in recs if r["rankable"]],
                    key=lambda r: (-(r["burden_score"] if r["burden_score"] is not None else -1),
                                   -(r["raw_burden"] if r["raw_burden"] is not None else -1),
                                   -r["axes_scored"], r["entity"]))
    not_placed = sorted([r for r in recs if not r["rankable"]],
                        key=lambda r: (-r["axes_scored"], r["entity"]))
    for i, r in enumerate(placed, 1):
        r["residual_rank"] = i
        r["rank_shift_vs_raw"] = (r["raw_rank"] - i) if r["raw_rank"] is not None else None
    for r in not_placed:
        r["residual_rank"] = None
        r["rank_shift_vs_raw"] = None
    recs = placed + not_placed

    # ---- residual sensitivity under the five R3 weightings ----
    # recompute raw_burden(weighting) over placed, scale by R_treat -> residual(weighting),
    # Spearman vs equal-weight residual default.
    alt_weightings = {
        "equal_default":         W,
        "onset_heavy":           {"O": 0.40, "P": 0.15, "S": 0.15, "M": 0.15, "D": 0.15},
        "mortality_heavy":       {"O": 0.15, "P": 0.15, "S": 0.15, "M": 0.40, "D": 0.15},
        "severity_heavy":        {"O": 0.15, "P": 0.15, "S": 0.40, "M": 0.15, "D": 0.15},
        "drop_disability_core4": {"O": 0.25, "P": 0.25, "S": 0.25, "M": 0.25, "D": 0.0},
    }
    default_resid = []
    for r in placed:
        rb = weighted_burden(r["components"], W)
        default_resid.append((rb if rb is not None else 0.0) * r["treatability"]["value"])
    sensitivity = {}
    for label, ww in alt_weightings.items():
        vals = []
        for r in placed:
            rb = weighted_burden(r["components"], ww)
            vals.append((rb if rb is not None else 0.0) * r["treatability"]["value"])
        sensitivity[label] = {"weights": ww, "spearman_vs_default": spearman(default_resid, vals)}

    # ---- CSV ----
    cols = ["residual_rank", "raw_rank", "rank_shift_vs_raw", "rankable", "entity", "cui",
            "tier", "system_class", "raw_burden", "raw_burden_grade_present",
            "evidence_status", "efficacy_offset_e", "R_treat", "R_treat_grade",
            "burden_score", "burden_score_grade"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for r in recs:
            def cell(v):
                return "" if v is None else (f"{v:.4f}" if isinstance(v, float) else v)
            w.writerow([
                cell(r["residual_rank"]), cell(r["raw_rank"]), cell(r["rank_shift_vs_raw"]),
                "yes" if r["rankable"] else "no", r["entity"], r["cui"], r["tier"], r["system_class"],
                cell(r["raw_burden"]), r["raw_burden_grade_present"],
                r["evidence_status"], cell(r["efficacy_offset_e"]),
                cell(r["treatability"]["value"]), r["treatability"]["grade"],
                cell(r["burden_score"]), r["burden_score_grade"],
            ])

    # ---- JSON ----
    out = {
        "schema": "disease_wp.burden_residual/v1",
        "phase": "R4", "investigation_only": True, "generated": RETRIEVED,
        "method": "methodology/TREATMENT_INDEX.md (R_treat = 1 - e; burden_score = raw_burden * R_treat)",
        "reads_unchanged": "data/curated/burden_scores.json raw_burden (R3 banked; not mutated)",
        "offset_source": "data/curated/treatments.csv (R4 survey)",
        "residual_rule": "burden_score = raw_burden * (1 - e); placed set = R3 rankability cut (axes_scored>=3), re-ranked by residual burden_score desc, then raw_burden desc, then axes_scored desc, then entity",
        "grade_rule": "burden_score grade = floor over (raw_burden grade_present, R_treat grade [H]); null where raw_burden null",
        "weights_default": W,
        "cohort_size": len(recs),
        "placed": len(placed), "not_placed": len(not_placed),
        "sensitivity": sensitivity,
        "status_distribution": dict(collections.Counter(r["evidence_status"] for r in recs)),
        "records": [{
            "residual_rank": r["residual_rank"], "raw_rank": r["raw_rank"],
            "rank_shift_vs_raw": r["rank_shift_vs_raw"],
            "entity": r["entity"], "cui": r["cui"], "tier": r["tier"],
            "system_class": r["system_class"], "genes": r["genes"], "omim_codes": r["omim_codes"],
            "rankable": r["rankable"], "axes_scored": r["axes_scored"],
            "raw_burden": r["raw_burden"], "raw_burden_grade_present": r["raw_burden_grade_present"],
            "evidence_status": r["evidence_status"], "evidence_tier": r["evidence_tier"],
            "efficacy_offset_e": r["efficacy_offset_e"],
            "treatability": r["treatability"],
            "burden_score": r["burden_score"], "burden_score_grade": r["burden_score_grade"],
        } for r in recs],
        "grade_vocabulary": {
            "[L]": "registry-stated and cited (carried from R3 burden axes)",
            "[H]": "inference from cited text / established science (burden axes and/or treatability)",
            "[O]": "open/unavailable; obstacle named; not guessed",
        },
        "note": ("Residual (post-treatment) order. raw_burden is the R3 pre-treatment burden, read "
                 "unchanged. The treatability offset e is the R4 [H]-grade survey value; the residual "
                 "burden_score therefore inherits an [H] grade (TREATMENT_INDEX.md two-tier evidence, "
                 "accession-dated [L] verification deferred). Like the R3 order, this is a provisional "
                 "[H]-grade prioritisation device, not a registry-locked ranking."),
    }
    json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # ---- report ----
    print("--- R4 residual burden built ---")
    print(f"  cohort: {len(recs)}  placed: {len(placed)}  not_placed: {len(not_placed)}")
    print(f"  -> {os.path.relpath(OUT_CSV, ROOT)}")
    print("\n  RESIDUAL ORDER (burden_score = raw_burden * (1 - e); shift vs R3 raw order):")
    print(f"    {'#':>2} {'was':>3} {'Δ':>3}  {'disease':40s} {'raw':>5s} {'e':>4s} {'resid':>6s} {'grd':>4s}  status")
    for r in placed:
        sh = r["rank_shift_vs_raw"]
        sh_s = (f"+{sh}" if sh > 0 else (str(sh) if sh < 0 else "·"))
        print(f"    {r['residual_rank']:2d} {r['raw_rank']:>3} {sh_s:>3}  {r['entity'][:40]:40s} "
              f"{r['raw_burden']:.3f} {r['efficacy_offset_e']:.2f} {r['burden_score']:.4f} "
              f"{r['burden_score_grade']:>4s}  {r['evidence_status']}")
    print("\n  residual sensitivity (Spearman rho vs equal-weight residual default):")
    for label, sd in sensitivity.items():
        print(f"    {label:24s} rho = {sd['spearman_vs_default']}")

    h = hashlib.sha256()
    for p in (OUT_CSV, OUT_JSON):
        h.update(open(p, "rb").read())
    print(f"\n  residual sha256[:12]: {h.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
