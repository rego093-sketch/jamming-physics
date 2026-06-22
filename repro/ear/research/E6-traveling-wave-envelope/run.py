#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E6 :  the cochlear traveling-wave ENVELOPE.
                         Turns the seed's DEEPEST named [O] (BLUEPRINT-E1, "the [O] this seed exists to
                         close") from a black box into a CHARACTERISED open problem: the envelope FORM is
                         FORCED, and exactly ONE dimensionless scalar (the sharpness Q) remains [O], with
                         a proof that fixing it would require TUNING.

WHAT THIS BUILDS (BLUEPRINT.md E-plan, slot BLUEPRINT-E1 / WORK_HANDOVER open item 1).
  Every prior increment forced only the traveling-wave PEAK PLACE (E1: x*(f)=inverse-Greenwood) and
  deferred the FULL fluid-loaded dispersive ENVELOPE — peak width, the apical cutoff, phase/group delay,
  the active gain — as the named [O], because "a closed envelope would require tuning Q (forbidden)."
  E6 does NOT close that [O] by tuning. Instead it does what E5 did for the readout layer: it forces the
  STRUCTURE and keeps the MAGNITUDE [O]. It proves, composing only the FROZEN inherited foundation
  (the √-law Greenwood place map + the R19 cubic), that:

    (A) the envelope's PEAK sits EXACTLY at the characteristic frequency ω0(x)=CF(x) — i.e. on E1's
        forced inverse-Greenwood place — for ALL Q (the basilar-membrane VELOCITY resonance peaks at ω0
        independently of damping). The near-peak FORM is the universal single-pole resonance.
    (B) the envelope's ASYMMETRY is FORCED by the long-wave dispersion: the partition reactance changes
        sign at ω0, so a tone PROPAGATES basal of its characteristic place (stiffness-controlled, real k)
        and is EVANESCENT / CUT OFF apical of it (mass-controlled, imaginary k). The apical cutoff and its
        SIDE are forced and Q-free; only the cutoff SLOPE is [O]. (Lighthill 1981; de Boer; Zweig.)
    (C) the SHARPNESS is the single scalar Q: the −3 dB VELOCITY bandwidth is EXACTLY ω0/Q (analytic
        half-power roots, machine precision). Vary Q → the peak PLACE is invariant; the bandwidth scales
        as 1/Q. Location forced; width [O].
    (D) the active amplifier (the E3 bridge) is NEGATIVE DAMPING: Q_eff = Q0/(1−G) rises with the active
        gain fraction G, and at NET-ZERO linear damping (the R19 cubic's critical point g=0) the steady
        response is the inherited cube root settle(0,F) ≈ F^(1/3). DIRECTION forced; the gain magnitude G
        is the inherited E3 [O].
    (E) the GROUP DELAY of the velocity resonance PEAKS at the characteristic frequency, with magnitude
        2Q/ω0. Location forced (high-Q); the absolute delay in ms is [O].
    (F) THE META-RESULT (the point of E6): after non-dimensionalising (ω/ω0, place via Greenwood) the
        whole envelope is a ONE-PARAMETER family in Q. Every LOCATION (peak place, cutoff side, delay
        peak) is Q-INVARIANT and forced; every WIDTH / HEIGHT / SLOPE / ABSOLUTE DELAY scales with Q and
        is NOT fixed by ANY inherited constant (the √-law fixes ω0, the wave speed fixes propagation, and
        γ is promoter STRUCTURE only by the firewall — none of them is a damping). Therefore Q is the
        SINGLE IRREDUCIBLE [O]; any specific numeric envelope = a choice of Q = TUNING (forbidden). The
        named [O] is now CHARACTERISED, not closed.

THE PHYSICS (cited, not re-opened; built on the inherited wave theory).
  In the long-wavelength (1-D macromechanical) cochlear model the fluid-loaded partition behaves, near a
  place x, as a driven damped resonator of natural frequency ω0(x)=√(S(x)/m)=CF(x) — the INHERITED √-law
  Greenwood place (vp_sound_wave.py). The partition impedance per area Z(x,ω) = i(S−ω²m)/ω + r has a
  reactance (S−ω²m) that is stiffness-controlled (>0) below CF and mass-controlled (<0) above CF; the
  long-wave dispersion k² ∝ ω²/Z makes k REAL (propagating) where the reactance is positive and IMAGINARY
  (evanescent) where it is negative — the traveling wave is therefore cut off APICAL to its resonant
  place. The active cochlear amplifier (E3) supplies negative damping near a Hopf/critical point
  (Eguíluz–Ospeck–Choe–Hudspeth–Magnasco 2000; Camalet–Duke–Jülicher–Prost 2000; Hudspeth 2008); at
  criticality the response is the inherited cubic's cube root. The whole envelope FORM is fixed by these;
  only the damping/quality factor Q (passive r and the active gain) sets the absolute sharpness, and it is
  not derivable without a measured/fitted constant.

HOW IT RELATES TO THE FOUNDATION (no-regression — note: NO inherited byte changes in E6).
  EXTENDS the inherited foundation by IMPORTING it. Like E5, E6 fetches NO new gene and folds nothing
  into the cache/atlas — it touches NOT ONE inherited byte and triggers NO re-freeze (every frozen hash
  stays valid as recorded at seed time). It consumes the INHERITED `vp_sound_wave.py` (the Greenwood
  place map ω0(x)=CF(x), re-verified to machine precision) and the INHERITED `vp_substrate.py` cubic
  directly (`settle` at g=0 — the SAME cube root E3 reads), plus E1's `inv_greenwood` (the forced peak
  place) and `read_measured` (the amplifier gene SLC26A5 recomputes from the frozen cache and equals the
  atlas bit-for-bit). The wave theory and the cubic are consumed, never re-opened.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the velocity-resonance PEAK at ω0 for all Q (analytic + verified) ; the near-peak single-pole
            FORM ; the reactance-sign APICAL CUTOFF (propagating basal / evanescent apical of CF) and its
            Q-free SIDE ; the asymmetry SIGN (apical steeper than basal, robust to the [O] decay scale) ;
            the EXACT −3 dB velocity bandwidth = ω0/Q (machine precision) ; the active=negative-damping
            relation Q_eff=Q0/(1−G) and the criticality → cube-root bridge to E3 ; the group-delay PEAK at
            ω0 with magnitude 2Q/ω0 ; and THE META-RESULT — the Q-invariance of all locations vs the
            Q-scaling of all magnitudes (the proof that Q is the single irreducible degree of freedom).
  [L]      : the amplifier gene γ (NCBI-measured, cached) ; the Greenwood A/a/k place-map calibration.
  [O]      : the absolute SHARPNESS Q / Q10dB / bandwidth in Hz ; the apical cutoff SLOPE (dB/octave) ;
            the active gain magnitude G / proximity μ to the bifurcation (the inherited E3 [O]) ; the
            absolute group delay (ms), phase (cycles), and traveling-wave speed (need the fluid density ρ,
            duct height H, and BM mass — Lighthill/Zweig hydrodynamics) ; the full 2-D/3-D short-wave
            fluid solution and the "second filter" ; two-tone suppression / distortion products ; the felt
            pitch/timbre percept (→ mind volume). Each names its obstacle below; none closes without
            TUNING a constant.

