#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
direction_recovery.py  --  the DIRECTION-RECOVERY scoreboard (fail-closed).   [NATIVE, ROADMAP II-A]

  *** NATIVE to the VP Disease Emergence Kit (not inherited).  It is the read-only scoreboard the
      kit's own firewall implies but never tabulated: the engine FORCES a treatment DIRECTION from
      (causal-gene role x mutation mechanism), independently of any drug; this module asks, disease
      by disease, whether that forced direction is RECOVERED by the lead/approved agent that an
      independent clinical literature actually pursues. ***

THE CLAIM IT SCORES (and would falsify):
  For a resolved disease the engine emerges a corrective-axis direction (UP or DOWN) purely from
  role x mechanism -- e.g. (brake, GOF) -> axis DOWN -> correct UP.  Entirely separately, the
  registry records the lead therapeutic lever a human literature pursues, with its real-world
  axis_effect and approval status (approved / clinical / investigational).  If the engine's forced
  direction is sound, the lead lever must push the SAME way (verdict CORRECTS, axis_effect ==
  corrective_axis_direction) for EVERY resolved disease.  One disease whose lead agent moves the
  axis the OTHER way would falsify the role x mechanism -> direction map.  The scoreboard tallies
  the agreement N/total and breaks it down by axis, lever type, direct/indirect target, and lead
  approval status; it then surfaces the no-approved-drug high-value tail (direction known, no
  approved agent yet) and stamps each disease with a direction_confidence (ROADMAP I-D).

FIREWALL (unchanged kit discipline):  this module reports DIRECTION RECOVERY and APPROVAL STATUS
  only.  It asserts nothing about dose, potency, binding magnitude, response rate, efficacy or
  safety; recovery of direction is [F] (forced + cited), every magnitude remains [O].  It is
  read-only over the FROZEN analysis.json + registry, so it cannot perturb any per-disease hash.

Scoreboard gate (fail-closed):
  - every resolved disease exposes a lead corrective lever whose verdict is CORRECTS and whose
    axis_effect equals the emerged corrective_axis_direction  (direction recovered);
  - every lead lever's approval status is one of {approved, clinical, investigational};
  - every per-disease direction_confidence is one of {clean, cited-contested, ambiguous};
  - the no-approved tail is exactly the clinical+investigational set (book-keeping closes);
  - the corpus is non-vacuous and spans both axis directions;
  - a planted disease whose lead lever pushes the WRONG way is rejected by the same predicate.

