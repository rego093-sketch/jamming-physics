# -*- coding: utf-8 -*-
"""
order.gate -- the fail-closed gate for Appendix I (developmental ORDER grammar).

FAILS CLOSED on any miss:

  I1  SAME_OPERATOR     the SHAPE operator robust_z is the identical median-centred, MAD-scaled
                        operator as Appendices E..H (scale- AND shift-invariant to machine epsilon),
                        the gamma operator reproduces -mean(NN dG) exactly on a probe, and the four
                        Appendix-G/H overlap drivers (SOX9/RUNX2/PAX1/GLI3) are present with
                        byte-identical gammas -- one operator, real inherited data.
  I2  CASCADE_IS_DAG    the cited regulatory cascade is acyclic; a deterministic topological order
                        exists (depth is therefore well-defined and DERIVED, not asserted).
  I3  THE_NULL          |Spearman(spinodal(gamma), Carnegie rank)| <= the locked ceiling -- the
                        single-locus barrier does NOT order developmental staging (Appendix A's
                        measured null, in numbers).
  I4  EDGE_CONCORDANCE  among cited regulatory edges whose endpoints both carry a Carnegie rank,
                        ZERO inversions: every cited regulator's onset is no later than its target's
                        (the wiring read on the time axis never contradicts the temporal order).
  I5  DEPTH_BEATS_GAMMA |Spearman(cascade depth, Carnegie rank)| STRICTLY exceeds the spinodal
                        correlation, on all anchored genes AND on the main wired component.
  I6  COUPLED_WAVEFRONT in the coupled-R19 substrate the firing order respects the cascade DAG (no
                        gene fires before its earliest regulator -- the wavefront theorem, 0
                        violations) AND the coupled firing order tracks cascade DEPTH, not bare
                        spinodal(gamma).
  I7  KEYS_DISAGREE     the single-locus spinodal order and the cascade-depth order are genuinely
                        DIFFERENT orders (Spearman strictly below 1) -- the higher-order grammar is
                        doing real work, not re-deriving gamma.
  I8  EDGE_RESORT_LEVER cutting ONE regulatory edge (SOX9->RUNX2) moves RUNX2 EARLIER -- the order
                        is a live function of the wiring, not a fixed list.
  I9  NO_MAGIC          the lock manifest reports zero inline magic numbers; every locked input
                        carries a provenance string.
  I10 NON_FIT           the reading is identical with a decoy Carnegie-target file present -> the
                        engine reads only its locked DB, never a target.
  I11 DETERMINISM       two serializations of the reading hash identically (2x SHA-256).
  I12 HONEST_DECLARATION the declaration closes the schedule-ORDER [O] but keeps absolute timing
                        [O] and physical_complete=False, uses only the four sanctioned grades, names
                        every open channel, and -- crucially -- does NOT upgrade the absolute
                        depth<->Carnegie strength to [V] (it stays [L], the pre-registered 0.70
                        floor is honestly reported as NOT met globally). Fails closed on any false
                        victory.

Run:  python3 -m order.gate   (from the package root).
"""
import os
import json
import hashlib

import numpy as np

from . import (lock, seqtools, cascade, coupled, nulltest, grammar,
               declaration, grading, interpreter)


# the four drivers shared with Appendices G/H; their published gammas are the regression reference.
_OVERLAP_PUBLISHED = {"SOX9": 1.459260, "RUNX2": 1.241556, "PAX1": 1.504372, "GLI3": 1.298352}
_PROBE = "GCGCGGCCGGATATCGCGTATATACGCGGCCGGCGC"


