#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E10-light-dark-adaptation/run.py — INCREMENT E10: light/dark adaptation as GAIN CONTROL.

  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
  │ SCOPE — THEORETICAL, NON-CLINICAL (read first; binding, FIREWALL.md / BLUEPRINT.md).           │
  │ E10 studies a NORMAL physiological mechanism — how the eye keeps working across a huge range of │
  │ background light — as a question in dynamical-systems theory: the SAME frozen R19 switch read   │
  │ on its steady-state (light-adapted) branch. It is not a disease chapter; it diagnoses nothing,  │
  │ designs no molecule, and states no clinical quantity. The felt brightness percept is deferred   │
  │ to the mind volume.                                                                             │
  └──────────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E10 DOES (BLUEPRINT "beyond the ladder spine"; research/E10-light-dark-adaptation/START_HERE.md).
  Four things, built ONLY on the frozen inherited substrate and the already-measured atlas — it adds
  NO new γ, fetches nothing, and re-derives nothing. The whole result is ONE fact about the cubic:

    The steady state of the FROZEN field  ds/dt = γ·s − s³ + h  (E2's switch, here on its upper/ON
    branch) is the real root of  s³ − γ·s − h = 0.  For a large background drive h the cubic term
    dominates, so  s*(h) → h^(1/3)  — a COMPRESSIVE (saturating) response. Everything below follows.

    PART A — THE RESPONSE COMPRESSES (the saturating nonlinearity is intrinsic).
      Settle the ON-branch steady state s*(h) over a background sweep spanning many decades. s* grows
      but SATURATES onto the cube root: s*/h^(1/3) → 1. A ~5-decade rise in background produces only a
      ~1.5-decade rise in response; deep in the saturated branch the log-compression → exactly the
      cubic order n=3. This is how one switch spans the eye's enormous intensity range without pinning.
      The steady state is the zero of the FROZEN sdot (residual |γ·s−s³+h| ≈ 0, machine-checked). [F]/[V]

    PART B — GAIN CONTROL: the incremental gain FALLS as the background rises (light adaptation).
      The incremental gain is ds*/dh = 1/(3s*²−γ) (implicit differentiation of the frozen field;
      3s²−γ = −∂sdot/∂s). It falls monotonically with background — high in dim light, low in bright
      light — so a bright surround automatically turns the switch DOWN. No new machinery: gain control
      is a property of the cubic's own steady-state curve. [F]/[V]

    PART C — WEBER / CONTRAST CONSTANCY: fractional sensitivity is constant = 1/n = 1/3 (forced).
      The CONTRAST gain (response to a FRACTIONAL change) is (h/s*)·ds*/dh = (h/s*)/(3s*²−γ). On the
      saturated branch s*→h^(1/3) so this → (h^(2/3))/(3h^(2/3)) = **1/3 EXACTLY = 1/n** (n=3, the cubic
      order). In the pure-cube limit (γ-term off) it is 0.333333 for ANY h; the real γ-carrying field
      converges to it. This is a Weber-Fechner-like law — equal fractional steps feel equal — FORCED by
      the cube, not fitted, and INDEPENDENT of γ (same limit for two different genes). [F]

    PART D — TWO REGIMES, AND WHERE γ AND τ SIT (the ladder ties together).
      Dim (operating point near the fold h*(γ)) = high incremental gain + the single-photon FLIP (E2,
      the detection threshold). Bright (driven deep into the cube root) = low gain, response compressed
      against saturation. Adaptation is the operating point SLIDING from the fold into the cube-root
      tail; the gain falls automatically while the contrast gain stays ~1/3. γ is READ-ONLY: it sets
      WHERE the fold (the dark sensitivity offset) sits, NOT the compression law (the cubic order,
      γ-independent) — exactly as in E7 (band is τ, not γ) and E8 (γ is an offset). The TIME COURSE of
      re-sensitisation in the dark is the FROZEN Neuron's recovery τ_s (E7/E8), READ-ONLY; the absolute
      seconds are the inherited [O]. The felt brightness percept → mind volume. [F] structure; [O] scale.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E10 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing and adds no γ.
    - the R19 field ds/dt=γ·s−s³+h, spinodal h*(γ) ← inherited/vp_substrate.py (frozen, no-regression)
    - the recovery time-constant τ_s, β        ← inherited/vp_substrate.py Neuron (frozen, read-only)
    - γ (LEVEL) of RHO / CNGB3 (read-only)      ← inherited/organ_gamma.json   (MEASURED [L]; re-proved
                                                  by verify_seed [3] offline bit-for-bit [V])
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never a channel voltage,
  transduction gain, photocurrent, potency, dose, or clinical effect (FIREWALL #1). The background drive
  h and the operating points are INPUTS that sweep the field, never fitted targets. The felt percept
  belongs to the mind volume (FIREWALL #4). Nothing here diagnoses, treats, or prescribes.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib + the frozen substrate's scalar helpers (pure math, no RNG). Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E10-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, Neuron           # FROZEN: the R19 field + the recovery τ
ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# anchor gene: RHO (rhodopsin) — the rod pigment, the dim-light (scotopic) photoreceptor. READ-ONLY.
G_RHO   = ATLAS["RHO"]["gamma"]      # 1.4719 (measured, frozen)
G_CNGB3 = ATLAS["CNGB3"]["gamma"]    # 1.2425 (measured, frozen) — used only to show γ-independence

N_ITERS = 200                        # fixed-count Newton ⇒ deterministic (no RNG, no tolerance branch)


def s_star(g, h):
    """The ON-branch steady state of the FROZEN field γ·s−s³+h = 0, i.e. the real root of
    s³−γ·s−h = 0 above the fold. Newton from a guess above √γ and above the cube root; the field's
    own sdot is used for the residual check, so this is the inherited switch's steady state, not a
    re-derivation. (settle() is the inherited integrator for the NEAR-FOLD regime; for a large
    background drive it is stiff, so the steady state is taken as the field's exact zero here.)"""
    s = max(math.sqrt(g) if g > 0 else 0.0, h ** (1.0 / 3.0)) + 1.0
    for _ in range(N_ITERS):
        f  = s ** 3 - g * s - h
        fp = 3.0 * s * s - g
        s  = s - f / fp
    return s


def run(P):
    P("=" * 80)
    P("E10 — LIGHT/DARK ADAPTATION   (gain control = the R19 switch on its saturating ON branch)")
    P("=" * 80)
    P("SCOPE: theoretical, NON-CLINICAL — a NORMAL mechanism (not a disease chapter).")
    P("consumes (frozen): vp_substrate.sdot/spinodal (the R19 field) · Neuron τ_s,β · organ_gamma.json γ")
    P("re-derives: nothing; adds no γ. γ measured, never fitted; γ = promoter STRUCTURE only (firewall).")
    P(f"anchor gene RHO (rod pigment): γ = {G_RHO:.4f}  →  fold h*(γ) = spinodal(γ) = {spinodal(G_RHO):.5f}")
    P("the steady state of γ·s − s³ + h = 0 (E2's switch, ON branch) is the real root of s³ − γ·s − h = 0;")
    P("for a large background drive h the cubic dominates ⇒ s*(h) → h^(1/3): a COMPRESSIVE response.")

    SWEEP = [1, 10, 100, 1000, 10000, 100000]      # background drive h, spanning 5 decades

    # ----------------------------------------------------------------------------------------
    # PART A — the response compresses onto the cube root (the saturating nonlinearity)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — the ON-branch steady state s*(h) SATURATES onto the cube root (s*/h^(1/3) → 1)")
    P("-" * 80)
    P("    %-10s %-12s %-12s %-12s %-15s %-10s" %
      ("h (bg)", "s*", "h^(1/3)", "s*/h^1/3", "gain=1/(3s^2-g)", "contrast"))
    rows = []
    max_resid = 0.0
    for h in SWEEP:
        s    = s_star(G_RHO, float(h))
        resid = abs(sdot(s, G_RHO, float(h)))           # FROZEN-field residual: this IS a steady state
        max_resid = max(max_resid, resid)
        cube = float(h) ** (1.0 / 3.0)
        gain = 1.0 / (3.0 * s * s - G_RHO)
        contrast = (float(h) / s) * gain
        rows.append((h, s, cube, s / cube, gain, contrast))
        P("    %-10d %-12.6f %-12.6f %-12.6f %-15.6e %-10.6f" % (h, s, cube, s / cube, gain, contrast))
    sat_mono = all(rows[i + 1][3] <= rows[i][3] + 1e-12 for i in range(len(rows) - 1))  # ratio → 1 from above
    P(f"\n    s*/h^(1/3) decreases monotonically toward 1 (saturation onto the cube root): {sat_mono}")
    assert sat_mono and abs(rows[-1][3] - 1.0) < 1e-3, "the ON-branch steady state must saturate onto h^(1/3)"
    assert max_resid < 1e-9, "each s* must be a true zero of the FROZEN field (steady state, not approximate)"
    P(f"    every s* is a true zero of the FROZEN field (max |γ·s−s³+h| = {max_resid:.1e}). [V]")

    # dynamic-range compression: a huge background range fits into a bounded response range
    s_lo, s_hi = rows[0][1], rows[-1][1]
    dec_in  = math.log10(SWEEP[-1] / SWEEP[0])
    dec_out = math.log10(s_hi / s_lo)
    P(f"\n    operating sweep  {SWEEP[0]} → {SWEEP[-1]}: background = {dec_in:.6f} decades, "
      f"response = {dec_out:.6f} decades")
    P(f"    → compression = {dec_in/dec_out:.6f} (a 5-decade background fits a ~1.5-decade response)")
    # asymptotic compression deep in the saturated branch → exactly n = 3
    sa, sb = s_star(G_RHO, 100.0), s_star(G_RHO, 1.0e8)
    dec_in2, dec_out2 = 6.000000, math.log10(sb / sa)
    P(f"    saturated sweep  100 → 100000000: background = {dec_in2:.6f} decades, "
      f"response = {dec_out2:.6f} decades")
    P(f"    → compression = {dec_in2/dec_out2:.6f} → the cubic order n=3 (pure cube-root log-compression). [F]")
    assert abs(dec_in2 / dec_out2 - 3.0) < 0.05, "deep saturation must log-compress by the cubic order n=3"

    # ----------------------------------------------------------------------------------------
    # PART B — gain control: incremental gain falls as the background rises (light adaptation)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — gain control: the incremental gain ds*/dh = 1/(3s*²−γ) FALLS with the background")
    P("-" * 80)
    gains = [r[4] for r in rows]
    gain_mono = all(gains[i + 1] < gains[i] for i in range(len(gains) - 1))
    P(f"    gain at dim background   (h={SWEEP[0]}):    {gains[0]:.6e}")
    P(f"    gain at bright background (h={SWEEP[-1]}): {gains[-1]:.6e}")
    P(f"    gain falls monotonically dim → bright: {gain_mono}")
    P(f"    dim/bright gain ratio = {gains[0]/gains[-1]:.1f}  (the bright surround turns the switch DOWN)")
    assert gain_mono, "the incremental gain must fall monotonically as the background rises (light adaptation)"
    # gain ∝ h^(-2/3): gain·h^(2/3) is ~constant on the saturated branch
    g_times = [rows[i][4] * (float(SWEEP[i]) ** (2.0 / 3.0)) for i in range(len(SWEEP))]
    P(f"    gain·h^(2/3) (≈ const ⇒ gain ∝ h^(−2/3)): "
      f"{g_times[2]:.6f} (h=100) … {g_times[-1]:.6f} (h={SWEEP[-1]}) → 1/3")
    P("    → a saturating response gives AUTOMATIC gain control: no separate machinery is invoked. [F]")

    # ----------------------------------------------------------------------------------------
    # PART C — Weber/contrast: fractional sensitivity is constant = 1/n = 1/3 (forced, γ-independent)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — contrast gain (response to a FRACTIONAL change) → 1/n = 1/3 EXACTLY (Weber-like)")
    P("-" * 80)
    contrasts = [r[5] for r in rows]
    P("    contrast gain (h/s*)·ds*/dh along the sweep:")
    P("        " + " → ".join("%.6f" % c for c in contrasts))
    con_mono = all(contrasts[i + 1] >= contrasts[i] - 1e-12 for i in range(len(contrasts) - 1))
    P(f"    rises monotonically toward a constant: {con_mono}")
    # the EXACT limit: pure-cube field (γ-term off) ⇒ s*=h^(1/3) ⇒ contrast = 1/3 for ANY h
    P("\n    pure-cube limit (γ-term off ⇒ s*=h^(1/3) exactly): contrast = (h/s*)/(3s*²) for any h —")
    for h in (8.0, 1000.0, 1.0e9):
        s = h ** (1.0 / 3.0)
        c = (h / s) * (1.0 / (3.0 * s * s))
        P(f"        h={h:<12g} s*={s:<12.6f} contrast = {c:.6f}")
    one_over_n = 1.0 / 3.0
    P(f"    → the cube-root response makes the contrast gain EXACTLY 1/n = {one_over_n:.6f}  (n=3, the cubic). [F]")
    pure_cube_contrast = (1000.0 / (1000.0 ** (1.0 / 3.0))) * (1.0 / (3.0 * (1000.0 ** (1.0 / 3.0)) ** 2))
    assert abs(pure_cube_contrast - one_over_n) < 1e-12, "the pure-cube contrast gain must equal 1/n exactly"
    # γ-independence: the same limit for a DIFFERENT gene's γ ⇒ the compression is the cubic, not γ
    P("\n    γ-INDEPENDENCE (the compression is the cubic ORDER, not the threshold γ):")
    for g, nm in ((G_RHO, "RHO  "), (G_CNGB3, "CNGB3")):
        s = s_star(g, 1.0e6)
        c = (1.0e6 / s) * (1.0 / (3.0 * s * s - g))
        P(f"        {nm} (γ={g:.4f}): contrast gain at h=1000000 = {c:.6f} → 1/3")
    P("    → equal fractional steps feel equal regardless of γ: a Weber-Fechner-like law, FORCED not fitted.")
    P("    [honest scope] this is the SATURATED branch; near the fold (small h) the γ·s term matters and the")
    P("    response is steeper than a clean power law — the Weber regime is the cube-root tail, stated not hidden.")

    # ----------------------------------------------------------------------------------------
    # PART D — two regimes; where γ and τ sit; the felt percept hands off
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART D — two regimes (dark/fold vs bright/saturated); γ sets the offset, τ sets the recovery")
    P("-" * 80)
    P("    DARK  (operating point near the fold h*): high incremental gain + the single-photon FLIP")
    P(f"          (E2 detection threshold at h*={spinodal(G_RHO):.5f}); the ON-branch gain here is the")
    P(f"          largest in the sweep ({gains[0]:.6e} at h={SWEEP[0]}).")
    P(f"    BRIGHT (driven deep into the cube root): low gain ({gains[-1]:.6e}), the response")
    P("          compressed against saturation. Adaptation = the operating point SLIDING fold → cube-root.")
    # γ is READ-ONLY: it sets WHERE the fold sits (offset), NOT the compression (cubic order, γ-independent)
    P(f"\n    γ READ-ONLY: γ(RHO)={G_RHO:.4f} sets the fold/offset (where dark sensitivity sits); the")
    P("    compression law (contrast gain → 1/3) is γ-INDEPENDENT (PART C) — γ is an OFFSET, as in E7/E8.")
    # the recovery τ is the time course of re-sensitisation (E7/E8 inheritance), READ-ONLY
    nu = Neuron()
    P(f"    τ READ-ONLY: dark re-sensitisation runs on the FROZEN Neuron's recovery τ_s = {nu.tau_s:.1f} "
      f"(β = {nu.beta:.1f}),")
    P("    the same time-constant that set the band (E7) and the rate code (E8). Structure [F]; absolute")
    P("    seconds are the inherited [O]. The felt brightness percept is OUT OF SCOPE (→ mind volume).")
    assert nu.tau_s == 40.0 and nu.beta == 0.5, "the recovery τ_s/β must be read byte-equal from the frozen Neuron"

    # no-drift: the γ E10 reads is byte-equal to the frozen atlas (no fitting)
    no_drift = (ATLAS["RHO"]["gamma"] == G_RHO and ATLAS["CNGB3"]["gamma"] == G_CNGB3)
    P(f"\n    [no-drift] anchor γ byte-equal to frozen atlas (no fitting): {no_drift}")
    assert no_drift, "E10 must consume the frozen γ unchanged (no fitting)"

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E10 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the ON-branch steady state saturates onto the cube root s*→h^(1/3); the")
    P("                 incremental gain ds*/dh = 1/(3s*²−γ) falls with the background (gain control);")
    P("                 the CONTRAST gain → exactly 1/n = 1/3 (a Weber-like law) and is γ-independent;")
    P("                 deep-saturation log-compression → the cubic order n=3; γ is an offset, not the law.")
    P("  [V] verified : every s* is a true zero of the FROZEN field (residual ≈ 0); s*/h^(1/3) → 1")
    P("                 monotonically; the gain falls monotonically dim→bright; the contrast gain rises to")
    P("                 1/3 and the pure-cube limit is exactly 0.333333; τ_s/β byte-equal; γ byte-equal.")
    P("  [L] measured : γ(RHO), γ(CNGB3) (NCBI promoters, cached, read-only); Weber's law and the")
    P("                 brightness power-law exponent (~1/3) are the cited psychophysics this matches.")
    P("  [O] open     : the absolute background→drive→firing scale (inherited E2/E5) — so no absolute")
    P("                 threshold, Weber fraction, or luminance unit is produced; the absolute τ→seconds")
    P("                 of dark adaptation (inherited E7/E8); the molecular adaptation machinery (Ca²⁺")
    P("                 feedback on guanylate cyclase, pigment bleaching/regeneration) — the substrate")
    P("                 captures the COMPRESSION, not that feedback loop; the felt brightness percept")
    P("                 (→ mind volume). Each obstacle named, not invented.")
    P("\nLEARNED: light/dark adaptation needs no new machinery — it is the SAME R19 switch read on its")
    P("         steady-state ON branch, where the cube makes the response saturate (s*→h^(1/3)). That one")
    P("         fact gives all three signatures: a huge background range is log-compressed by the cubic")
    P("         order n=3 (dynamic range), the incremental gain falls automatically as the surround")
    P("         brightens (gain control), and — the headline — the FRACTIONAL (contrast) gain is constant")
    P("         at exactly 1/n = 1/3, a Weber-Fechner-like law FORCED by the cube and INDEPENDENT of γ.")
    P("         γ only sets where the dark fold sits (an offset, as in E7/E8); τ sets the dark-recovery")
    P("         time course (E7/E8); the absolute scales and the felt percept stay honestly open.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    text = buf.getvalue()
    return hashlib.sha256(text.encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
