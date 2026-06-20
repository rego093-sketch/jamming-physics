#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
addiction_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11 via the
bipolar/epilepsy/depression/schizophrenia/autism/ADHD T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. Addiction is the SECOND PARTIAL
[L] fit in the series, and -- unlike ADHD, which was L3-ONLY (a channelopathy-free, L1/L2-EMPTY frame) --
addiction is L3-DOMINANT WITH L1 AND L2 BOTH PRESENT: the up-stream reward DRIVE nodes load most
(opioid/dopamine/nicotinic receptors + the dopamine transporter: OPRM1, OPRK1, DRD2, SLC6A3/DAT, CHRNA5),
but the glutamatergic plasticity SUBSTRATE (L1: GRIN2A/GRIN2B) and the inhibitory-RESTORE arm (L2:
GABRA2/GABRG3) are ALSO engaged -- the TEXTURAL INVERSE of ADHD's emptiness. For every reward-drive node
the map may read the gene's threshold structure and PLACE it, but it MUST grade the reward/incentive
SIGNALLING MECHANISM as cited-biology [O], never as a derived mechanism. This gate enforces that, and the
addiction-specific structure:

  - addiction is L3-DOMINANT but NOT L3-ONLY: L1 and L2 are BOTH PRESENT (the ADHD INVERSE). The gate
    checks L3 is the UNIQUE dominant lever AND L1>0 AND L2>0 (NOT l1_l2_empty).
  - the DOMAIN-RESTRICTION reaches the INSTANT (instantaneous drive/excitability operating point) axis
    across all three lever classes -- where the established addiction pharmacology acts. The DOMINANT
    addiction fault, the SG (consolidated sensitisation GAIN) axis, is NOT reached and is NAMED
    out-of-reach (real genes FOSB/BDNF/CREB1/ARC). This is WHY the fit is PARTIAL [L]: the dominant axis
    is the out-of-reach one -- and for a DEEPER reason than ADHD, because SG is a GAIN not a fold (the
    ADHD lesson) AND moreover CONSOLIDATED/LEARNED, a plasticity (E0-layer, sec.26) variable.
  - the SG axis is precisely the E0 plasticity layer -- the CONVERGENCE point where threshold-leverisation
    (B-i) structurally meets the dynamics route (B-ii). B-i NAMES the trace out-of-reach honestly.

