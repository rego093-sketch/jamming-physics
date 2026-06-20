#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_cytopenia.py  --  EMERGENT lineage-targeted autoimmune CYTOPENIA (a latched autoreactive clone attacking a
hematopoietic lineage output) and its basin-acting restoration by direct coupled stochastic simulation (the
hematologic composition of T23 + T27 + T19, not asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D6, T33.]

WHY THIS EXISTS (v0.11.0). Three measured results in this package compose exactly onto autoimmune cytopenias
(autoimmune hemolytic anemia, ITP, autoimmune neutropenia, pure red-cell aplasia, and the cytopenias of large
granular-lymphocyte disease): T23 MEASURED that an escaped self-clone LATCHES ON past the +spinodal break; T27
MEASURED that a deep TRANSIENT re-tolerization pulse re-flips it OFF durably whereas sub-critical suppression
relapses on withdrawal; T19 MEASURED that combining a basin-acting cure with a population-support layer accelerates
recovery WITHOUT changing the destination, while support ALONE is insufficient against an ongoing driver. The
lineage-specific fact here is that the autoreactive clone's target is a PRODUCED CELL LINEAGE (the bone-marrow
output): while the clone is ON it raises the clearance of the lineage, so the lineage output COLLAPSES to a
cytopenic floor. The roadmap asks for the break-gated output collapse, the durable basin-acting restoration vs
relapsing suppression, the combination (cure + lineage support) with support-alone insufficiency, and the honest
sub-threshold control. The VP discipline is emergence: all of it must come OUT of the SAME R19 substrate, MEASURED.

This module couples the autoreactive clone (an R19 switch in the adaptive compartment, residual self-drive
base·spinodal, bistable) to a produced lineage output L (the blood-cell count) whose clearance is raised by the
clone's EFFECTOR intensity (the relu mean of the switch field -- so sub-critical suppression DAMPENS the attack
without silencing it, the T27-honest statement), under cellular noise,

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt)·ξ,    attack = ⟨max(s,0)⟩ / √γ,
    dL = ( production(t) − (clear_base + clear_attack · attack) · L ) dt,

with h(t) the autoimmune insult / re-tolerization pulse / sub-critical suppressor, and production optionally given
a TRANSIENT lineage-support boost. The collapse, the restoration, the combination, and the controls are all
MEASURED from the coupled trajectories. Nothing is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. LINEAGE OUTPUT COLLAPSES, GATED BY THE T23 BREAK. With the clone tolerant (OFF) the lineage output sits at its
     healthy level; once the autoreactive clone is LATCHED ON, the raised clearance collapses the output to a
     cytopenic FLOOR -- and the collapse is GATED by the +spinodal break: a SUB-spinodal autoimmune insult does NOT
     latch the clone and the output stays healthy, while a SUPRA-spinodal insult latches it and the output
     collapses. The cytopenia is the T23 break read out on a produced lineage, MEASURED.
  2. RE-TOLERIZATION RESTORES THE OUTPUT DURABLY vs SUPPRESSION-ONLY RELAPSES -- the central claim, as coupled
     trajectories. A deep TRANSIENT re-tolerization pulse (T27) flips the clone OFF, the attack ceases, and the
     lineage output RECOVERS to healthy and STAYS there after withdrawal (durable). A sub-critical suppressor held
     continuously only DAMPENS the attack -- the output partially recovers WHILE applied (contained, not cured) --
     and on WITHDRAWAL the attack resumes and the output RE-COLLAPSES to the cytopenic floor (relapse). Basin-acting
     restoration is the DURABLE class; suppression-only is containment-not-cure, MEASURED.
  3. COMBINATION (CURE + LINEAGE SUPPORT): SUPPORT ALONE IS INSUFFICIENT; COMBINATION ACCELERATES WITHOUT CHANGING
     THE DESTINATION (the T19 mirror). A transient lineage-support boost WITHOUT re-tolerization raises the output
     only transiently and it RE-COLLAPSES (the ongoing attack clears the supported lineage -- support alone is
     insufficient). The COMBINATION (re-tolerization + the same transient support) reaches the healthy destination
     FASTER than re-tolerization alone, but to the SAME destination (the cure sets where the output lands; support
     only sets how fast) -- MEASURED time-to-recovery shorter, final level equal.
  4. SUB-THRESHOLD RE-TOLERIZATION FAILS (honest control). A sub-critical re-tolerization pulse does NOT restore the
     output -- the clone refills ON on withdrawal and the output stays at the cytopenic floor: the restoration is a
     basin/threshold property, not a graded improvement, MEASURED.