FIREWALL. γ reads promoter STRUCTURE only — it is NOT the partition damping, NOT the quality factor Q,
NOT the active force, NOT a gain, a delay, or a clinical effect (the amplifier gene is reproduced offline
ONLY to show the cascade gene still recomputes and NO byte moved; its γ is never used as Q).
No disease claim here (E6 is macromechanics; it neighbours the E4 deafness goal but states none).
The percept of pitch/timbre is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E6-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate  as SUB                               # the R19 cubic (settle at g=0 = the E3 cube root)
import vp_sound_wave as SND                               # √-law Greenwood place map ω0(x)=CF(x)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (every increment ships a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's inv_greenwood (the forced peak place) + read_measured (cache==atlas, A4⊥) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

AMPLIFIER_GENE = "SLC26A5"                                # prestin — the OHC active-amplifier gene (γ measured)

# the converged drive range for the criticality cube-root [V] (identical convention to E3/E5; E3 N5)
_F_LO_EXP, _F_HI_EXP, _F_N, _SETTLE_N = -1.0, 2.0, 10, 20000
# fixed, deterministic frequency grid for the resonance peak/argmax demonstrations
_W_GRID = np.linspace(0.2, 3.0, 400001)
_W_STEP = float(_W_GRID[1] - _W_GRID[0])                  # ~7e-6 ; peak must land within one grid step of ω0