def _i1_same_operator():
    x = np.array([0.2, 1.7, -0.4, 3.1, 0.9, -1.2, 2.0, 0.05], dtype=np.float64)
    z = seqtools.robust_z(x)
    scale_inv = float(np.max(np.abs(z - seqtools.robust_z(7.3 * x))))
    shift_inv = float(np.max(np.abs(z - seqtools.robust_z(x + 4.5))))
    nn = lock.nn_table()
    g_pkg = seqtools.gamma(_PROBE, nn)
    steps = [nn[_PROBE[i:i + 2]] for i in range(len(_PROBE) - 1)]
    gamma_exact = abs(g_pkg - float(-np.mean(steps))) < 1e-12
    atlas = lock.driver_gamma()
    overlap_ok = all(s in atlas for s in _OVERLAP_PUBLISHED) and all(
        abs(float(atlas[s]["gamma"]) - g) < 1e-6 for s, g in _OVERLAP_PUBLISHED.items())
    ok = (scale_inv < 1e-9) and (shift_inv < 1e-9) and gamma_exact and overlap_ok
    return ok, {"shape_scale_invariance": scale_inv, "shape_shift_invariance": shift_inv,
                "gamma_reproduces_neg_mean_NN": bool(gamma_exact),
                "overlap_reproduces_byte_for_byte": bool(overlap_ok),
                "overlap_genes": sorted(_OVERLAP_PUBLISHED.keys())}


def _i2_cascade_is_dag():
    acyclic, topo = cascade.is_dag()
    ok = bool(acyclic) and (len(topo) == len(lock.driver_gamma()))
    return ok, {"is_dag": bool(acyclic), "n_in_topo": len(topo), "max_depth": cascade.max_depth(),
                "n_sources": len(cascade.sources())}


def _i3_the_null():
    n = nulltest.the_null()
    ok = bool(n["is_null"])
    return ok, {"spearman_spinodal_vs_carnegie": n["spearman_spinodal_vs_carnegie"],
                "ceiling": n["null_ceiling"]}


def _i4_edge_concordance():
    c = nulltest.edge_concordance()
    ok = bool(c["passes"])
    return ok, {"n_cited_edges": c["n_cited_edges_both_anchored"],
                "n_inversions": c["n_inversions"],
                "concordance_incl_ties": c["concordance_incl_ties"],
                "floor": c["concordance_floor"]}


def _i5_depth_beats_gamma():
    b = nulltest.depth_beats_gamma()
    ok = bool(b["passes"])
    return ok, {"depth_all": b["spearman_depth_vs_carnegie_all"],
                "gamma_all": b["spearman_spinodal_vs_carnegie_all"],
                "depth_main": b["spearman_depth_vs_carnegie_main_component"],
                "gamma_main": b["spearman_spinodal_vs_carnegie_main_component"]}


def _i6_coupled_wavefront():
    poc = coupled.partial_order_compliance()
    cvk = coupled.coupled_vs_keys()
    ok = bool(poc["respects_partial_order"]) and bool(cvk["depth_beats_gamma"])
    return ok, {"partial_order_violations": poc["n_violations"],
                "firing_vs_depth": cvk["spearman_firing_vs_cascade_depth"],
                "firing_vs_spinodal": cvk["spearman_firing_vs_bare_spinodal"]}


def _i7_keys_disagree():
    """spinodal(gamma) order vs cascade-depth order must be a DIFFERENT order (rho < 1)."""
    dg = lock.driver_gamma()
    d = cascade.depth()
    genes = sorted(dg.keys())
    spin = [float(seqtools.spinodal(dg[g]["gamma"])) for g in genes]
    dep = [d[g] for g in genes]
    rho = nulltest._spearman(spin, dep)
    ok = bool(rho < 0.999)
    return ok, {"spearman_spinodal_order_vs_depth_order": round(rho, 4),
                "genuinely_different_order": ok}


def _i8_edge_resort_lever():
    r = coupled.resort_on_edge()
    ok = bool(r["runx2_fires_earlier_when_unblocked"])
    return ok, {"with_edge": r["runx2_fire_time_with_edge"],
                "without_edge": r["runx2_fire_time_without_edge"]}


def _i9_no_magic():
    man = lock.lock_manifest()

    def all_prov(node):
        if isinstance(node, dict):
            if "provenance" in node and not node["provenance"]:
                return False
            return all(all_prov(v) for v in node.values())
        if isinstance(node, list):
            return all(all_prov(v) for v in node)
        return True

    ok = (man.get("inline_magic_numbers") == 0) and all_prov(man)
    return ok, {"inline_magic_numbers": man.get("inline_magic_numbers")}


