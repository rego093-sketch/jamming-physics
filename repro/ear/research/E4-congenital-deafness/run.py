#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E4 :  congenital DEAFNESS as an R19 FAILURE-MODE decomposition (the goal).

WHAT THIS BUILDS (BLUEPRINT.md E-plan, slot E4 — the volume's destination).
  The congenital-deafness genes — GJB2, GJB6 (DFNB1, the commonest), SLC26A4 (Pendred/DFNB4), LHFPL5
  (DFNB67), MYO15A (DFNB3), USH2A, MYO7A (Usher), OTOF (auditory neuropathy/DFNB9), with SLC26A5
  (prestin, the E3 amplifier) as the fourth class — are read NOT one-by-one but as a DECOMPOSITION of
  the inherited R19 cubic. The keystone: the cubic ṡ = g·s − s³ + h has exactly THREE loci a
  congenital sensory switch can fail at — its STRUCTURE g, its DRIVE h, or the layer DOWNSTREAM of the
  flip — plus the CRITICAL regime g→0 (the E3 amplifier). Every deafness gene maps to ONE locus by its
  cited protein function, and the R19 geometry then forces a DIFFERENT substrate-inverse lever DIRECTION
  for each class — direction-only, proposal-only, never a diagnosis, dose, molecule, or efficacy.

  This is the firewall made constructive. Two of the four classes yield HONEST NEGATIVES forced by the
  cubic itself: a STRUCTURE-class failure (g→0) cannot be rescued by any drive h (the switch is gone,
  not un-driven), and a READOUT-class failure is invisible to the cubic (the switch flips fine; the
  broken layer is downstream). Only the DRIVE class (connexins, pendrin — the apparatus is whole, the
  power is off) and the AMPLIFIER class admit a substrate-inverse lever, and even there only the
  DIRECTION is forced.

THE BIOLOGY (cited, not re-opened; identity/function are the DNA + biology volumes', consumed here).
  • DRIVE  (h): GJB2/GJB6 gap-junction K⁺ recycling to endolymph (DFNB1); SLC26A4 pendrin Cl⁻/HCO₃⁻
    exchange, endolymph ion/pH homeostasis (Pendred). These maintain the endolymphatic ENVIRONMENT that
    supplies the MET drive — the switch apparatus is intact; h has collapsed below the spinodal.
  • STRUCTURE (g): LHFPL5 (MET-complex/tip-link tension), MYO15A (stereocilia elongation), USH2A
    (usherin scaffold/ankle-links), MYO7A (myosin VIIa tip-link tension); TMC1 (the pore) is the E1/E2
    reference. These BUILD the mechanotransduction apparatus — the gating spring itself.
  • READOUT (downstream): OTOF otoferlin, the Ca²⁺ sensor for ribbon-synapse vesicle fusion. The hair
    cell transduces normally; the failure is transmission to the nerve (auditory neuropathy).
  • AMPLIFIER (g→0 critical): SLC26A5 prestin (E3) — loss of operation at the critical point loses the
    F^(−2/3) gain (elevated thresholds, lost compression).

HOW IT RELATES TO THE FOUNDATION (no-regression).
  EXTENDS the inherited foundation by IMPORTING it — not one inherited byte is edited (frozen hashes
  valid). It consumes the INHERITED `vp_substrate.py` cubic directly (`sdot`/`settle`/`spinodal`/
  `barrier`/`is_on`) — the failure loci are read off the SAME math the E1 switch and E3 amplifier use —
  plus the measured atlas via E1's `read_measured` (every deafness gene's γ+A4 recomputes from the
  frozen cache and equals the atlas bit-for-bit). The three new genes (SLC26A4, LHFPL5, MYO15A) were
  fetched from NCBI by the shipped fetcher and folded into the cache+atlas; their hashes were re-frozen
  deliberately (INHERITANCE_LEDGER.md), never silently.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the cubic's THREE failure loci (g / h / downstream) + the critical regime ; DRIVE-class
            recoverability (an intact-g switch flips once h is restored past spinodal) ; STRUCTURE-class
            NON-rescuability (the bistable window 2·spinodal(g) → 0 as g→0 — forced by the cubic
            discriminant — so no drive flips it) ; the amplifier F^(−2/3) gain (E3, re-shown) ; the
            emergence placement order argsort(spinodal(γ)) ; and the firewall-enforcing negative that
            γ/A4 do NOT separate the failure classes.
  [L]      : every γ (NCBI-measured, cached) ; the failure-class LABELS are cited protein function
            (DNA + biology volumes), not derived from γ here.
  [O]      : every magnitude / threshold in physical units ; the molecule / dose / in-vivo selectivity /
            efficacy of ANY lever (firewall — proposal-only) ; the synaptic READOUT layer (OTOF — not
            modelled by this transduction substrate) ; the felt percept of hearing (→ mind volume) ;
            and the full fluid-loaded dispersive traveling-wave ENVELOPE (still the named [O] — a
            closed envelope would require TUNING Q, forbidden). Each names its obstacle below.

FIREWALL. γ reads promoter STRUCTURE only — never a channel function, a drive magnitude, a motor force,
a dose, an in-vivo selectivity, or a clinical effect. The disease layer is PROPOSAL-ONLY: direction-only
R19 failure modes and substrate-inverse lever DIRECTIONS. Nothing here diagnoses, treats, or prescribes;
no molecule is designed; no dose or efficacy is stated. The felt percept of sound is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E4-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate   as SUB                              # the R19 cubic (sdot/settle/spinodal/barrier)
import vp_sound_wave  as SND                              # √-law place map (Greenwood form)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (every increment ships a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's read_measured (asserts cache==atlas, A4⊥, exact-precision spinodal) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

# ---- the E4 deafness genes, each tagged with its CITED failure class (biology, not γ) -------------
# class ∈ {drive (h), structure (g), readout (downstream), amplifier (g→0)}.  TMC1 = the structure
# reference (E1/E2 pore); SLC26A5 = the amplifier reference (E3).  γ is measured; the CLASS is cited.
DEAF = [
    ("GJB2",    "drive",     "connexin 26 — gap-junction K⁺ recycling to endolymph (DFNB1, commonest)"),
    ("GJB6",    "drive",     "connexin 30 — same K⁺-recycling pathway (DFNB1)"),
    ("SLC26A4", "drive",     "pendrin — Cl⁻/HCO₃⁻ exchange, endolymph ion/pH homeostasis (Pendred/DFNB4)"),
    ("LHFPL5",  "structure", "MET-complex member, tip-link tension (DFNB67)"),
    ("MYO15A",  "structure", "myosin XVa — stereocilia elongation/structure (DFNB3)"),
    ("USH2A",   "structure", "usherin — stereocilia ankle-link scaffold (Usher type 2)"),
    ("MYO7A",   "structure", "myosin VIIa — tip-link tension/adaptation (Usher type 1)"),
    ("OTOF",    "readout",   "otoferlin — Ca²⁺ sensor for ribbon-synapse fusion (auditory neuropathy/DFNB9)"),
    ("SLC26A5", "amplifier", "prestin — OHC somatic motor at criticality (E3 amplifier)"),
    ("TMC1",    "structure", "the MET pore itself (E1/E2 switch reference)"),
]
CLASSES = ("drive", "structure", "readout", "amplifier")

# the converged drive range for the amplifier-gain [V] (identical convention to E3; N5 there)
_F_LO_EXP, _F_HI_EXP, _F_N, _SETTLE_N = -1.0, 2.0, 10, 20000


def drive_grid():
    return [10.0 ** e for e in np.linspace(_F_LO_EXP, _F_HI_EXP, _F_N)]


def analytic_bistable_width(g):
    """The width in DRIVE h of the bistable (two-stable-state) window of the inherited cubic =
    2·spinodal(g) = 4·(g/3)^1.5. This is the SWITCH's defining property — the range of drive over which
    an all-or-none flip exists. Forced by the cubic's discriminant; → 0 as the STRUCTURE g → 0.  [F]"""
    return 2.0 * SUB.spinodal(g)


def measured_hysteresis_width(g, pad=0.2, npts=400, n_settle=400):
    """CONFIRM the switch on the inherited integrator: sweep drive h up (from OFF) then down (from ON)
    with continuation; return the h-gap between the up-flip and the down-flip = the hysteresis loop
    width. At intact g this ≈ 2·spinodal(g); as g→0 it collapses to the h-grid floor (no real switch).
    The rigorous [F] is `analytic_bistable_width`; this is the [V] confirmation (grid-resolution bound)."""
    if g <= 0:
        return 0.0
    H  = analytic_bistable_width(g) + pad
    hs = np.linspace(-H, H, npts)
    s  = -math.sqrt(g); up = None
    for h in hs:
        s = SUB.settle(g, h, s0=s, n=n_settle)
        if up is None and s > 0: up = float(h)
    s = math.sqrt(g); dn = None
    for h in hs[::-1]:
        s = SUB.settle(g, h, s0=s, n=n_settle)
        if dn is None and s < 0: dn = float(h)
    return (up - dn) if (up is not None and dn is not None) else 0.0


# =====================================================================================================
def run(P):
    P("=" * 94)
    P("E4 — congenital DEAFNESS as an R19 FAILURE-MODE decomposition (the goal)")
    P("     each deafness gene → ONE locus of the inherited cubic ṡ=g·s−s³+h → a direction-only lever")
    P("=" * 94)

    # -- PART 0 : every E4 gene reproduces offline (γ LEVEL + A4 SHAPE) --------------------------------
    P("\n[0] every E4 deafness gene reproduces offline (γ LEVEL + A4 SHAPE, recomputed from frozen cache):")
    recs = {}
    for sym, cls, note in DEAF:
        r = E1.read_measured(sym); recs[sym] = r
        P(f"    [PASS] {sym:8s} γ={r['gamma']:.4f}  A4 amp={r['shape_amplitude']:.5f} "
          f"spinodal={r['spinodal']:.4f}  class=[{cls}]  ({r['node']})")
    P("    -> every γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9). The three")
    P("       newly-fetched genes (SLC26A4, LHFPL5, MYO15A) recompute identically — hashes re-frozen.  [V]")

    # -- PART A : the cubic has exactly THREE failure loci + the critical regime -----------------------
    P("\n[A] the keystone — the inherited cubic ṡ=g·s−s³+h has exactly THREE loci a switch can fail at:")
    P("      • STRUCTURE g : the gating apparatus (sets the bistable window 2·spinodal(g)=4(g/3)^1.5)")
    P("      • DRIVE     h : the deflection/endolymphatic power that pushes s past the spinodal")
    P("      • READOUT     : the layer AFTER the flip (the cubic is intact; the broken part is downstream)")
    P("      • + CRITICAL g→0 : the E3 amplifier regime (the F^(−2/3) gain) — a fourth, distinct failure")
    P("    each deafness gene maps to ONE locus by its CITED protein function (γ does NOT assign it — H):")
    for cls in CLASSES:
        members = [s for s, c, _ in DEAF if c == cls]
        P(f"      [{cls:9s}] {', '.join(members)}")

    # -- PART B : DRIVE class is RECOVERABLE — intact g flips once h is restored past spinodal ---------
    P("\n[B] DRIVE class (connexins / pendrin) — the apparatus is WHOLE, the power is OFF; it RECOVERS:")
    gT = recs["TMC1"]["gamma"]; sp = SUB.spinodal(gT)        # an intact MET switch (structure present)
    off = SUB.settle(gT, 0.0); on = SUB.settle(gT, 1.5 * sp)
    P(f"    a structurally-intact switch g=γ_TMC1={gT:.4f} (spinodal={sp:.4f}):")
    P(f"       drive h=0      (endolymphatic power removed = the K⁺-recycling failure): s={off:+.4f} OFF")
    P(f"       drive h=1.5·sp (power restored past the spinodal):                       s={on:+.4f} ON")
    P("    -> the SAME intact switch flips ON once drive is restored — the DRIVE-class failure is")
    P("       RECOVERABLE in principle. Substrate-inverse lever (DIRECTION ONLY, proposal-only):")
    P("       restore h toward/past +spinodal(g). The DIRECTION is forced by the cubic.  [F]/[V]")
    P("       (magnitude, molecule, dose, in-vivo selectivity, efficacy — all [O], firewall.)")
    assert off < 0 and on > 0

    # -- PART C : STRUCTURE class is NOT drive-rescuable — the bistable window vanishes as g→0 ---------
    P("\n[C] STRUCTURE class (stereocilia / tip-link genes) — the switch ITSELF is gone; drive can't help:")
    P("    the SWITCH = a finite bistable window in drive; its width is set by the STRUCTURE g, not h:")
    P("       analytic bistable width 2·spinodal(g)=4(g/3)^1.5  [F]  · integrator hysteresis loop  [V]")
    grid = [1.30, 0.80, 0.40, 0.10, 0.01]
    widths = []
    for g in grid:
        aw = analytic_bistable_width(g); mw = measured_hysteresis_width(g); widths.append(aw)
        P(f"       structure g={g:4.2f}  analytic width={aw:.4f}  integrator loop={mw:.4f}")
    mono = all(widths[i] > widths[i + 1] for i in range(len(widths) - 1))
    P(f"    -> the bistable window is MONOTONE in g ({mono}) and → 0 as g → 0 "
      f"(2·spinodal(0.01)={analytic_bistable_width(0.01):.5f}).")
    P("       Drive h moves you ALONG the h-axis; it cannot restore the window the lost STRUCTURE g")
    P("       created. So NO finite drive flips a structure-class failure — an HONEST NEGATIVE forced by")
    P("       the cubic's discriminant. The lever must act on g (the structural/genetic layer), which")
    P("       this substrate cannot supply; the firewall forbids claiming a fix.  [F]/[V]")
    assert mono and analytic_bistable_width(0.01) < 1e-3
    # the integrator loop at intact g vastly exceeds the grid floor at degraded g (the [V] contrast)
    assert measured_hysteresis_width(1.30) > 20.0 * analytic_bistable_width(0.01)

    # -- PART D : READOUT class is INVISIBLE to the cubic — the switch flips fine, the wire is cut -----
    P("\n[D] READOUT class (OTOF / auditory neuropathy) — the switch flips NORMALLY; the cubic is intact:")
    flip_off = SUB.settle(gT, 0.0); flip_on = SUB.settle(gT, 1.5 * sp)
    P(f"    the hair-cell MET switch in an OTOF patient (g=γ_TMC1={gT:.4f}) flips just as a hearing one:")
    P(f"       sub-threshold drive -> s={flip_off:+.4f} OFF ; supra-threshold drive -> s={flip_on:+.4f} ON")
    P("    -> the substrate sees NOTHING wrong: transduction is normal. The failure is the Ca²⁺-triggered")
    P("       ribbon-synapse RELEASE — the layer DOWNSTREAM of the flip, which this cubic does not model.")
    P("       Substrate-inverse lever: the cubic is the WRONG layer; no (g,h) change addresses it. The")
    P("       intervention layer is the synapse.  HONEST scope statement; the synaptic layer is [O].")
    assert flip_off < 0 and flip_on > 0

    # -- PART E : AMPLIFIER class (the E3 bridge) — losing criticality loses the F^(−2/3) gain ---------
    P("\n[E] AMPLIFIER class (prestin / SLC26A5) — the E3 bridge: criticality lost ⇒ the F^(−2/3) gain lost:")
    Fs = drive_grid()
    rs = [SUB.settle(0.0, F, n=_SETTLE_N, dt=0.01) for F in Fs]
    gains = [rs[i] / Fs[i] for i in range(len(Fs))]
    gslope = float(np.polyfit(np.log10(Fs), np.log10(gains), 1)[0])
    P(f"    at the critical point g=0 the inherited integrator gives gain r/F ∝ F^(−2/3) "
      f"(fitted exponent={gslope:.6f}):")
    P(f"       gain at faint F={Fs[0]:.2g}: {gains[0]:7.2f}   at loud F={Fs[-1]:.2g}: {gains[-1]:6.3f}   "
      f"(faint/loud = {gains[0]/gains[-1]:.0f}×)")
    P("    -> outer-hair-cell / prestin failure pulls the operating point OFF criticality: the F^(−2/3)")
    P("       compression collapses ⇒ elevated thresholds + lost dynamic range (sensorineural loss).")
    P("       Substrate-inverse lever: restore operation toward the critical point g→0⁺ (DIRECTION only).")
    P("       Exponent/direction [F] (E3); absolute gain/dB/Q [O] (E3 N1).  [F]/[V]")
    assert abs(gslope - (-2.0 / 3.0)) < 1e-6

    # -- PART F : the substrate-inverse lever TABLE (direction-only, proposal-only) --------------------
    P("\n[F] the substrate-inverse lever — DIRECTION-ONLY, PROPOSAL-ONLY (the firewall, made constructive):")
    P("    +----------- +------------------- +------------------------------- +----------------------+")
    P("    | class      | failed locus       | R19 lever (DIRECTION ONLY)     | drive-recoverable?   |")
    P("    +----------- +------------------- +------------------------------- +----------------------+")
    P("    | drive      | h < spinodal(g)    | restore h toward +spinodal(g)  | YES — apparatus whole|")
    P("    | structure  | g → 0              | act on g (structural layer)    | NO  — geometry forbids|")
    P("    | readout    | downstream of cubic| act on the synapse layer       | N/A — wrong layer    |")
    P("    | amplifier  | criticality g→0    | restore operation at g→0⁺      | partial — magnitude[O]|")
    P("    +----------- +------------------- +------------------------------- +----------------------+")
    P("    Every cell is a DIRECTION — no dose, molecule, selectivity, or efficacy. TWO of four are honest")
    P("    negatives (structure forbids drive-rescue; readout is the wrong layer). The framework's most")
    P("    useful HONEST output for the congenitally affected: it says which failures are switch-")
    P("    recoverable IN PRINCIPLE (drive: connexins/pendrin — power off, switch whole) and which are")
    P("    NOT (structure: the switch must be rebuilt) — and refuses to promise any of them a treatment.")

    # -- PART G : EMERGE the placement — the deafness genes ARE the lineage genes, classified ----------
    P("\n[G] EMERGE the placement — order = argsort(spinodal(γ)); the deafness genes interleave the lineage:")
    rows = sorted((recs[s] for s, _, _ in DEAF), key=lambda r: r["spinodal"])
    cls_of = {s: c for s, c, _ in DEAF}
    for i, r in enumerate(rows, 1):
        P(f"    {i:2d}. {r['sym']:8s} spinodal={r['spinodal']:.4f}  γ={r['gamma']:.4f}  "
          f"class=[{cls_of[r['sym']]:9s}]  [{r['node']}]")
    P("    -> the deafness genes are NOT a separate catalogue: they ARE the emergence-lineage genes, read")
    P("       by WHERE on the cubic each fails. Order [F]; γ measured [L]; class cited [L].")

    # -- PART H : the firewall-enforcing negative — γ/A4 do NOT separate the failure classes -----------
    P("\n[H] the firewall negative — γ (and A4) do NOT separate the failure classes (γ is structure-only):")
    by = {c: [recs[s]["gamma"] for s, cc, _ in DEAF if cc == c] for c in CLASSES}
    for c in CLASSES:
        v = by[c]
        P(f"       [{c:9s}] γ ∈ [{min(v):.4f}, {max(v):.4f}]   (n={len(v)})")
    dg, sg = by["drive"], by["structure"]
    overlap = max(0.0, min(max(dg), max(sg)) - max(min(dg), min(sg)))
    # is there ANY γ-threshold τ that puts all drive-class on one side and all structure on the other?
    separable = (max(dg) < min(sg)) or (max(sg) < min(dg))
    P(f"    drive↔structure γ-range overlap = {overlap:.4f}; a single γ-threshold separates them? "
      f"{separable}")
    P("    -> γ CANNOT assign the failure class — it reads promoter STRUCTURE (stiffness), not protein")
    P("       FUNCTION. The class labels come from cited biology; the R19 geometry supplies the lever.")
    P("       This is the firewall, quantified: γ never becomes a function, a drive, a dose, or an effect.  [V]")
    assert overlap > 0.0 and not separable

    # -- honest negatives preserved as the starting line for the next attempt --------------------------
    P("\n[honest negatives — preserved, not hidden]")
    P("    N1  EVERY physical magnitude is [O] — the drive in volts/Hz, the structural g in real units,")
    P("        the amplifier gain/dB/Q, any threshold value. Only DIRECTIONS and EXPONENTS are forced.")
    P("    N2  the failure CLASS is cited protein function, NOT derived from γ ([H] proves γ can't assign")
    P("        it). A gene with mixed roles (e.g. MYO7A in both tip-link tension and transport) is placed")
    P("        by its dominant transduction role; finer multi-locus failure is [O].")
    P("    N3  the substrate-inverse lever is PROPOSAL-ONLY and direction-only. No molecule is designed,")
    P("        no dose or efficacy is stated, nothing is diagnosed or treated (firewall).")
    P("    N4  the READOUT layer (OTOF/synapse) is NOT modelled by this transduction cubic — its rescue")
    P("        direction is [O] (a different substrate: Ca²⁺-vesicle release).")
    P("    N5  the amplifier-gain [V] inherits E3's small-drive under-convergence (E3 N5): the rigorous")
    P("        result is the analytic fixed point; the integrator fit holds on the converged range.")
    P("    N6  the full fluid-loaded dispersive traveling-wave ENVELOPE is STILL the named [O] — a closed")
    P("        envelope needs Q + fluid mass-loading + the E3 amplifier, and would require TUNING Q")
    P("        (forbidden). E4 does not touch it; it remains open with its obstacle named.")

    # -- naming note (E4 folder is unambiguous; the v0.3.0 folder-numbering reconciliation still pends) --
    P("\n[naming note] This delivers BLUEPRINT-E4 in the unambiguous folder research/E4-congenital-deafness/.")
    P("    The v0.3.0 folder-numbering slip stands flagged (BLUEPRINT-E2 shipped in the folder labelled E1;")
    P("    BLUEPRINT-E1, the traveling-wave ENVELOPE, remains the named [O]). A future session may reconcile")
    P("    BLUEPRINT.md's E-numbering with the folder names; E4 itself introduces no new inconsistency.")

    P("\nLEARNED (E4): congenital deafness DECOMPOSES onto the inherited R19 cubic — every gene fails at")
    P("  its STRUCTURE g, its DRIVE h, the READOUT downstream, or the CRITICAL regime (the E3 amplifier).")
    P("  The geometry forces a DIFFERENT direction-only lever per class and yields two HONEST NEGATIVES:")
    P("  structure-class failures can't be drive-rescued (the switch is gone, not un-driven), and readout")
    P("  failures are invisible to the cubic (the switch flips; the wire is cut). γ cannot assign the")
    P("  class — it is structure-only — so the labels are cited biology and the levers are proposal-only.")
    P("  The disease layer states DIRECTIONS, never doses: the firewall made constructive for research.")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
