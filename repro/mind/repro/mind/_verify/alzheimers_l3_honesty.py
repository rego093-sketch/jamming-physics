#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
alzheimers_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11 via the
bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. Alzheimer's is the THIRD PARTIAL
[L] fit in the series, and the DEEPEST -- and like addiction it is L3-DOMINANT WITH L1 AND L2 BOTH PRESENT
(not L3-ONLY like ADHD): the up-stream cholinergic DRIVE nodes load most (the cholinesterase enzymes and
the nicotinic/muscarinic receptors: ACHE, BCHE, CHRNA7, CHRM1), but the glutamatergic EXCITOTOXICITY axis
(L1: GRIN2B/GRIN2A) and the inhibitory-RESTORE / network arm (L2: GABRA1/GABRA5/GABRB3) are ALSO engaged.
For every cholinergic-drive node the map may read the gene's threshold structure and PLACE it, but it MUST
grade the acetylcholine SIGNALLING MECHANISM as cited-biology [O], never as a derived mechanism. This gate
enforces that, and the Alzheimer's-specific structure:

  - Alzheimer's is L3-DOMINANT but NOT L3-ONLY: L1 and L2 are BOTH PRESENT. The gate checks L3 is the
    UNIQUE dominant lever AND L1>0 AND L2>0 (NOT l1_l2_empty).
  - the DOMAIN-RESTRICTION reaches the SYMP (instantaneous symptomatic network operating point) axis across
    all three lever classes -- where the established AD symptomatic pharmacology acts, PURELY
    SYMPTOMATICALLY. The DOMINANT Alzheimer's fault, the PROG (neurodegenerative-progression) axis, is NOT
    reached and is NAMED out-of-reach (real genes APP/PSEN1/PSEN2/MAPT/APOE/TREM2). This is WHY the fit is
    PARTIAL [L]: the dominant axis is the out-of-reach one -- and for a DEEPER reason than addiction,
    because PROG is not a fold (the ADHD lesson) AND a PROGRESSION over time (an E0-layer DECAY variable,
    the addiction lesson) AND a DEGENERATION / cumulative LOSS (the structural inverse of addiction's E0
    GAIN).
  - the PROG axis is precisely the E0 progression-dynamics layer -- the CONVERGENCE point where threshold-
    leverisation (B-i) structurally meets the dynamics route (B-ii), as an E0 DECAY. B-i NAMES the
    trajectory out-of-reach honestly.

