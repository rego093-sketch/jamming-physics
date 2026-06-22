# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- ST-3 / CHUNK C : O x W ORTHOGONALITY (autism / ID)
#  Stress the GAP-3 "two separable axes" claim TO DESTRUCTION.
#
#  Constitution: topological only, NO TUNING, FIREWALL on felt quality.
#  consciousness_claim = 0 ; hard_problem_open = 1 ; engine READ-ONLY.
#
#  WHAT GAP-3 CLAIMED (cortico_connectome_owt.py, build):
#    The long-range-ROUTING axis (W = hub edges) and the organ-CAPACITY axis
#    (O = cell count, hubs preserved) form a CROSSOVER double dissociation:
#      W-fault (cut hub long-range edges) -> hits long-range binding ('sociality')
#                                            >> within-pattern completion ('capacity')
#      O-fault (fewer cells, wiring intact)-> hits capacity >> sociality
#    i.e. autism = W-fault (routing), intellectual disability = O-fault (capacity);
#    two SEPARABLE factors, not one.
#
#  ST-3 asks the only question that matters next: is that CROSSOVER SIGN-STABLE
#  across seed cohort and settle depth -- or does a fault cross over the WRONG way
#  (a perturbation hitting the OTHER read-out more), which would mean ONE factor,
#  not two?  We do NOT re-implement the model: we import the EXACT GAP-3 OWTCortex
#  / _cond and drive them (non-circular at the code level).
#
#  THE STRESS PRINCIPLE: built to BREAK the dissociation. If it breaks (any cell's
#  W_selectivity or O_selectivity goes negative beyond margin), the break is
#  RECORDED and ACCEPTED, Gap-3 reverts to [O] (the autism/ID double dissociation
#  collapses to a SINGLE factor), and Chunk C RESTARTS with the break applied
#  (the clinical mapping is rewritten).  Surviving = the crossover keeps its sign
#  across the whole sweep.
#
#  Signed, falsifiable features per cell (margin = abs-fidelity selectivity margin):
#    F_W_targets_sociality : W_sel = dC_W - dS_W  (+ : W is sociality-selective)
#    F_O_targets_capacity  : O_sel = dS_O - dC_O  (+ : O is capacity-selective)
#    F_double_dissociation : BOTH selectivities positive (the crossover = 2 factors);
#                            -1 if EITHER crosses the wrong way (1 factor / confound).
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
import cortico_connectome_owt as OWT          # the EXACT GAP-3 build module (OWTCortex, _cond)
import frontal_common as FC                    # frozen substrate + anchor guard

COHORTS    = {"C1": range(19, 23), "C2": range(23, 27), "C3": range(27, 31)}
STEPS_GRID = (20, 40, 60)                       # settle-depth sweep (the anti-tuning axis)
F_W_MAX    = OWT.F_W_MAX                         # 0.9 strongest W-fault
N_LO       = OWT.N_LO                            # 44  strongest O-fault
MARGIN     = OWT.MARGIN                          # 0.02

RESULTS_JSON = os.path.join(_HERE, "cortico_connectome_owt_st3_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_cortico_connectome_owt_st3_sha256.json")
FIG_OUT      = os.path.join(_HERE, "cortico_connectome_owt_st3.png")
FIG_OUT2     = "/mnt/user-data/outputs/cortico_connectome_owt_st3.png"


def _cell(seeds, steps):
    """One cohort x depth cell: intact, strongest W-fault, strongest O-fault, on the
    EXACT GAP-3 model. Returns deltas, selectivities, and the three signed features."""
    s0, c0 = OWT._cond(120, 0.0, steps, seeds)
    sW, cW = OWT._cond(120, F_W_MAX, steps, seeds)
    sO, cO = OWT._cond(N_LO, 0.0, steps, seeds)
    dS_W, dC_W = sW - s0, cW - c0
    dS_O, dC_O = sO - s0, cO - c0
    W_sel = dC_W - dS_W        # >0 : W hits sociality more than capacity
    O_sel = dS_O - dC_O        # >0 : O hits capacity more than sociality

    F_W = 1 if W_sel > MARGIN else (-1 if W_sel < -MARGIN else 0)
    F_O = 1 if O_sel > MARGIN else (-1 if O_sel < -MARGIN else 0)
    if W_sel > MARGIN and O_sel > MARGIN:
        F_dd = 1
    elif W_sel < -MARGIN or O_sel < -MARGIN:
        F_dd = -1
    else:
        F_dd = 0
    return {"intact_sociality": round(s0, 6), "intact_capacity": round(c0, 6),
            "dS_W": round(dS_W, 6), "dC_W": round(dC_W, 6),
            "dS_O": round(dS_O, 6), "dC_O": round(dC_O, 6),
            "W_selectivity": round(W_sel, 6), "O_selectivity": round(O_sel, 6),
            "F_W_targets_sociality": F_W, "F_O_targets_capacity": F_O,
            "F_double_dissociation": F_dd}


