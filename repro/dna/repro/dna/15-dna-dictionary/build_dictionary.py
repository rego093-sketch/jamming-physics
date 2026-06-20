#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_dictionary.py — engine-generated DNA Dictionary (Part II of the whitepaper).

A Dictionary of *reads*, not *traits* (Strong's-style gloss): for each curated
locus it emits ONLY the mechanical Layer-1 read produced by the locked engine —
the material gamma, its R19 threshold scale (spinodal, barrier), GC, CpG density,
and whether the R19 well is bistable (can-fire). STATE (on/off), sign, dosage and
timing are runtime and are NOT assigned here; they are flagged as runtime.

Nothing is hand-assigned. Every value comes from dna_interpreter (the same locked
engine the paper uses, which re-derives human_SOX2 gamma = 1.287315 every run).

Run:   python3 build_dictionary.py
Output: expected/dictionary.json   (table + provenance + per-locus mechanical read)
"""
import sys, os, json, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_verify", "engine"))
SEQDIR = os.path.normpath(os.path.join(HERE, "..", "_verify", "inputs", "sequences_v6"))
sys.path.insert(0, ENGINE)
import dna_interpreter as D   # locked engine

def load_fa(path):
    return "".join(l.strip() for l in open(path) if not l.startswith(">")).upper()

def read_locus(name, seq):
    """Pure mechanical Layer-1 read. No role, no trait, no state assigned."""
    g  = D.gamma(seq)
    sp = D.switch_params(g)
    spin = sp["spinodal"]; bar = sp["barrier"]
    return {
        "locus": name,
        "length_bp": len(seq),
        "gamma": round(g, 9),                    # material: stacking stiffness
        "gc": round(D.gc_frac(seq), 9),
        "cpg_density": round(D.cpg_density(seq), 9),   # CpG handles (raw)
        "spinodal": round(spin, 9),              # R19 threshold scale |h_sp| = (2/3sqrt3) g^1.5
        "barrier": round(bar, 9),                # R19 barrier g^2/4
        "rest_basin_|s|": round(sp["rest_state_magnitude"], 9),
        "r19_bistable": bool(g > 0.0),           # can-fire: double-well exists for gamma>0
        "state_on_off": "RUNTIME (not readable)",
        "sign_dosage_timing": "RUNTIME (not readable)",
        "grade": "admissible (mechanical Layer-1 read)",
    }

def build():
    files = sorted(f for f in os.listdir(SEQDIR) if f.endswith(".fa"))
    entries = [read_locus(f[:-3], load_fa(os.path.join(SEQDIR, f))) for f in files]
    entries.sort(key=lambda e: e["gamma"])       # deterministic order: by gamma
    gammas = [e["gamma"] for e in entries]
    table = {
        "title": "DNA Dictionary — mechanical Layer-1 reads (engine-generated)",
        "engine": "repro/dna/_verify/engine/dna_interpreter.py (locked)",
        "definition": ("Each entry is the locked engine's mechanical read of one locus: material gamma, "
                       "its R19 threshold scale, GC, CpG density, and R19 bistability (can-fire). "
                       "STATE/sign/dosage/timing are runtime and are not assigned."),
        "n_loci": len(entries),
        "gamma_band": [min(gammas), max(gammas)],
        "anchor_check": {"human_SOX2": next(e["gamma"] for e in entries if e["locus"] == "human_SOX2")},
        "all_bistable": all(e["r19_bistable"] for e in entries),
        "entries": entries,
    }
    return table

if __name__ == "__main__":
    table = build()
    out = os.path.join(HERE, "expected", "dictionary.json")
    txt = json.dumps(table, ensure_ascii=False, indent=2, sort_keys=False)
    open(out, "w", encoding="utf-8").write(txt)
    print(f"wrote {out}")
    print(f"n_loci={table['n_loci']}  gamma_band={table['gamma_band']}  "
          f"human_SOX2={table['anchor_check']['human_SOX2']}  all_bistable={table['all_bistable']}")