TREATMENT DIRECTION (roadmap discipline -- CLASS only, never agent/dose). The dynamics separate basin-acting
RE-TOLERIZATION of the lineage-attacking clone (durable restoration of the output) from chronic SUPPRESSION
(containment; relapse on withdrawal), and show lineage SUPPORT as an accelerant that is insufficient alone against
an ongoing attack but useful in COMBINATION with the cure (faster recovery, same destination). This is a
re-description of autoimmune-cytopenia dynamics in the R19 formalism and a principled treatment DIRECTION; it is NOT
a drug, dose, schedule, clinical recommendation, or VP validation, and NOT medical advice.

GRADES (C3): the break-gated output collapse, the durable-vs-relapsing restoration, the combination
(support-alone-insufficient, combination-accelerates-same-destination), and the sub-threshold control are [V]
emergent (measured from the coupled clone+lineage trajectories). The ABSOLUTE counts / clearance rates / recovery
times -- set by the production and clearance scales, the support boost, and the free cellular-noise scale D -- are
[O], no fabricated numbers, and every clinical scale stays [O] with a stated obstacle. Determinism: fixed seed,
BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_CLONE   = "lymphoid_adaptive"               # the adaptive compartment carrying the autoreactive clone
_LINEAGE = "bone_marrow_hematopoiesis"       # the attacked produced lineage (RUNX1 hematopoietic output)

_N        = 400       # clone cells
_DT       = 0.01
_D        = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_BASE     = 0.30      # residual self-drive of the escaped clone (× spinodal; sub-spinodal -> bistable); [O]
_PULSE    = 800       # phase-A duration (re-tolerization pulse / suppressor hold / support boost)
_TOTAL    = 3000      # total steps (covers phase A + recovery/relapse settle)
_SUPRA    = 0.30      # supra-threshold margin above suppress_crit for the re-tolerization pulse
_SUB      = 0.20      # sub-critical margin below suppress_crit for the suppressor / failed pulse

# produced-lineage output layer (production - clearance; clearance raised by clone effector intensity)
_PROD     = 1.0       # base production (arbitrary; [O])
_CLEAR_B  = 0.15      # baseline clearance (healthy output = PROD/CLEAR_B); [O]
_CLEAR_A  = 0.90      # attack-driven extra clearance (cytopenic floor = PROD/(CLEAR_B+CLEAR_A)); [O]
_BOOST    = 3.0       # transient lineage-support production boost (× base); [O]
_HEALTHY  = _PROD / _CLEAR_B
_ROOTG    = None      # set per call


def _cytopenia_run(g, mode, base=_BASE, insult=0.0, pulse=_PULSE, total=_TOTAL, boost=_BOOST,
                   D=_D, N=_N, dt=_DT, seed=SEED):
    """MEASURE coupled (clone, lineage-output) trajectories. mode selects the intervention applied in phase A
    (t<pulse), withdrawn after. Returns (output/healthy trajectory, attack-intensity trajectory)."""
    rng = np.random.default_rng(seed); sp = spinodal(g); rootg = math.sqrt(g)
    crit = 1.0 + base                                  # the negative saddle-node suppression depth (T27)
    sq = math.sqrt(2.0 * D * dt)
    if mode in ("healthy", "break"):
        s = np.full(N, -rootg)                         # clone tolerant (OFF)
        L = _HEALTHY
    else:
        s = np.full(N, rootg)                          # established disease: clone latched ON
        L = _PROD / (_CLEAR_B + _CLEAR_A)              # start at the cytopenic floor
    trajL = np.empty(total); trajA = np.empty(total)
    for t in range(total):
        inA = t < pulse
        if mode == "break":
            h = (insult * sp) if inA else (base * sp)                       # autoimmune insult, then residual
        elif mode in ("retolerize", "retolerize_support"):
            h = ((base - (crit + _SUPRA)) * sp) if inA else (base * sp)     # supra re-tolerization pulse, withdraw
        elif mode in ("suppress_withdrawn", "subthreshold"):
            h = ((base - (crit - _SUB)) * sp) if inA else (base * sp)       # sub-critical hold/pulse, withdraw
        else:                                                              # healthy / attacked / support_only
            h = base * sp                                                  # clone untouched
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
        attack = float(np.clip(s, 0.0, None).mean()) / rootg               # effector intensity (relu mean)
        prod = _PROD * (boost if (mode in ("support_only", "retolerize_support") and inA) else 1.0)  # TRANSIENT
        L += (prod - (_CLEAR_B + _CLEAR_A * attack) * L) * dt; L = max(L, 0.0)
        trajL[t] = L / _HEALTHY; trajA[t] = attack
    return trajL, trajA


