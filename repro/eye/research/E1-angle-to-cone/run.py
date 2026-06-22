#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E1-angle-to-cone/run.py — INCREMENT E1: angle → cone (the first emergence).

WHAT E1 DOES (BLUEPRINT.md E1; research/E1-angle-to-cone/START_HERE.md).
  Three things, built ONLY on the frozen inherited foundation — nothing re-derived here:

    PART A — TRICHROMACY AS THREE ANGLE-BANDS.
      The inherited angle law sinχ = λ/(mD), m=⌈λ/D⌉, D = 2λ_C,e invariant
      (vp_color_by_angle.chi_deg / D, FROZEN) maps each wavelength to a propagation
      angle χ. The three cone opsins OPN1LW / OPN1MW / OPN1SW are placed on that map
      by their MEASURED peak wavelength λmax (vision-science literature, [L] cited —
      NOT derived from γ, NOT fitted). They land at three DISTINCT angle-bands ⇒ the
      eye samples colour as three angles ⇒ trichromacy. The falsifier is the committed
      633/532 anchor (red 89.9378° ≠ green 89.8248°, sep 0.1130°) — asserted, no fitting.

    PART B — EMERGE THE CONE/ROD LINEAGE VIA THE R19 Organ.
      Each gene is built as the inherited Organ(name, γ) primitive (vp_substrate, FROZEN).
      Emergence order = argsort(spinodal(γ)) — the lowest-threshold switch flips first
      (the substrate's FORCED ordering key [F]). Relative size = dwell ∝ γ^1.5 [F]
      (absolute magnitude [O]). The three cones' rank positions and relative dwell are
      reported. Whether this substrate order coincides with real retinal developmental
      TIME is an open empirical question [O] — this seed does NOT fit the order to known
      biology; it reports the substrate order and flags the correspondence, never invents it.

    PART C — THE A4 TIE-BREAK (do not collapse equal-γ genes).
      The order key is a TOTAL ORDER: primary = spinodal(γ); tie-break = the A4 SHAPE
      (shape_amplitude, then stiffest_offset_bp, then symbol — a stated derived convention,
      not a fit). Real demonstration on CNGA1 vs CNGB1 — the rod CNG channel α/β subunits,
      the CLOSEST γ pair in the whole eye atlas (Δγ=0.0003). At 3-decimal γ resolution they
      COLLAPSE to an identical value (γ→1.436, spinodal→0.662): reading γ ALONE makes them
      interchangeable — exactly the failure mode START_HERE warns about. Their A4 shapes
      differ 2.17× in amplitude, so the shape tie-break orders them deterministically. The
      full key gives every gene a unique rank (no collapse) — asserted.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E1 CONSUMES the frozen foundation and the MEASURED atlas; it re-derives nothing.
    - the angle law + D            ← inherited/vp_color_by_angle.py   (frozen, no-regression)
    - the R19 switch math (Organ)  ← inherited/vp_substrate.py        (frozen, no-regression)
    - γ (LEVEL) + A4 (SHAPE)        ← inherited/organ_gamma.json       (MEASURED [L]; the
                                      verifier [3] re-proves it offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2). γ is promoter STRUCTURE only — never a channel
  voltage, transduction gain, potency, dose, or clinical effect (FIREWALL #1). The optical
  layer (λmax → angle) and the DNA-structural layer (γ/A4 → emergence) are kept SEPARATE:
  E1 does NOT claim γ predicts λmax. The felt colour percept belongs to the mind volume
  (FIREWALL #4); nothing here diagnoses, treats, or prescribes (FIREWALL #3).

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib + numpy (only via the frozen substrate's scalar helpers — pure math, no RNG).
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E1-angle-to-cone → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_color_by_angle import chi_deg, D                  # FROZEN: the angle law + invariant size D
from vp_substrate import Organ, spinodal, dwell           # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the three cone opsins' MEASURED peak wavelength λmax (nm) — [L], cited, NOT from γ, NOT fitted.
#   S 420 / M 530 / L 560 nm: human cone spectral peaks (Stockman & Sharpe 2000;
#   Bowmaker & Dartnall 1980). Each is the central peak; the real sensitivity is a broad band.
OPSIN_LMAX_NM = {"OPN1SW": 420.0, "OPN1MW": 530.0, "OPN1LW": 560.0}
OPSIN_TAG     = {"OPN1SW": "S/blue", "OPN1MW": "M/green", "OPN1LW": "L/red"}

# the cone/rod photoreceptor lineage (by atlas node) — stated, not selected to a target:
LINEAGE_NODES = ("cone_color_angle", "rod", "rod_phototransduction", "photoreceptor")


def shape_key(rec):
    """A4 SHAPE tie-break key (a stated derived convention, not a fit): amplitude of the
    shape coordinate first (the size of the A4 vector), then its stiffest-window position,
    then the symbol — a deterministic TOTAL order used ONLY to break γ-ties."""
    return (rec["shape_amplitude"], rec["stiffest_offset_bp"], rec["_sym"])


def run(P):
    P("=" * 80)
    P("E1 — ANGLE → CONE   (the first emergence; built on the frozen inherited foundation)")
    P("=" * 80)
    P(f"inherited invariant quantum size D = {D*1e12:.6f} pm  (χ depends on λ alone)")
    P("consumes (frozen): vp_color_by_angle.chi_deg/D · vp_substrate.Organ · organ_gamma.json γ+A4")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")

    # ----------------------------------------------------------------------------------------
    # PART A — trichromacy as three angle-bands
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — three cone opsins on the angle map → trichromacy as three angle-bands")
    P("-" * 80)

    # the committed anchor = the falsifier (must hold, no fitting) -- [F], inherited B1 anchor
    xr, xg = chi_deg(632.99e-9), chi_deg(532.0e-9)
    sep = abs(xr - xg)
    P(f"[falsifier] committed anchor: red 633nm → χ={xr:.4f}°, green 532nm → χ={xg:.4f}°, "
      f"sep={sep:.4f}°   [F]")
    assert sep > 0.05, "committed 633/532 angle separation must hold (inherited B1 anchor)"

    # place the three cones by MEASURED λmax → three angles -- [L] inputs, [F] mapping
    P("\n[place] each cone opsin at its MEASURED λmax (literature [L]), mapped by the inherited law:")
    ang = {}
    for sym in ("OPN1SW", "OPN1MW", "OPN1LW"):
        lam = OPSIN_LMAX_NM[sym]
        a = chi_deg(lam * 1e-9)
        ang[sym] = a
        g = ATLAS[sym]["gamma"]
        P(f"    {sym} ({OPSIN_TAG[sym]:7s}) λmax={lam:5.0f}nm → χ={a:.4f}°    "
          f"(γ={g:.4f} read separately; NOT used to place the angle — firewall)")

    # the three bands are distinct and (here) monotone S<M<L -- the trichromacy structure [F]
    P("\n[bands] pairwise angle separations (each colour is a BAND, not a sharp line):")
    order_ang = sorted(ang, key=lambda s: ang[s])
    for i in range(len(order_ang)):
        for j in range(i + 1, len(order_ang)):
            si, sj = order_ang[i], order_ang[j]
            P(f"    {si} vs {sj}: Δχ={abs(ang[si]-ang[sj]):.4f}°")
    distinct = len({round(v, 4) for v in ang.values()}) == 3
    monotone = ang["OPN1SW"] < ang["OPN1MW"] < ang["OPN1LW"]
    P(f"    three distinct angle-bands? {distinct}   ·   S<M<L monotone at these peaks? {monotone}")
    assert distinct, "trichromacy requires three DISTINCT angle-bands"
    P("    → the eye reads colour as three angles (trichromacy). Globally χ(λ) is "
      "hypersensitive/distributional")
    P("      (inherited honesty: not a smooth monotone lookup); the felt colour percept is the "
      "mind volume's. [F]/[O]")

    # ----------------------------------------------------------------------------------------
    # PART B — emerge the cone/rod lineage via the R19 Organ
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — emerge the cone/rod lineage via the R19 Organ (order = argsort(spinodal(γ)))")
    P("-" * 80)

    # build every gene as the inherited Organ primitive (consume the substrate; do not reimplement)
    organs = {}
    for sym, rec in ATLAS.items():
        o = Organ(sym, rec["gamma"], layer=rec["node"])
        organs[sym] = o
        # the Organ recomputes spinodal from γ via the FROZEN formula; the atlas lists the same
        # quantity computed from full-precision γ then rounded — agree within one γ-rounding unit.
        assert abs(o.spinodal - rec["spinodal"]) < 2e-4, \
            f"{sym}: Organ spinodal must match measured atlas (γ-rounding tol)"

    # the cone/rod photoreceptor lineage (stated by node), emerged by the substrate's forced key [F]
    lineage = [s for s, r in ATLAS.items() if r["node"] in LINEAGE_NODES]
    lineage.sort(key=lambda s: organs[s].functional_spinodal())     # argsort(spinodal(γ)) ascending
    P("the cone/rod lineage (nodes: cone_color_angle, rod, rod_phototransduction, photoreceptor),")
    P("emerged by the substrate rule — lowest spinodal flips first:  [F] order · [F] dwell∝γ^1.5 (abs [O])")
    P(f"  {'rank':>4} {'gene':9s} {'node':22s} {'γ':>8s} {'spinodal':>9s} {'rel.dwell':>9s}")
    base = organs[lineage[0]].size()
    for k, sym in enumerate(lineage, 1):
        o = organs[sym]
        rel = o.size() / base
        mark = "  ← cone" if ATLAS[sym]["node"] == "cone_color_angle" else ""
        P(f"  {k:4d} {sym:9s} {ATLAS[sym]['node']:22s} {o.g:8.4f} {ATLAS[sym]['spinodal']:9.4f} {rel:9.4f}{mark}")

    # the three cones' positions within the lineage
    cone_ranks = {s: lineage.index(s) + 1 for s in ("OPN1SW", "OPN1MW", "OPN1LW")}
    P(f"\n  cone ranks in the lineage: " +
      ", ".join(f"{s}={cone_ranks[s]}" for s in ("OPN1SW", "OPN1MW", "OPN1LW")))
    P("  [O] whether this substrate order maps onto real retinal developmental TIME is an open")
    P("      empirical question — obstacle: needs developmental-timing data; NOT fitted, NOT assumed.")

    # ----------------------------------------------------------------------------------------
    # PART C — the A4 tie-break (do not collapse equal-γ genes)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — A4 tie-break: equal-γ genes are NOT interchangeable (DNA v1.13)")
    P("-" * 80)
    P("order key (TOTAL): primary = spinodal(γ); tie-break = A4 shape "
      "(amplitude → stiffest_offset → symbol).")
    P("the A4 key acts ONLY as a tie-break — for distinct γ, γ alone decides; it is a stated")
    P("derived convention, not a fit.")

    # attach symbol so shape_key is self-contained, then verify the FULL key is a strict total order
    recs = {s: dict(r, _sym=s) for s, r in ATLAS.items()}
    full_key = {s: (round(organs[s].spinodal, 4), shape_key(recs[s])) for s in ATLAS}
    n_unique = len({full_key[s] for s in ATLAS})
    P(f"\n[total order] full key gives {n_unique}/{len(ATLAS)} unique ranks → no two genes collapse.")
    assert n_unique == len(ATLAS), "the full (spinodal, A4-shape) key must give every gene a unique rank"

    # the REAL demonstration: CNGA1 vs CNGB1 — closest γ pair, the rod CNG α/β subunits
    a, b = recs["CNGA1"], recs["CNGB1"]
    dg = abs(a["gamma"] - b["gamma"])
    P(f"\n[real near-degeneracy] CNGA1 vs CNGB1 — the rod CNG channel α/β subunits, "
      f"closest γ pair in the atlas:")
    P(f"    CNGA1: γ={a['gamma']:.4f} spinodal={a['spinodal']:.4f} "
      f"shape_amp={a['shape_amplitude']:.5f} stiffest_off={a['stiffest_offset_bp']}")
    P(f"    CNGB1: γ={b['gamma']:.4f} spinodal={b['spinodal']:.4f} "
      f"shape_amp={b['shape_amplitude']:.5f} stiffest_off={b['stiffest_offset_bp']}")
    P(f"    Δγ = {dg:.4f}")

    # at 3-decimal γ resolution they COLLAPSE: reading γ ALONE makes them interchangeable
    ga3, gb3 = round(a["gamma"], 3), round(b["gamma"], 3)
    sa3, sb3 = round(a["spinodal"], 3), round(b["spinodal"], 3)
    collapse = (ga3 == gb3) and (sa3 == sb3)
    P(f"    at 3-decimal γ resolution: CNGA1 γ→{ga3:.3f}/spinodal→{sa3:.3f}, "
      f"CNGB1 γ→{gb3:.3f}/spinodal→{sb3:.3f}")
    P(f"    γ-ALONE collapses them to one value? {collapse}  ← the failure mode (genes read as identical)")
    assert collapse, "CNGA1/CNGB1 must collapse at γ-only 3-decimal resolution (the tie to break)"

    # the A4 shape breaks the degeneracy deterministically
    ratio = max(a["shape_amplitude"], b["shape_amplitude"]) / min(a["shape_amplitude"], b["shape_amplitude"])
    broken = sorted(("CNGA1", "CNGB1"), key=lambda s: shape_key(recs[s]))
    P(f"    A4 shape_amplitude differs {ratio:.2f}× → shape tie-break orders them: "
      f"{broken[0]} before {broken[1]}  [V]")
    P("    → two genes with equal γ but different A4 shape are NOT interchangeable: the emergence")
    P("      reads LEVEL (γ) AND SHAPE (A4), never γ alone.")

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E1 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the angle law λ→χ and the 633/532 anchor; the three distinct angle-bands;")
    P("                 the R19 order = argsort(spinodal(γ)); dwell ∝ γ^1.5; the A4 tie-break rule.")
    P("  [V] verified : Organ spinodal == measured atlas for all 16 genes; the full (spinodal,A4)")
    P("                 key is a strict total order; CNGA1/CNGB1 collapse under γ-alone and are")
    P("                 broken by A4 shape. (γ+A4 themselves re-proved offline by verify_seed [3].)")
    P("  [L] measured : every γ + A4 (NCBI promoters, cached); the cone λmax (S420/M530/L560, lit.).")
    P("  [O] open     : absolute angle→firing and photon→Hz scale (E2 / calibration); whether the")
    P("                 substrate order matches real developmental TIME (needs timing data); the")
    P("                 full A4 anchor/loop/anchor-phase (needs the NCBI feature table); the FELT")
    P("                 colour percept (→ mind volume). Each obstacle named, never invented.")
    P("\nLEARNED: the eye reads colour as the light-propagation ANGLE χ(λmax) — three cone opsins at")
    P("         three distinct angle-bands = trichromacy — and the cone/rod lineage EMERGES from the")
    P("         R19 switch ordered by spinodal(γ), with the A4 SHAPE breaking γ-degeneracies (equal-γ")
    P("         genes are not interchangeable). Foundation untouched; nothing fitted; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
