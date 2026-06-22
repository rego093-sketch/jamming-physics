#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E1 :  the tip-link MET switch on the place map.

WHAT THIS BUILDS (START_HERE.md / BLUEPRINT.md E-plan).
  The hair-cell mechanotransduction (MET) lineage — the tip-link switch TMC1 / PCDH15 / CDH23
  (the three genes START_HERE names; TMIE, the 4th MET partner, is shown for the full complex) —
  EMERGED from the measured DNA reading and the R19 `Organ` primitive, sitting on the inherited
  √-law place map. Each gene is read as γ (LEVEL) **and** its A4 coordinate (SHAPE), not γ alone
  (DNA v1.13). The developmental order is argsort(spinodal(γ)); γ-ties are broken by the A4 SHAPE
  so genes of equal γ are NOT collapsed.

HOW IT RELATES TO THE FOUNDATION (no-regression).
  This module EXTENDS the inherited foundation by IMPORTING it — it does not edit a single inherited
  byte (the frozen hashes stay valid). It consumes `inherited/vp_dna_reading.py` (γ + A4),
  `inherited/vp_substrate.py` (the R19 Organ / spinodal / dwell), and `inherited/vp_sound_wave.py`
  (the Greenwood-form place map), and the measured atlas `inherited/organ_gamma.json`. The γ + A4 of
  every consumed gene is RECOMPUTED here from the frozen promoter cache and asserted bit-identical to
  the atlas, so E1's inputs reproduce offline with no network.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the reading γ(LEVEL)+A4(SHAPE) with A4 = signal−γ ; the emergence order argsort(spinodal(γ)) ;
            the A4 tie-break that refuses to collapse equal-γ genes ; the R19 DISCONTINUOUS presence
            threshold (all-or-none gating) ; the place map's exponential SHAPE ; the parameter-free
            traveling-wave PEAK PLACE = inverse-Greenwood.
  [L]      : every γ (NCBI-measured, cached) ; the Greenwood A/a/k calibration constants.
  [O]      : the absolute developmental time / organ size scale ; the full fluid-loaded dispersive
            traveling-wave ENVELOPE (width, phase, apical cutoff, active gain) ; the concordance of the
            emerged order with the measured hair-cell developmental sequence ; the felt percept (→ mind).
            Each names its obstacle below.

FIREWALL. γ reads promoter STRUCTURE only — never a channel voltage, transduction gain, dose, or
clinical effect. No disease claim here (E1 is pre-disease). The percept of hearing is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E1-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_dna_reading as DNA                              # γ (LEVEL) + A4 (SHAPE)
import vp_substrate   as SUB                              # R19 Organ / spinodal / barrier / dwell
import vp_sound_wave  as SND                              # √-law place map (Greenwood form)

CACHE = json.load(open(os.path.join(ROOT, "inherited/ear_promoters.cache.json"), encoding="utf-8"))["genes"]
ATLAS = json.load(open(os.path.join(ROOT, "inherited/organ_gamma.json"), encoding="utf-8"))["genes"]

# The MET tip-link switch. START_HERE names the trio; TMIE completes the MET complex (shown, flagged).
MET_TRIO = ["TMC1", "PCDH15", "CDH23"]                    # the explicit START_HERE deliverable
MET_FULL = MET_TRIO + ["TMIE"]                            # + 4th partner (full complex, for context)

# A4-SHAPE fields the reading exposes (orthogonal to γ; the texture γ-alone discards)
_SHAPE_FIELDS = ("shape_amplitude", "shape_range", "stiff_side_frac", "stiffest_offset_bp", "softest_offset_bp")


