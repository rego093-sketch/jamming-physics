# -*- coding: utf-8 -*-
# ==========================================================================
#  vp_frontal v2 -- CHUNK B / ST-2 : CORTICAL MICRO-MODEL NON-CIRCULARITY
#  Stress the GAP-2 frontal phenotype TO DESTRUCTION.
#
#  Constitution: NO TUNING, FIREWALL on felt quality. engine READ-ONLY.
#  consciousness_claim = 0 ; hard_problem_open = 1 ; new_tuned_constants = 0.
#
#  WHAT GAP-2 CLAIMED (cortical_microcircuit.py, this chunk's build):
#    An additive cortical micro-model (frozen Hippocampus + cortico-cortical HUB
#    topology + hub-mediated reentrant settle) shows a frontal-specific
#    dissociation: long-range binding collapses under hub-edge loss but is spared
#    under matched random local loss; the gap vanishes on an all-to-all buffer.
#
#  ST-2 asks the two questions the v2 whitepaper (S4) names:
#    (1) NON-CIRCULARITY -- does the phenotype appear in a read-out INDEPENDENT of
#        the perturbed edge? The perturbation is "cut hub edges". A CIRCULAR read-out
#        (sum of hub-edge weights) MUST drop trivially -- that proves nothing. The
#        test is whether the BEHAVIOURAL read-out (distant-block recovery, a function
#        of the settled network state, not the severed edges) ALSO shows the gap,
#        and whether it exceeds the all-to-all (no-hub) control (=> topology, not
#        edge-cutting per se).
#    (2) SET-SHIFTING under a DURATION SWEEP -- is the hub-lesion perseveration
#        increase SIGN-STABLE across the settle-duration sweep, or does it flip
#        (the F1 lesson: a clean signal at one operating point flipped under a
#        duration sweep)?
#
#  We do NOT re-implement the model: we import the EXACT CorticalMicrocircuit and
#  drive it (non-circular at the code level too).
#
#  THE STRESS PRINCIPLE: built to BREAK the phenotype. If the behavioural gap
#  vanishes (phenotype was only in the circular read-out) OR the set-shift effect
#  flips sign across durations, the break is RECORDED and ACCEPTED: per the v2
#  handover (S4), the additive micro-model is judged INSUFFICIENT and the fork
#  "resolve cortex INSIDE the kernel (breaks M9)" is put on the table. Surviving
#  means the phenotype keeps its sign in the non-circular read-out across the sweep.
#    usage:  python3 cortical_microcircuit_st2.py
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
import frontal_common as FC                                   # anchor guard + digest
from cortical_microcircuit import CorticalMicrocircuit, FRACS, K, FOXG1, N_CELLS  # EXACT model

# ----- ST-2 grid (mirrors ST-1's cohort structure) -----
COHORTS   = {"C1": list(range(19, 23)), "C2": list(range(23, 27)), "C3": list(range(27, 31))}
DURATIONS = [20, 40, 60]                 # settle-step budget for the set-shift (anti-tuning)
LESION_SEEDS = list(range(3))
MARGIN = 0.01                            # absolute overlap margin (gaps reach ~0.13, ~0.10)

RESULTS_JSON = os.path.join(_HERE, "cortical_microcircuit_st2_results.json")
EXPECTED_SHA = os.path.join(_HERE, "expected_cortical_microcircuit_st2_sha256.json")
FIG_OUT      = "/mnt/user-data/outputs/cortical_microcircuit_st2.png"


# --------------------------------------------------------------------------
#  Per-cohort BINDING gap (non-circular) + its all-to-all control + the
#  CIRCULAR read-out (hub-edge weight sum) shown only to contrast.
# --------------------------------------------------------------------------
def binding_profile(seeds, all_to_all=False):
    """Mean (rand_cut - hub_cut) distant-block recovery over the matched-fraction
    sweep, seed-averaged. NON-CIRCULAR: scored on the free distant bits."""
    gaps = []
    for f in FRACS:
        hub_v, rand_v = [], []
        for ps in seeds:
            mc = CorticalMicrocircuit(topo_seed=ps, all_to_all=all_to_all).write_items(K, ps)
            k = int(round(f * min(len(mc.hub_pool), len(mc.loc_pool))))
            for ls in LESION_SEEDS:
                seed = ls * 101 + ps
                hub_v.append(mc.far_binding(mc.cut(mc.hub_pool, k, seed)))
                rand_v.append(mc.far_binding(mc.cut(mc.loc_pool, k, seed)))
        gaps.append(float(np.mean(rand_v) - np.mean(hub_v)))
    return float(np.mean([g for g, fr in zip(gaps, FRACS) if fr > 0])), gaps


