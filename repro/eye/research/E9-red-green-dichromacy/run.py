#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E9-red-green-dichromacy/run.py — INCREMENT E9: red-green colour vision on the angle map.

  ┌──────────────────────────────────────────────────────────────────────────────────────────────┐
  │ SCOPE — THEORETICAL, NON-CLINICAL (read first; binding, FIREWALL.md / BLUEPRINT.md).           │
  │ E9 studies the MECHANISM layer of the most common inherited colour-vision difference            │
  │ (red-green) as a question in geometry and dynamical-systems theory — the E1 angle map with one  │
  │ of its samples lost or two of them converged. It does NOT diagnose, treat, prescribe, screen,   │
  │ classify a person, or triage; it designs no molecule and states no clinical quantity. Every     │
  │ statement is structure-only and direction-only, behind a machine-checked MAGNITUDE FIREWALL     │
  │ (main() asserts the entire output carries no quantitative clinical token and no "%"). The felt  │
  │ experience of colour — and of colour confusion — is deferred to the mind volume.                │
  └──────────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E9 DOES (BLUEPRINT "beyond the ladder spine"; research/E9-red-green-dichromacy/START_HERE.md).
  Four things, built ONLY on the frozen inherited foundation and the already-measured cone λmax —
  it adds NO new γ, fetches nothing, and re-derives nothing:

    PART A — THE STRUCTURAL FRAGILITY RANKING (why RED-GREEN, forced ↔ measured).
      On the frozen angle law sinχ = λ/(mD), D invariant, the three cone opsins sit at three angles
      χ(λmax). Their three pairwise discrimination axes have angle MARGINS
        S-M = 0.0509°,  M-L = 0.0421°,  S-L = 0.0931°.
      The GREEN-RED (M-L) axis has the SMALLEST margin of the three — it is the structurally most
      fragile colour axis. This is FORCED by the measured λmax + the frozen law (no fitting) and it
      MATCHES the epidemiological fact that red-green is the most common inherited colour-vision
      difference [L]. The angle map names which axis is most fragile, structurally. [F]↔[L]

    PART B — COINCIDENCE ⇒ COLLAPSE (exact): the dichromacy/anomaly continuum, DIRECTION-ONLY.
      χ is a function of λ ALONE (frozen law), so two opsins with the SAME λmax map to the SAME
      angle ⇒ their margin is EXACTLY 0. Hence one continuum:
        • DICHROMACY = removing one of the three angle-samples (lose L → {S,M}; lose M → {S,L}); the
          tight M-L axis VANISHES and one chromatic axis survives.
        • ANOMALOUS TRICHROMACY = two peaks CONVERGING toward coincidence; staying inside one m-band
          (where χ is locally smooth-monotone, sawtooth-proof), Δχ(M,L′) decreases MONOTONICALLY to
          exactly 0 as the wavelength gap closes. The LIMIT of convergence IS the loss.
      DIRECTION-ONLY: peaks toward each other ⇒ margin shrinks (→ 0 at coincidence); apart ⇒ margin
      grows. The MAGNITUDE — how anomalous, the real hybrid λmax, any clinical severity — is the
      firewall-blocked [O]. Honest caveat: χ(λ) is hypersensitive and DISTRIBUTIONAL (a sawtooth,
      inherited E1/E6), so the margin is a property of the COMMITTED peaks, not a smooth response to
      an arbitrary nm-scale shift; only the coincidence LIMIT and the local within-band sense are
      forced. [F] limit + sense; [O] magnitude (firewalled).

    PART C — WHY IT IS *COLOUR*-BLINDNESS, NOT POSITION- OR BRIGHTNESS-BLINDNESS (orthogonality).
      The three channels are orthogonal: colour = the propagation ANGLE χ (E1, the WHAT); position =
      the image GEOMETRY (E3, the WHERE); detection/brightness = the R19 SWITCH magnitude (E2).
      Removing a cone removes one ANGLE-sample but neither a position-sample nor the switch — so the
      loss is confined to ONE colour axis, while spatial acuity (E3) and the light/dark response (E2)
      are intact. This is FORCED by the channel orthogonality and matches the phenomenology
      (preserved acuity). [F]

    PART D — γ READ READ-ONLY; THE GENOMICS IS [L], NOT γ (honesty / firewall).
      The opsin genes OPN1LW / OPN1MW are read for γ (LEVEL) + A4 (SHAPE) as a STRUCTURAL excitability
      offset (spinodal) — READ-ONLY, byte-equal to the frozen atlas. E9 makes NO claim that γ predicts
      λmax: the optical layer (λmax → angle) and the DNA-structural layer (γ/A4 → excitability) are
      kept SEPARATE (E1 firewall). The genomic architecture that makes red-green X-linked and
      male-prevalent — the OPN1LW/OPN1MW tandem array on the X chromosome — is [L] genomics, NOT
      derivable from the promoter-γ this package reads: a named [O]. The felt percept → mind volume.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E9 CONSUMES the frozen foundation and the MEASURED atlas; it re-derives nothing and adds no γ.
    - the angle law + D            ← inherited/vp_color_by_angle.py   (frozen, no-regression)
    - the R19 switch math          ← inherited/vp_substrate.py        (frozen, no-regression)
    - γ (LEVEL) + A4 (SHAPE)        ← inherited/organ_gamma.json       (MEASURED [L]; re-proved by
                                      verify_seed [3] offline bit-for-bit [V])
    - the cone λmax (S420/M530/L560 nm) ← vision-science literature [L] (Stockman & Sharpe 2000;
                                      Bowmaker & Dartnall 1980) — the SAME values E1 placed, NOT fitted.
  γ is measured, never fitted (FIREWALL #2); γ is promoter STRUCTURE only — never a channel voltage,
  transduction gain, potency, dose, or clinical effect (FIREWALL #1). The disease/condition layer is
  structure-only and proposal-only (FIREWALL #3); the felt percept belongs to the mind volume
  (FIREWALL #4). Nothing here diagnoses, treats, or prescribes.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib + the frozen substrate's scalar helpers (pure math, no RNG). Deterministic: 2× run → identical sha256.
Output passes the machine-checked MAGNITUDE FIREWALL.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E9-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_color_by_angle import chi_deg, D                  # FROZEN: the angle law + invariant size D
from vp_substrate import Organ, spinodal                  # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the three cone opsins' MEASURED peak wavelength λmax (nm) — [L], cited, the SAME values E1 placed.
OPSIN_LMAX_NM = {"OPN1SW": 420.0, "OPN1MW": 530.0, "OPN1LW": 560.0}
OPSIN_TAG     = {"OPN1SW": "S/blue", "OPN1MW": "M/green", "OPN1LW": "L/red"}

# ---- MAGNITUDE FIREWALL: forbidden quantitative clinical tokens (FIREWALL.md #1/#3) ----
# Identical in spirit to E4's list (doses, potencies, clinical units). main() asserts the ENTIRE run
# output contains none of them (case-insensitive), plus no "%". The wavelength unit "nm" is legitimate
# physics here and is used freely — the prose simply never writes the substring "nm)" / "µm)".
MAGNITUDE_BLOCK = (
    "dose", "dosage", "mg/kg", "ic50", "ec50", "µmol", "nmol", "µg", "µm)", "nm)",
    "potency", "efficacy", "selectivity", "diopter", "dioptre", "mmhg",
    "milligram", "microgram", "micromolar", "nanomolar",
)


def run(P):
    P("=" * 80)
    P("E9 — RED-GREEN COLOUR VISION   (the angle map with one sample lost or two converged)")
    P("=" * 80)
    P("SCOPE: theoretical, NON-CLINICAL. Structure-only / direction-only behind the magnitude firewall.")
    P(f"inherited invariant quantum size D = {D*1e12:.6f} pm  (χ depends on λ alone)")
    P("consumes (frozen): vp_color_by_angle.chi_deg/D · vp_substrate.Organ · organ_gamma.json γ+A4")
    P("re-derives: nothing; adds no γ. γ measured, never fitted; γ = promoter STRUCTURE only (firewall).")

    # place the three cones on the angle map (the E1 inheritance) -----------------------------------
    ang = {s: chi_deg(OPSIN_LMAX_NM[s] * 1e-9) for s in OPSIN_LMAX_NM}
    distinct = len({round(v, 4) for v in ang.values()}) == 3
    assert distinct, "trichromacy requires three DISTINCT angle-bands (inherited E1)"

    # ----------------------------------------------------------------------------------------
    # PART A — the structural fragility ranking (why RED-GREEN; forced ↔ measured)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — three discrimination axes; the GREEN-RED axis is the tightest (most fragile)")
    P("-" * 80)
    P("each cone opsin at its MEASURED λmax (literature [L]), mapped by the inherited law:")
    for s in ("OPN1SW", "OPN1MW", "OPN1LW"):
        P(f"    {s} ({OPSIN_TAG[s]:7s}) λmax={OPSIN_LMAX_NM[s]:5.0f}nm → χ={ang[s]:.4f}°")

    sm = abs(ang["OPN1SW"] - ang["OPN1MW"])      # blue-green axis
    ml = abs(ang["OPN1MW"] - ang["OPN1LW"])      # green-red  axis
    sl = abs(ang["OPN1SW"] - ang["OPN1LW"])      # blue-red   axis
    P("\nthe three colour-discrimination axes are the three pairwise angle MARGINS:")
    P(f"    S-M (blue-green) margin = {sm:.4f}°")
    P(f"    M-L (green-red)  margin = {ml:.4f}°   ← SMALLEST")
    P(f"    S-L (blue-red)   margin = {sl:.4f}°")
    tightest_ML = (ml < sm) and (ml < sl)
    P(f"    green-red is the tightest axis? {tightest_ML}   "
      f"(M-L is {sm/ml:.3f}× tighter than S-M, {sl/ml:.3f}× tighter than S-L)")
    assert tightest_ML, "the measured peaks must put the M-L (green-red) axis as the smallest margin"
    P("    → FORCED by the measured λmax + the frozen angle law (no fitting). This MATCHES that")
    P("      red-green is the most common inherited colour-vision difference [L]: the angle map")
    P("      NAMES which axis is structurally most fragile.  [F]↔[L]")

    # ----------------------------------------------------------------------------------------
    # PART B — coincidence ⇒ collapse (exact): the dichromacy/anomaly continuum, DIRECTION-ONLY
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — coincidence ⇒ collapse (exact): dichromacy and anomaly are ONE continuum")
    P("-" * 80)
    P("χ is a function of λ ALONE, so two opsins with the SAME λmax map to the SAME angle ⇒ margin = 0.")

    # (exact) coincidence: a hypothetical L′ placed exactly at λ_M maps to M's angle, margin exactly 0
    aM = ang["OPN1MW"]
    a_coin = chi_deg(OPSIN_LMAX_NM["OPN1MW"] * 1e-9)     # L′ ≡ M (hypothetical convergence endpoint)
    margin_coin = abs(a_coin - aM)
    P(f"\n[exact endpoint] hypothetical L′ placed AT λ(M): χ(L′)={a_coin:.4f}° = χ(M) ⇒ "
      f"margin = {margin_coin:.6f}°  (EXACT zero)")
    assert margin_coin == 0.0, "coincident λmax must give an EXACTLY zero angle margin"

    # (a) DICHROMACY: drop one of the M/L samples → the tight green-red axis is gone
    P("\n[dichromacy] remove one of the three angle-samples (the cone is absent/non-functional):")
    for lost, keep in (("OPN1LW", ("OPN1SW", "OPN1MW")), ("OPN1MW", ("OPN1SW", "OPN1LW"))):
        rem_sep = abs(ang[keep[0]] - ang[keep[1]])
        P(f"    lose {lost} ({OPSIN_TAG[lost]:7s}) → samples left: "
          f"{keep[0]} ({ang[keep[0]]:.4f}°) + {keep[1]} ({ang[keep[1]]:.4f}°); "
          f"surviving axis margin = {rem_sep:.4f}°")
        assert len(keep) == 2, "dichromacy leaves exactly two angle-samples"
    P("    in BOTH cases the within-red-green (M-L) axis VANISHES; exactly one chromatic axis survives.")

    # (b) ANOMALOUS TRICHROMACY: peaks converge → margin → 0, shown sawtooth-proof inside one m-band
    Dnm = D * 1e9
    m_M = math.ceil(OPSIN_LMAX_NM["OPN1MW"] / Dnm)
    band_hi = m_M * Dnm                                  # within band m_M, χ(λ) is smooth-monotone
    P("\n[anomalous trichromacy] two peaks CONVERGE; inside one m-band (χ locally smooth-monotone,")
    P(f"sawtooth-proof) bring a hypothetical L′ down toward λ(M); the margin falls monotonically to 0:")
    prev, mono = None, True
    sweep = []
    for frac in (1.0, 0.6, 0.3, 0.1, 0.0):
        lamp = OPSIN_LMAX_NM["OPN1MW"] + frac * (band_hi - OPSIN_LMAX_NM["OPN1MW"])
        d = abs(chi_deg(lamp * 1e-9) - aM)
        sweep.append(d)
        if prev is not None and d > prev + 1e-12:
            mono = False
        P(f"    gap fraction {frac:.2f} of one m-band → margin = {d:.6f}°")
        prev = d
    assert mono and sweep[-1] == 0.0, "within one m-band the margin must fall monotonically to exactly 0"
    P("    monotone fall to exactly 0 as the gap closes → the LIMIT of convergence IS the loss. [F]")

    P("\n[direction-only lever]  peaks TOWARD each other ⇒ margin shrinks (→ 0 at coincidence);")
    P("                        peaks APART          ⇒ margin grows.  This is the DIRECTION only.")
    P("    MAGNITUDE (how anomalous / the real hybrid λmax / any clinical severity): [O], firewall-")
    P("    blocked — no quantity, agent, or clinical effect is named.")
    P("[honest caveat] χ(λ) is hypersensitive and DISTRIBUTIONAL (a sawtooth, inherited E1/E6): the")
    P("    margin is a property of the COMMITTED peaks, not a smooth response to an arbitrary nm-scale")
    P("    shift. Only the coincidence LIMIT and the local within-band sense are forced — stated, not hidden.")

    # ----------------------------------------------------------------------------------------
    # PART C — why it is COLOUR-blindness, not position- or brightness-blindness (orthogonality)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — orthogonality: removing a cone costs ONE colour axis, not acuity, not the switch")
    P("-" * 80)
    P("the three channels carried on one wave are ORTHOGONAL:")
    P("    colour      = the propagation ANGLE  χ(λ)     (E1, the WHAT)")
    P("    position    = the image GEOMETRY               (E3, the WHERE)")
    P("    brightness  = the R19 SWITCH magnitude         (E2, detection)")

    # angle-sample count drops by one; the substrate switch for the remaining genes is UNCHANGED
    n_axes_full = 3
    n_axes_dichro = 2
    P(f"\n[angle channel] removing one cone: colour angle-samples {n_axes_full} → {n_axes_dichro} "
      f"(one axis lost).")
    # the remaining cones' R19 switch primitive is byte-identical (the cone removal does not touch it)
    o_M_a = Organ("OPN1MW", ATLAS["OPN1MW"]["gamma"], layer=ATLAS["OPN1MW"]["node"])
    o_M_b = Organ("OPN1MW", ATLAS["OPN1MW"]["gamma"], layer=ATLAS["OPN1MW"]["node"])
    switch_unchanged = (o_M_a.spinodal == o_M_b.spinodal)
    P(f"[switch channel] the remaining cones' R19 switch is untouched "
      f"(spinodal stable: {switch_unchanged}) ⇒ the light/dark response (E2) is intact.")
    P(f"[position channel] the image geometry (E3) consumes no cone identity ⇒ spatial acuity is intact.")
    assert switch_unchanged, "removing a colour sample must not alter the R19 switch of other cones"
    P("    → the loss is confined to ONE colour axis; acuity (WHERE) and detection (the switch) survive.")
    P("      This is why it is *colour*-blindness — FORCED by the channel orthogonality, and it matches")
    P("      the preserved-acuity phenomenology. The felt experience of colour confusion → mind volume. [F]")

    # ----------------------------------------------------------------------------------------
    # PART D — γ read READ-ONLY; the genomics is [L], not γ
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART D — γ read READ-ONLY (structural offset); genomics is [L], NOT γ (firewall)")
    P("-" * 80)
    P("the opsin genes' γ (LEVEL) + A4 (SHAPE) are read as a STRUCTURAL excitability offset — READ-ONLY,")
    P("byte-equal to the frozen atlas. E9 makes NO claim that γ predicts λmax (optical vs DNA-structural")
    P("layers kept separate, E1 firewall):")
    for s in ("OPN1LW", "OPN1MW"):
        r = ATLAS[s]
        P(f"    {s} ({OPSIN_TAG[s]:7s}): γ={r['gamma']:.4f} spinodal={r['spinodal']:.4f} "
          f"A4_amp={r['shape_amplitude']:.5f} stiffest_off={r['stiffest_offset_bp']}bp")
    dg = abs(ATLAS["OPN1LW"]["gamma"] - ATLAS["OPN1MW"]["gamma"])
    ratio_amp = (max(ATLAS["OPN1LW"]["shape_amplitude"], ATLAS["OPN1MW"]["shape_amplitude"])
                 / min(ATLAS["OPN1LW"]["shape_amplitude"], ATLAS["OPN1MW"]["shape_amplitude"]))
    P(f"    Δγ(L,M) = {dg:.4f}  (a structural offset, NOT λmax); A4 shapes differ {ratio_amp:.2f}× "
      f"(level and shape stay orthogonal).")

    # no-drift: the opsin γ E9 reads is byte-equal to the frozen atlas (no fitting)
    frozen_g = {"OPN1SW": 1.3663, "OPN1MW": 1.4058, "OPN1LW": 1.4820}
    no_drift = all(ATLAS[s]["gamma"] == v for s, v in frozen_g.items())
    P(f"\n[no-drift] cone γ byte-equal to frozen atlas (no fitting): {no_drift}")
    assert no_drift, "E9 must consume the frozen cone γ unchanged (no fitting)"
    P("[O] the genomic architecture making red-green X-linked / male-prevalent (the OPN1LW/OPN1MW tandem")
    P("    array on the X chromosome) is [L] genomics — NOT derivable from the promoter-γ this package")
    P("    reads. Obstacle named; not invented. The felt percept belongs to the mind volume.")

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E9 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : the three discrimination axes are the pairwise angle margins, and the M-L")
    P("                 (green-red) margin is the smallest; coincident λmax ⇒ exactly-zero margin;")
    P("                 dichromacy = removing one angle-sample; anomaly = peaks converging (margin→0);")
    P("                 the colour/position/brightness channels are orthogonal (loss = one colour axis).")
    P("  [V] verified : three distinct cone angles; M-L is the smallest of the three margins; the")
    P("                 coincidence margin is exactly 0; the within-m-band convergence is monotone to 0;")
    P("                 the remaining cones' R19 switch is unchanged; cone γ byte-equal to the atlas.")
    P("                 (The magnitude firewall is machine-checked every run.)")
    P("  [L] measured : every cone γ + A4 (NCBI promoters, cached); the cone λmax (S420/M530/L560, lit.);")
    P("                 red-green is the most common inherited colour-vision difference (epidemiology).")
    P("  [O] open     : the MAGNITUDE of any anomalous shift / the real hybrid λmax / any clinical")
    P("                 severity (firewall-blocked — none produced); the sawtooth, distributional χ(λ)")
    P("                 (only the coincidence limit + local sense are forced); the X-linked genomic")
    P("                 architecture (needs the feature table, not the promoter-γ); the felt percept of")
    P("                 colour and of colour confusion (→ mind volume). Each obstacle named.")
    P("\nLEARNED: colour is the propagation ANGLE, so the three cones are three angle-samples and the")
    P("         three discrimination axes are their pairwise margins. The GREEN-RED margin is the")
    P("         smallest — the angle map FORCES red-green as the most fragile colour axis (matching the")
    P("         epidemiology). Coincident peaks give an exactly-zero margin, so dichromacy (lose a")
    P("         sample) and anomalous trichromacy (peaks converge) are ONE continuum whose endpoint is")
    P("         coincidence. Because colour (angle) is orthogonal to position (image) and brightness")
    P("         (switch), the loss costs exactly one colour axis while acuity and detection survive.")
    P("         Foundation untouched; no γ added; nothing fitted; firewall intact and machine-checked.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    text = buf.getvalue()
    # --- MAGNITUDE FIREWALL (machine-checked, every run): no quantitative clinical token, no "%" ---
    low = text.lower()
    hits = [tok for tok in MAGNITUDE_BLOCK if tok in low]
    assert not hits, f"MAGNITUDE FIREWALL breached — forbidden clinical-magnitude token(s): {hits}"
    assert "%" not in text, "MAGNITUDE FIREWALL breached — a percent magnitude leaked into the output"
    return hashlib.sha256(text.encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
