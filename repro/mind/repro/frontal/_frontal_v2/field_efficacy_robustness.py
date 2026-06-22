# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- ST-1 / CHUNK A : EM-FIELD EFFICACY ROBUSTNESS
#  Stress the GAP-1 "EM-field causal window" TO DESTRUCTION.
#
#  Constitution: physics-derived, NO TUNING, FIREWALL on felt quality.
#  consciousness_claim = 0 ; hard_problem_open = 1 ; engine READ-ONLY.
#
#  WHAT GAP-1 CLAIMED (cognition_consciousness_body.py, Session 1):
#    The ephaptic field has a CAUSAL WINDOW for access (a PCI analog):
#      - field OFF (coupling -> 0)      -> access FLOOR
#      - field at the MEASURED coupling -> access OPEN
#      - field OVER-DRIVEN              -> access COLLAPSES while arousal climbs
#    i.e. a non-monotone PCI(coupling) with an INTERIOR peak, DISSOCIATED from a
#    monotonically-rising arousal (the vegetative/seizure signature).
#    Session 1 already conceded one honest residual: the peak sits ABOVE the
#    measured coupling (~3x), not AT it -- so "criticality at measured" is [O].
#
#  ST-1 asks the only question that matters next: is that WINDOW SIGN-STABLE
#  across (a) seed cohort, (b) duration, and (c) perturbation node -- or is it
#  an operating-point artefact (flips / seed-specific)?  We do NOT re-implement
#  the metric: we import the EXACT GAP-1 pci_analog and drive it (non-circular).
#
#  THE STRESS PRINCIPLE: built to BREAK the window. If it breaks, the break is
#  RECORDED and ACCEPTED, Gap-1 reverts to [O], and the "field is causally
#  necessary" claim is WITHDRAWN (per the v2 handover, S4). Surviving means the
#  window keeps its sign across the whole sweep.
#
#  RUNNER: resumable + wall-clock-budgeted. Each invocation finishes as many
#  cells as fit in BUDGET_S, checkpoints after EVERY cell to _st1_partial.json,
#  and the next invocation resumes. Determinism => cells are call-invariant.
#    usage:  python3 field_efficacy_robustness.py [budget_seconds]
# ==========================================================================
import sys, os, math, json, time
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
sys.path.insert(0, os.path.join(_HERE, "..", "_frontal"))
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
import cognition_consciousness_body as CCB     # the EXACT GAP-1 module (pci_analog)
import frontal_common as FC                     # frozen substrate + anchor guard

# ----- sweep grid (the three ST-1 axes); couplings are MULTIPLES of measured kappa -----
COUPLINGS    = [0.0, 1.0, 2.0, 3.0, 5.0, 8.0]    # OFF / measured / interior / over-drive
COHORTS      = {"C1": list(range(19, 23)), "C2": list(range(23, 27)), "C3": list(range(27, 31))}
DURATIONS    = [0.4, 0.6, 1.0]                    # brackets GAP-1 T=0.6 both sides
NODES        = ["neocortex", "thalamus", "hippocampus", "striatum"]
MEASURED_KS  = 1.0
OVERDRIVE_KS = max(COUPLINGS)                     # 8.0
MARGIN       = 0.012                              # abs-PCI margin (above cohort noise)
BUDGET_S     = 240                                # default per-invocation wall-clock budget

PARTIAL_JSON = os.path.join(_HERE, "_st1_partial.json")
RESULTS_JSON = os.path.join(_HERE, "field_efficacy_robustness_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_field_efficacy_robustness_sha256.json")
FIG_OUT      = "/mnt/user-data/outputs/field_efficacy_robustness.png"


def _curve(seeds, T, node):
    """The EXACT GAP-1 pci_analog across the coupling grid for one cell."""
    ni = FC.idx(node)
    return [[float(ks)] + list(map(float, CCB.pci_analog(ks, seeds=seeds, T=T, perturb_node=ni)))
            for ks in COUPLINGS]