def drive_grid():
    return [10.0 ** e for e in np.linspace(_F_LO_EXP, _F_HI_EXP, _F_N)]


# ============================================================================================
#  the cochlear partition as a driven damped resonator — BM VELOCITY response (long-wave model)
#    |V(ω)|² ∝ ω² / [ (ω0²−ω²)² + (ω0 ω / Q)² ]      ω0 = CF(x) is the INHERITED Greenwood place
#    The FORM is the claim; the value of Q is [O].
# ============================================================================================
def vel_mag2(w, w0, Q):
    """Squared BM-velocity magnitude of the driven damped partition resonator (single-pole FORM)."""
    return (w * w) / ((w0 * w0 - w * w) ** 2 + (w0 * w / Q) ** 2)


def half_power_bandwidth(w0, Q):
    """EXACT −3 dB (half-power) bandwidth of the VELOCITY resonance, from the analytic half-power roots
    of |V|² = 1/((ω0²/ω − ω)² + (ω0/Q)²): the two positive roots of ω² ∓ (ω0/Q)ω − ω0² = 0 differ by
    EXACTLY ω0/Q. Returns (w_lo, w_hi, bandwidth). No tuned constant; closed form."""
    a = w0 / Q
    disc = math.sqrt(a * a + 4.0 * w0 * w0)
    w_lo = (-a + disc) / 2.0
    w_hi = (+a + disc) / 2.0
    return w_lo, w_hi, (w_hi - w_lo)


def reactance(w, w0):
    """Dimensionless partition reactance χ = 1 − (ω/ω0)² = (S−ω²m)/S. χ>0 stiffness-controlled
    (real k, the wave PROPAGATES); χ<0 mass-controlled (imaginary k, the wave is EVANESCENT / cut off).
    Sign change at ω=ω0 is the forced apical cutoff. Q- and magnitude-prefactor-independent."""
    return 1.0 - (w / w0) ** 2


def excitation_envelope(f, Q, kappa, npts=20001):
    """Excitation pattern E(x; f) of a fixed tone f vs place x∈[0,1] (apex→base), SHAPE only.
    amplitude = √(velocity-resonance at the local CF(x)) × evanescent decay where the reactance is
    mass-controlled (apical of the characteristic place). `kappa` bundles the long-wave dispersion's
    [O] magnitude prefactor (∝√(ρ/(H·m))) — it sets the cutoff STEEPNESS only; the asymmetry SIGN
    (apical steeper than basal) is independent of it (asserted over a range of kappa in PART B)."""
    xs = np.linspace(0.0, 1.0, npts)
    E = np.empty_like(xs)
    for j, x in enumerate(xs):
        CF = SND.greenwood_f(max(x, 1e-6))               # INHERITED √-law place: ω0(x)=CF(x)
        res = vel_mag2(f, CF, Q)
        chi = reactance(f, CF)
        decay = 1.0 if chi >= 0.0 else math.exp(kappa * chi)   # χ<0 (apical) → evanescent decay <1
        E[j] = math.sqrt(res) * decay
    return xs, E / E.max()


def edge_widths(xs, E, thr=0.1):
    """Basal-side and apical-side widths of an excitation envelope at a relative threshold thr.
    Basal = toward the base (x>peak); apical = toward the apex (x<peak)."""
    ip = int(np.argmax(E)); xp = xs[ip]
    basal = xs[(xs >= xp) & (E >= thr)]
    apical = xs[(xs <= xp) & (E >= thr)]
    return xp, (basal.max() - xp), (xp - apical.min())


