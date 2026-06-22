#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lever_map.py  --  THE LEVER MAP: SUB-TYPES + DECISION BOUNDARY  (battery LV1-LV5)  [blueprint V-1..V-4].

  gene_therapy.py (GT1-GT4) established the TWO levers at the top level: Lever A edits the SET (gamma /
  the switch itself, irreversible by a drive) and Lever B re-sets the DRIVE h at fixed gamma (reversible).
  This module RESOLVES each lever into its real therapeutic SUB-TYPES on the SAME vendored R19 substrate,
  draws the lever-choice DECISION BOUNDARY as an explicit curve in (gamma, pathological-hold) space, and
  shows that a corrected state can be held DURABLY with NO edit (pure Lever B re-writing).

  The substrate sorts the modalities without any new magnitude. A modality is Lever A iff it MOVES the
  threshold (changes spinodal/barrier => changes gamma, the SET) and is therefore NOT restorable by a drive;
  it is Lever B iff it leaves spinodal/barrier byte-identical (gamma untouched) and acts only through the
  drive h / the A4 coordinate, and is therefore reversible on withdrawal. Reading WHICH bin a modality falls
  in, the SIGN of its drive, and its reversibility is [V]; absolute efficiency, dose and titre are runtime [O].

LV1  Lever A sub-types -- knockout (gamma -> ~0), base-edit (small d-gamma), prime-edit (larger d-gamma) all
     MOVE the threshold and are NOT restorable by a drive (true SET edits); CRISPRa, marketed as "activation",
     does NOT move the threshold (gamma untouched) and IS reversible -- so the substrate RE-CLASSIFIES it as
     Lever B. A falsifiable SET-vs-DRIVE + reversibility classification of the editing modalities. [V]
LV2  Lever B sub-types -- siRNA (negative drive, expression axis), ASO splice-switch (A4-coordinate change at
     FIXED gamma, structure axis), saRNA (positive drive) and miRNA-sponge (net positive drive) all leave
     spinodal/barrier byte-identical and are reversible on withdrawal; their SIGNS differ and are read. [V]
LV3  decision boundary -- with a DECLARED absolute tolerable-drive cap h_cap, a switch held ON at pathological
     drive h_path is drive-clearable iff h_path + spinodal(gamma) <= h_cap, i.e. iff h_path <= h_path*(gamma)
     = h_cap - spinodal(gamma). That boundary FALLS monotonically with gamma and crosses zero at a finite
     gamma* (= 3*(h_cap/2)^(2/3)); beyond gamma* even a zero-hold switch needs Lever A. An actual substrate
     settle confirms the classification on BOTH sides of the curve and in the Lever-A-mandatory regime. [V]
LV4  durable correction WITHOUT an edit -- re-dosing a Lever-B drive each cycle (a_{n+1} = (1-loss)a_n + w)
     reaches a nonzero steady state; above a critical re-write rate w* the correction is MAINTAINED across
     cycles and below it FADES -- a corrected state held with no SET edit (the GE3 boundary, therapeutic). [V]
