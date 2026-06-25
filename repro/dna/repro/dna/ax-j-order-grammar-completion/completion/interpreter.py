# -*- coding: utf-8 -*-
"""
completion.interpreter -- assemble the whole Appendix-J reading and stamp it with a deterministic
hash.

The reading_hash is SHA-256 applied TWICE over the canonical JSON of the full reading (the same
double-hash discipline as the prior appendices). Any drift in any number changes the hash, so the
gate's determinism check (run twice, compare) is exact.
"""
import json
import hashlib

from . import (lock, cascade, coupled, timing, nulltest, grammar, declaration,
               grading)


def interpret():
    """The complete Appendix-J reading: lock manifest, the filled-kit cascade structure, the
    coupled theorem under OR / AND-threshold-k / sequence-drive, the real-data null + floor re-test,
    the timing sub-clock, the grammar statement, the honest ledger and declaration."""
    return {
        "appendix": "J -- the order-grammar COMPLETION",
        "lock_manifest": lock.lock_manifest(),
        "cascade": {
            "is_dag": cascade.is_dag()[0],
            "n_genes": len(lock.driver_gamma()),
            "n_edges": len(lock.cascade_edges()),
            "n_sources": len(cascade.sources()),
            "max_depth": cascade.max_depth(),
            "axial_chain": cascade.longest_path(),
            "composite_order_table": cascade.order_table(),
        },
        "coupled_theorem": {
            "or_partial_order_compliance": coupled.or_partial_order_compliance(),
            "threshold_k_wavefront": coupled.threshold_k_wavefront(alpha=1.0),
            "and_delays_convergent_nodes": coupled.and_delays_convergent_nodes(),
            "sequence_drive_preserves_order": coupled.sequence_drive_preserves_order(),
            "coupled_vs_keys": coupled.coupled_vs_keys(),
        },
        "timing": timing.read(),
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
            "o1_floor_met_but_L": (r["declaration"]["o1_floor_met_on_filled_kit"]
                                   and r["grading"]["o1_is_L_not_V"]),
            "physical_complete": r["declaration"]["physical_complete"]}
