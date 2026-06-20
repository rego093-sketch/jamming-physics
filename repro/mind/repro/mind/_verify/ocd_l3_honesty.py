#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ocd_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11 via the
bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction/Alzheimer's T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. OCD is the FOURTH PARTIAL [L]
fit in the series, and a NEW MODE -- and like addiction and Alzheimer's it is L3-DOMINANT WITH L1 AND L2
BOTH PRESENT (not L3-ONLY like ADHD), but with a SPARSE L2 arm: the up-stream serotonergic/dopaminergic
DRIVE nodes load most (SLC6A4, HTR2A, HTR1B, DRD2), the glutamatergic EXCITATORY axis (L1: SLC1A1/GRIN2B/
GRIK2) is strongly engaged, and the inhibitory-RESTORE arm (L2: GABRA1) is a single, weak, SPARSE node.
For every serotonergic/dopaminergic-drive node the map may read the gene's threshold structure and PLACE
it, but it MUST grade the serotonin/dopamine SIGNALLING MECHANISM as cited-biology [O], never as a derived
mechanism. This gate enforces that, and the OCD-specific structure:

  - OCD is L3-DOMINANT but NOT L3-ONLY, with a SPARSE L2: L1 and L2 are BOTH PRESENT and L2 is a single
    node. The gate checks L3 is the UNIQUE dominant lever AND L1>0 AND L2>0 (NOT l1_l2_empty) AND L2 is
    SPARSE (==1).
  - the DOMAIN-RESTRICTION reaches the INSTANT (instantaneous CSTC-loop excitability operating point) axis
    across all three lever classes -- where the established + investigational OCD pharmacology acts, and
    genuinely (partially) helps. The DOMINANT OCD fault, the LOCK (pathological-stabilisation / stuck-
    attractor) axis, is NOT reached and is NAMED out-of-reach (real genes DLGAP3/SLITRK5/PTPRD/BTBD3).
    This is WHY the fit is PARTIAL [L]: the dominant axis is the out-of-reach one -- and for a NEW reason
    (a third E0 mode), because LOCK is not a fold (the ADHD lesson) AND a consolidated/learned plasticity
    (E0-layer) variable (the addiction lesson) AND a pathological STABILISATION / LOCK (an over-deep basin
    / hysteresis -- distinct from addiction's E0 GAIN and Alzheimer's E0 DECAY).
  - the LOCK axis is precisely the E2 (state-switching) + E0 (consolidation) dynamics layer -- the
    CONVERGENCE point where threshold-leverisation (B-i) structurally meets the dynamics route (B-ii), as
    an E0 STABILISATION (the third distinct mode, completing the trio). B-i NAMES the loop-lock out-of-
    reach honestly.

Gate (fail-closed):
  - every L3 entry carries grade_mechanism beginning with "[O]"; is not presented as derived ([V]/[F]);
    carries a non-empty citation; is not mislabelled as an ion channel (channel=None);
  - the declared L3 set (the four serotonergic/dopaminergic-drive nodes) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the pathological-stabilisation LOCK quantity;
  - L3 is the UNIQUE dominant lever AND L1>0 AND L2>0 AND L2 is SPARSE (==1);
  - the domain-restriction witness records INSTANT=reached, LOCK=NOT-reached;
  - the out_of_reach_targets NAME the LOCK axis (>=1 stabilisation gene), all flagged NOT REACHED;
  - the fit is graded PARTIAL [L] (the series' FOURTH non-clean fit), with reached=INSTANT, oor=LOCK, and
    the LOCK axis recorded as the THIRD distinct E0 mode (completes_e0_trio).

Run:  python3 ocd_l3_honesty.py  -> ocd_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "ocd_threshold_levers_results.json")

DECLARED_L3 = {"SLC6A4", "HTR2A", "HTR1B", "DRD2"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (OCD)")

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
      ("l3" in fw) and ("[o]" in fw) and ("not derive" in fw or "does not derive" in fw or "is not derived" in fw or "it does not derive" in fw))

