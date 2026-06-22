#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E2-transduction-switch/run.py — INCREMENT E2: the olfactory transduction switch.

WHAT E2 DOES (BLUEPRINT.md E2; research/E2-transduction-switch/START_HERE.md).
  This is where the sibling senses' skeleton SURVIVES. Smell has no wave (E1), but its back end is
  the SAME all-or-none R19 transduction switch as vision. The olfactory cascade is
      odorant → OR → GNAL (Golf) → ADCY3 (cAMP) → CNG channel (CNGA2·CNGA4·CNGB1) → ANO2 (amplifier),
  and the CNG channel is the inherited R19 bistable switch — the SAME gene family as rod vision's CNG.
  Built ONLY on the frozen inherited substrate + the measured atlas, three things:

    PART A — ALL-OR-NONE: THE TRANSDUCTION FLIP IS DISCONTINUOUS PAST THE SPINODAL.
      For each transduction gene (GNAL, ADCY3, CNGA2, CNGA4, CNGB1, ANO2 — γ MEASURED), the inherited
      R19 field ds/dt = γ·s − s³ + h (vp_substrate.sdot, FROZEN) settled FROM REST (s0=−√γ) under a
      drive sweeping through the gene's spinodal h*=(2/3√3)γ^1.5 stays in the rest basin below h*
      (s<0: no transduction) and snaps to the on basin above it (s>0) — a finite, discontinuous jump.
      One quantum of drive across h* flips the switch; less does nothing. [V] structure; the absolute
      odorant→drive→firing (Hz) scale is a named [O] (same calibration gap as vision's photon→Hz).

    PART B — COOPERATIVITY IS THE CUBIC (n=3), AND IT IS NECESSARY.
      The all-or-none behaviour is FORCED by the third-order restoring term −s³ [F, inherited]: this is
      where olfactory "Hill ≈ 2–3" comes from — the cubic, not a fit. We demonstrate NECESSITY with a
      structural control: strike out the cubic (a first-order restoring field −γ·s + h, NOT the
      substrate) and the threshold, the basin, and the all-or-none jump all VANISH — the response
      becomes graded. The cubic switch is ≥ an order of magnitude steeper across the fold. The literal
      in-vivo olfactory Hill value is a calibration [O]; the polynomial order 3 and the cubic's
      necessity are [F]/[V].

    PART C — CROSS-SENSE: THE TRANSDUCTION SWITCH IS GENUINELY SHARED (CNGB1), AND ITS SUBUNITS READ.
      CNGB1 — the CNG channel β subunit — is the SAME gene in rod vision and in olfaction. Its
      promoter γ measured HERE (olfactory seed) is byte-identical to the value measured INDEPENDENTLY
      for rod vision in the sibling eye seed: the R19 transduction switch is not an analogy, it is the
      SAME substrate primitive reused across senses [V]. The olfactory CNG channel's three subunits
      (CNGA2 principal · CNGA4 · CNGB1 modulatory) are separated by their measured (γ, A4) readings —
      here γ is already well-separated (unlike rod vision's degenerate CNGA1/CNGB1, which needed the
      A4 SHAPE to break a γ-tie); the A4 is carried regardless. Whether the substrate threshold-order
      matches the real biochemical cascade SEQUENCE (Golf→ADCY3→CNG→ANO2) is an open empirical
      question [O] — reported, never fitted.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E2 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing, fits nothing.
    - the R19 switch math (sdot/spinodal/settle/is_on) ← inherited/vp_substrate.py (frozen, no-regression)
    - γ (LEVEL) + A4 (SHAPE) per gene                  ← inherited/organ_gamma.json (MEASURED [L]; the
                                                         verifier [3] re-proves it offline bit-for-bit)
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never a channel voltage, a
  transduction gain, a current, or a percept (FIREWALL #1); the order-parameter s is the abstract R19
  field, NOT a receptor current/voltage/Hz. The felt experience of smelling belongs to the mind volume
  (FIREWALL #4); nothing here diagnoses or treats (FIREWALL #3). The _linear_control is the substrate
  with its cubic STRUCK OUT — it proves the cubic is necessary; it does not fork the substrate.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, barrier, settle, is_on   # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the olfactory transduction cascade genes (by atlas node) — stated, not selected to a target.
TRANSD = tuple(s for s in ("GNAL", "ADCY3", "CNGA2", "CNGA4", "CNGB1", "ANO2")
               if ATLAS.get(s, {}).get("node") == "olfactory_transduction")
ROLE = {s: ATLAS[s].get("role", "") for s in TRANSD}

# CITED cross-sense reference: CNGB1 γ as independently measured for ROD VISION (sibling eye seed).
ROD_VISION_CNGB1_GAMMA = 1.4357      # vp_eye_emergence_seed atlas (same gene, same promoter window)

N_STEPS, DT = 1500, 0.02             # the FROZEN settle() defaults — fixed, not tuned


def rest_basin(g):
    return -math.sqrt(g)


def _linear_control(g, h, s0=0.0, n=4000, dt=DT):
    """STRUCTURAL CONTROL — NOT the substrate. The substrate field with its cubic −s³ STRUCK OUT,
    leaving a stable first-order field ds/dt = −g·s + h (steady state s* = h/g): no double well, no
    spinodal, no discontinuity — a graded response. It exists ONLY to prove the cubic is necessary."""
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)
    return s


def run(P):
    P("=" * 80)
    P("E2 — THE OLFACTORY TRANSDUCTION SWITCH   (the R19 all-or-none flip survives; shared with vision)")
    P("=" * 80)
    P("consumes (frozen): vp_substrate.sdot/spinodal/settle/is_on · organ_gamma.json γ+A4 (MEASURED)")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")
    P("the order-parameter s is the abstract R19 field — NOT a receptor current/voltage/Hz.")
    P(f"the measured transduction cascade: {' → '.join(TRANSD)}")

    # ------------------------------------------------------------------------------------------
    # PART A — all-or-none: the flip is discontinuous past the spinodal
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — all-or-none: the R19 transduction flip is DISCONTINUOUS past the spinodal h*  [V]")
    P("-" * 80)
    P("for each gene: settle the FROZEN field FROM REST (s0=−√γ) under a drive h sweeping through h*.")
    P(f"  {'gene':6s} {'role':38s} {'γ':>7s} {'h*':>9s} {'s@0.90h*':>9s} {'s@1.10h*':>9s} {'jump':>7s}")
    for sym in TRANSD:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
        assert abs(hstar - ATLAS[sym]["spinodal"]) < 2e-4, f"{sym}: spinodal must match atlas (γ-rounding)"
        s_below = settle(g, 0.90 * hstar, s0=s0, n=N_STEPS, dt=DT)
        s_above = settle(g, 1.10 * hstar, s0=s0, n=N_STEPS, dt=DT)
        jump = s_above - s_below
        P(f"  {sym:6s} {ROLE[sym]:38s} {g:7.4f} {hstar:9.5f} {s_below:+9.4f} {s_above:+9.4f} {jump:+7.4f}")
        assert s_below < 0.0,  f"{sym}: below h* the switch must stay dark/rest (s<0)"
        assert s_above > 0.0,  f"{sym}: above h* the switch must flip on (s>0)"
        assert jump > 1.5,     f"{sym}: the all-or-none jump must be large & finite (saddle-node)"

    # locate the discontinuity on the principal CNG subunit (CNGA2) — flat then jump
    P("\n[discontinuity] CNGA2 (principal CNG subunit), fine sweep — FLAT below h* then JUMPS (all-or-none):")
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    prev_on = None; crossed = False
    for frac in (0.90, 0.95, 0.99, 1.00, 1.01, 1.05, 1.10):
        fs = settle(g, frac * hstar, s0=s0, n=N_STEPS, dt=DT); on = fs > 0.0
        flip = ""
        if prev_on is not None and on != prev_on:
            flip = "   <<< FLIP (discontinuous)"; crossed = True
        P(f"    h = {frac:.2f}·h* = {frac*hstar:.5f}   final_s = {fs:+.4f}   on={on}{flip}")
        prev_on = on
    assert crossed, "CNGA2 must show a discontinuous off→on flip as the drive crosses the spinodal"
    P("    → one quantum of drive across h* flips the whole transduction switch; less does nothing.")
    P("      [V] the discontinuity (structure).  [O] the absolute odorant→drive→Hz scale (calibration).")

    # ------------------------------------------------------------------------------------------
    # PART B — cooperativity is the cubic (n=3), and it is necessary
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — the cooperativity is the CUBIC −s³ (order n=3), and it is NECESSARY for all-or-none")
    P("-" * 80)
    P("the substrate field ds/dt = γ·s − s³ + h. the restoring term is THIRD-order ⇒ cooperativity")
    P("order n = 3  [F, inherited] — this is where olfactory 'Hill≈2–3' comes from: the cubic, NOT a fit.")
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    s_lo, s_hi = settle(g, 0.99 * hstar, s0=s0, n=N_STEPS, dt=DT), settle(g, 1.01 * hstar, s0=s0, n=N_STEPS, dt=DT)
    cubic_slope = abs(s_hi - s_lo) / (0.02 * hstar)
    P("\n  drive h        cubic switch (real)       linear control (cubic deleted)")
    for frac in (0.50, 0.90, 1.00, 1.10, 1.50):
        h = frac * hstar
        P(f"    {frac:.2f}·h*      final_s = {settle(g, h, s0=s0, n=N_STEPS, dt=DT):+.4f}            "
          f"final_s = {_linear_control(g, h):+.4f}")
    g_lo, g_hi = _linear_control(g, 0.90 * hstar), _linear_control(g, 1.10 * hstar)
    graded_slope = abs(g_hi - g_lo) / (0.20 * hstar)
    ratio = cubic_slope / graded_slope
    P(f"\n  [steepness] cubic switch slope across h* ≈ {cubic_slope:.1f}  (formally → ∞ at the fold)")
    P(f"              linear control slope          ≈ {graded_slope:.3f}  (smooth, proportional)")
    P(f"              ratio ≈ {ratio:.0f}×  → the cubic makes the response a STEP; the control is graded.")
    assert (s_hi > 0.0) and (s_lo < 0.0), "the cubic switch must straddle off/on across h*"
    assert ratio > 20.0, "the cubic switch must be ≥ an order of magnitude steeper than the linear control"
    assert _linear_control(g, 0.50 * hstar) > 0.0, "the linear control has no threshold (always graded)"
    P("  → removing the cubic removes the threshold, the basin, and the all-or-none jump. The")
    P("    cooperativity (the −s³) is NECESSARY.  [F] order n=3 · [V] necessity · [O] in-vivo Hill value.")

    # ------------------------------------------------------------------------------------------
    # PART C — cross-sense: the transduction switch is shared (CNGB1); the CNG subunits read
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the transduction switch is GENUINELY SHARED across senses (CNGB1), and its subunits read")
    P("-" * 80)
    cngb1 = ATLAS["CNGB1"]["gamma"]
    P(f"CNGB1 (CNG channel β) is the SAME gene in rod vision and olfaction:")
    P(f"    olfactory seed (here): γ = {cngb1:.4f}")
    P(f"    rod-vision seed (cited eye sibling): γ = {ROD_VISION_CNGB1_GAMMA:.4f}")
    P(f"    byte-identical? {cngb1 == ROD_VISION_CNGB1_GAMMA}  → the R19 transduction switch is the SAME")
    P(f"    substrate primitive reused across senses (independently fetched, same promoter).  [V]")
    assert cngb1 == ROD_VISION_CNGB1_GAMMA, "CNGB1 γ must match the rod-vision sibling (same gene)"

    # the olfactory CNG channel's three subunits, separated by (γ, A4)
    P("\n[the olfactory CNG channel — three subunits, separated by their measured (γ, A4) readings]:")
    P(f"  {'subunit':8s} {'role':38s} {'γ':>7s} {'h*=spinodal':>11s} {'shape_amp(A4)':>13s}")
    cng = ("CNGA2", "CNGA4", "CNGB1")
    for sym in cng:
        a = ATLAS[sym]
        P(f"  {sym:8s} {a.get('role',''):38s} {a['gamma']:7.4f} {a['spinodal']:11.5f} {a['shape_amplitude']:13.5f}")
    gammas3 = [round(ATLAS[s]["gamma"], 3) for s in cng]
    well_separated = len(set(gammas3)) == len(gammas3)
    P(f"  γ already separates all three at 3-decimals? {well_separated}  → unlike rod vision's degenerate")
    P(f"    CNGA1/CNGB1 (which needed the A4 SHAPE to break a γ-tie), here γ alone distinguishes them;")
    P(f"    the A4 SHAPE is carried regardless (verify_seed [3] re-proves it offline).  [V]/[L]")
    assert well_separated, "the olfactory CNG subunits should be γ-separable (no degeneracy to break here)"

    # cascade ordering by spinodal(γ) vs the biochemical sequence — the [O]
    order = sorted(TRANSD, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    P("\n[cascade order] the six switches ordered by spinodal(γ) — lowest threshold first  [F]:")
    P(f"    {' → '.join(order)}")
    P("  [O] whether this threshold-order matches the real biochemical cascade SEQUENCE")
    P("      (Golf → ADCY3 → cAMP → CNG → ANO2) is an open empirical question — obstacle: needs the")
    P("      measured cascade kinetics; NOT fitted, NOT assumed.")

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E2 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the all-or-none flip is a saddle-node past h*=spinodal(γ); cooperativity")
    P("                 order n=3 = the cubic −s³; the cascade order = argsort(spinodal(γ)).")
    P("  [V] verified : every transduction gene stays dark below h* and snaps on above it (finite")
    P("                 jump); the discontinuous off→on flip on CNGA2; deleting the cubic removes the")
    P("                 switch (≥20× steeper than the graded control); CNGB1 γ byte-identical to the")
    P("                 rod-vision sibling (the shared transduction switch); the CNG subunits read")
    P("                 distinctly. (γ+A4 re-proved offline by verify_seed [3].)")
    P("  [L] measured : every transduction-gene γ (+A4) from NCBI promoters, cached, byte-identical")
    P("                 to atlas; the cited rod-vision CNGB1 γ (sibling eye seed).")
    P("  [O] open     : the absolute odorant→drive→firing (Hz) scale (calibration); the literal in-vivo")
    P("                 olfactory Hill value; whether the substrate threshold-order matches the real")
    P("                 biochemical cascade sequence (needs kinetics); the FELT percept (→ mind volume).")
    P("\nLEARNED: smell's back end is the SAME inherited R19 switch as vision, made ALL-OR-NONE by its")
    P("         cubic −s³ — below the spinodal no transduction, one quantum of drive across it flips the")
    P("         whole switch discontinuously. The cubic (n=3) is necessary. CNGB1 is literally the same")
    P("         gene as rod vision's CNG β (byte-identical γ), so the transduction switch is shared, not")
    P("         analogous. What differs from vision is only the FRONT END (E1: combinatorial, ligand-")
    P("         limited [O]); the transduction switch is genuinely substrate-derived. Foundation")
    P("         untouched; nothing fitted; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
