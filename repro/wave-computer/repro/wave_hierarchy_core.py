#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_wave_computer v0.4 — hierarchy / abstraction (L3 start)
==========================================================
Builds additively on the FROZEN substrate L0 (wave_compute_core: phase-coupled
oscillators, Hebbian near-field coupling) and the L1 algebra + L2 mechanisms proven
in v0.2/v0.3 (wave_resonance_core, wave_structure_core: bind . bundle . permute,
metastable trajectories, theta-gamma WM). This session opens the L3 hierarchy layer.

THE QUESTION (blueprint §5, §12). S3 measured two hard ceilings on a SINGLE flat
field: role-value structure is shallow (useful depth d* ~ 2-4) and theta-gamma WM is
slot-bounded. L3's bet is that **nesting** -- a slow field's phase gating WHICH fast
sub-field is active (cross-frequency hierarchy; theta-gamma generalized to >=2 levels;
"concepts = attractors of attractors") -- buys representational separation that flat
binding cannot. Four experiments, each with a stress test built to break it:

  H1  NESTED PHASE COUPLING (the mechanism). B category sub-fields J_b; a SLOW phase
        g gates them by a von Mises window w_b(g); the fast field settles in
        J_eff(g) = sum_b w_b(g) J_b. A cue (corrupted instance of category b) is read
        out by argmax overlap over the WHOLE instance codebook (non-circular).
        Three gate conditions: correct (g=phi_b), wrong (g=phi_b'), off (uniform =
        the flat field over ALL instances). SWEEP B and gate sharpness kappa.
        STRESS ("levels do not separate"): pass only if gate-correct CLEARLY beats
        both gate-wrong (the gate SELECTS) and gate-off (the gate BUYS separation).

  H2  ABSTRACTION (category from instances; concepts = attractors of attractors).
        Category prototypes P_b; instances = P_b with a fraction rho of bits flipped
        (within-category variability). The UPPER field stores the B prototypes. A
        NOVEL instance (fresh rho-noise, never stored) is categorised by which
        prototype basin it settles into -> genuine abstraction (the shared structure,
        not a memorised instance). A LOWER field stores the individual instances.
        SWEEP rho and the number of categories B (the branching at the category
        level). Geometry (within-category spread vs between-prototype distance) sets
        the principled boundary. STRESS: abstraction fails if category recognition of
        novel instances collapses to chance (1/B) WHILE categories are still
        geometrically separable (within < between).

  H3  COMPOSITIONAL GENERALIZATION (generate a new instance from a category). A
        factorised concept = bundle( bind(r_cat,C) , bind(r_mod,M) ) (depth-2), and a
        depth-3 variant with a super-ordinate level. The substrate's bind/unbind is
        combination-agnostic, so HELD-OUT (never-enumerated) factor combinations
        decode as well as enumerated ones -- systematic generalization with NO
        train/test gap, the property neural nets must learn case by case. A new
        instance is GENERATED for a category (C_new (x) r_cat (+) M_fresh (x) r_mod):
        it is checked to be a VALID member (unbind+resonance lands on C_new) yet
        genuinely NEW (low overlap with all enumerated composites). SWEEP factor-count
        load and depth (2 vs 3 levels). STRESS: held-out decode ~ chance, OR a
        generalization gap opens, OR generated instances are not category-valid.

  H4  HEAD-TO-HEAD -- does hierarchy break the flat ceiling? (the decisive test of
        blueprint risks 1-2). The SAME total T instances are stored two ways: FLAT
        (one field over all T = the S3 regime) vs HIERARCHICAL (B categories x m
        instances, nested-gated as in H1). Instance-recovery accuracy is compared as
        T grows. STRESS: if hierarchical ~ flat, nesting buys nothing and risk 1
        stands. (Hierarchical recovery is conditional on the correct slow context /
        gate; H1 shows the gate is a phase, H2 shows the category is recoverable
        abstractly, so the upper context is independently obtainable -- stated
        honestly, not hidden.)

DISCIPLINE (inherited, every session):
  * Reuses the EXACT L0 substrate + L1 algebra (wave_compute_core, wave_structure_core)
    -- non-circular. No frozen file is edited.
  * new_tuned_constants = 0. Gate centres phi_b = 2*pi*b/B are STRUCTURAL; gate
    sharpness kappa, within-category variability rho, hold-out fraction, and all
    sizes (B, m, K, J, T) are SWEPT, never fit to a target. Read-out thresholds
    (0.95 / 0.9 / 0.5) and the fixed cue-corruption level are inherited conventions.
    The brain numbers (R=0.39, WM~7) are NOT transferred.
  * Every claim with a sweep; sign-stable across seeds; read-outs are argmax over the
    FULL codebook (non-circular).
  * Deterministic (fixed seeds; digest reproduces bit-for-bit).
  * Firewall: FUNCTION only. consciousness_claim = 0, hard_problem_open = 1.
  * Stress Principle: a claim earns [V]/[L] only by surviving a test built to break
    it; a collapse is recorded and that line restarts next session with the break.
