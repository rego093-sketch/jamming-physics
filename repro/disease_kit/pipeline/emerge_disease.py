#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emerge_disease.py  --  the CORE of the pivot.

NOT a classifier. Given a disease's CAUSAL GENE(S), this:

  1. PULLS each gene's real promoter DNA from NCBI (fetch/ncbi_gene_promoter.py,
     cache-backed -> offline reproducible). A gene whose DNA cannot be resolved is
     SUSPENDED, never guessed (author's rule: no DNA -> hold the analysis).

  2. EMERGES each gene through the VP DNA engine -- the SAME R19 jamming-bistable
     substrate that writes genes (engine/vp_neuro_engine.py, engine/organism/core.py):
        gamma     = promoter switch-threshold scale  (-mean NN stacking dG)   [V] read
        spinodal  = |h_sp| = 2*(gamma/3)^1.5         the discontinuous-flip threshold
        barrier   = gamma^2/4                          the basin (state-stability) depth
        dwell     = gamma^1.5/(K+brake)               relative run-length -> relative SIZE

  3. READS THE DISEASE AS A PERTURBATION of that switch. The DNA mutation does not
     create a new physics; it MOVES the switch the gene already encodes. The map from
     (role x mechanism) to a DIRECTION on the emergent quantity is FORCED [F]:

        role=brake        + GOF  -> brake over-active  -> dwell DOWN (over-suppression)
        role=brake        + LOF  -> brake released     -> dwell UP   (over-growth)
        role=accelerator  + LOF  -> drive lost         -> dwell DOWN (under-growth)
        role=accelerator  + GOF  -> drive excess       -> dwell UP
        role=channel      + LOF  -> gate stuck OFF basin (no current)
        role=channel      + GOF  -> gate stuck ON basin (runaway current)
        role=enzyme       + LOF  -> pathway throughput DOWN (substrate accumulates)
        role=master_TF/morphogen + LOF -> lineage/threshold not reached (organ absent/small)

     DIRECTION is forced & cited; absolute MAGNITUDE (how far the switch moves) is the
     runtime/Layer-2 quantity and is graded [O] -- it is not derivable from sequence.

FIREWALL (binding): gamma reads switch-threshold STRUCTURE only. No claim here is a
voltage, affinity, dose, expression level, or clinical effect.

Deterministic: pure arithmetic over cached sequences; 2x run -> identical sha256.
"""
import os, sys, json, math, hashlib

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
ENGINE = os.path.join(ROOT, "engine")
FETCH  = os.path.join(ROOT, "fetch")
for p in (ENGINE, FETCH, os.path.join(ENGINE, "organism")):
    if p not in sys.path: sys.path.insert(0, p)

import vp_neuro_engine as VN          # spinodal, barrier, dwell, Organ
import ncbi_gene_promoter as NF       # read_gene / read_panel (cache-backed)

# reference growth brake (the K+brake denominator term). A single UNIVERSAL modelling
# choice [F], identical for every gene; never per-disease-tuned. dwell ratios below are
# taken relative to this reference, so the absolute value cancels in the DIRECTION read.
BRAKE_REF = 0.5
K_DWELL   = 0.6

# (role, mechanism) -> (direction on the emergent quantity, prose). FORCED [F].
PERTURB = {
    ("brake","GOF"):       (-1, "brake over-active -> target over-suppressed"),
    ("brake","LOF"):       (+1, "brake released -> target over-driven"),
    ("accelerator","LOF"): (-1, "drive lost -> target under-driven"),
    ("accelerator","GOF"): (+1, "drive excess -> target over-driven"),
    ("channel","LOF"):     (-1, "gate stuck in OFF basin -> current lost"),
    ("channel","GOF"):     (+1, "gate stuck in ON basin -> current runaway"),
    ("enzyme","LOF"):      (-1, "pathway throughput down -> substrate accumulates"),
    ("enzyme","GOF"):      (+1, "pathway throughput up -> product excess"),
    ("master_TF","LOF"):   (-1, "lineage threshold not reached -> program absent/reduced"),
    ("master_TF","GOF"):   (+1, "lineage over-specified"),
    ("morphogen","LOF"):   (-1, "morphogen drive low -> length scale / threshold shifted down"),
    ("morphogen","GOF"):   (+1, "morphogen drive high -> length scale / threshold shifted up"),
    ("structural","LOF"):  (-1, "structural element deficient -> tissue integrity reduced"),
}

DIRWORD = {-1: "DOWN", +1: "UP", 0: "unchanged"}


def emerge_gene(read, role, mechanism):
    """Emerge one causal gene from its measured gamma and read its disease perturbation."""
    g = read["gamma"]
    spin = VN.spinodal(g)
    barr = VN.barrier(g)
    dwell = VN.dwell(g, BRAKE_REF, K_DWELL)
    direction, why = PERTURB.get((role, mechanism), (0, "perturbation direction not in forced map"))
    return {
        "gene": read["gene"],
        "gamma": round(g, 4),                                  # [V] reproducible read
        "spinodal_h_sp": round(spin, 5),                       # [V] R19 flip threshold
        "barrier": round(barr, 5),                             # [V] R19 basin depth
        "dwell_relative_size": round(dwell, 5),                # [F] relative size key
        "role": role, "disease_mechanism": mechanism,
        "perturbation_direction": DIRWORD[direction],          # [F] forced direction
        "perturbation_int": direction,
        "perturbation_reason": why,
        "ncbi": read["ncbi"],
        "grades": {
            "gamma_read": "[V] reproducible promoter switch-threshold read",
            "switch_threshold": "[V] R19 |h_sp| and barrier (locked forms)",
            "perturbation_direction": "[F] forced by (role x mechanism); cited biology",
            "perturbation_magnitude": "[O] OPEN -- how far the switch moves is runtime/Layer-2, not sequence-derivable",
        },
    }


def emerge_disease(spec, offline=False):
    """spec = {
         'disease': str, 'omim': str|None, 'summary': str,
         'organism': 'Homo sapiens',
         'causal_genes': [ {'gene':..,'role':..,'mechanism':..,'note':..,'src':..}, ... ],
         'emergent_axis': str   # what the perturbed switch controls (e.g. 'endochondral bone growth')
       }
       Returns the full structured emergence reading, with suspended genes listed.
    """
    organism = spec.get("organism", "Homo sapiens")
    syms = [cg["gene"] for cg in spec["causal_genes"]]
    panel = NF.read_panel(syms, organism=organism, offline=offline)
    per_gene, suspended = [], list(panel["suspended"])
    for cg in spec["causal_genes"]:
        r = panel["resolved"].get(cg["gene"].upper())
        if r is None:
            continue                                   # already in suspended
        eg = emerge_gene(r, cg["role"], cg["mechanism"])
        eg["note"] = cg.get("note", "")
        eg["src"] = cg.get("src", "")
        per_gene.append(eg)

    # the primary perturbed switch = the causal gene with the deepest barrier among the
    # direction-bearing genes (stiffest, most-committed switch); ties broken by |h_sp|.
    bearing = [g for g in per_gene if g["perturbation_int"] != 0]
    primary = None
    if bearing:
        primary = sorted(bearing, key=lambda g: (g["barrier"], g["spinodal_h_sp"]),
                         reverse=True)[0]

    net_dir = 0
    if primary is not None:
        net_dir = primary["perturbation_int"]

    out = {
        "disease": spec["disease"],
        "omim": spec.get("omim"),
        "summary": spec.get("summary", ""),
        "emergent_axis": spec.get("emergent_axis", ""),
        "organism": organism,
        "n_causal_genes": len(syms),
        "n_emerged": len(per_gene),
        "suspended_genes": suspended,
        "per_gene": sorted(per_gene, key=lambda g: g["barrier"], reverse=True),
        "primary_switch": None if primary is None else {
            "gene": primary["gene"], "role": primary["role"],
            "mechanism": primary["disease_mechanism"],
            "emergent_axis_direction": DIRWORD[net_dir],
            "reason": primary["perturbation_reason"],
        },
        "firewall": ("gamma reads promoter switch-threshold STRUCTURE only; perturbation DIRECTION "
                     "is forced+cited; MAGNITUDE is [O] (runtime/Layer-2, not sequence-derivable)."),
    }
    out["determinism_sha"] = hashlib.sha256(
        json.dumps(out, sort_keys=True).encode()).hexdigest()[:12]
    return out


def print_reading(rd):
    print("=" * 84)
    print(f"  DISEASE EMERGENCE:  {rd['disease']}" + (f"  (OMIM {rd['omim']})" if rd.get("omim") else ""))
    print(f"  emergent axis: {rd['emergent_axis']}")
    print("=" * 84)
    print(f"  {'gene':8} {'gamma':>7} {'|h_sp|':>8} {'barrier':>8} {'dwell':>8}  "
          f"{'role':12} {'mech':5} {'axis-dir':9}")
    for g in rd["per_gene"]:
        print(f"  {g['gene']:8} {g['gamma']:7.4f} {g['spinodal_h_sp']:8.5f} {g['barrier']:8.5f} "
              f"{g['dwell_relative_size']:8.5f}  {g['role']:12} {g['disease_mechanism']:5} "
              f"{g['perturbation_direction']:9}")
    if rd["primary_switch"]:
        ps = rd["primary_switch"]
        print(f"\n  PRIMARY PERTURBED SWITCH: {ps['gene']} ({ps['role']}, {ps['mechanism']}) "
              f"-> emergent axis {ps['emergent_axis_direction']}")
        print(f"    {ps['reason']}")
    if rd["suspended_genes"]:
        print(f"\n  SUSPENDED (no resolvable DNA): {', '.join(rd['suspended_genes'])}")
    print(f"\n  GRADES: gamma/threshold=[V] reproducible ; direction=[F] forced+cited ; magnitude=[O].")
    print(f"  determinism sha={rd['determinism_sha']}")
    print("=" * 84)


if __name__ == "__main__":
    # smoke test on a minimal inline spec (achondroplasia growth-plate)
    spec = {
        "disease": "Achondroplasia (smoke test)", "omim": "100800",
        "summary": "FGFR3 gain-of-function over-activates the growth-plate brake.",
        "emergent_axis": "endochondral (growth-plate) bone elongation",
        "causal_genes": [
            {"gene": "FGFR3", "role": "brake", "mechanism": "GOF",
             "note": "G380R constitutive activation", "src": "Shiang 1994 Cell 78:335"},
        ],
    }
    rd = emerge_disease(spec, offline=True)
    print_reading(rd)
