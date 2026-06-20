#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_references.py  --  single-source loader for inherited/cross_references.json.

Live-wires the cross-volume gene-key references (handoff section 4 item 2): instead of the VHL/HFE
cross-references living as hand-typed prose in several places, both the research battery
(repro/_verify/stress_tests.py, T22/T23) and the site generator (tools/build_docs.py) read them from
ONE file here. SSOT: circulatory consumes these references; the entities themselves are OWNED and
derived by disease_wp (MASTER MAP 6.1). stdlib only; nothing here feeds the hashed emergence core, so
determinism (2x sha256 on circulate/emit) is untouched.
"""
import os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_PATH = os.path.join(_HERE, "cross_references.json")


def load():
    """Return the full parsed cross-reference manifest."""
    with open(_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def for_entity(key):
    """Return one cross-reference record by key ('hereditary_RCC' | 'hereditary_HCC')."""
    return load()[key]


def as_prose(key):
    """Compact one-line summary of a cross-reference, for inline use in a value dict or a page."""
    r = for_entity(key)
    return ("%s (gene-key %s, %s) is owned by %s (%s); seam: %s [%s]"
            % (r["entity"], r["gene_key"], r["locus"], r["owner_volume"],
               r["ownership_clause"], r["seam_to_circulatory"], r["grade"]))


if __name__ == "__main__":
    m = load()
    keys = [k for k in m if not k.startswith("_")]
    print("cross_references.json keys:", keys)
    for k in keys:
        print("\n--- %s ---" % k)
        print(as_prose(k))
