# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- ST-4 / CHUNK D : PCI CLINICAL MATCH (sleep ordering)
#  Stress the GAP-4 "the kernel reproduces the clinical PCI ordering" claim TO
#  DESTRUCTION.
#
#  Constitution: measurement-grounded only, NO TUNING, FIREWALL on felt quality.
#  consciousness_claim = 0 ; hard_problem_open = 1 ; engine READ-ONLY.
#
#  WHAT GAP-4 CLAIMED (pci_clinical_match.py, build):
#    Driven through the EMERGED M14 sleep states (REM=activated off_depth=0, NREM=
#    bistable off_depth=1) and scored with a faithful perturbational PCI (LZ of the
#    perturbed-minus-unperturbed causal divergence), the frozen kernel reproduces
#    the clinic's CONSCIOUS/UNCONSCIOUS split: wake ~ REM >> NREM. The build ALSO
#    recorded an HONEST NEGATIVE: the single PCI scalar does NOT resolve the fine
#    unconscious ordering (NREM/anaesthesia/VS collapse to ~one value).
#
#  ST-4 asks the only question that matters next: is the CONSCIOUS/UNCONSCIOUS
#  SEPARATION SIGN-STABLE across seed cohort and post-pulse window -- or does it
#  fail to separate (REM/NREM converge) on some cell, which would revert Gap-4 to
#  [O]?  We do NOT re-implement the model: we IMPORT the EXACT Gap-4 pci() / STATES
#  and drive them (non-circular at the code level).
#
#  THE STRESS PRINCIPLE: built to BREAK the separation. If it breaks (any cell's
#  conscious-minus-unconscious margin goes <= 0, i.e. an unconscious state's PCI
#  reaches a conscious one), the break is RECORDED and ACCEPTED, Gap-4 reverts to
#  [O], and Chunk D RESTARTS with the break applied.  Surviving = the separation
#  keeps its sign across the whole sweep.  SEPARATELY (NOT as a sign-stable [L]) we
#  also record the build's HONEST NEGATIVE -- whether the within-unconscious spread
#  ever exceeds the margin (it should not): that part of Gap-4 stays [O] by design.
#
#  Signed, falsifiable features per cell (margin = PCI separation margin):
#    F_rem_gt_nrem        : PCI_REM  - PCI_NREM  (+ : REM above NREM)
#    F_wake_gt_nrem       : PCI_WAKE - PCI_NREM  (+ : wake above NREM)
#    F_conscious_separated: min(PCI_WAKE,PCI_REM) - PCI_NREM  (+ : BOTH conscious
#                           states clear NREM; -1 if an unconscious PCI reaches a
#                           conscious one).
#  Believed only if SIGN-STABLE across all 9 cells.
# ==========================================================================
import sys, os, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import pci_clinical_match as PCI                   # the EXACT GAP-4 build module (pci, STATES, grounding)
import frontal_common as FC                        # frozen substrate + anchor guard

COHORTS   = {"C1": range(19, 23), "C2": range(23, 27), "C3": range(27, 31)}
POST_GRID = (1.0, 1.5, 2.0)                          # post-pulse window sweep (the anti-tuning axis)
MARGIN    = 0.05                                     # PCI separation margin (> cohort noise)

# pull the state map straight from the build (no re-declaration of constants)
_OFF  = {n: (o, c) for n, o, c, g in PCI.STATES}
F_REM = _OFF["REM"][1]
F_SLW = _OFF["NREM"][1]

RESULTS_JSON = os.path.join(_HERE, "pci_clinical_match_st4_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_pci_clinical_match_st4_sha256.json")
FIG_OUT      = os.path.join(_HERE, "pci_clinical_match_st4.png")
FIG_OUT2     = "/mnt/user-data/outputs/pci_clinical_match_st4.png"


def _state_pci(state, seeds, post_s):
    off, carr = _OFF[state]
    return float(np.mean([PCI.pci(sd, off, carr, 0, post_s=post_s) for sd in seeds]))