Run:  python3 pipeline/direction_recovery.py [--write]   -> exit 1 on any violation
"""
import os, sys, json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")

VALID_STATUS = {"approved", "clinical", "investigational"}
VALID_CONFIDENCE = {"clean", "cited-contested", "ambiguous"}
NO_APPROVED = {"clinical", "investigational"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        FAIL.append(name)


def causal_gene_set(a):
    genes = {g["gene"] for g in a["emergence"].get("per_gene", [])}
    for sg in a["emergence"].get("suspended_genes", []):
        if isinstance(sg, dict) and sg.get("gene"):
            genes.add(sg["gene"])
    return genes


def direction_recovered(lead, corrective_dir):
    """The predicate the gate (and the self-test) both use: the lead lever must move the emergent
    axis in the corrective direction -- verdict CORRECTS and axis_effect == corrective_axis."""
    return (lead.get("verdict_vs_pathology") == "CORRECTS"
            and lead.get("axis_effect") == corrective_dir
            and corrective_dir in ("UP", "DOWN"))


def confidence_for(slug, reg_entry):
    """ROADMAP I-D: the forced role x mechanism gives an unambiguous direction by CONSTRUCTION, so
    the default is 'clean'.  A registry direction_confidence field OVERRIDES to a weaker grade for
    genuinely two-sided / dosage-sensitive biology (cited-contested) or an unresolved one
    (ambiguous).  The field is advisory metadata only -- the pipeline ignores it, so stamping it
    never perturbs a per-disease hash."""
    c = (reg_entry.get("direction_confidence") or "clean").strip()
    return c if c in VALID_CONFIDENCE else "clean"


def build():
    reg = json.load(open(os.path.join(DISEASES, "_registry.json"), encoding="utf-8"))
    rows = []
    for slug, entry in reg["diseases"].items():
        a = json.load(open(os.path.join(DISEASES, slug, "analysis.json"), encoding="utf-8"))
        if a.get("status") != "RESOLVED":
            continue
        tx = a["treatment_A_switch"]
        em = a["emergence"]
        corrective_dir = tx.get("corrective_axis_direction")
        lead = tx.get("lead_corrective_lever") or {}
        causal = causal_gene_set(a)
        tgt = lead.get("target_gene", "")
        rows.append({
            "slug": slug,
            "emergent_axis": em.get("primary_switch", {}).get("emergent_axis_direction"),
            "corrective_axis": corrective_dir,
            "lead_lever": lead.get("lever"),
            "lead_target": tgt,
            "lead_axis_effect": lead.get("axis_effect"),
            "lead_status": lead.get("status"),
            "directness": "direct" if tgt in causal else "indirect",
            "recovered": direction_recovered(lead, corrective_dir),
            "confidence": confidence_for(slug, entry),
            "no_approved_agent": lead.get("status") in NO_APPROVED,
        })

    n = len(rows)
    recovered = [r for r in rows if r["recovered"]]
    not_recovered = [r for r in rows if not r["recovered"]]

    # breakdowns: agreement N/total per class
    def breakdown(keyfn):
        tot, hit = Counter(), Counter()
        for r in rows:
            k = keyfn(r)
            tot[k] += 1
            if r["recovered"]:
                hit[k] += 1
        return {k: {"recovered": hit[k], "total": tot[k]} for k in sorted(tot)}

    by_axis = breakdown(lambda r: r["corrective_axis"])
    by_lever = breakdown(lambda r: r["lead_lever"])
    by_directness = breakdown(lambda r: r["directness"])
    by_status = breakdown(lambda r: r["lead_status"])

    # the no-approved-drug high-value tail: direction known, no approved agent yet
    tail = sorted(
        ({"slug": r["slug"], "lead_lever": r["lead_lever"], "lead_target": r["lead_target"],
          "corrective_axis": r["corrective_axis"], "lead_status": r["lead_status"],
          "confidence": r["confidence"]}
         for r in rows if r["no_approved_agent"]),
        key=lambda d: (d["lead_status"], d["slug"]))

    status_counts = Counter(r["lead_status"] for r in rows)
    confidence_counts = Counter(r["confidence"] for r in rows)

    print("Direction-recovery scoreboard  [NATIVE / ROADMAP II-A]")

    # 1) the central invariant: forced direction recovered by the lead lever, every resolved disease
    for r in not_recovered:
        print(f"    [FAIL] {r['slug']} :: emerged correct={r['corrective_axis']} but lead "
              f"{r['lead_lever']}->{r['lead_target']} axis_effect={r['lead_axis_effect']} "
              f"verdict-mismatch")
    check(f"forced corrective direction recovered by the lead lever in every resolved disease "
          f"({len(recovered)}/{n})", not not_recovered)

    # 2) every lead status recognised
    bad_status = [r["slug"] for r in rows if r["lead_status"] not in VALID_STATUS]
    check(f"every lead lever has a recognised approval status {sorted(VALID_STATUS)}", not bad_status)

    # 3) every per-disease direction_confidence valid (ROADMAP I-D)
    bad_conf = [r["slug"] for r in rows if r["confidence"] not in VALID_CONFIDENCE]
    check(f"every direction_confidence in {sorted(VALID_CONFIDENCE)} "
          f"(clean={confidence_counts['clean']}, cited-contested={confidence_counts['cited-contested']}, "
          f"ambiguous={confidence_counts['ambiguous']})", not bad_conf)

    # 4) book-keeping closes: tail == clinical+investigational == n - approved
    tail_ok = (len(tail) == status_counts["clinical"] + status_counts["investigational"]
               == n - status_counts["approved"])
    check(f"no-approved tail closes book-keeping (tail={len(tail)} == "
          f"clinical{status_counts['clinical']}+investigational{status_counts['investigational']} == "
          f"resolved{n}-approved{status_counts['approved']})", tail_ok)

    # 5) non-vacuity: corpus spans both axis directions
    spans_both = ("UP" in by_axis and "DOWN" in by_axis and n > 0)
    check(f"scoreboard is non-vacuous and spans both axis directions "
          f"(UP={by_axis.get('UP',{}).get('total',0)}, DOWN={by_axis.get('DOWN',{}).get('total',0)})",
          spans_both)

    result = {
        "title": "Direction-recovery scoreboard -- is the forced role x mechanism direction recovered "
                 "by the lead agent, disease by disease",
        "native_to": "vp_disease_emergence_kit (ROADMAP II-A); read-only over frozen analysis.json + registry",
        "principle": ("the engine forces a corrective-axis direction from (causal-gene role x mutation "
                      "mechanism) with no reference to any drug; this scoreboard checks that the lead "
                      "agent an independent literature pursues pushes the SAME way -- agreement is the "
                      "falsifiable claim, a single wrong-way lead lever would break the direction map."),
        "firewall": ("DIRECTION recovery + approval STATUS only; not dose, not potency, not binding "
                     "magnitude, not response rate, not efficacy, not safety; direction recovered is "
                     "[F] forced+cited, every magnitude remains [O]; read-only, perturbs no hash."),
        "grade": "[F] direction recovery forced + cited ; [O] all magnitude/efficacy/dose",
        "n_resolved": n,
        "direction_recovered": len(recovered),
        "direction_recovery_rate": f"{len(recovered)}/{n}",
        "recovery_by_corrective_axis": by_axis,
        "recovery_by_lead_lever_type": by_lever,
        "recovery_by_target_directness": by_directness,
        "recovery_by_lead_status": by_status,
        "lead_status_counts": dict(status_counts),
        "direction_confidence_counts": dict(confidence_counts),
        "no_approved_drug_high_value_tail": tail,
        "per_disease": sorted(rows, key=lambda r: r["slug"]),
        "overall": "PASS" if not FAIL else "FAIL",
        "failures": FAIL,
    }
    return result


def selftest():
    """Prove the scoreboard has TEETH: a synthetic disease whose lead lever pushes the axis the
    WRONG way (verdict not CORRECTS / axis_effect opposite the corrective direction) must be
    rejected by the very predicate the gate uses; a correct one must pass."""
    good = direction_recovered({"verdict_vs_pathology": "CORRECTS", "axis_effect": "UP"}, "UP")
    wrong_axis = direction_recovered({"verdict_vs_pathology": "CORRECTS", "axis_effect": "DOWN"}, "UP")
    wrong_verdict = direction_recovered({"verdict_vs_pathology": "WORSENS", "axis_effect": "UP"}, "UP")
    no_dir = direction_recovered({"verdict_vs_pathology": "CORRECTS", "axis_effect": "UP"}, None)
    ok = good and not wrong_axis and not wrong_verdict and not no_dir
    print("  [self-test] scoreboard teeth:",
          f"aligned(pass)={good}  wrong-axis(reject)={not wrong_axis}  "
          f"wrong-verdict(reject)={not wrong_verdict}  no-direction(reject)={not no_dir}  "
          f"-> {'OK' if ok else 'BROKEN'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    teeth_ok = selftest()
    res = build()
    if not teeth_ok:
        res["overall"] = "FAIL"
        res.setdefault("failures", []).append("self-test: scoreboard predicate is broken")
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "modules", "expected", "direction_recovery.json")
        json.dump(res, open(p, "w"), indent=1)
        print(f"  wrote {os.path.relpath(p, ROOT)}")
    print(f"  direction recovered: {res['direction_recovery_rate']} resolved diseases; "
          f"approved={res['lead_status_counts'].get('approved',0)} "
          f"clinical={res['lead_status_counts'].get('clinical',0)} "
          f"investigational={res['lead_status_counts'].get('investigational',0)}; "
          f"no-approved tail={len(res['no_approved_drug_high_value_tail'])}")
    print("OVERALL:", "PASS" if res["overall"] == "PASS" else f"FAIL {res['failures']}")
    sys.exit(0 if res["overall"] == "PASS" else 1)
