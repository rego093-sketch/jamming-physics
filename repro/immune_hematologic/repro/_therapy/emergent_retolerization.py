#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_retolerization.py  --  EMERGENT therapeutic re-tolerization as a MEASURED basin re-flip of a LATCHED
autoreactive clone back across the saddle-node into the tolerant basin (the therapeutic MIRROR of T23, not
asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D1, target T27.]

WHY THIS EXISTS (v0.11.0). T23 (emergent_autoimmunity.py) MEASURED the autoimmune tolerance BREAK: an escaped
self-clone (sub-spinodal residual self-drive h_self=base·spinodal, so BISTABLE) hit by an inflammatory insult
latches ON past the saddle-node (total drive = +spinodal) and STAYS ON after the insult clears -- a
self-sustaining pathological state, the dark mirror of immune memory. That is the DISEASE. This module asks the
therapeutic dual, the single most-motivated missing piece flagged in the roadmap: can a transient deep-suppression
/ barrier-restoration pulse push the latched clone back ACROSS the saddle-node into the tolerant basin, and -- the
whole clinical question -- is the result DURABLE (basin-acting: stays tolerant after the pulse is withdrawn) or
RELAPSING (drive-suppression only: re-fills the moment the pressure is released)? The VP discipline is emergence:
the answer, and the threshold, must come OUT of the SAME R19 substrate, MEASURED.

This module starts a self-clone in the LATCHED ON basin (the T23 broken state), carrying the persisting residual
self-drive h_self = base·spinodal, and applies a rectangular re-tolerization pulse of suppression depth
suppress·spinodal for a duration, under cellular noise,

    ds = (γ s − s³ + h(t)) dt + sqrt(2 D dt)·ξ,   h = (base − suppress)·spinodal during the pulse,

then WITHDRAWS the pulse and lets the field settle UNDER the persisting residual self-drive h = base·spinodal
(NOT to zero -- the self-antigen does not go away), and MEASURES the basin it lands in: tolerant (OFF, re-tolerized)
or still autoreactive (ON, refilled). Sweeping suppression depth × duration, and sweeping the residual self-drive
`base`, MEASURES the re-tolerization boundary. Nothing about it is assumed; it is the exact reflection of T23 with
the drive sign flipped.