def circular_readout(seeds, frac=0.6):
    """The CIRCULAR control: fraction of hub-incident edge WEIGHT removed by a hub
    cut vs a matched random cut. This is a direct function of the severed edge and
    MUST drop for the hub cut -- included to make the contrast explicit, NOT used
    as a feature."""
    hub_drop, rand_drop = [], []
    for ps in seeds:
        mc = CorticalMicrocircuit(topo_seed=ps, all_to_all=False).write_items(K, ps)
        k = int(round(frac * min(len(mc.hub_pool), len(mc.loc_pool))))
        Wbase = mc.W
        hub_mass = float(np.sum(np.abs(Wbase[mc.ishub, :])))
        for ls in LESION_SEEDS:
            seed = ls * 101 + ps
            Wh = mc.cut(mc.hub_pool, k, seed); Wr = mc.cut(mc.loc_pool, k, seed)
            hub_drop.append(1.0 - float(np.sum(np.abs(Wh[mc.ishub, :]))) / (hub_mass + 1e-12))
            rand_drop.append(1.0 - float(np.sum(np.abs(Wr[mc.ishub, :]))) / (hub_mass + 1e-12))
    return {"hub_cut_hubmass_drop": float(np.mean(hub_drop)),
            "rand_cut_hubmass_drop": float(np.mean(rand_drop))}


