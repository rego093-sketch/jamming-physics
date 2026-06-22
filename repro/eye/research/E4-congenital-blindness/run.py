#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research/E4-congenital-blindness/run.py — INCREMENT E4: congenital blindness (the goal).

  ┌──────────────────────────────────────────────────────────────────────────────────────────┐
  │ SCOPE — THEORETICAL, NON-CLINICAL (read first; binding, FIREWALL.md / BLUEPRINT.md).        │
  │ This is purely academic dynamical-systems research. It does NOT diagnose, treat, prescribe, │
  │ screen, or triage; it designs NO molecule and states NO dose, potency, selectivity, or       │
  │ efficacy. The congenital-blindness layer is DIRECTION-ONLY and PROPOSAL-ONLY, behind a       │
  │ machine-checked MAGNITUDE FIREWALL (main() asserts the entire output carries no quantitative │
  │ clinical token). The felt percept of sight is deferred to the mind volume.                   │
  └──────────────────────────────────────────────────────────────────────────────────────────┘

WHAT E4 DOES (BLUEPRINT.md E4; research/E4-congenital-blindness/START_HERE.md).
  Read each congenital-blindness master gene — GUCY2D (LCA1), RPE65 (LCA2), AIPL1 (LCA4),
  RPGR (X-linked RP), PDE6B (RP), CNGB3 (achromatopsia), every γ MEASURED from NCBI — from the
  FROZEN R19 substrate as a single, shared FAILURE MODE: a loss-of-function lesion means the
  effective drive to the transduction switch can no longer reach the switch's own threshold, so
  the all-or-none flip established in E2 NEVER FIRES — no transduction. The whole increment is the
  E2 single-photon switch read in reverse: E2 showed one quantum of drive across the spinodal h*
  flips the switch; E4 shows that when the drive cannot clear h*, the switch is stuck dark.

  Three things, built ONLY on the frozen inherited foundation (the same R19 field and the same
  MEASURED γ — no new dynamics, nothing fitted):

    PART A — LOSS-OF-FUNCTION = THE SWITCH HELD BELOW ITS OWN SPINODAL (THE DARK BASIN IS ALL THERE IS).
      For each blindness gene, using its MEASURED γ, the inherited field ds/dt = γ·s − s³ + h
      (vp_substrate.sdot, FROZEN) is settled FROM THE DARK REST BASIN (s0 = −√γ). In health a photon
      delivers a transient drive that CLEARS the gene's spinodal h* = (2/3√3)·γ^1.5 and the switch
      snaps on (s>0 — transduction, exactly E2). A loss-of-function lesion is modelled — abstractly,
      structure-only — as the EFFECTIVE drive falling SHORT of h*: below h* the dark basin is the
      only basin, so the field relaxes back to dark (s<0) and the switch CANNOT FLIP. The healthy↔
      affected difference is nothing but whether the drive clears h*. The flip is forced by the
      saddle-node [F]; that the sub-threshold field stays dark for every gene is verified [V]. The
      absolute photon→drive→firing scale (what a real lesion does to the drive in physical units) is
      a named [O], inherited from E2 — no clinical magnitude is produced.

    PART B — THE SUBSTRATE-INVERSE LEVER: RAISE THE DRIVE PAST h*, OR LOWER h* (DIRECTION-ONLY).
      Because the flip condition is exactly drive ≥ h*(γ), its substrate inverse is FORCED and has
      exactly two directions: (i) RAISE the effective drive back across h* (a restore-the-drive
      direction), or (ii) LOWER the effective switching threshold h* below the residual drive (a
      lower-the-barrier direction). We DEMONSTRATE both as DIRECTIONS on the frozen switch — (i)
      re-supplying drive across h* re-flips it, all-or-none (the same discontinuity as E2); (ii) with
      the residual drive held fixed, a switch whose EFFECTIVE threshold is pushed below that drive
      flips, while at the native threshold it stays dark. We state ONLY the directions. HOW MUCH
      drive, BY WHAT MEANS, WHICH molecule, at WHAT dose — every magnitude is the firewall-blocked
      [O]; nothing is diagnosed, designed, prescribed, or quantified. The felt restoration of sight
      is the mind volume's. The measured γ is NEVER altered — lever (ii) is a hypothetical
      threshold probe (real γ frozen), shown only to expose the second geometric degree of freedom.

    PART C — THE BLINDNESS SWITCHES RANK BY THRESHOLD spinodal(γ); A4 RIDES ORTHOGONAL; γ IS PROMOTER
             CONTEXT, NOT THE LESION (stated outright).
      The six switches order by spinodal(γ) — a STRUCTURAL fragility / rescue-direction ordering
      (the lowest-threshold switch needs the smallest drive deficit to fail and the smallest
      restoration to re-flip). This is a falsifiable property of the switch GEOMETRY, direction-only;
      it is explicitly NOT a clinical severity, prognosis, or onset claim (that would be [O], firewall-
      blocked). Among these six the γ-LEVEL alone already separates every gene (no degeneracy here —
      stated honestly: there is no tie to break), yet each carries a non-trivial A4 SHAPE and the
      closest-γ pair is cleanly separated by that shape — so the DNA-v1.13 discipline "read γ (LEVEL)
      AND A4 (SHAPE), never γ alone" still holds (the canonical γ-collapse is the rod CNG α/β pair
      CNGA1/CNGB1 from E1/E2). And the brutal caveat, NOT papered over: the measured γ is the PROMOTER
      stiffness; almost every congenital-blindness lesion is CODING / downstream, so γ supplies the
      switch's THRESHOLD CONTEXT, not the lesion site. That gap is a named [O], never hidden.

