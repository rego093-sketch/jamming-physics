#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
run.py — increment E5 :  the READOUT substrate (otoferlin Ca²⁺-triggered ribbon-synapse release).
                         Turns E4's named [O] (the synaptic layer the cubic cannot see) into a MODELLED
                         READOUT failure — auditory neuropathy as a two-stage cascade.

WHAT THIS BUILDS (BLUEPRINT.md E-plan — the open item E4 N4 / WORK_HANDOVER item 3).
  E4 closed congenital deafness as the cubic's failure-mode decomposition, but ONE class was left as
  an honest [O]: the READOUT class (OTOF / auditory neuropathy). E4's own words — "the switch flips
  normally, the cubic sees nothing wrong, the broken layer is the downstream synapse [O]". E5 supplies
  that downstream layer EXPLICITLY and composes it with the (frozen, unedited) transduction cubic, so
  the OTOF phenotype stops being asserted and becomes REPRODUCED.

  The keystone is a STRUCTURAL one: the readout layer CANNOT be the R19 cubic, and that is forced, not
  assumed. The cubic ṡ = g·s − s³ + h is two-sided, odd-symmetric, and BISTABLE (a detector). A
  vesicle-release rate is none of those: it is NON-NEGATIVE (you cannot release negative vesicles),
  MONOTONE in Ca²⁺, and SATURATING (a finite readily-releasable pool). Those three properties are
  forced by what release physically IS — a non-negative, pool-limited counting process — and the
  minimal normal form carrying exactly them is a rectified saturating (Hill) sensor, NOT a cubic. So
  the READOUT layer is a genuinely DIFFERENT substrate downstream of the switch; E4 was right that the
  cubic is blind to it, and E5 says precisely why.

  Composed with the cubic, this forces three results: (1) auditory neuropathy = a NORMAL switch flip
  (s identical to a hearing ear, the E4 number) feeding a ZEROED sensor → silence; (2) the auditory-
  nerve rate inherits a COMPOSED compression exponent F^(m/3) = (E3 amplifier cube-root 1/3) × (synaptic
  Ca²⁺-cooperativity m); (3) the clinical OAE-present / ABR-absent dissociation, because the amplifier
  (E3, outer-hair-cell) and the readout (E5, inner-hair-cell synapse) are SEPARABLE stages of one
  cascade. The lever direction for OTOF — left [O] by E4 — is now FORCED: restore the sensor coupling
  (the readout stage), not (g,h). Its magnitude stays [O].

THE BIOLOGY (cited, not re-opened; consumed from the DNA + biology volumes).
  OTOF encodes otoferlin, the multi-C2-domain Ca²⁺ SENSOR for vesicle fusion at the inner-hair-cell
  (IHC) ribbon synapse — the hair cell's synaptotagmin-replacement (Roux et al. 2006). Loss causes
  DFNB9 / auditory neuropathy spectrum disorder: the cochlea transduces and (via outer hair cells)
  amplifies normally — otoacoustic emissions (OAE) are PRESENT — but Ca²⁺-triggered transmitter
  release to the auditory nerve fails, so the auditory brainstem response (ABR) is absent/grossly
  abnormal. The Ca²⁺-dependence of mature-IHC exocytosis is reported as low-order / near-linear
  (cooperativity ~1), versus the high-order (~3–4) cooperativity of conventional synapses (Dodge &
  Rahamimoff 1967; Beutner et al. 2001; Johnson et al. 2005) — but the exact order is study-dependent
  and is treated here as a CITED knob [L], never derived, never tuned.

HOW IT RELATES TO THE FOUNDATION (no-regression — note: NO inherited byte changes in E5).
  EXTENDS the inherited foundation by IMPORTING it. Unlike E4, E5 fetches NO new gene and folds nothing
  into the cache/atlas — it touches NOT ONE inherited byte and triggers NO re-freeze (every frozen hash
  stays valid as recorded at seed time). It consumes the INHERITED `vp_substrate.py` cubic directly
  (`sdot`/`settle`/`spinodal`/`is_on`) — the switch states it reads are the SAME numbers E1/E2/E3/E4
  produce — and the measured atlas via E1's `read_measured` (OTOF's γ+A4 recompute from the frozen
  cache and equal the atlas bit-for-bit). The cubic is consumed, never re-opened.