def _features(curve):
    ks  = [c[0] for c in curve]; pci = [c[1] for c in curve]; act = [c[2] for c in curve]
    pos = [i for i, k in enumerate(ks) if k > 0.0]
    i_off, i_meas, i_over = ks.index(0.0), ks.index(MEASURED_KS), ks.index(OVERDRIVE_KS)
    off_pci, meas_pci, over_pci = pci[i_off], pci[i_meas], pci[i_over]
    peak_i = max(pos, key=lambda i: pci[i]); peak_ks, peak_pci = ks[peak_i], pci[peak_i]
    interior_peak = bool(peak_ks < OVERDRIVE_KS)
    act_pos = [act[i] for i in pos]
    act_monotone_up = all(act_pos[j + 1] >= act_pos[j] - 1e-4 for j in range(len(act_pos) - 1))
    collapse_mag  = float(peak_pci - over_pci)
    necessity_mag = float(meas_pci - off_pci)

    if   necessity_mag >  MARGIN: F_nec = 1
    elif necessity_mag < -MARGIN: F_nec = -1
    else:                          F_nec = 0
    if interior_peak and collapse_mag > MARGIN:                       F_col = 1
    elif (not interior_peak) and (over_pci - meas_pci) > MARGIN:      F_col = -1
    else:                                                             F_col = 0
    if act_monotone_up and interior_peak and collapse_mag > MARGIN:                   F_diss = 1
    elif act_monotone_up and (not interior_peak) and (over_pci - meas_pci) > MARGIN:  F_diss = -1
    else:                                                                             F_diss = 0
    return {"off_pci": round(off_pci, 6), "measured_pci": round(meas_pci, 6),
            "overdrive_pci": round(over_pci, 6), "peak_ks": peak_ks,
            "peak_pci": round(peak_pci, 6), "interior_peak": interior_peak,
            "act_monotone_up": bool(act_monotone_up), "collapse_mag": round(collapse_mag, 6),
            "necessity_mag": round(necessity_mag, 6),
            "F_necessity": F_nec, "F_collapse": F_col, "F_dissociation": F_diss}


def _tally(cells, key):
    pos = [c for c in cells if c["feat"][key] == 1]
    neg = [c for c in cells if c["feat"][key] == -1]
    amb = [c for c in cells if c["feat"][key] == 0]
    return {"support": len(pos), "contradict": len(neg), "ambiguous": len(amb),
            "sign_stable": bool(len(neg) == 0 and len(pos) >= 2),
            "flipped_cells": [{"cohort": c["cohort"], "T": c["T"], "node": c["node"]} for c in neg]}


def _cell_list():
    out = []
    for cname, seeds in COHORTS.items():
        for T in DURATIONS:
            for node in NODES:
                out.append((cname, seeds, T, node))
    return out


def _load_partial():
    if os.path.exists(PARTIAL_JSON):
        with open(PARTIAL_JSON) as f:
            return json.load(f)
    return {"baseline": None, "cells": {}}


def _save_partial(state):
    with open(PARTIAL_JSON, "w") as f:
        json.dump(state, f)


