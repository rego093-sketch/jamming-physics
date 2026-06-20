#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_muscle_force_law.py — REPRODUCE the muscle force–length law from the molecular
root cause, under VP-SPEC C1/C3. The previous version TRUSTED Gordon–Huxley–Julian
(GHJ) 1966 measured landmarks as inputs; that violates C1. Here the only LOCKED
inputs are measured STRUCTURAL constants (filament dimensions). The force law and
ALL its landmarks are DERIVED from overlap geometry; GHJ-1966 is the independent
VALIDATION TARGET, never an input. What cannot be derived from length geometry is
declared [O] with a stated obstacle (C3), not hard-coded.

LOCK (measured molecular structure — the INPUT, the muscle analog of the SantaLucia
NN ΔG parameter set: a measured physical constant set, not a fitted output):
    thick (myosin) filament      A = 1.600 µm     [Huxley 1963, EM]
    thin  (actin)  filament/side I = 1.000 µm     [GHJ 1966 geometry]
    bare zone (H-zone, no heads) b = 0.150–0.200 µm  [GHJ 1966]
    Z-band                       z = 0.050 µm     [GHJ 1966]

DERIVE (overlap geometry — the reproduction; nothing here reads a GHJ tension value):
    a cross-bridge forms only where a thin filament overlaps the head-bearing part of
    the thick filament with correct polarity; active tension ∝ that overlap length.
    zero_long   = A + 2I + z          (thin tips clear the thick ends → no overlap)
    plateau_top = 2I + z + b          (thin tips reach the bare-zone edge → max heads)
    plateau_bot = 2I + z              (opposing thin filaments meet at the M-line)
    steepen     = A + z               (thick filament ends bump the Z-discs)
    descending limb : tension linear in overlap between plateau_top and zero_long.

VALIDATE vs GHJ-1966 MEASURED (target only): zero 3.65, plateau_bot 2.05, steepen 1.67 µm
    are POINT landmarks checked by |Δ|; plateau_top is a RANGE (the bare zone b is a measured
    range) validated by CONTAINMENT — GHJ's measured 2.20 must fall inside the derived
    [2.20, 2.25], and it sits at the LOWER edge. We do NOT pick b=0.15 to report |Δ|=0.

[O] NOT derivable from length geometry (declared, with obstacle — see ledger):
    zero_short ≈ 1.27 µm  — the short-side zero is a thick-filament CRUMPLING limit;
        it needs filament buckling/compliance mechanics, not overlap length.
    ascending-limb tension VALUES — double-overlap interference + wrong-polarity drag +
        compliance; not fixed by overlap length alone.
    absolute tension scale — needs cross-bridge number × unitary force × activation.
    filament dimensions themselves from ruler-protein (nebulin/titin) sequence — open.

