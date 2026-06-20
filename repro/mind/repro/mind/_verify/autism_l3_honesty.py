#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
autism_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11 via the
bipolar/epilepsy/depression/schizophrenia T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. The autism L3 axis is SPARSE:
unlike depression (HPA/monoamine, L3-dominant) or schizophrenia (dopamine, L3 co-dominant), autism has
NO clean up-stream pharmacological drive that sets the E/I operating point -- only a SINGLE serotonergic
[O] handle (SLC6A4; hyperserotonemia, the oldest ASD biomarker, but an indirect/non-monotone link to the
cortical E/I fold). For that one node, the map may read the gene's threshold structure and PLACE it, but
it MUST grade the MECHANISM LINK as cited-biology [O], never as a derived mechanism. This gate enforces
that, and the autism-specific structure:

  - autism is L1-DOMINANT with a NEARLY-EMPTY L3 (NOT co-dominant like schizophrenia, NOT L3-dominant
    like depression). The gate checks L1 is the UNIQUE largest lever and L3 is sparse (<=1).
  - the DOMAIN-RESTRICTION is the T (E/I-excess) axis ONLY; the O (synaptic-gain/output) and W (long-
    range wiring) axes are NOT reached. The gate enforces this AND the autism-specific strengthenings:
      * the unreachable axes are NAMED (out_of_reach_targets present, with real genes on O and on W);
      * the W unreachability is cited to sec.19 (autism_candidate_limits PROVED a threshold lever masks-
        but-cannot-correct the W fault).

Gate (fail-closed):
  - the single L3 entry carries grade_mechanism beginning with "[O]"; is not presented as derived
    ([V]/[F]); carries a non-empty citation; is not mislabelled as an ion channel (channel=None);
  - the declared L3 set (the serotonergic handle) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the sec.18 network over-excitation fold;
  - L1 is the UNIQUE dominant lever and L3 is sparse (autism's distribution, NOT co-dominant/L3-dominant);
  - the domain-restriction witness records T=reached, O=not, W=not;
  - the out_of_reach_targets are NAMED (>=1 gene on the O axis AND >=1 on the W axis), and the W
    unreachability cites sec.19.

Run:  python3 autism_l3_honesty.py  -> autism_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "autism_threshold_levers_results.json")

DECLARED_L3 = {"SLC6A4"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (autism)")

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
check("no L3 serotonergic node mislabelled as an ion channel", chan_misclass == [])

# autism-specific: the promoter |h_sp| must NOT be equated with the sec.18 network E/I fold
op_guard = all(e.get("grade_promoter_vs_network_threshold", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the sec.18 network over-excitation fold", op_guard)

# autism-specific: L1 must be the UNIQUE dominant lever and L3 must be SPARSE (not co-dominant/L3-dominant)
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
l1_unique_dominant = (counts.get("L1", 0) == maxn) and \
                     (sum(1 for v in counts.values() if v == maxn) == 1) and \
                     (max(counts, key=lambda k: counts[k]) == "L1")
l3_sparse = counts.get("L3", 0) <= 1
check(f"L1 is the UNIQUE dominant lever (autism's distribution; counts={counts})", l1_unique_dominant)
check(f"L3 is SPARSE (<=1 target; counts L3={counts.get('L3', 0)})", l3_sparse)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=False, dominant_levers=[L1], l3_sparse=True",
      ldw.get("codominant") is False and ldw.get("dominant_levers", []) == ["L1"]
      and ldw.get("l3_sparse") is True)

# autism-specific: the DOMAIN-RESTRICTION must be recorded (T only)
drw = m.get("domain_restriction_witness", {})
t_ok = drw.get("T", {}).get("reached_by_levers") is True
o_ok = drw.get("O", {}).get("reached_by_levers") is False
w_ok = drw.get("W", {}).get("reached_by_levers") is False
check("domain-restriction witness records T=reached, O=NOT, W=NOT", t_ok and o_ok and w_ok)

# autism-specific: the out-of-reach targets must be NAMED (>=1 gene on O AND >=1 on W)
oor = m.get("out_of_reach_targets", {})
oor_by_axis = oor.get("by_axis", {})
named_O = len(oor_by_axis.get("O", [])) >= 1
named_W = len(oor_by_axis.get("W", [])) >= 1
oor_all_not_reached = all(e.get("reached_by_threshold_levers") is False for e in oor.get("entries", []))
check("out-of-reach targets NAMED (>=1 gene on the O axis AND >=1 on the W axis), all flagged NOT REACHED",
      named_O and named_W and oor_all_not_reached and len(oor.get("entries", [])) >= 2)

# autism-specific: the W unreachability must cite sec.19 (the chemical-reach-limit proof)
cites = (drw.get("cites", "") + " " + drw.get("W", {}).get("why_not", "")).lower()
check("W unreachability cites sec.19 (autism_candidate_limits, the chemical-reach-limit proof)",
      "sec.19" in cites and ("candidate_limits" in cites or "chemical-reach" in cites or "chemical reach" in cites))

result = {
    "title": ("L3 honesty pass (autism) -- the single serotonergic [O] handle (L3-sparse); L1 the UNIQUE "
              "dominant lever; T-axis restricted; O/W axes NAMED out-of-reach and W proven in sec.19"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression/schizophrenia T-L gates"),
    "principle": ("gamma reads promoter threshold structure; the L3 serotonergic (SLC6A4) signalling "
                  "mechanism is NOT captured and is graded cited-biology [O] (and is indirect/non-monotone). "
                  "The promoter |h_sp| is held distinct from the sec.18 network over-excitation fold; L1 is "
                  "verified the UNIQUE dominant lever and L3 verified SPARSE (autism's fifth distribution "
                  "pattern -- L1-dominant, nearly-empty L3); and the lever map is verified to reach the T "
                  "(E/I-excess) axis ONLY, with the O (synaptic-gain/output) and W (long-range wiring) axes "
                  "NAMED out-of-reach (real genes, real citations) and the W unreachability PROVEN in sec.19."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "l1_unique_dominant": l1_unique_dominant, "l3_sparse": l3_sparse,
    "domain_restriction": {"T_reached": t_ok, "O_reached": not o_ok, "W_reached": not w_ok},
    "out_of_reach_named": {"O_axis_genes": oor_by_axis.get("O", []), "W_axis_genes": oor_by_axis.get("W", []),
                           "W_unreachability_proven_sec19": ("sec.19" in cites)},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "autism_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
