#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
l3_honesty.py  —  M11 (v2): the L3 honesty gate (fail-closed).

The framework reads PERIPHERAL promoter threshold structure best. The L3 axis (NGF/TrkA and the
CGRP system) and any central-sensitisation note involve RECEPTOR SIGNALLING and NETWORK GAIN that
the gamma read does NOT capture. For those, the framework may read the gene's threshold structure
and PLACE it in the lever map, but it must grade the MECHANISM LINK as cited-biology [O], never as
a derived mechanism. This gate enforces exactly that, target by target.

Gate (fail-closed):
  - every threshold-map entry with lever == "L3" carries grade_mechanism beginning with "[O]";
  - none is presented as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the declared L3 set (NGF + CGRP axis + TrkA) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O].

Run:  python3 l3_honesty.py   -> expected/l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.normpath(os.path.join(HERE, "..", "03-threshold-map", "expected", "threshold_map.json"))

# the L3 axes that MUST be graded as cited-biology [O] (not derived):
DECLARED_L3 = {"NGF", "NTRK1", "CALCA", "CALCB", "CALCRL", "RAMP1"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("M11 L3 honesty pass")

# 1) every L3 entry's mechanism link is [O], not derived, and cited
per_target = {}
for g, e in sorted(l3.items()):
    gm = e.get("grade_mechanism", "")
    is_open    = gm.strip().startswith("[O]")
    not_derived = not (gm.strip().startswith("[V]") or gm.strip().startswith("[F]"))
    cited      = bool(e.get("src", "").strip())
    ok = is_open and not_derived and cited
    per_target[g] = {"grade_mechanism": gm, "open": is_open, "not_derived": not_derived,
                     "cited": cited, "ok": ok}
    if not ok:
        print(f"    [FAIL] {g}: open={is_open} not_derived={not_derived} cited={cited}  gm={gm!r}")
check("every L3 target graded [O] cited-biology (not a derived mechanism), with citation",
      all(v["ok"] for v in per_target.values()))

# 2) the declared L3 set is present and all routed through the L3-honesty grade
present = DECLARED_L3 & set(l3.keys())
check(f"declared L3 set present in map ({sorted(present)})", present == DECLARED_L3)

# 3) the map firewall explicitly states the L3 mechanism link is [O]
fw = m.get("firewall", "").lower()
check("map firewall states L3 mechanism link is [O]",
      ("l3" in fw) and ("[o]" in fw) and ("not derive" in fw or "does not derive" in fw))

# 4) no L3 target appears in the channels_present list as if it were an ion-channel read
#    (NGF/CGRP are ligands/receptors/RAMP, not channels — they must carry protein, channel=None)
chan_misclass = [g for g, e in l3.items() if e.get("channel") is not None]
check("no L3 ligand/receptor mislabelled as an ion channel", chan_misclass == [])

result = {
    "title": "L3 honesty pass — NGF/CGRP mechanism link graded [O], never derived",
    "principle": ("gamma reads peripheral promoter threshold structure; the L3 receptor/network "
                  "mechanism is NOT captured by the read and is graded cited-biology [O]."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "expected", "l3_honesty.json"), "w"), indent=1)

for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:70]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
