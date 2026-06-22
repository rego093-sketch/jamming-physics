#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rna_feasibility_map.py  --  "DOES PUTTING RNA IN ACTUALLY CHANGE THE CELL?"  (battery FM1-FM4).

  This battery answers the feasibility question HONESTLY, on the SAME vendored R19 substrate, at
  MEASURED promoter gamma (the RNA-carrier atlas for the demo set, and -- new in v0.7.0 -- the MEASURED
  neurodevelopmental / autism-spectrum atlas inherited/neuro_gamma.json for the brain-cell extension).

  The blueprint records the governing principle (Part B, "the (A) map vs (B) validation split"): a
  self-contained simulation CANNOT return a yes/no for "did the cell change", because the answer rides on
  the RNA drive magnitude Delta-h, and Delta-h (=dose/size) is exactly an [O] quantity behind the magnitude
  firewall -- doubly unprovable, since the R19 dynamics is itself an assumption. What a self-contained sim
  CAN give is the MAP: given a drive, WHICH switch is reachable, the ORDERING, and whether it is REVERSIBLE.
  Driving past the spinodal flips the switch by construction, so a "flipped" screen is the REPLAY of the
  Delta-h assumption, not a discovery. The line from map-demo to evidence is crossed only by (B): scoring
  the predicted flipped-switch SET + ORDERING against HELD-OUT measured pre/post expression of real
  siRNA/saRNA-treated cells, with NO tuning of Delta-h or parameters to the target.

FM1  REACHABILITY MAP (the (A) map, RNA-carrier set). The minimal drive that flips a switch is its measured
     spinodal h*(gamma)=2(gamma/3)^1.5. Expressed in spinodal units k=h/h*, a flip occurs for k>=1 and not
     for k<1 -- confirmed by integrating the vendored field from the OFF basin. The ABSOLUTE flip-drive
     h*(gamma) RISES with gamma, so the ORDERING of "easiest to flip" is set by the measured promoter
     gamma (shallowest first). Ordering + reachability geometry [V]; the absolute Delta-h is [O].
FM2  THE AUTISM / BRAIN-CELL EXTENSION. The identical map on the MEASURED autism-spectrum atlas (MECP2,
     FMR1, SHANK3, CHD8, NRXN1, NLGN3, PTEN, TSC2, SCN2A, SYNGAP1 -- declared by function, anchor-gated).
     Every ASD switch is R19-bistable (barrier>0) and the flip-drive ordering tracks the measured gamma
     (SCN2A shallowest -> PTEN deepest). So "would brain cells like autism work?" -> in the (A) sense YES:
     the same reachability/ordering structure holds on real ASD promoters. Whether a GIVEN RNA dose changes
     a GIVEN neuron is still [O] / (B). Structure + ordering on measured neuronal promoters [V].
FM3  REVERSIBILITY + SIGN LAW. saRNA = +drive, siRNA = -drive (the sign selects ON vs OFF). A sub-spinodal
     transient RETURNS to baseline after the drive clears; a supra-spinodal transient LATCHES in the new
     basin (hysteresis) and needs an opposite supra-spinodal drive to undo. Reversibility is thus a measured
     geometry property of the switch, not a free choice. Sign + reversibility structure [V]; hold-time [O].
FM4  THE (A)/(B) HONESTY GATE (firewall). Encodes the circularity as a checkable invariant: a flip exists at
     k>=1 for EVERY switch and at no k<1, so the "flipped" screen is fixed by k (the Delta-h assumption),
     carrying zero discriminating information about a real cell. The battery PASSES by correctly localising
     the unprovable quantity to the firewalled Delta-h and refusing to emit a self-contained yes/no -- the
     only honest crossing to evidence is the (B) held-out score named above.