def phase_lag(w, w0, Q):
    """Phase LAG of the velocity response = phase of the denominator (ω0²−ω²+iω0ω/Q): rises
    monotonically 0 → π/2 (at ω0) → π. Group delay τ = +dΦ/dω peaks where the phase turns fastest."""
    return math.atan2(w0 * w / Q, w0 * w0 - w * w)


# =====================================================================================================
def run(P):
    P("=" * 96)
    P("E6 — the cochlear traveling-wave ENVELOPE  ·  FORM forced, the sharpness Q the single [O]")
    P("     a wave -> a spatial code (place) -> an R19 switch ; here the ENVELOPE on that place map")
    P("     turning the seed's DEEPEST [O] (BLUEPRINT-E1) from a black box into a CHARACTERISED one")
    P("=" * 96)

    # -- PART 0 : the amplifier gene reproduces offline; NO inherited byte changed ---------------------
    P("\n[0] the active-amplifier gene reproduces offline (γ LEVEL + A4 SHAPE, from the frozen cache):")
    amp = E1.read_measured(AMPLIFIER_GENE)               # asserts cache==atlas & A4 = signal−γ for SLC26A5
    P(f"    [PASS] {AMPLIFIER_GENE:8s} γ(level)={amp['gamma']:.4f}  A4 amp={amp['shape_amplitude']:.5f} "
      f"range={amp['shape_range']:.5f}  node={amp['node']}  (prestin / OHC active amplifier)")
    P("    -> SLC26A5 γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9). No gene")
    P("       was fetched and NO inherited byte changed in E6 (no re-freeze — frozen hashes stay valid). [V]")
    P("    FIREWALL: γ is promoter STRUCTURE only — it is NOT the damping, NOT Q, NOT the active force.")

    # -- PART A : the PEAK is forced — velocity resonance peaks EXACTLY at ω0=CF(x), for ALL Q ---------
    P("\n[A] the keystone — the envelope PEAK sits at the characteristic frequency ω0=CF(x), for ALL Q:")
    P("    model the partition as a driven damped resonator; the BM-VELOCITY peak is at ω0 independently")
    P("    of the damping (analytic: d/dω[ω²/((ω0²−ω²)²+(ω0ω/Q)²)]=0 ⇒ ω=ω0 exactly). Verify on a grid:")
    w0 = 1.0
    maxdev_peak = 0.0
    for Q in (0.8, 1.0, 3.0, 10.0, 30.0, 100.0):
        vals = vel_mag2(_W_GRID, w0, Q)
        w_peak = float(_W_GRID[int(np.argmax(vals))])
        maxdev_peak = max(maxdev_peak, abs(w_peak - w0))
        if Q in (0.8, 10.0, 100.0):
            P(f"       Q={Q:6.1f}  argmax velocity at ω={w_peak:.6f}   (ω0=1.000000, within one grid step)")
    P(f"    -> velocity peak == ω0 for every Q (max|ω_peak−ω0|={maxdev_peak:.1e} ≤ grid step {_W_STEP:.1e}).")
    assert maxdev_peak <= 2.0 * _W_STEP
    P("    and ω0(x)=CF(x) is the INHERITED Greenwood place, so the envelope peak IS E1's forced place:")
    for f in (500.0, 2000.0, 8000.0):
        xs, E = excitation_envelope(f, Q=20.0, kappa=8.0)
        xp = xs[int(np.argmax(E))]; xstar = E1.inv_greenwood(f)
        P(f"       f={f:6.0f} Hz  envelope-peak x={xp:.4f}  ==  E1 inverse-Greenwood x*={xstar:.4f}  "
          f"(|Δ|={abs(xp - xstar):.4f})")
    P("    -> the near-peak FORM is the universal single-pole resonance; its LOCATION is forced [F]/[V].")

    # -- PART B : the ASYMMETRY is forced by dispersion — apical cutoff at the characteristic place -----
    P("\n[B] the asymmetry is FORCED — the partition reactance flips sign at ω0 (apical cutoff):")
    P("    χ(x;f) = 1 − (f/CF(x))² : χ>0 stiffness-controlled (real k, PROPAGATES) ; χ<0 mass-controlled")
    P("    (imaginary k, EVANESCENT). A tone propagates basal of its place x* and is cut off apical of it:")
    for f in (500.0, 2000.0, 8000.0):
        xstar = E1.inv_greenwood(f)
        xb = min(1.0, xstar + 0.12); xa = max(0.0, xstar - 0.12)
        CFb, CFa = SND.greenwood_f(xb), SND.greenwood_f(xa)
        chib, chia = reactance(f, CFb), reactance(f, CFa)
        assert chib > 0.0 and chia < 0.0                 # propagating basal, cut off apical — forced
        P(f"       f={f:6.0f}Hz x*={xstar:.4f} | basal x={xb:.3f}(CF={CFb:6.0f}) χ={chib:+.3f}[propagate]"
          f" | apical x={xa:.3f}(CF={CFa:6.0f}) χ={chia:+.3f}[cut off]")
    P("    the resulting excitation envelope is ASYMMETRIC — gradual basal tail, steep apical cutoff —")
    P("    and the SIGN is robust to the [O] cutoff-steepness scale κ (κ sets the slope, not the side):")
    f = 2000.0
    for kappa in (2.0, 6.0, 12.0, 25.0):
        xs, E = excitation_envelope(f, Q=20.0, kappa=kappa)
        xp, wb, wa = edge_widths(xs, E)
        assert wa < wb                                   # apical width < basal width — steep apical side
        P(f"       κ={kappa:5.1f}  basal 10%-width={wb:.4f}  apical 10%-width={wa:.4f}  apical<basal={wa < wb}")
    P("    -> the apical cutoff (and its SIDE) is FORCED by the reactance sign, Q- and prefactor-free [F]/[V];")
    P("       the cutoff SLOPE in dB/octave needs Q + the fluid mass-loading prefactor → [O] (see N2).")

    # -- PART C : the SHARPNESS is the single scalar Q — EXACT bandwidth = ω0/Q ------------------------
    P("\n[C] the sharpness is the single scalar Q — the −3 dB VELOCITY bandwidth is EXACTLY ω0/Q:")
    P("    half-power roots of |V|²=1/((ω0²/ω−ω)²+(ω0/Q)²) ⇒ ω²∓(ω0/Q)ω−ω0²=0, difference = ω0/Q exactly:")
    maxdev_bw = 0.0
    for Q in (3.0, 10.0, 30.0, 100.0):
        w_lo, w_hi, bw = half_power_bandwidth(w0, Q)
        maxdev_bw = max(maxdev_bw, abs(bw - w0 / Q))
        P(f"       Q={Q:6.1f}  ω_lo={w_lo:.6f} ω_hi={w_hi:.6f}  BW={bw:.12f}  ω0/Q={w0 / Q:.12f}  "
          f"|Δ|={abs(bw - w0 / Q):.1e}")
    P(f"    -> BW = ω0/Q to machine precision (max|Δ|={maxdev_bw:.1e}). The PEAK PLACE is Q-invariant")
    P("       (PART A); only the WIDTH carries Q. So sharpness is EXACTLY the one scalar Q.  [F]/[V]")
    assert maxdev_bw < 1e-12

    # -- PART D : the active amplifier = NEGATIVE DAMPING; criticality -> the inherited cube root -------
    P("\n[D] the active amplifier (the E3 bridge) is NEGATIVE DAMPING: Q_eff = Q0/(1−G) (G = gain fraction):")
    Q0 = 5.0
    last = 0.0
    for G in (0.0, 0.5, 0.8, 0.95):
        Qeff = Q0 / (1.0 - G)
        assert Qeff >= last - 1e-12; last = Qeff
        P(f"       gain fraction G={G:4.2f}  ->  Q_eff = Q0/(1−G) = {Qeff:8.3f}   (sharper, taller)")
    P("    as G→1 the net linear damping → 0 and the linear gain diverges — capped by the cubic. AT the")
    P("    critical point (the R19 cubic g=0) the steady response is the INHERITED cube root settle(0,F):")
    Fs = drive_grid()
    rs = [SUB.settle(0.0, F, n=_SETTLE_N, dt=0.01) for F in Fs]
    slope = float(np.polyfit(np.log10(Fs), np.log10(rs), 1)[0])
    P(f"       fitted exponent of settle(0,F) over F∈[{Fs[0]:.2g},{Fs[-1]:.2g}] = {slope:.6f}  "
      f"(cube root 1/3 = {1/3:.6f}; |Δ|={abs(slope - 1/3):.1e})")
    assert abs(slope - 1.0 / 3.0) < 1e-6
    P("    -> the active process SHARPENS the envelope (raises Q_eff), RAISES the peak gain, and at")
    P("       criticality imposes the E3 compressive cube root. The DIRECTION is forced [F]/[V]; the gain")
    P("       MAGNITUDE G / proximity μ to the bifurcation is the inherited E3 [O] (see N3).")

    # -- PART E : the GROUP DELAY peaks at the characteristic frequency --------------------------------
    P("\n[E] the phase — the GROUP DELAY of the velocity resonance PEAKS at the characteristic frequency:")
    P("    phase lag Φ(ω)=atan2(ω0ω/Q, ω0²−ω²) rises 0→π/2(at ω0)→π; τ=+dΦ/dω peaks at ω0, magnitude 2Q/ω0:")
    ws = np.linspace(0.3, 2.5, 200001); dw = ws[1] - ws[0]
    for Q in (5.0, 20.0, 80.0):
        Phi = np.unwrap(np.array([phase_lag(w, w0, Q) for w in ws]))
        tau = np.gradient(Phi, dw)
        ip = int(np.argmax(tau)); wp = float(ws[ip])
        P(f"       Q={Q:5.1f}  group-delay peak at ω={wp:.5f} (→ω0=1 as Q grows)  τ_max={tau[ip]:.3f}  "
          f"2Q/ω0={2*Q/w0:.3f}")
    # at high Q the peak location -> ω0; assert the high-Q case + the exact magnitude scaling
    Phi = np.unwrap(np.array([phase_lag(w, w0, 80.0) for w in ws])); tau = np.gradient(Phi, dw)
    wp_hi = float(ws[int(np.argmax(tau))])
    assert abs(wp_hi - w0) < 1e-3 and abs(tau.max() - 2 * 80.0 / w0) < 0.5
    P("    -> the cochlear group delay is greatest AT the characteristic place (location forced, high-Q);")
    P("       the peak magnitude 2Q/ω0 scales with Q, so the absolute delay (ms) is [O] (see N4).  [F]/[V]")

    # -- PART F : THE META-RESULT — Q is the single irreducible [O] (the proof) ------------------------
    P("\n[F] the point of E6 — the envelope is a ONE-PARAMETER family in Q; Q is the SINGLE irreducible [O]:")
    P("    vary Q ×10 and watch LOCATIONS stay fixed while WIDTHS scale — there is exactly one free knob:")
    for Q in (10.0, 100.0):
        vals = vel_mag2(_W_GRID, w0, Q); wpk = float(_W_GRID[int(np.argmax(vals))])
        _, _, bw = half_power_bandwidth(w0, Q)
        P(f"       Q={Q:6.1f}  peak place ω={wpk:.6f} (INVARIANT)   −3dB BW={bw:.5f} (∝1/Q, SCALES)")
    P("    LOCATIONS forced & Q-invariant : peak place (A) · apical-cutoff side (B) · group-delay peak (E).")
    P("    MAGNITUDES that scale with Q   : peak width/Q10dB (C) · peak gain/height (D) · cutoff slope (B)")
    P("                                     · absolute group delay (E).")
    P("    NONE of those magnitudes is fixed by an inherited constant: the √-law fixes ω0 (the place), the")
    P("    wave speed √(B/ρ) fixes propagation, and γ is promoter STRUCTURE only (firewall) — NOT a damping.")
    P("    The only thing that sets Q is the partition damping r and the active gain, neither derivable")
    P("    without a measured/fitted number. ⇒ a closed numeric envelope = a CHOICE of Q = TUNING (forbidden).")
    P("    So E6 does NOT close the [O]; it CHARACTERISES it: FORM forced, exactly ONE scalar Q open.  [F]")

    # -- honest negatives preserved -------------------------------------------------------------------
    P("\n[honest negatives — preserved, not hidden]")
    P("    N1  the absolute SHARPNESS is [O]: Q / Q10dB / the −3dB bandwidth in Hz / the peak gain in dB.")
    P("        Only the FORM (single-pole resonance), the EXACT bandwidth LAW (=ω0/Q), and the peak PLACE")
    P("        are forced. A number for Q would require TUNING — forbidden.")
    P("    N2  the apical cutoff SLOPE (dB/octave) is [O] — it needs Q plus the long-wave fluid mass-")
    P("        loading prefactor (∝√(ρ/(H·m))). Only the cutoff's EXISTENCE and SIDE (apical) are forced")
    P("        (the reactance sign), robust to the decay scale κ.")
    P("    N3  the active gain MAGNITUDE (the fraction G, equivalently the proximity μ to the Hopf/critical")
    P("        point) is the inherited E3 [O]. E6 forces only the DIRECTION (active → higher Q_eff, higher")
    P("        gain, → cube-root compression at criticality), never the amount of gain.")
    P("    N4  the ABSOLUTE group delay (ms), the phase in cycles, and the traveling-wave speed are [O] —")
    P("        they need ρ, the duct height H, and the BM mass (Lighthill/Zweig hydrodynamics). Only that")
    P("        the delay PEAKS at CF (location) and that phase accrues monotonically through CF is forced.")
    P("    N5  the model is the LONG-WAVE (1-D, WKB) approximation. The full 2-D/3-D fluid problem, the")
    P("        short-wave region right at the peak, the 'second filter', and the active feedback's spatial")
    P("        extent are NOT captured — they are the deeper [O] hydrodynamics. The forced results here are")
    P("        the near-peak resonance FORM, the reactance-sign cutoff, and the Q-invariances — not the")
    P("        full waveform.")
    P("    N6  two-tone suppression, distortion products, and combination tones (the active nonlinearity's")
    P("        products) are downstream of the cubic but are NOT derived in this envelope — [O].")
    P("    N7  the felt percept of pitch and timbre is the MIND volume's (firewall); E6 moves only the")
    P("        physical/mechanical envelope, not the experience.")

    # -- naming note (the E-numbering, partially addressed; literal folder reconciliation still flagged) -
    P("\n[naming note] E6 delivers BLUEPRINT-E1 CONTENT (the traveling-wave envelope — the seed's named [O])")
    P("    in the unambiguous folder research/E6-traveling-wave-envelope/. To preserve every frozen hash and")
    P("    the no-omission set, the EXISTING folders are NOT renamed; the v0.3.0 label slip (BLUEPRINT-E2 in")
    P("    the folder labelled E1) therefore still stands flagged as a separate bookkeeping item. What E6")
    P("    changes is the SUBSTANCE: BLUEPRINT-E1's envelope now has a home and a characterised [O], rather")
    P("    than being only a deferred target.")

    P("\nLEARNED (E6): the cochlear traveling-wave ENVELOPE — the seed's deepest [O] — is now CHARACTERISED")
    P("  without tuning. Built on the FROZEN √-law place map and the R19 cubic: the VELOCITY peak sits at")
    P("  the characteristic frequency ω0=CF(x)=E1's place for ALL Q (single-pole FORM); the partition")
    P("  reactance flips sign at ω0, forcing a propagating basal tail and an evanescent APICAL CUTOFF (the")
    P("  asymmetry SIGN, κ-robust); the −3 dB velocity bandwidth is EXACTLY ω0/Q; the active amplifier is")
    P("  negative damping (Q_eff=Q0/(1−G)) whose critical point is the E3 cube root; the group delay peaks")
    P("  at CF with magnitude 2Q/ω0. The whole envelope is a ONE-PARAMETER family in Q: every LOCATION is")
    P("  forced and Q-invariant, every MAGNITUDE scales with Q and is fixed by no inherited constant — so")
    P("  Q is the SINGLE irreducible [O], and a closed numeric envelope would require TUNING it (forbidden).")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
