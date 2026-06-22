#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
frontal_registry.py  --  the frontal sim's OWN module manifest
==============================================================
Lists the frontal-local modules and their FROZEN result digests.  This is the
frontal analogue of the atlas registry, but it lists ONLY frontal modules and is
consumed ONLY by frontal_gate.py.  It NEVER references the mind atlas registry or
the mind atlas runner.

To add a module: run it once (it writes results.json + expected_*.json), then add
an entry here with the frozen sha it produced.
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")

FRONTAL_MODULES = [
    {
        "name": "frontal_f1_temporal_holding",
        "module_dir": "_frontal",
        "module_file": "frontal_f1_temporal_holding.py",
        "entry": "frontal_f1_results",
        "results_json": "frontal_f1_temporal_holding_results.json",
        "expected_json": "expected_frontal_f1_temporal_holding_sha256.json",
        "frozen_sha256": "21bf28f6e91e6fa781bebb35d6bf2782e46bd0ae5586012959ae854594b98e66",
        "axis": "D (proposed frontal temporal-holding axis)",
        "headline": "cortical node = NOT a gatherer + a fast broadcaster [V mech]; the "
                    "engine reproduces NO robust frontal-lesion behavioural phenotype -- "
                    "temporal-holding negligible [O] and leucotomy perseveration sign-flips "
                    "under anti-tuning [O]; only static structure + 'removal nearly silent' "
                    "are robust (Hard Limit 1, strongest form)",
    },
    # F2 (stereotypy T x W x E0) and F3 (cohort O x W x T x D double dissociation)
    # will be appended here once built.
]


def expected_sha_on_disk(entry):
    p = os.path.join(ROOT, entry["module_dir"], entry["expected_json"])
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return d.get(entry["results_json"])


if __name__ == "__main__":
    print("frontal registry -- modules:")
    for m in FRONTAL_MODULES:
        disk = expected_sha_on_disk(m)
        match = (disk == m["frozen_sha256"]) if disk else None
        print(f"  {m['name']:<34} frozen={m['frozen_sha256'][:16]}... on_disk_match={match}")