GRADES (VP-SPEC C3 ; [F] forced · [V] verified · [L] measured/calibrated · [O] open, obstacle named).
  [F]/[V] : the readout layer is a DIFFERENT normal form forced by what release is (non-negative,
            monotone, saturating, NON-bistable — no hysteresis, in contrast to the cubic) ; the
            auditory-neuropathy DISSOCIATION (identical switch flip s=+1.3864 in a hearing AND an OTOF
            ear — the substrate sees nothing wrong — feeding an intact sensor R>0 vs a zeroed sensor
            R=0) ; the COMPOSED compression exponent F^(m/3) (the E3 cube-root composed with the
            power-law sensor, fit to m/3 at machine precision) ; the OAE-present/ABR-absent dissociation
            (amplifier stage intact while readout stage zeroed — separable stages) ; the OTOF lever
            DIRECTION (restore the readout/sensor stage, not the switch) — upgrading E4 N4.
  [L]      : OTOF's γ (NCBI-measured, cached) ; the synaptic Ca²⁺-cooperativity m (cited biology,
            study-dependent ~1 mature-IHC / ~3–4 conventional) — a knob read in, never fitted.
  [O]      : EVERY magnitude — absolute [Ca²⁺], the sensor Kd / Rmax, the readily-releasable-pool size,
            the release rate in vesicles/s, the auditory-nerve rate in Hz, any threshold in real units ;
            the exact Ca²⁺(s) map (the CaV1.3 I–V curve + nanodomain geometry — here a minimal monotone
            rectifying proxy Ca ∝ s₊) ; the molecule / dose / in-vivo selectivity / efficacy of the
            OTOF lever (firewall — proposal-only) ; the felt percept of hearing (→ mind volume) ; and
            the full fluid-loaded dispersive traveling-wave ENVELOPE (still the named [O] — closing it
            would require TUNING Q, forbidden). Each names its obstacle below.

FIREWALL. γ reads promoter STRUCTURE only — never a Ca²⁺-sensor affinity, a release rate, a vesicle
count, a dose, an in-vivo selectivity, or a clinical effect. The disease layer is PROPOSAL-ONLY:
a direction-only READOUT-failure mode and a direction-only substrate-inverse lever. Nothing here
diagnoses, treats, or prescribes; no molecule is designed; no dose or efficacy is stated. The felt
percept of sound is the mind volume's.