INHERITANCE DISCIPLINE (learned first, per WORK_HANDOVER / INHERITANCE_LEDGER).
  E4 CONSUMES the frozen substrate and the MEASURED atlas; it re-derives nothing and adds no γ.
    - the R19 switch math (sdot/spinodal/barrier/settle/is_on) ← inherited/vp_substrate.py (frozen)
    - γ (LEVEL) + A4 (SHAPE) per blindness gene               ← inherited/organ_gamma.json (MEASURED [L];
                                                                 verify_seed [3] re-proves it offline [V])
  γ is measured, never fitted (FIREWALL #2). γ is promoter STRUCTURE only — never a channel voltage,
  a transduction gain, a current, a potency, a dose, an in-vivo selectivity, or a clinical effect
  (FIREWALL #1); the order parameter s is the abstract R19 field, NOT a photocurrent/voltage/firing
  rate. The disease layer is proposal-only (FIREWALL #3) and the felt percept belongs to the mind
  volume (FIREWALL #4). The lever-(ii) threshold probe below is a hypothetical geometric direction —
  it constructs no biology, alters no measured γ, and forks nothing in the substrate.

GRADES (VP-SPEC C3): [F] forced · [V] verified · [L] measured/calibrated · [O] open (obstacle named).
stdlib only (math); imports the frozen substrate's scalar helpers — pure math, no RNG.
Deterministic: 2× run → identical sha256. Output passes the machine-checked MAGNITUDE FIREWALL.
"""
import os, sys, json, math, hashlib, io

# --- locate the package root cwd-independently, import ONLY the frozen inherited foundation ---
_HERE = os.path.dirname(os.path.abspath(__file__))
PKG   = os.path.dirname(os.path.dirname(_HERE))           # research/E4-… → research → PKG
_INH  = os.path.join(PKG, "inherited")
if _INH not in sys.path:
    sys.path.insert(0, _INH)

from vp_substrate import sdot, spinodal, barrier, settle, is_on   # FROZEN: the R19 switch primitive

ATLAS = json.load(open(os.path.join(_INH, "organ_gamma.json"), encoding="utf-8"))["genes"]

# the congenital-blindness master switches (by atlas node) — stated, not selected to a target.
# Gene→condition-class associations are standard literature [L]: mechanism classes, NOT diagnoses.
BLIND = ("GUCY2D", "RPE65", "AIPL1", "RPGR", "PDE6B", "CNGB3")
BLIND_CLASS = {
    "GUCY2D": "Leber congenital amaurosis 1 (retGC1)",
    "RPE65":  "Leber congenital amaurosis 2 (RPE65)",
    "AIPL1":  "Leber congenital amaurosis 4 (chaperone)",
    "RPGR":   "X-linked retinitis pigmentosa (RPGR)",
    "PDE6B":  "retinitis pigmentosa (rod PDE β)",
    "CNGB3":  "achromatopsia (cone CNG β)",
}

# the substrate's integration grid (the FROZEN settle() defaults) — fixed, not tuned.
N_STEPS, DT = 1500, 0.02

# ---- MAGNITUDE FIREWALL: forbidden quantitative clinical tokens (FIREWALL.md #1/#3) ----
# These are the magnitude concepts the firewall blocks outright (doses, potencies, clinical units).
# main() asserts the ENTIRE run output contains none of them (case-insensitive), plus no "%".
# (The qualitative act-words diagnose/treat/prescribe are governed separately and only NEGATED here.)
MAGNITUDE_BLOCK = (
    "dose", "dosage", "mg/kg", "ic50", "ec50", "µmol", "nmol", "µg", "µm)", "nm)",
    "potency", "efficacy", "selectivity", "diopter", "dioptre", "mmhg",
    "milligram", "microgram", "micromolar", "nanomolar",
)


def rest_basin(g):
    """The dark resting state of the R19 field: the lower well s = −√γ (vp_substrate.settle's s0)."""
    return -math.sqrt(g)


def gamma_for_threshold(h_star):
    """Invert the spinodal h* = (2/3√3)·γ^1.5  →  γ = 3·(h*/2)^(2/3). Used ONLY to build the
    lever-(ii) hypothetical-threshold PROBE; it constructs no biology and alters no measured γ."""
    return 3.0 * (h_star / 2.0) ** (2.0 / 3.0)


def run(P):
    P("=" * 80)
    P("E4 — CONGENITAL BLINDNESS   (the transduction switch that cannot flip; frozen substrate)")
    P("=" * 80)
    P("SCOPE: theoretical, NON-CLINICAL. Direction-only / proposal-only behind the magnitude firewall.")
    P("       No diagnosis, no molecule, no quantity. The felt percept of sight → mind volume.")
    P("consumes (frozen): vp_substrate.sdot/spinodal/barrier/settle/is_on · organ_gamma.json γ+A4")
    P("re-derives: nothing; adds no γ. γ measured, never fitted; γ = promoter STRUCTURE only (firewall).")
    P("the order parameter s is the abstract R19 field — NOT a photocurrent/voltage/firing rate.")
    P("E4 reads E2 in reverse: one quantum across h* flips the switch (E2); a drive that cannot")
    P("clear h* leaves it stuck dark (E4). Same field, same measured γ — the failure is geometric.")

    # ----------------------------------------------------------------------------------------
    # PART A — loss-of-function = the switch held below its own spinodal (only the dark basin exists)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART A — loss-of-function = the R19 switch held BELOW its spinodal: it cannot flip (dark)")
    P("-" * 80)
    P("for each blindness gene: settle the FROZEN field from the dark rest basin (s0=−√γ).")
    P("  healthy:  a photon's drive CLEARS h* (1.15·h*) → snaps on (s>0): transduction (= E2).")
    P("  affected: a loss-of-function lesion ⇒ the EFFECTIVE drive falls short (0.85·h*) → the dark")
    P("            basin is all there is → relaxes back to dark (s<0): the switch CANNOT FLIP.")
    P("  the ONLY difference is whether the drive clears h*. (the lesion→drive magnitude is [O].)")
    P(f"\n  {'gene':7s} {'condition class [L]':36s} {'γ':>7s} {'h*':>7s} "
      f"{'s:healthy':>10s} {'s:affected':>11s} {'flips?':>7s}")
    affected_all_dark = True
    healthy_all_on = True
    for sym in BLIND:
        g = ATLAS[sym]["gamma"]
        hstar = spinodal(g)
        # the substrate recomputes spinodal from γ via the FROZEN formula; the atlas lists the same
        # quantity from full-precision γ then rounded — agree within one γ-rounding unit.
        assert abs(hstar - ATLAS[sym]["spinodal"]) < 2e-4, f"{sym}: spinodal must match atlas (γ-rounding)"
        s0 = rest_basin(g)
        s_heal = settle(g, 1.15 * hstar, s0=s0, n=N_STEPS, dt=DT)    # photon clears h* → on
        s_aff  = settle(g, 0.85 * hstar, s0=s0, n=N_STEPS, dt=DT)    # LOF: drive short of h* → dark
        flips  = s_aff > 0.0
        affected_all_dark &= (s_aff < 0.0)
        healthy_all_on    &= (s_heal > 0.0)
        P(f"  {sym:7s} {BLIND_CLASS[sym]:36s} {g:7.4f} {hstar:7.4f} "
          f"{s_heal:+10.4f} {s_aff:+11.4f} {'on' if flips else 'NO':>7s}")
        assert s_heal > 0.0, f"{sym}: healthy drive (1.15·h*) must flip the switch on (transduction)"
        assert s_aff  < 0.0, f"{sym}: the LOF-attenuated drive (0.85·h*) must leave the switch dark"
    assert healthy_all_on and affected_all_dark, "every gene: healthy flips on, affected stays dark"
    P("  → every blindness switch: clears h* in health (transduction), stuck in the dark basin when")
    P("    the drive falls short — loss-of-function IS 'the switch cannot flip'.  [F] fold · [V] all dark.")

    # show the all-or-none threshold is sharp (flat below h*, jump at h*) on a representative gene
    P("\n[sharp threshold] GUCY2D (LCA1), fine drive sweep — FLAT in the dark below h*, JUMPS at h*:")
    g = ATLAS["GUCY2D"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    prev_on = None; crossed = False
    for frac in (0.80, 0.90, 0.95, 1.00, 1.01, 1.05, 1.15):
        fs = settle(g, frac * hstar, s0=s0, n=N_STEPS, dt=DT)
        on = fs > 0.0
        mark = ""
        if prev_on is not None and on != prev_on:
            mark = "   <<< the flip (all-or-none)"; crossed = True
        P(f"    drive = {frac:.2f}·h* = {frac*hstar:.4f}   final_s = {fs:+.4f}   on={on}{mark}")
        prev_on = on
    assert crossed, "the affected→restored flip must be a discontinuous step across h* (all-or-none)"
    P("    → a drive even slightly short of h* does NOTHING; the transduction is all-or-none. The")
    P("      lesion sits on the 'cannot reach h*' side of this exact fold (structure-only).")

    # ----------------------------------------------------------------------------------------
    # PART B — the substrate-inverse lever: raise the drive past h*, OR lower h* (direction-only)
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART B — the substrate-inverse lever (proposal-only, DIRECTION-ONLY): the two ways back over h*")
    P("-" * 80)
    P("the flip condition is exactly  drive ≥ h*(γ). Its inverse is FORCED and has two directions:")
    P("  (i)  RAISE the effective drive back across h*      (restore-the-drive direction)")
    P("  (ii) LOWER the effective threshold h* below the drive (lower-the-barrier direction)")
    P("we show the DIRECTIONS only. HOW MUCH / BY WHAT MEANS / WHICH agent = the firewall-blocked [O].")

    g = ATLAS["GUCY2D"]["gamma"]; hstar = spinodal(g); s0 = rest_basin(g)
    d_residual = 0.85 * hstar                                  # the affected residual drive (Part A)

    # lever (i): raise the drive — re-supplying drive across h* re-flips the switch, all-or-none
    P(f"\n  lever (i) — raise the drive (GUCY2D, affected residual drive = 0.85·h* = {d_residual:.4f}):")
    restored_i = None
    for frac in (0.85, 0.95, 1.00, 1.05, 1.15):
        fs = settle(g, frac * hstar, s0=s0, n=N_STEPS, dt=DT)
        if fs > 0.0 and restored_i is None:
            restored_i = frac
        P(f"     effective drive {frac:.2f}·h* → final_s = {fs:+.4f}  switch {'ON' if fs>0 else 'dark'}")
    assert restored_i is not None and restored_i >= 1.00, "raising the drive must re-flip only past h*"
    P(f"     → the switch re-flips once the drive crosses h* (here at {restored_i:.2f}·h*), all-or-none.")
    P("       DIRECTION: increase the effective transduction drive toward the gene's own spinodal.")
    P("       MAGNITUDE (how much): [O], firewall-blocked. No agent, no quantity is named.")

    # lever (ii): lower the effective threshold below the FIXED residual drive (real γ untouched)
    P(f"\n  lever (ii) — lower the effective threshold below the FIXED residual drive d={d_residual:.4f}")
    P("     (a hypothetical threshold PROBE; the measured γ is frozen — this only exposes the geometry):")
    flipped_ii = None
    for frac in (1.00, 0.95, 0.90, 0.85, 0.80):
        h_eff = frac * hstar
        g_probe = gamma_for_threshold(h_eff)                  # build a switch with effective threshold h_eff
        fs = settle(g_probe, d_residual, s0=rest_basin(g_probe), n=N_STEPS, dt=DT)
        if fs > 0.0 and flipped_ii is None:
            flipped_ii = frac
        P(f"     effective threshold {frac:.2f}·h* = {h_eff:.4f} → final_s = {fs:+.4f}  "
          f"switch {'ON' if fs>0 else 'dark'}")
    assert flipped_ii is not None and flipped_ii < 0.85 + 1e-9, \
        "lowering the threshold below the residual drive must re-flip the switch"
    P(f"     → with the drive UNCHANGED, the switch flips once its threshold drops below d (here at")
    P(f"       {flipped_ii:.2f}·h* < 0.85·h*). DIRECTION: reduce the effective switching barrier.")
    P("       MAGNITUDE (how far) and the real γ are untouched: [O], firewall-blocked.")
    P("\n  both levers are the SAME fold read two ways (drive ↑ or threshold ↓ until drive ≥ h*). The")
    P("  research aim is this DIRECTION; the felt return of sight is the mind volume's, not derived here.")

    # ----------------------------------------------------------------------------------------
    # PART C — the blindness switches rank by spinodal(γ); A4 orthogonal; γ is promoter CONTEXT [O]
    # ----------------------------------------------------------------------------------------
    P("\n" + "-" * 80)
    P("PART C — the six switches rank by threshold spinodal(γ); A4 rides orthogonal; γ is CONTEXT, not lesion")
    P("-" * 80)
    order = sorted(BLIND, key=lambda s: ATLAS[s]["spinodal"])
    P("ordered by spinodal(γ) — a STRUCTURAL fragility / rescue-direction ordering (lowest threshold")
    P("= smallest drive deficit to fail, smallest restoration to re-flip). NOT a clinical severity/")
    P("prognosis claim (that is [O], firewall-blocked) — purely the switch geometry  [F]:")
    P(f"  {'rank':>4} {'gene':7s} {'condition class [L]':36s} {'γ':>7s} {'h*=spinodal':>11s} "
      f"{'barrier':>8s} {'A4 amp':>7s}")
    for k, sym in enumerate(order, 1):
        g = ATLAS[sym]
        P(f"  {k:4d} {sym:7s} {BLIND_CLASS[sym]:36s} {g['gamma']:7.4f} {g['spinodal']:11.4f} "
          f"{g['barrier']:8.4f} {g['shape_amplitude']:7.5f}")
    # the threshold axis is REAL measured spread — the same axis lever (ii) moves along:
    lo, hi = ATLAS[order[0]], ATLAS[order[-1]]
    P(f"  → the six span a real threshold range h*∈[{lo['spinodal']:.4f}, {hi['spinodal']:.4f}]: the very")
    P(f"    axis lever (ii) moves along. {order[0]} (lowest h*) is the most drive-fragile / most easily")
    P(f"    re-flipped switch; {order[-1]} (highest h*) the stiffest — direction-only, no clinical claim.")

    # honesty: γ-LEVEL alone already separates all six (no tie to break) — stated plainly
    gam3 = {s: round(ATLAS[s]["gamma"], 3) for s in BLIND}
    all_distinct = (len(set(gam3.values())) == len(BLIND))
    P("\n[γ separability — honest] among these six the γ-LEVEL alone separates every gene at 3 decimals")
    P(f"  ({', '.join(f'{s} {gam3[s]:.3f}' for s in order)}): all distinct? {all_distinct}.")
    assert all_distinct, "report honestly: the six blindness γ are all distinct at 3dp (no collapse here)"
    P("  so there is NO γ-tie to break here — reported as it is, not dramatised. (The canonical γ-collapse")
    P("  needing A4 is the rod CNG α/β pair CNGA1/CNGB1 from E1/E2.) But A4 is still read for each gene:")

    # A4 still carries non-trivial orthogonal shape; the closest-γ pair is clearly separated by it
    a, b = order[0], order[1]
    pair = sorted(BLIND, key=lambda s: ATLAS[s]["gamma"])
    closest = min(((pair[i], pair[i+1], abs(ATLAS[pair[i]]["gamma"] - ATLAS[pair[i+1]]["gamma"]))
                   for i in range(len(pair) - 1)), key=lambda t: t[2])
    g1, g2, dgam = closest
    amp1, amp2 = ATLAS[g1]["shape_amplitude"], ATLAS[g2]["shape_amplitude"]
    ratio_amp = max(amp1, amp2) / min(amp1, amp2) if min(amp1, amp2) > 0 else float("inf")
    n_textured = sum(1 for s in BLIND if ATLAS[s]["shape_amplitude"] > 0.0)
    P(f"  all {n_textured}/{len(BLIND)} carry non-trivial A4 SHAPE (γ-alone would discard it). closest-γ pair:")
    P(f"    {g1} (γ={ATLAS[g1]['gamma']:.4f}, A4 amp={amp1:.5f}) vs {g2} (γ={ATLAS[g2]['gamma']:.4f}, "
      f"A4 amp={amp2:.5f}) — Δγ={dgam:.4f}, A4 differs {ratio_amp:.2f}×")
    assert ratio_amp > 1.2, "the closest-γ blindness pair must still differ clearly in A4 shape (orthogonality)"
    P("    → level and shape stay orthogonal: even close-γ genes carry distinct texture. Read γ AND A4.  [V]")

    # the brutal caveat — γ is promoter context, NOT the (coding) lesion site
    P("\n[brutal honesty — γ is CONTEXT, not the lesion]  the measured γ is the PROMOTER stiffness")
    P("  (TSS−2000..+500); almost every congenital-blindness lesion is CODING / downstream of it. So γ")
    P("  supplies the switch's THRESHOLD CONTEXT — the fold the transduction must clear — NOT the lesion")
    P("  itself. Mapping a specific coding lesion onto a Δdrive in physical units is a named [O], inherited")
    P("  from E2's photon→drive scale. This gap is stated outright, never hidden behind the geometry.")

    # ----------------------------------------------------------------------------------------
    # grades + learned
    # ----------------------------------------------------------------------------------------
    P("\n" + "=" * 80)
    P("E4 GRADES (VP-SPEC C3) — honest")
    P("=" * 80)
    P("  [F] forced   : loss-of-function = the field held below the saddle-node h*=spinodal(γ) (only")
    P("                 the dark basin exists → no flip); the substrate-inverse lever has exactly two")
    P("                 directions, raise drive past h* or lower h* below the drive; the six switches'")
    P("                 threshold order = argsort(spinodal(γ)).")
    P("  [V] verified : every blindness switch flips on under a clearing drive and stays dark under the")
    P("                 LOF-attenuated drive; the flip is a discontinuous step across h* (all-or-none);")
    P("                 both lever directions re-flip the frozen switch; the six γ are all distinct at")
    P("                 3dp (no tie) yet each carries A4 shape and the closest-γ pair is A4-separated.")
    P("                 (γ+A4 re-proved offline by verify_seed [3]; the magnitude firewall is checked.)")
    P("  [L] measured : every blindness-gene γ (+A4) from NCBI promoters, cached, byte-identical to atlas.")
    P("  [O] open     : the absolute photon→drive→firing scale and the map from a real (coding) lesion to")
    P("                 a Δdrive (inherited E2 [O]); WHICH lever agent and at WHAT magnitude (firewall-")
    P("                 blocked — none produced); clinical severity/prognosis/onset (firewall-blocked);")
    P("                 the FELT percept and felt restoration of sight (→ mind volume). Each obstacle named.")
    P("\nLEARNED: congenital blindness, on the frozen substrate, is the E2 single-photon switch read in")
    P("         reverse — a transduction switch whose drive can no longer clear its own spinodal, so the")
    P("         all-or-none flip never fires. The cure-DIRECTION is forced by the same fold (push the")
    P("         drive over h*, or lower h* under the drive) and is stated as direction only — no molecule,")
    P("         no quantity, no clinical magnitude, nothing diagnosed. The six switches rank by threshold")
    P("         (geometry, not severity); A4 stays orthogonal to γ; γ is honestly the promoter CONTEXT, not")
    P("         the coding lesion. Foundation untouched; nothing fitted; firewall intact and machine-checked.")


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
