#!/usr/bin/env python3
# =============================================================================
# W-phase - UNMET-NEED / TREATMENT-GAP SURFACE  (no new data; a registry view)
# -----------------------------------------------------------------------------
# FUTURE_WORK.md S4: the single highest-value, most patient- and field-beneficial
# output the framework can produce -- a transparent, fully-graded "where the gap
# between burden and available therapy is largest" surface, framed EXPLICITLY as a
# research-prioritisation signal for researchers and funders, NOT clinical advice
# and NOT a promise. It needs almost no new data: it is a deterministic re-
# presentation of what the index already computes.
#
#   residual (unmet-need) signal  =  burden_score  =  raw_burden * (1 - e)
#
# A disease with HIGH burden and LOW treatability (high R_treat = small efficacy
# offset e) has a LARGE residual -- a large gap between suffering and available
# therapy. The HONEST HEADLINE of unmet need is the set of diseases whose burden
# is registry-grade [L] AND whose evidence_status is 'none' (no disease-directed
# therapy exists): high-confidence burden with no therapy to offset it.
#
# Every cell carries its grade; the burden-order PROVISIONAL flag is kept intact
# wherever the order is provisional (i.e. wherever the disease is not order-locked).
# This surface makes NO cure claim, NO outcome prediction, and NO individual
# prognosis -- it is a map of WHERE TO LOOK, not a claim about WHAT WILL BE FOUND.
#
# Pure view: every value is re-derived from the R9 registry; the gate re-derives
# every cell from the registry, so the surface cannot drift from it. LIVING CODE,
# NOT in the frozen engine pin.
#
# Out: data/curated/unmet_need_surface.{json,csv}
# =============================================================================
import os, csv, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
RESID_C = os.path.join(CUR, "burden_residual_registry.csv")
OUT_J = os.path.join(CUR, "unmet_need_surface.json")
OUT_C = os.path.join(CUR, "unmet_need_surface.csv")
GENERATED = "2026-06-18"

# evidence_status -> a transparent treatment-gap class label (declared; not fitted)
GAP_CLASS = {
    "none": "no_disease_directed_therapy",
    "symptomatic": "symptomatic_only",
    "disease-modifying (partial)": "partial_disease_modifying",
    "disease-modifying (substantial)": "substantial_disease_modifying",
    "curative / effectively normalizing": "curative_or_normalizing",
    "curative": "curative_or_normalizing",
}


