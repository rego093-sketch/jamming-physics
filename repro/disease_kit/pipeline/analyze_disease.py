#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
analyze_disease.py  --  run the FULL emergence stack for one disease (by slug).

For a RESOLVED disease:
    NCBI DNA -> emerge_disease (R19 perturbation read)
             -> treatment_switch (pathway A: corrective levers + dwell emergence)
             -> treatment_chem   (pathway B: VP-chemistry feasibility, if candidates)
             -> honesty_gate     (forbidden-claim scan + falsifier register)
    -> diseases/<slug>/analysis.json   (deterministic; the shipped artifact)

For a SUSPENDED disease:
    emit diseases/<slug>/analysis.json recording the suspension + reason (honest hold).

Run:   python3 analyze_disease.py <slug> [--offline]
       python3 analyze_disease.py --all [--offline]
"""
import os, sys, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
if HERE not in sys.path: sys.path.insert(0, HERE)

import emerge_disease as ED
import treatment_switch as TS
import treatment_chem as TC
import honesty_gate as HG

REGISTRY = os.path.join(ROOT, "diseases", "_registry.json")


def _load_registry():
    return json.load(open(REGISTRY, encoding="utf-8"))


def analyze(slug, offline=False):
    reg = _load_registry()
    spec = reg["diseases"][slug]
    out_dir = os.path.join(ROOT, "diseases", slug)
    os.makedirs(out_dir, exist_ok=True)

    if spec.get("status") == "suspended":
        rec = {
            "disease": spec["disease"], "omim": spec.get("omim"),
            "status": "SUSPENDED",
            "suspended_reason": spec["suspended_reason"],
            "discipline": "no analyzable single-gene DNA read -> held (author's rule). Disclosed, not dropped.",
        }
        rec["determinism_sha"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()[:12]
        json.dump(rec, open(os.path.join(out_dir, "analysis.json"), "w"), indent=1)
        return rec

    # 1) emerge
    em = ED.emerge_disease(spec, offline=offline)
    # 2) pathway A
    tA = TS.switch_treatment(em, spec.get("therapeutic_axes", []))
    # 3) pathway B (only if chem candidates given)
    tB = None
    if spec.get("chem_candidates"):
        tB = TC.chem_treatment(spec["disease"], spec["chem_candidates"])
    # 4) honesty gates over the artifacts we just built
    artifacts = {"emergence": em, "treatment_A": tA}
    if tB is not None: artifacts["treatment_B"] = tB
    gates = HG.run_gates(artifacts, {spec["disease"]: spec.get("falsifiers", [])})

    analysis = {
        "disease": spec["disease"], "omim": spec.get("omim"), "status": "RESOLVED",
        "emergence": em, "treatment_A_switch": tA, "treatment_B_chem": tB,
        "falsifiers": spec.get("falsifiers", []),
        "honesty_gates": gates,
    }
    analysis["determinism_sha"] = hashlib.sha256(
        json.dumps({k: v for k, v in analysis.items() if k != "determinism_sha"},
                   sort_keys=True).encode()).hexdigest()[:12]
    json.dump(analysis, open(os.path.join(out_dir, "analysis.json"), "w"), indent=1)
    return analysis


def print_summary(a):
    if a["status"] == "SUSPENDED":
        print(f"  [SUSPENDED] {a['disease']}  ({a['determinism_sha']})")
        print(f"      reason: {a['suspended_reason'][:110]}...")
        return
    em = a["emergence"]; tA = a["treatment_A_switch"]
    ps = em.get("primary_switch")
    g = "PASS" if a["honesty_gates"]["OVERALL"] == "PASS" else "FAIL"
    print(f"  [RESOLVED] {a['disease']}  (sha {a['determinism_sha']} ; gates {g})")
    if ps:
        print(f"      primary switch: {ps['gene']} ({ps['role']}/{ps['mechanism']}) "
              f"-> axis {ps['emergent_axis_direction']}  |  corrective: {tA['corrective_axis_direction']}")
    if tA.get("lead_corrective_lever"):
        L = tA["lead_corrective_lever"]
        print(f"      lead lever: {L['lever']} {L['target_gene']} via {L['agent_class']} ({L['status']})")
    if tA.get("switch_state_emergence"):
        s = tA["switch_state_emergence"]
        if s.get("axis_direction") == "UP" or "ordering_healthy_lt_treated_lt_disease" in s:
            print(f"      dwell[axis UP]: healthy {s['dwell_healthy']} < treated {s['dwell_treated']} < disease {s['dwell_disease']} "
                  f"[ordered={s.get('ordering_healthy_lt_treated_lt_disease')}]")
        else:
            print(f"      dwell: disease {s['dwell_disease']} < treated {s['dwell_treated']} < healthy {s['dwell_healthy']} "
                  f"[ordered={s['ordering_disease_lt_treated_lt_healthy']}]")
    if a.get("treatment_B_chem"):
        print(f"      pathway B: {a['treatment_B_chem']['n_candidates']} chemistry candidate(s), "
              f"{a['treatment_B_chem']['n_open_inputs']} open input(s)")
    if em.get("suspended_genes"):
        print(f"      suspended genes: {', '.join(em['suspended_genes'])}")


if __name__ == "__main__":
    offline = "--offline" in sys.argv
    if "--all" in sys.argv:
        reg = _load_registry()
        for slug in reg["diseases"]:
            a = analyze(slug, offline=offline)
            print_summary(a)
    else:
        args = [x for x in sys.argv[1:] if not x.startswith("--")]
        slug = args[0] if args else "achondroplasia"
        a = analyze(slug, offline=offline)
        print(json.dumps(a, indent=1)[:4000])