Gate (fail-closed):
  - every L3 entry carries grade_mechanism beginning with "[O]"; is not presented as derived
    ([V]/[F]); carries a non-empty citation; is not mislabelled as an ion channel (channel=None);
  - the declared L3 set (the five reward-drive nodes) is present and all-[O];
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the consolidated sensitisation-gain quantity;
  - L3 is the UNIQUE dominant lever AND L1>0 AND L2>0 (addiction's distribution, NOT L3-only);
  - the domain-restriction witness records INSTANT=reached, SG=NOT-reached;
  - the out_of_reach_targets NAME the SG axis (>=1 sensitisation-gain gene), all flagged NOT REACHED;
  - the fit is graded PARTIAL [L] (the series' second non-clean fit), with reached=INSTANT, oor=SG.

Run:  python3 addiction_l3_honesty.py  -> addiction_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "addiction_threshold_levers_results.json")

DECLARED_L3 = {"OPRM1", "OPRK1", "DRD2", "SLC6A3", "CHRNA5"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (addiction)")

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
check("no L3 reward-drive node mislabelled as an ion channel", chan_misclass == [])

# addiction-specific: the promoter |h_sp| must NOT be equated with the consolidated sensitisation-gain quantity
op_guard = all(e.get("grade_promoter_vs_sensitisation_gain", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the consolidated sensitisation-gain quantity", op_guard)

# addiction-specific: L3 must be the UNIQUE dominant lever, AND L1>0 AND L2>0 (the ADHD INVERSE; NOT L3-only)
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
l3_unique_dominant = (counts.get("L3", 0) == maxn) and \
                     (sum(1 for v in counts.values() if v == maxn) == 1) and \
                     (max(counts, key=lambda k: counts[k]) == "L3")
l1_l2_present = (counts.get("L1", 0) > 0) and (counts.get("L2", 0) > 0)
check(f"L3 is the UNIQUE dominant lever (addiction's distribution; counts={counts})", l3_unique_dominant)
check(f"L1 and L2 are BOTH PRESENT (the ADHD inverse; counts L1={counts.get('L1', 0)} L2={counts.get('L2', 0)})",
      l1_l2_present)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=False, dominant_levers=[L3], l3_dominant=True, l1_present=True, l2_present=True, l3_only=False",
      ldw.get("codominant") is False and ldw.get("dominant_levers", []) == ["L3"]
      and ldw.get("l3_dominant") is True and ldw.get("l1_present") is True
      and ldw.get("l2_present") is True and ldw.get("l3_only") is False)

# addiction-specific: the DOMAIN-RESTRICTION must be recorded (INSTANT reached; SG not)
drw = m.get("domain_restriction_witness", {})
instant_ok = drw.get("INSTANT", {}).get("reached_by_levers") is True
sg_not      = drw.get("SG", {}).get("reached_by_levers") is False
check("domain-restriction witness records INSTANT=reached, SG=NOT", instant_ok and sg_not)

# addiction-specific: the out-of-reach targets must NAME the SG (sensitisation-gain) axis (>=1 gene), all NOT reached
oor = m.get("out_of_reach_targets", {})
oor_by_axis = oor.get("by_axis", {})
named_SG = len(oor_by_axis.get("SG", [])) >= 1
oor_all_not_reached = all(e.get("reached_by_threshold_levers") is False for e in oor.get("entries", []))
check("out-of-reach targets NAME the SG consolidated-sensitisation-gain axis (>=1 gene), all flagged NOT REACHED",
      named_SG and oor_all_not_reached and len(oor.get("entries", [])) >= 1)

# addiction-specific: SG is named out-of-reach for the DEEPER (consolidated/learned) reason -- the convergence with E0
sg_block = drw.get("SG", {})
sg_named = len(sg_block.get("named_genes", [])) >= 1
check("SG axis NAMED out-of-reach (>=1 sensitisation-gain gene) -- the dominant addiction fault made concrete",
      sg_named)

# addiction-specific: the fit is the series' SECOND PARTIAL [L] (reached INSTANT; out-of-reach SG)
pfw = m.get("partial_fit_witness", {})
partial_L = pfw.get("fit_grade", "").strip().startswith("[L]") and \
            (pfw.get("fit_index_in_series") == 2) and \
            ("INSTANT" in pfw.get("reached_axis", "")) and \
            ("SG" in pfw.get("out_of_reach_axis", ""))
check("fit graded PARTIAL [L] (series' SECOND non-clean fit; reached=INSTANT, out-of-reach=SG)", partial_L)

result = {
    "title": ("L3 honesty pass (addiction) -- five reward-drive [O] handles; L3 the UNIQUE dominant lever "
              "with L1 AND L2 BOTH present (the ADHD inverse); INSTANT axis reached across L1/L2/L3; the "
              "dominant SG consolidated-sensitisation-gain axis NAMED out-of-reach; the series' SECOND "
              "PARTIAL [L] fit -- the convergence point with the E0 plasticity layer"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression/schizophrenia/autism/ADHD T-L gates"),
    "principle": ("gamma reads promoter threshold structure; each of the five L3 reward-drive "
                  "(OPRM1/OPRK1/DRD2/SLC6A3/CHRNA5) opioid/dopamine/nicotinic signalling mechanisms is "
                  "NOT captured and is graded cited-biology [O]. The promoter |h_sp| is held distinct from "
                  "the consolidated sensitisation-gain quantity; L3 is verified the UNIQUE dominant lever "
                  "with L1 AND L2 BOTH present (addiction's seventh distribution pattern -- L3-dominant but "
                  "engaging the ionic levers too, the TEXTURAL INVERSE of ADHD's L3-only emptiness); the "
                  "lever map is verified to reach the INSTANT (instantaneous drive/excitability) axis "
                  "across all three lever classes -- where the established pharmacology acts -- with the "
                  "DOMINANT SG (consolidated sensitisation-gain) axis NAMED out-of-reach (real genes "
                  "FOSB/BDNF/CREB1/ARC, real citations); and the fit is verified the series' SECOND PARTIAL "
                  "[L], because the dominant axis (SG) is the out-of-reach one -- for a DEEPER reason than "
                  "ADHD: SG is a GAIN not a fold (the ADHD lesson) AND moreover CONSOLIDATED/LEARNED, a "
                  "plasticity (E0-layer, sec.26) variable. The SG axis is precisely the E0 plasticity layer "
                  "-- the convergence point where threshold-leverisation meets the dynamics route."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "l3_unique_dominant": l3_unique_dominant, "l1_l2_present": l1_l2_present,
    "domain_restriction": {"INSTANT_reached": instant_ok, "SG_reached": not sg_not},
    "out_of_reach_named": {"SG_axis_genes": oor_by_axis.get("SG", [])},
    "partial_fit": {"fit_grade": pfw.get("fit_grade"), "fit_index_in_series": pfw.get("fit_index_in_series"),
                    "reached_axis": pfw.get("reached_axis"), "out_of_reach_axis": pfw.get("out_of_reach_axis"),
                    "second_partial_L": partial_L},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "addiction_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
