#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
burden_prioritisation.py  --  IV burden-weighted target-AXIS prioritisation.

Ported from analgesic_threshold_logic v2.0's M10 (Zenodo concept DOI 10.5281/zenodo.20733420).
Ranks the comfort-map target AXES by DECLARED, cited weights -- it ranks AXES, never drugs, doses,
or efficacy. The measured master-gene gamma is carried alongside (provenance) but is NEVER folded
into the score, exactly as the analgesic build carried gamma-|h_sp| alongside without scoring it.

Score = w_burden * burden + w_unmet * unmet + w_counterreg * counterreg_freedom + w_ground * grounding.
All four sub-scores are CITED 1-5 tiers (or, for counter-regulation-freedom, READ off the proven
loop: H1=free=5, H2=low=4, H3=prone-alone=2). The weights are DECLARED here, never reverse-fit.

FIREWALL: this is a target-AXIS ranking for research prioritisation. It is NOT a recommendation of any
drug, dose, regimen, or clinical decision; no efficacy/safety/tolerability is implied by rank. The
per-axis molecular mechanism remains [O] cited biology. No medical responsibility.

Run:  python3 burden_prioritisation.py  -> expected/comfort_priority.json
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HERE, "expected", "comfort_map.json")

# DECLARED weights (sum = 1.0), never reverse-fit from a desired ranking.
WEIGHTS = {"burden": 0.35, "unmet_need": 0.25, "counterreg_freedom": 0.25, "grounding": 0.15}

# CITED 1-5 tiers per axis (burden + unmet-need), source-tagged. counterreg_freedom is READ off the
# proven loop (not a citation): H1 free=5, H2 low=4, H1-like(HF)=5, H3 prone-alone=2. grounding: a
# DNA-measured master-gene gamma = 5, a cited molecular sensor/axis = 3.
AXIS_TIERS = {
  "raas_ren": dict(
      burden=5, unmet_need=4,
      burden_src="essential hypertension is the leading modifiable cardiovascular risk worldwide (GBD) [L]",
      unmet_src="lifelong operating-point regimens with escape/adherence burden; durable reference reset under-served [L]"),
  "sodium_volume_reference": dict(
      burden=5, unmet_need=4,
      burden_src="population-attributable Na-BP burden (INTERSALT/DASH) [L]",
      unmet_src="sustained Na/weight reference reset is behaviourally hard; durable adherence under-served [L]"),
  "renal_sympathetic": dict(
      burden=4, unmet_need=4,
      burden_src="resistant/essential hypertension subset (SPYRAL) [L]",
      unmet_src="device reference reset newly approved; access/durability data maturing [L]"),
  "baroreflex_piezo": dict(
      burden=3, unmet_need=3,
      burden_src="resistant hypertension / autonomic lability subset [L]",
      unmet_src="baroreflex activation is niche; mechanistic sensor (PIEZO) under-exploited [L]"),
  "hf_margin_fourpillar": dict(
      burden=5, unmet_need=3,
      burden_src="chronic heart failure morbidity/mortality (Tier-1) [L]",
      unmet_src="four pillars established but under-titrated; margin-growing logic under-applied [L]"),
  "svr_effector": dict(
      burden=4, unmet_need=2,
      burden_src="broad antihypertensive use (effector class) [L]",
      unmet_src="well-served as adjunct; monotherapy escapes -- low UNMET as a paired adjunct [L]"),
}

# counter-regulation-freedom read off the proven loop (lever -> 1-5)
CR_FREEDOM = {"H1": 5, "H1-like (HF)": 5, "H2": 4, "H3": 2}


def _grounding(entry):
    return 5 if entry.get("dna_grounded") else 3


def prioritise():
    m = json.load(open(MAP, encoding="utf-8"))
    entries = {e["axis"]: e for e in m["entries"]}
    rows = []
    for axis, t in AXIS_TIERS.items():
        e = entries[axis]
        crf = CR_FREEDOM.get(e["lever"], 3)
        grd = _grounding(e)
        score = (WEIGHTS["burden"] * t["burden"]
                 + WEIGHTS["unmet_need"] * t["unmet_need"]
                 + WEIGHTS["counterreg_freedom"] * crf
                 + WEIGHTS["grounding"] * grd)
        rows.append({
            "axis": axis, "lever": e["lever"],
            "burden_tier": t["burden"], "unmet_need_tier": t["unmet_need"],
            "counterreg_freedom_tier": crf, "grounding_tier": grd,
            "score": round(score, 4),
            "measured_gamma_carried_not_scored": e.get("measured_gamma"),
            "dna_grounded": e.get("dna_grounded"),
            "burden_src": t["burden_src"], "unmet_src": t["unmet_src"],
            "grade": "[F] rank from DECLARED weights x CITED/loop tiers; gamma carried, never scored",
        })
    rows.sort(key=lambda r: (-r["score"], r["axis"]))
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return {
        "title": "Burden-weighted comfort target-AXIS prioritisation (ranks axes, not agents or regimens)",
        "imported_from": "analgesic_threshold_logic v2.0 M10 (Zenodo concept DOI 10.5281/zenodo.20733420)",
        "weights_declared": WEIGHTS,
        "scoring_note": ("score = sum(declared weight x tier); counter-regulation-freedom is READ off the "
                         "proven loop (H1 free / H2 low / H3 prone-alone); measured gamma is carried for "
                         "provenance and is NEVER folded into the score"),
        "firewall": ("a target-AXIS ranking for research prioritisation only -- NOT a drug, dose, regimen, "
                     "clinical decision, efficacy, safety, or tolerability claim. Per-axis molecular mechanism "
                     "stays [O] cited biology. No medical responsibility."),
        "n_axes": len(rows),
        "order": [r["axis"] for r in rows],
        "ranking": rows,
    }


if __name__ == "__main__":
    p = prioritise()
    json.dump(p, open(os.path.join(HERE, "expected", "comfort_priority.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("IV burden-weighted target-axis prioritisation (declared weights; gamma carried, not scored):")
    print("  %-4s %-26s %-12s %-7s %s" % ("rank", "axis", "lever", "score", "grounded(gamma)"))
    for r in p["ranking"]:
        g = ("yes g=%s" % r["measured_gamma_carried_not_scored"]) if r["dna_grounded"] else "cited"
        print("  %-4d %-26s %-12s %-7g %s" % (r["rank"], r["axis"], r["lever"], r["score"], g))
    print("wrote expected/comfort_priority.json  (%d axes)" % p["n_axes"])