def main():
    scores = json.load(open(SCORES_J))
    if "R9_litcurate_severity_progression" not in scores.get("registry_passes", []):
        raise SystemExit("ERROR: unmet-need surface expects the R9 registry (registry_passes missing R9)")
    rec_by_cui = {r["cui"]: r for r in scores["records"]}

    # residual registry carries evidence_status / efficacy_offset / R_treat / burden_score per disease
    resid = list(csv.DictReader(open(RESID_C, newline="")))

    rows = []
    for r in resid:
        cui = r["cui"]
        sc = rec_by_cui[cui]
        # numeric fields come from the FULL-PRECISION registry JSON (not the 4-dp CSV),
        # so residual_unmet_need == the registry burden_score exactly and re-derives cleanly.
        raw = sc["raw_burden"]
        residual = sc["burden_score"]
        Rt = round(sc["treatability"]["value"], 12)
        e = round(1.0 - Rt, 12)
        ev = r["evidence_status"]
        gap_class = GAP_CLASS.get(ev, "unknown")
        order_locked = bool(sc.get("order_locked"))
        burden_grade = sc["raw_burden_grade_present"]
        headline = (burden_grade == "[L]" and ev == "none")
        rows.append({
            "entity": r["entity"], "cui": cui, "tier": r["tier"], "system_class": r["system_class"],
            "rankable": r["rankable"] == "yes",
            "raw_burden": raw, "burden_grade": burden_grade,
            "evidence_status": ev, "treatment_gap_class": gap_class,
            "efficacy_offset_e": e, "R_treat": Rt,
            "treatment_grade": sc["treatment_grade"],
            "residual_unmet_need": residual, "residual_grade": sc["burden_score_grade"],
            "burden_order_provisional": (not order_locked),
            "order_locked": order_locked,
            "headline_unmet_need": headline,
        })

    placed = sorted([x for x in rows if x["rankable"]],
                    key=lambda x: (-(x["residual_unmet_need"] if x["residual_unmet_need"] is not None else -1),
                                   -(x["raw_burden"] if x["raw_burden"] is not None else -1), x["entity"]))
    not_placed = sorted([x for x in rows if not x["rankable"]],
                        key=lambda x: (-(x["residual_unmet_need"] if x["residual_unmet_need"] is not None else -1),
                                       x["entity"]))
    for i, x in enumerate(placed, 1):
        x["unmet_rank"] = i
    for x in not_placed:
        x["unmet_rank"] = None
    ordered = placed + not_placed

    headline = [x["entity"] for x in ordered if x["headline_unmet_need"]]

    payload = {
        "schema": "disease_wp.unmet_need_surface/v1",
        "phase": "W (unmet-need / treatment-gap surface; a graded view over the R9 registry)",
        "generated": GENERATED,
        "derived_from": "burden_scores_registry.json (R5..R9) + burden_residual_registry.csv",
        "what_this_is": ("a transparent, fully-graded research-PRIORITISATION signal: for each disease, its "
                         "burden, its treatability, and the RESIDUAL (the gap between them), surfaced so that "
                         "researchers and funders can see where the unmet need is largest. The residual "
                         "(unmet-need) signal is burden_score = raw_burden * (1 - e)."),
        "what_this_is_not": ("NOT clinical guidance; NOT a diagnosis, dose, or individual prognosis; NOT a cure "
                             "claim, an outcome prediction, or a timeline; NOT a ranking of patients. It is a map "
                             "of WHERE TO LOOK, not a claim about WHAT WILL BE FOUND."),
        "residual_rule": "residual_unmet_need = burden_score = raw_burden * (1 - efficacy_offset_e)",
        "headline_rule": ("headline_unmet_need = (burden is registry-grade [L]) AND (evidence_status == 'none', "
                          "i.e. no disease-directed therapy exists): the highest-confidence burden with no therapy "
                          "to offset it -- the honest headline of unmet need."),
        "provisional_note": ("burden_order_provisional is kept intact wherever the disease is NOT order-locked: the "
                             "burden ORDER remains a provisional [H] prioritisation device cohort-wide, and only "
                             "order-locked diseases (all scored axes registry-grade) carry a registry-locked burden "
                             "VALUE. Grades are carried on every cell."),
        "treatment_gap_class_map": GAP_CLASS,
        "grade_carried": ("burden_grade = raw_burden_grade_present (trustworthiness of the burden value); "
                          "treatment_grade and residual_grade carried from the registry."),
        "placed": len(placed),
        "not_placed": len(not_placed),
        "headline_unmet_need_diseases": headline,
        "order_locked_count": sum(1 for x in ordered if x["order_locked"]),
        "records": ordered,
    }
    json.dump(payload, open(OUT_J, "w"), indent=2, ensure_ascii=False)

    cols = ["unmet_rank", "entity", "cui", "tier", "system_class", "rankable",
            "raw_burden", "burden_grade", "evidence_status", "treatment_gap_class",
            "efficacy_offset_e", "R_treat", "treatment_grade",
            "residual_unmet_need", "residual_grade",
            "burden_order_provisional", "order_locked", "headline_unmet_need"]
    with open(OUT_C, "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols)
        for x in ordered:
            def cell(v):
                if v is None:
                    return ""
                if isinstance(v, bool):
                    return "yes" if v else "no"
                if isinstance(v, float):
                    return f"{v:.4f}"
                return v
            w.writerow([cell(x[c]) for c in cols])

    # ----- report -----
    print("--- unmet-need / treatment-gap surface (graded view over the R9 registry) ---")
    print(f"  placed {len(placed)} / not-placed {len(not_placed)};  order-locked burden values: "
          f"{payload['order_locked_count']}")
    print(f"\n  HONEST HEADLINE (burden [L] + no disease-directed therapy): {len(headline)}")
    for e in headline:
        print(f"      * {e}")
    print("\n  largest treatment gaps (top of the placed residual order):")
    for x in placed[:8]:
        prov = "provisional" if x["burden_order_provisional"] else "LOCKED"
        print(f"    {x['unmet_rank']:>2}. {x['entity'][:34]:34s} burden {x['raw_burden']:.3f}{x['burden_grade']} "
              f"x R_treat {x['R_treat']:.2f} = residual {x['residual_unmet_need']:.3f}{x['residual_grade']}  "
              f"[{x['treatment_gap_class']}; {prov}]")

    h = hashlib.sha256()
    for p in (OUT_C, OUT_J):
        h.update(open(p, "rb").read())
    print(f"\n  unmet-need surface sha256[:12]: {h.hexdigest()[:12]}")


if __name__ == "__main__":
    main()
