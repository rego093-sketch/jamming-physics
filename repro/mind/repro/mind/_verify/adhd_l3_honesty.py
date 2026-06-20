#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhd_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11 via the
bipolar/epilepsy/depression/schizophrenia/autism T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. ADHD is the FIRST PARTIAL [L]
fit in the series, and its L3 axis is the WHOLE of the threshold-frame engagement: unlike depression
(HPA/monoamine, L3-dominant but with a reachable L1/L2 mix) or schizophrenia (dopamine, L3 co-dominant
with L1), ADHD is L3-ONLY -- every lever the frame reaches is an UPSTREAM catecholamine/monoaminergic
DRIVE-TONE node (reuptake transporters + tone receptors: SLC6A3/DAT, SLC6A2/NET, SLC6A4/SERT,
ADRA2A/alpha-2A, DRD4/D4), and L1 (ionic-fold) and L2 (network-timing) are BOTH EMPTY. For every one of
those drive nodes, the map may read the gene's threshold structure and PLACE it, but it MUST grade the
SIGNALLING MECHANISM as cited-biology [O], never as a derived mechanism. This gate enforces that, and the
ADHD-specific structure -- which is the AUTISM INVERSE:

  - ADHD is L3-DOMINANT and indeed L3-ONLY (NOT L1-dominant like autism, NOT co-dominant like
    schizophrenia). The gate checks L3 is the UNIQUE dominant lever and L1==L2==0 (BOTH empty).
  - the DOMAIN-RESTRICTION reaches the DT (drive-tone / arousal) axis ONLY -- the SECONDARY ADHD axis.
    The dominant GA (gain-amplitude / output: synthesis/release/catabolism) axis is NOT reached, and is
    NAMED out-of-reach (real genes TH/DBH/SNAP25/COMT). This is WHY the fit is PARTIAL [L]: the dominant
    axis is the out-of-reach one.
  - the W (long-range wiring) axis is ABSENT from the disorder (ADHD has intact wiring -- sec.22
    adhd_axis_specific). This is the DISCRIMINANT from autism. The gate enforces W has ZERO named genes
    and present_in_disorder=False (the INVERSE of the autism gate, which REQUIRED W genes proven in
    sec.19).

