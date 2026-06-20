#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cross_references.py  --  single-source loader for inherited/cross_references.json.

Live-wires the cross-system seams (NEXT_INSTRUCTIONS section 8 item 8): instead of the circulatory /
mind seams living as hand-typed prose scattered across sections 18 / 24 / 25, the seam layer
(repro/_seams/seam_wiring.py), the research battery (repro/_verify/stress_tests.py, DZS) and the site
generator (tools/build_docs.py) all read them from ONE file here. SSOT: digestive CONSUMES these
sibling-owned quantities; the siblings (circulatory / mind) are the SSOT for the OUT-seams they declare.

DISCIPLINE (neuro<->mind PROJECT_BOUNDARY): citation/pointer-only. This module is stdlib-only and imports
NO sibling code; the consumed circulatory hepatic interface is a VENDORED SNAPSHOT (verified once against
circulatory's engine at vendoring time, the source function named in the JSON), not a live import. Nothing
here feeds the hashed emergence core, so engine determinism (2x sha256 on circulate/emit) is untouched.
"""
import os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
_PATH = os.path.join(_HERE, "cross_references.json")


def load():
    """Return the full parsed seam manifest."""
    with open(_PATH, encoding="utf-8") as fh:
        return json.load(fh)


def seam_keys():
    """The seam record keys (skips the leading _doc / _grade_legend metadata)."""
    return [k for k in load() if not k.startswith("_")]


def for_seam(key):
    """Return one seam record by key."""
    return load()[key]


def consumed_circulatory_hepatic():
    """The vendored circulatory hepatic interface snapshot that sections 24/25 consume as the
    delivery substrate. SSOT: this is circulatory's hepatic_clearance() output, recorded here once."""
    return for_seam("circulatory_hepatic_interface")["vendored_snapshot"]


def as_prose(key):
    """Compact one-line summary of a seam, for inline use in a value dict or a page."""
    r = for_seam(key)
    owner = r.get("owner_volume", "?")
    doi = r.get("owner_concept_doi", "pending")
    return ("%s | owner %s (DOI %s) | %s [%s]"
            % (r["seam"], owner, doi, r.get("seam_to_digestive", r.get("boundary_clause", "")), r["grade"]))


if __name__ == "__main__":
    keys = seam_keys()
    print("cross_references.json seam keys:", keys)
    for k in keys:
        print("\n--- %s ---" % k)
        print(as_prose(k))
    print("\nconsumed circulatory hepatic snapshot:", consumed_circulatory_hepatic())
