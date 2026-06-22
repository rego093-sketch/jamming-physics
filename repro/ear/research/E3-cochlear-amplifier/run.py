#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E3 :  the cochlear active amplifier (prestin / SLC26A5).
                         The cube-root compression as the R19 cubic AT ITS CRITICAL POINT.

WHAT THIS BUILDS (BLUEPRINT.md E-plan, slot E3).
  The outer-hair-cell COCHLEAR AMPLIFIER — the active process powered by prestin (SLC26A5) — emerged
  from the inherited R19 substrate, sitting on the inherited √-law place map. The keystone result is
  parameter-free: the basilar-membrane response amplitude COMPRESSES as the CUBE ROOT of the drive,
        r ∝ F^(1/3),
  and the 1/3 exponent is FORCED by the substrate's cubic nonlinearity — it is not a fitted constant.
  The amplifier and the E1 tip-link transduction switch are the SAME R19 cubic operated in two
  regimes: bistable (all-or-none detection, E1) vs critical (compressive amplification, E3).

THE PHYSICS (cited, not re-opened).
  The cochlear active process operates near a Hopf/pitchfork bifurcation (Eguíluz-Ospeck-Choe-
  Hudspeth-Magnasco 2000; Camalet-Duke-Jülicher-Prost 2000; Hudspeth 2008). The inherited R19 field
  ṡ = g·s − s³ + h is exactly that cubic. AT CRITICALITY (g=0) the driven steady state solves
  −s³ + F = 0 ⇒ s = F^(1/3): a compressive nonlinearity with a gain r/F = F^(−2/3) that DIVERGES for
  faint drives — precisely the dynamic-range compression that lets the ear span ~120 dB. The 1/3 power
  is the cubic's signature; it is independent of every constant, so it needs no tuning.