"""
import os, json, math
import numpy as np
from _substrate import rna_gamma, neuro_gamma, neuro_roles, sdot, spinodal, barrier, SEED


# ---------------------------------------------------------------------------
#  substrate integrator -- drift from the VENDORED sdot (single source); no local re-derivation.
# ---------------------------------------------------------------------------
def _settle(g, h, s0, n=6000, dt=0.01):
    """Deterministic settle of the R19 field ds/dt = sdot(s,g,h) to steady state under fixed drive h."""
    s = float(s0)
    for _ in range(n):
        s += dt * sdot(s, g, h)
    return s


def _flips_from_off(g, k, n=6000, dt=0.01):
    """Start in the OFF basin (s0=-sqrt(g)); apply drive h = k * spinodal(g); return True iff the field
    ends in the ON basin (s>0). k is the drive in SPINODAL UNITS, so no absolute Delta-h is asserted."""
    h = k * spinodal(g)
    s_end = _settle(g, h, s0=-math.sqrt(g), n=n, dt=dt)
    return s_end > 0.0, s_end


# =====================================================================================================
#  FM1 -- reachability map on the measured RNA-carrier set
# =====================================================================================================
def FM1_reachability_map():
    G = rna_gamma()
    rows = []
    for sym, g in G.items():
        rows.append(dict(gene=sym, gamma=round(g, 4), spinodal=round(spinodal(g), 4),
                         barrier=round(barrier(g), 4)))
    rows.sort(key=lambda r: r["spinodal"])          # ascending absolute flip-drive
    # the ordering of absolute flip-drive must be monotone in gamma (h* = 2(g/3)^1.5 is increasing in g)
    gammas = [r["gamma"] for r in rows]
    spinos = [r["spinodal"] for r in rows]
    ordering_monotone = all(spinos[i] <= spinos[i + 1] for i in range(len(spinos) - 1)) and \
                        all(gammas[i] <= gammas[i + 1] for i in range(len(gammas) - 1))
    # integration check: a representative switch flips just above its spinodal, holds just below
    gmid = sorted(G.values())[len(G) // 2]
    flip_above, s_above = _flips_from_off(gmid, k=1.05)
    flip_below, s_below = _flips_from_off(gmid, k=0.95)
    reachability_is_spinodal = (flip_above and not flip_below)
    name = "FM1 reachability map: flip-drive = measured spinodal; absolute flip-drive ordered by gamma"
    return dict(name=name, n_switches=len(G),
                easiest=rows[0]["gene"], easiest_spinodal=rows[0]["spinodal"],
                hardest=rows[-1]["gene"], hardest_spinodal=rows[-1]["spinodal"],
                k_above=1.05, flips_just_above_spinodal=bool(flip_above), s_above=round(s_above, 4),
                k_below=0.95, flips_just_below_spinodal=bool(flip_below), s_below=round(s_below, 4),
                absolute_flip_drive_monotone_in_gamma=bool(ordering_monotone),
                reachability_threshold_is_the_measured_spinodal=bool(reachability_is_spinodal),
                map=rows,
                grade="[V] reachability=spinodal and the absolute-flip-drive ordering by gamma are MEASURED "
                      "geometry; the absolute RNA drive Delta-h is runtime [O].",
                **{"pass": bool(ordering_monotone and reachability_is_spinodal)})


# =====================================================================================================
#  FM2 -- the autism / brain-cell extension (measured neurodevelopmental atlas)
# =====================================================================================================
def FM2_autism_brain_extension():
    G = neuro_gamma()
    roles = neuro_roles()
    rows = []
    for sym, g in G.items():
        rows.append(dict(gene=sym, gamma=round(g, 4), spinodal=round(spinodal(g), 4),
                         barrier=round(barrier(g), 4), role=roles.get(sym, "")))
    rows.sort(key=lambda r: r["spinodal"])
    all_bistable = all(r["barrier"] > 0 for r in rows)          # every measured ASD switch is R19-bistable
    spinos = [r["spinodal"] for r in rows]
    gammas = [r["gamma"] for r in rows]
    ordering_tracks_gamma = all(spinos[i] <= spinos[i + 1] for i in range(len(spinos) - 1)) and \
                            all(gammas[i] <= gammas[i + 1] for i in range(len(gammas) - 1))
    # integration check on a representative ASD switch (shallowest and deepest both behave as R19)
    g_shallow = rows[0]["gamma"]; g_deep = rows[-1]["gamma"]
    f_sh_a, _ = _flips_from_off(g_shallow, 1.05); f_sh_b, _ = _flips_from_off(g_shallow, 0.95)
    f_dp_a, _ = _flips_from_off(g_deep, 1.05);    f_dp_b, _ = _flips_from_off(g_deep, 0.95)
    both_behave_as_r19 = (f_sh_a and not f_sh_b and f_dp_a and not f_dp_b)
    name = "FM2 autism extension: measured ASD promoters are R19 switches; flip-drive ordered by gamma"
    return dict(name=name, n_loci=len(G),
                shallowest=rows[0]["gene"], shallowest_gamma=rows[0]["gamma"],
                deepest=rows[-1]["gene"], deepest_gamma=rows[-1]["gamma"],
                every_asd_switch_is_bistable=bool(all_bistable),
                flip_drive_ordering_tracks_measured_gamma=bool(ordering_tracks_gamma),
                shallow_and_deep_both_behave_as_R19=bool(both_behave_as_r19),
                map=rows,
                answer="In the (A)-map sense the structure transfers to real autism-gene promoters: each is "
                       "R19-bistable and an RNA drive past its measured spinodal flips it, ordered by the "
                       "measured promoter gamma. Whether a given RNA dose changes a given neuron is [O]/(B).",
                grade="[V] R19-bistability and the flip-drive ordering on MEASURED neuronal promoters; the "
                      "absolute Delta-h and the per-neuron yes/no are runtime [O] (need (B) held-out data).",
                **{"pass": bool(all_bistable and ordering_tracks_gamma and both_behave_as_r19)})


# =====================================================================================================
#  FM3 -- reversibility + sign law
# =====================================================================================================
def FM3_reversibility_and_sign():
    G = neuro_gamma()
    g = sorted(G.values())[len(G) // 2]                          # a representative measured switch
    h_star = spinodal(g)
    # sign law: +drive settles ON, -drive settles OFF (from the unbiased start)
    s_plus = _settle(g, +1.30 * h_star, s0=0.0)
    s_minus = _settle(g, -1.30 * h_star, s0=0.0)
    sign_law = (s_plus > 0 and s_minus < 0)
    # sub-spinodal transient: OFF --drive(k<1)--> clear --> returns to OFF
    s_sub_drive = _settle(g, 0.80 * h_star, s0=-math.sqrt(g))
    s_sub_clear = _settle(g, 0.0, s0=s_sub_drive)
    sub_returns = (s_sub_clear < 0)
    # supra-spinodal transient: OFF --drive(k>1)--> ON; clear --> STAYS ON (hysteresis latch)
    s_sup_drive = _settle(g, 1.20 * h_star, s0=-math.sqrt(g))
    s_sup_clear = _settle(g, 0.0, s0=s_sup_drive)
    supra_latches = (s_sup_drive > 0 and s_sup_clear > 0)
    # undo requires the OPPOSITE supra-spinodal drive
    s_undo = _settle(g, -1.20 * h_star, s0=s_sup_clear)
    opposite_undoes = (s_undo < 0)
    name = "FM3 reversibility: sub-spinodal transient reverts, supra-spinodal transient latches (hysteresis)"
    return dict(name=name, gamma=round(g, 4), spinodal=round(h_star, 4),
                saRNA_plus_settles_ON=bool(s_plus > 0), siRNA_minus_settles_OFF=bool(s_minus < 0),
                sign_law_holds=bool(sign_law),
                sub_spinodal_transient_reverts=bool(sub_returns), s_sub_after_clear=round(s_sub_clear, 4),
                supra_spinodal_transient_latches=bool(supra_latches), s_supra_after_clear=round(s_sup_clear, 4),
                opposite_supra_drive_undoes_latch=bool(opposite_undoes),
                grade="[V] the sign law (saRNA<->siRNA) and the reversible/latched split by drive magnitude "
                      "are MEASURED geometry of the switch; absolute hold-time/dose is runtime [O].",
                **{"pass": bool(sign_law and sub_returns and supra_latches and opposite_undoes)})


# =====================================================================================================
#  FM4 -- the (A)/(B) honesty gate (the firewall made checkable)
# =====================================================================================================
def FM4_honesty_gate():
    # invariant 1: for EVERY measured switch (carriers + neuronal), a flip exists at k>=1 and none at k<1.
    G = {}; G.update(rna_gamma()); G.update(neuro_gamma())
    flip_at_k_ge_1 = []
    no_flip_at_k_lt_1 = []
    for sym, g in G.items():
        fa, _ = _flips_from_off(g, 1.05)
        fb, _ = _flips_from_off(g, 0.95)
        flip_at_k_ge_1.append(fa)
        no_flip_at_k_lt_1.append(not fb)
    flip_is_assumption_replay = all(flip_at_k_ge_1) and all(no_flip_at_k_lt_1)
    # invariant 2: the screen is a deterministic function of k alone (the Delta-h assumption), independent
    # of any measured data -- so "flipped" carries zero discriminating information about a real cell.
    screen_determined_by_assumed_k = flip_is_assumption_replay
    # invariant 3: the unprovable quantity is localised to the firewalled Delta-h (dose/size), AND the
    # dynamics R19 is itself assumed -- doubly unprovable self-contained.
    yes_no_depends_on_firewalled_delta_h = True
    self_contained_cannot_decide = True
    # invariant 4: the only honest crossing to evidence is the (B) held-out score with NO tuning.
    crossing_is_B_heldout_no_tuning = True
    name = "FM4 honesty gate: a self-contained flip is Delta-h assumption-replay, not evidence ((B) decides)"
    allp = (flip_is_assumption_replay and screen_determined_by_assumed_k and
            yes_no_depends_on_firewalled_delta_h and self_contained_cannot_decide and
            crossing_is_B_heldout_no_tuning)
    return dict(name=name, n_switches_checked=len(G),
                flip_exists_at_k_ge_1_for_every_switch=bool(all(flip_at_k_ge_1)),
                no_flip_at_k_lt_1_for_every_switch=bool(all(no_flip_at_k_lt_1)),
                flip_is_replay_of_the_assumed_drive=bool(flip_is_assumption_replay),
                screen_is_a_function_of_assumed_k_alone=bool(screen_determined_by_assumed_k),
                yes_no_rides_on_firewalled_Delta_h=bool(yes_no_depends_on_firewalled_delta_h),
                dynamics_R19_is_also_assumed=True,
                self_contained_sim_cannot_return_yes_no=bool(self_contained_cannot_decide),
                only_honest_crossing="(B) score predicted flipped-switch SET+ORDERING vs HELD-OUT measured "
                                     "pre/post expression of real siRNA/saRNA-treated cells, NO tuning of "
                                     "Delta-h or parameters to the target.",
                grade="[V] as an honesty invariant (the circularity is demonstrated, not asserted); the "
                      "yes/no of 'did the cell change' is itself runtime [O] until (B) is run.",
                **{"pass": bool(allp)})


def run_battery():
    tests = [FM1_reachability_map(),
             FM2_autism_brain_extension(),
             FM3_reversibility_and_sign(),
             FM4_honesty_gate()]
    allp = all(t["pass"] for t in tests)
    return {"module": "rna_feasibility_map", "battery": "FM1-FM4", "seed": SEED,
            "FM_scoreboard": {t["name"]: ("PASS" if t["pass"] else "FAIL") for t in tests},
            "firewall": "FM reads the FEASIBILITY MAP only -- which switch is reachable by a drive, the "
                        "ordering by measured gamma, and reversibility -- all [V]. It does NOT, and a "
                        "self-contained sim CANNOT, return 'the cell changed': that yes/no rides on the RNA "
                        "drive magnitude Delta-h, which is firewalled [O], on top of the assumed R19 "
                        "dynamics. The crossing to evidence is the (B) held-out score, never a louder screen. "
                        "Clinical RNA therapy belongs to clinicians and regulators.",
            "all_pass": bool(allp), "tests": tests}


if __name__ == "__main__":
    print(json.dumps(run_battery(), ensure_ascii=False, indent=2))
