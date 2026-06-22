#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E4-congenital-anosmia/run.py — INCREMENT E4: congenital anosmia (the goal).

  ┌─ SCOPE & SAFETY — THEORETICAL, NON-CLINICAL — READ FIRST ────────────────────────────────────┐
  │ This is purely academic, theoretical, computational research into the MECHANISM LAYER of      │
  │ congenital olfactory conditions as a dynamical-systems question (the R19 switch). It does NOT  │
  │ diagnose, treat, screen, triage, or prescribe; it designs NO molecule and states NO dose,      │
  │ potency, selectivity, efficacy, or clinical effect. EVERY statement here is DIRECTION-ONLY and │
  │ PROPOSAL-ONLY (FIREWALL.md #4). The felt experience of anosmia is the mind volume's. Nothing    │
  │ here is, or is usable as, medical advice or clinical software.                                 │
  └────────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E4 DOES (BLUEPRINT.md E4; research/E4-congenital-anosmia/START_HERE.md).
  The goal increment. Vision/hearing's congenital sensory disease is "the transduction switch fails
  to flip." Smell adds a second failure route — "the smelling apparatus never forms" — and E4 reads
  BOTH from the FROZEN substrate, as the substrate's TWO R19 failure modes. The congenital-anosmia
  genes split cleanly into the two classes, and each class is one substrate primitive failing:

    PART A — THE TWO R19 FAILURE MODES (each read from the frozen substrate; direction-only).
      (1) TRANSDUCTION-SWITCH failure — CNGA2 (CNG α, principal), CNGB1 (CNG β). The olfactory CNG
          channel IS the inherited R19 switch (E2). A loss-of-function removes the bistable switch:
          with the cubic restoring term gone, the field has NO on-basin, so the all-or-none
          transduction flip can NEVER occur regardless of drive → no transduction → no smell. We show
          the WT switch flips past h* and that deleting the switch destroys the flip (E2's necessity,
          re-pointed as the failure). The substrate-inverse lever DIRECTION (proposal-only, no
          dose/molecule/efficacy): restore a bistable switch whose on-basin is reachable by
          physiological drive — i.e. re-enable the flip. A direction, never a therapy.
      (2) ORGAN-FORMATION failure — ANOS1, FGFR1, PROKR2, PROK2 (Kallmann syndrome). Here the
          smelling apparatus (olfactory sensory neurons + bulb) never EMERGES: the master switch
          never clears its R19 presence threshold (vp_substrate.Organ, FROZEN) → the organ is ABSENT
          ("parts present ≠ trait") → no smell. Because the same GnRH-neuron migration depends on this
          olfactory-placode programme, the Kallmann signature is anosmia WITH hypogonadotropic
          hypogonadism — the organ-formation failure's fingerprint. The inverse-lever DIRECTION
          (proposal-only): restore the master switch's clearing of its presence threshold. Direction only.

    PART B — THE CROSS-SENSE CASE: CNGB1 LOF IMPAIRS BOTH SMELL AND ROD VISION (the shared switch).
      CNGB1 (CNG β) is the SAME gene in olfaction and rod vision; its measured γ here is byte-identical
      to the rod-vision sibling (E2). So a CNGB1 loss-of-function is the SAME R19 switch failing in TWO
      senses at once — predicted to impair smell AND rod-mediated (dim-light) vision (the CNGB1 retinal
      phenotype) together. This is FORCED by the shared substrate primitive, not an analogy [V].

    PART C — THE FIREWALL IN ACTION (honest scope, restated where it matters most).
      Every line above is direction-only / proposal-only: no diagnosis, no dose, no molecule, no
      efficacy. The substrate gives the FAILURE-MODE CLASS (which R19 primitive fails) and the SIGN of
      a hypothetical restorative lever — nothing more. The odorant-identity layer is still the named
      [O] (E1); the felt experience of anosmia is the mind volume's; the absolute restorative magnitude
      is an [O] that this volume deliberately does NOT supply.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E4 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing, fits nothing.
    - the R19 switch + Organ math (sdot/spinodal/settle/is_on/Organ) ← inherited/vp_substrate.py (frozen)
    - γ (LEVEL) + A4 (SHAPE) per anosmia gene                        ← inherited/organ_gamma.json (MEASURED
                                                                       [L]; verify_seed [3] re-proves it offline)
      (CNGA2, CNGB1, ANOS1, FGFR1 inherited; PROKR2, PROK2 fetched from NCBI and folded in at v0.6.0.)
  γ is measured, never fitted (FIREWALL #3); γ is promoter STRUCTURE only — never a channel current, a
  dose, a potency, or a clinical effect (FIREWALL #1). The order-parameter s is the abstract R19 field,
  NOT a receptor current/Hz. The disease layer is PROPOSAL-ONLY (FIREWALL #4); the felt percept belongs
  to the mind volume (FIREWALL #5). The _linear_control is the substrate with its cubic STRUCK OUT — it
  shows what losing the switch costs; it does not fork the substrate.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers + Organ — pure math, no RNG.
Deterministic: 2× run → identical sha256.
"""
import os, sys, json, math, hashlib, io

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, barrier, settle, is_on, Organ   # FROZEN: the R19 switch + Organ

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the two failure CLASSES, read from the atlas nodes — stated, not selected to a target.
CHANNELOPATHY = ("CNGA2", "CNGB1")                         # transduction-switch failure (CNG channel)
DEVELOPMENTAL = tuple(sorted(s for s, r in ATLAS.items()  # organ-formation failure (Kallmann)
                             if r.get("node") == "congenital_anosmia"))

# CITED cross-sense reference: CNGB1 γ as independently measured for ROD VISION (sibling eye seed).
ROD_VISION_CNGB1_GAMMA = 1.4357

N_STEPS, DT = 1500, 0.02             # the FROZEN settle() defaults — fixed, not tuned


def rest_basin(g):
    return -math.sqrt(g)


def _linear_control(g, h, s0=0.0, n=4000, dt=DT):
    """STRUCTURAL CONTROL — NOT the substrate. The substrate field with its cubic −s³ STRUCK OUT,
    leaving a stable first-order field ds/dt = −g·s + h (steady state s* = h/g): no double well, no
    on-basin, no all-or-none flip. It models what a loss-of-function of the CHANNEL costs: the switch
    is gone. It exists ONLY to show the failure mode; it does not fork the substrate."""
    s = s0
    for _ in range(n):
        s += dt * (-g * s + h)
    return s


def run(P):
    P("=" * 80)
    P("E4 — CONGENITAL ANOSMIA   (theoretical / NON-CLINICAL — DIRECTION-ONLY, PROPOSAL-ONLY)")
    P("=" * 80)
    P("SCOPE: mechanism-layer research only. No diagnosis, dose, molecule, or efficacy. Felt percept → mind.")
    P("consumes (frozen): vp_substrate.sdot/spinodal/settle/Organ · organ_gamma.json γ+A4 (MEASURED)")
    P("re-derives: nothing. γ measured, never fitted. γ = promoter STRUCTURE only (firewall).")
    P("the substrate's TWO R19 failure modes: (1) the transduction switch can't flip; (2) the organ can't form.")
    P(f"  channelopathy genes : {', '.join(CHANNELOPATHY)}  (CNG channel = the R19 transduction switch, E2)")
    P(f"  organ-formation genes: {', '.join(DEVELOPMENTAL)}  (Kallmann: OSN/bulb never emerges)")

    # ------------------------------------------------------------------------------------------
    # PART A(1) — transduction-switch failure (CNGA2, CNGB1)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A(1) — TRANSDUCTION-SWITCH failure: a CNG loss-of-function removes the R19 flip  [V] / direction-only")
    P("-" * 80)
    P("the olfactory CNG channel IS the inherited R19 switch (E2). WT: the field flips on past h*.")
    P("LOF: with the bistable switch gone (cubic struck out) there is NO on-basin — the flip can NEVER")
    P("occur, at any drive → no transduction → no smell. (We re-point E2's necessity result as the failure.)")
    P(f"\n  {'gene':6s} {'role':38s} {'γ':>7s} {'h*':>9s} {'WT s@1.10h*':>11s} {'LOF(no switch)@1.10h*':>21s}")
    for sym in CHANNELOPATHY:
        g = ATLAS[sym]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
        wt_below = settle(g, 0.90 * hstar, s0=s0, n=N_STEPS, dt=DT)
        wt_above = settle(g, 1.10 * hstar, s0=s0, n=N_STEPS, dt=DT)
        lof_above = _linear_control(g, 1.10 * hstar)        # the switch removed → graded, no on-basin
        P(f"  {sym:6s} {ATLAS[sym].get('role','')[:38]:38s} {g:7.4f} {hstar:9.5f} "
          f"{wt_above:+11.4f} {lof_above:+21.4f}")
        assert wt_below < 0.0 < wt_above and (wt_above - wt_below) > 1.5, f"{sym}: WT switch must flip past h*"
    # NECESSITY: the cubic switch is all-or-none; deleting it (the LOF) destroys the flip (E2 G4, re-pointed)
    g = ATLAS["CNGA2"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    s_lo, s_hi = settle(g, 0.99 * hstar, s0=s0, n=N_STEPS, dt=DT), settle(g, 1.01 * hstar, s0=s0, n=N_STEPS, dt=DT)
    cubic_slope  = abs(s_hi - s_lo) / (0.02 * hstar)
    graded_slope = abs(_linear_control(g, 1.10 * hstar) - _linear_control(g, 0.90 * hstar)) / (0.20 * hstar)
    ratio = cubic_slope / graded_slope
    P(f"\n  [the cost of losing the switch] WT cubic flip slope ≈ {cubic_slope:.0f} vs switch-removed "
      f"≈ {graded_slope:.2f}  ({ratio:.0f}×)")
    P(f"  → removing the channel removes the all-or-none flip entirely. The failure mode is: the R19")
    P(f"    transduction switch cannot flip.  [V] structure of the failure.")
    assert ratio > 20.0, "the WT switch must be ≥ an order of magnitude steeper than the switch-removed control"
    P("  [direction-only lever, PROPOSAL-ONLY] restore a bistable switch whose on-basin is reachable by")
    P("    physiological drive — i.e. re-enable the flip (sign: +). NO dose, NO molecule, NO efficacy. [O] magnitude.")

    # ------------------------------------------------------------------------------------------
    # PART A(2) — organ-formation failure (ANOS1, FGFR1, PROKR2, PROK2 — Kallmann)
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A(2) — ORGAN-FORMATION failure (Kallmann): the OSN/bulb never EMERGES  [V] / direction-only")
    P("-" * 80)
    P("here the smelling apparatus never forms: the master switch never clears its R19 presence threshold")
    P("(vp_substrate.Organ) → the organ is ABSENT ('parts present ≠ trait') → no smell. Signature: anosmia")
    P("WITH hypogonadotropic hypogonadism (the shared olfactory-placode/GnRH programme failing).")
    P(f"\n  {'gene':7s} {'role':36s} {'γ':>7s} {'h*':>9s} {'LOF: present@0.90h*':>20s} {'WT: present@1.10h*':>19s}")
    for sym in DEVELOPMENTAL:
        o = Organ(sym, ATLAS[sym]["gamma"], master=sym, layer="congenital_anosmia")
        hstar = o.functional_spinodal()
        lof = o.present(0.90 * hstar)                       # LOF → switch fails to clear threshold → absent
        wt  = o.present(1.10 * hstar)                       # WT  → clears threshold → organ emerges
        P(f"  {sym:7s} {ATLAS[sym].get('role','')[:36]:36s} {o.g:7.4f} {hstar:9.5f} "
          f"{str(lof):>20s} {str(wt):>19s}")
        assert (lof is False) and (wt is True), f"{sym}: LOF must yield absence, WT must yield emergence"
    P("  → an intact downstream pathway with the master switch below threshold still yields organ ABSENCE.")
    P("    The failure mode is: the R19 organ-emergence switch cannot clear its presence threshold.  [V]")
    P("  [direction-only lever, PROPOSAL-ONLY] restore the master switch's clearing of its presence")
    P("    threshold (sign: +). NO dose, NO molecule, NO efficacy. [O] magnitude / developmental window.")

    # ------------------------------------------------------------------------------------------
    # PART B — cross-sense: CNGB1 LOF impairs BOTH smell and rod vision
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — cross-sense: a CNGB1 loss-of-function impairs BOTH smell and rod vision (the SHARED switch)")
    P("-" * 80)
    cngb1 = ATLAS["CNGB1"]["gamma"]
    P(f"CNGB1 (CNG β) is the SAME gene in olfaction and rod vision:")
    P(f"    olfactory seed (here): γ = {cngb1:.4f}   spinodal h* = {spinodal(cngb1):.5f}")
    P(f"    rod-vision seed (cited eye sibling): γ = {ROD_VISION_CNGB1_GAMMA:.4f}")
    P(f"    byte-identical? {cngb1 == ROD_VISION_CNGB1_GAMMA}")
    assert cngb1 == ROD_VISION_CNGB1_GAMMA, "CNGB1 γ must match the rod-vision sibling (same gene)"
    P("  → it is the SAME R19 transduction switch. A CNGB1 LOF is therefore predicted to fail in TWO")
    P("    senses at once: olfaction AND rod-mediated (dim-light) vision (the CNGB1 retinal phenotype),")
    P("    together. FORCED by the shared substrate primitive — a cross-sense prediction, not an analogy.  [V]")

    # ------------------------------------------------------------------------------------------
    # PART C — the firewall in action
    # ------------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the firewall in action (honest scope, where it matters most)")
    P("-" * 80)
    P("every statement above is DIRECTION-ONLY / PROPOSAL-ONLY:")
    P("  · no diagnosis, no screening, no triage;")
    P("  · no molecule designed; no dose, potency, selectivity, or efficacy stated;")
    P("  · the substrate gives only the FAILURE-MODE CLASS (which R19 primitive fails) + the SIGN of a")
    P("    hypothetical restorative lever — the absolute magnitude is an [O] this volume does NOT supply;")
    P("  · the odorant-identity layer remains the named [O] (E1: binding-pocket chemistry);")
    P("  · the felt EXPERIENCE of anosmia (and of smelling) belongs to the mind volume, cited not re-derived.")

    # ------------------------------------------------------------------------------------------
    # grades + learned
    # ------------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E4 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : congenital anosmia falls into exactly the substrate's TWO R19 failure modes —")
    P("                 the transduction switch can't flip (CNG channelopathy) or the organ can't form")
    P("                 (Kallmann); CNGB1's two-sense impairment is forced by the shared primitive.")
    P("  [V] verified : the WT CNG switch flips past h* and deleting the switch destroys the flip")
    P("                 (≥20× steeper); each Kallmann Organ is absent below its presence threshold and")
    P("                 present above it (parts ≠ trait); CNGB1 γ is byte-identical to the rod-vision")
    P("                 sibling. (γ+A4 re-proved offline by verify_seed [3]; PROKR2/PROK2 measured.)")
    P("  [L] measured : every anosmia-gene γ (+A4) from NCBI promoters, cached, byte-identical to atlas")
    P("                 (CNGA2/CNGB1/ANOS1/FGFR1 inherited; PROKR2/PROK2 fetched and folded in at v0.6.0).")
    P("  [O] open     : the ABSOLUTE restorative magnitude / dose / efficacy — DELIBERATELY NOT supplied")
    P("                 (proposal-only); the developmental window; the odorant-identity layer (E1 [O]);")
    P("                 the FELT experience of anosmia (→ mind volume).")
    P("\nLEARNED: congenital anosmia reads cleanly as the substrate's TWO R19 failure modes — the")
    P("         transduction switch failing to flip (CNG channelopathy: CNGA2, CNGB1) or the organ")
    P("         failing to emerge (Kallmann: ANOS1, FGFR1, PROKR2, PROK2). The cross-sense bite is real:")
    P("         CNGB1 is literally rod vision's CNG β (byte-identical γ), so its loss is predicted to")
    P("         impair smell AND dim-light vision together — the shared switch failing twice. Every")
    P("         statement stays direction-only / proposal-only; no dose, molecule, or efficacy is")
    P("         produced. This is the seed's goal layer, reached honestly. Foundation untouched; firewall intact.")


def main():
    buf = io.StringIO()
    def P(*a):
        print(*a); print(*a, file=buf)
    run(P)
    return hashlib.sha256(buf.getvalue().encode()).hexdigest()


if __name__ == "__main__":
    print("\nsha256:", main())