def read_measured(sym):
    """Recompute γ (LEVEL) + A4 (SHAPE) for a gene from the FROZEN cache, assert == atlas, return it."""
    rec  = CACHE[sym]
    assert hashlib.sha256(rec["seq"].encode()).hexdigest() == rec["seq_sha256"], f"{sym}: cache seq drift"
    r    = DNA.read_promoter(rec["seq"])                  # γ + A4, offline, deterministic
    a    = ATLAS[sym]
    for k in ("gamma",) + _SHAPE_FIELDS:                  # consumed inputs must match the atlas bit-for-bit
        assert r[k] == a[k], f"{sym}.{k}: recompute {r[k]} != atlas {a[k]}"
    assert r["shape_mean_abs"] < 1e-9, f"{sym}: A4 orthogonality mean(shape)!=0"   # A4 = signal − γ
    return dict(sym=sym, node=a["node"], gamma=r["gamma"], spinodal=r["spinodal"], barrier=r["barrier"],
                shape_amplitude=r["shape_amplitude"], shape_range=r["shape_range"],
                stiff_side_frac=r["stiff_side_frac"], stiffest_offset_bp=r["stiffest_offset_bp"],
                softest_offset_bp=r["softest_offset_bp"])


def order_key(rec):
    """Developmental-order key. PRIMARY: spinodal(γ) ascending — the lower the discontinuous threshold,
    the earlier the switch can flip (argsort(spinodal(γ)), DNA §5). TIE-BREAK (A4 SHAPE, measured): if
    two genes share γ (hence spinodal), order by A4 texture so they are NOT collapsed. The tie-break is a
    fixed, documented, measured ordering — it asserts no developmental MEANING for the A4 order (that is
    [O]); its sole job is to keep equal-γ genes distinct."""
    return (round(rec["spinodal"], 9),                   # [F] primary: discontinuous-threshold order
            round(rec["shape_amplitude"], 9),            # [L] A4 tie-break, fixed convention
            round(rec["shape_range"], 9),
            rec["stiffest_offset_bp"])


def inv_greenwood(f_hz):
    """Characteristic PLACE of a pure tone = inverse of the inherited Greenwood map f=A(10^(a x)−k),
    using the SAME measured A=165.4, a=2.1, k=0.88 the place map uses (no new constant). Parameter-free;
    x_frac in [0,1] from apex.  [F]/[V]."""
    return math.log10(f_hz / 165.4 + 0.88) / 2.1