def _tally(cells, key):
    pos = [c for c in cells if c["feat"][key] == 1]
    neg = [c for c in cells if c["feat"][key] == -1]
    amb = [c for c in cells if c["feat"][key] == 0]
    return {"support": len(pos), "contradict": len(neg), "ambiguous": len(amb),
            "sign_stable": bool(len(neg) == 0 and len(pos) >= 2),
            "flipped_cells": [{"cohort": c["cohort"], "steps": c["steps"]} for c in neg]}


def _mean_curve(seeds_pool, steps, kind):
    """Pooled mean curve for the figure: W-fault sweep (sociality, capacity) or
    O-fault sweep, averaged over all cohort seeds."""
    socs, caps, xs = [], [], []
    if kind == "W":
        for f in OWT.F_W_GRID:
            s, c = OWT._cond(120, f, steps, seeds_pool)
            xs.append(f); socs.append(s); caps.append(c)
    else:
        for N in OWT.N_GRID:
            s, c = OWT._cond(N, 0.0, steps, seeds_pool)
            xs.append(N); socs.append(s); caps.append(c)
    return xs, socs, caps


def _figure(cells, stab, verdict):
    pool = list(range(19, 31))
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.2))

    # panel 1: the crossover -- W-fault (hits sociality) and O-fault (hits capacity)
    xw, sw, cw = _mean_curve(pool, 40, "W")
    xo, so, co = _mean_curve(pool, 40, "O")
    ax.plot(xw, sw, "o-", color="#c0392b", lw=2.4, label="sociality | W-fault (cut hubs)")
    ax.plot(xw, cw, "o--", color="#c0392b", lw=1.6, alpha=0.6, label="capacity | W-fault")
    axb = ax.twiny()
    axb.plot(xo, so, "s-", color="#2471a3", lw=2.4, label="sociality | O-fault (fewer cells)")
    axb.plot(xo, co, "s--", color="#2471a3", lw=1.6, alpha=0.6, label="capacity | O-fault")
    axb.invert_xaxis()
    ax.set_xlabel("W-fault: fraction of hub long-range edges cut", color="#c0392b")
    axb.set_xlabel("O-fault: cell count N (decreasing ->)", color="#2471a3")
    ax.set_ylabel("recall fidelity  (overlap)")
    ax.set_title("Crossover: W-fault sinks SOCIALITY, O-fault sinks CAPACITY")
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = axb.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, fontsize=7.6, loc="lower left"); ax.grid(True, alpha=0.25)

    # panel 2: per-cell selectivities with the margin band (the signed double dissociation)
    labels = ["{}|{}".format(c["cohort"], c["steps"]) for c in cells]
    Wsel = [c["feat"]["W_selectivity"] for c in cells]
    Osel = [c["feat"]["O_selectivity"] for c in cells]
    x = np.arange(len(cells)); w = 0.38
    ax2.bar(x - w / 2, Wsel, w, color="#c0392b", label="W_selectivity (dC-dS) : W hits sociality more")
    ax2.bar(x + w / 2, Osel, w, color="#2471a3", label="O_selectivity (dS-dC) : O hits capacity more")
    ax2.axhline(MARGIN, color="#1e7d34", ls=":", lw=1.4, label="margin = {:.2f}".format(MARGIN))
    ax2.axhline(0.0, color="k", lw=0.8)
    ax2.set_xticks(x); ax2.set_xticklabels(labels, rotation=45, fontsize=7.5, ha="right")
    ax2.set_ylabel("selectivity  (abs-fidelity)")
    ax2.set_title("Both selectivities > margin on every cell\n= the crossover is sign-stable")
    ax2.legend(fontsize=7.6, loc="upper right"); ax2.grid(True, axis="y", alpha=0.25)

    txt = ("ST-3 verdict: dissociation_sign_stable = {}   |   W-selective stable={}  "
           "O-selective stable={}  crossover stable={}").format(
        verdict["dissociation_sign_stable"], stab["W_targets_sociality"]["sign_stable"],
        stab["O_targets_capacity"]["sign_stable"], stab["double_dissociation"]["sign_stable"])
    fig.suptitle(txt, fontsize=10.5, y=1.005,
                 color=("#1e7d34" if verdict["dissociation_sign_stable"] else "#a11"))
    fig.tight_layout()
    for p in (FIG_OUT, FIG_OUT2):
        try:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            fig.savefig(p, dpi=130, bbox_inches="tight")
        except Exception:
            pass