chan_misclass = [g for g, e in l3.items() if e.get("channel") is not None]
check("no L3 serotonergic/dopaminergic-drive node mislabelled as an ion channel", chan_misclass == [])

# OCD-specific: the promoter |h_sp| must NOT be equated with the pathological-stabilisation LOCK quantity
op_guard = all(e.get("grade_promoter_vs_lock", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the pathological-stabilisation LOCK quantity", op_guard)

# OCD-specific: L3 must be the UNIQUE dominant lever, AND L1>0 AND L2>0 AND L2 SPARSE (==1)
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
l3_unique_dominant = (counts.get("L3", 0) == maxn) and \
                     (sum(1 for v in counts.values() if v == maxn) == 1) and \
                     (max(counts, key=lambda k: counts[k]) == "L3")
l1_l2_present = (counts.get("L1", 0) > 0) and (counts.get("L2", 0) > 0)
l2_sparse = (counts.get("L2", 0) == 1)
check(f"L3 is the UNIQUE dominant lever (OCD distribution; counts={counts})", l3_unique_dominant)
check(f"L1 and L2 are BOTH PRESENT (counts L1={counts.get('L1', 0)} L2={counts.get('L2', 0)})", l1_l2_present)
check(f"L2 is SPARSE -- a single weak node (counts L2={counts.get('L2', 0)})", l2_sparse)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=False, dominant_levers=[L3], l3_dominant=True, l1_present=True, l2_present=True, l2_sparse=True, l3_only=False",
      ldw.get("codominant") is False and ldw.get("dominant_levers", []) == ["L3"]
      and ldw.get("l3_dominant") is True and ldw.get("l1_present") is True
      and ldw.get("l2_present") is True and ldw.get("l2_sparse") is True
      and ldw.get("l3_only") is False)

# OCD-specific: the reachable surface is recorded as mixed-sign, and the LOCK axis as the third E0 mode
check("lever-distribution witness records mixed_sign_reachable_surface=True and lock_axis_is_third_e0_mode=True",
      ldw.get("mixed_sign_reachable_surface") is True and ldw.get("lock_axis_is_third_e0_mode") is True)

# OCD-specific: the DOMAIN-RESTRICTION must be recorded (INSTANT reached; LOCK not)
drw = m.get("domain_restriction_witness", {})
instant_ok = drw.get("INSTANT", {}).get("reached_by_levers") is True
lock_not = drw.get("LOCK", {}).get("reached_by_levers") is False
check("domain-restriction witness records INSTANT=reached, LOCK=NOT", instant_ok and lock_not)
check("INSTANT axis recorded reachable_but_partial=True (the levers genuinely but partially help)",
      drw.get("INSTANT", {}).get("reachable_but_partial") is True)

# OCD-specific: the out-of-reach targets must NAME the LOCK (stabilisation) axis (>=1 gene), all NOT reached
oor = m.get("out_of_reach_targets", {})
oor_by_axis = oor.get("by_axis", {})
named_LOCK = len(oor_by_axis.get("LOCK", [])) >= 1
oor_all_not_reached = all(e.get("reached_by_threshold_levers") is False for e in oor.get("entries", []))
check("out-of-reach targets NAME the LOCK pathological-stabilisation axis (>=1 gene), all flagged NOT REACHED",
      named_LOCK and oor_all_not_reached and len(oor.get("entries", [])) >= 1)

# OCD-specific: LOCK is named out-of-reach for the NEW (stabilisation) reason -- the convergence with E2/E0
lock_block = drw.get("LOCK", {})
lock_named = len(lock_block.get("named_genes", [])) >= 1
check("LOCK axis NAMED out-of-reach (>=1 stabilisation gene) -- the dominant OCD fault made concrete",
      lock_named)

# OCD-specific: the fit is the series' FOURTH PARTIAL [L] (reached INSTANT; out-of-reach LOCK), third E0 mode
pfw = m.get("partial_fit_witness", {})
partial_L = pfw.get("fit_grade", "").strip().startswith("[L]") and \
            (pfw.get("fit_index_in_series") == 4) and \
            (pfw.get("completes_e0_trio") is True) and \
            ("INSTANT" in pfw.get("reached_axis", "")) and \
            ("LOCK" in pfw.get("out_of_reach_axis", ""))
check("fit graded PARTIAL [L] (series' FOURTH non-clean fit, LOCK=third E0 mode; reached=INSTANT, out-of-reach=LOCK)", partial_L)

result = {
    "title": ("L3 honesty pass (OCD) -- four serotonergic/dopaminergic-drive [O] handles; L3 the UNIQUE "
              "dominant lever with L1 strongly present and L2 SPARSE (a single weak node); INSTANT axis "
              "reached across L1/L2/L3 (reachable-but-partial, mixed sign); the dominant LOCK pathological-"
              "stabilisation axis NAMED out-of-reach; the series' FOURTH PARTIAL [L] fit and a NEW MODE -- "
              "the convergence point with the E2/E0 dynamics layer (an E0 STABILISATION, the third distinct "
              "mode)"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression/schizophrenia/autism/ADHD/addiction/Alzheimer's T-L gates"),
    "principle": ("gamma reads promoter threshold structure; each of the four L3 serotonergic/dopaminergic-"
                  "drive (SLC6A4/HTR2A/HTR1B/DRD2) signalling mechanisms is NOT captured and is graded "
                  "cited-biology [O]. The promoter |h_sp| is held distinct from the pathological-"
                  "stabilisation LOCK quantity; L3 is verified the UNIQUE dominant lever with L1 strongly "
                  "present and L2 SPARSE (OCD's ninth distribution pattern -- L3-dominant with a strong L1 "
                  "and a single weak L2 node, the GABAergic arm thin); the lever map is verified to reach "
                  "the INSTANT (instantaneous CSTC excitability) axis across all three lever classes -- "
                  "where the established + investigational pharmacology acts and genuinely (partially) helps "
                  "-- with the DOMINANT LOCK (pathological-stabilisation) axis NAMED out-of-reach (real "
                  "genes DLGAP3/SLITRK5/PTPRD/BTBD3, real citations); and the fit is verified the series' "
                  "FOURTH PARTIAL [L] and a NEW MODE, because the dominant axis (LOCK) is the out-of-reach "
                  "one -- for a NEW reason: LOCK is not a fold (the ADHD lesson) AND a consolidated/learned "
                  "plasticity E0-layer variable (the addiction lesson) AND a pathological STABILISATION / "
                  "LOCK -- an over-deep basin / hysteresis (an E2 phenomenon), the THIRD distinct E0 mode, "
                  "distinct from addiction's E0 GAIN and Alzheimer's E0 DECAY. The LOCK axis is precisely "
                  "the E2/E0 dynamics layer -- the convergence point where threshold-leverisation meets the "
                  "dynamics route, as an E0 STABILISATION."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "l3_unique_dominant": l3_unique_dominant, "l1_l2_present": l1_l2_present, "l2_sparse": l2_sparse,
    "domain_restriction": {"INSTANT_reached": instant_ok, "LOCK_reached": not lock_not,
                           "reachable_but_partial": drw.get("INSTANT", {}).get("reachable_but_partial")},
    "out_of_reach_named": {"LOCK_axis_genes": oor_by_axis.get("LOCK", [])},
    "partial_fit": {"fit_grade": pfw.get("fit_grade"), "fit_index_in_series": pfw.get("fit_index_in_series"),
                    "completes_e0_trio": pfw.get("completes_e0_trio"), "e0_mode": pfw.get("e0_mode"),
                    "reached_axis": pfw.get("reached_axis"), "out_of_reach_axis": pfw.get("out_of_reach_axis"),
                    "fourth_partial_L": partial_L},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "ocd_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
