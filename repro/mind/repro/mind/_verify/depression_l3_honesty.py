#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
depression_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11
via the bipolar/epilepsy T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. The depression L3 axis is
the DOMINANT lever and the most signalling-heavy: it spans the HPA stress axis (NR3C1/CRHR1/FKBP5),
the monoaminergic drives (SLC6A4/SLC6A2/MAOA/TPH2/HTR1A/HTR2A/COMT) and the neurotrophic/plasticity
axis (BDNF/NTRK2) -- nuclear-receptor / GPCR / transporter / enzyme / neurotrophin signalling that the
gamma read does NOT capture. For those, the map may read the gene's threshold structure and PLACE it
in the lever map, but it MUST grade the MECHANISM LINK as cited-biology [O], never as a derived
mechanism. This gate enforces exactly that, target by target. (Because depression is L3-dominant, this
gate guards MORE of the map than the bipolar/epilepsy versions did -- 12 of 18 targets.)

Gate (fail-closed):
  - every threshold-map entry with lever == "L3" carries grade_mechanism beginning with "[O]";
  - none is presented as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the declared L3 set (HPA + monoamine + neurotrophic) is present and all-[O];
  - no L3 entry is mislabelled as an ion channel (they are receptors/transporters/enzymes/neurotrophins/
    TFs: channel=None);
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the sec.27 network operating-point (R below health);
  - the L3-DOMINANCE is real (L3 is the largest lever) -- the qualitative claim the chapter makes.

Run:  python3 depression_l3_honesty.py   -> depression_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "depression_threshold_levers_results.json")

DECLARED_L3 = {"NR3C1", "CRHR1", "FKBP5", "SLC6A4", "SLC6A2", "MAOA",
               "TPH2", "HTR1A", "HTR2A", "COMT", "BDNF", "NTRK2"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (depression)")

per_target = {}
for g, e in sorted(l3.items()):
    gm = e.get("grade_mechanism", "")
    is_open     = gm.strip().startswith("[O]")
    not_derived = not (gm.strip().startswith("[V]") or gm.strip().startswith("[F]"))
    cited       = bool(e.get("src", "").strip())
    ok = is_open and not_derived and cited
    per_target[g] = {"grade_mechanism": gm, "open": is_open, "not_derived": not_derived,
                     "cited": cited, "ok": ok}
    if not ok:
        print(f"    [FAIL] {g}: open={is_open} not_derived={not_derived} cited={cited}  gm={gm!r}")
check("every L3 target graded [O] cited-biology (not derived), with citation",
      all(v["ok"] for v in per_target.values()))

present = DECLARED_L3 & set(l3.keys())
check(f"declared L3 set present ({len(present)}/{len(DECLARED_L3)})", present == DECLARED_L3)

fw = m.get("firewall", "").lower()
check("map firewall states L3 mechanism link is [O]",
      ("l3" in fw) and ("[o]" in fw) and ("not derive" in fw or "does not derive" in fw))

chan_misclass = [g for g, e in l3.items() if e.get("channel") is not None]
check("no L3 HPA/monoamine/neurotrophic node mislabelled as an ion channel", chan_misclass == [])

# depression-specific: the promoter |h_sp| must NOT be equated with the network operating point
op_guard = all(e.get("grade_promoter_vs_operating_point", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the sec.27 network operating-point (R below health)", op_guard)

# depression-specific: L3 must be the DOMINANT lever (the chapter's qualitative claim)
by_lever = m.get("targets_by_lever", {})
l3_dominant = all(len(l3) >= len(v) for v in by_lever.values()) and len(l3) > 0
check(f"L3 is the dominant lever (L3={len(l3)} vs others {[len(v) for k,v in by_lever.items() if k!='L3']})",
      l3_dominant)

result = {
    "title": "L3 honesty pass (depression) -- HPA/monoamine/neurotrophic mechanism link graded [O], never derived; L3-dominant",
    "inherited_from": "analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via bipolar/epilepsy T-L gates",
    "principle": ("gamma reads promoter threshold structure; the L3 HPA(NR3C1/CRHR1/FKBP5) + monoamine(SLC6A4/"
                  "SLC6A2/MAOA/TPH2/HTR1A/HTR2A/COMT) + neurotrophic(BDNF/NTRK2) signalling mechanism is NOT captured "
                  "by the read and is graded cited-biology [O]. Additionally the promoter |h_sp| is held distinct from "
                  "the sec.27 network operating-point (the coordination level R below health), and L3 is verified to be "
                  "the DOMINANT lever (depression's qualitative difference from bipolar/epilepsy)."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": {k: len(v) for k, v in by_lever.items()},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "depression_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