# --------------------------------------------------------------------------
#  Micro SET-SHIFT: establish attractor A, cue B on the near block, hold for
#  `dur` settle steps, measure perseveration = distant block still on A.
#  NON-CIRCULAR: scored on the FREE distant block, not the cued/severed edges.
# --------------------------------------------------------------------------
def setshift_perseveration(seeds, dur, lesion):
    left = np.arange(0, N_CELLS // 2); right = np.arange(N_CELLS // 2, N_CELLS)
    vals = []
    for ps in seeds:
        mc = CorticalMicrocircuit(topo_seed=ps, all_to_all=False).write_items(K, ps)
        k = int(round(0.5 * min(len(mc.hub_pool), len(mc.loc_pool))))
        A, B = mc.stored[0], mc.stored[1]
        for ls in LESION_SEEDS:
            W = mc.cut(mc.hub_pool, k, ls * 101 + ps) if lesion else mc.W
            sA = mc._settle(A.copy(), clamp=None, steps=60, W=W)            # establish A on this W
            sB = mc._settle(sA.copy(), clamp=(left, B[left]), steps=dur, W=W)  # switch B on near block
            vals.append(float(np.mean(sB[right] == A[right])))         # distant block still A?
    return float(np.mean(vals))


def _cell_features(coh_bind, coh_bind_aa, persev_intact, persev_hub):
    bind_gap = coh_bind
    topo_excess = coh_bind - coh_bind_aa
    persev_delta = persev_hub - persev_intact
    F_nc  = 1 if bind_gap     >  MARGIN else (-1 if bind_gap     < -MARGIN else 0)
    F_top = 1 if topo_excess  >  MARGIN else (-1 if topo_excess  < -MARGIN else 0)
    F_ss  = 1 if persev_delta >  MARGIN else (-1 if persev_delta < -MARGIN else 0)
    return {"bind_gap": round(bind_gap, 6), "topo_excess": round(topo_excess, 6),
            "persev_intact": round(persev_intact, 6), "persev_hub": round(persev_hub, 6),
            "persev_delta": round(persev_delta, 6),
            "F_noncircular": F_nc, "F_topological": F_top, "F_setshift": F_ss}


def _tally(cells, key):
    pos = [c for c in cells if c["feat"][key] == 1]
    neg = [c for c in cells if c["feat"][key] == -1]
    amb = [c for c in cells if c["feat"][key] == 0]
    return {"support": len(pos), "contradict": len(neg), "ambiguous": len(amb),
            "sign_stable": bool(len(neg) == 0 and len(pos) >= 2),
            "flipped_cells": [{"cohort": c["cohort"], "dur": c["dur"]} for c in neg]}


def main():
    print("=" * 78)
    print(" vp_frontal v2 -- CHUNK B / ST-2 : cortical micro-model NON-CIRCULARITY")
    print(" stress the GAP-2 frontal phenotype to destruction. NO TUNING. engine READ-ONLY.")
    print("=" * 78)

    anchor = FC.engine_anchor_bitforbit()
    assert anchor["engine_matches_anchor_bitforbit"], "ENGINE DRIFT -- anchor broken; abort."
    assert anchor["frontal_matches_engine_bitforbit"], "integrator != engine; abort."
    print(" engine M9 anchor bit-for-bit: R={}  (matches={})".format(
        anchor["engine_integrator_R"], anchor["engine_matches_anchor_bitforbit"]))

    # per-cohort binding profiles (non-circular) + all-to-all control + circular contrast
    coh_bind, coh_bind_aa, coh_circular = {}, {}, {}
    coh_bind_curve = {}
    for cname, seeds in COHORTS.items():
        b, curve = binding_profile(seeds, all_to_all=False)
        baa, _ = binding_profile(seeds, all_to_all=True)
        coh_bind[cname], coh_bind_aa[cname] = b, baa
        coh_bind_curve[cname] = curve
        coh_circular[cname] = circular_readout(seeds)
        print("  {}: behavioural bind-gap={:+.4f}  all-to-all control={:+.4f}  "
              "(circular hub-mass drop hub={:.3f} vs rand={:.3f})".format(
                  cname, b, baa, coh_circular[cname]["hub_cut_hubmass_drop"],
                  coh_circular[cname]["rand_cut_hubmass_drop"]))

    # cells = cohort x duration; set-shift perseveration per duration
    cells = []
    print()
    print(" SET-SHIFT perseveration (distant block still on A after switch) vs duration:")
    for cname, seeds in COHORTS.items():
        for dur in DURATIONS:
            pin = setshift_perseveration(seeds, dur, lesion=False)
            phb = setshift_perseveration(seeds, dur, lesion=True)
            feat = _cell_features(coh_bind[cname], coh_bind_aa[cname], pin, phb)
            cells.append({"cohort": cname, "seeds": seeds, "dur": dur, "feat": feat})
            print("   {} dur={:2d}: intact={:.3f} hub-lesion={:.3f} delta={:+.4f}  "
                  "F(nc,top,ss)=({:+d},{:+d},{:+d})".format(
                      cname, dur, pin, phb, feat["persev_delta"],
                      feat["F_noncircular"], feat["F_topological"], feat["F_setshift"]))

    stab = {"noncircular": _tally(cells, "F_noncircular"),
            "topological": _tally(cells, "F_topological"),
            "setshift":    _tally(cells, "F_setshift")}
    phenotype_sign_stable = bool(stab["noncircular"]["sign_stable"] and
                                 stab["topological"]["sign_stable"] and
                                 stab["setshift"]["sign_stable"])
    broke = (stab["noncircular"]["flipped_cells"] + stab["topological"]["flipped_cells"]
             + stab["setshift"]["flipped_cells"])
    broke_axes = sorted(set("cohort={}".format(c["cohort"]) for c in broke) |
                        set("dur={}".format(c["dur"]) for c in broke))

    if phenotype_sign_stable:
        gap2_grade = "[L] in-silico (additive micro-model yields a non-circular, sign-stable frontal phenotype)"
        statement = (
            "The GAP-2 frontal phenotype SURVIVED ST-2. The hub>random long-range-binding "
            "dissociation appears in the BEHAVIOURAL read-out (distant-block recovery, "
            "independent of the severed edges) and EXCEEDS the all-to-all control "
            "(topological, not edge-cutting per se), and the hub-lesion SET-SHIFT "
            "perseveration increase is SIGN-STABLE across the settle-duration sweep. "
            "The additive cortical micro-model (hippocampus precedent) is therefore "
            "SUFFICIENT to carry a frontal-specific executive signature WITHOUT touching "
            "the frozen kernel -- M9 stays bit-identical. HONEST RESIDUAL: the effect is "
            "purely TOPOLOGICAL (hub wiring); the engine sign() dynamics ignore the cell "
            "gain g, so this does not yet distinguish FOXG1 from LHX2. Magnitudes [O]; "
            "the sign/structure is the claim.")
    else:
        gap2_grade = "[O] open (phenotype did NOT survive -- additive micro-model judged insufficient)"
        statement = (
            "The phenotype BROKE under ST-2: a signed feature flipped (behavioural gap "
            "vanished -> phenotype was circular, and/or set-shift flipped across durations). "
            "Per the Stress Principle, the additive micro-model is judged INSUFFICIENT for "
            "frontal specificity; the fork 'resolve cortex INSIDE the frozen kernel (breaks "
            "M9)' is put on the table. Flips under verdict.broke_on / stability.*.flipped_cells.")

    results = {
        "module": "cortical_microcircuit_st2 (Chunk B / ST-2)",
        "constitution": {"new_tuned_constants": 0, "consciousness_claim": 0,
                         "hard_problem_open": 1, "engine_readonly": True},
        "engine_anchor_bitforbit": {"R": anchor["engine_integrator_R"],
                                    "matches_M9_anchor": anchor["engine_matches_anchor_bitforbit"],
                                    "integrator_matches_engine": anchor["frontal_matches_engine_bitforbit"]},
        "grid": {"cohorts": COHORTS, "durations": DURATIONS, "lesion_seeds": LESION_SEEDS,
                 "fracs": list(FRACS), "abs_margin": MARGIN, "n_cells": len(cells)},
        "cohort_binding_gap_behavioural": coh_bind,
        "cohort_binding_gap_all_to_all": coh_bind_aa,
        "cohort_binding_curve_over_fracs": coh_bind_curve,
        "circular_readout_contrast": coh_circular,
        "cells": cells,
        "stability": stab,
        "verdict": {"phenotype_sign_stable": phenotype_sign_stable, "gap2_grade": gap2_grade,
                    "broke_on": broke_axes, "statement": statement},
        "grades": ("behavioural long-range binding + set-shift are FUNCTIONAL measures "
                   "[V mechanism]; sign-stability across cohort/duration is the ST-2 result; "
                   "gene-specificity stays [O] (g not in sign() dynamics); felt quality [O] OPEN. "
                   "new_tuned_constants=0; engine READ-ONLY."),
    }
    digest = FC.digest_of(results); results["digest"] = digest
    with open(RESULTS_JSON, "w") as f:
        f.write(FC.blob(results))
    with open(EXPECTED_SHA, "w") as f:
        json.dump({"cortical_microcircuit_st2_results.json": digest}, f, indent=2)
    _figure(coh_bind_curve, coh_bind_aa, cells, stab, results["verdict"])

    print()
    print(" SIGN-STABILITY (no contradicting cell + >=2 supporting => stable):")
    for k in ("noncircular", "topological", "setshift"):
        s = stab[k]
        print("   {:<12s} support={:2d} contradict={:2d} ambiguous={:2d}  -> sign_stable={}".format(
            k, s["support"], s["contradict"], s["ambiguous"], s["sign_stable"]))
    print(" VERDICT: phenotype_sign_stable =", phenotype_sign_stable, "| Gap-2 grade:", gap2_grade)
    if broke_axes:
        print("          broke_on =", broke_axes)
    print(" " + statement)
    print(" results ->", RESULTS_JSON)
    print(" sha     ->", digest)
    print(" figure  ->", FIG_OUT)
    print(" STATUS: COMPLETE")


def _figure(coh_bind_curve, coh_bind_aa, cells, stab, verdict):
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(12.6, 5.2))
    # left: behavioural binding gap vs matched fraction, per cohort, + all-to-all control band
    colors = {"C1": "#c0392b", "C2": "#8e44ad", "C3": "#16a085"}
    for cname, curve in coh_bind_curve.items():
        ax.plot(FRACS, curve, "o-", color=colors.get(cname, "#333"), lw=2.2,
                label="cortex (hub topology)  {}".format(cname))
    aa_mean = float(np.mean(list(coh_bind_aa.values())))
    ax.axhline(aa_mean, color="#888", ls="--", lw=1.6, label="all-to-all control (no hubs)")
    ax.axhline(0.0, color="k", lw=0.8, alpha=0.5)
    ax.set_xlabel("matched fraction of edges severed  (hub pool vs local pool)")
    ax.set_ylabel("binding gap = recovery(rand cut) - recovery(hub cut)")
    ax.set_title("NON-CIRCULAR phenotype: long-range binding is hub-borne\n"
                 "(behavioural read-out, scored on the free distant block)")
    ax.legend(fontsize=8, loc="upper left"); ax.grid(True, alpha=0.25)
    # right: set-shift perseveration delta (hub - intact) vs duration, per cohort
    for cname in coh_bind_curve:
        sub = [c for c in cells if c["cohort"] == cname]
        sub = sorted(sub, key=lambda c: c["dur"])
        ax2.plot([c["dur"] for c in sub], [c["feat"]["persev_delta"] for c in sub],
                 "s-", color=colors.get(cname, "#333"), lw=2.2, label="{}".format(cname))
    ax2.axhline(0.0, color="k", lw=0.8, alpha=0.5)
    ax2.set_xlabel("set-shift settle duration (steps)")
    ax2.set_ylabel("perseveration delta = hub-lesion - intact")
    ax2.set_title("SET-SHIFT under a DURATION SWEEP\n(hub lesion -> distant block locked on A; sign-stable?)")
    ax2.legend(fontsize=8, loc="upper right"); ax2.grid(True, alpha=0.25)
    txt = ("ST-2 verdict: phenotype_sign_stable = {}   |   non-circular stable={}  "
           "topological stable={}  set-shift stable={}").format(
        verdict["phenotype_sign_stable"], stab["noncircular"]["sign_stable"],
        stab["topological"]["sign_stable"], stab["setshift"]["sign_stable"])
    fig.suptitle(txt, fontsize=10.5, y=1.005,
                 color=("#1e7d34" if verdict["phenotype_sign_stable"] else "#a11"))
    fig.tight_layout(); fig.savefig(FIG_OUT, dpi=130, bbox_inches="tight")


if __name__ == "__main__":
    main()