def _finalize(state):
    cells = []
    for cname, seeds, T, node in _cell_list():
        key = "{}|{}|{}".format(cname, T, node)
        rec = state["cells"][key]
        cells.append({"cohort": cname, "seeds": seeds, "T": T, "node": node,
                      "curve": rec["curve"], "feat": rec["feat"]})
    base_curve = state["baseline"]["curve"]; base_feat = state["baseline"]["feat"]
    stab = {"necessity": _tally(cells, "F_necessity"),
            "overdrive_collapse": _tally(cells, "F_collapse"),
            "dissociation": _tally(cells, "F_dissociation")}
    window_sign_stable = bool(stab["overdrive_collapse"]["sign_stable"] and stab["dissociation"]["sign_stable"])
    broke = stab["overdrive_collapse"]["flipped_cells"] + stab["dissociation"]["flipped_cells"]
    broke_axes = sorted(set("cohort={}".format(c["cohort"]) for c in broke) |
                        set("T={}".format(c["T"]) for c in broke) |
                        set("node={}".format(c["node"]) for c in broke))
    gap1_grade = ("[L] in-silico (window survives stress)" if window_sign_stable
                  else "[O] open (window did NOT survive -- field-necessity claim withdrawn)")
    if window_sign_stable:
        statement = ("The EM-field causal WINDOW is SIGN-STABLE across seed, duration, and "
                     "perturbation node: access shows an interior peak with a real over-drive "
                     "collapse while arousal rises monotonically (the dissociation holds). Gap-1 "
                     "stands as an in-silico [L]. HONEST RESIDUAL (unchanged from S1): the peak "
                     "sits ABOVE the measured coupling, so 'criticality AT the measured coupling' "
                     "remains [O]; what survives is the DISSOCIATION, not the location.")
    else:
        statement = ("The window BROKE under stress: the interior-peak / over-drive-collapse "
                     "feature flipped sign on at least one cell. Per the Stress Principle, Gap-1 "
                     "reverts to [O]; the 'field is causally necessary for access' claim is "
                     "WITHDRAWN; Chunk A restarts with this break applied (re-examine the "
                     "coordination layer). Flips under verdict.broke_on / stability.*.flipped_cells.")
    anchor = state["baseline"]["anchor"]
    results = {
        "module": "field_efficacy_robustness (ST-1, Chunk A)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": anchor,
        "grid": {"couplings_x_measured_kappa": COUPLINGS, "measured_kappa": FC.KAP,
                 "omega0": FC.OMEGA0, "cohorts": COHORTS, "durations_s": DURATIONS,
                 "perturb_nodes": NODES, "n_cells": len(cells), "abs_pci_margin": MARGIN},
        "baseline_reproduction": {"operating_point": "seeds 19-26, T=0.6, neocortex",
                                  "curve": base_curve, "features": base_feat},
        "cells": cells, "stability": stab,
        "verdict": {"window_sign_stable": window_sign_stable, "gap1_grade": gap1_grade,
                    "broke_on": broke_axes, "statement": statement},
        "grades": ("PCI/activity are FUNCTIONAL measures [V mechanism]; the window's "
                   "sign-stability is the ST-1 result; peak-AT-measured stays [O]; felt quality "
                   "[O] OPEN. new_tuned_constants=0; engine READ-ONLY."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"field_efficacy_robustness_results.json": digest}, f, indent=2)
    _figure(cells, base_curve, stab, results["verdict"])
    if os.path.exists(PARTIAL_JSON):
        os.remove(PARTIAL_JSON)

    print("=" * 78)
    print(" ST-1 / CHUNK A -- COMPLETE")
    print("=" * 78)
    print(" baseline: peak_ks={} peak_pci={:.4f} off={:.4f} measured={:.4f} overdrive={:.4f}".format(
        base_feat["peak_ks"], base_feat["peak_pci"], base_feat["off_pci"],
        base_feat["measured_pci"], base_feat["overdrive_pci"]))
    print(" SIGN-STABILITY (no contradicting cell + >=2 supporting => stable):")
    for k in ("necessity", "overdrive_collapse", "dissociation"):
        s = stab[k]
        print("   {:<20s} support={:2d} contradict={:2d} ambiguous={:2d}  -> sign_stable={}".format(
            k, s["support"], s["contradict"], s["ambiguous"], s["sign_stable"]))
    print(" VERDICT: window_sign_stable =", window_sign_stable, "| Gap-1 grade:", gap1_grade)
    if broke_axes:
        print("          broke_on =", broke_axes)
    print(" " + statement)
    print(" results ->", RESULTS_JSON)
    print(" sha     ->", digest)
    print(" figure  ->", FIG_OUT)
    print(" GRADES:", results["grades"])
    print(" STATUS: COMPLETE")


