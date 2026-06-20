#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
schizophrenia_l3_honesty.py  —  the L3 honesty gate (fail-closed). Inherited from analgesic v2.0 M11
via the bipolar/epilepsy/depression T-L gates.

The framework reads PERIPHERAL/promoter switch-threshold structure best. The schizophrenia L3 axis is
the DOPAMINE antipsychotic axis -- the most established psychosis target set: the dopamine RECEPTORS
(DRD2 = the D2-antagonist target shared by every licensed antipsychotic, DRD4 = the clozapine-affinity
sub-route), the dopamine SYNTHESIS/TRANSPORT set (TH = elevated striatal synthesis capacity, SLC6A3 =
the transporter), the serotonergic MODULATION of dopamine (HTR2A, the atypical axis, non-monotone) and
the prefrontal catabolic set-point (COMT). These are GPCR / transporter / enzyme signalling that the
gamma read does NOT capture. For those, the map may read the gene's threshold structure and PLACE it in
the lever map, but it MUST grade the MECHANISM LINK as cited-biology [O], never as a derived mechanism.
This gate enforces exactly that, target by target.

Schizophrenia is the FIRST case where L1 and L3 are CO-DOMINANT (6 targets each): the glutamate/NMDA
axis (L1) and the dopamine axis (L3) load the POSITIVE-domain raise at once. This gate therefore checks
CO-DOMINANCE (L1 and L3 are jointly the largest levers) -- NOT L3-dominance (depression's claim). It also
enforces the DOMAIN-RESTRICTION witness: the lever map reaches the POSITIVE domain ONLY; the negative
(output-deficit) and cognitive (wiring) domains are NOT reached -- the map is axis-structured, not
disorder-wide. This is schizophrenia's qualitative difference from every prior T-L chapter.

Gate (fail-closed):
  - every threshold-map entry with lever == "L3" carries grade_mechanism beginning with "[O]";
  - none is presented as a derived ([V]/[F]) mechanism;
  - each carries a non-empty citation (src);
  - the declared L3 set (dopamine receptor + synthesis/transport + serotonergic + catabolic) is present
    and all-[O];
  - no L3 entry is mislabelled as an ion channel (they are receptors/transporters/enzymes: channel=None);
  - the map's firewall text states the L3 mechanism link is [O];
  - the promoter |h_sp| is held distinct from the sec.24 network over-ignition threshold;
  - L1 and L3 are CO-DOMINANT (jointly the largest levers) -- NOT L3-dominant;
  - the domain-restriction witness records positive=reached, negative=not, cognitive=not.

Run:  python3 schizophrenia_l3_honesty.py  -> schizophrenia_l3_honesty.json ; exit 1 on any violation
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
MAP  = os.path.join(HERE, "schizophrenia_threshold_levers_results.json")

DECLARED_L3 = {"DRD2", "DRD4", "SLC6A3", "TH", "COMT", "HTR2A"}

FAIL = []
def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond: FAIL.append(name)

m = json.load(open(MAP))
entries = {e["gene"]: e for e in m["entries"]}
l3 = {g: e for g, e in entries.items() if e["lever"] == "L3"}

print("L3 honesty pass (schizophrenia)")

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
check("no L3 dopamine/serotonergic node mislabelled as an ion channel", chan_misclass == [])

# schizophrenia-specific: the promoter |h_sp| must NOT be equated with the sec.24 network threshold
op_guard = all(e.get("grade_promoter_vs_network_threshold", "").strip().startswith("[O]")
               for e in entries.values())
check("promoter |h_sp| graded [O] distinct from the sec.24 network over-ignition threshold", op_guard)

# schizophrenia-specific: L1 and L3 must be CO-DOMINANT (jointly the largest), NOT L3-dominant
by_lever = m.get("targets_by_lever", {})
counts = {k: len(v) for k, v in by_lever.items()}
maxn = max(counts.values()) if counts else 0
codominant = (counts.get("L1", 0) == maxn) and (counts.get("L3", 0) == maxn) and maxn > 0
check(f"L1 and L3 are CO-DOMINANT (jointly the largest levers; counts={counts})", codominant)

ldw = m.get("lever_distribution_witness", {})
check("lever-distribution witness records codominant=True with dominant_levers={L1,L3}",
      ldw.get("codominant") is True and set(ldw.get("dominant_levers", [])) == {"L1", "L3"})

# schizophrenia-specific: the DOMAIN-RESTRICTION must be recorded (positive only)
drw = m.get("domain_restriction_witness", {})
pos_ok = drw.get("positive", {}).get("reached_by_levers") is True
neg_ok = drw.get("negative", {}).get("reached_by_levers") is False
cog_ok = drw.get("cognitive", {}).get("reached_by_levers") is False
check("domain-restriction witness records positive=reached, negative=NOT, cognitive=NOT",
      pos_ok and neg_ok and cog_ok)

result = {
    "title": ("L3 honesty pass (schizophrenia) -- dopamine antipsychotic-axis mechanism link graded [O], "
              "never derived; L1+L3 CO-DOMINANT; POSITIVE-domain restricted"),
    "inherited_from": ("analgesic_threshold_logic v2.0 M11 (DOI 10.5281/zenodo.20733420) via "
                       "bipolar/epilepsy/depression T-L gates"),
    "principle": ("gamma reads promoter threshold structure; the L3 dopamine RECEPTOR(DRD2/DRD4) + "
                  "SYNTHESIS/TRANSPORT(TH/SLC6A3) + serotonergic(HTR2A) + catabolic(COMT) signalling "
                  "mechanism is NOT captured by the read and is graded cited-biology [O]. The promoter "
                  "|h_sp| is held distinct from the sec.24 network over-ignition threshold; L1 and L3 are "
                  "verified CO-DOMINANT (schizophrenia's third distribution pattern); and the lever map is "
                  "verified to reach the POSITIVE domain ONLY (the negative-output and cognitive-wiring "
                  "domains are deficits/geometry a gain-reducing scalar lever cannot reach)."),
    "declared_l3": sorted(DECLARED_L3),
    "l3_targets_in_map": sorted(l3.keys()),
    "l3_count": len(l3), "lever_counts": counts,
    "codominant_L1_L3": codominant,
    "domain_restriction": {"positive_reached": pos_ok, "negative_reached": not neg_ok,
                           "cognitive_reached": not cog_ok},
    "per_target": per_target,
    "overall": "PASS" if not FAIL else "FAIL", "failures": FAIL,
}
json.dump(result, open(os.path.join(HERE, "schizophrenia_l3_honesty.json"), "w"), indent=1)
for g in sorted(l3.keys()):
    print(f"    L3 {g:8} -> {per_target[g]['grade_mechanism'][:72]}")
print("OVERALL:", "PASS" if not FAIL else f"FAIL {FAIL}")
sys.exit(1 if FAIL else 0)