Gate (fail-closed):
  - every L3 entry carries grade_mechanism beginning with "[O]"; is not presented as derived
    ([V]/[F]); carries a non-empty citation; is not mislabelled as an ion channel (channel=None);
  - the declared L3 set (the four cholinergic-drive nodes) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the neurodegeneration-progression quantity;
  - L3 is the UNIQUE dominant lever AND L1>0 AND L2>0 (Alzheimer's distribution, NOT L3-only);
  - the domain-restriction witness records SYMP=reached, PROG=NOT-reached;
  - the out_of_reach_targets NAME the PROG axis (>=1 progression gene), all flagged NOT REACHED;
  - the fit is graded PARTIAL [L] (the series' THIRD non-clean fit, deepest), with reached=SYMP, oor=PROG.

Run:  python3 alzheimers_l3_honesty.py  -> alzheimers_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "alzheimers_threshold_levers_results.json")

DECLARED_L3 = {"ACHE", "BCHE", "CHRNA7", "CHRM1"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (Alzheimer's)")

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
      ("l3" in fw) and ("[o]" in fw) and ("not derive" in fw or "does not derive" in fw or "is not derived" in fw))

chan_misclass = [g for g, e in l3.items() if e.get("channel") is not None]
check("no L3 cholinergic-drive node mislabelled as an ion channel", chan_misclass == [])

# AD-specific: the promoter |h_sp| must NOT be equated with the neurodegeneration-progression quantity
op_guard = all(e.get("grade_promoter_vs_progression", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the neurodegeneration-progression quantity", op_guard)

# AD-specific: L3 must be the UNIQUE dominant lever, AND L1>0 AND L2>0 (the ADHD INVERSE; NOT L3-only)
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
l3_unique_dominant = (counts.get("L3", 0) == maxn) and \
                     (sum(1 for v in counts.values() if v == maxn) == 1) and \
                     (max(counts, key=lambda k: counts[k]) == "L3")
l1_l2_present = (counts.get("L1", 0) > 0) and (counts.get("L2", 0) > 0)
check(f"L3 is the UNIQUE dominant lever (Alzheimer's distribution; counts={counts})", l3_unique_dominant)
check(f"L1 and L2 are BOTH PRESENT (the ADHD inverse; counts L1={counts.get('L1', 0)} L2={counts.get('L2', 0)})",
      l1_l2_present)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=False, dominant_levers=[L3], l3_dominant=True, l1_present=True, l2_present=True, l3_only=False",
      ldw.get("codominant") is False and ldw.get("dominant_levers", []) == ["L3"]
      and ldw.get("l3_dominant") is True and ldw.get("l1_present") is True
      and ldw.get("l2_present") is True and ldw.get("l3_only") is False)

# AD-specific: the reachable surface is recorded as split-sign AND purely symptomatic
check("lever-distribution witness records split_sign_reachable_surface=True and purely_symptomatic_reachable_surface=True",
      ldw.get("split_sign_reachable_surface") is True and ldw.get("purely_symptomatic_reachable_surface") is True)

# AD-specific: the DOMAIN-RESTRICTION must be recorded (SYMP reached; PROG not)
drw = m.get("domain_restriction_witness", {})
symp_ok = drw.get("SYMP", {}).get("reached_by_levers") is True
prog_not = drw.get("PROG", {}).get("reached_by_levers") is False
check("domain-restriction witness records SYMP=reached, PROG=NOT", symp_ok and prog_not)
check("SYMP axis recorded symptomatic_only=True (reachable surface is purely symptomatic)",
      drw.get("SYMP", {}).get("symptomatic_only") is True)

# AD-specific: the out-of-reach targets must NAME the PROG (progression) axis (>=1 gene), all NOT reached
oor = m.get("out_of_reach_targets", {})
oor_by_axis = oor.get("by_axis", {})
named_PROG = len(oor_by_axis.get("PROG", [])) >= 1
oor_all_not_reached = all(e.get("reached_by_threshold_levers") is False for e in oor.get("entries", []))
check("out-of-reach targets NAME the PROG neurodegenerative-progression axis (>=1 gene), all flagged NOT REACHED",
      named_PROG and oor_all_not_reached and len(oor.get("entries", [])) >= 1)

# AD-specific: PROG is named out-of-reach for the DEEPEST (degenerative/progression) reason -- the convergence with E0
prog_block = drw.get("PROG", {})
prog_named = len(prog_block.get("named_genes", [])) >= 1
check("PROG axis NAMED out-of-reach (>=1 progression gene) -- the dominant Alzheimer's fault made concrete",
      prog_named)

# AD-specific: the fit is the series' THIRD PARTIAL [L] (reached SYMP; out-of-reach PROG) and the deepest
pfw = m.get("partial_fit_witness", {})
partial_L = pfw.get("fit_grade", "").strip().startswith("[L]") and \
            (pfw.get("fit_index_in_series") == 3) and \
            (pfw.get("deepest_partial") is True) and \
            ("SYMP" in pfw.get("reached_axis", "")) and \
            ("PROG" in pfw.get("out_of_reach_axis", ""))
check("fit graded PARTIAL [L] (series' THIRD non-clean fit, DEEPEST; reached=SYMP, out-of-reach=PROG)", partial_L)

result = {
    "title": ("L3 honesty pass (Alzheimer's) -- four cholinergic-drive [O] handles; L3 the UNIQUE dominant "
              "lever with L1 AND L2 BOTH present (the ADHD inverse); SYMP axis reached across L1/L2/L3 "
              "(purely symptomatic, split-sign); the dominant PROG neurodegenerative-progression axis NAMED "
              "out-of-reach; the series' THIRD and DEEPEST PARTIAL [L] fit -- the convergence point with the "
              "E0 progression-dynamics layer (an E0 DECAY)"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction T-L gates"),
    "principle": ("gamma reads promoter threshold structure; each of the four L3 cholinergic-drive "
                  "(ACHE/BCHE/CHRNA7/CHRM1) acetylcholine signalling mechanisms is NOT captured and is graded "
                  "cited-biology [O]. The promoter |h_sp| is held distinct from the neurodegeneration-"
                  "progression quantity; L3 is verified the UNIQUE dominant lever with L1 AND L2 BOTH present "
                  "(Alzheimer's eighth distribution pattern -- L3-dominant but engaging the ionic levers too, "
                  "like addiction, yet with a SPLIT corrective sign and a PURELY SYMPTOMATIC reachable "
                  "surface); the lever map is verified to reach the SYMP (instantaneous symptomatic) axis "
                  "across all three lever classes -- where the established symptomatic pharmacology acts -- "
                  "with the DOMINANT PROG (neurodegenerative-progression) axis NAMED out-of-reach (real genes "
                  "APP/PSEN1/PSEN2/MAPT/APOE/TREM2, real citations); and the fit is verified the series' THIRD "
                  "and DEEPEST PARTIAL [L], because the dominant axis (PROG) is the out-of-reach one -- for a "
                  "DEEPER reason than addiction: PROG is not a fold (the ADHD lesson) AND a PROGRESSION over "
                  "time, an E0-layer DECAY variable (the addiction lesson) AND a DEGENERATION / cumulative "
                  "LOSS (the structural inverse of addiction's E0 GAIN). The PROG axis is precisely the E0 "
                  "progression-dynamics layer -- the convergence point where threshold-leverisation meets the "
                  "dynamics route, as an E0 DECAY."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "l3_unique_dominant": l3_unique_dominant, "l1_l2_present": l1_l2_present,
    "domain_restriction": {"SYMP_reached": symp_ok, "PROG_reached": not prog_not,
                           "symptomatic_only": drw.get("SYMP", {}).get("symptomatic_only")},
    "out_of_reach_named": {"PROG_axis_genes": oor_by_axis.get("PROG", [])},
    "partial_fit": {"fit_grade": pfw.get("fit_grade"), "fit_index_in_series": pfw.get("fit_index_in_series"),
                    "deepest_partial": pfw.get("deepest_partial"),
                    "reached_axis": pfw.get("reached_axis"), "out_of_reach_axis": pfw.get("out_of_reach_axis"),
                    "third_partial_L": partial_L},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "alzheimers_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