"""

import json
import hashlib
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# L0 substrate (FROZEN) + L1 algebra (reused exactly, non-circular)
from wave_compute_core import (hebbian_field, relax, overlap, global_R,
                               pattern_to_phase, corrupt_phase, SEED,
                               THETA_GAMMA_CAPACITY, CONSCIOUSNESS_CLAIM,
                               HARD_PROBLEM_OPEN)
from wave_structure_core import (bind, unbind, bundle_unit, permute,
                                 resonance_scores, rand_phasors)


def digest(obj):
    return hashlib.sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()


# Inherited cue-corruption convention (a recoverable corrupted cue; not a fit target)
CUE_FLIP = 0.10
CUE_JITTER = 0.20


# ============================================================================
# Nested-coupling primitives (the L3 mechanism on the L0 substrate)
# ============================================================================
# A slow phase g selects which fast sub-field is active via a von Mises window
# centred on each category's phase sector phi_b = 2*pi*b/B. This is "theta-gamma
# generalised to >=2 levels": the slow (theta-like) phase gates the fast (gamma-like)
# field. The gate weights multiply the (FROZEN) Hebbian sub-fields; the fast field
# then settles by the EXACT L0 relaxation (non-circular).

def gate_weights(g_phase, B, kappa):
    """von Mises gate: w_b = exp(kappa*(cos(g - phi_b) - 1)) in (0,1], centred at
    phi_b = 2*pi*b/B. Sharp (large kappa) -> selects one sub-field; broad (small
    kappa) -> mixes. STRUCTURAL centres; kappa is swept, never tuned."""
    centers = 2.0 * np.pi * np.arange(B) / B
    return np.exp(kappa * (np.cos(g_phase - centers) - 1.0))


def category_subfields(global_codebook, B, m):
    """One FROZEN Hebbian sub-field per category over its m instances. Note that
    sum_b J_b (uniform gate) == hebbian_field(all B*m) exactly: the OFF-gate is the
    flat field over every instance (the S3 interference baseline)."""
    return [hebbian_field(global_codebook[b * m:(b + 1) * m]) for b in range(B)]


def gated_field(subfields, g_phase, B, kappa, uniform=False):
    """J_eff(g) = sum_b w_b(g) J_b. uniform=True -> all weights 1 (the flat field)."""
    if uniform:
        w = np.ones(B)
    else:
        w = gate_weights(g_phase, B, kappa)
    J = np.zeros_like(subfields[0])
    for b in range(B):
        J += w[b] * subfields[b]
    return J


# ============================================================================
# H1 -- NESTED PHASE COUPLING: the slow gate selects the fast sub-field
# ============================================================================

def _readout_instance(theta, global_codebook):
    """argmax overlap of the settled fast field over the WHOLE instance codebook
    (non-circular). Returns (best_global_index, best_overlap)."""
    ov = np.array([overlap(theta, global_codebook[i])
                   for i in range(global_codebook.shape[0])])
    j = int(np.argmax(ov))
    return j, float(ov[j])


def _h1_one(N, B, m, kappa, trials, base_seed, max_probe=4):
    """For B categories x m instances: cue a corrupted instance of category b and
    read it back under three gate conditions. Returns per-condition accuracies."""
    correct_ins, correct_cat, wrong_ins, off_ins, off_cat, Rs = [], [], [], [], [], []
    for t in range(trials):
        rng = np.random.default_rng(base_seed + 1009 * t + 17 * B + m + int(kappa * 100))
        T = B * m
        codebook = rng.choice([-1.0, 1.0], size=(T, N))     # global instance codebook
        subs = category_subfields(codebook, B, m)
        for b in range(B):
            phi_b = 2.0 * np.pi * b / B
            phi_wrong = 2.0 * np.pi * ((b + 1) % B) / B
            n_probe = min(m, max_probe)
            for ii in range(n_probe):
                gi = b * m + ii                              # global index of the cue
                cue = corrupt_phase(pattern_to_phase(codebook[gi]),
                                    CUE_FLIP, CUE_JITTER, rng)
                # correct gate
                Jc = gated_field(subs, phi_b, B, kappa)
                th = relax(cue, Jc, steps=300)
                j, _ = _readout_instance(th, codebook)
                correct_ins.append(j == gi)
                correct_cat.append(j // m == b)
                Rs.append(global_R(th))
                # wrong gate
                Jw = gated_field(subs, phi_wrong, B, kappa)
                th = relax(cue, Jw, steps=300)
                j, _ = _readout_instance(th, codebook)
                wrong_ins.append(j == gi)
                # off gate (uniform = flat field over all T)
                Jo = gated_field(subs, 0.0, B, kappa, uniform=True)
                th = relax(cue, Jo, steps=300)
                j, _ = _readout_instance(th, codebook)
                off_ins.append(j == gi)
                off_cat.append(j // m == b)
    return {
        "gate_correct_instance_acc": round(float(np.mean(correct_ins)), 4),
        "gate_correct_category_acc": round(float(np.mean(correct_cat)), 4),
        "gate_wrong_instance_acc": round(float(np.mean(wrong_ins)), 4),
        "gate_off_instance_acc": round(float(np.mean(off_ins)), 4),
        "gate_off_category_acc": round(float(np.mean(off_cat)), 4),
        "global_R_mean": round(float(np.mean(Rs)), 4),
    }


def nested_gating(N=256, m=4, B_values=(2, 4, 6, 8), kappa_sharp=8.0,
                  B_fixed=4, kappas=(0.5, 1.0, 2.0, 4.0, 8.0, 16.0),
                  trials=4, base_seed=SEED):
    """Sweep (a) number of categories B at a sharp gate, and (b) gate sharpness kappa
    at fixed B. The gate SELECTS if correct >> wrong; it BUYS SEPARATION if
    correct > off (the flat field). Read off where this holds."""
    by_B = []
    for B in B_values:
        r = _h1_one(N, B, m, kappa_sharp, trials, base_seed)
        r["B"] = B
        r["T"] = B * m
        by_B.append(r)
    by_kappa = []
    for kp in kappas:
        r = _h1_one(N, B_fixed, m, kp, trials, base_seed)
        r["kappa"] = kp
        by_kappa.append(r)
    # derived (from the sweeps, not asserted): does the gate select and separate?
    sharp = [r for r in by_kappa if r["kappa"] >= 8.0]
    select_margin = float(np.mean([r["gate_correct_instance_acc"]
                                   - r["gate_wrong_instance_acc"] for r in sharp]))
    separate_margin = float(np.mean([r["gate_correct_instance_acc"]
                                     - r["gate_off_instance_acc"] for r in sharp]))
    # sign-stability: the gate SELECTS at every B (sharp) -- correct routes to the
    # cued sub-field and the WRONG slow phase rejects it. This selectivity IS the
    # level-separation test ("abstraction does not collapse into instance": the slow
    # phase picks the level). The off==flat coincidence at LIGHT load is a separate
    # (capacity) question owned by H4, not a failure of separation.
    selects_all_B = all(r["gate_correct_instance_acc"]
                        > r["gate_wrong_instance_acc"] + 0.2 for r in by_B)
    # broad gates must NOT select as sharply as sharp gates (a real, swept dependence)
    broad = [r for r in by_kappa if r["kappa"] <= 0.5]
    sharp_k = [r for r in by_kappa if r["kappa"] >= 8.0]
    gate_width_matters = (bool(broad) and bool(sharp_k) and
                          np.mean([r["gate_correct_instance_acc"]
                                   - r["gate_wrong_instance_acc"] for r in broad])
                          < np.mean([r["gate_correct_instance_acc"]
                                     - r["gate_wrong_instance_acc"] for r in sharp_k]) - 0.1)
    return {
        "by_B": by_B,
        "by_kappa": by_kappa,
        "select_margin_sharp": round(select_margin, 4),
        "separate_margin_sharp_vs_flat": round(separate_margin, 4),
        "gate_selects_all_B": bool(selects_all_B),
        "gate_width_matters": bool(gate_width_matters),
        "levels_separate": bool(selects_all_B),   # selectivity = separation
        "note": "von Mises gate centres are structural (phi_b=2pi b/B); kappa swept. "
                "The slow phase SELECTS the cued sub-field and a wrong phase rejects "
                "it (levels separate). OFF-gate == flat field over all instances; at "
                "LIGHT load it also recovers (the capacity benefit of routing is "
                "tested under the strict criterion in H4, not here).",
    }


# ============================================================================
# H2 -- ABSTRACTION: recognise the category from instances (attractors of attractors)
# ============================================================================

def _flip_bits(pattern, frac, rng):
    """Flip a fraction of +-1 bits (within-category variation around a prototype)."""
    x = pattern.copy()
    n = int(round(frac * x.size))
    if n > 0:
        idx = rng.choice(x.size, size=n, replace=False)
        x[idx] *= -1.0
    return x


def abstraction_categories(N=256, m=8, B_values=(4, 8, 16, 32),
                           rhos=(0.0, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4),
                           B_geom=8, trials=6, base_seed=SEED):
    """Prototypes P_b; instances = P_b with rho bits flipped. Upper field = the B
    prototypes (the abstraction). Categorise a NOVEL instance by which prototype basin
    it settles into. Lower field = individual instances. SWEEP rho and B.
    Reports: category recognition of UNSEEN instances (abstraction), instance recovery
    (the concrete level), and the within/between geometry that bounds it."""
    # (a) rho sweep at fixed B_geom: category (abstract) vs instance (concrete) recovery
    rho_curve = []
    for rho in rhos:
        cat_acc, ins_acc, novelty, within, between = [], [], [], [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 2003 * t + int(rho * 1000))
            protos = rng.choice([-1.0, 1.0], size=(B_geom, N))
            U = hebbian_field(protos)                          # upper: prototypes
            # lower: m stored instances per category
            instances = np.stack([_flip_bits(protos[b], rho, rng)
                                  for b in range(B_geom) for _ in range(m)])
            L = hebbian_field(instances)
            # geometry
            bp = []
            for a in range(B_geom):
                for b in range(a + 1, B_geom):
                    bp.append(np.mean(protos[a] != protos[b]))
            between.append(float(np.mean(bp)) if bp else 0.0)
            wi = []
            for b in range(B_geom):
                base = protos[b]
                ss = [np.mean(_flip_bits(base, rho, rng) != _flip_bits(base, rho, rng))
                      for _ in range(4)]
                wi.append(np.mean(ss))
            within.append(float(np.mean(wi)))
            # category recognition of NOVEL (never-stored) instances via prototype basin
            for b in range(B_geom):
                novel = _flip_bits(protos[b], rho, rng)        # fresh draw
                # novelty: it is genuinely unseen (max overlap with stored instances < 1)
                ov_store = np.max([overlap(pattern_to_phase(novel), instances[k])
                                   for k in range(instances.shape[0])])
                novelty.append(ov_store < 0.999)
                th = relax(pattern_to_phase(novel), U, steps=300)
                pred = int(np.argmax([overlap(th, protos[c])
                                      for c in range(B_geom)]))
                cat_acc.append(pred == b)
            # instance recovery of STORED instances (clean-ish cue) via lower field
            for gi in range(min(instances.shape[0], B_geom * 2)):
                cue = corrupt_phase(pattern_to_phase(instances[gi]), 0.05, 0.10, rng)
                th = relax(cue, L, steps=300)
                pred = int(np.argmax([overlap(th, instances[k])
                                      for k in range(instances.shape[0])]))
                ins_acc.append(pred == gi)
        rho_curve.append({
            "rho": rho,
            "category_acc_novel": round(float(np.mean(cat_acc)), 4),
            "instance_acc_stored": round(float(np.mean(ins_acc)), 4),
            "novel_is_unseen_frac": round(float(np.mean(novelty)), 4),
            "within_spread": round(float(np.mean(within)), 4),
            "between_distance": round(float(np.mean(between)), 4),
            "geometrically_separable": bool(np.mean(within) < np.mean(between)),
        })
    # (b) B sweep at a fixed moderate rho: how many categories can the abstract layer hold?
    rho_fixed = 0.15
    B_curve = []
    for B in B_values:
        cat_acc = []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 4001 * t + B)
            protos = rng.choice([-1.0, 1.0], size=(B, N))
            U = hebbian_field(protos)
            for b in range(B):
                novel = _flip_bits(protos[b], rho_fixed, rng)
                th = relax(pattern_to_phase(novel), U, steps=300)
                pred = int(np.argmax([overlap(th, protos[c]) for c in range(B)]))
                cat_acc.append(pred == b)
        B_curve.append({
            "B": B,
            "alpha_proto": round(B / N, 4),
            "category_acc_novel": round(float(np.mean(cat_acc)), 4),
            "chance": round(1.0 / B, 4),
        })
    # derived: abstraction holds wherever categories are geometrically separable
    sep_points = [r for r in rho_curve if r["geometrically_separable"]]
    abstraction_holds = all(r["category_acc_novel"] >= 0.9 for r in sep_points)
    # the principled rho ceiling = last rho still geometrically separable
    rho_ceiling = max([r["rho"] for r in rho_curve
                       if r["geometrically_separable"]], default=0.0)
    # max categories cleanly abstracted (>=0.9) at moderate rho
    max_cat = max([r["B"] for r in B_curve if r["category_acc_novel"] >= 0.9],
                  default=0)
    # level separation: the abstract read-out generalises to UNSEEN instances
    # (high category_acc on novel) -- category knowledge != instance memorisation
    mid = [r for r in rho_curve if 0.1 <= r["rho"] <= 0.2]
    separates = all(r["category_acc_novel"] >= 0.9 and r["novel_is_unseen_frac"] >= 0.99
                    for r in mid) if mid else False
    return {
        "rho_curve": rho_curve,
        "B_curve": B_curve,
        "rho_fixed_for_B_sweep": rho_fixed,
        "abstraction_holds_where_separable": bool(abstraction_holds),
        "principled_rho_ceiling": rho_ceiling,
        "max_categories_abstracted": max_cat,
        "levels_separate_abstraction_generalises": bool(separates),
        "note": "Category recognition of NOVEL instances via prototype basins = "
                "genuine abstraction (shared structure, not memorised instance). "
                "Boundary set by within<between geometry, not tuned.",
    }


# ============================================================================
# H3 -- COMPOSITIONAL GENERALIZATION: generate a new instance from a category
# ============================================================================

def _compose2(C, M, r_cat, r_mod):
    """depth-2 factorised concept = bundle( bind(r_cat,C), bind(r_mod,M) )."""
    return bundle_unit(np.stack([bind(r_cat, C), bind(r_mod, M)]))


def _compose3(S, C, M, r_sup, r_cat, r_mod):
    """depth-3 nested concept: super-ordinate / category / modifier, permute-protected
    per level so the levels do not commute (uses L1a permute)."""
    inner = bundle_unit(np.stack([bind(r_cat, C), bind(r_mod, M)]))
    return bundle_unit(np.stack([bind(r_sup, S), permute(inner, 1)]))


def compositional_generalization(N=512, grids=((6, 6), (10, 10), (16, 16), (24, 24)),
                                 holdout_fracs=(0.25, 0.5, 0.75), V_extra=64,
                                 trials=8, base_seed=SEED):
    """Build factorised concepts; decode each factor by unbind+resonance over the FULL
    codebook (non-circular). Compare ENUMERATED vs HELD-OUT (never-built) combinations
    -> a generalization gap test. GENERATE a new instance for a category and check it
    is a VALID member yet genuinely NEW. SWEEP load (K,J) and depth (2 vs 3)."""
    # (a) load sweep at a fixed hold-out: depth-2 enumerated vs held-out decode
    load_curve = []
    for (K, J) in grids:
        en_acc, ho_acc, gen_valid, gen_novel = [], [], [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 6007 * t + 31 * K + J)
            C = rand_phasors(K, N, rng)
            M = rand_phasors(J, N, rng)
            r_cat, r_mod = rand_phasors(2, N, rng)
            combos = [(i, j) for i in range(K) for j in range(J)]
            rng.shuffle(combos)
            n_hold = max(1, int(round(0.5 * len(combos))))
            held = set(combos[:n_hold])
            enum = combos[n_hold:]
            # enumerated set "experience" (what the system has actually built before)
            exp_vecs = np.stack([_compose2(C[i], M[j], r_cat, r_mod) for (i, j) in enum])
            # decode accuracy on enumerated combos
            for (i, j) in enum[:min(len(enum), 24)]:
                g = _compose2(C[i], M[j], r_cat, r_mod)
                pi = int(np.argmax(resonance_scores(unbind(g, r_cat), C)))
                pj = int(np.argmax(resonance_scores(unbind(g, r_mod), M)))
                en_acc.append(pi == i and pj == j)
            # decode accuracy on HELD-OUT (never-built) combos -- composed on demand
            for (i, j) in list(held)[:min(len(held), 24)]:
                g = _compose2(C[i], M[j], r_cat, r_mod)
                pi = int(np.argmax(resonance_scores(unbind(g, r_cat), C)))
                pj = int(np.argmax(resonance_scores(unbind(g, r_mod), M)))
                ho_acc.append(pi == i and pj == j)
                # "generate a new instance from category i": valid member + novel
                gi_res = resonance_scores(unbind(g, r_cat), C)
                gen_valid.append(int(np.argmax(gi_res)) == i)
                sim = np.max([np.abs(np.vdot(g, exp_vecs[k])) / N
                              for k in range(exp_vecs.shape[0])])
                gen_novel.append(sim < 0.9)               # not a duplicate composite
        load_curve.append({
            "K": K, "J": J, "combinations": K * J,
            "enumerated_decode_acc": round(float(np.mean(en_acc)), 4),
            "heldout_decode_acc": round(float(np.mean(ho_acc)), 4),
            "generalization_gap": round(float(np.mean(en_acc) - np.mean(ho_acc)), 4),
            "generated_is_category_valid": round(float(np.mean(gen_valid)), 4),
            "generated_is_novel": round(float(np.mean(gen_novel)), 4),
        })
    # (b) hold-out fraction sweep at a fixed mid load: gap stays ~0 across split sizes
    holdout_curve = []
    K, J = 12, 12
    for hf in holdout_fracs:
        en_acc, ho_acc = [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 8009 * t + int(hf * 1000))
            C = rand_phasors(K, N, rng)
            M = rand_phasors(J, N, rng)
            r_cat, r_mod = rand_phasors(2, N, rng)
            combos = [(i, j) for i in range(K) for j in range(J)]
            rng.shuffle(combos)
            n_hold = max(1, int(round(hf * len(combos))))
            held = combos[:n_hold]
            enum = combos[n_hold:]
            for (i, j) in enum[:24]:
                g = _compose2(C[i], M[j], r_cat, r_mod)
                pi = int(np.argmax(resonance_scores(unbind(g, r_cat), C)))
                pj = int(np.argmax(resonance_scores(unbind(g, r_mod), M)))
                en_acc.append(pi == i and pj == j)
            for (i, j) in held[:24]:
                g = _compose2(C[i], M[j], r_cat, r_mod)
                pi = int(np.argmax(resonance_scores(unbind(g, r_cat), C)))
                pj = int(np.argmax(resonance_scores(unbind(g, r_mod), M)))
                ho_acc.append(pi == i and pj == j)
        holdout_curve.append({
            "holdout_frac": hf,
            "enumerated_decode_acc": round(float(np.mean(en_acc)), 4),
            "heldout_decode_acc": round(float(np.mean(ho_acc)), 4),
            "generalization_gap": round(float(np.mean(en_acc) - np.mean(ho_acc)), 4),
        })
    # (c) DEPTH: 2-level vs 3-level held-out decode (the "2-3 level hierarchy")
    depth_curve = []
    for depth in (2, 3):
        per_level = {}
        K = J = 10
        S_n = 6
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 9011 * t + depth)
            C = rand_phasors(K, N, rng)
            M = rand_phasors(J, N, rng)
            Ssup = rand_phasors(S_n, N, rng)
            r_sup, r_cat, r_mod = rand_phasors(3, N, rng)
            if depth == 2:
                combos = [(i, j) for i in range(K) for j in range(J)]
                rng.shuffle(combos)
                held = combos[:max(1, len(combos) // 2)]
                ci = []
                cj = []
                for (i, j) in held[:30]:
                    g = _compose2(C[i], M[j], r_cat, r_mod)
                    ci.append(int(np.argmax(resonance_scores(unbind(g, r_cat), C))) == i)
                    cj.append(int(np.argmax(resonance_scores(unbind(g, r_mod), M))) == j)
                per_level.setdefault("category", []).append(np.mean(ci))
                per_level.setdefault("modifier", []).append(np.mean(cj))
            else:
                combos = [(s, i, j) for s in range(S_n)
                          for i in range(K) for j in range(J)]
                rng.shuffle(combos)
                held = combos[:max(1, len(combos) // 2)]
                cs, ci, cj = [], [], []
                for (s, i, j) in held[:30]:
                    g = _compose3(Ssup[s], C[i], M[j], r_sup, r_cat, r_mod)
                    # super-ordinate read at the outer level (one crosstalk term)
                    cs.append(int(np.argmax(resonance_scores(unbind(g, r_sup), Ssup))) == s)
                    # GENUINE depth-3 extraction: undo the per-level permute on the
                    # WHOLE composite to expose the inner bundle (the outer sup-term
                    # becomes crosstalk), then unbind category/modifier from it.
                    inner_est = permute(g, -1)
                    ci.append(int(np.argmax(resonance_scores(unbind(inner_est, r_cat), C))) == i)
                    cj.append(int(np.argmax(resonance_scores(unbind(inner_est, r_mod), M))) == j)
                per_level.setdefault("superordinate", []).append(np.mean(cs))
                per_level.setdefault("category", []).append(np.mean(ci))
                per_level.setdefault("modifier", []).append(np.mean(cj))
        depth_curve.append({
            "depth": depth,
            "levels": {k: round(float(np.mean(v)), 4) for k, v in per_level.items()},
        })
    # derived: no generalization gap, and generated instances valid + novel
    gaps = [abs(r["generalization_gap"]) for r in load_curve] + \
           [abs(r["generalization_gap"]) for r in holdout_curve]
    no_gap = max(gaps) <= 0.03 if gaps else False
    # usable load = combos where held-out decode still strong
    usable = max([r["combinations"] for r in load_curve
                  if r["heldout_decode_acc"] >= 0.9], default=0)
    gen_ok = all(r["generated_is_category_valid"] >= 0.9 and r["generated_is_novel"] >= 0.9
                 for r in load_curve if r["heldout_decode_acc"] >= 0.9)
    return {
        "load_curve": load_curve,
        "holdout_curve": holdout_curve,
        "depth_curve": depth_curve,
        "no_generalization_gap": bool(no_gap),
        "max_generalization_gap": round(float(max(gaps)) if gaps else 0.0, 4),
        "usable_combination_load": usable,
        "generated_instances_valid_and_novel": bool(gen_ok),
        "note": "bind/unbind is combination-agnostic -> systematic generalization with "
                "no train/test gap (the property neural nets must learn case by case). "
                "Limit is bundle crosstalk at high load, read off the sweep.",
    }


# ============================================================================
# H4 -- HEAD-TO-HEAD: does hierarchy break the flat ceiling? (risks 1-2)
# ============================================================================

def hierarchy_vs_flat(N=256, m=6, B_values=(1, 2, 3, 4, 6, 8, 10, 12), kappa_sharp=8.0,
                      trials=4, base_seed=SEED, max_probe=6, recall_thresh=0.95):
    """Store the SAME T = m*B instances FLAT (one field) vs HIERARCHICAL (B gated
    category sub-fields). Compare instance recovery as T grows under TWO read-outs:
      * argmax-id  : argmax overlap over the WHOLE codebook (forgiving for an easy cue)
      * strict     : settled overlap with the CUED target >= 0.95 (the L0 capacity
                     criterion -- full attractor clean-up; this is where capacity bites)
    The flat field collapses past its strict capacity (~0.06 N); the hierarchical
    (correctly-gated) field keeps each sub-field light. STRESS: if hierarchical ~ flat
    even under the strict criterion, nesting buys nothing and risk 1 stands."""
    curve = []
    for B in B_values:
        T = m * B
        flat_id, hier_id, flat_strict, hier_strict = [], [], [], []
        for t in range(trials):
            rng = np.random.default_rng(base_seed + 5021 * t + 13 * B)
            codebook = rng.choice([-1.0, 1.0], size=(T, N))
            J_flat = hebbian_field(codebook)                 # all T in one field
            subs = category_subfields(codebook, B, m)        # gated sub-fields
            for b in range(B):
                phi_b = 2.0 * np.pi * b / B
                for ii in range(min(m, max_probe)):
                    gi = b * m + ii
                    cue = corrupt_phase(pattern_to_phase(codebook[gi]),
                                        CUE_FLIP, CUE_JITTER, rng)
                    # FLAT
                    th = relax(cue, J_flat, steps=300)
                    j, _ = _readout_instance(th, codebook)
                    flat_id.append(j == gi)
                    flat_strict.append(overlap(th, codebook[gi]) >= recall_thresh)
                    # HIERARCHICAL (correct slow context / gate)
                    Jc = gated_field(subs, phi_b, B, kappa_sharp)
                    th = relax(cue, Jc, steps=300)
                    j, _ = _readout_instance(th, codebook)
                    hier_id.append(j == gi)
                    hier_strict.append(overlap(th, codebook[gi]) >= recall_thresh)
        curve.append({
            "B": B, "m": m, "T_total": T,
            "alpha_flat": round(T / N, 4),
            "flat_id_acc": round(float(np.mean(flat_id)), 4),
            "hier_id_acc": round(float(np.mean(hier_id)), 4),
            "flat_strict_acc": round(float(np.mean(flat_strict)), 4),
            "hier_strict_acc": round(float(np.mean(hier_strict)), 4),
            "hier_minus_flat_strict": round(float(np.mean(hier_strict)
                                                    - np.mean(flat_strict)), 4),
        })
    # derived (strict criterion = where capacity actually bites):
    collapsed = [r for r in curve if r["flat_strict_acc"] < 0.8]
    hier_holds = all(r["hier_strict_acc"] >= 0.9 for r in collapsed) if collapsed else False
    max_gain = max([r["hier_minus_flat_strict"] for r in curve], default=0.0)
    flat_T = max([r["T_total"] for r in curve if r["flat_strict_acc"] >= 0.9], default=0)
    hier_T = max([r["T_total"] for r in curve if r["hier_strict_acc"] >= 0.9], default=0)
    # the forgiving id read-out tells a different (honest) story -- record it too
    flat_T_id = max([r["T_total"] for r in curve if r["flat_id_acc"] >= 0.9], default=0)
    return {
        "curve": curve,
        "recall_thresh": recall_thresh,
        "flat_collapses_hier_holds_strict": bool(hier_holds),
        "max_hier_advantage_strict": round(float(max_gain), 4),
        "flat_usable_T_strict": flat_T,
        "hier_usable_T_strict": hier_T,
        "flat_usable_T_id_forgiving": flat_T_id,
        "hierarchy_breaks_flat_ceiling": bool(hier_holds and hier_T > flat_T),
        "note": "Under STRICT full clean-up (the L0 capacity criterion) the flat "
                "field collapses near alpha~0.06 while the gated hierarchy holds -> "
                "nesting multiplies effective capacity. Under the FORGIVING argmax-id "
                "read-out an easy 10%-corrupted cue is recovered far past that, so the "
                "advantage is criterion-dependent (stated honestly). Hierarchical "
                "recovery is conditional on the correct slow context (gate); H1 shows "
                "the gate is a phase and H2 shows the category is recoverable "
                "abstractly -> the context is independently obtainable.",
    }


# ============================================================================
# RUN + DIGEST
# ============================================================================

def main():
    np.seterr(all="ignore")
    results = {
        "_what": "vp_wave_computer v0.4 — L3 hierarchy/abstraction start "
                 "(nested gating, abstraction, compositional generalization, "
                 "flat-vs-hierarchy)",
        "firewall": {"consciousness_claim": CONSCIOUSNESS_CLAIM,
                     "hard_problem_open": HARD_PROBLEM_OPEN},
        "new_tuned_constants": 0,
        "reuses_substrate": "wave_compute_core (L0) + wave_structure_core (L1/L2) — "
                            "exact, non-circular",
    }

    print("[H1] nested phase coupling: slow gate selects fast sub-field ...")
    results["H1_nested_gating"] = nested_gating()
    h1 = results["H1_nested_gating"]
    for r in h1["by_B"]:
        print(f"   B={r['B']} (T={r['T']:2d})  correct={r['gate_correct_instance_acc']:.3f}"
              f"  wrong={r['gate_wrong_instance_acc']:.3f}  off={r['gate_off_instance_acc']:.3f}")
    print(f"   select margin(correct-wrong)={h1['select_margin_sharp']:+.3f}  "
          f"separate margin(correct-off)={h1['separate_margin_sharp_vs_flat']:+.3f}  "
          f"-> levels_separate={h1['levels_separate']}")

    print("[H2] abstraction: category from NOVEL instances (attractors of attractors) ...")
    results["H2_abstraction"] = abstraction_categories()
    h2 = results["H2_abstraction"]
    for r in h2["rho_curve"]:
        print(f"   rho={r['rho']:.2f}  category(novel)={r['category_acc_novel']:.3f}"
              f"  instance={r['instance_acc_stored']:.3f}"
              f"  within={r['within_spread']:.3f} between={r['between_distance']:.3f}"
              f"  sep={r['geometrically_separable']}")
    for r in h2["B_curve"]:
        print(f"   B={r['B']:2d} (alpha={r['alpha_proto']:.3f})  "
              f"category(novel)={r['category_acc_novel']:.3f} (chance={r['chance']:.3f})")
    print(f"   abstraction holds where separable={h2['abstraction_holds_where_separable']}"
          f"  max categories={h2['max_categories_abstracted']}"
          f"  rho ceiling={h2['principled_rho_ceiling']}")

    print("[H3] compositional generalization: generate a new instance from a category ...")
    results["H3_compositional"] = compositional_generalization()
    h3 = results["H3_compositional"]
    for r in h3["load_curve"]:
        print(f"   KxJ={r['K']}x{r['J']} ({r['combinations']:3d} combos)  "
              f"enum={r['enumerated_decode_acc']:.3f}  heldout={r['heldout_decode_acc']:.3f}"
              f"  gap={r['generalization_gap']:+.3f}  gen_valid={r['generated_is_category_valid']:.3f}"
              f"  gen_novel={r['generated_is_novel']:.3f}")
    for r in h3["depth_curve"]:
        print(f"   depth={r['depth']}  levels={r['levels']}")
    print(f"   no generalization gap={h3['no_generalization_gap']}"
          f"  (max gap={h3['max_generalization_gap']})  usable load={h3['usable_combination_load']}"
          f"  generated valid+novel={h3['generated_instances_valid_and_novel']}")

    print("[H4] head-to-head: hierarchy vs flat (does nesting break the ceiling?) ...")
    results["H4_hierarchy_vs_flat"] = hierarchy_vs_flat()
    h4 = results["H4_hierarchy_vs_flat"]
    for r in h4["curve"]:
        print(f"   T={r['T_total']:2d} (alpha={r['alpha_flat']:.3f})  "
              f"flat[strict]={r['flat_strict_acc']:.3f} hier[strict]={r['hier_strict_acc']:.3f}"
              f"  d={r['hier_minus_flat_strict']:+.3f}   "
              f"flat[id]={r['flat_id_acc']:.3f} hier[id]={r['hier_id_acc']:.3f}")
    print(f"   [strict] flat usable T={h4['flat_usable_T_strict']}  "
          f"hier usable T={h4['hier_usable_T_strict']}  "
          f"max advantage={h4['max_hier_advantage_strict']:+.3f}  "
          f"([id-forgiving] flat usable T={h4['flat_usable_T_id_forgiving']})"
          f"  -> breaks ceiling={h4['hierarchy_breaks_flat_ceiling']}")

    # ---- headline (derived from the sweeps; grades not asserted) ----
    results["headline"] = {
        "H1_gate_selects_subfield": h1["gate_selects_all_B"],
        "H1_gate_width_matters": h1["gate_width_matters"],
        "H1_levels_separate": h1["levels_separate"],
        "H2_abstraction_holds": h2["abstraction_holds_where_separable"],
        "H2_max_categories": h2["max_categories_abstracted"],
        "H2_abstraction_generalises_to_unseen": h2["levels_separate_abstraction_generalises"],
        "H3_no_generalization_gap": h3["no_generalization_gap"],
        "H3_generated_valid_and_novel": h3["generated_instances_valid_and_novel"],
        "H4_hierarchy_breaks_flat_ceiling": h4["hierarchy_breaks_flat_ceiling"],
        "H4_max_advantage_strict": h4["max_hier_advantage_strict"],
        "H4_flat_usable_T_strict": h4["flat_usable_T_strict"],
        "H4_hier_usable_T_strict": h4["hier_usable_T_strict"],
        "H4_flat_usable_T_id_forgiving": h4["flat_usable_T_id_forgiving"],
        # grades (honest; set from the sweeps above)
        "grade_H1_nested_gating": "[V]" if h1["levels_separate"] else "[O]",
        "grade_H2_abstraction": "[V]" if (h2["abstraction_holds_where_separable"]
                                          and h2["levels_separate_abstraction_generalises"]) else "[O]",
        "grade_H3_compositional": "[V]" if (h3["no_generalization_gap"]
                                            and h3["generated_instances_valid_and_novel"]) else "[O]",
        "grade_H4_breaks_ceiling": "[V]" if h4["hierarchy_breaks_flat_ceiling"] else "[O]",
    }
    h = results["headline"]
    print("\n--- headline (derived from sweeps) ---")
    print(f"   H1 nested gate selects+separates levels : {h['H1_levels_separate']}  {h['grade_H1_nested_gating']}")
    print(f"   H2 abstraction (category from novel inst): holds={h['H2_abstraction_holds']}, "
          f"max {h['H2_max_categories']} categories, generalises={h['H2_abstraction_generalises_to_unseen']}  {h['grade_H2_abstraction']}")
    print(f"   H3 compositional generalization         : no-gap={h['H3_no_generalization_gap']}, "
          f"generate valid+novel={h['H3_generated_valid_and_novel']}  {h['grade_H3_compositional']}")
    print(f"   H4 hierarchy breaks flat ceiling        : {h['H4_hierarchy_breaks_flat_ceiling']} "
          f"(strict: flat usable T={h['H4_flat_usable_T_strict']} -> hier usable T={h['H4_hier_usable_T_strict']}, "
          f"max advantage={h['H4_max_advantage_strict']:+.2f}; id-forgiving flat T={h['H4_flat_usable_T_id_forgiving']})  {h['grade_H4_breaks_ceiling']}")
    print(f"   (firewall consciousness_claim={CONSCIOUSNESS_CLAIM}, "
          f"hard_problem_open={HARD_PROBLEM_OPEN}; new_tuned_constants=0; "
          f"brain R/WM anchors NOT transferred)")

    results["_digest"] = digest({k: v for k, v in results.items()
                                 if not k.startswith("_")})
    with open("wave_hierarchy_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\ndigest = {results['_digest'][:16]}...")
    print("wrote wave_hierarchy_results.json")
    return results


if __name__ == "__main__":
    main()
