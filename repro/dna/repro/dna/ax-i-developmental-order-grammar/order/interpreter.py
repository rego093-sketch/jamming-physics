# -*- coding: utf-8 -*-
"""
order.interpreter -- assemble the whole Appendix-I reading and stamp it with a deterministic hash.

The reading_hash is SHA-256 applied TWICE over the canonical JSON of the full reading (the same
double-hash discipline as the prior appendices). Any drift in any number changes the hash, so the
gate's determinism check (run twice, compare) is exact.
"""
import json
import hashlib

from . import lock, cascade, coupled, nulltest, grammar, declaration, grading


def interpret():
    """The complete Appendix-I reading: lock manifest, cascade structure, the coupled theorem,
    the real-data null/discovery, the grammar statement, the honest ledger and declaration."""
    return {
        "appendix": "I -- developmental ORDER grammar",
        "lock_manifest": lock.lock_manifest(),
        "cascade": {
            "is_dag": cascade.is_dag()[0],
            "n_sources": len(cascade.sources()),
            "max_depth": cascade.max_depth(),
            "axial_chain": cascade.longest_path(),
            "composite_order_table": cascade.order_table(),
        },
        "coupled_theorem": {
            "partial_order_compliance": coupled.partial_order_compliance(),
            "coupled_vs_keys": coupled.coupled_vs_keys(),
            "resort_on_edge": coupled.resort_on_edge(),
        },
        "real_data": nulltest.read(),
        "grammar": grammar.read(),
        "grading": grading.read(),
        "declaration": declaration.declare(),
    }


def _canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def reading_hash():
    """SHA-256 twice over the canonical reading."""
    blob = _canonical(interpret()).encode("utf-8")
    h1 = hashlib.sha256(blob).digest()
    h2 = hashlib.sha256(h1).hexdigest()
    return h2


def read():
    r = interpret()
    return {"reading_hash_sha256x2": reading_hash(),
            "headline": r["declaration"]["headline"],
            "grade_counts": r["grading"]["counts"],
            "physical_complete": r["declaration"]["physical_complete"]}
