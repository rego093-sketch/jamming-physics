#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
counterreg_honesty.py  --  IV counter-regulation honesty gate (fail-closed).

The hemodynamic analogue of analgesic_threshold_logic v2.0's M11 L3-honesty gate (Zenodo concept DOI
10.5281/zenodo.20733420). The comfort map may read the PROVEN loop direction (RP4 reject / T1 durable)
and PLACE each axis in the lever frame -- that placement is [V] structural. But the PER-AXIS MOLECULAR
mechanism (which receptor / transporter / channel, and its pharmacology) is NOT captured by the loop
read and must be graded cited-biology [O], never as a derived mechanism. This gate enforces exactly
that, axis by axis, so the "counter-regulation-free comfort" framing never masquerades as derived
pharmacology.

Gate (fail-closed):
  - every comfort-map axis carries grade_mechanism beginning with "[O]" (molecular link is cited);
  - none presents the molecular mechanism as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the lever placement grade is [V] structural-from-the-proven-loop (read, not assumed);
  - the DNA-grounded axes (REN, SIX2) carry a measured gamma (provenance), and that gamma is NOT
    presented as the comfort mechanism;
  - the map's firewall text states the molecular mechanism link is [O] and not derived, and that
    'counter-regulation-free' is structural, not a safety/tolerability claim.

Run:  python3 counterreg_honesty.py  -> expected/counterreg_honesty.json ; exit 1 on any violation
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(HERE, "expected", "comfort_map.json")

def run():
    FAIL = []
    def check(name, cond):
        if not cond:
            FAIL.append(name)
        return cond

    m = json.load(open(MAP, encoding="utf-8"))
    entries = {e["axis"]: e for e in m["entries"]}

    # 1) every axis's molecular mechanism link is [O], not derived, and cited
    per_axis = {}
    for axis, e in sorted(entries.items()):
        gm = e.get("grade_mechanism", "")
        is_open = gm.strip().startswith("[O]")
        not_derived = not (gm.strip().startswith("[V]") or gm.strip().startswith("[F]"))
        cited = bool(e.get("src", "").strip())
        ok = is_open and not_derived and cited
        per_axis[axis] = {"grade_mechanism": gm, "open": is_open, "not_derived": not_derived,
                          "cited": cited, "ok": ok}
    check("every axis molecular mechanism graded [O] cited-biology (not derived), with citation",
          all(v["ok"] for v in per_axis.values()))

    # 2) the lever placement grade is [V] structural read off the proven loop
    lever_ok = all(e.get("grade_lever", "").strip().startswith("[V]") for e in entries.values())
    check("every lever placement graded [V] structural-from-the-proven-loop", lever_ok)

    # 3) the DNA-grounded axes carry a measured gamma, but gamma is NOT the comfort mechanism
    dna_axes = {a: e for a, e in entries.items() if e.get("dna_grounded")}
    dna_gamma_ok = all(e.get("measured_gamma") is not None for e in dna_axes.values())
    gamma_not_mechanism = all(not e.get("grade_mechanism", "").strip().startswith("[V]")
                              for e in dna_axes.values())
    check("DNA-grounded axes carry a measured gamma (provenance), gamma NOT presented as the mechanism",
          bool(dna_axes) and dna_gamma_ok and gamma_not_mechanism)

    # 4) the map firewall states the molecular link is [O]/not-derived AND counter-reg-free is structural
    fw = m.get("firewall", "").lower()
    fw_ok = (("[o]" in fw) and ("never derived" in fw or "not derived" in fw)
             and ("structural" in fw) and ("safety" in fw or "tolerability" in fw))
    check("map firewall states molecular link is [O]/not-derived and 'counter-regulation-free' is structural",
          fw_ok)

    # 5) no axis presents an asserted safety/tolerability/efficacy outcome (clinical map [O])
    clinmap_open = all(e.get("grade_clinical_map", "").strip().startswith("[O]") for e in entries.values())
    check("every axis's clinical map graded [O] (no asserted safety/tolerability/efficacy)", clinmap_open)

    result = {
        "title": "Counter-regulation honesty pass -- molecular mechanism graded [O], never derived",
        "imported_from": "analgesic_threshold_logic v2.0 M11 (Zenodo concept DOI 10.5281/zenodo.20733420)",
        "principle": ("the loop read PLACES each axis in the lever frame ([V] structural from RP4/T1); the "
                      "per-axis receptor/transporter/channel pharmacology is NOT captured by the read and is "
                      "graded cited-biology [O]. 'Counter-regulation-free' is structural, not a safety claim."),
        "axes_in_map": sorted(entries.keys()),
        "dna_grounded_axes": sorted(dna_axes.keys()),
        "per_axis": per_axis,
        "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
    }
    return result


if __name__ == "__main__":
    r = run()
    json.dump(r, open(os.path.join(HERE, "expected", "counterreg_honesty.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("IV counter-regulation honesty pass")
    for a in r["axes_in_map"]:
        print("    axis %-26s -> %s" % (a, r["per_axis"][a]["grade_mechanism"][:64]))
    print("OVERALL:", r["overall"], "" if r["overall"] == "PASS" else r["failures"])
    raise SystemExit(0 if r["overall"] == "PASS" else 1)