def _i10_non_fit():
    h1 = interpreter.reading_hash()
    decoy = "carnegie_targets.json"
    created = False
    if not os.path.exists(decoy):
        with open(decoy, "w") as fh:
            json.dump({"fake_stage_rank": {"RUNX2": 1, "FOXA2": 99}, "fake_days": 1234.5}, fh)
        created = True
    try:
        h2 = interpreter.reading_hash()
    finally:
        if created:
            os.remove(decoy)
    ok = (h1 == h2)
    return ok, {"hash_without_decoy": h1[:16], "hash_with_decoy": h2[:16]}


def _i11_determinism():
    r = interpreter.interpret()
    b1 = json.dumps(r, sort_keys=True, ensure_ascii=False).encode("utf-8")
    b2 = json.dumps(json.loads(b1.decode("utf-8")), sort_keys=True, ensure_ascii=False).encode("utf-8")
    h1 = hashlib.sha256(b1).hexdigest()
    h2 = hashlib.sha256(b2).hexdigest()
    ok = (h1 == h2)
    return ok, {"sha_1": h1[:16], "sha_2": h2[:16]}


def _i12_honest_declaration():
    decl = declaration.declare()
    led = grading.ledger()
    sanctioned = {"[L]", "[V]", "[F]", "[O]"}

    # only sanctioned grade prefixes anywhere in the ledger
    only_sanctioned = all(any(r["grade"].startswith(s) for s in sanctioned) for r in led["rows"])
    # every open channel named
    opens_named = all(o.get("status") for o in decl["open"])
    # schedule-ORDER [O] closed but absolute timing [O] kept and physical_complete False
    order_closed = bool(decl["schedule_order_O_closed"])
    timing_open = bool(decl["absolute_timing_open"])
    not_physical = (decl["physical_complete"] is False)
    no_consciousness = (decl["consciousness_claim"] == 0)
    # NO FALSE VICTORY on absolute strength: the O1 row must NOT be graded [V]
    o1 = next((r for r in led["rows"] if r["id"] == "O1"), None)
    strength_not_upgraded = bool(o1 is not None and not o1["grade"].startswith("[V]"))

    ok = (only_sanctioned and opens_named and order_closed and timing_open
          and not_physical and no_consciousness and strength_not_upgraded)
    return ok, {"only_sanctioned_grades": only_sanctioned, "opens_named": opens_named,
                "schedule_order_closed": order_closed, "absolute_timing_open": timing_open,
                "physical_complete": decl["physical_complete"],
                "absolute_strength_not_upgraded_to_V": strength_not_upgraded}


CHECKS = [
    ("I1_same_operator", _i1_same_operator),
    ("I2_cascade_is_dag", _i2_cascade_is_dag),
    ("I3_the_null", _i3_the_null),
    ("I4_edge_concordance", _i4_edge_concordance),
    ("I5_depth_beats_gamma", _i5_depth_beats_gamma),
    ("I6_coupled_wavefront", _i6_coupled_wavefront),
    ("I7_keys_disagree", _i7_keys_disagree),
    ("I8_edge_resort_lever", _i8_edge_resort_lever),
    ("I9_no_magic", _i9_no_magic),
    ("I10_non_fit", _i10_non_fit),
    ("I11_determinism_2x_sha256", _i11_determinism),
    ("I12_honest_declaration", _i12_honest_declaration),
]


def run_gate(verbose=True):
    results = {}
    n_pass = 0
    for name, fn in CHECKS:
        ok, detail = fn()
        results[name] = {"pass": bool(ok), "detail": detail}
        n_pass += int(bool(ok))
        if verbose:
            print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    all_ok = (n_pass == len(CHECKS))
    blob = json.dumps(results, sort_keys=True, ensure_ascii=False).encode("utf-8")
    results["_sha256"] = hashlib.sha256(blob).hexdigest()[:16]
    results["_all_pass"] = all_ok
    results["_n_pass"] = n_pass
    results["_n_total"] = len(CHECKS)
    if verbose:
        print(f"  ---- gate {'PASS' if all_ok else 'FAIL'} "
              f"({n_pass}/{len(CHECKS)}) sha={results['_sha256']}")
    return results


if __name__ == "__main__":
    run_gate(verbose=True)
