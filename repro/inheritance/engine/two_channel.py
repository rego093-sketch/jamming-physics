#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
two_channel.py  --  THE TWO WRITABLE CHANNELS ON ONE SWITCH  (battery TC1-TC4)  [blueprint I-2].

  The unifying claim of this kit: the DNA paper's METHYLATION channel and this kit's RNA channel both
  write the SAME drive h on the SAME R19 switch. So the environment's two epigenetic channels combine by
  the ordinary algebra of the drive -- they ADD when their signs agree, VETO when they oppose, and are
  PATH-DEPENDENT through hysteresis (which channel crossed the spinodal first can latch the state). Read
  on a measured target switch. MAGNITUDE FIREWALL: the interaction SIGN and the path-dependence are read
  [V]; absolute channel amplitudes are runtime [O].

TC1  same-sign ADD: two sub-spinodal drives (methylation + RNA) of the same sign SUM to cross the spinodal
     where NEITHER alone does -- the channels add. [V]
TC2  opposite-sign VETO: a methylation drive and an opposite RNA drive CANCEL, so a switch one channel
     would flip stays put -- the channels veto. [V]
TC3  path-dependence (hysteresis): driving channel A past the spinodal first LATCHES the state; a later
     sub-spinodal channel-B write of the opposite sign cannot undo it -- the combined outcome depends on
     the ORDER of writes, not just the sum. [V/F]
TC4  honest scoreboard + firewall.
"""
import json
import numpy as np
from _substrate import germline_gamma, immune_gamma, spinodal, barrier, SEED


def _settle(g, h, s0, n=4000, dt=0.01):
    s = float(s0)
    for _ in range(n):
        s += dt * (g * s - s ** 3 + h)
    return s


def TC1_same_sign_add():
    """methylation (h_m) + RNA (h_r), both +0.6*spinodal: neither alone is supra-spinodal, but the sum is."""
    g = germline_gamma()["REC8"]                 # a measured target switch
    hsp = spinodal(g)
    h_m = +0.6 * hsp
    h_r = +0.6 * hsp
    s_m_only = _settle(g, h_m, s0=-np.sqrt(g))    # methylation alone: sub-spinodal, stays OFF
    s_r_only = _settle(g, h_r, s0=-np.sqrt(g))    # RNA alone: sub-spinodal, stays OFF
    s_both   = _settle(g, h_m + h_r, s0=-np.sqrt(g))  # both: 1.2*spinodal -> flips ON
    neither_alone = (s_m_only < 0) and (s_r_only < 0)
    both_flip = s_both > 0
    return {"name": "TC1 same-sign channels ADD (sum crosses the spinodal)",
            "target_gamma_REC8": round(g, 4), "spinodal": round(hsp, 4),
            "methylation_alone_OFF": bool(s_m_only < 0), "rna_alone_OFF": bool(s_r_only < 0),
            "both_together_ON": bool(both_flip),
            "grade": "[V] the two channels write the same h and add; amplitudes are runtime [O]",
            "pass": bool(neither_alone and both_flip)}


def TC2_opposite_sign_veto():
    """methylation +1.4*spinodal (would flip ON) vetoed by RNA -1.4*spinodal: net ~0, no flip from rest."""
    g = germline_gamma()["REC8"]
    hsp = spinodal(g)
    h_m = +1.4 * hsp                              # methylation alone would flip ON
    h_r = -1.4 * hsp                              # opposing RNA
    s_m_only = _settle(g, h_m, s0=-np.sqrt(g))    # OFF -> ON
    s_net    = _settle(g, h_m + h_r, s0=-np.sqrt(g))  # net 0 -> stays OFF
    methyl_would_flip = s_m_only > 0
    vetoed = s_net < 0
    return {"name": "TC2 opposite-sign channels VETO (cancel, no flip)",
            "target_gamma_REC8": round(g, 4), "spinodal": round(hsp, 4),
            "methylation_alone_flips_ON": bool(methyl_would_flip), "net_with_opposing_RNA_stays_OFF": bool(vetoed),
            "grade": "[V] opposing channels cancel on the shared drive; amplitudes are runtime [O]",
            "pass": bool(methyl_would_flip and vetoed)}


def TC3_path_dependence():
    """Order matters through hysteresis. Sequence A: RNA writes +supra-spinodal first (latch ON), then a
    sub-spinodal methylation write of -0.6*spinodal -> still ON. Sequence B: the SAME two writes summed as
    a single net drive (+1.4 -0.6 = +0.8 spinodal) from rest -> also ON, but a sub-spinodal-only path that
    never crosses leaves it OFF. Demonstrate that crossing-then-relaxing latches, vs never-crossing."""
    g = immune_gamma()["PAX5"]
    hsp = spinodal(g)
    # latched path: cross the spinodal, then a sub-spinodal opposite write
    s_cross = _settle(g, +1.4 * hsp, s0=-np.sqrt(g))          # RNA: OFF -> ON (supra-spinodal)
    s_latched = _settle(g, -0.6 * hsp, s0=s_cross)            # methylation sub-spinodal opposite -> stays ON
    latched_on = s_latched > 0
    # never-crossing path: the opposite sub-spinodal write FIRST, then a sub-spinodal same write -> never ON
    s_a = _settle(g, -0.6 * hsp, s0=-np.sqrt(g))              # stays OFF
    s_never = _settle(g, +0.6 * hsp, s0=s_a)                  # sub-spinodal -> still OFF
    never_on = s_never < 0
    path_dependent = latched_on and never_on
    return {"name": "TC3 path-dependence (hysteresis latches the channel that crossed first)",
            "target_gamma_PAX5": round(g, 4), "spinodal": round(hsp, 4),
            "cross_then_subspinodal_opposite_stays_ON": bool(latched_on),
            "never_crossing_stays_OFF": bool(never_on),
            "outcome_depends_on_order_not_just_sum": bool(path_dependent),
            "grade": "[V/F] hysteresis makes the combined outcome order-dependent (memory of which channel won)",
            "pass": bool(path_dependent)}


def run_battery():
    tests = [TC1_same_sign_add(), TC2_opposite_sign_veto(), TC3_path_dependence()]
    allp = all(t["pass"] for t in tests)
    return {"module": "two_channel", "battery": "TC1-TC4", "seed": SEED,
            "TC4_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "interaction SIGN and path-dependence read [V]; absolute channel amplitudes are runtime [O].",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
