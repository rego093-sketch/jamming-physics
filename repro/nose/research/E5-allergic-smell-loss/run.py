#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E5-allergic-smell-loss/run.py — INCREMENT E5: allergic (acquired) smell loss.

                THEORETICAL / NON-CLINICAL.  Direction-only / proposal-only (FIREWALL.md #4, #8).
                No diagnosis, dose, molecule, or efficacy. The felt experience is the mind volume's.

WHAT E5 DOES (BLUEPRINT.md E5; research/E5-allergic-smell-loss/START_HERE.md).
  This is the seed's ACQUIRED disease layer — the sibling of E4's CONGENITAL anosmia. The most common
  real-world nose complaint, allergic rhinitis (Type-2 airway inflammation), is NOT primarily an
  olfactory-transduction or olfactory-development disease: it is an IMMUNE hypersensitivity. The VP
  discipline is to take the allergy MECHANISM from the volume that owns it and derive ONLY the part
  that is genuinely olfactory — how Type-2 inflammation makes you lose your SMELL.

  CONSUMED, NOT RE-DERIVED (one-way cite, FIREWALL.md #8):
    - the allergic MECHANISM — sensitization at the R19 spinodal, the dose×repetition threshold, the
      LATCH, and controlled DESENSITIZATION (= allergen immunotherapy = basin-acting re-tolerization)
      — is the IMMUNE/HEMATOLOGIC volume's §11 "Allergy: sensitization, the latch, and controlled
      desensitization", graded [V] there (DOI 10.5281/zenodo.20755280). E5 computes NONE of it (no
      priming, no tolerance accumulator, no crossover dose); it cites it.
    - the ABSOLUTE airway aeroallergen load and mucosal scale are the RESPIRATORY volume's [O] (the
      immune volume itself defers the airway antigen scale to the surface owner). E5 owns NONE of it.

  OWNED HERE (the olfactory-surface consequence — what no other volume can state): allergic rhinitis
  impairs smell by TWO substrate-expressible routes, and they are TELLABLE APART by one move —
  RESTORE THE DRIVE: conductive recovers, sensorineural does not. Built ONLY on the FROZEN inherited
  substrate + the measured atlas:

    PART A — CONDUCTIVE loss = a DRIVE suppression on the E1/E2 switches (REVERSIBLE; the switch is intact).
      Mucosal swelling + secretion reduce the odorant flux reaching the olfactory cleft, so the
      per-receptor drive on the FROZEN OR/transduction switches is attenuated by a conductive factor
      κ∈[0,1] (κ=1 clear, κ<1 inflamed). γ is UNTOUCHED — this is not a switch defect. Sweep κ down:
      the measured OR panel flips OFF in spinodal(γ) order (E1's thermometer in reverse) and the smell
      percept fades to anosmia; RESTORE κ→1 and the percept returns EXACTLY, because nothing was
      damaged. The geometry of "stuffy-nose smell loss that comes back". [F]/[V]

    PART B — SENSORINEURAL loss = an ORGAN degradation on E2/E3 (PERSISTENT; the SAME R19 organ-
      formation failure as E4, but ACQUIRED). Chronic Type-2 inflammation damages the olfactory
      epithelium / OSNs. This is NOT a drive problem: the OSN compartment's master cis-drive falls
      below its γ-set R19 PRESENCE threshold (inherited Organ; "parts present ≠ trait"), so the OSNs
      are absent and NO receptor can carry a percept — regardless of κ. This is E4's organ-formation
      failure mode reached by inflammation instead of a Kallmann mutation. [F]/[V]

    PART C — THE DISCRIMINATOR + the firewall in action. Restore the conductive drive (κ→1): the
      CONDUCTIVE percept recovers to baseline (decongestion helps), the SENSORINEURAL percept stays
      zero (decongestion cannot help; the restorative lever must act on the ORGAN, and recovery is not
      guaranteed). DIRECTION-only levers (sign only): conductive → κ↑ (restore odorant access), and
      its UPSTREAM cause is addressed by the immune volume's §11 desensitization (cited); sensorineural
      → protect/restore the epithelium (anti-inflammatory), recovery not guaranteed. No dose, molecule,
      or efficacy. The odorant→receptor key stays E1's [O]; the felt percept is the mind volume's.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E5 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing, fits nothing, and
  adds NO gene (no new γ; the two frozen DATA files are untouched — no-regression).
    - the R19 switch + Organ (spinodal/settle/is_on/Organ) ← inherited/vp_substrate.py (frozen)
    - the OR bank + OSN-identity organisers' γ            ← inherited/organ_gamma.json (MEASURED [L];
                                                            verify_seed [3] re-proves it offline [V])
    - the allergy mechanism (sensitization/latch/desens.) ← immune/hematologic §11 (cited [V]; DOI
                                                            10.5281/zenodo.20755280) — NOT re-derived
  κ (the conductive factor) and the organ degradation are ABSTRACT STRUCTURAL representations: κ is NOT
  a measured mucus/airflow value (that absolute airway scale is the respiratory volume's [O]); the
  organ loss is the inherited Organ presence mechanism, NOT a measured cell count. γ is promoter
  STRUCTURE only (FIREWALL #1); nothing diagnoses or treats (FIREWALL #3, #4, #8).

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

from vp_substrate import spinodal, barrier, settle, is_on, Organ      # FROZEN: the R19 switch + Organ

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the olfactory-receptor bank (E1's channels) and the OSN-identity organisers (E3's apparatus) — by
# atlas node; stated, not selected to a target.
OR_GENES   = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_receptor"))
ORGANISERS = tuple(sorted(s for s, r in ATLAS.items() if r.get("node") == "olfactory_neuron_identity"))

N_STEPS, DT = 1500, 0.02            # the FROZEN settle() defaults — fixed, not tuned

# the immune volume that OWNS the allergy mechanism (cited, never re-derived here)
IMMUNE_ALLERGY = "immune/hematologic §11 (sensitization · latch · desensitization), DOI 10.5281/zenodo.20755280 [V]"


def rest_basin(g):
    return -math.sqrt(g)


def or_on(sym, h):
    """One OR channel: does the FROZEN R19 switch (measured γ) flip ON under drive h?"""
    g = ATLAS[sym]["gamma"]
    return settle(g, h, s0=rest_basin(g), n=N_STEPS, dt=DT) > 0.0


def osn_compartment_present(cis_drive):
    """The OSN population exists only if its identity organisers clear their γ-set R19 PRESENCE
    threshold (inherited Organ; 'parts present ≠ trait'). SENSORINEURAL allergic damage drops the
    compartment's effective master drive below threshold — the SAME organ-formation failure as E4,
    reached by chronic inflammation instead of a Kallmann mutation."""
    return all(Organ(s, ATLAS[s]["gamma"]).present(cis_drive) for s in ORGANISERS)


def percept_count(kappa, h0, cis_drive):
    """How many OR channels carry an odour percept. SENSORINEURAL gate: the OSN compartment must be
    PRESENT (organ intact). CONDUCTIVE gate: the attenuated drive κ·h0 must clear each OR's FROZEN
    spinodal. If the organ is gone, no κ can help; if the organ is intact, κ alone modulates."""
    if not osn_compartment_present(cis_drive):
        return 0
    return sum(or_on(s, kappa * h0) for s in OR_GENES)


def on_set(kappa, h0, cis_drive):
    order = sorted(OR_GENES, key=lambda s: spinodal(ATLAS[s]["gamma"]))
    if not osn_compartment_present(cis_drive):
        return ()
    return tuple(s for s in order if or_on(s, kappa * h0))


def run(P):
    N = len(OR_GENES)
    or_thr  = [spinodal(ATLAS[s]["gamma"]) for s in OR_GENES]
    org_thr = [spinodal(ATLAS[s]["gamma"]) for s in ORGANISERS]
    H0          = 1.15 * max(or_thr)          # a healthy supra-threshold odour: all ORs on at κ=1
    CIS_HEALTHY = 1.10 * max(org_thr)         # OSN compartment present  (above every organiser's h*)
    CIS_DAMAGED = 0.90 * min(org_thr)         # OSN compartment lost     (below every organiser's h*)

    P("=" * 80)
    P("E5 — ALLERGIC (ACQUIRED) SMELL LOSS   (conductive ↔ sensorineural; tell apart by RESTORING drive)")
    P("=" * 80)
    P("THEORETICAL / NON-CLINICAL — direction-only / proposal-only (FIREWALL #4,#8). No dose/molecule/efficacy.")
    P("consumes (frozen): vp_substrate.Organ/spinodal/settle/is_on · organ_gamma.json γ+A4 (MEASURED)")
    P("consumes (cited, NOT re-derived): the allergy mechanism = " + IMMUNE_ALLERGY)
    P("owns here: ONLY the olfactory-surface consequence (smell loss). aeroallergen/airway scale = respiratory [O].")
    P(f"the OR bank (N={N}): {', '.join(OR_GENES)}")
    P(f"the OSN-identity organisers (N={len(ORGANISERS)}): {', '.join(ORGANISERS)}")

    # ------------------------------------------------------------------------------------------
    # PART A — conductive loss = drive suppression on the E1/E2 switches (reversible)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — CONDUCTIVE loss: a DRIVE suppression (κ↓) on the FROZEN OR switches — REVERSIBLE  [F]/[V]")
    P("-" * 80)
    P("allergic mucosal swelling reduces odorant flux → the per-receptor drive is attenuated h → κ·h0.")
    P("γ is UNTOUCHED (no switch defect); the OR panel flips OFF in spinodal(γ) order (E1 thermometer, reversed):")
    P(f"  baseline healthy odour drive H0 = 1.15·max(h*_OR) = {H0:.5f}  (organ intact: cis = {CIS_HEALTHY:.4f})")
    P(f"  {'κ (conductive)':>14s} {'# OR on':>8s}  percept (ON set in spinodal order)")
    sweep = (1.00, 0.95, 0.90, 0.86, 0.82, 0.60, 0.30, 0.00)
    counts = []
    for k in sweep:
        n = percept_count(k, H0, CIS_HEALTHY)
        counts.append(n)
        st = on_set(k, H0, CIS_HEALTHY)
        P(f"  {k:14.2f} {n:8d}  {st if st else '(anosmia — no OR above threshold)'}")
    # the fade is monotone (lower drive can only switch OR channels OFF, never ON — a nested thermometer)
    assert counts[0] == N, "at κ=1 (clear nose) the healthy odour lights all OR channels"
    assert counts[-1] == 0, "at κ=0 (total conductive block) the percept is anosmia"
    assert all(counts[i] >= counts[i + 1] for i in range(len(counts) - 1)), \
        "conductive fade must be monotone in κ (drive↓ can only turn channels OFF)"
    # REVERSIBLE: restore the drive (κ→1) and the percept returns EXACTLY — the switches were never damaged
    recovered = percept_count(1.00, H0, CIS_HEALTHY)
    P(f"  → RESTORE κ→1 (decongestion / inflammation resolves): percept = {recovered}/{N} — FULLY RECOVERED.")
    P("    conductive smell loss is REVERSIBLE: γ intact, the FROZEN flip intact; only the drive moved.  [F]/[V]")
    assert recovered == N, "conductive loss must fully reverse when the drive is restored (switch intact)"

    # ------------------------------------------------------------------------------------------
    # PART B — sensorineural loss = organ degradation on E2/E3 (persistent; acquired E4-type failure)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — SENSORINEURAL loss: the OSN ORGAN degrades (E2/E3) — PERSISTENT (acquired E4 failure)  [F]/[V]")
    P("-" * 80)
    P("chronic Type-2 inflammation damages the olfactory epithelium/OSNs: the OSN compartment's master")
    P("cis-drive falls below its γ-set PRESENCE threshold — the SAME R19 organ-formation failure as E4,")
    P("reached by inflammation, not a Kallmann mutation. NO κ can help: with the organ gone, no channel fires.")
    P(f"  {'organiser':9s} {'γ':>7s} {'h*=presence':>11s} {'present@healthy cis':>20s} {'present@damaged cis':>20s}")
    for s in sorted(ORGANISERS, key=lambda s: spinodal(ATLAS[s]["gamma"])):
        g = ATLAS[s]["gamma"]; o = Organ(s, g)
        ph = o.present(CIS_HEALTHY); pd = o.present(CIS_DAMAGED)
        P(f"  {s:9s} {g:7.4f} {o.functional_spinodal():11.5f} {str(ph):>20s} {str(pd):>20s}")
        assert ph is True and pd is False, f"{s}: OSN organ must be present @healthy cis, absent @damaged cis"
    present_healthy = osn_compartment_present(CIS_HEALTHY)
    present_damaged = osn_compartment_present(CIS_DAMAGED)
    n_sensorineural_fulldrive = percept_count(1.00, H0, CIS_DAMAGED)   # FULL conductive drive, organ gone
    P(f"  OSN compartment present?  healthy: {present_healthy}   damaged: {present_damaged}")
    P(f"  → percept at FULL conductive drive κ=1 with the organ damaged = {n_sensorineural_fulldrive}/{N} (anosmia).")
    P("    sensorineural smell loss is PERSISTENT: it is an ORGAN failure, not a drive failure.  [F]/[V]")
    assert present_healthy is True and present_damaged is False, "OSN compartment present↔absent across the threshold"
    assert n_sensorineural_fulldrive == 0, "with the OSN organ gone, even full conductive drive gives anosmia"

    # ------------------------------------------------------------------------------------------
    # PART C — the discriminator (restore the drive) + the firewall in action
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — THE DISCRIMINATOR: restore the drive (κ→1). conductive recovers; sensorineural does not.")
    P("-" * 80)
    kappa_block = 0.82
    n_block          = percept_count(kappa_block, H0, CIS_HEALTHY)   # conductive disease, partial block
    n_block_treated  = percept_count(1.00,        H0, CIS_HEALTHY)   # restore drive → recovers
    n_sn             = percept_count(1.00,        H0, CIS_DAMAGED)   # sensorineural, full drive → stays 0
    P(f"  CONDUCTIVE    : partial block κ={kappa_block} → percept {n_block}/{N};  restore κ=1 → {n_block_treated}/{N}  (RECOVERS)")
    P(f"  SENSORINEURAL : organ damaged, full drive κ=1 → percept {n_sn}/{N}                       (does NOT recover)")
    P("  → ONE move separates them: restoring the drive. The substrate expresses the clinical")
    P("    conductive-vs-sensorineural distinction as DRIVE (E1/E2) vs ORGAN (E2/E3).  [F]/[V]")
    assert n_block < N and n_block_treated == N and n_sn == 0, "the discriminator must hold (conductive reverses; sensorineural does not)"

    P("\n[direction-only restorative levers — SIGN only, no dose/molecule/efficacy (FIREWALL #4,#8)]")
    P("  conductive    : κ↑  — restore odorant access (reduce the mucosal drive). The UPSTREAM allergic")
    P("                  cause (why the inflammation persists, and how to re-tolerize it) is the immune")
    P("                  volume's §11 desensitization — CITED, not re-derived here.")
    P("  sensorineural : the lever must act on the ORGAN (protect/restore the epithelium), NOT on κ;")
    P("                  recovery is NOT guaranteed (a degraded organ may not return). DIRECTION only.")
    P("  NEITHER lever states a dose, a molecule, a potency, or an efficacy. The felt experience of")
    P("  smelling — and of an allergy attack — is the mind volume's, cited not re-derived.")

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E5 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : conductive loss = a drive suppression on the FROZEN OR switches (γ intact), so it")
    P("                 is reversible by restoring the drive; sensorineural loss = the inherited R19 organ-")
    P("                 presence failure (parts present ≠ trait), so it is persistent under any drive —")
    P("                 the acquired form of E4's organ-formation mode. The discriminator (restore drive)")
    P("                 is forced by which layer moved (drive vs organ).")
    P("  [V] verified : the conductive fade is monotone in κ and recovers EXACTLY at κ=1; the OSN organ is")
    P("                 present↔absent across its presence threshold; sensorineural percept stays 0 at full")
    P("                 drive. (OR/organiser γ+A4 re-proved offline bit-for-bit by verify_seed [3].)")
    P("  [L] measured : every OR and organiser γ (+A4) from NCBI promoters — UNCHANGED, byte-identical to")
    P("                 the frozen atlas. E5 adds NO gene and fits NOTHING (no-regression).")
    P("  [O] open / cited : the ALLERGY MECHANISM (sensitization, latch, desensitization) is the immune")
    P("                 volume's §11 [V] (DOI 10.5281/zenodo.20755280), cited not re-derived; the ABSOLUTE")
    P("                 aeroallergen/airway-mucosal scale (and the literal value of κ) is the respiratory")
    P("                 volume's [O]; the odorant→receptor key stays E1's [O]; the felt percept → mind volume.")
    P("\nLEARNED: the most common nose disease is an IMMUNE disease, so its mechanism is NOT re-derived here —")
    P("         it is consumed from the volume that owns it. What the olfactory substrate genuinely OWNS, and")
    P("         what no other volume can say, is the CONSEQUENCE: allergic rhinitis takes your smell two ways —")
    P("         conductively (a reversible DRIVE suppression on the intact E1/E2 switches) and sensorineurally")
    P("         (a persistent ORGAN degradation, the acquired form of E4's failure) — and the two are told")
    P("         apart by a single substrate move, restoring the drive. Foundation untouched; no gene added;")
    P("         nothing fitted; the allergy mechanism cited; the airway scale deferred; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