WHAT EMERGES (measured, deterministic seed=19):
  1. RE-TOLERIZATION THRESHOLD IS THE NEGATIVE SADDLE-NODE: TOTAL DRIVE = −SPINODAL. The suppression depth at which
     P(re-tolerize) crosses 0.5 makes the total pulse drive (base − suppress) reach −1×spinodal, organ by organ
     (the mirror of T23's break at +1×spinodal). Across a residual-self-drive sweep the measured
     (suppress_crit − base) sum stays at 1×spinodal -- i.e. suppress_crit = 1 + base: the boundary is the switch's
     OTHER saddle-node, and self-antigen and therapeutic suppression are interchangeable ways of reaching it,
     MEASURED not posited.
  2. THE CURE IS DURABLE -- BASIN-ACTING, A THERAPEUTIC MEMORY. A supra-threshold pulse flips the latched clone OFF
     and after the pulse is WITHDRAWN to the persisting residual self-drive the clone STAYS OFF (measured P(OFF)
     after a long settle ≈ 1, unchanged when the settle is tripled) -- the clone has genuinely re-entered the
     tolerant basin and remains there without ongoing therapy, the healing mirror of T23's irreversible
     persistence. A sub-threshold pulse does NOT durably re-tolerize (refills to ON on withdrawal) -- honest
     negative control.
  3. DURABLE (BASIN-ACTING) vs RELAPSING (SUPPRESSION-ONLY) CONTRAST -- the central claim. Two interventions are
     MEASURED as basin-gated population trajectories of the autoreactive responding fraction A(t)/K:
       • BASIN-ACTING re-tolerization: a deep TRANSIENT pulse crosses the negative saddle-node, so after withdrawal
         the basin is emptied (measured ON fraction ≈ 0) and the autoreactive fraction DECAYS to ≈0 -- durable cure.
       • DRIVE-SUPPRESSION ONLY: a SUB-CRITICAL suppressor field held CONTINUOUSLY -- it holds the response DOWN
         while applied (measured ON fraction low: contained, the T24 peripheral-suppression regime), but it never
         crosses the saddle-node, so on WITHDRAWAL the residual self-drive REFILLS the ON basin (measured ON
         fraction ≈ 1) and the autoreactive fraction REGROWS -- relapse on withdrawal.
     The substrate verdict (the exact reflection of T17/T19's cytotoxic-contrast, here for autoimmune disease):
     basin-acting re-tolerization is the DURABLE class; drive-suppression-only is preventive-not-curative and
     relapses when the pressure is released.
  4. CURABILITY vs NEGATIVE-SELECTION DEPTH (the T21 → T27 link, mirror of T23's susceptibility link). Sweeping the
     residual self-drive from deep-tolerant toward the deletion threshold, the critical suppression depth RISES
     monotonically (suppress_crit = 1 + base): a near-threshold escapee needs a DEEPER re-tolerization pulse.
     Because central tolerance (T21) deletes exactly the near-threshold clones, DEEPER negative selection leaves
     only smaller-residual survivors and so makes re-tolerization EASIER -- deeper central tolerance simultaneously
     LOWERS break susceptibility (T23) and EASES re-tolerization (T27), one structural fact with two faces.

TREATMENT DIRECTION (roadmap discipline -- CLASS only, never agent/dose). The dynamics point to basin-acting,
antigen-specific tolerance RESTORATION as the durable class; chronic blanket suppression only holds the clone
sub-threshold and relapses on withdrawal. Susceptibility-of-cure is set by deletion depth (deeper T21 → easier).
This is a re-description of known re-tolerization immunology in the R19/Kramers formalism and a principled
treatment DIRECTION; it is NOT a drug, dose, schedule, clinical recommendation, or VP validation, and NOT medical
advice.

GRADES (C3): the re-tolerization boundary shape -- total-drive = −spinodal invariant (suppress_crit = 1+base),
the durable basin-acting persistence, the durable-vs-relapsing (suppression-only) trajectory contrast, and the
negative-selection-depth curability link -- are [V] emergent (measured from the coupled stochastic latch). The
ABSOLUTE pulse depth / clinical suppression magnitude / boundary timing -- set by the residual-drive depth, the
pulse amplitude / duration, and the free cellular-noise scale D -- is [O], no fabricated numbers, and every
clinical scale stays [O] with a stated obstacle. Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"        # the adaptive compartment where the latched autoreactive clone resides

# --- deterministic simulation size (fixed; the exact mirror of T23; no per-condition tuning) ----------
_N      = 260       # cells per (depth, duration, base) condition
_DT     = 0.01      # integration timestep
_RELAX  = 1000      # settle steps after the pulse is withdrawn (decide final basin)
_D      = 0.02      # cellular-noise scale (low: sharp boundary; absolute value is [O])
_DUR_LONG = 800     # "long" pulse duration for the depth threshold

_SUPPRESS_DEPTHS = (0.20, 0.60, 1.00, 1.15, 1.30, 1.45, 1.60, 2.00)  # suppression depth grid (× spinodal, coarsened)
_DUR_GRID        = (50, 150, 300, 550, 900)        # duration grid for the dose×time tradeoff
_BASE_REF        = 0.30          # reference residual self-drive of the latched escapee (× spinodal; sub-spinodal)
_BASE_SWEEP      = (0.00, 0.20, 0.40, 0.60, 0.80)                      # residual self-drive sweep (deletion depth)

# --- basin-gated population (relapse vs cure) layer (mirrors T17) -------------------------------------
_K_POP   = 2000     # carrying capacity of the autoreactive responding pool (absolute scale is [O])
_M_POP   = 400      # independent foci per condition
_PDT     = 0.05     # population timestep
_R_GROW  = 1.0      # autoreactive proliferation rate (arbitrary; [O])
_CONV    = 1.0      # re-tolerized clearance rate (arbitrary; [O])
_T_POP   = 300      # population steps (long enough to relapse or clear)


def p_retolerize(g, suppress_frac, dur, base=_BASE_REF, D=_D, N=_N, dt=_DT, relax=_RELAX, seed=SEED, relax_mult=1):
    """MEASURED probability the latched clone is RE-TOLERIZED: from the autoreactive ON basin, hold
    h=(base−suppress)·spinodal for `dur` steps (the re-tolerization pulse), then WITHDRAW the pulse and settle under
    the persisting residual self-drive h=base·spinodal; report the fraction that lands in the OFF (tolerant) basin.
    The residual self-drive does NOT go to zero (the self-antigen persists)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, math.sqrt(g))                  # start in the autoreactive (ON / broken) basin (T23 endpoint)
    sq = math.sqrt(2.0 * D * dt)
    h_pulse = (base - suppress_frac) * sp
    h_rest  = base * sp                           # the pulse is withdrawn TO the residual self-drive, not to 0
    for _ in range(int(dur)):
        s += (g * s - s ** 3 + h_pulse) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    for _ in range(int(relax * relax_mult)):      # withdraw pulse, let it decide a basin under residual self-drive
        s += (g * s - s ** 3 + h_rest) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float((s < 0.0).mean())                # OFF (tolerant) fraction = re-tolerized


def _mean_effector_held(g, suppress_frac, base=_BASE_REF, D=_D, N=_N, dt=_DT, hold=_DUR_LONG, seed=SEED):
    """MEASURED mean autoreactive EFFECTOR LEVEL ⟨s⟩ WHILE a suppressor field of depth suppress is HELD (not
    withdrawn): from the ON basin, hold h=(base−suppress)·spinodal and report mean s. A sub-critical suppressor
    DAMPENS the effector output (⟨s⟩ falls) without crossing the saddle-node (⟨s⟩ stays > 0, basin not emptied) --
    the physically correct 'improves on drug but not cured' statement (in a clean bistable switch you cannot
    strongly suppress the ON state without crossing into the tolerant basin)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, math.sqrt(g))
    sq = math.sqrt(2.0 * D * dt)
    h_hold = (base - suppress_frac) * sp
    for _ in range(int(hold)):
        s += (g * s - s ** 3 + h_hold) * dt + sq * rng.standard_normal(N)
        np.clip(s, -5.0, 5.0, out=s)
    return float(s.mean())


def _suppress_threshold(g, base, dur=_DUR_LONG, depths=_SUPPRESS_DEPTHS, D=_D, seed=SEED):
    """Interpolate the suppression depth (× spinodal) at which P(re-tolerize) crosses 0.5 (rising in depth)."""
    ps = [p_retolerize(g, d, dur, base=base, D=D, seed=seed) for d in depths]
    if ps[0] >= 0.5:
        return depths[0]
    for i in range(1, len(ps)):
        if ps[i - 1] < 0.5 <= ps[i]:
            f = (0.5 - ps[i - 1]) / (ps[i] - ps[i - 1])
            return depths[i - 1] + f * (depths[i] - depths[i - 1])
    return depths[-1] if ps[-1] >= 0.5 else float("inf")


def _dur_threshold(g, total_depth, base, durs=_DUR_GRID, D=_D, seed=SEED):
    """Smallest pulse duration (steps) for which P(re-tolerize) >= 0.5, at a fixed TOTAL suppression depth =
    total_depth·spinodal (pulse depth = total_depth, i.e. total drive = base − total_depth)."""
    for d in durs:
        if p_retolerize(g, total_depth, d, base=base, D=D, seed=seed) >= 0.5:
            return d
    return None


def _basin_fraction_retol(g, mode, base=_BASE_REF, D=_D, N=_N, dt=_DT, seed=SEED):
    """MEASURE residual autoreactive-ON basin fraction after an intervention, for the population contrast.
    mode 'retolerize': supra-threshold TRANSIENT pulse then withdraw (≈0, basin emptied).
    mode 'suppress_withdrawn': SUB-CRITICAL suppressor held then withdrawn (≈1, refills)."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    s = np.full(N, math.sqrt(g))                  # all cells start in the autoreactive ON basin
    sq = math.sqrt(2.0 * D * dt)
    if mode == "retolerize":
        depth = (1.0 + base) + 0.30               # supra-threshold (crosses the negative saddle-node)
        h = (base - depth) * sp
        for _ in range(int(_DUR_LONG)):
            s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
        for _ in range(int(_RELAX)):              # withdraw, settle under residual self-drive
            s += (g * s - s ** 3 + base * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    else:                                         # suppress_withdrawn: sub-critical hold then release
        depth = (1.0 + base) - 0.30               # SUB-critical (does NOT cross the saddle-node)
        h = (base - depth) * sp
        for _ in range(int(_DUR_LONG)):           # hold the suppressor (contained while applied)
            s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
        for _ in range(int(_RELAX)):              # WITHDRAW -> residual self-drive refills the ON basin
            s += (g * s - s ** 3 + base * sp) * dt + sq * rng.standard_normal(N); np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _population(f, K=_K_POP, M=_M_POP, dt=_PDT, T=_T_POP, r=_R_GROW, conv=_CONV, seed=SEED):
    """MEASURE the autoreactive responding population A(t)/K under a logistic layer GATED by the basin fraction f
    (f≈1: the autoreactive basin is the niche -> grows; f≈0: re-tolerized cells leave the pool -> decays)."""
    rng = np.random.default_rng(seed)
    N = np.full(M, int(K), dtype=float)           # start at full autoreactive load (the active disease)
    traj = np.empty(T)
    for t in range(T):
        p_grow = np.clip(r * (1.0 - N / K) * f * dt, 0.0, 1.0)
        p_decay = min(max(conv * (1.0 - f) * dt, 0.0), 1.0)
        births = rng.binomial(N.astype(int), p_grow)
        deaths = rng.binomial(N.astype(int), p_decay) if p_decay > 0 else np.zeros(M, dtype=int)
        N = N + births - deaths
        np.clip(N, 0, K, out=N)
        traj[t] = float(N.mean()) / K
    return traj


def _coarse_monotone(traj, rising=True, nb=10, tol=0.03):
    blk = max(1, len(traj) // nb)
    means = [float(traj[i:i + blk].mean()) for i in range(0, len(traj) - blk + 1, blk)]
    if rising:
        return all(means[i + 1] >= means[i] - tol for i in range(len(means) - 1))
    return all(means[i + 1] <= means[i] + tol for i in range(len(means) - 1))


def emergent_retolerization(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1a) no-residual critical suppression == spinodal, organ by organ (mirror of T23 break == spinodal)
    depth_rows = {}
    crit_ok = True
    for o in _ORGANS:
        g = gammas[o]
        d_crit = _suppress_threshold(g, base=0.0, dur=_DUR_LONG, D=D)
        depth_rows[o] = dict(suppress_crit_over_spinodal=round(d_crit, 3),
                             matches_spinodal=bool(abs(d_crit - 1.0) < 0.12))
        crit_ok = crit_ok and depth_rows[o]["matches_spinodal"]

    # (1b) NEGATIVE-SADDLE-NODE INVARIANT: across a residual sweep, suppress_crit − base == 1×spinodal
    invariant_rows = []
    inv_ok = True
    for base in _BASE_SWEEP:
        d_crit = _suppress_threshold(g_ref, base=base, dur=_DUR_LONG, D=D)
        net = d_crit - base                       # total pulse drive at threshold = −net×spinodal
        ok = bool(abs(net - 1.0) < 0.14)
        invariant_rows.append(dict(residual_self_drive=round(base, 3),
                                   critical_suppress=round(d_crit, 3),
                                   net_depth_over_spinodal=round(net, 3),
                                   equals_spinodal=ok))
        inv_ok = inv_ok and ok

    # (2) DURABLE PERSISTENCE (therapeutic memory) for the latched escapee (base=_BASE_REF)
    #     supra-threshold pulse -> OFF and STAYS OFF after withdrawal; sub-threshold -> refills; tripled settle = same
    crit_ref = _suppress_threshold(g_ref, base=_BASE_REF, dur=_DUR_LONG, D=D)
    supra = crit_ref + 0.30
    sub   = max(crit_ref - 0.30, 0.05)
    p_supra      = p_retolerize(g_ref, supra, _DUR_LONG, base=_BASE_REF, D=D)
    p_supra_long = p_retolerize(g_ref, supra, _DUR_LONG, base=_BASE_REF, D=D, relax_mult=3)  # triple the settle
    p_sub        = p_retolerize(g_ref, sub,   _DUR_LONG, base=_BASE_REF, D=D)
    durable       = bool(p_supra > 0.5 and abs(p_supra_long - p_supra) < 0.05)
    sub_relapses  = bool(p_sub < 0.5)

    # (3) DURABLE (basin-acting) vs RELAPSING (suppression-only) CONTRAST -- population trajectories + held control
    f_retol = _basin_fraction_retol(g_ref, "retolerize",        base=_BASE_REF, D=D)   # ≈ 0 (basin emptied)
    f_supp  = _basin_fraction_retol(g_ref, "suppress_withdrawn", base=_BASE_REF, D=D)  # ≈ 1 (refilled)
    sp_ref0 = spinodal(g_ref)
    s_on_unsuppressed = _mean_effector_held(g_ref, 0.0, base=_BASE_REF, D=D)                       # full disease activity
    s_on_suppressed   = _mean_effector_held(g_ref, (1.0 + _BASE_REF) - 0.30, base=_BASE_REF, D=D)  # dampened on therapy
    s_retolerized     = _mean_effector_held(g_ref, (1.0 + _BASE_REF) + 0.30, base=_BASE_REF, D=D)  # tolerant (cured)
    retol_traj = _population(f_retol, seed=SEED)
    supp_traj  = _population(f_supp,  seed=SEED + 1)
    retol_final = float(retol_traj[-int(len(retol_traj) * 0.1):].mean())
    supp_final  = float(supp_traj[-int(len(supp_traj) * 0.1):].mean())
    retol_cures      = bool(retol_final <= 0.10 and _coarse_monotone(retol_traj, rising=False))
    supp_relapses    = bool(supp_final >= 0.90 and _coarse_monotone(supp_traj, rising=True))
    # honest 'improves on drug but not cured': suppressor dampens effector output while held (⟨s⟩ falls) yet stays
    # in the ON basin (⟨s⟩ > 0), whereas the basin-acting pulse crosses into the tolerant basin (⟨s⟩ < 0)
    suppression_dampens_while_held = bool(s_on_suppressed < s_on_unsuppressed and s_on_suppressed > 0.0)
    retolerization_crosses_basin   = bool(s_retolerized < 0.0)
    durable_vs_relapsing = bool(retol_cures and supp_relapses
                               and suppression_dampens_while_held and retolerization_crosses_basin)
    retol_traj_s = [round(float(retol_traj[i]), 3) for i in range(0, len(retol_traj), max(1, len(retol_traj) // 10))]
    supp_traj_s  = [round(float(supp_traj[i]),  3) for i in range(0, len(supp_traj),  max(1, len(supp_traj)  // 10))]

    # (4) CURABILITY vs NEGATIVE-SELECTION DEPTH (T21 -> T27): critical suppression RISES as residual self-drive rises
    curability = [dict(residual_self_drive=r["residual_self_drive"], critical_suppress=r["critical_suppress"])
                  for r in invariant_rows]
    crit_seq = [r["critical_suppress"] for r in curability]
    curability_monotone = bool(all(crit_seq[i] <= crit_seq[i + 1] for i in range(len(crit_seq) - 1))
                               and crit_seq[-1] > crit_seq[0])

    ok = bool(crit_ok and inv_ok and durable and sub_relapses
              and durable_vs_relapsing and curability_monotone)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6),
        noise_D=D, residual_self_drive_ref=_BASE_REF,
        no_residual_critical_suppress=depth_rows,
        no_residual_critical_equals_spinodal=bool(crit_ok),
        negative_saddle_node_invariant=invariant_rows,
        negative_saddle_node_invariant_holds=bool(inv_ok),
        durability=dict(critical_suppress=round(crit_ref, 3),
                        p_retol_supra=round(p_supra, 3), p_retol_supra_tripled_settle=round(p_supra_long, 3),
                        p_retol_sub=round(p_sub, 3),
                        durable_basin_acting=bool(durable), sub_threshold_relapses=bool(sub_relapses)),
        durable_vs_relapsing=dict(
            measured_basin_fraction=dict(retolerization_residual_ON=round(f_retol, 3),
                                         suppression_withdrawn_ON=round(f_supp, 3)),
            measured_effector_level=dict(autoreactive_ON_unsuppressed=round(s_on_unsuppressed, 3),
                                         suppression_while_held=round(s_on_suppressed, 3),
                                         retolerized=round(s_retolerized, 3)),
            retolerization_fraction_of_K=retol_traj_s, suppression_only_fraction_of_K=supp_traj_s,
            retolerization_final_fraction=round(retol_final, 3), suppression_final_fraction=round(supp_final, 3),
            retolerization_cures=bool(retol_cures), suppression_only_relapses=bool(supp_relapses),
            suppression_dampens_while_held=bool(suppression_dampens_while_held),
            retolerization_crosses_basin=bool(retolerization_crosses_basin),
            contrast=bool(durable_vs_relapsing)),
        curability_vs_deletion_depth=curability, curability_monotone=bool(curability_monotone),
        all_pass=ok,
        grade="[V] therapeutic re-tolerization EMERGES as the R19 mirror of the T23 tolerance break: a transient "
              "suppression pulse re-flips a latched autoreactive clone back across the switch's OTHER saddle-node "
              "(measured critical suppression makes the total pulse drive = −spinodal, suppress_crit = 1 + residual "
              "across a residual sweep, organ by organ -- self-antigen and therapeutic suppression interchangeable), "
              "the cure is DURABLE (the clone re-enters the tolerant basin and stays OFF after the pulse is "
              "withdrawn, the healing mirror of T23 persistence), basin-acting re-tolerization CURES while a "
              "sub-critical suppressor-only field merely CONTAINS while applied and RELAPSES on withdrawal (measured "
              "trajectory contrast, the T17 cytotoxic-contrast reflected into autoimmune disease), and re-tolerization "
              "is EASIER for a deeper-tolerant clone so deeper central tolerance (T21) both lowers break "
              "susceptibility and eases cure -- measured, not assumed; [O] absolute pulse depth / clinical "
              "suppression magnitude / boundary timing (residual depth, pulse amplitude / duration, cellular-noise "
              "scale D); treatment = CLASS/DIRECTION (basin-acting re-tolerization is the durable class), never "
              "agent / dose / recommendation")


def run(gammas):
    """T27: emergent therapeutic re-tolerization -- a latched autoreactive clone re-flipped back across the
    saddle-node into the tolerant basin MEASURED, with a negative-saddle-node threshold (suppress_crit = 1 +
    residual), durable basin-acting persistence, a durable-vs-relapsing (suppression-only) trajectory contrast,
    and a negative-selection-depth curability link -- the therapeutic dual of the T23 autoimmune break."""
    r = emergent_retolerization(gammas)
    return dict(T27=dict(target="T27",
                         claim="therapeutic re-tolerization EMERGES as the R19 mirror of the T23 autoimmune break: "
                               "a transient deep-suppression pulse re-flips a latched autoreactive clone back across "
                               "the switch's other saddle-node (measured total pulse drive = −spinodal, suppress_crit "
                               "= 1 + residual self-drive across a residual sweep), the cure is DURABLE -- the clone "
                               "re-enters the tolerant basin and stays OFF after the pulse is withdrawn (the healing "
                               "mirror of the T23 pathological memory) -- and basin-acting re-tolerization CURES "
                               "while a sub-critical suppression-only field only CONTAINS while applied and RELAPSES "
                               "on withdrawal, with re-tolerization made easier by deeper central tolerance (T21); "
                               "treatment is direction/class only and absolute pulse depth stays [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T27"]["result"]
    print("THERAPEUTIC RE-TOLERIZATION of a latched autoreactive clone (primary=%s, γ=%.4f, spinodal=%.4f, D=%.3f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["noise_D"]))
    print("\n(1a) no-residual critical suppression == spinodal, organ by organ:")
    for o, row in r["no_residual_critical_suppress"].items():
        print("     %-28s suppress_crit=%.3f×sp  matches=%s" % (o, row["suppress_crit_over_spinodal"], row["matches_spinodal"]))
    print("     -> all organs: %s" % r["no_residual_critical_equals_spinodal"])
    print("\n(1b) NEGATIVE-SADDLE-NODE INVARIANT (suppress_crit − residual == 1×spinodal):")
    for row in r["negative_saddle_node_invariant"]:
        print("     residual=%.2f  critical_suppress=%.3f  net=%.3f×sp  ==spinodal:%s"
              % (row["residual_self_drive"], row["critical_suppress"], row["net_depth_over_spinodal"], row["equals_spinodal"]))
    print("     -> invariant holds: %s" % r["negative_saddle_node_invariant_holds"])
    d = r["durability"]
    print("\n(2) DURABLE PERSISTENCE (therapeutic memory), latched escapee residual=%.2f, critical suppress=%.3f:"
          % (r["residual_self_drive_ref"], d["critical_suppress"]))
    print("     supra-threshold pulse: P(re-tol)=%.3f ; tripled settle: %.3f -> durable=%s"
          % (d["p_retol_supra"], d["p_retol_supra_tripled_settle"], d["durable_basin_acting"]))
    print("     sub-threshold pulse: P(re-tol)=%.3f -> relapses=%s" % (d["p_retol_sub"], d["sub_threshold_relapses"]))
    c = r["durable_vs_relapsing"]; mb = c["measured_basin_fraction"]; me = c["measured_effector_level"]
    print("\n(3) DURABLE (basin-acting) vs RELAPSING (suppression-only) CONTRAST:")
    print("     basin fraction (after withdrawal): re-tol residual ON=%.3f | suppression-only ON=%.3f"
          % (mb["retolerization_residual_ON"], mb["suppression_withdrawn_ON"]))
    print("     effector ⟨s⟩: autoreactive ON (unsuppressed)=%.3f | suppression WHILE held=%.3f | re-tolerized=%.3f"
          % (me["autoreactive_ON_unsuppressed"], me["suppression_while_held"], me["retolerized"]))
    print("     re-tolerization A(t)/K:", c["retolerization_fraction_of_K"])
    print("     suppression-only A(t)/K:", c["suppression_only_fraction_of_K"])
    print("     re-tol final=%.3f (cures=%s) | suppression final=%.3f (relapses=%s) | dampens while held=%s | crosses basin=%s -> contrast=%s"
          % (c["retolerization_final_fraction"], c["retolerization_cures"], c["suppression_final_fraction"],
             c["suppression_only_relapses"], c["suppression_dampens_while_held"],
             c["retolerization_crosses_basin"], c["contrast"]))
    print("\n(4) CURABILITY vs NEGATIVE-SELECTION DEPTH (critical suppression rises as residual self-drive rises):")
    for row in r["curability_vs_deletion_depth"]:
        print("     residual_self_drive=%.2f  critical_suppress=%.3f×sp" % (row["residual_self_drive"], row["critical_suppress"]))
    print("     -> deeper deletion (smaller residual) => smaller critical suppression => easier cure: %s" % r["curability_monotone"])
    print("\nT27 all_pass:", r["all_pass"])