def _t_recover(trajL, thresh=0.9):
    for t in range(len(trajL)):
        if trajL[t] >= thresh:
            return t
    return None


def _coarse_monotone(traj, rising=True, nb=10, tol=0.03):
    blk = max(1, len(traj) // nb)
    means = [float(traj[i:i + blk].mean()) for i in range(0, len(traj) - blk + 1, blk)]
    if rising:
        return all(means[i + 1] >= means[i] - tol for i in range(len(means) - 1))
    return all(means[i + 1] <= means[i] + tol for i in range(len(means) - 1))


def emergent_cytopenia(gammas, D=_D):
    g_clone = gammas[_CLONE]; sp_ref = spinodal(g_clone)

    # (1) LINEAGE OUTPUT COLLAPSE, GATED BY THE T23 BREAK
    trajL_h, _ = _cytopenia_run(g_clone, "healthy", D=D)
    trajL_att, trajA_att = _cytopenia_run(g_clone, "attacked", D=D)
    healthy_out = float(trajL_h[-int(len(trajL_h) * 0.1):].mean())
    floor_out = float(trajL_att[-int(len(trajL_att) * 0.1):].mean())
    # break gating: sub-spinodal insult (no break, output stays healthy) vs supra-spinodal (break, collapse)
    trajL_sub, _ = _cytopenia_run(g_clone, "break", insult=0.70, D=D)
    trajL_sup, _ = _cytopenia_run(g_clone, "break", insult=1.30, D=D)
    out_sub = float(trajL_sub[-int(len(trajL_sub) * 0.1):].mean())
    out_sup = float(trajL_sup[-int(len(trajL_sup) * 0.1):].mean())
    collapses = bool(healthy_out >= 0.85 and floor_out <= 0.25)
    break_gated = bool(out_sub >= 0.7 and out_sup <= 0.25)
    collapse_ok = bool(collapses and break_gated)

    # (2) DURABLE RE-TOLERIZATION vs RELAPSING SUPPRESSION (coupled trajectories)
    trajL_retol, trajA_retol = _cytopenia_run(g_clone, "retolerize", D=D)
    trajL_supp, trajA_supp = _cytopenia_run(g_clone, "suppress_withdrawn", D=D)
    retol_end = float(trajL_retol[-int(len(trajL_retol) * 0.1):].mean())
    supp_hold = float(trajL_supp[_PULSE - 100:_PULSE].mean())     # output WHILE suppressor applied (contained)
    supp_end = float(trajL_supp[-int(len(trajL_supp) * 0.1):].mean())  # output AFTER withdrawal (relapsed)
    retol_durable = bool(retol_end >= 0.85 and trajA_retol[-1] <= 0.1)
    supp_contains = bool(supp_hold > floor_out + 0.05)            # some recovery while applied
    supp_relapses = bool(supp_end <= 0.25 and trajA_supp[-1] >= 0.8)
    restore_ok = bool(retol_durable and supp_contains and supp_relapses)

    # (3) COMBINATION: support-alone insufficient; combination accelerates, same destination (T19)
    trajL_supp_only, _ = _cytopenia_run(g_clone, "support_only", D=D)
    trajL_combo, _ = _cytopenia_run(g_clone, "retolerize_support", D=D)
    support_only_end = float(trajL_supp_only[-int(len(trajL_supp_only) * 0.1):].mean())
    combo_end = float(trajL_combo[-int(len(trajL_combo) * 0.1):].mean())
    t_rec_retol = _t_recover(trajL_retol)
    t_rec_combo = _t_recover(trajL_combo)
    support_insufficient = bool(support_only_end <= 0.30)
    combo_same_destination = bool(abs(combo_end - retol_end) < 0.12 and combo_end >= 0.85)
    combo_faster = bool(t_rec_combo is not None and t_rec_retol is not None and t_rec_combo < t_rec_retol)
    combination_ok = bool(support_insufficient and combo_same_destination and combo_faster)

    # (4) SUB-THRESHOLD RE-TOLERIZATION FAILS (honest control)
    trajL_subthr, trajA_subthr = _cytopenia_run(g_clone, "subthreshold", D=D)
    subthr_end = float(trajL_subthr[-int(len(trajL_subthr) * 0.1):].mean())
    subthreshold_fails = bool(subthr_end <= 0.25 and trajA_subthr[-1] >= 0.8)
    control_ok = bool(subthreshold_fails)

    ok = bool(collapse_ok and restore_ok and combination_ok and control_ok)
    return dict(
        clone=_CLONE, gamma_clone=round(g_clone, 6), spinodal=round(sp_ref, 6),
        lineage=_LINEAGE, gamma_lineage=round(gammas[_LINEAGE], 6), noise_D=D, residual_self_drive=_BASE,
        healthy_output=round(_HEALTHY, 3), cytopenic_floor_norm=round(floor_out, 3),
        output_collapse=dict(healthy_output_norm=round(healthy_out, 3), attacked_output_norm=round(floor_out, 3),
                             break_sub_spinodal_output=round(out_sub, 3), break_supra_spinodal_output=round(out_sup, 3),
                             collapses=bool(collapses), break_gated=bool(break_gated), collapse_ok=bool(collapse_ok)),
        durable_vs_relapsing=dict(retolerize_output_end=round(retol_end, 3),
                                  suppress_output_while_applied=round(supp_hold, 3),
                                  suppress_output_after_withdrawal=round(supp_end, 3),
                                  retolerize_durable=bool(retol_durable), suppress_contains=bool(supp_contains),
                                  suppress_relapses=bool(supp_relapses), restore_ok=bool(restore_ok)),
        combination=dict(support_only_output_end=round(support_only_end, 3), combination_output_end=round(combo_end, 3),
                         retolerize_alone_output_end=round(retol_end, 3),
                         t_recover_retolerize=t_rec_retol, t_recover_combination=t_rec_combo,
                         support_alone_insufficient=bool(support_insufficient),
                         combination_same_destination=bool(combo_same_destination),
                         combination_faster=bool(combo_faster), combination_ok=bool(combination_ok)),
        sub_threshold_control=dict(subthreshold_output_end=round(subthr_end, 3),
                                   subthreshold_fails=bool(subthreshold_fails), control_ok=bool(control_ok)),
        all_pass=ok,
        grade="[V] lineage-targeted autoimmune CYTOPENIA and its basin-acting restoration EMERGE from a clone+lineage "
              "coupling: a latched autoreactive clone (T23) raises the clearance of a produced lineage so the output "
              "COLLAPSES to a cytopenic floor -- gated by the +spinodal break (a sub-spinodal insult leaves the "
              "output healthy, a supra-spinodal one collapses it); a deep TRANSIENT re-tolerization pulse (T27) "
              "ceases the attack and the output RECOVERS to healthy DURABLY, whereas a sub-critical suppressor only "
              "DAMPENS the attack (output partially recovers WHILE applied) and RE-COLLAPSES on withdrawal (relapse); "
              "lineage SUPPORT alone is insufficient (the ongoing attack clears the supported output -- re-collapses) "
              "while the COMBINATION reaches the healthy destination FASTER than the cure alone but to the SAME "
              "destination (T19 -- cure sets the destination, support the rate); and a sub-threshold pulse fails "
              "(honest control) -- measured, not assumed; [O] absolute counts / clearance rates / recovery times "
              "(production & clearance scales, support boost, cellular-noise scale D); treatment = CLASS (basin-acting "
              "re-tolerization, support as accelerant only), never agent / dose / recommendation")


def run(gammas):
    """T33: emergent lineage-targeted autoimmune cytopenia -- a latched autoreactive clone (T23) attacking a
    produced hematopoietic lineage collapses its output (break-gated), basin-acting re-tolerization (T27) restores
    it durably while suppression-only relapses, lineage support alone is insufficient but the combination
    accelerates recovery to the same destination (T19), with an honest sub-threshold control."""
    r = emergent_cytopenia(gammas)
    return dict(T33=dict(target="T33",
                         claim="lineage-targeted autoimmune CYTOPENIA EMERGES from a clone+lineage coupling: a "
                               "latched autoreactive clone (T23) raises lineage clearance so the produced output "
                               "COLLAPSES to a cytopenic floor (gated by the +spinodal break), a deep TRANSIENT "
                               "re-tolerization (T27) restores the output DURABLY while sub-critical suppression "
                               "only contains and RE-COLLAPSES on withdrawal, lineage SUPPORT alone is insufficient "
                               "but the COMBINATION reaches the SAME healthy destination FASTER (T19 -- cure sets "
                               "destination, support sets rate), and a sub-threshold pulse fails; treatment is "
                               "direction/class only and absolute counts stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T33"]["result"]
    print("LINEAGE-TARGETED AUTOIMMUNE CYTOPENIA (clone=%s γ=%.4f -> lineage=%s γ=%.4f, spinodal=%.4f, residual=%.2f, "
          "healthy_output=%.2f, D=%.3f):" % (r["clone"], r["gamma_clone"], r["lineage"], r["gamma_lineage"],
                                             r["spinodal"], r["residual_self_drive"], r["healthy_output"], r["noise_D"]))
    oc = r["output_collapse"]
    print("\n(1) LINEAGE OUTPUT COLLAPSE, gated by the T23 +spinodal break:")
    print("     healthy output=%.3f | attacked output=%.3f (cytopenic floor) -> collapses=%s"
          % (oc["healthy_output_norm"], oc["attacked_output_norm"], oc["collapses"]))
    print("     break gating: sub-spinodal insult output=%.3f (stays healthy) | supra-spinodal output=%.3f (collapses) -> gated=%s"
          % (oc["break_sub_spinodal_output"], oc["break_supra_spinodal_output"], oc["break_gated"]))
    print("     -> collapse ok=%s" % oc["collapse_ok"])
    dr = r["durable_vs_relapsing"]
    print("\n(2) DURABLE RE-TOLERIZATION vs RELAPSING SUPPRESSION (coupled output trajectories):")
    print("     re-tolerization: output end=%.3f -> durable=%s" % (dr["retolerize_output_end"], dr["retolerize_durable"]))
    print("     suppression: output while applied=%.3f (contained) -> output after withdrawal=%.3f (relapsed) -> relapses=%s"
          % (dr["suppress_output_while_applied"], dr["suppress_output_after_withdrawal"], dr["suppress_relapses"]))
    print("     -> restore ok=%s" % dr["restore_ok"])
    cb = r["combination"]
    print("\n(3) COMBINATION (cure + lineage support), T19 mirror:")
    print("     support ALONE: output end=%.3f -> insufficient=%s" % (cb["support_only_output_end"], cb["support_alone_insufficient"]))
    print("     re-tolerize alone: output end=%.3f, t_recover=%s" % (cb["retolerize_alone_output_end"], cb["t_recover_retolerize"]))
    print("     COMBINATION: output end=%.3f, t_recover=%s -> same destination=%s, faster=%s"
          % (cb["combination_output_end"], cb["t_recover_combination"], cb["combination_same_destination"], cb["combination_faster"]))
    print("     -> combination ok=%s" % cb["combination_ok"])
    sc = r["sub_threshold_control"]
    print("\n(4) SUB-THRESHOLD RE-TOLERIZATION FAILS (honest control): output end=%.3f -> fails=%s -> control ok=%s"
          % (sc["subthreshold_output_end"], sc["subthreshold_fails"], sc["control_ok"]))
    print("\nT33 all_pass:", r["all_pass"])