def run(budget_s):
    t0 = time.time()
    state = _load_partial()

    # engine-invariance guard (every invocation)
    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    anchor_rec = {"R": anchor["engine_integrator_R"],
                  "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                  "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]}

    if state["baseline"] is None:
        print("[baseline] reproducing GAP-1 operating point (seeds 19-26, T=0.6, neocortex)...", flush=True)
        bc = _curve(list(range(19, 27)), 0.6, "neocortex")
        state["baseline"] = {"curve": bc, "feat": _features(bc), "anchor": anchor_rec}
        _save_partial(state)
        print("[baseline] done ({:.1f}s)".format(time.time() - t0), flush=True)

    cells = _cell_list()
    total = len(cells)
    done0 = len(state["cells"])
    for cname, seeds, T, node in cells:
        key = "{}|{}|{}".format(cname, T, node)
        if key in state["cells"]:
            continue
        if time.time() - t0 > budget_s:
            break
        tc = time.time()
        curve = _curve(seeds, T, node)
        feat = _features(curve)
        state["cells"][key] = {"curve": curve, "feat": feat}
        _save_partial(state)
        print("  [{:2d}/{:2d}] {:>3s} T={:.1f} {:<11s} peak_ks={} col={:+.4f} nec={:+.4f} "
              "F(nec,col,diss)=({:+d},{:+d},{:+d}) [{:.1f}s]".format(
                  len(state["cells"]), total, cname, T, node, feat["peak_ks"],
                  feat["collapse_mag"], feat["necessity_mag"],
                  feat["F_necessity"], feat["F_collapse"], feat["F_dissociation"],
                  time.time() - tc), flush=True)

    ndone = len(state["cells"])
    if ndone >= total:
        _finalize(state)
    else:
        print("STATUS: INCOMPLETE {}/{} cells (+{} this call, {:.1f}s). Re-run to continue.".format(
            ndone, total, ndone - done0, time.time() - t0), flush=True)


def _figure(cells, base_curve, stab, verdict):
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.2)); ax, ax2 = axes
    ks = COUPLINGS
    for c in cells:
        ax.plot(ks, [p[1] for p in c["curve"]], "-", color="#bbbbbb", lw=0.7, alpha=0.5, zorder=1)
    dur_colors = {0.4: "#27ae60", 0.6: "#c0392b", 1.0: "#8e44ad"}
    for T, col in dur_colors.items():
        sub = [c for c in cells if c["T"] == T]
        if not sub: continue
        mean = np.mean([[p[1] for p in c["curve"]] for c in sub], axis=0)
        ax.plot(ks, mean, "o-", color=col, lw=2.6, zorder=3, label="mean PCI  T={:.1f}s".format(T))
    ax.plot(ks, [p[1] for p in base_curve], "k^--", lw=1.6, alpha=0.8, zorder=4,
            label="GAP-1 baseline (T=0.6, 8 seeds)")
    ax.axvline(MEASURED_KS, color="k", ls=":", lw=1.4)
    yl = ax.get_ylim()
    ax.annotate("measured\ncoupling", (MEASURED_KS, yl[1]), fontsize=8.5,
                xytext=(MEASURED_KS + 0.25, yl[1] - 0.03 * (yl[1] - yl[0])), va="top")
    ax.set_xlabel("coupling scale  (x measured kappa = {:.4f})".format(FC.KAP))
    ax.set_ylabel("PCI analog  (access / 'consciousness')")
    ax.set_title("Access window vs field strength\n(interior peak + over-drive collapse = the window)")
    ax.legend(fontsize=8, loc="lower center"); ax.grid(True, alpha=0.25)
    for c in cells:
        ax2.plot(ks, [p[2] for p in c["curve"]], "-", color="#cdd7e0", lw=0.7, alpha=0.6, zorder=1)
    for T, col in dur_colors.items():
        sub = [c for c in cells if c["T"] == T]
        if not sub: continue
        mean = np.mean([[p[2] for p in c["curve"]] for c in sub], axis=0)
        ax2.plot(ks, mean, "s--", color=col, lw=2.4, zorder=3, label="mean arousal  T={:.1f}s".format(T))
    ax2.set_xlabel("coupling scale  (x measured kappa)")
    ax2.set_ylabel("activity  (coherence / 'arousal')")
    ax2.set_title("Arousal rises monotonically as access turns over\n= the vegetative/seizure dissociation")
    ax2.legend(fontsize=8, loc="upper left"); ax2.grid(True, alpha=0.25)
    txt = ("ST-1 verdict: window_sign_stable = {}   |   collapse stable={}  "
           "dissociation stable={}  necessity stable={}").format(
        verdict["window_sign_stable"], stab["overdrive_collapse"]["sign_stable"],
        stab["dissociation"]["sign_stable"], stab["necessity"]["sign_stable"])
    fig.suptitle(txt, fontsize=10.5, y=1.005,
                 color=("#1e7d34" if verdict["window_sign_stable"] else "#a11"))
    fig.tight_layout(); fig.savefig(FIG_OUT, dpi=130, bbox_inches="tight")


if __name__ == "__main__":
    budget = float(sys.argv[1]) if len(sys.argv) > 1 else BUDGET_S
    run(budget)
