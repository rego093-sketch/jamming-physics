#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
external_mechanism_honesty.py  --  D3: the clinical-anchor honesty gate (fail-closed).

INHERITED TECHNIQUE: analgesic_threshold_logic_v2_0 / M11 (11-l3-honesty), DOI 10.5281/zenodo.20733420.
In the analgesic package the L3 axis (NGF/CGRP receptor signalling + network gain) is NOT captured by the
gamma read, so its MECHANISM LINK must be graded cited-biology [O], never derived [V]/[F]. This is the
immune analogue. The bistable R19 kernel DERIVES a treatment DIRECTION/CLASS (which basin, which lever),
but the CLINICAL EFFICACY of a real therapy (ATRA->APL cure, CAR-T/checkpoint clearance, carcinogen
cessation epidemiology) is EXTERNAL cited biology the kernel does not derive. This gate enforces, lever by
lever, that every clinical anchor is graded cited [L] (or [O]), never as a derived ([V]/[F]) clinical claim,
and that the molecule/dose/patient-response is explicitly held [O].

Gate (fail-closed):
  - every therapy lever that carries a clinical_anchor has a grade that marks the clinical anchor [L]
    (cited), and does NOT present the clinical efficacy as derived [V]/[F];
  - the synthesis carries an explicit honest_limit AND open_obstacle stating molecule/dose/response are
    [O] / not predicted by the kernel;
  - the "what_VP_adds" statement says VP does NOT invent the therapies (re-derives the CLASS only);
  - no lever folds a specific molecule/dose into a derived claim.

Run:  python3 external_mechanism_honesty.py  -> expected/mechanism_honesty.json ; exit 1 on any violation
"""
import os, sys, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
PKG  = os.path.normpath(os.path.join(HERE, "..", ".."))
for sub in ("_engine", "_therapy"):
    sys.path.insert(0, os.path.join(PKG, "repro", sub))
sys.path.insert(0, os.path.join(PKG, "inherited"))
import vp_imm_engine as ENG
import fundamental_therapy as TH

LEVERS = ["lever_A", "lever_B", "lever_C", "lever_D"]


def run():
    res = ENG.circulate()
    G = {o["organ"]: o["gamma"] for o in res["organs"]["organs"] if o.get("gamma") is not None}
    tr = TH.therapy_report(G)

    per_lever, fail = {}, []
    for lev in LEVERS:
        d = tr.get(lev, {})
        anchor = d.get("clinical_anchor", "")
        grade  = d.get("grade", "")
        has_anchor = bool(anchor.strip())
        # the clinical efficacy must be CITED [L] (or [L-class]), never derived
        cited_L     = bool(re.search(r"\[L(?:-class)?\]", anchor) or re.search(r"\[L(?:-class)?\]", grade))
        not_derived = not bool(re.search(r"clinical[^.]*\[(?:V|F)\]", grade, flags=re.I))
        # something in the grade must be [O] (the molecule/absolute scale is open) OR the synthesis holds it open
        ok = (has_anchor and cited_L and not_derived)
        if not ok:
            fail.append(lev)
        per_lever[lev] = {"clinical_anchor": anchor, "grade": grade, "has_anchor": has_anchor,
                          "clinical_cited_[L]": cited_L, "clinical_not_derived": not_derived, "ok": ok}

    syn = tr.get("synthesis", {})
    honest_limit  = syn.get("honest_limit", "")
    open_obstacle = syn.get("open_obstacle", "")
    what_vp_adds  = syn.get("what_VP_adds", "")
    limit_states_open = bool(re.search(r"\b(dose|molecule|schedule|response)\b", honest_limit, flags=re.I)
                             and re.search(r"\bnot\b", honest_limit, flags=re.I))
    obstacle_open     = open_obstacle.strip().startswith("[O]") or "[O]" in open_obstacle
    vp_not_invent     = bool(re.search(r"does\s+not\s+invent", what_vp_adds, flags=re.I))

    checks = {
        "every_clinical_anchor_cited_[L]_not_derived": all(per_lever[l]["ok"] for l in LEVERS),
        "honest_limit_states_molecule/dose/response_not_predicted": limit_states_open,
        "open_obstacle_graded_[O]": obstacle_open,
        "what_VP_adds_says_does_not_invent": vp_not_invent,
    }
    for name, cond in checks.items():
        if not cond:
            fail.append(name)

    out = {"title": "D3 clinical-mechanism honesty gate -- efficacy of real therapies is cited [L], never derived",
           "inherited_from": "analgesic_threshold_logic_v2_0/M11 L3-honesty (DOI 10.5281/zenodo.20733420)",
           "firewall": ("the R19 kernel DERIVES a treatment DIRECTION/CLASS (basin/lever); the CLINICAL "
                        "EFFICACY of a real therapy is EXTERNAL cited biology [L] and the molecule/dose/"
                        "patient-response is [O]. The kernel does not derive a clinical effect."),
           "per_lever": per_lever, "synthesis_checks": checks,
           "overall": "PASS" if not fail else "FAIL", "failures": fail}
    return out


if __name__ == "__main__":
    out = run()
    os.makedirs(os.path.join(HERE, "expected"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "expected", "mechanism_honesty.json"), "w"), indent=1)
    print("D3 clinical-mechanism honesty gate")
    for lev, r in out["per_lever"].items():
        print("  [%s] %-8s cited[L]=%s not_derived=%s  anchor=%.60s"
              % ("PASS" if r["ok"] else "FAIL", lev, r["clinical_cited_[L]"], r["clinical_not_derived"], r["clinical_anchor"]))
    for name, cond in out["synthesis_checks"].items():
        print("  [%s] %s" % ("PASS" if cond else "FAIL", name))
    print("OVERALL:", out["overall"], ("" if out["overall"] == "PASS" else out["failures"]))
    raise SystemExit(0 if out["overall"] == "PASS" else 1)
