#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bipolar_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11.

The framework reads PERIPHERAL/promoter switch-threshold structure best. The bipolar L3 axis
(circadian: ARNTL/CLOCK/PER2; HPA: NR3C1/CRHR1; and lithium's node GSK-3beta) involves RECEPTOR
SIGNALLING, NETWORK GAIN and CLOCK DYNAMICS that the gamma read does NOT capture. For those, the
map may read the gene's threshold structure and PLACE it in the lever map, but it MUST grade the
MECHANISM LINK as cited-biology [O], never as a derived mechanism. This gate enforces exactly
that, target by target.

Gate (fail-closed):
  - every threshold-map entry with lever == "L3" carries grade_mechanism beginning with "[O]";
  - none is presented as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the declared L3 set (circadian + HPA + GSK-3beta) is present and all-[O];
  - no L3 entry is mislabelled as an ion channel (they are TFs / receptors / kinase: channel=None);
  - the map's firewall text states the L3 mechanism link is [O].

Run:  python3 bipolar_l3_honesty.py   -> bipolar_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "bipolar_threshold_levers_results.json")

DECLARED_L3 = {"ARNTL", "CLOCK", "PER2", "NR3C1", "CRHR1", "GSK3B"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (bipolar)")

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
check(f"declared L3 set present ({sorted(present)})", present == DECLARED_L3)

fw = m.get("firewall", "").lower()
check("map firewall states L3 mechanism link is [O]",
      ("l3" in fw) and ("[o]" in fw) and ("not derive" in fw or "does not derive" in fw))

chan_misclass = [g for g, e in l3.items() if e.get("channel") is not None]
check("no L3 circadian/HPA/kinase node mislabelled as an ion channel", chan_misclass == [])

# bipolar-specific: the promoter |h_sp| must NOT be equated with the network mood fold
fold_guard = all(e.get("grade_promoter_vs_mood_fold", "").strip().startswith("[O]")
                 for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the sec.29 network mood-switch barrier", fold_guard)

result = {
    "title": "L3 honesty pass (bipolar) -- circadian/HPA/GSK-3beta mechanism link graded [O], never derived",
    "inherited_from": "analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420)",
    "principle": ("gamma reads promoter threshold structure; the L3 circadian/HPA/kinase mechanism is NOT "
                  "captured by the read and is graded cited-biology [O]. Additionally the promoter |h_sp| is "
                  "held distinct from the network mood-switch barrier g of sec.29."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "bipolar_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
