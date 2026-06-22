#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_nose_ssot.py — the numeric SINGLE SOURCE OF TRUTH for the nose-emergence HTML volume.

Run from the package root:   python3 tools/vp_nose_ssot.py        # → prints JSON + sha256

WHY THIS FILE EXISTS (VP-SPEC v1.8, C1 + Phase-4 drift gate).
The full HTML volume must display NO number that is not reproduced deterministically from the
FROZEN substrate + the MEASURED atlas (HTML↔code drift = 0). So every quantity the volume shows is
computed HERE, once, from:
    - inherited/vp_substrate.py   (the R19 switch: spinodal/barrier/settle/is_on/dwell/Organ) — FROZEN
    - inherited/organ_gamma.json  (γ LEVEL + A4 SHAPE, MEASURED from NCBI promoters)          — FROZEN
This module re-derives NOTHING of its own (γ is never fitted; FIREWALL #1–#3) and reuses the SAME
methods as the E1–E5 increments, so the volume's numbers are bit-for-bit consistent with them.

`ssot()` returns a flat {key: formatted-string} registry. `tools/build_volume.py` inserts each value
as `<span class="vp-num" data-key="{key}">{value}</span>`; `tools/gate_volume.py` re-derives this
registry and asserts every displayed span equals the freshly computed value (drift 0). Determinism is
proven by the 2×sha256 of the JSON dump (verify_seed.py [2] idiom).

stdlib + numpy (same as the foundation modules); no network.
"""
import os, sys, json, math, hashlib
from collections import OrderedDict

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(_HERE)
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import spinodal, barrier, settle, is_on, dwell, Organ   # FROZEN R19 primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# ----------------------------------------------------------------------------------------------
#  FIXED inputs — the FROZEN settle() defaults, never tuned (identical to every E* increment).
# ----------------------------------------------------------------------------------------------
N_STEPS, DT = 1500, 0.02
ROD_VISION_CNGB1_GAMMA = 1.4357     # CITED cross-sense ref (sibling eye seed; same gene/promoter)

# gene groups BY ATLAS NODE (stated, never selected to a target) ----------------------------------
def _by_node(node):
    return tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == node))

OR_GENES   = _by_node("olfactory_receptor")            # N=7
TRANSD     = ("GNAL", "ADCY3", "CNGA2", "CNGA4", "CNGB1", "ANO2")   # cascade order (biochemical)
ORGANISERS = _by_node("olfactory_neuron_identity")     # N=3
ANOSMIA    = _by_node("congenital_anosmia")            # N=4 (Kallmann)
CHANNELOP  = ("CNGA2", "CNGB1")                         # the two CNG channelopathy genes


def _rest(g):
    return -math.sqrt(g)


def _linear_control(g, h, s0=0.0, n=4000, dt=DT):
    """STRUCTURAL CONTROL — the substrate field with its cubic −s³ STRUCK OUT (ds/dt = −g·s + h):
    no double well, no spinodal, graded. Exists ONLY to prove the cubic is necessary (E2/E4)."""
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)
    return s


def _settle_rest(g, h):
    return settle(g, h, s0=_rest(g), n=N_STEPS, dt=DT)


# ==================================================================================================
#  the registry
# ==================================================================================================
def ssot():
    R = OrderedDict()

    def put(key, val):
        assert key not in R, f"duplicate SSOT key: {key}"
        R[key] = val

    # ---- E0 — counts + per-gene fundamentals (γ, h*, barrier, A4 shape amplitude) ---------------
    put("count.genes",      str(len(ATLAS)))
    put("count.or",         str(len(OR_GENES)))
    put("count.transd",     str(len(TRANSD)))
    put("count.organiser",  str(len(ORGANISERS)))
    put("count.anosmia",    str(len(ANOSMIA)))
    put("count.channelop",  str(len(CHANNELOP)))
    put("count.chapters",   "6")

    for sym, rec in ATLAS.items():
        g = rec["gamma"]; hstar = spinodal(g)
        put(f"gene.{sym}.gamma",   f"{g:.4f}")
        put(f"gene.{sym}.hstar",   f"{hstar:.5f}")
        put(f"gene.{sym}.barrier", f"{barrier(g):.4f}")
        put(f"gene.{sym}.a4",      f"{rec['shape_amplitude']:.5f}")
        put(f"gene.{sym}.gc",      f"{rec['gc']:.4f}")

    # corr(γ, GC) over all genes (the verifier's [3] statistic) ------------------------------------
    gam = [ATLAS[s]["gamma"] for s in ATLAS]
    gc  = [ATLAS[s]["gc"]     for s in ATLAS]
    n = len(gam); mg, mc = sum(gam)/n, sum(gc)/n
    cov = sum((gam[i]-mg)*(gc[i]-mc) for i in range(n))
    sg  = math.sqrt(sum((x-mg)**2 for x in gam)); sc = math.sqrt(sum((x-mc)**2 for x in gc))
    put("e0.corr_gamma_gc", f"{cov/(sg*sc):.3f}")
    put("e0.textured",      str(sum(1 for s in ATLAS if ATLAS[s]["shape_amplitude"] > 0.0)))

    # ---- E1 — combinatorial code ----------------------------------------------------------------
    N = len(OR_GENES)
    put("e1.capacity",  str(2 ** N))                 # 2^7 = 128
    put("e1.np1",       str(N + 1))                  # N+1 = 8
    or_order = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))   # threshold order
    for rank, sym in enumerate(or_order, 1):
        put(f"e1.rank.{sym}", str(rank))
    put("e1.or_order", ", ".join(or_order))

    # uniform-drive thermometer (substrate-derived): sweep h up, count distinct nested ON-sets -----
    thr_sorted = sorted(spinodal(ATLAS[s]["gamma"]) for s in OR_GENES)
    seen, counts = [], []
    for frac in (0.0, 0.50, 0.80, 0.90, 0.95, 1.00, 1.05, 1.20):
        h = frac * thr_sorted[-1] * 1.05
        on_set = tuple(s for s in or_order if _settle_rest(ATLAS[s]["gamma"], h) > 0.0)
        counts.append(len(on_set))
        if on_set not in seen:
            seen.append(on_set)
    put("e1.thermo_patterns", str(len(seen)))         # 4
    put("e1.thermo_counts",   "{" + ", ".join(str(c) for c in sorted(set(counts))) + "}")
    # an ABSTRACT (NOT measured) odorant vector driving only ranks 1 & 3 hard → a NON-nested pattern
    hot = {or_order[0], or_order[2]}
    drive_hi = 1.20 * thr_sorted[-1] * 1.05
    nonnested = tuple(s for s in or_order
                      if _settle_rest(ATLAS[s]["gamma"], drive_hi if s in hot else 0.0) > 0.0)
    put("e1.nonnested", ", ".join(nonnested))         # ('OR2J3','OR51E2')

    # ---- E2 — transduction switch ---------------------------------------------------------------
    for sym in TRANSD:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = _rest(g)
        sb = settle(g, 0.90 * hstar, s0=s0, n=N_STEPS, dt=DT)
        sa = settle(g, 1.10 * hstar, s0=s0, n=N_STEPS, dt=DT)
        put(f"e2.{sym}.s_below", f"{sb:+.4f}")
        put(f"e2.{sym}.s_above", f"{sa:+.4f}")
        put(f"e2.{sym}.jump",    f"{sa - sb:+.4f}")

    # CNGA2 discontinuity: off just below, on just above the spinodal ------------------------------
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = _rest(g)
    put("e2.flip.s_at_100", f"{settle(g, 1.00 * hstar, s0=s0, n=N_STEPS, dt=DT):+.4f}")  # off
    put("e2.flip.s_at_101", f"{settle(g, 1.01 * hstar, s0=s0, n=N_STEPS, dt=DT):+.4f}")  # on
    # cubic vs linear steepness (the necessity of the cubic) ---------------------------------------
    s_lo = settle(g, 0.99 * hstar, s0=s0, n=N_STEPS, dt=DT)
    s_hi = settle(g, 1.01 * hstar, s0=s0, n=N_STEPS, dt=DT)
    cubic_slope  = abs(s_hi - s_lo) / (0.02 * hstar)
    graded_slope = abs(_linear_control(g, 1.10 * hstar) - _linear_control(g, 0.90 * hstar)) / (0.20 * hstar)
    put("e2.cubic_slope",  f"{cubic_slope:.1f}")      # ≈177.2
    put("e2.graded_slope", f"{graded_slope:.3f}")     # ≈0.773
    put("e2.ratio",        f"{cubic_slope / graded_slope:.0f}")   # ≈229
    put("e2.hill_order",   "3")
    # cross-sense CNGB1 + cascade threshold order --------------------------------------------------
    put("e2.cngb1.gamma_olf", f"{ATLAS['CNGB1']['gamma']:.4f}")
    put("e2.cngb1.gamma_rod", f"{ROD_VISION_CNGB1_GAMMA:.4f}")
    put("e2.cascade_order", " → ".join(sorted(TRANSD, key=lambda s: spinodal(ATLAS[s]["gamma"]))))

    # ---- E3 — bulb map --------------------------------------------------------------------------
    org_order = sorted(ORGANISERS, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    for rank, sym in enumerate(org_order, 1):
        o = Organ(sym, ATLAS[sym]["gamma"])
        put(f"e3.rank.{sym}",  str(rank))
        put(f"e3.dwell.{sym}", f"{o.size(brake=0.5):.5f}")
    put("e3.org_order",   " → ".join(org_order))      # EBF1 → EMX2 → LHX2
    put("e3.capacity",    str(2 ** N))                # bijection preserves 2^N = 128
    # spatial thermometer patterns (same chain as E1, relabelled bijectively) ----------------------
    put("e3.spatial_patterns", str(len(seen)))        # 4

    # ---- E4 — congenital anosmia (DIRECTION-ONLY) -----------------------------------------------
    for sym in CHANNELOP:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = _rest(g)
        put(f"e4.{sym}.wt_above",  f"{settle(g, 1.10 * hstar, s0=s0, n=N_STEPS, dt=DT):+.4f}")
        put(f"e4.{sym}.lof_above", f"{_linear_control(g, 1.10 * hstar):+.4f}")
    # the channelopathy steepness (re-points E2's necessity result) --------------------------------
    put("e4.cubic_slope",  f"{cubic_slope:.0f}")      # ≈177
    put("e4.graded_slope", f"{graded_slope:.2f}")     # ≈0.77
    put("e4.ratio",        f"{cubic_slope / graded_slope:.0f}")   # ≈229
    # Kallmann organ-formation genes ---------------------------------------------------------------
    for sym in ANOSMIA:
        put(f"e4.kallmann.{sym}.gamma", f"{ATLAS[sym]['gamma']:.4f}")
        put(f"e4.kallmann.{sym}.hstar", f"{spinodal(ATLAS[sym]['gamma']):.5f}")
    put("e4.cngb1.gamma", f"{ATLAS['CNGB1']['gamma']:.4f}")
    put("e4.cngb1.hstar", f"{spinodal(ATLAS['CNGB1']['gamma']):.5f}")

    # ---- E5 — allergic (acquired) smell loss (DIRECTION-ONLY; mechanism cited to immune §11) -----
    or_thr  = [spinodal(ATLAS[s]["gamma"]) for s in OR_GENES]
    org_thr = [spinodal(ATLAS[s]["gamma"]) for s in ORGANISERS]
    H0          = 1.15 * max(or_thr)
    CIS_HEALTHY = 1.10 * max(org_thr)
    CIS_DAMAGED = 0.90 * min(org_thr)
    put("e5.h0", f"{H0:.5f}")

    def _osn_present(cis):
        return all(Organ(s, ATLAS[s]["gamma"]).present(cis) for s in ORGANISERS)

    def _percept(kappa, cis):
        if not _osn_present(cis):
            return 0
        return sum(1 for s in OR_GENES if _settle_rest(ATLAS[s]["gamma"], kappa * H0) > 0.0)

    kappa_sweep = (1.00, 0.95, 0.90, 0.86, 0.82, 0.60, 0.30, 0.00)
    for k in kappa_sweep:
        put(f"e5.cond.k{int(round(k*100)):03d}", str(_percept(k, CIS_HEALTHY)))
    put("e5.cond_block",   str(_percept(0.82, CIS_HEALTHY)))   # 3
    put("e5.cond_restore", str(_percept(1.00, CIS_HEALTHY)))   # 7
    put("e5.sensorineural", str(_percept(1.00, CIS_DAMAGED)))  # 0 (organ gone — no κ rescues)
    # organiser presence: healthy (present) vs damaged (absent) ------------------------------------
    for sym in ORGANISERS:
        o = Organ(sym, ATLAS[sym]["gamma"])
        put(f"e5.org.{sym}.healthy", "present" if o.present(CIS_HEALTHY) else "absent")
        put(f"e5.org.{sym}.damaged", "present" if o.present(CIS_DAMAGED) else "absent")

    return R


def dump():
    return json.dumps(ssot(), ensure_ascii=False, indent=1)


def main():
    txt = dump()
    print(txt)
    print("sha256: " + hashlib.sha256(txt.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
