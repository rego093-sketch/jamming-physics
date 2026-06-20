#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
explain_disease.py  --  render ONE disease's emergence read in plain language,
                        with the simulation disclaimer ALWAYS printed FIRST.

This is the human-facing front door to a `diseases/<slug>/analysis.json`. By the
author's rule the disclaimer banner is emitted at the VERY TOP, BEFORE any
explanation, so a reader cannot reach the disease content without first seeing
that this is a DNA-emergence COMPUTER SIMULATION that may differ from reality and
is not medical advice.

It is READ-ONLY over the frozen `analysis.json` artifacts (and imports the single
-source disclaimer from `disclaimer_banner.py`), so it perturbs NO determinism
hash.

CLI:
    python3 pipeline/explain_disease.py cystic_fibrosis
    python3 pipeline/explain_disease.py atypical_hemolytic_uremic_syndrome
    python3 pipeline/explain_disease.py --all          # every disease, banner-first each
    python3 pipeline/explain_disease.py mccune_albright_syndrome   # a SUSPENDED hold
"""
import os, sys, json, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")
sys.path.insert(0, HERE)
from disclaimer_banner import banner  # noqa: E402  (single source of truth)

RULE = "-" * 78


def _load(slug):
    p = os.path.join(DISEASES, slug, "analysis.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p))


def explain(slug):
    a = _load(slug)
    if a is None:
        print(f"[no such disease artifact: {slug}]")
        return

    # 1) DISCLAIMER FIRST -- always, before any explanation.
    print(banner())
    print()

    name = a.get("disease", slug)
    omim = a.get("omim", "?")
    status = a.get("status", "?")
    print(f"DISEASE : {name}")
    print(f"OMIM    : {omim}    STATUS: {status}")
    print(RULE)

    # 2) SUSPENDED holds: state the honest reason, then stop.
    if status == "SUSPENDED":
        print("This disease is HELD (SUSPENDED), not interpreted.")
        print("이 질병은 해석을 '보류'한 사례입니다 (분석하지 않았습니다).")
        print()
        reason = a.get("suspended_reason", "(no reason recorded)")
        for line in _para(reason):
            print(line)
        print()
        print("Why a hold and not a guess: the kit reads a single-gene PROMOTER")
        print("switch from the INHERITED reference DNA. When the cause is not")
        print("readable that way, it is disclosed as a hold rather than forced.")
        print(RULE)
        _closing()
        return

    # 3) RESOLVED: the emergence read + the forced corrective DIRECTION.
    em = a.get("emergence", {})
    print("WHAT THE SIMULATION READS (structure, [V]):")
    print(f"  emergent axis : {em.get('emergent_axis','?')}")
    for g in em.get("per_gene", []):
        print(f"  gene {g.get('gene','?')}: role={g.get('role','?')}, "
              f"mechanism={g.get('disease_mechanism','?')}, "
              f"\u03b3={g.get('gamma','?')}  ->  axis perturbed "
              f"{g.get('perturbation_direction','?')}")
        if g.get("note"):
            print(f"      ({g['note']})")
    ps = em.get("primary_switch", {})
    if ps:
        print(f"  PRIMARY switch: {ps.get('gene','?')} "
              f"({ps.get('role','?')}/{ps.get('mechanism','?')}) "
              f"-> emergent axis {ps.get('emergent_axis_direction','?')}")
    print()

    tA = a.get("treatment_A_switch", {}) or {}
    print("THE DIRECTION THE MODEL FORCES (corrective, [F]):")
    print(f"  pathology axis : {tA.get('pathology_axis_direction','?')}   "
          f"-> corrective axis : {tA.get('corrective_axis_direction','?')}")
    lead = tA.get("lead_corrective_lever")
    if lead:
        print(f"  LEAD lever     : {lead.get('lever','?')} -> "
              f"{lead.get('target_gene','?')}")
        print(f"  agent class    : {lead.get('agent_class','?')}")
        print(f"  approval status: {lead.get('status','?')}  "
              f"(this is real-world status, NOT a claim the kit makes)")
        print(f"  magnitude      : {lead.get('mechanism_grade','[O]')}")
        # honest directness note
        causal = {g.get('gene') for g in em.get('per_gene', [])}
        directness = ("DIRECT (acts on the causal gene)"
                      if lead.get("target_gene") in causal else
                      "INDIRECT (acts off the causal gene, downstream/upstream)")
        print(f"  directness     : {directness}")
    others = [l for l in tA.get("levers", []) if l is not lead]
    if others:
        print("  other candidate directions (each direction-only, magnitude [O]):")
        for l in others:
            print(f"    - {l.get('lever','?')} {l.get('target_gene','?')} "
                  f"[{l.get('status','?')}]: {l.get('agent_class','?')}")
    print()

    fs = a.get("falsifiers", [])
    if fs:
        print("HOW THIS COULD BE PROVEN WRONG (a falsifier):")
        f0 = fs[0]
        print(f"  claim    : {f0.get('claim','?')}")
        print(f"  falsifier: {f0.get('falsifier','?')}")
        print(f"  testable : {f0.get('measurable_by','?')}")
    print(RULE)
    _closing()


def _para(text, width=78):
    out, line = [], ""
    for word in text.split():
        if len(line) + 1 + len(word) > width:
            out.append(line)
            line = word
        else:
            line = (line + " " + word).strip()
    if line:
        out.append(line)
    return out


def _closing():
    print("REMINDER / 다시 강조: 이것은 DNA 창발 컴퓨터 시뮬레이션이며 현실과")
    print("다를 수 있습니다. 의료 조언이 아닙니다 \u2014 반드시 주치의와 상의하세요.")
    print("This was a DNA-emergence computer simulation that may differ from")
    print("reality. Not medical advice \u2014 please consult your physician.")


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("-")]
    if "--all" in sys.argv:
        slugs = sorted(os.path.basename(os.path.dirname(p))
                       for p in glob.glob(os.path.join(DISEASES, "*", "analysis.json")))
    elif args:
        slugs = args
    else:
        print("usage: explain_disease.py <slug> [<slug> ...] | --all")
        sys.exit(2)
    for i, slug in enumerate(slugs):
        if i:
            print("\n" + "=" * 78 + "\n")
        explain(slug)


if __name__ == "__main__":
    main()
