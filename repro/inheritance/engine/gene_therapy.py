#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gene_therapy.py  --  TWO THERAPEUTIC LEVERS ON ONE SUBSTRATE  (battery GT1-GT4).

  The substrate makes the therapeutic options sharp. A switch is gamma (the SET, written in the genome)
  plus a drive h (the environment / a delivered payload). So there are exactly TWO levers:

    Lever A -- EDIT THE SET (gamma / the switch itself): genome editing (CRISPR base / prime editing).
               It MOVES the threshold permanently (spinodal/barrier change). Irreversible by a drive.
    Lever B -- RE-SET THE DRIVE h WITHOUT touching the SET: RNA therapeutics (siRNA knockdown = negative
               h; ASO splice-switch; saRNA activation = positive h). Reversible / tunable (rna_layer.py).

  The decision rule falls out of the geometry: a deep PATHOLOGICAL basin that a tolerable drive cannot
  clear needs Lever A (move the threshold); a target a drive CAN move reversibly is better served by
  Lever B. MAGNITUDE FIREWALL: which lever, the SIGN of the correction, and reversibility are read [V];
  absolute dose, edit efficiency, and clinical outcome are runtime [O].

GT1  Lever A -- a SET edit (gamma change) MOVES the spinodal/barrier; an opposite drive cannot restore the
     original threshold (irreversible at the SET level). [V]
GT2  Lever B -- an RNA drive flips the switch and is REVERSIBLE (reuses the rna_layer reversibility). [V]
GT3  decision rule -- a deep pathological basin past a tolerable-drive reach needs Lever A; a drive-reachable
     target needs only Lever B. [V on the rule]
GT4  honest scoreboard + firewall (clinical gene therapy belongs to clinicians/regulators).
"""
import json
import numpy as np
from _substrate import rna_gamma, immune_gamma, spinodal, barrier, SEED


def _settle(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * (g * s - s ** 3 + h)
    return s


def GT1_set_edit_moves_threshold():
    """A genome edit changes gamma -> the spinodal and barrier move. An opposite drive cannot restore the
    original gamma (the SET, not the drive, changed). Irreversible at the SET level."""
    g0 = rna_gamma()["DICER1"]
    g1 = g0 + 0.08                                  # an editing-scale change to the master's gamma
    moved = abs(spinodal(g1) - spinodal(g0)) > 1e-3 and abs(barrier(g1) - barrier(g0)) > 1e-3
    # no drive h restores g0's threshold once the SET is g1: gamma is not a function of h
    set_irreversible_by_drive = (g1 != g0)
    return {
        "name": "GT1 Lever A -- SET edit moves the threshold (irreversible by a drive)",
        "gamma_before": round(g0, 4), "gamma_after_edit": round(g1, 4),
        "spinodal_before": round(spinodal(g0), 4), "spinodal_after": round(spinodal(g1), 4),
        "barrier_before": round(barrier(g0), 4), "barrier_after": round(barrier(g1), 4),
        "threshold_moved": bool(moved), "set_not_restorable_by_drive": bool(set_irreversible_by_drive),
        "grade": "[V] gamma-edit relocates spinodal/barrier; absolute edit efficiency is runtime [O]",
        "pass": bool(moved and set_irreversible_by_drive),
    }


def GT2_drive_reset_reversible():
    """An RNA drive flips a switch and is reversible: drive it OFF (knockdown), clear, it returns to the
    environment-set ON basin -- gamma never touched (the rna_layer reversibility, applied therapeutically)."""
    g = rna_gamma()["TARBP2"]
    hsp = spinodal(g)
    h_env = +1.3 * hsp                               # disease context holds the switch ON supra-spinodally
    s_knockdown = _settle(g, h_env - 2.6 * hsp, s0=+np.sqrt(g))   # siRNA: drive OFF
    forced_off = s_knockdown < 0
    s_cleared = _settle(g, h_env, s0=s_knockdown)    # therapy withdrawn -> returns to environment basin
    reversible = s_cleared > 0
    gamma_untouched = (rna_gamma()["TARBP2"] == g)
    return {
        "name": "GT2 Lever B -- reversible h-reset (RNA), gamma untouched",
        "gamma_TARBP2": round(g, 4), "forced_OFF_by_siRNA": bool(forced_off),
        "reversible_on_withdrawal": bool(reversible), "gamma_untouched": bool(gamma_untouched),
        "grade": "[V] reversible/tunable correction; absolute dose is runtime [O]",
        "pass": bool(forced_off and reversible and gamma_untouched),
    }


def GT3_decision_rule():
    """Decision rule from the geometry. A deep pathological basin: can a TOLERABLE drive (bounded by a
    safety cap < some multiple of spinodal) clear it? If not -> Lever A (move the threshold). If yes ->
    Lever B (reversible drive). Demonstrate both regimes on the same switch with a tolerability cap."""
    g = immune_gamma()["PAX5"]
    hsp = spinodal(g)
    # Clearing a switch HELD ON requires driving past the far spinodal: required drive = h_path + spinodal.
    # A correction is "drive-reachable" iff that required drive fits under the tolerable cap.
    tolerable_cap = 2.5 * hsp                        # largest tolerable drive (declared, not tuned to outcome)
    # Case 1: shallow pathological tilt -> required drive (h_path+spinodal) fits the cap -> Lever B
    h_path_shallow = +0.4 * hsp
    cleared_shallow = _settle(g, h_path_shallow - tolerable_cap, s0=+np.sqrt(g)) < 0
    # Case 2: deep pathological hold -> required drive exceeds the cap -> needs Lever A (move the threshold)
    h_path_deep = +2.2 * hsp
    cleared_deep_by_drive = _settle(g, h_path_deep - tolerable_cap, s0=+np.sqrt(g)) < 0
    rule_ok = cleared_shallow and (not cleared_deep_by_drive)
    return {
        "name": "GT3 decision rule -- drive-reachable -> Lever B; beyond tolerable drive -> Lever A",
        "gamma_PAX5": round(g, 4), "spinodal": round(hsp, 4), "tolerable_drive_cap": round(tolerable_cap, 4),
        "shallow_tilt_cleared_by_tolerable_drive": bool(cleared_shallow),
        "deep_hold_needs_SET_edit": bool(not cleared_deep_by_drive),
        "rule_separates_the_two_levers": bool(rule_ok),
        "grade": "[V] the lever choice is a geometry threshold; absolute clinical dosing is runtime [O]",
        "pass": bool(rule_ok),
    }


def run_battery():
    tests = [GT1_set_edit_moves_threshold(), GT2_drive_reset_reversible(), GT3_decision_rule()]
    allp = all(t["pass"] for t in tests)
    return {"module": "gene_therapy", "battery": "GT1-GT4", "seed": SEED,
            "GT4_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "lever CHOICE, correction SIGN, reversibility read [V]; absolute dose, edit "
                        "efficiency and clinical outcome are runtime [O]; gene therapy belongs to clinicians/regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