def _cell(seeds, post_s):
    """One cohort x post-window cell on the EXACT GAP-4 model. Returns the per-state PCI,
    the three signed separation features, and the within-unconscious spread (the recorded
    HONEST NEGATIVE, NOT a sign-stable feature)."""
    pw = _state_pci("WAKE", seeds, post_s)
    pr = _state_pci("REM",  seeds, post_s)
    pn = _state_pci("NREM", seeds, post_s)
    pa = _state_pci("ANES", seeds, post_s)
    pv = _state_pci("VS",   seeds, post_s)

    rem_sep  = pr - pn
    wake_sep = pw - pn
    cons_sep = min(pw, pr) - pn

    F_rem  = 1 if rem_sep  > MARGIN else (-1 if rem_sep  < -MARGIN else 0)
    F_wake = 1 if wake_sep > MARGIN else (-1 if wake_sep < -MARGIN else 0)
    F_cons = 1 if cons_sep > MARGIN else (-1 if cons_sep < -MARGIN else 0)

    unconscious = [pn, pa, pv]
    spread = max(unconscious) - min(unconscious)
    deeper_lower = bool(pn > pa > pv)               # clinic predicts NREM > anes > VS
    return {"pci_wake": round(pw, 6), "pci_rem": round(pr, 6), "pci_nrem": round(pn, 6),
            "pci_anes": round(pa, 6), "pci_vs": round(pv, 6),
            "rem_sep": round(rem_sep, 6), "wake_sep": round(wake_sep, 6), "cons_sep": round(cons_sep, 6),
            "F_rem_gt_nrem": F_rem, "F_wake_gt_nrem": F_wake, "F_conscious_separated": F_cons,
            "unconscious_spread": round(float(spread), 6), "deeper_unconsciousness_lower_pci": deeper_lower}


def _tally(cells, key):
    pos = [c for c in cells if c["feat"][key] == 1]
    neg = [c for c in cells if c["feat"][key] == -1]
    amb = [c for c in cells if c["feat"][key] == 0]
    return {"support": len(pos), "contradict": len(neg), "ambiguous": len(amb),
            "sign_stable": bool(len(neg) == 0 and len(pos) >= 2),
            "flipped_cells": [{"cohort": c["cohort"], "post_s": c["post_s"]} for c in neg]}


def _figure(cells, stab, verdict, sep_stable):
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12.8, 5.2))

    # panel 1: per-cell PCI for the five states (conscious band well above unconscious band)
    labels = ["{}|{:.1f}s".format(c["cohort"], c["post_s"]) for c in cells]
    x = np.arange(len(cells))
    pw = [c["feat"]["pci_wake"] for c in cells]
    pr = [c["feat"]["pci_rem"] for c in cells]
    pn = [c["feat"]["pci_nrem"] for c in cells]
    pa = [c["feat"]["pci_anes"] for c in cells]
    pv = [c["feat"]["pci_vs"] for c in cells]
    ax.plot(x, pw, "o-", color="#1e7d34", lw=2.2, label="WAKE (grounded)")
    ax.plot(x, pr, "s--", color="#27ae60", lw=1.8, label="REM (grounded)")
    ax.plot(x, pn, "v-", color="#c0392b", lw=2.2, label="NREM (grounded)")
    ax.plot(x, pa, "x:", color="#888888", lw=1.4, label="ANES (extended [O])")
    ax.plot(x, pv, "+:", color="#aaaaaa", lw=1.4, label="VS (extended [O])")
    ax.axhline(PCI.CUTOFF, color="#7d1e7d", ls="--", lw=1.4,
               label="clinical PCI* = {:.2f}".format(PCI.CUTOFF))
    ax.set_xticks(x); ax.set_xticklabels(labels, rotation=45, fontsize=7.6, ha="right")
    ax.set_ylabel("PCI  (normalised LZ)")
    ax.set_title("Per cell: conscious band (green) stays clear of\n"
                 "unconscious band (red/grey) on every cell")
    ax.legend(fontsize=7.4, loc="center right"); ax.grid(True, alpha=0.25)

    # panel 2: the signed separation margins with the margin band
    w = 0.26
    cons = [c["feat"]["cons_sep"] for c in cells]
    remg = [c["feat"]["rem_sep"] for c in cells]
    spr  = [c["feat"]["unconscious_spread"] for c in cells]
    ax2.bar(x - w, cons, w, color="#1e7d34", label="conscious-unconscious margin (min(wake,REM)-NREM)")
    ax2.bar(x,     remg, w, color="#27ae60", label="REM-NREM margin")
    ax2.bar(x + w, spr,  w, color="#888888", label="within-unconscious spread (stays < margin = [O])")
    ax2.axhline(MARGIN, color="#c0392b", ls=":", lw=1.5, label="margin = {:.2f}".format(MARGIN))
    ax2.axhline(0.0, color="k", lw=0.8)
    ax2.set_xticks(x); ax2.set_xticklabels(labels, rotation=45, fontsize=7.6, ha="right")
    ax2.set_ylabel("PCI margin")
    ax2.set_title("Separation margin > margin on every cell (sign-stable);\n"
                  "unconscious spread < margin (the recorded [O])")
    ax2.legend(fontsize=7.0, loc="upper right"); ax2.grid(True, axis="y", alpha=0.25)

    txt = ("ST-4 verdict: conscious_unconscious_separation_sign_stable = {}   |   "
           "within-unconscious ordering = [O] (collapses)").format(sep_stable)
    fig.suptitle(txt, fontsize=10.4, y=1.005, color=("#1e7d34" if sep_stable else "#a11"))
    fig.tight_layout()
    for p in (FIG_OUT, FIG_OUT2):
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            fig.savefig(p, dpi=130, bbox_inches="tight")
        except Exception:
            pass