Gate (fail-closed):
  - every L3 entry carries grade_mechanism beginning with "[O]"; is not presented as derived
    ([V]/[F]); carries a non-empty citation; is not mislabelled as an ion channel (channel=None);
  - the declared L3 set (the five drive-tone nodes) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the sec.22 network gain/arousal quantity;
  - L3 is the UNIQUE dominant lever and L1==L2==0 (ADHD's distribution, NOT L1-dominant/co-dominant);
  - the domain-restriction witness records DT=reached, GA=NOT, W=NOT-and-ABSENT;
  - the out_of_reach_targets NAME the GA axis (>=1 gain gene), all flagged NOT REACHED;
  - W is ABSENT (named_genes==[], present_in_disorder=False) -- the autism INVERSE / the discriminant;
  - the fit is graded PARTIAL [L] (the series' first non-clean fit).

Run:  python3 adhd_l3_honesty.py  -> adhd_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "adhd_threshold_levers_results.json")

DECLARED_L3 = {"SLC6A3", "SLC6A2", "SLC6A4", "ADRA2A", "DRD4"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (ADHD)")

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
check("no L3 drive-tone node mislabelled as an ion channel", chan_misclass == [])

# ADHD-specific: the promoter |h_sp| must NOT be equated with the sec.22 network gain/arousal quantity
op_guard = all(e.get("grade_promoter_vs_network_quantity", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the sec.22 network gain/arousal quantity", op_guard)

# ADHD-specific: L3 must be the UNIQUE dominant lever and L1==L2==0 (the autism INVERSE; L3-ONLY)
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
l3_unique_dominant = (counts.get("L3", 0) == maxn) and \
                     (sum(1 for v in counts.values() if v == maxn) == 1) and \
                     (max(counts, key=lambda k: counts[k]) == "L3")
l1_l2_empty = (counts.get("L1", 0) == 0) and (counts.get("L2", 0) == 0)
check(f"L3 is the UNIQUE dominant lever (ADHD's distribution; counts={counts})", l3_unique_dominant)
check(f"L1 and L2 are BOTH EMPTY (L3-only; counts L1={counts.get('L1', 0)} L2={counts.get('L2', 0)})", l1_l2_empty)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=False, dominant_levers=[L3], l3_only=True, l1_l2_empty=True",
      ldw.get("codominant") is False and ldw.get("dominant_levers", []) == ["L3"]
      and ldw.get("l3_only") is True and ldw.get("l1_l2_empty") is True)

# ADHD-specific: the DOMAIN-RESTRICTION must be recorded (DT reached; GA not; W not)
drw = m.get("domain_restriction_witness", {})
dt_ok = drw.get("DT", {}).get("reached_by_levers") is True
ga_ok = drw.get("GA", {}).get("reached_by_levers") is False
w_not = drw.get("W", {}).get("reached_by_levers") is False
check("domain-restriction witness records DT=reached, GA=NOT, W=NOT", dt_ok and ga_ok and w_not)

# ADHD-specific: the out-of-reach targets must NAME the GA (gain-amplitude) axis (>=1 gene), all NOT reached
oor = m.get("out_of_reach_targets", {})
oor_by_axis = oor.get("by_axis", {})
named_GA = len(oor_by_axis.get("GA", [])) >= 1
oor_all_not_reached = all(e.get("reached_by_threshold_levers") is False for e in oor.get("entries", []))
check("out-of-reach targets NAME the GA gain-amplitude axis (>=1 gene), all flagged NOT REACHED",
      named_GA and oor_all_not_reached and len(oor.get("entries", [])) >= 1)

# ADHD-specific (the DISCRIMINANT / autism INVERSE): W must be ABSENT from the disorder
w_block = drw.get("W", {})
w_absent = (w_block.get("present_in_disorder") is False) and (len(w_block.get("named_genes", [])) == 0)
check("W axis is ABSENT (named_genes==[], present_in_disorder=False) -- the autism INVERSE / discriminant",
      w_absent)

# ADHD-specific: the fit is the series' FIRST PARTIAL [L] (not the clean [V] of the five prior disorders)
pfw = m.get("partial_fit_witness", {})
partial_L = pfw.get("fit_grade", "").strip().startswith("[L]") and \
            (pfw.get("w_present_in_disorder") is False)
check("fit graded PARTIAL [L] (series' first non-clean fit; W absent)", partial_L)

result = {
    "title": ("L3 honesty pass (ADHD) -- five drive-tone [O] handles (L3-ONLY); L3 the UNIQUE dominant "
              "lever with L1/L2 BOTH empty; DT-axis restricted; the dominant GA axis NAMED out-of-reach; "
              "W ABSENT (the autism inverse / discriminant); the series' first PARTIAL [L] fit"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression/schizophrenia/autism T-L gates"),
    "principle": ("gamma reads promoter threshold structure; each of the five L3 drive-tone "
                  "(SLC6A3/SLC6A2/SLC6A4/ADRA2A/DRD4) catecholamine/monoaminergic signalling mechanisms is "
                  "NOT captured and is graded cited-biology [O]. The promoter |h_sp| is held distinct from "
                  "the sec.22 network gain/arousal quantity; L3 is verified the UNIQUE dominant lever and "
                  "L1==L2==0 (ADHD's sixth distribution pattern -- L3-ONLY, the purest L3 case); the lever "
                  "map is verified to reach the DT (drive-tone/arousal) axis ONLY -- the SECONDARY ADHD "
                  "axis -- with the DOMINANT GA (gain-amplitude/output: synthesis/release/catabolism) axis "
                  "NAMED out-of-reach (real genes, real citations); the W (long-range wiring) axis is "
                  "verified ABSENT from the disorder (the discriminant from autism / the autism INVERSE); "
                  "and the fit is verified the series' FIRST PARTIAL [L], because the dominant axis (GA) is "
                  "the out-of-reach one."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "l3_unique_dominant": l3_unique_dominant, "l1_l2_empty": l1_l2_empty,
    "domain_restriction": {"DT_reached": dt_ok, "GA_reached": not ga_ok, "W_reached": not w_not},
    "out_of_reach_named": {"GA_axis_genes": oor_by_axis.get("GA", [])},
    "w_absent_discriminant": {"present_in_disorder": w_block.get("present_in_disorder"),
                              "named_W_genes": w_block.get("named_genes", []),
                              "is_autism_inverse": w_absent},
    "partial_fit": {"fit_grade": pfw.get("fit_grade"), "w_present_in_disorder": pfw.get("w_present_in_disorder"),
                    "first_partial_L": partial_L},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "adhd_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