stdlib + numpy. Deterministic; 2× run → identical sha256 (the verifier greps the last 'sha256:' line).
"""
import os, sys, json, math, hashlib, io, importlib.util
import numpy as np

# --- locate the package root and import the FROZEN inherited foundation (never edited) -------------
_HERE = os.path.dirname(os.path.abspath(__file__))
ROOT  = os.path.dirname(os.path.dirname(_HERE))           # research/E5-*/ -> package root
sys.path.insert(0, os.path.join(ROOT, "inherited"))
import vp_substrate as SUB                                # the R19 cubic (sdot/settle/spinodal/is_on)


def _load(name, path):
    """Load a module by file path under a UNIQUE name (every increment ships a file called run.py;
    importing under the bare name 'run' would collide in sys.modules — this keeps them distinct)."""
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod; spec.loader.exec_module(mod)
    return mod

# reuse E1's read_measured (asserts cache==atlas, A4⊥, exact-precision spinodal) under a unique name
E1 = _load("e1_run", os.path.join(ROOT, "research", "E1-place-and-traveling-wave", "run.py"))

READOUT_GENE = "OTOF"                                     # otoferlin — the IHC ribbon-synapse Ca²⁺ sensor
SWITCH_GENE  = "TMC1"                                     # the MET pore (E1/E2/E4 switch reference)

# the converged drive range for the composed-exponent [V] (identical convention to E3/E4; E3 N5)
_F_LO_EXP, _F_HI_EXP, _F_N, _SETTLE_N = -1.0, 2.0, 10, 20000


def drive_grid():
    return [10.0 ** e for e in np.linspace(_F_LO_EXP, _F_HI_EXP, _F_N)]


# ============================================================================================
#  the READOUT substrate — a DIFFERENT normal form, downstream of the cubic (NOT bistable)
#    Forced by what release IS: non-negative (rectified), monotone in Ca²⁺, saturating (RRP).
#    The minimal form with exactly those properties is a rectified saturating (Hill) sensor.
#    Magnitudes (Kd, Rmax, the Ca²⁺(s) scale) are [O]; the STRUCTURE is what is forced.
# ============================================================================================
def ca_proxy(s):
    """Minimal monotone RECTIFYING Ca²⁺ proxy from the switch output: only the depolarised (ON, s>0)
    basin gates Ca²⁺ influx; the hyperpolarised (OFF, s<0) basin gives none. Uses the substrate's OWN
    zero (the basin boundary) — no tuned resting point. The exact Ca²⁺(s) map (CaV1.3 I–V + nanodomain
    geometry) is [O]; this proxy carries only the forced sign/rectification."""
    return max(0.0, float(s))


def release(ca, m, Kd=1.0, Rmax=1.0):
    """Sensor-INTACT evoked release: rectified, monotone, SATURATING Hill response of cooperativity m.
    Kd=Rmax=1.0 are SCALE units (magnitudes are [O]); only the SHAPE/structure is the claim."""
    c = max(0.0, float(ca))
    return Rmax * (c ** m) / (Kd ** m + c ** m)


def release_unsat(ca, m):
    """Sub-saturating (small-signal / operating-regime) limit R ∝ Ca^m — used ONLY to read off the
    COMPOSED exponent cleanly (away from RRP saturation). Pure power law, no tuned constant."""
    c = max(0.0, float(ca))
    return c ** m


def release_knockout(ca, m, Kd=1.0, Rmax=1.0):
    """Sensor-REMOVED (OTOF-class): the Ca²⁺ sensor is gone, so Ca²⁺-triggered fusion does not occur for
    ANY Ca²⁺ level — the evoked release is identically zero. Models 'otoferlin absent' (auditory
    neuropathy): no diagnosis, dose, or efficacy is implied (firewall)."""
    return 0.0


def composed_exponent(m):
    """Fit the exponent of the cascade output R_unsat(settle(0,F)) vs drive F over the E3/E4 converged
    range. The transduction output at criticality is settle(0,F) ≈ F^(1/3) (E3); feeding it into R∝Ca^m
    gives R ∝ F^(m/3). Returns the FITTED slope (not imposed)."""
    Fs = drive_grid()
    R  = [release_unsat(SUB.settle(0.0, F, n=_SETTLE_N, dt=0.01), m) for F in Fs]
    return float(np.polyfit(np.log10(Fs), np.log10(R), 1)[0])


# =====================================================================================================
def run(P):
    P("=" * 94)
    P("E5 — the READOUT substrate (otoferlin / OTOF): Ca²⁺-triggered ribbon-synapse release")
    P("     a wave -> a spatial code -> an R19 switch -> [E5] a DOWNSTREAM Ca²⁺-sensor readout")
    P("     turning E4's [O] (the synaptic layer) into a MODELLED auditory-neuropathy failure")
    P("=" * 94)

    # -- PART 0 : the readout gene reproduces offline (γ LEVEL + A4 SHAPE) -----------------------------
    P("\n[0] the readout gene reproduces offline (γ LEVEL + A4 SHAPE, recomputed from frozen cache):")
    ot = E1.read_measured(READOUT_GENE)                  # asserts cache==atlas & A4 = signal−γ for OTOF
    P(f"    [PASS] {READOUT_GENE:8s} γ(level)={ot['gamma']:.4f}  A4 amp={ot['shape_amplitude']:.5f} "
      f"range={ot['shape_range']:.5f}  node={ot['node']}  (otoferlin / IHC ribbon-synapse Ca²⁺ sensor)")
    P("    -> OTOF γ+A4 equals the atlas bit-for-bit; A4 = signal − γ (|mean(shape)|<1e-9). No new gene")
    P("       was fetched and NO inherited byte changed in E5 (no re-freeze — frozen hashes stay valid). [V]")

    # -- PART A : the readout layer is a DIFFERENT normal form, forced by what release IS --------------
    P("\n[A] the keystone — the readout layer CANNOT be the cubic (forced by what release physically is):")
    P("    A vesicle-release rate is NON-NEGATIVE, MONOTONE in Ca²⁺, and SATURATING (finite RRP). The")
    P("    cubic ṡ=g·s−s³+h is two-sided, odd, and BISTABLE — none of those. Verify the sensor's three")
    P("    forced properties, and that (unlike the cubic) it has NO hysteresis (it is not bistable):")
    m_demo = 3
    cas = [0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0]
    Rs  = [release(c, m_demo) for c in cas]
    nonneg = all(r >= 0.0 for r in Rs)
    mono   = all(Rs[i + 1] >= Rs[i] for i in range(len(Rs) - 1))
    sat    = (release(1e6, m_demo) <= 1.0 + 1e-12) and (release(1e6, m_demo) > release(1.0, m_demo))
    for c, r in zip(cas, Rs):
        P(f"       Ca₊={c:5.2f}  ->  R={r:.5f}")
    P(f"    non-negative={nonneg}   monotone↑={mono}   saturating→Rmax={sat}  (m={m_demo}, Kd=Rmax=1 units)")
    # hysteresis test: the sensor is a pure function of Ca — up-sweep and down-sweep coincide (no memory)
    up   = [release(c, m_demo) for c in cas]
    down = [release(c, m_demo) for c in reversed(cas)][::-1]
    no_hyst = max(abs(up[i] - down[i]) for i in range(len(cas))) < 1e-15
    P(f"    NON-bistable: up-sweep == down-sweep (hysteresis area = 0, max|Δ|<1e-15) -> {no_hyst}")
    P("    -> the READOUT is a rectified saturating sensor, a DIFFERENT substrate from the bistable")
    P("       cubic. This is WHY E4's cubic is blind to OTOF: it is the wrong layer, provably.  [F]/[V]")
    assert nonneg and mono and sat and no_hyst

    # -- PART B : the cascade — feed the FROZEN cubic's flip into the sensor; auditory neuropathy -------
    P("\n[B] the cascade — the (frozen) switch flips IDENTICALLY in a hearing AND an OTOF ear; only the")
    P("    downstream sensor differs. Drive a sound (h past the spinodal); read the switch, then release:")
    gT = E1.read_measured(SWITCH_GENE)["gamma"]; sp = SUB.spinodal(gT)
    s_rest = SUB.settle(gT, 0.0)                          # silence: switch OFF (the E4 number)
    s_on   = SUB.settle(gT, 1.5 * sp)                     # sound: switch flips ON (the E4 number)
    ca_rest, ca_on = ca_proxy(s_rest), ca_proxy(s_on)
    m_ihc = 1                                             # cited mature-IHC near-linear cooperativity [L]
    R_hear_rest = release(ca_rest, m_ihc); R_hear_on = release(ca_on, m_ihc)
    R_otof_rest = release_knockout(ca_rest, m_ihc); R_otof_on = release_knockout(ca_on, m_ihc)
    P(f"    switch g=γ_TMC1={gT:.4f}, spinodal={sp:.4f}:")
    P(f"      SILENCE (h=0)      : s={s_rest:+.4f} OFF  -> Ca₊={ca_rest:.4f}")
    P(f"      SOUND   (h=1.5·sp) : s={s_on:+.4f} ON   -> Ca₊={ca_on:.4f}   (IDENTICAL in both ears)")
    P(f"    HEARING ear (sensor intact, m={m_ihc}): release  silence={R_hear_rest:.4f}  sound={R_hear_on:.4f}  -> nerve FIRES")
    P(f"    OTOF    ear (sensor removed)         : release  silence={R_otof_rest:.4f}  sound={R_otof_on:.4f}  -> nerve SILENT")
    P("    -> auditory neuropathy MODELLED: the switch flip is byte-identical to a hearing ear (the")
    P("       substrate sees nothing wrong — E4's [H]); the ZEROED Ca²⁺ sensor breaks transmission. The")
    P("       defect is purely downstream of the flip — exactly E4's READOUT class, now reproduced.  [F]/[V]")
    assert abs(s_on - 1.3864) < 1e-3 and R_hear_on > 0.0 and R_otof_on == 0.0

    # -- PART C : the COMPOSED exponent — E3 cube-root composed with the synaptic power law -------------
    P("\n[C] the composition law — the auditory-nerve rate inherits a COMPOSED exponent F^(m/3):")
    P("    at criticality the transduction output compresses as settle(0,F) ≈ F^(1/3) (E3); feeding it")
    P("    into a power-law sensor R ∝ Ca^m gives R ∝ (F^(1/3))^m = F^(m/3). Fit it (NOT imposed):")
    for m in (1, 2, 3, 4):
        slope = composed_exponent(m)
        P(f"      synaptic cooperativity m={m}: fitted cascade exponent = {slope:.6f}   (m/3 = {m/3:.6f}; "
          f"|Δ|={abs(slope - m/3):.1e})")
        assert abs(slope - m / 3.0) < 1e-5
    P("    -> the cascade's compression is the AMPLIFIER cube-root (1/3, forced [F]) TIMES the synaptic")
    P("       cooperativity m (cited [L]). The composition exponent is FORCED given m; the absolute rate")
    P("       is [O]. Falsifiable: the auditory-nerve rate-level slope = (1/3)·m, e.g. ~1/3 if m≈1.  [F]/[V]")

    # -- PART D : the OAE-present / ABR-absent dissociation (the clinical fingerprint) ------------------
    P("\n[D] the clinical fingerprint — OAE PRESENT, ABR ABSENT, forced by SEPARABLE cascade stages:")
    amp_slope = float(np.polyfit(np.log10(drive_grid()),
                                 np.log10([SUB.settle(0.0, F, n=_SETTLE_N, dt=0.01) for F in drive_grid()]), 1)[0])
    P(f"    stage 1 AMPLIFIER (E3, outer hair cell / prestin): cube-root response intact, exponent="
      f"{amp_slope:.6f}")
    P(f"      -> otoacoustic emissions (the amplifier's signature) are PRESENT in an OTOF ear.")
    P(f"    stage 2 READOUT  (E5, inner hair cell / otoferlin): release ZEROED (sensor removed)")
    P(f"      -> the auditory-brainstem response (neural firing) is ABSENT in an OTOF ear.")
    P("    -> OAE⁺/ABR⁻ is the textbook auditory-neuropathy signature, and it is FORCED here: the")
    P("       amplifier (OHC, upstream/parallel) and the readout (IHC synapse, downstream) are DIFFERENT")
    P("       stages, so one is intact while the other fails. It also DISTINGUISHES the readout class from")
    P("       the drive/structure classes (which would also degrade OAE / thresholds).  [F]/[V]")
    assert abs(amp_slope - 1.0 / 3.0) < 1e-6

    # -- PART E : the substrate-inverse lever DIRECTION (upgrades E4 N4 from [O] to forced direction) ---
    P("\n[E] the lever — DIRECTION now forced (E4 left it [O]); magnitude [O]; proposal-only:")
    P("    E4: 'the READOUT layer (OTOF/synapse) is not modelled ... its rescue direction is [O]'.")
    P("    E5: the layer IS modelled, and the geometry forces the lever DIRECTION — act on the READOUT")
    P("        STAGE (restore Ca²⁺-sensor coupling / Ca²⁺-triggered fusion), NOT on the switch (g,h): the")
    P("        switch is provably intact (PART B). This is the OPPOSITE locus from the drive class")
    P("        (restore h) and the structure class (rebuild g). DIRECTION-ONLY, PROPOSAL-ONLY — no")
    P("        molecule, dose, in-vivo selectivity, or efficacy; nothing diagnosed or treated.  [F] direction")

    # -- honest negatives preserved (readout-specific) -------------------------------------------------
    P("\n[honest negatives — preserved, not hidden]")
    P("    N1  EVERY magnitude is [O]: absolute [Ca²⁺], the sensor Kd/Rmax, the readily-releasable-pool")
    P("        size, the release rate (vesicles/s), the auditory-nerve rate (Hz), any real-unit threshold.")
    P("        Only the STRUCTURE (rectifying/saturating/non-bistable), the dissociation, and the")
    P("        composed EXPONENT m/3 are forced.")
    P("    N2  the synaptic cooperativity m is CITED biology [L], study-dependent (~1 mature IHC / ~3–4")
    P("        conventional), NEVER derived from the substrate and NEVER tuned. The composed result is")
    P("        given parametrically in m; its qualitative force (silence on knockout) is m-independent.")
    P("    N3  the Ca²⁺(s) map is a MINIMAL monotone rectifying proxy Ca ∝ s₊ on the substrate's own")
    P("        zero. The real map (CaV1.3 I–V curve + Ca²⁺-nanodomain geometry) is [O]; only the sign/")
    P("        rectification is used, and the disease result does not depend on its detailed shape.")
    P("    N4  'sensor removed' is modelled as evoked release ≡ 0 (no Ca²⁺-triggered fusion). Graded/")
    P("        partial otoferlin loss, temperature-sensitive variants, and the spontaneous (resting)")
    P("        release component are [O]; E5 models the EVOKED, sound-driven release only.")
    P("    N5  the lever is DIRECTION-ONLY and PROPOSAL-ONLY (firewall). No molecule is designed, no dose")
    P("        or efficacy stated; nothing is diagnosed or treated. The felt percept is the mind volume's.")
    P("    N6  the full fluid-loaded dispersive traveling-wave ENVELOPE is STILL the named [O] — a closed")
    P("        envelope needs Q + fluid mass-loading + the E3 amplifier and would require TUNING Q")
    P("        (forbidden). E5 does not touch it; it remains open with its obstacle named.")

    # -- naming note (flagged, not silently fixed) ----------------------------------------------------
    P("\n[naming note] This delivers the E4-N4 READOUT extension in the unambiguous folder")
    P("    research/E5-readout-synapse/. The v0.3.0 folder/BLUEPRINT E-numbering slip (BLUEPRINT-E2 in the")
    P("    folder labelled E1; BLUEPRINT-E1 = the traveling-wave ENVELOPE, still the named [O]) STANDS")
    P("    flagged; E5 introduces no new inconsistency.")

    P("\nLEARNED (E5): the auditory-neuropathy READOUT class — E4's honest [O] — is now MODELLED. The")
    P("  readout is a rectified saturating Ca²⁺ sensor, a DIFFERENT substrate from the bistable cubic")
    P("  (forced by what release is), so the cubic is provably blind to it. Composing the sensor with the")
    P("  FROZEN switch reproduces auditory neuropathy (identical flip s=+1.3864, zeroed release), forces")
    P("  the rate-level compression F^(m/3) (E3 cube-root × cited cooperativity m), forces the OAE⁺/ABR⁻")
    P("  dissociation (separable amplifier ∥ readout stages), and forces the lever DIRECTION (restore the")
    P("  sensor stage). Every magnitude stays [O]; nothing is tuned; no inherited byte changed.")


def main():
    SUB.seed_everything(SUB.SEED)            # determinism (no RNG is used, but lock the seed anyway)
    buf = io.StringIO()
    def P(*a): print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