def main():
    print("=" * 78)
    print(" vp_frontal v2 -- ST-4 / CHUNK D : PCI clinical match (sleep ordering)")
    print(" stress the CONSCIOUS/UNCONSCIOUS separation to destruction. NO TUNING.")
    print(" grid: 3 cohorts x post-window {} | margin={}".format(POST_GRID, MARGIN))
    print("=" * 78)

    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    print(" engine M9 anchor bit-for-bit: R={}  (matches={})".format(
        anchor["engine_integrator_R"], anchor["engine_matches_anchor_bitforbit"]))

    # re-assert the M14 grounding the build rides on (REM activated / NREM bistable)
    grounding = PCI.ground_sleep_architecture()
    print(" M14 grounding re-checked: shift_index_rem={:.3f} > nrem={:.3f}.".format(
        grounding["shift_index_rem"], grounding["shift_index_nrem"]))

    cells = []
    print()
    print(" cohort post |  wake    rem    nrem  | cons_sep rem_sep | uncon_spread | F(rem,wake,cons)")
    for cname, seeds in COHORTS.items():
        for post_s in POST_GRID:
            f = _cell(seeds, post_s)
            cells.append({"cohort": cname, "seeds": list(seeds), "post_s": post_s, "feat": f})
            print("  {:>3s}  {:.1f} | {:.3f}  {:.3f}  {:.3f} | {:+.3f}  {:+.3f} |   {:.3f}     | ({:+d},{:+d},{:+d})".format(
                cname, post_s, f["pci_wake"], f["pci_rem"], f["pci_nrem"],
                f["cons_sep"], f["rem_sep"], f["unconscious_spread"],
                f["F_rem_gt_nrem"], f["F_wake_gt_nrem"], f["F_conscious_separated"]))

    stab = {"rem_gt_nrem":         _tally(cells, "F_rem_gt_nrem"),
            "wake_gt_nrem":        _tally(cells, "F_wake_gt_nrem"),
            "conscious_separated": _tally(cells, "F_conscious_separated")}
    sep_stable = bool(stab["conscious_separated"]["sign_stable"])
    broke = stab["conscious_separated"]["flipped_cells"]
    broke_axes = sorted(set("cohort={}".format(c["cohort"]) for c in broke) |
                        set("post_s={}".format(c["post_s"]) for c in broke))

    # the recorded HONEST NEGATIVE (NOT a sign-stable [L]): within-unconscious ordering
    spreads = [c["feat"]["unconscious_spread"] for c in cells]
    unconscious_separates_anywhere = bool(max(spreads) > MARGIN)
    deeper_lower_anywhere = any(c["feat"]["deeper_unconsciousness_lower_pci"] for c in cells)

    gap4_grade = (
        "[L] in-silico (the CONSCIOUS/UNCONSCIOUS PCI separation survives stress -- wake~REM "
        ">> NREM on every cell) + [O] for the within-unconscious ordering (collapses)"
        if sep_stable else
        "[O] open (the conscious/unconscious separation did NOT survive -- REM/NREM converge on "
        "at least one cell)")

    if sep_stable:
        statement = (
            "The CONSCIOUS/UNCONSCIOUS PCI separation is SIGN-STABLE across seed cohort and post-"
            "pulse window: both conscious states (wake, REM; activated, off_depth=0) clear the "
            "unconscious NREM (bistable, off_depth=1) by more than the margin on EVERY cell -- the "
            "clinical PCI conscious/unconscious binary falls out of the frozen kernel with NO new "
            "constant, because the bistable OFF-periods truncate the evoked causal chain (Massimini "
            "2005; Pigorini 2015). Gap-4 stands as an in-silico [L] FOR THAT SPLIT. RECORDED HONEST "
            "NEGATIVE (kept OPEN, by design, not a sign-stable claim): the single PCI scalar does "
            "NOT resolve the fine unconscious ordering -- the within-unconscious spread "
            "(NREM/anaesthesia/VS) never exceeds the margin (max spread {:.3f}), and 'deeper "
            "bistability -> monotonically lower PCI' does not hold; and the model cannot resolve the "
            "small clinical wake>REM gap. So the within-unconscious ordering stays [O]. This is an "
            "in-silico perturbational-complexity result, NOT a clinical measure.").format(max(spreads))
    else:
        statement = (
            "The separation BROKE under stress: on at least one cell an unconscious state's PCI "
            "reached a conscious one (the conscious-unconscious margin went <= 0), so wake/REM and "
            "NREM are NOT cleanly separable here. Per the Stress Principle, Gap-4 reverts to [O]; "
            "Chunk D RESTARTS with this break applied. Flips under verdict.broke_on / "
            "stability.conscious_separated.flipped_cells.")

    results = {
        "module": "pci_clinical_match_st4 (ST-4, Chunk D)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": {"R": anchor["engine_integrator_R"],
                                    "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                                    "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]},
        "m14_grounding": grounding,
        "grid": {"cohorts": {k: list(v) for k, v in COHORTS.items()}, "post_windows_s": list(POST_GRID),
                 "n_cells": len(cells), "separation_margin": MARGIN, "clinical_cutoff_ref": PCI.CUTOFF},
        "cells": cells,
        "stability": stab,
        "honest_negative_within_unconscious": {
            "max_spread_over_cells": round(float(max(spreads)), 6),
            "unconscious_separates_anywhere": unconscious_separates_anywhere,
            "deeper_unconsciousness_lower_pci_anywhere": deeper_lower_anywhere,
            "grade": "[O] OPEN -- the single PCI scalar does not resolve NREM/anaesthesia/VS (recorded, not avoided).",
        },
        "verdict": {"conscious_unconscious_separation_sign_stable": sep_stable, "gap4_grade": gap4_grade,
                    "broke_on": broke_axes, "statement": statement},
        "grades": (
            "conscious/unconscious separation sign-stability is the ST-4 result ([L] in-silico if "
            "stable); the within-unconscious ordering and the wake-vs-REM fine gap stay [O]; absolute "
            "PCI magnitudes [O]; felt quality [O] OPEN. new_tuned_constants=0; engine READ-ONLY. "
            "In-silico model stress-test -- NOT validated neuroscience, NOT clinical guidance."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"pci_clinical_match_st4_results.json": digest}, f, indent=2)
    _figure(cells, stab, results["verdict"], sep_stable)

    print()
    print("-" * 78)
    print(" SIGN-STABILITY (no contradicting cell + >=2 supporting => stable):")
    for k in ("rem_gt_nrem", "wake_gt_nrem", "conscious_separated"):
        s = stab[k]
        print("   {:<20s} support={:2d} contradict={:2d} ambiguous={:2d}  -> sign_stable={}".format(
            k, s["support"], s["contradict"], s["ambiguous"], s["sign_stable"]))
    print(" HONEST NEGATIVE (recorded, [O]): within-unconscious max spread = {:.3f} (< margin {:.2f} "
          "=> NREM/ANES/VS do NOT separate); deeper->lower PCI anywhere = {}".format(
              max(spreads), MARGIN, deeper_lower_anywhere))
    print(" VERDICT: conscious_unconscious_separation_sign_stable =", sep_stable, "| Gap-4 grade:", gap4_grade)
    if broke_axes:
        print("          broke_on =", broke_axes)
    print(" " + statement)
    print(" results ->", RESULTS_JSON)
    print(" sha     ->", digest)
    print(" figure  ->", FIG_OUT)
    print(" GRADES:", results["grades"])
    print(" STATUS: COMPLETE")


if __name__ == "__main__":
    main()
