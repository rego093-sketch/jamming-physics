#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E2-single-photon-switch/run.py — INCREMENT E2: the single-photon switch.

WHAT E2 DOES (BLUEPRINT.md E2; research/E2-single-photon-switch/START_HERE.md).
  Rod phototransduction (RHO · CNGA1 · CNGB1 · GNAT1, γ already MEASURED in the atlas) as a
  cooperative ALL-OR-NONE R19 flip — the inherited vp_substrate switch fired by one quantum of
  drive (one absorbed photon). Three things, built ONLY on the frozen inherited foundation:

    PART A — ALL-OR-NONE: THE FLIP IS DISCONTINUOUS PAST THE SPINODAL.
      For each of the four rod-phototransduction genes, using its MEASURED γ, the inherited R19
      field ds/dt = g·s − s³ + h (vp_substrate.sdot, FROZEN) is settled FROM THE REST BASIN
      (s0 = −√g) under a drive h that sweeps through the gene's spinodal h* = (2/3√3)·γ^1.5
      (vp_substrate.spinodal, FROZEN). Below h* the field stays in the rest basin (s<0: dark,
      no transduction); the instant the drive crosses h* the rest basin DISAPPEARS (saddle-node)
      and the field snaps to the on basin (s>0) — a finite, discontinuous jump. THAT is all-or-none:
      one quantum of drive across h* flips the whole switch; anything less does nothing. The
      photon→drive (and hence photon→Hz) ABSOLUTE scale is a named [O]; the discontinuity is [V].

    PART B — COOPERATIVITY IS THE CUBIC (n=3), AND IT IS NECESSARY.
      The all-or-none behaviour is not assumed — it is FORCED by the third-order restoring term
      −s³. The substrate's cooperativity ORDER is the order of that polynomial = 3 [F, inherited]:
      this is where "Hill ≈ 3" comes from — the cubic, not a fit. We demonstrate NECESSITY with a
      structural control: strike out the cubic (a first-order restoring field, NOT the substrate —
      it is the substrate with −s³ deleted) and the threshold, the basin, and the all-or-none jump
      all VANISH — the response becomes smooth and proportional (graded). The cubic switch's slope
      across the fold is ≥ an order of magnitude steeper than the graded control (formally → ∞ at
      the bifurcation). The literal physiological rod Hill coefficient is a calibration [O]; the
      polynomial order 3 and the necessity of the cubic are [F]/[V].

    PART C — THE ROD CASCADE = ORDERED SWITCHES; THE CNG α/β SUBUNITS NEED A4 (γ ALONE IS LOSSY).
      The four switches are ordered by spinodal(γ) — lowest threshold = most trigger-happy [F].
      The CNG channel is ONE channel built from TWO genes (CNGA1 = α, CNGB1 = β); their γ-LEVEL is
      degenerate (Δγ=0.0003 — the closest pair in the eye atlas; they COLLAPSE at 3-decimal γ) yet
      their A4 SHAPE differs 2.17× — so even the two halves of a single transduction switch are NOT
      interchangeable: the switch reads γ (LEVEL) AND A4 (SHAPE), never γ alone (DNA v1.13). Whether
      the substrate threshold-order matches the real biochemical cascade SEQUENCE (photon→RHO→GNAT1→
      …→CNG) is an open empirical question [O] — reported, never fitted, never assumed.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E2 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing.
    - the R19 switch math (sdot/spinodal/settle/is_on) ← inherited/vp_substrate.py (frozen, no-regression)
    - γ (LEVEL) + A4 (SHAPE) per rod gene               ← inherited/organ_gamma.json  (MEASURED [L]; the
                                                          verifier [3] re-proves it offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2). γ is promoter STRUCTURE only — never a channel voltage,
  a transduction gain, a current, a potency, a dose, or a clinical effect (FIREWALL #1); the switch
  order-parameter s is the abstract R19 field, NOT a photocurrent/voltage (no pA, no mV, no Hz here).
  The felt percept of sight belongs to the mind volume (FIREWALL #4); nothing here diagnoses, treats,
  or prescribes (FIREWALL #3). The _linear_control below is the substrate with its cubic STRUCK OUT —
  it exists only to prove the cubic is necessary; it does not fork or re-derive the substrate.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E2-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, barrier, settle, is_on   # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the rod single-photon phototransduction switch genes (by atlas node) — stated, not selected to a target.
ROD = ("RHO", "CNGA1", "CNGB1", "GNAT1")
ROD_ROLE = {"RHO": "rhodopsin (photopigment)", "CNGA1": "CNG channel α-subunit",
            "CNGB1": "CNG channel β-subunit", "GNAT1": "transducin α (Gt)"}

# the substrate's integration grid (the FROZEN settle() defaults) — fixed, not tuned.
N_STEPS, DT = 1500, 0.02


def rest_basin(g):
    """The dark resting state of the R19 field: the lower well s = −√g (vp_substrate.settle's s0)."""
    return -math.sqrt(g)


def _linear_control(g, h, s0=0.0, n=4000, dt=DT):
    """STRUCTURAL CONTROL — NOT the substrate. The substrate field with its cubic −s³ STRUCK OUT,
    leaving a stable first-order restoring field ds/dt = −g·s + h (steady state s* = h/g). It has
    NO double well, NO spinodal, NO discontinuity: a graded, proportional response. It exists ONLY
    to prove the cubic is what makes the real switch all-or-none. It is never used as biology."""
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)            # cubic deleted → smooth proportional relaxation
    return s


def run(P):
    P("=" * 80)
    P("E2 — THE SINGLE-PHOTON SWITCH   (cooperative all-or-none R19 flip; frozen substrate)")
    P("=" * 80)
    P("consumes (frozen): vp_substrate.sdot/spinodal/settle/is_on · organ_gamma.json γ+A4")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")
    P("the switch order-parameter s is the abstract R19 field — NOT a photocurrent/voltage/Hz.")

    # ----------------------------------------------------------------------------------------
    # PART A — all-or-none: the flip is discontinuous past the spinodal
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — all-or-none: the R19 flip is DISCONTINUOUS past the spinodal h* (one photon flips it)")
    P("-" * 80)
    P("for each rod gene: settle the field FROM REST (s0=−√γ) under a drive h sweeping through h*.")
    P("below h* → stays dark (s<0); across h* the rest basin disappears → snaps on (s>0).  [V]")
    P(f"  {'gene':6s} {'role':26s} {'γ':>7s} {'h*=spinodal':>11s} {'rest(−√γ)':>9s} "
      f"{'s@0.90h*':>9s} {'s@1.10h*':>9s} {'jump':>7s}")
    jumps = {}
    for sym in ROD:
        g = ATLAS[sym]["gamma"]
        hstar = spinodal(g)
        # the substrate recomputes spinodal from γ via the FROZEN formula; the atlas lists the same
        # quantity from full-precision γ then rounded — agree within one γ-rounding unit.
        assert abs(hstar - ATLAS[sym]["spinodal"]) < 2e-4, f"{sym}: spinodal must match atlas (γ-rounding)"
        s0 = rest_basin(g)
        s_below = settle(g, 0.90 * hstar, s0=s0, n=N_STEPS, dt=DT)     # clearly below threshold
        s_above = settle(g, 1.10 * hstar, s0=s0, n=N_STEPS, dt=DT)     # clearly above threshold
        jump = s_above - s_below
        jumps[sym] = jump
        P(f"  {sym:6s} {ROD_ROLE[sym]:26s} {g:7.4f} {hstar:11.5f} {s0:9.4f} "
          f"{s_below:+9.4f} {s_above:+9.4f} {jump:+7.4f}")
        # all-or-none: dark below, on above, with a large finite jump (a saddle-node, not a smooth ramp)
        assert s_below < 0.0,  f"{sym}: below h* the switch must stay in the dark/rest basin (s<0)"
        assert s_above > 0.0,  f"{sym}: above h* the switch must flip on (s>0)"
        assert jump > 1.5,     f"{sym}: the all-or-none jump must be large & finite (saddle-node)"

    # locate the discontinuity on RHO — the response is FLAT then JUMPS (no graded middle)
    P("\n[discontinuity] RHO, fine drive sweep — the switch is FLAT below h* then JUMPS (all-or-none):")
    g = ATLAS["RHO"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    prev_on = None; crossed = False
    for frac in (0.90, 0.95, 0.99, 1.00, 1.01, 1.05, 1.10):
        fs = settle(g, frac * hstar, s0=s0, n=N_STEPS, dt=DT)
        on = fs > 0.0
        flip = ""
        if prev_on is not None and on != prev_on:
            flip = "   <<< FLIP (discontinuous)"; crossed = True
        P(f"    h = {frac:.2f}·h* = {frac*hstar:.5f}   final_s = {fs:+.4f}   on={on}{flip}")
        prev_on = on
    assert crossed, "RHO must show a discontinuous off→on flip as the drive crosses the spinodal"
    P("    → one quantum of drive across h* flips the entire switch; anything less does nothing.")
    P("      [V] the discontinuity (structure).  [O] the absolute photon→drive→Hz scale (calibration).")

    # ----------------------------------------------------------------------------------------
    # PART B — cooperativity is the cubic (n=3), and it is necessary
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — the cooperativity is the CUBIC −s³ (order n=3), and it is NECESSARY for all-or-none")
    P("-" * 80)
    P("the substrate field ds/dt = γ·s − s³ + h. the restoring term is THIRD-order ⇒ cooperativity")
    P("order n = 3  [F, inherited] — this is where 'Hill≈3' comes from: the cubic, NOT a fit.")
    P("necessity test — delete the cubic (a first-order control field −γ·s + h, NOT the substrate):")

    g = ATLAS["RHO"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    # the real (cubic) switch: a step across the fold
    s_lo, s_hi = settle(g, 0.99 * hstar, s0=s0, n=N_STEPS, dt=DT), settle(g, 1.01 * hstar, s0=s0, n=N_STEPS, dt=DT)
    cubic_slope = abs(s_hi - s_lo) / (0.02 * hstar)                 # slope across a tight straddle of h*
    # the graded control (cubic struck out): smooth, proportional, no threshold
    P("\n  drive h        cubic switch (real)       linear control (cubic deleted)")
    for frac in (0.50, 0.90, 1.00, 1.10, 1.50):
        h = frac * hstar
        cs = settle(g, h, s0=s0, n=N_STEPS, dt=DT)
        ls = _linear_control(g, h)
        P(f"    {frac:.2f}·h*      final_s = {cs:+.4f}            final_s = {ls:+.4f}")
    g_lo, g_hi = _linear_control(g, 0.90 * hstar), _linear_control(g, 1.10 * hstar)
    graded_slope = abs(g_hi - g_lo) / (0.20 * hstar)               # gentle, finite slope
    ratio = cubic_slope / graded_slope
    P(f"\n  [steepness] cubic switch slope across h* ≈ {cubic_slope:.1f}  (formally → ∞ at the fold)")
    P(f"              linear control slope          ≈ {graded_slope:.3f}  (smooth, proportional)")
    P(f"              ratio ≈ {ratio:.0f}×  → the cubic makes the response a STEP; the control is graded.")
    # the cubic switch is all-or-none (huge jump); the control never crosses zero from below → no switch
    assert (s_hi > 0.0) and (s_lo < 0.0), "the cubic switch must straddle off/on across h*"
    assert ratio > 20.0, "the cubic switch must be ≥ an order of magnitude steeper than the linear control"
    assert _linear_control(g, 0.50 * hstar) > 0.0, "the linear control has no threshold (proportional, always graded)"
    P("  → removing the cubic removes the threshold, the basin, and the all-or-none jump. The")
    P("    cooperativity (the −s³) is NECESSARY.  [F] order n=3 · [V] necessity · [O] in-vivo Hill value.")

    # ----------------------------------------------------------------------------------------
    # PART C — the rod cascade = ordered switches; the CNG α/β subunits need A4
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the rod cascade = four ordered R19 switches; the CNG α/β subunits need A4, not γ alone")
    P("-" * 80)
    # order the four rod switches by spinodal(γ): lowest threshold = most trigger-happy [F]
    order = sorted(ROD, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    P("the four switches ordered by spinodal(γ) — lowest threshold flips first  [F]:")
    P(f"  {'rank':>4} {'gene':6s} {'role':26s} {'γ':>7s} {'h*=spinodal':>11s} {'barrier':>8s}")
    for k, sym in enumerate(order, 1):
        g = ATLAS[sym]["gamma"]
        P(f"  {k:4d} {sym:6s} {ROD_ROLE[sym]:26s} {g:7.4f} {spinodal(g):11.5f} {barrier(g):8.4f}")
    P("  [O] whether this threshold-order matches the real biochemical cascade SEQUENCE")
    P("      (photon → RHO → GNAT1 → … → CNG) is an open empirical question — obstacle: needs the")
    P("      measured cascade kinetics; NOT fitted, NOT assumed (note: it is ~reverse of signalling).")

    # the CNG channel = one channel, two genes, degenerate γ → A4 SHAPE distinguishes them
    a, b = dict(ATLAS["CNGA1"], _sym="CNGA1"), dict(ATLAS["CNGB1"], _sym="CNGB1")
    dg = abs(a["gamma"] - b["gamma"])
    ga3, gb3 = round(a["gamma"], 3), round(b["gamma"], 3)
    sa3, sb3 = round(a["spinodal"], 3), round(b["spinodal"], 3)
    collapse = (ga3 == gb3) and (sa3 == sb3)
    P("\n[one channel, two genes] CNGA1 (α) + CNGB1 (β) form the SINGLE rod CNG channel — closest γ pair:")
    P(f"    CNGA1: γ={a['gamma']:.4f} spinodal={a['spinodal']:.4f} shape_amp={a['shape_amplitude']:.5f}")
    P(f"    CNGB1: γ={b['gamma']:.4f} spinodal={b['spinodal']:.4f} shape_amp={b['shape_amplitude']:.5f}")
    P(f"    Δγ = {dg:.4f}   →  at 3-decimal γ they COLLAPSE (CNGA1 γ→{ga3:.3f}, CNGB1 γ→{gb3:.3f}): "
      f"γ-alone reads them as identical? {collapse}")
    assert collapse, "CNGA1/CNGB1 must collapse at γ-only 3-decimal resolution (the degeneracy to break)"
    ratio_amp = max(a["shape_amplitude"], b["shape_amplitude"]) / min(a["shape_amplitude"], b["shape_amplitude"])
    broken = sorted(("CNGA1", "CNGB1"), key=lambda s: ATLAS[s]["shape_amplitude"])
    P(f"    A4 shape_amplitude differs {ratio_amp:.2f}× → the SHAPE separates them: {broken[0]} ≠ {broken[1]}  [V]")
    P("    → even the two halves of ONE transduction switch are not interchangeable: read γ AND A4.")
    assert ratio_amp > 1.5, "the CNG α/β A4 shapes must be clearly distinct (γ-degeneracy broken by shape)"

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E2 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the all-or-none flip is a saddle-node past h*=spinodal(γ); cooperativity")
    P("                 order n=3 = the cubic −s³; the four switches' order = argsort(spinodal(γ)).")
    P("  [V] verified : every rod gene stays dark below h* and snaps on above it (finite jump);")
    P("                 the discontinuous off→on flip; deleting the cubic removes the switch")
    P("                 (≥20× steeper than the graded control); CNGA1/CNGB1 collapse under γ-alone")
    P("                 and are separated by A4 shape. (γ+A4 re-proved offline by verify_seed [3].)")
    P("  [L] measured : every rod-gene γ (+A4) from NCBI promoters, cached, byte-identical to atlas.")
    P("  [O] open     : the absolute photon→drive→firing (Hz) scale (calibration); the literal")
    P("                 physiological rod Hill value; whether the substrate threshold-order matches")
    P("                 the real biochemical cascade sequence (needs kinetics); the FELT percept of")
    P("                 light (→ mind volume). Each obstacle named, never invented.")
    P("\nLEARNED: rod phototransduction is the inherited R19 switch made ALL-OR-NONE by its cubic −s³:")
    P("         below the spinodal the field is dark; one quantum of drive across it flips the whole")
    P("         switch discontinuously (single-photon sensitivity, structure-only). The cooperativity")
    P("         IS the cubic (n=3) and is necessary — delete it and the switch becomes graded. The CNG")
    P("         channel's α/β subunits share γ but differ in A4 shape, so the switch reads LEVEL AND")
    P("         SHAPE. Foundation untouched; nothing fitted; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
