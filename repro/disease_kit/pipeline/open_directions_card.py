#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
open_directions_card.py  --  ACTIONABLE OPEN-DIRECTIONS cards for the no-approved tail.  [NATIVE, ROADMAP III-A]

  *** NATIVE to the VP Disease Emergence Kit (not inherited).  This is the kit's ROADMAP III-A
      output: it takes the diseases that have NO approved therapy on their lead axis -- the part of
      the pond where the stone is supposed to sink -- and renders each one as a single, self-contained,
      ACTIONABLE card a researcher or sponsor can actually pick up:

          disease  ->  emergent axis  ->  [F]-forced corrective direction
                   ->  candidate drug CLASS (from the repurposing scanner, if a same-axis approved
                       donor exists; honestly NULL if the direction is an orphan)
                   ->  the CHEAPEST falsification experiment that would kill the direction
                   ->  [O] grade + lead clinical status.

      The bare forced direction is often already obvious to a specialist; what makes the direction
      ACTIONABLE is (a) a concrete candidate class to test, and (b) the single cheapest experiment
      that would refute it.  Both are taken from FROZEN artifacts -- the scanner's frozen hypotheses
      and each disease's own frozen falsifier -- so nothing here is fabricated. ***

INPUTS (all FROZEN, READ-ONLY -- this module perturbs no per-disease hash):
  - repro/modules/expected/repurposing_hypotheses.json   (the III-A2 scanner output: the recipient/
                                                           orphan partition + candidate agent classes)
  - diseases/<slug>/analysis.json                          (per disease: the CORRECTIVE-direction
                                                           falsifier's `measurable_by` = cheapest expt)

  The recipient/orphan partition is taken verbatim from the scanner (single source of truth); the
  cheapest experiment is the `measurable_by` of the UNIQUE falsifier whose claim names the CORRECTIVE
  direction (verified to be exactly one per tail disease).  No experiment is invented.

FIREWALL (strict -- ROADMAP III-A):  DIRECTION + CANDIDATE CLASS + FALSIFIER ONLY.  Never dose,
  potency, efficacy, response rate, or a specific-product efficacy claim.  Every card carries an [O]
  grade for all magnitude / efficacy, the [F]-forced direction, and -- for recipients -- the scanner's
  "same-axis != same-disease" caveat.  A card with no cheapest-falsification experiment FAILS the gate
  (an un-falsifiable "direction" is not actionable).  This JSON is a MACHINE artifact; the human-facing
  rendering is the HTML site, which is responsible for emitting the patient-facing disclaimer banner.

USAGE:
  python3 pipeline/open_directions_card.py            # build + self-test + gate, print summary
  python3 pipeline/open_directions_card.py --write    # also freeze open_directions_cards.json
  python3 pipeline/open_directions_card.py --selftest  # teeth only (exit 0/1) -- for run_modules
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DISEASES = os.path.join(ROOT, "diseases")
SCANNER_OUT = os.path.join(ROOT, "repro", "modules", "expected", "repurposing_hypotheses.json")

FAIL = []


def check(name, cond):
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {name}")
    if not cond:
        FAIL.append(name)
    return cond


def _corrective_experiment(slug):
    """The cheapest falsification experiment = `measurable_by` of the UNIQUE falsifier whose claim
    names the CORRECTIVE direction.  Verified exactly one such falsifier exists per tail disease;
    if that invariant ever breaks (0 or >1), return None so the gate fails closed."""
    a = json.load(open(os.path.join(DISEASES, slug, "analysis.json")))
    corr = [f for f in a.get("falsifiers", []) if "CORRECTIVE" in (f.get("claim") or "")]
    if len(corr) != 1:
        return None, len(corr)
    f = corr[0]
    expt = f.get("measurable_by") or f.get("falsifier")
    return (expt or None), 1


def build():
    """Assemble one actionable card per no-approved-tail disease from the FROZEN scanner output +
    each disease's frozen corrective-direction falsifier."""
    del FAIL[:]
    scan = json.load(open(SCANNER_OUT))

    recipients = scan["repurposing_hypotheses"]      # diseases WITH a same-axis approved donor
    orphans = scan["orphan_directions_no_donor"]     # diseases with NO same-axis approved donor
    no_approved = set(scan["no_approved_lead"])      # the full tail (single source of truth)

    cards = []

    # ---- recipient cards: a candidate CLASS exists (from a same-axis approved donor) ----
    for h in recipients:
        slug = h["recipient"]
        expt, n_corr = _corrective_experiment(slug)
        # flatten donor -> classes, preserving attribution, de-duplicated, order-stable
        candidates = []
        seen = set()
        for d in h["donors"]:
            for cls in d["approved_agent_class"]:
                key = (cls, d["donor"])
                if key not in seen:
                    seen.add(key)
                    candidates.append({"agent_class": cls, "approved_for_donor": d["donor"]})
        cards.append({
            "slug": slug,
            "disease": json.load(open(os.path.join(DISEASES, slug, "analysis.json")))["disease"],
            "kind": "repurposing_candidate",
            "emergent_axis": h["recipient_axis"],
            "forced_corrective_direction": h["shared_corrective_direction"],
            "lead_lever_class": h["shared_lever_class"],
            "lead_clinical_status": h["recipient_lead_status"],
            "candidate_drug_classes": candidates,                # >=1 (gate-enforced)
            "shared_axis_family": h["shared_axis_family"],
            "cheapest_falsification_experiment": expt,
            "novelty": h["novelty"],
            "grade": "[F] corrective direction forced + cited ; [O] candidate-class efficacy / dose / "
                     "repurposing-success NOT asserted",
            "honesty_caveat": h["honesty_caveat"],
            "_n_corrective_falsifiers": n_corr,
        })

    # ---- orphan cards: forced direction stands, but NO same-axis approved donor to repurpose ----
    for o in orphans:
        slug = o["slug"]
        expt, n_corr = _corrective_experiment(slug)
        cards.append({
            "slug": slug,
            "disease": json.load(open(os.path.join(DISEASES, slug, "analysis.json")))["disease"],
            "kind": "orphan_direction",
            "emergent_axis": o["axis"],
            "forced_corrective_direction": o["corrective_direction"],
            "lead_lever_class": o["lead_lever"],
            "lead_clinical_status": o["lead_status"],
            "candidate_drug_classes": [],                        # honestly empty (gate-enforced)
            "shared_axis_family": o["axis_family"],
            "cheapest_falsification_experiment": expt,
            "novelty": "orphan-direction (no same-axis approved donor exists to repurpose from -- the "
                       "[F] direction is the actionable claim; the cheapest experiment below would "
                       "refute it)",
            "grade": "[F] corrective direction forced + cited ; [O] no candidate class asserted "
                     "(no same-axis approved donor)",
            "honesty_caveat": o["why_orphan"],
            "_n_corrective_falsifiers": n_corr,
        })

    cards.sort(key=lambda c: c["slug"])

    # ---------------------------- fail-closed gate ----------------------------
    card_slugs = [c["slug"] for c in cards]
    check("one card per no-approved-tail disease, partitioning the scanner's tail exactly "
          f"({len(no_approved)} tail; {len(card_slugs)} cards)",
          set(card_slugs) == no_approved and len(card_slugs) == len(no_approved))

    check("every card carries slug / disease / emergent_axis / forced_corrective_direction",
          all(c.get("slug") and c.get("disease") and c.get("emergent_axis")
              and c.get("forced_corrective_direction") in ("UP", "DOWN") for c in cards))

    check("every card has a non-empty CHEAPEST-FALSIFICATION experiment (actionable = falsifiable)",
          all(isinstance(c.get("cheapest_falsification_experiment"), str)
              and c["cheapest_falsification_experiment"].strip() for c in cards))

    check("exactly one corrective-direction falsifier underlies each card (frozen-data invariant)",
          all(c.get("_n_corrective_falsifiers") == 1 for c in cards))

    rec_cards = [c for c in cards if c["kind"] == "repurposing_candidate"]
    orp_cards = [c for c in cards if c["kind"] == "orphan_direction"]
    check("every REPURPOSING card carries >=1 candidate drug class with donor attribution",
          all(c["candidate_drug_classes"]
              and all(d.get("agent_class") and d.get("approved_for_donor")
                      for d in c["candidate_drug_classes"]) for c in rec_cards))
    check("every ORPHAN card honestly carries NO candidate drug class (empty)",
          all(c["candidate_drug_classes"] == [] for c in orp_cards))

    check("every card carries an [O] firewall grade and an honesty caveat",
          all("[O]" in c.get("grade", "") and c.get("honesty_caveat") for c in cards))

    # strip the private bookkeeping field from the frozen artifact
    for c in cards:
        c.pop("_n_corrective_falsifiers", None)

    result = {
        "title": "Open-directions cards -- the no-approved-therapy tail rendered as actionable, "
                 "falsifiable corrective-direction hypotheses",
        "native_to": "vp_disease_emergence_kit (ROADMAP III-A); read-only over the frozen III-A2 "
                     "scanner output + each disease's frozen corrective-direction falsifier",
        "principle": "a disease with no approved therapy is only ACTIONABLE if the forced corrective "
                     "direction comes with (a) a concrete candidate drug CLASS to test -- supplied by "
                     "the repurposing scanner when a same-axis approved donor exists, honestly NULL "
                     "otherwise -- and (b) the single CHEAPEST experiment that would refute the "
                     "direction.  Both are read from frozen artifacts; nothing is invented.",
        "firewall": "DIRECTION + CANDIDATE CLASS + FALSIFIER ONLY; never dose, potency, efficacy, "
                    "response rate, or a specific-product efficacy claim; every card is [O] for "
                    "magnitude + [F] for the cited direction; a card with no falsification experiment "
                    "fails the gate; read-only, perturbs no per-disease hash.  Machine artifact -- the "
                    "HTML site carries the patient-facing disclaimer.",
        "grade": "[F] corrective direction forced + cited ; [O] all magnitude / efficacy / "
                 "candidate-class success",
        "n_cards": len(cards),
        "n_repurposing_candidate": len(rec_cards),
        "n_orphan_direction": len(orp_cards),
        "cards": cards,
        "overall": "PASS" if not FAIL else "FAIL",
        "failures": list(FAIL),
    }
    return result


def selftest():
    """Prove the card builder has TEETH on its two firewall predicates:
       (1) a repurposing card MUST carry >=1 candidate class AND a non-empty cheapest experiment;
       (2) an orphan card MUST carry NO candidate class but STILL a non-empty cheapest experiment;
       (3) a card missing the cheapest experiment is REJECTED (un-falsifiable = not actionable);
       (4) a repurposing card with an empty candidate-class list is REJECTED."""
    def card_ok(card):
        has_expt = isinstance(card.get("cheapest_falsification_experiment"), str) \
            and bool(card["cheapest_falsification_experiment"].strip())
        if card["kind"] == "repurposing_candidate":
            has_cls = bool(card.get("candidate_drug_classes"))
            return has_expt and has_cls
        if card["kind"] == "orphan_direction":
            no_cls = (card.get("candidate_drug_classes") == [])
            return has_expt and no_cls
        return False

    good_rec = {"kind": "repurposing_candidate",
                "candidate_drug_classes": [{"agent_class": "X-lowering ASO", "approved_for_donor": "y"}],
                "cheapest_falsification_experiment": "measure axis in model"}
    good_orp = {"kind": "orphan_direction",
                "candidate_drug_classes": [],
                "cheapest_falsification_experiment": "measure axis in model"}
    bad_no_expt = {"kind": "orphan_direction",
                   "candidate_drug_classes": [],
                   "cheapest_falsification_experiment": "   "}
    bad_rec_no_cls = {"kind": "repurposing_candidate",
                      "candidate_drug_classes": [],
                      "cheapest_falsification_experiment": "measure axis in model"}

    p_rec = card_ok(good_rec)
    p_orp = card_ok(good_orp)
    r_expt = not card_ok(bad_no_expt)
    r_cls = not card_ok(bad_rec_no_cls)
    ok = p_rec and p_orp and r_expt and r_cls
    print("  [self-test] card teeth:",
          f"repurposing(accept)={p_rec}  orphan(accept)={p_orp}  "
          f"no-experiment(reject)={r_expt}  repurposing-no-class(reject)={r_cls}  "
          f"-> {'OK' if ok else 'BROKEN'}")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    teeth_ok = selftest()
    res = build()
    if not teeth_ok:
        res["overall"] = "FAIL"
        res.setdefault("failures", []).append("self-test: card predicate is broken")
    if "--write" in sys.argv:
        p = os.path.join(ROOT, "repro", "modules", "expected", "open_directions_cards.json")
        json.dump(res, open(p, "w"), indent=1)
        print(f"  wrote {os.path.relpath(p, ROOT)}")
    print("Open-directions cards  [NATIVE / ROADMAP III-A]")
    print(f"  cards={res['n_cards']}  repurposing-candidate={res['n_repurposing_candidate']}  "
          f"orphan-direction={res['n_orphan_direction']}")
    for c in res["cards"]:
        if c["kind"] == "repurposing_candidate":
            cls = ", ".join(sorted({d["agent_class"] for d in c["candidate_drug_classes"]}))
            print(f"    [{c['forced_corrective_direction']}|{c['lead_lever_class']}] {c['slug']}  "
                  f"-> candidate: {cls}")
        else:
            print(f"    [{c['forced_corrective_direction']}|{c['lead_lever_class']}] {c['slug']}  "
                  f"-> ORPHAN (no same-axis approved donor)")
    print(f"OVERALL: {res['overall']}")
    sys.exit(0 if res["overall"] == "PASS" and teeth_ok else 1)