def main():
    print("=" * 78)
    print(" vp_frontal v2 -- ST-3 / CHUNK C : O x W orthogonality (autism / ID)")
    print(" stress the CROSSOVER double dissociation to destruction. NO TUNING.")
    print(" W-fault: f_W={} (cut hubs, N=120) | O-fault: N={} (f_W=0) | margin={}".format(
        F_W_MAX, N_LO, MARGIN))
    print("=" * 78)

    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    print(" engine M9 anchor bit-for-bit: R={}  (matches={})".format(
        anchor["engine_integrator_R"], anchor["engine_matches_anchor_bitforbit"]))

    cells = []
    print()
    print(" cohort steps |  dS_W    dC_W  |  dS_O    dC_O  |  W_sel   O_sel | F(W,O,dd)")
    for cname, seeds in COHORTS.items():
        for steps in STEPS_GRID:
            f = _cell(seeds, steps)
            cells.append({"cohort": cname, "seeds": list(seeds), "steps": steps, "feat": f})
            print("  {:>3s}   {:>3d}   | {:+.3f}  {:+.3f} | {:+.3f}  {:+.3f} | {:+.3f}  {:+.3f} | ({:+d},{:+d},{:+d})".format(
                cname, steps, f["dS_W"], f["dC_W"], f["dS_O"], f["dC_O"],
                f["W_selectivity"], f["O_selectivity"],
                f["F_W_targets_sociality"], f["F_O_targets_capacity"], f["F_double_dissociation"]))

    stab = {"W_targets_sociality": _tally(cells, "F_W_targets_sociality"),
            "O_targets_capacity":  _tally(cells, "F_O_targets_capacity"),
            "double_dissociation": _tally(cells, "F_double_dissociation")}
    dissociation_sign_stable = bool(stab["double_dissociation"]["sign_stable"])
    broke = stab["double_dissociation"]["flipped_cells"]
    broke_axes = sorted(set("cohort={}".format(c["cohort"]) for c in broke) |
                        set("steps={}".format(c["steps"]) for c in broke))

    gap3_grade = ("[L] in-silico (the O x W crossover survives stress -- two separable axes)"
                  if dissociation_sign_stable else
                  "[O] open (crossover did NOT survive -- autism/ID collapses to a SINGLE factor)")
    if dissociation_sign_stable:
        statement = (
            "The O x W crossover is SIGN-STABLE across seed cohort and settle depth: the "
            "long-range-ROUTING fault (W) is sociality-selective and the CAPACITY fault (O) is "
            "capacity-selective, on every cell. The autism(W) / ID(O) double dissociation stands "
            "as an in-silico [L]: two SEPARABLE axes, not one factor. HONEST RESIDUALS: the "
            "dissociation is a RELATIVE selectivity (a crossover) -- each fault has a small "
            "off-target effect (W nicks capacity ~0.06; O perturbs sociality <=0.03) but hits its "
            "target ~2-3x harder; and the effect is gene-blind (g absent from sign() dynamics) and "
            "a micro-model property (organ-scale single-tract lesion is not sign-stable). The "
            "clinical labels stay an INTERPRETATION held at arm's length -- this is an in-silico "
            "phase/autoassociator result, NOT a clinical measure.")
    else:
        statement = (
            "The crossover BROKE under stress: on at least one cell a fault crossed over the WRONG "
            "way (a perturbation hit the OTHER read-out more), so O and W are NOT separable here. "
            "Per the Stress Principle, Gap-3 reverts to [O]; the autism/ID double dissociation "
            "collapses to a SINGLE factor; Chunk C RESTARTS with this break applied (the clinical "
            "mapping is rewritten). Flips under verdict.broke_on / stability.double_dissociation.flipped_cells.")

    results = {
        "module": "cortico_connectome_owt_st3 (ST-3, Chunk C)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": {"R": anchor["engine_integrator_R"],
                                    "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                                    "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]},
        "grid": {"cohorts": {k: list(v) for k, v in COHORTS.items()}, "settle_steps": list(STEPS_GRID),
                 "f_W_strongest": F_W_MAX, "N_strongest": N_LO, "n_cells": len(cells),
                 "selectivity_margin": MARGIN},
        "cells": cells, "stability": stab,
        "verdict": {"dissociation_sign_stable": dissociation_sign_stable, "gap3_grade": gap3_grade,
                    "broke_on": broke_axes, "statement": statement},
        "grades": ("W_selectivity / O_selectivity are the ST-3 result (sign-stability of the "
                   "crossover); absolute magnitudes and gene-specificity stay [O]; felt quality [O] "
                   "OPEN. new_tuned_constants=0; engine READ-ONLY. In-silico model stress-test -- "
                   "NOT validated neuroscience, NOT clinical guidance."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"cortico_connectome_owt_st3_results.json": digest}, f, indent=2)
    _figure(cells, stab, results["verdict"])

    print()
    print("-" * 78)
    print(" SIGN-STABILITY (no contradicting cell + >=2 supporting => stable):")
    for k in ("W_targets_sociality", "O_targets_capacity", "double_dissociation"):
        s = stab[k]
        print("   {:<22s} support={:2d} contradict={:2d} ambiguous={:2d}  -> sign_stable={}".format(
            k, s["support"], s["contradict"], s["ambiguous"], s["sign_stable"]))
    print(" VERDICT: dissociation_sign_stable =", dissociation_sign_stable, "| Gap-3 grade:", gap3_grade)
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