# =====================================================================================================
def run(P):
    P("=" * 86)
    P("E1 — the tip-link MET switch (TMC1 / PCDH15 / CDH23) on the place map")
    P("     a wave property -> a spatial code (place) -> an R19 transduction switch")
    P("=" * 86)

    # -- PART 0 : the consumed reading reproduces offline from the frozen cache ------------------------
    P("\n[0] measured reading reproduces offline (γ LEVEL + A4 SHAPE, recomputed from frozen cache):")
    genes = {s: read_measured(s) for s in MET_FULL}
    for s in MET_FULL:
        g = genes[s]
        tag = "tip-link MET trio" if s in MET_TRIO else "4th MET partner (full complex)"
        P(f"    [PASS] {s:7s} γ(level)={g['gamma']:.4f}  A4 amp={g['shape_amplitude']:.5f} "
          f"range={g['shape_range']:.5f} stiff_side={g['stiff_side_frac']:.3f}  ({tag})")
    P("    -> every consumed γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9).  [V]")

    # -- PART A : EMERGE the lineage order = argsort(spinodal(γ)), A4 breaks γ-ties --------------------
    P("\n[A] EMERGE the MET lineage — order = argsort(spinodal(γ)),  spinodal = 2·(γ/3)^1.5:")
    ordered = sorted((genes[s] for s in MET_FULL), key=order_key)
    for i, g in enumerate(ordered, 1):
        core = "  <- START_HERE trio" if g["sym"] in MET_TRIO else ""
        P(f"    {i}. {g['sym']:7s} spinodal={g['spinodal']:.4f}  γ={g['gamma']:.4f}  "
          f"(flips {'first' if i==1 else 'later'}){core}")
    trio_order = [g["sym"] for g in ordered if g["sym"] in MET_TRIO]
    P(f"    -> tip-link trio emergence order (earliest-flipping first): {' < '.join(trio_order)}   [F]")
    P("       (lower spinodal = lower discontinuous threshold = earlier switch competence; γ measured.)")

    # -- relative size: DWELL ∝ γ^1.5 (order/direction forced; absolute scale [O]) --------------------
    P("\n    DWELL ∝ γ^1.5 (relative organ/lineage size; direction [F], absolute magnitude [O]):")
    dwell = {g["sym"]: SUB.dwell(g["gamma"], brake=0.5) for g in ordered}
    base  = min(dwell.values())
    for g in ordered:
        P(f"      {g['sym']:7s} dwell={dwell[g['sym']]:.4f}  relative={dwell[g['sym']]/base:.4f}")

    # -- PART B : the A4 tie-break does NOT collapse equal-γ genes ------------------------------------
    P("\n[B] A4 tie-break — equal-γ genes are NOT collapsed (the reason to read SHAPE, not γ alone):")
    # constructed unit test: a synthetic pair with IDENTICAL γ (=> identical spinodal, an exact tie on
    # the primary key) but DIFFERENT measured A4 shapes (drawn from two real genes). Proves no-collapse.
    gx, gy = genes["TMC1"], genes["CDH23"]
    twin_a = dict(sym="TWIN_A", gamma=gx["gamma"], spinodal=gx["spinodal"],
                  shape_amplitude=gx["shape_amplitude"], shape_range=gx["shape_range"],
                  stiff_side_frac=gx["stiff_side_frac"], stiffest_offset_bp=gx["stiffest_offset_bp"])
    twin_b = dict(sym="TWIN_B", gamma=gx["gamma"], spinodal=gx["spinodal"],              # SAME γ as A
                  shape_amplitude=gy["shape_amplitude"], shape_range=gy["shape_range"],   # DIFFERENT A4
                  stiff_side_frac=gy["stiff_side_frac"], stiffest_offset_bp=gy["stiffest_offset_bp"])
    tie_sorted = sorted([twin_a, twin_b], key=order_key)
    gamma_only_key          = lambda r: round(r["gamma"], 9)
    collapsed_if_gamma_only = (gamma_only_key(twin_a) == gamma_only_key(twin_b))   # True: γ-alone loses them
    distinct_with_A4        = (order_key(twin_a) != order_key(twin_b))             # True: A4 keeps them apart
    P(f"    [unit-test, constructed] two synthetic loci, SAME γ={twin_a['gamma']:.4f} "
      f"(=> SAME spinodal={twin_a['spinodal']:.4f}), DIFFERENT A4 shape:")
    P(f"       order by γ ALONE -> collapse (indistinguishable) = {collapsed_if_gamma_only}  "
      f"(True = the compressed view loses them)")
    P(f"       order by γ + A4  -> kept distinct = {distinct_with_A4}; "
      f"resolved {tie_sorted[0]['sym']} < {tie_sorted[1]['sym']}  "
      f"(A4 amp {tie_sorted[0]['shape_amplitude']:.5f} < {tie_sorted[1]['shape_amplitude']:.5f})")
    P(f"       output count preserved = {len(tie_sorted)} (NOT collapsed to 1).  [V]  (synthetic; "
      f"not a real locus — excluded from the lineage above)")
    # honest null result on the REAL data
    real_spins = [round(genes[s]["spinodal"], 9) for s in MET_FULL]
    n_real_ties = len(real_spins) - len(set(real_spins))
    P(f"    [HONEST NULL] in the REAL atlas all {len(MET_FULL)} MET γ are distinct "
      f"(spinodal ties = {n_real_ties}); the A4 tie-break is correct but does NOT fire here — its")
    P("                  necessity on this data is null. It is kept because equal-γ genes CAN occur; "
      "reading γ alone would be unsafe in general.")

    # -- PART C : the R19 switch is DISCONTINUOUS (all-or-none gating) --------------------------------
    P("\n[C] the MET switch is an R19 all-or-none flip (deflection drive vs the spinodal threshold):")
    org = SUB.Organ("hair_cell_MET", genes["TMC1"]["gamma"], master="TMC1", layer="mechanotransduction")
    sp  = org.functional_spinodal()
    probes = [("rest",          0.00),
              ("0.90·spinodal", 0.90 * sp),
              ("0.99·spinodal", 0.99 * sp),
              ("1.01·spinodal", 1.01 * sp),
              ("1.50·spinodal", 1.50 * sp)]
    P(f"    Organ(TMC1)  γ={org.g:.4f}  spinodal threshold = {sp:.4f}:")
    last = None
    for label, h in probes:
        s_end = SUB.settle(org.g, h)
        on    = SUB.is_on(org.g, h)
        flip  = "  <== DISCONTINUOUS flip" if (last is not None and on != last) else ""
        P(f"       drive {label:14s} (h={h:6.4f}) -> steady s={s_end:+.4f}  state={'ON' if on else 'OFF':3s}{flip}")
        last  = on
    P("    -> sub-threshold deflection => OFF (no graded leak across the barrier); past the spinodal the")
    P("       open state appears discontinuously. The tip-link gating spring reads PLACE deflection into")
    P("       an all-or-none transduction event.  [F] switch structure ; absolute SPL->Hz scale is [O].")

    # -- PART D : the place map (inherited foundation re-verified) ------------------------------------
    P("\n[D] the place map the switch sits on (√-law, Greenwood SHAPE — inherited, re-verified):")
    xs, fG, sqrtS, max_dev = SND.stiffness_graded_tonotopy()
    P(f"    ω=√(S/m) + log-graded stiffness => exponential place map; √S ∝ 10^(a·x) reproduces")
    P(f"    Greenwood's 10^(a·x) term: max|ratio−1| = {max_dev:.2e}  [F/V]   (apex {fG[0]:.0f} Hz "
      f"-> base {fG[-1]:.0f} Hz, A/a/k measured [L])")
    assert max_dev < 1e-9
    P("    -> the MET switch operates at EVERY place x; no per-gene tonotopic place is assigned "
      "(MET genes span the partition — assigning one would be invention).  [F] SHAPE.")

    # -- PART E : the traveling wave — parameter-free PEAK PLACE ; envelope is the named [O] -----------
    P("\n[E] the traveling wave: the PEAK PLACE is forced; the ENVELOPE is the named open target:")
    P("    characteristic place of a tone  x*(f) = inverse-Greenwood(f)  (parameter-free, no new constant):")
    for f in (250, 1000, 4000, 16000):
        x = inv_greenwood(f)
        P(f"       f={f:6d} Hz -> peak at x*={x:.4f}  (round-trip Greenwood f={SND.greenwood_f(x):.1f} Hz)")
    P("    -> the WHERE of the traveling-wave peak (von Bekesy) is FORCED by the √-law place map.  [F/V]")
    P("    [O] the full fluid-loaded, dispersive traveling-wave ENVELOPE (peak width, phase accumulation,")
    P("        apical cutoff slope, active gain) is NOT derived here. OBSTACLE: a passive envelope needs a")
    P("        damping/Q and the cochlear fluid mass-loading (Lighthill/Zweig hydrodynamics) plus the E3")
    P("        active amplifier; a closed envelope would require TUNING Q — forbidden by the no-tuning")
    P("        rule. So E1 forces the peak PLACE and leaves the envelope open, obstacle named (VP-SPEC C3).")

    # -- honest negatives preserved as the E1->E2 starting line ---------------------------------------
    P("\n[honest negatives — preserved as the starting line for E2, not hidden]")
    P("    N1  the A4 tie-break never fires on this atlas (all γ distinct) — necessity here is null.")
    P("    N2  argsort(spinodal(γ)) is a structural [F] order; its match to the MEASURED hair-cell")
    P("        developmental sequence is NOT asserted ([O] — needs cited timing data).")
    P("    N3  only the traveling-wave PEAK PLACE is forced; the ENVELOPE stays [O] (Q + fluid + active).")
    P("    N4  no per-gene tonotopic place is claimed (MET genes span the cochlea).")

    P("\nLEARNED (E1): the tip-link MET lineage emerges from measured γ via the R19 Organ — order by")
    P("  spinodal(γ), A4 ready to keep equal-γ genes distinct, the switch all-or-none, the place map the")
    P("  √-law SHAPE, the traveling-wave peak place parameter-free. Colour↔angle ∥ pitch↔place. The")
    P("  fluid-loaded wave ENVELOPE is the honest [O] this seed grows toward (E2 switch, E3 amplifier).")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