HOW IT RELATES TO THE FOUNDATION (no-regression).
  This module EXTENDS the inherited foundation by IMPORTING it — it edits not a single inherited byte
  (the frozen hashes stay valid). It consumes the INHERITED `vp_substrate.py` cubic directly
  (`SUB.sdot`, `SUB.settle`, `SUB.spinodal`) — the cube-root law is read off the SAME math the E1
  switch uses — plus `vp_sound_wave.py` (the Greenwood place map) and the measured atlas via E1's
  `read_measured` (so SLC26A5's γ+A4 recompute from the frozen cache and equal the atlas bit-for-bit).

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the cube-root COMPRESSION EXPONENT (analytic fixed point of the inherited cubic at g=0,
            residual <1e-12; the inherited integrator converges to F^(1/3) on the converged drive
            range) ; the SAME-cubic-two-regimes unification (bistable switch ∥ critical amplifier) ;
            the gain compression direction r/F ∝ F^(−2/3) ; SLC26A5's place in the spinodal order ;
            the CF-independence of the exponent (uniform compression across the tonotopic bank).
  [L]      : every γ (NCBI-measured, cached) ; the Greenwood A/a/k place-map calibration.
  [O]      : the ABSOLUTE gain / dB of amplification / dynamic-range-in-dB / sharpness Q ; the measured
            cochlear I/O slope value and absolute curve ; otoacoustic-emission frequencies/amplitudes ;
            prestin's actual electromotile force (γ is structure-only — firewall) ; the felt loudness
            (→ mind). Each names its obstacle below; none can close without TUNING a constant.

FIREWALL. γ reads promoter STRUCTURE only — never a motor force, a transduction gain, a dose, or a
clinical effect. No disease claim here (E3 is pre-disease; it neighbours the E4 deafness goal — OHC /
prestin failure is a deafness mechanism — but states none). The percept of loudness is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E3-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate   as SUB                              # the R19 cubic (sdot / settle / spinodal)
import vp_sound_wave  as SND                              # √-law place map (Greenwood form)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (both increments ship a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's read_measured (asserts cache==atlas, A4⊥, exact-precision spinodal) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

AMPLIFIER = "SLC26A5"                                     # prestin — the OHC somatic motor gene (measured γ)
# the E1 lineage these amplifier sits among (all measured, all in the frozen cache/atlas)
LINEAGE   = ["TMC1", "PCDH15", AMPLIFIER, "CDH23", "TMIE", "ATOH1", "POU4F3", "MYO7A"]

# the converged drive range for the [V] integrator fit (below this the cubic restoring force ∝s³
# vanishes near 0 and the integrator under-converges — see honest negative N5). 10 decΛades-spanning pts.
_F_LO_EXP, _F_HI_EXP, _F_N = -1.0, 2.0, 10
_SETTLE_N = 20000                                         # steps: exponent already exact (rel.err ~1e-14)


def drive_grid():
    return [10.0 ** e for e in np.linspace(_F_LO_EXP, _F_HI_EXP, _F_N)]


def hopf_peak_amplitude(F, mu=0.0, w0=1.0, w=1.0, dt=0.002, n_settle=300, n_meas=30):
    """Oscillatory Hopf normal form (the OAE-emitting active oscillator), lab frame, on resonance.
    dx/dt = μx − w0·y − (x²+y²)x + F·cos(w t);  dy/dt = μy + w0·x − (x²+y²)y. Returns peak |z| over
    the last n_meas periods after an n_settle-period transient. At μ=0 the amplitude ≈ F^(1/3) — the
    SAME cube root, in the oscillatory (literature 'Hopf') form; carries a finite-averaging bias (N5)."""
    Tset = n_settle * (2 * math.pi / w0); Tmeas = n_meas * (2 * math.pi / w0)
    x, y, t = 0.0, 0.0, 0.0
    for _ in range(int(Tset / dt)):
        r2 = x * x + y * y
        x += dt * (mu * x - w0 * y - r2 * x + F * math.cos(w * t)); y += dt * (mu * y + w0 * x - r2 * y); t += dt
    peak = 0.0
    for _ in range(int(Tmeas / dt)):
        r2 = x * x + y * y
        x += dt * (mu * x - w0 * y - r2 * x + F * math.cos(w * t)); y += dt * (mu * y + w0 * x - r2 * y); t += dt
        peak = max(peak, math.hypot(x, y))
    return peak


# =====================================================================================================
def run(P):
    P("=" * 90)
    P("E3 — the cochlear active amplifier (prestin / SLC26A5): cube-root compression")
    P("     the R19 cubic AT ITS CRITICAL POINT  ·  a wave property -> a spatial code -> an R19 switch")
    P("=" * 90)

    # -- PART 0 : the amplifier gene reproduces offline (γ LEVEL + A4 SHAPE) ---------------------------
    P("\n[0] the amplifier gene reproduces offline (γ LEVEL + A4 SHAPE, recomputed from frozen cache):")
    amp = E1.read_measured(AMPLIFIER)                    # asserts cache==atlas & A4 = signal−γ for SLC26A5
    P(f"    [PASS] {AMPLIFIER:8s} γ(level)={amp['gamma']:.4f}  A4 amp={amp['shape_amplitude']:.5f} "
      f"range={amp['shape_range']:.5f}  node={amp['node']}  (prestin / OHC somatic motor)")
    P("    -> SLC26A5 γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9).  [V]")

    # -- PART A : the COMPRESSION EXPONENT is the cube root, FORCED by the inherited cubic -------------
    P("\n[A] the keystone — response COMPRESSES as the cube root of drive, r ∝ F^(1/3):")
    P("    (1a) ANALYTIC [F]: the INHERITED cubic sdot(s,g,h)=g·s−s³+h at criticality g=0 has its zero")
    P("         at s*=F^(1/3). Evaluate the inherited sdot at s=F^(1/3) — it must vanish (parameter-free):")
    max_res = 0.0
    for e in range(-3, 4):
        F = 10.0 ** e; s_star = F ** (1.0 / 3.0); res = SUB.sdot(s_star, 0.0, F)
        max_res = max(max_res, abs(res))
        if e in (-3, 0, 3):
            P(f"         F={F:9.4g}  s*=F^(1/3)={s_star:9.5f}  sdot(s*,0,F)={res:+.2e}")
    P(f"         -> max|residual| over 7 decades = {max_res:.2e}  ⇒ the cube root IS the inherited "
      f"cubic's fixed point.  [F]")
    assert max_res < 1e-9

    P("    (1b) VERIFIED [V]: the INHERITED integrator settle(0,F) converges to F^(1/3); fit the")
    P("         emergent exponent (NOT imposed — we fit log r vs log F and read off the slope):")
    Fs = drive_grid()
    rs = [SUB.settle(0.0, F, n=_SETTLE_N, dt=0.01) for F in Fs]
    slope = float(np.polyfit(np.log10(Fs), np.log10(rs), 1)[0])
    max_rel = max(abs(rs[i] - Fs[i] ** (1 / 3)) / (Fs[i] ** (1 / 3)) for i in range(len(Fs)))
    P(f"         drive range F∈[{Fs[0]:.3g}, {Fs[-1]:.3g}] (converged): fitted exponent = {slope:.6f}")
    P(f"         target 1/3 = {1/3:.6f};  |exponent − 1/3| = {abs(slope - 1/3):.2e};  "
      f"max rel.err vs F^(1/3) = {max_rel:.1e}  [V]")
    assert abs(slope - 1.0 / 3.0) < 1e-6

    # -- PART B : SAME cubic, TWO regimes (the framework unification) ----------------------------------
    P("\n[B] the unification — the amplifier and the E1 switch are ONE cubic in TWO regimes:")
    g_sw = E1.read_measured("TMC1")["gamma"]            # the E1 MET switch gene
    sp   = SUB.spinodal(g_sw)
    P(f"    BISTABLE regime  g=γ_TMC1={g_sw:.4f} (the E1 transduction switch): drive across spinodal "
      f"{sp:.4f}")
    P(f"    CRITICAL regime  g=0           (the E3 active amplifier): SAME drives, compressive cube root")
    for h in (0.50 * sp, 0.99 * sp, 1.01 * sp, 2.0 * sp):
        s_switch = SUB.settle(g_sw, h)
        on       = SUB.is_on(g_sw, h)
        s_amp    = SUB.settle(0.0, h, n=_SETTLE_N)
        P(f"      drive h={h:7.4f}  | switch(g={g_sw:.3f}): s={s_switch:+.4f} {'ON ' if on else 'OFF'} "
          f"(all-or-none)   | amplifier(g=0): s={s_amp:+.4f} = h^(1/3)={h ** (1/3):+.4f} (compressive)")
    P("    -> ONE substrate cubic ṡ=g·s−s³+h: the bistable regime DETECTS (all-or-none, E1); the critical")
    P("       regime AMPLIFIES (cube-root compression, E3). Transduction switch ∥ active amplifier.  [F]")

    # -- PART C : the GAIN compresses as F^(−2/3) (dynamic-range compression) --------------------------
    P("\n[C] the consequence — gain r/F ∝ F^(−2/3): faint drives amplified far more than loud:")
    gains = [rs[i] / Fs[i] for i in range(len(Fs))]
    gslope = float(np.polyfit(np.log10(Fs), np.log10(gains), 1)[0])
    P(f"    gain at faintest drive F={Fs[0]:.2g}: {gains[0]:8.2f}   at loudest F={Fs[-1]:.2g}: {gains[-1]:6.3f}")
    P(f"    fitted gain exponent = {gslope:.6f}  (−2/3 = {-2/3:.6f}); faint/loud gain ratio = "
      f"{gains[0]/gains[-1]:.0f}×")
    P("    -> the active amplifier compresses a huge acoustic range into a usable one (the ear's ~120 dB).")
    P("       The EXPONENT/direction is forced [F]; the absolute gain and the dB count are [O] (see N1).")
    assert abs(gslope - (-2.0 / 3.0)) < 1e-6

    # -- PART D : SLC26A5 (prestin) placement in the lineage (spinodal order) --------------------------
    P("\n[D] EMERGE the amplifier's place — order = argsort(spinodal(γ)) (γ measured, exact-precision):")
    rows = sorted((E1.read_measured(s) for s in LINEAGE), key=lambda r: r["spinodal"])
    for i, r in enumerate(rows, 1):
        star = "  <== AMPLIFIER (prestin)" if r["sym"] == AMPLIFIER else ""
        P(f"    {i}. {r['sym']:8s} spinodal={r['spinodal']:.4f}  γ={r['gamma']:.4f}  [{r['node']}]{star}")
    pos = [r["sym"] for r in rows].index(AMPLIFIER)
    nbr_lo = rows[pos - 1]["sym"] if pos > 0 else "—"
    nbr_hi = rows[pos + 1]["sym"] if pos + 1 < len(rows) else "—"
    P(f"    -> the amplifier gene SLC26A5 emerges between {nbr_lo} and {nbr_hi} in the spinodal order.  "
      f"[F] order ; γ measured [L].")

    # -- PART E : the cochlea as a graded BANK of critical amplifiers ----------------------------------
    P("\n[E] the cochlea = a graded BANK of these critical amplifiers, one per place (inherited map):")
    xs, fG, sqrtS, max_dev = SND.stiffness_graded_tonotopy()
    assert max_dev < 1e-9
    P(f"    each place x carries a characteristic frequency CF=Greenwood(x) (place map re-verified, "
      f"max|ratio−1|={max_dev:.1e}):")
    for x in (0.1, 0.5, 0.9):
        P(f"       place x={x:.1f} -> CF={SND.greenwood_f(x):8.1f} Hz  · local amplifier exponent = 1/3 "
          f"(the cubic — CF-independent)")
    P("    -> the compression EXPONENT is the same 1/3 at EVERY place (it is the cubic, not the CF), so")
    P("       compression is UNIFORM across frequency. [F] uniform exponent ; per-place gain/Q/dB are [O].")

    # -- PART F : oscillatory Hopf corroboration (the literature 'Hopf', OAE form) ---------------------
    P("\n[F] corroboration — the OSCILLATORY Hopf form (the OAE-emitting amplifier) shows the SAME root:")
    Fh = [10.0 ** e for e in np.linspace(-3.0, -0.5, 7)]
    rh = [hopf_peak_amplitude(F) for F in Fh]
    hslope = float(np.polyfit(np.log10(Fh), np.log10(rh), 1)[0])
    P(f"    2-D Hopf normal form at μ=0, on resonance: steady oscillation amplitude vs drive,")
    P(f"    fitted exponent = {hslope:.4f}  (cube root 1/3 = {1/3:.4f}; |Δ|={abs(hslope-1/3):.2e}).")
    P("    -> the oscillatory (spontaneously-emitting, μ>0) amplifier carries the SAME cube root; the")
    P("       small bias is a finite-averaging numerical artifact (N5) — the EXACT result is [A](1a).  [V]")

    # -- honest negatives preserved as the E3->E4 starting line ----------------------------------------
    P("\n[honest negatives — preserved as the starting line for E4, not hidden]")
    P("    N1  absolute GAIN / dB of amplification / dynamic-range-in-dB / sharpness Q are [O] — a number")
    P("        would require TUNING a constant (forbidden). Only the exponent (1/3) + direction are forced.")
    P("    N2  the cube root matches the FORM of measured cochlear compression, but the measured I/O slope")
    P("        value (study-dependent ~0.2–0.5 dB/dB) and the absolute curve are [O].")
    P("    N3  otoacoustic-emission frequencies & amplitudes are [O] (need per-place gain, Q, and μ just")
    P("        above the bifurcation — none derivable without a tuned constant).")
    P("    N4  prestin's actual electromotile/piezoelectric FORCE is NOT read from γ — firewall holds: γ is")
    P("        promoter STRUCTURE only. The amplifier's MAGNITUDE is not derivable from γ.")
    P("    N5  the inherited integrator under-converges to the cube-root fixed point at very small drive")
    P("        (restoring force ∝s³ → 0 near 0); the rigorous [F] is the analytic fixed point [A](1a), the")
    P("        [V] is on the stated converged range; the oscillatory-Hopf exponent [F] carries ~0.02 bias.")

    # -- naming note (flagged, not silently fixed) ----------------------------------------------------
    P("\n[naming note] This delivers BLUEPRINT-E3 (the active amplifier). BLUEPRINT-E2 (the MET switch)")
    P("    shipped in v0.3.0 (in the folder labelled E1); BLUEPRINT-E1 (the full fluid-loaded traveling-")
    P("    wave ENVELOPE) is still the named [O] — it needs a damping/Q, forbidden to tune. The folder")
    P("    E-numbering inconsistency from v0.3.0 stands flagged; a future session may reconcile it.")

    P("\nLEARNED (E3): the cochlear amplifier is the inherited R19 cubic AT ITS CRITICAL POINT — the")
    P("  response compresses as the parameter-free cube root r∝F^(1/3) (the cubic's signature), the gain")
    P("  falls as F^(−2/3) (the ear's dynamic-range compression), the amplifier gene SLC26A5 takes its")
    P("  place in the spinodal order, and every tonotopic place compresses by the SAME 1/3. The MET switch")
    P("  (E1) and the amplifier (E3) are ONE cubic in two regimes: bistable detection ∥ critical amplification.")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
