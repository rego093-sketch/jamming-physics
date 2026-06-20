#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_dna_emergence.py  —  §20b DNA-emergence inheritance, made EXPLICIT and ACTIVE.

The whole emergence chain stands on one inherited fact: the measured promoter gamma of a
master gene, read on the shared R19 switch, EMERGES the cell/organ. This volume already used
it (sec.12 sensory-organ-4d, sec.20 atlas), but the inheritance was implicit. This module makes
it explicit: it loads the explicit inherited DNA-grounded gamma (inherited/organ_gamma.json),
and for every nociceptor-lineage gene it emerges the element via THIS volume's own R19 Organ
primitive — presence threshold = spinodal(gamma), emergence order = argsort(spinodal(gamma)),
relative dwell ~ gamma^1.5 — exactly the DNA volume's rule (form <- gamma; order = argsort
spinodal). It then asserts the gamma it emerges from is bit-for-bit the measured atlas gamma the
analgesic map (sec.21) and the neuropathic-pain dynamics (sec.22) read, so all three sit on ONE
inherited DNA grounding. Nothing is fitted; gamma is measured.

DNA volume: 4D DNA Blueprint, concept DOI 10.5281/zenodo.20471407 (form <- gamma, Layer 1).

Run:  python3 verify_dna_emergence.py  ->  expected/dna_emergence.json
"""
import os, sys, json

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, "..", "..", ".."))   # package root
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
EXPECT = os.path.join(HERE, "expected")
sys.path.insert(0, ENGINE)
import vp_neuro_engine as VN     # spinodal/barrier + Organ (dwell ~ gamma^1.5) — locked R19

INHERITED = os.path.join(ROOT, "inherited", "organ_gamma.json")
ATLAS     = os.path.join(ENGINE, "data", "full_sensory_gamma.json")


def main():
    os.makedirs(EXPECT, exist_ok=True)
    inh = json.load(open(INHERITED))["genes"]
    atlas = json.load(open(ATLAS))["genes"]

    # (1) the inherited DNA-grounded gamma must be bit-for-bit the measured atlas gamma
    grounding_match = all(inh[g]["gamma"] == atlas[g]["gamma"] for g in inh)

    # (2) emerge each lineage element via the shared R19 Organ primitive (form <- gamma)
    rows = []
    for gene, rec in inh.items():
        g = rec["gamma"]
        org = VN.Organ(gene, g, master=gene, layer="somatosensory")
        rows.append(dict(
            gene=gene, gamma=g,
            presence_threshold_spinodal=round(VN.spinodal(g), 6),   # discontinuous presence gate
            barrier=round(VN.barrier(g), 6),                        # basin stability
            relative_dwell=round(org.size(brake=0.5), 6),           # dwell ~ gamma^1.5 -> relative size
        ))

    # (3) emergence ORDER = argsort(spinodal(gamma)) — the DNA volume's gene-clock rule
    order = [r["gene"] for r in sorted(rows, key=lambda r: r["presence_threshold_spinodal"])]

    out = dict(
        module="20b-dna-emergence-inheritance",
        dna_volume=dict(paper_id="dna", doi="10.5281/zenodo.20471407",
                        rule="form <- gamma (Layer 1); emergence order = argsort(spinodal(gamma))"),
        grounding=("the measured promoter gamma is the SINGLE inherited DNA fact; sec.21 (analgesic |h_sp|) "
                   "and sec.22 (neuropathic-pain dynamics) read this same gamma — one grounding, three readings"),
        inherited_gamma_is_measured_atlas=grounding_match,
        n_lineage_genes=len(rows),
        emergence_order_by_spinodal=order,
        elements=sorted(rows, key=lambda r: -r["presence_threshold_spinodal"]),
        firewall="gamma is MEASURED [V], never fitted; identity/order owned by DNA volume; this volume emerges via R19",
    )
    json.dump(out, open(os.path.join(EXPECT, "dna_emergence.json"), "w"), indent=1)

    print("=" * 68)
    print("§20b DNA-emergence inheritance (explicit & active)")
    print("-" * 68)
    print(f"inherited gamma == measured atlas : {grounding_match}")
    print(f"lineage genes emerged via R19     : {len(rows)}")
    print(f"emergence order (argsort spinodal): {' < '.join(order)}")
    print("=" * 68)
    if not grounding_match:
        sys.exit("FAIL: inherited DNA-grounded gamma is not the measured atlas gamma")
    print("PASS — nociceptor lineage emerges from one inherited measured gamma (form <- gamma)")


if __name__ == "__main__":
    main()