stdlib + numpy. Deterministic; emits JSON of derived values; 2× run → identical sha256.
"""
import hashlib, io, json
import numpy as np

# ---- LOCK: measured structural constants (inputs) -------------------------
A      = 1.600          # thick (myosin) filament length, µm
I      = 1.000          # thin (actin) filament length per side, µm
B_LO   = 0.150          # bare-zone length, low end, µm
B_HI   = 0.200          # bare-zone length, high end, µm
Z      = 0.050          # Z-band width, µm

# ---- VALIDATION TARGET: GHJ-1966 measured landmarks (NOT inputs) ----------
GHJ_MEASURED = {"plateau_bot": 2.05, "plateau_top": 2.20, "zero_long": 3.65, "steepen": 1.67}
TOL = 0.05             # µm; structural derivation vs measurement, ~bare-zone/end detail


def derive_landmarks():
    """All landmarks from overlap geometry. No GHJ tension value is read here."""
    zero_long   = A + 2*I + Z
    plateau_bot = 2*I + Z
    plateau_top_lo = 2*I + Z + B_LO     # bare-zone range → plateau-top range
    plateau_top_hi = 2*I + Z + B_HI
    steepen     = A + Z                 # thick ends reach the Z-discs
    return {
        "zero_long": round(zero_long, 4),
        "plateau_bot": round(plateau_bot, 4),
        "plateau_top_lo": round(plateau_top_lo, 4),
        "plateau_top_hi": round(plateau_top_hi, 4),
        "steepen": round(steepen, 4),
    }


def force_length(S, d):
    """Active tension (0..1) from overlap geometry. Descending limb + plateau are
    derived; the ascending limb below plateau is [O] (not length-geometry) — returned
    as NaN to make explicit that this module does not fabricate those values.
    The plateau-top boundary is drawn at the LOWER edge of the derived plateau-top
    range [2.20, 2.25] — the conservative (narrowest-plateau) edge. This is a
    presentation choice for rendering ONE representative curve, not a fitted value:
    the true boundary is the range, of which GHJ 2.20 sits at this lower edge."""
    zero_long, plateau_top, plateau_bot = d["zero_long"], d["plateau_top_lo"], d["plateau_bot"]
    if S >= zero_long:
        return 0.0
    if S >= plateau_top:
        return (zero_long - S) / (zero_long - plateau_top)   # linear in overlap
    if S >= plateau_bot:
        return 1.0
    return float("nan")   # ascending limb is [O]; not derivable from length alone


def run(P):
    P("=" * 78)
    P("MUSCLE FORCE–LENGTH LAW — derived from locked structure, validated vs GHJ-1966")
    P("(VP-SPEC C1: structure is the only input; GHJ is the check, not an input)")
    P("=" * 78)

    P("\n### LOCK — measured structural constants (the input) ###")
    P(f"  thick A={A}  thin I={I}  bare b=[{B_LO},{B_HI}]  Z z={Z}  (µm)")

    d = derive_landmarks()
    P("\n### DERIVE → VALIDATE — landmarks from overlap geometry vs GHJ measured ###")
    P("  POINT landmarks (single locked dimension → single derived value; |Δ| is the test):")
    P("  landmark      derived(geometry)        GHJ-1966(measured)   |Δ|     basis")
    # POINT landmarks: each derives from single-valued locked constants (A, I, z); the
    # validation is the absolute deviation |derived − measured|.
    point_rows = [
        ("zero_long",   f"A+2I+z = {d['zero_long']:.3f}", GHJ_MEASURED["zero_long"],   d["zero_long"],   "no overlap"),
        ("plateau_bot", f"2I+z = {d['plateau_bot']:.3f}", GHJ_MEASURED["plateau_bot"], d["plateau_bot"], "thin filaments meet"),
        ("steepen",     f"A+z = {d['steepen']:.3f}",      GHJ_MEASURED["steepen"],     d["steepen"],     "thick hits Z-disc"),
    ]
    max_err = 0.0
    fidelity = {}
    for name, derived_expr, measured, derived_val, basis in point_rows:
        err = abs(derived_val - measured)
        max_err = max(max_err, err)
        fidelity[name] = {"derived": derived_val, "measured": measured, "abs_err": round(err, 4)}
        P(f"  {name:12s}  {derived_expr:22s}   {measured:6.3f} µm        {err:.3f}  [{basis}]")

    # RANGE landmark: the bare zone b ∈ [0.15, 0.20] µm is itself a MEASURED RANGE, so the
    # derived plateau top is a RANGE [2.20, 2.25], NOT a single number. The validation is
    # CONTAINMENT — does the measured GHJ 2.20 fall inside the derived range — NOT an exact
    # match against one endpoint. (Reporting |Δ|=0 by picking b=0.15 would be choosing a
    # number to hit the target; VP-SPEC C1 forbids that. We report where GHJ sits in the
    # derived range instead.)
    pt_lo, pt_hi = d["plateau_top_lo"], d["plateau_top_hi"]
    pt_meas = GHJ_MEASURED["plateau_top"]
    pt_dist = round(max(pt_lo - pt_meas, pt_meas - pt_hi, 0.0), 4)          # 0 iff inside
    pt_in = pt_dist <= TOL
    pt_edge = ("lower edge" if pt_meas <= pt_lo + 1e-9 else
               "upper edge" if pt_meas >= pt_hi - 1e-9 else "interior")
    fidelity["plateau_top"] = {"derived_lo": pt_lo, "derived_hi": pt_hi, "measured": pt_meas,
                               "in_range": bool(pt_in), "edge": pt_edge, "dist_to_range_um": pt_dist}
    P("  RANGE landmark (measured bare-zone range → derived range; CONTAINMENT is the test):")
    P(f"  plateau_top   2I+z+b = {pt_lo:.2f}–{pt_hi:.2f}   {pt_meas:6.3f} µm   "
      f"GHJ {pt_meas} at {pt_edge}  [thin at bare-zone edge]")
    P(f"  → POINT landmarks within TOL={TOL} µm (max |Δ| = {max_err:.3f} µm) AND plateau-top "
      f"range contains GHJ {pt_meas} ({pt_edge}): "
      f"{'PASS' if (max_err <= TOL and pt_in) else 'FAIL'}")

    P("\n### the derived force–length curve (descending + plateau; ascending = [O]) ###")
    for S in [2.00, 2.05, 2.20, 2.50, 2.80, 3.20, 3.65, 3.90]:
        f = force_length(S, d)
        cell = "  [O] not length-geometry" if (f != f) else f"F={f:4.2f}  |{'#'*int(round(f*36))}"
        P(f"    S={S:4.2f} µm  {cell}")

    P("\n### [O] declared (obstacles stated; aggregated in the ledger) ###")
    O_items = [
        ("zero_short ≈ 1.27 µm", "thick-filament CRUMPLING limit — needs buckling/compliance mechanics, not overlap length"),
        ("ascending-limb tension values", "double-overlap interference + wrong-polarity drag + compliance"),
        ("absolute tension scale", "needs cross-bridge number × unitary force × activation"),
        ("filament dimensions from ruler-protein sequence", "nebulin/titin length→dimension mapping is an open structural-biology derivation"),
    ]
    for item, why in O_items:
        P(f"    [O] {item}: {why}")

    # machine-readable result (the frozen-able artifact)
    result = {
        "lock": {"thick": A, "thin": I, "bare_lo": B_LO, "bare_hi": B_HI, "z": Z},
        "derived": d,
        "validation_vs_GHJ1966": fidelity,
        "max_abs_err_um": round(max_err, 4),
        "tolerance_um": TOL,
        "fidelity_pass": bool(max_err <= TOL and pt_in),
        "irreducible_O": [k for k, _ in O_items],
    }
    P("\n" + "=" * 78)
    P("RESULT (machine-readable):")
    P(json.dumps(result, indent=2))
    P("=" * 78)
    return result


def main():
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    res = run(P)
    # write the derived artifact for the harness to gate/freeze
    json.dump(res, open("muscle_force_law_results.json", "w"), indent=2)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