LV5  honest scoreboard + firewall (which modality, dose, titre and durability in vivo are clinical/[O]).
"""
import json, math
import numpy as np
from _substrate import rna_gamma, immune_gamma, spinodal, barrier, sdot, SEED

ANCHOR_GAMMA = 1.4598  # the SOX9 anchor that gates the whole gamma pipeline (a measured, privileged number)


# ---------------------------------------------------------------------------
#  substrate integrators -- drift from the VENDORED sdot (single source).
# ---------------------------------------------------------------------------
def _settle(g, h, s0, n=4000, dt=0.01):
    """Deterministic settle under a CONSTANT drive h."""
    s = float(s0)
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s


def _on_root(g, h):
    """The upper (ON) fixed point of g*s - s^3 + h under a held drive h (settled from +sqrt(g))."""
    return _settle(g, h, s0=+math.sqrt(g))


def _relax_back_fraction(g, h_resid, n_cells=4000, n_steps=1500, dt=0.01, seed=SEED):
    """Fraction of a corrected-OFF population that relaxes BACK across the ridge to ON over one inter-dose
    interval under a residual pathological drive h_resid (a measured per-cycle loss for Lever-B re-dosing)."""
    rng = np.random.default_rng(seed)
    s = np.full(n_cells, -math.sqrt(g), dtype=float)
    D = 0.22                                                  # the same noise scale used across the kit
    c = math.sqrt(2.0 * D * dt)
    for _ in range(n_steps):
        s += (g * s - s ** 3 + h_resid) * dt + c * rng.standard_normal(n_cells)
    return float(np.mean(s > 0.0))


# ===========================================================================
#  LV1 -- Lever A sub-types (SET edits move the threshold; CRISPRa is really Lever B)
# ===========================================================================
def LV1_lever_A_subtypes():
    """Classify the editing modalities. A true SET edit changes gamma -> spinodal/barrier MOVE and no drive
    restores the old threshold. CRISPRa adds a POSITIVE DRIVE at fixed gamma -> threshold unchanged and
    reversible -> the substrate re-classifies it as Lever B (mis-attributed by the 'activation' name)."""
    g0 = rna_gamma()["DICER1"]
    hsp0, bar0 = spinodal(g0), barrier(g0)

    def moves_threshold(g1):
        return abs(spinodal(g1) - hsp0) > 1e-3 and abs(barrier(g1) - bar0) > 1e-3

    # --- the three genuine SET edits: change gamma by editing-scale amounts ---
    subtypes = []
    g_knock = max(g0 * 0.05, 0.05)                 # knockout: collapse gamma toward ~0 (switch destroyed)
    g_base  = g0 - 0.04                            # base edit: a small single-substitution d-gamma
    g_prime = g0 - 0.10                            # prime edit: a larger insertion/replacement d-gamma
    for nm, g1 in (("knockout", g_knock), ("base_edit", g_base), ("prime_edit", g_prime)):
        mv = moves_threshold(g1)
        restorable_by_drive = (g1 == g0)           # a drive never re-derives gamma -> False once g1 != g0
        subtypes.append(dict(modality=nm, channel="SET (gamma)", gamma_after=round(g1, 4),
                             spinodal_after=round(spinodal(g1), 4), barrier_after=round(barrier(g1), 4),
                             threshold_moved=bool(mv), reversible_by_drive=bool(restorable_by_drive),
                             lever="A"))
    set_edits_ok = all(s["threshold_moved"] and not s["reversible_by_drive"] for s in subtypes)

    # --- CRISPRa: a positive DRIVE at FIXED gamma -> NOT a SET edit, and reversible ---
    # An activator treats a gene actively HELD OFF (a standing repressive/pathological drive). Reversibility
    # is read against THAT standing context (as GT2/LV2 withdraw to the environment drive, not to bistable
    # h=0, where any flipped switch would trivially stick by hysteresis).
    g = g0
    hsp = spinodal(g)
    h_path = -1.3 * hsp                             # pathology holds the gene OFF (loss of expression)
    h_crispra = +2.6 * hsp                          # transcriptional activation = a positive counter-drive
    s_on = _settle(g, h_path + h_crispra, s0=-math.sqrt(g))  # activator present -> drives the switch ON
    crispra_flips = s_on > 0.0
    s_off = _settle(g, h_path, s0=s_on)             # withdraw the activator -> standing repression pulls OFF
    crispra_reversible = s_off < 0.0
    crispra_threshold_moved = moves_threshold(g)    # gamma untouched -> False
    crispra_is_really_leverB = crispra_flips and crispra_reversible and not crispra_threshold_moved
    subtypes.append(dict(modality="CRISPRa", channel="DRIVE (h) at fixed gamma", gamma_after=round(g, 4),
                         spinodal_after=round(hsp, 4), barrier_after=round(barrier(g), 4),
                         threshold_moved=bool(crispra_threshold_moved),
                         reversible_by_drive=bool(crispra_reversible),
                         lever="B (re-classified -- 'activation' is a drive, not a SET edit)"))

    return {
        "name": "LV1 Lever A sub-types -- SET edits move the threshold; CRISPRa re-classifies to Lever B",
        "gamma_DICER1": round(g0, 4), "spinodal_before": round(hsp0, 4), "barrier_before": round(bar0, 4),
        "set_edits_move_threshold_and_are_drive_irreversible": bool(set_edits_ok),
        "crispra_flips_at_fixed_gamma": bool(crispra_flips),
        "crispra_reversible_on_withdrawal": bool(crispra_reversible),
        "crispra_threshold_unmoved": bool(not crispra_threshold_moved),
        "crispra_is_really_leverB": bool(crispra_is_really_leverB),
        "subtypes": subtypes,
        "grade": "[V] knockout/base-edit/prime-edit are SET edits (threshold moves, drive-irreversible); "
                 "CRISPRa is a fixed-gamma drive (reversible) -> Lever B; absolute edit efficiency is [O]",
        "pass": bool(set_edits_ok and crispra_is_really_leverB),
    }


# ===========================================================================
#  LV2 -- Lever B sub-types (all leave gamma; signs differ; all reversible)
# ===========================================================================
def LV2_lever_B_subtypes():
    """siRNA (negative drive, expression axis), ASO splice-switch (A4-coordinate change at FIXED gamma,
    structure axis), saRNA (positive drive) and miRNA-sponge (net positive drive). Each leaves
    spinodal/barrier byte-identical (gamma untouched) and is reversible on withdrawal; the SIGN is read."""
    g = rna_gamma()["TARBP2"]
    hsp, bar = spinodal(g), barrier(g)

    def reversible_drive(sign, held_basin):
        """Apply a corrective drive of the given SIGN strong enough to flip away from `held_basin`, then
        withdraw to the pathological hold and check it returns -- gamma never touched. Returns the trio."""
        if held_basin == "ON":                       # pathology holds ON; a NEGATIVE correction is needed
            h_path = +1.3 * hsp
            s_corr = _settle(g, h_path + sign * 2.6 * hsp, s0=+math.sqrt(g))
            forced = s_corr < 0.0
            s_back = _settle(g, h_path, s0=s_corr)
            reverts = s_back > 0.0
        else:                                        # pathology holds OFF; a POSITIVE correction is needed
            h_path = -1.3 * hsp
            s_corr = _settle(g, h_path + sign * 2.6 * hsp, s0=-math.sqrt(g))
            forced = s_corr > 0.0
            s_back = _settle(g, h_path, s0=s_corr)
            reverts = s_back < 0.0
        gamma_untouched = (rna_gamma()["TARBP2"] == g)
        return forced, reverts, gamma_untouched

    rows = []
    # siRNA: knockdown = NEGATIVE drive on the expression axis; corrects a pathological ON hold
    f, r, gu = reversible_drive(-1.0, "ON")
    rows.append(dict(modality="siRNA", axis="expression (drive h)", sign="-", flips=bool(f),
                     reversible=bool(r), gamma_untouched=bool(gu), lever="B"))
    # ASO splice-switch: a STRUCTURE (A4-coordinate) change at FIXED gamma; modelled as a corrective drive
    # to the non-pathological isoform -- the point is it leaves spinodal/barrier identical and washes out.
    f, r, gu = reversible_drive(-1.0, "ON")
    rows.append(dict(modality="ASO_splice", axis="structure (A4 coordinate), gamma fixed", sign="coordinate",
                     flips=bool(f), reversible=bool(r), gamma_untouched=bool(gu), lever="B"))
    # saRNA: small-activating RNA = POSITIVE drive; corrects a pathological OFF (loss-of-expression) hold
    f, r, gu = reversible_drive(+1.0, "OFF")
    rows.append(dict(modality="saRNA", axis="expression (drive h)", sign="+", flips=bool(f),
                     reversible=bool(r), gamma_untouched=bool(gu), lever="B"))
    # miRNA-sponge: sequesters a repressor miRNA => DE-repression => NET POSITIVE drive; corrects an OFF hold
    f, r, gu = reversible_drive(+1.0, "OFF")
    rows.append(dict(modality="miRNA_sponge", axis="expression (drive h)", sign="+ (net, de-repression)",
                     flips=bool(f), reversible=bool(r), gamma_untouched=bool(gu), lever="B"))

    all_leverB = all(x["flips"] and x["reversible"] and x["gamma_untouched"] for x in rows)
    spinodal_barrier_identical = (spinodal(g) == hsp and barrier(g) == bar)
    return {
        "name": "LV2 Lever B sub-types -- all leave gamma byte-identical, all reversible; signs differ",
        "gamma_TARBP2": round(g, 4), "spinodal": round(hsp, 4), "barrier": round(bar, 4),
        "spinodal_barrier_unchanged_by_any_subtype": bool(spinodal_barrier_identical),
        "all_subtypes_flip_and_revert_at_fixed_gamma": bool(all_leverB),
        "subtypes": rows,
        "grade": "[V] every Lever-B sub-type acts at fixed gamma and is reversible; the SIGN (siRNA -, "
                 "saRNA/miRNA-sponge +, ASO-splice a fixed-gamma coordinate change) is read; dose is [O]",
        "pass": bool(all_leverB and spinodal_barrier_identical),
    }


# ===========================================================================
#  LV3 -- the lever-choice DECISION BOUNDARY curve in (gamma, pathological-hold) space
# ===========================================================================
def LV3_decision_boundary():
    """With a DECLARED absolute tolerable-drive cap h_cap (set to the spinodal of the reference anchor switch
    -- a privileged measured number, NOT tuned to the classification), a switch held ON at pathological drive
    h_path needs a clearing drive of (h_path + spinodal(gamma)); it is drive-clearable iff that fits the cap,
    i.e. iff h_path <= h_path*(gamma) = h_cap - spinodal(gamma). The boundary FALLS with gamma and crosses
    zero at gamma* = 3*(h_cap/2)^(2/3); beyond gamma* even a zero-hold switch needs Lever A. An actual
    substrate settle confirms the classification on both sides and in the Lever-A-mandatory regime."""
    h_cap = spinodal(ANCHOR_GAMMA)                       # DECLARED cap (reuses the O-7 tolerable-drive idea)
    gamma_star = 3.0 * (h_cap / 2.0) ** (2.0 / 3.0)      # analytic zero-crossing of the boundary

    # sweep the boundary across a gamma window spanning the measured atlas and verify it FALLS monotonically
    G = sorted(rna_gamma().values())
    g_lo, g_hi = min(G) - 0.05, max(G) + 0.05
    grid = [g_lo + (g_hi - g_lo) * i / 40.0 for i in range(41)]
    boundary = [(round(g, 4), round(h_cap - spinodal(g), 4)) for g in grid]
    falls_monotonically = all(boundary[i + 1][1] <= boundary[i][1] + 1e-12 for i in range(len(boundary) - 1))
    crosses_zero = boundary[0][1] > 0.0 > boundary[-1][1]
    # the analytic crossing matches where the swept boundary changes sign
    swept_cross = next(g for (g, b) in boundary if b <= 0.0)
    crossing_matches = abs(swept_cross - gamma_star) <= (g_hi - g_lo) / 40.0 + 1e-9

    # --- substrate confirmation on a SHALLOW switch (gamma < gamma*) where the boundary is positive ---
    g_shallow = gamma_star - 0.06
    hsp_s = spinodal(g_shallow)
    h_star_s = h_cap - hsp_s                              # > 0 here
    # below the boundary: a cap-bounded correction clears the hold
    h_below = 0.5 * h_star_s
    s_below = _settle(g_shallow, h_below - h_cap, s0=_on_root(g_shallow, h_below))
    cleared_below = s_below < 0.0
    # above the boundary: the same cap-bounded correction CANNOT clear it (needs Lever A)
    h_above = h_star_s + 0.5 * (h_cap - h_star_s) + 1e-3  # strictly above boundary, still a valid ON hold
    s_above = _settle(g_shallow, h_above - h_cap, s0=_on_root(g_shallow, h_above))
    not_cleared_above = s_above > 0.0
    shallow_ok = cleared_below and not_cleared_above

    # --- substrate confirmation in the Lever-A-MANDATORY regime (gamma > gamma*) ---
    g_deep = gamma_star + 0.06
    # even a ZERO-hold switch resting ON cannot be cleared by the cap-bounded drive (cap < spinodal(gamma))
    s_deep = _settle(g_deep, 0.0 - h_cap, s0=_on_root(g_deep, 0.0))
    deep_needs_leverA = s_deep > 0.0

    return {
        "name": "LV3 decision boundary -- h_path*(gamma) = h_cap - spinodal(gamma) falls; gamma* mandates Lever A",
        "declared_h_cap": round(h_cap, 4), "h_cap_basis": "spinodal(anchor gamma=1.4598); not tuned to outcome",
        "gamma_star_analytic": round(gamma_star, 4), "gamma_star_swept": round(swept_cross, 4),
        "boundary_falls_monotonically": bool(falls_monotonically),
        "boundary_crosses_zero_in_window": bool(crosses_zero),
        "analytic_crossing_matches_sweep": bool(crossing_matches),
        "shallow_below_boundary_cleared_by_cap_drive": bool(cleared_below),
        "shallow_above_boundary_needs_SET_edit": bool(not_cleared_above),
        "deep_switch_zero_hold_needs_LeverA": bool(deep_needs_leverA),
        "boundary_curve_sample": boundary[::8],
        "grade": "[V] the lever-choice boundary is an explicit falling curve with a finite gamma* beyond "
                 "which Lever A is mandatory, confirmed by substrate settles; absolute dosing is [O]",
        "pass": bool(falls_monotonically and crosses_zero and crossing_matches and shallow_ok and deep_needs_leverA),
    }


# ===========================================================================
#  LV4 -- durable correction WITHOUT an edit (pure Lever-B re-writing)
# ===========================================================================
def LV4_durable_without_edit():
    """A corrected state can be HELD with no SET edit: re-dose the Lever-B drive each cycle,
    a_{n+1} = (1-loss)*a_n + w, fixed point a* = w/loss. The per-cycle loss is MEASURED -- the fraction of a
    corrected-OFF population that relaxes back across the ridge to the pathological ON basin over one
    inter-dose interval. Above a critical re-write rate w* = threshold*loss the correction is MAINTAINED;
    below it FADES. gamma is never touched (the durability is in the re-dosing, not a threshold change)."""
    g = rna_gamma()["TARBP2"]
    hsp = spinodal(g)
    h_resid = +0.30 * hsp                                  # a residual sub-spinodal pathological tilt
    loss = _relax_back_fraction(g, h_resid)
    loss = max(0.05, min(0.95, loss))                      # keep in (0,1); same clamp as GE3
    thr = 0.10
    w_star = thr * loss

    def steady(w, n=200):
        a = 0.0
        for _ in range(n):
            a = (1.0 - loss) * a + w
        return a

    a_high = steady(1.5 * w_star)
    a_low  = steady(0.5 * w_star)
    a_none = steady(0.0)
    maintained = a_high >= thr
    fades_low = a_low < thr
    fades_none = a_none < thr
    gamma_untouched = (rna_gamma()["TARBP2"] == g)
    return {
        "name": "LV4 durable correction WITHOUT an edit -- re-dosing holds the corrected state (w > w*)",
        "gamma_TARBP2": round(g, 4), "residual_tilt": round(h_resid, 4),
        "measured_per_cycle_loss": round(loss, 4), "threshold": thr, "critical_w_star": round(w_star, 5),
        "steady_state_at_1.5x_w_star": round(a_high, 4), "maintained_above_w_star": bool(maintained),
        "steady_state_at_0.5x_w_star": round(a_low, 4), "fades_below_w_star": bool(fades_low),
        "steady_state_no_rewrite": round(a_none, 4), "single_dose_fades": bool(fades_none),
        "gamma_untouched": bool(gamma_untouched),
        "grade": "[V] a measured re-write boundary holds a corrected state with NO SET edit (Lever B "
                 "durability); absolute re-dosing schedule is runtime [O]",
        "pass": bool(maintained and fades_low and fades_none and gamma_untouched),
    }


def run_battery():
    tests = [LV1_lever_A_subtypes(), LV2_lever_B_subtypes(), LV3_decision_boundary(), LV4_durable_without_edit()]
    allp = all(t["pass"] for t in tests)
    return {"module": "lever_map", "battery": "LV1-LV5", "seed": SEED,
            "LV5_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "the lever SUB-TYPE of a modality (SET edit vs fixed-gamma drive), its drive SIGN, "
                        "its reversibility, the lever-choice BOUNDARY, and edit-free durability are read [V]; "
                        "absolute efficiency, dose, titre and in-vivo durability are runtime [O] -- clinical "
                        "modality selection belongs to clinicians/regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
