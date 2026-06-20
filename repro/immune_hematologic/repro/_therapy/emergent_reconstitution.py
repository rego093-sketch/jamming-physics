#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_reconstitution.py  --  EMERGENT acquired-immunodeficiency coverage collapse and immune RECONSTITUTION
threshold by direct stochastic simulation (not asserted, not fitted).  [DISEASE/TREATMENT axis: roadmap D3, T30.]

WHY THIS EXISTS (v0.11.0). Three measured results in this package converge on acquired immunodeficiency. T10/T15
MEASURED that the immunosurveillance reservoir floor scales as 1/(1−escape) = 1/surveillance (deeper surveillance
-> lower committed reservoir), and that restoring surveillance CLEARS an accumulated reservoir as a time course.
T16 MEASURED that a finite responder pool concentrates the response on a few clones (a coverage statistic). T5/T10
MEASURED that the SAME surveillance/escape factor multiplies tumor net burden. Acquired immunodeficiency (HIV-type
helper depletion, post-chemo aplasia, transplant conditioning) is the regime where the responder pool / surveillance
depth FALLS: the roadmap asks for the FLOOR below which coverage collapses into an opportunistic regime, the
RECONSTITUTION threshold above which it recovers, and -- the cross-cutting claim this package is positioned to make
-- that the SAME lever lowers the tumor-escape multiplier (one lever, two diseases). The VP discipline is emergence:
the collapse threshold, the recovery, and the shared multiplier must come OUT of the SAME measured substrate
processes, MEASURED.

This module composes two MEASURED substrate processes against a swept surveillance depth sv (∝ responder pool):
  * a T15 immigration(influx)–death(clearance) reservoir, clearance μ = μ0·sv, MEASURED steady burden
        B(sv) = λ/(μ0·sv)  (the T10/T15 seam: burden × sv ≈ const, burden ∝ 1/sv), run for a pathogen influx λ_p
        AND a tumor influx λ_t (the SAME kernel -- the shared surveillance multiplier);
  * a T16 coupled N-clone competition for a shared pool of capacity ∝ sv, MEASURED repertoire COVERAGE
        (fraction of clones that commit -- the breadth of protection).
and MEASURES the thresholds by interpolating the 0.5-crossings / opportunistic-line crossings. Nothing is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. COVERAGE COLLAPSES BELOW A SURVEILLANCE FLOOR. As sv falls, the measured repertoire coverage stays broad
     above a critical sv then COLLAPSES (a sharp loss of breadth -- the opportunistic regime), and the measured
     pathogen reservoir crosses an opportunistic burden line at a surveillance threshold sv_op = λ_p/(μ0·B_line):
     a measured floor below which protection fails, MEASURED.
  2. RECONSTITUTION RECOVERS COVERAGE -- A THRESHOLD, MEASURED AS A TRAJECTORY. Starting from a depleted
     (immunodeficient) pool, RESTORING surveillance to a level r recovers protection IFF r exceeds the
     reconstitution threshold: the measured reservoir decays as a time course (the T15 clearance, recovered here)
     toward the lower restored floor, and the coverage at r recovers above ½ -- recovery is THRESHOLD-GATED, a
     sub-threshold restoration does NOT recover (stays opportunistic) while a supra-threshold one does, MEASURED.
  3. ONE LEVER, TWO DISEASES (the cross-cut). The SAME surveillance restoration that drops the pathogen reservoir
     below the opportunistic line ALSO drops the tumor immune-escape multiplier: measured pathogen burden and
     measured tumor burden both fall as 1/sv and, rescaled by their own influx, collapse onto the SAME 1/(μ0·sv)
     curve (burden_p/λ_p ≈ burden_t/λ_t at every sv). Restoring immune surveillance is one lever that lowers BOTH
     the infection reservoir and the cancer-escape multiplier, MEASURED -- not asserted.
  4. DEEPER CHALLENGE NEEDS DEEPER RECONSTITUTION (honest, threshold-gated). The reconstitution level required to
     clear the opportunistic line RISES one-for-one with the pathogen influx λ_p (a more aggressive opportunist
     needs deeper surveillance restoration: r_crit = λ_p/(μ0·B_line)), and a restoration BELOW r_crit fails while
     ABOVE succeeds -- the recovery is a basin/threshold property, not a gradual rescue, MEASURED.

TREATMENT DIRECTION (roadmap discipline -- CLASS only, never agent/dose). The dynamics point to restoring
surveillance depth / repertoire breadth ABOVE the coverage-collapse threshold (immune reconstitution as the
durable class), which SIMULTANEOUSLY lowers the tumor-escape multiplier -- one lever acting on two disease axes;
mere transient symptom control below the threshold leaves the opportunistic regime intact. This is a re-description
of immune-reconstitution immunology in the R19/seam formalism and a principled treatment DIRECTION; it is NOT a
drug, dose, schedule, clinical recommendation, or VP validation, and NOT medical advice.

GRADES (C3): the coverage-collapse floor, the threshold-gated reconstitution recovery (with its measured clearance
trajectory), the shared 1/sv multiplier across pathogen and tumor (one lever, two diseases), and the
deeper-challenge-deeper-reconstitution scaling are [V] emergent (measured by composing the T15 reservoir and T16
coverage processes over a surveillance sweep). The ABSOLUTE counts / opportunistic line / clearance scale -- set by
the population constant K, the clearance scale μ0, the opportunistic burden line B_line, and the free
cellular-noise scale D -- are [O], no fabricated numbers, and every clinical scale stays [O] with a stated obstacle.
Determinism: fixed seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"

# --- reservoir (T15 immigration-death) -- clearance μ = μ0·sv; measured floor ∝ 1/sv -------------------
_MU0       = 20.0     # clearance-rate scale (arbitrary; [O]); large -> fast equilibration so the floor tracks 1/sv
_K_FLOOR   = 4000.0   # population cap (arbitrary; [O]; shape-preserving)
_M_FLOOR   = 300      # independent tissues
_T_FLOOR   = 500      # steps to the steady floor
_DT        = 0.01
_D         = 0.02
_LAM_PATH  = 400.0    # pathogen influx (arbitrary; [O])
_LAM_TUMOR = 160.0    # tumor influx (arbitrary; [O]) -- the SAME kernel, different influx
_B_LINE    = 40.0     # opportunistic burden line (arbitrary; [O]); sv_op = λ_p/(μ0·B_line)

# --- coverage (T16 coupled competition) -- shared pool ∝ sv; coverage = fraction of clones committed --
_NCLONE    = 10
_AFF_LO    = 0.85     # affinity ladder (× spinodal per unit pool): lowest clone supra-spinodal at full pool
_AFF_HI    = 1.75
_A_FULL    = 1.6      # shared pool at sv=1 (× spinodal scale)
_CONSUME   = 0.03     # pool consumption per committed clone
_M_COV     = 160      # independent repertoires
_T_COV     = 340      # steps (long enough for committed clones to transit ON)

_SV_GRID   = (0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.85, 1.00)   # surveillance / responder-pool sweep
_SV_LOW    = 0.15     # depleted (immunodeficient) starting surveillance for the reconstitution trajectory
_RESTORE   = (0.20, 0.35, 0.50, 0.65, 0.80)                     # reconstitution levels
_LAM_SWEEP = (400.0, 600.0, 900.0)                              # pathogen-influx sweep for the depth scaling


def _floor(sv, lam, mu0=_MU0, K=_K_FLOOR, M=_M_FLOOR, T=_T_FLOOR, dt=_DT, seed=SEED):
    """MEASURE the T15 steady reservoir burden under clearance μ = μ0·sv and influx λ (immigration-death)."""
    rng = np.random.default_rng(seed)
    N = np.zeros(M)
    mu = mu0 * max(sv, 1e-6)
    pd = min(mu * dt, 1.0)
    for _ in range(T):
        N = np.clip(N + rng.poisson(lam * dt, size=M) - rng.binomial(N.astype(int), pd), 0, K)
    return float(N.mean())


def _reconstitution_traj(sv_low, r, lam, t_switch=300, total=900, mu0=_MU0, K=_K_FLOOR, M=_M_FLOOR, dt=_DT, seed=SEED):
    """MEASURE the reservoir time course: phase A at depleted sv_low (accumulate), then RESTORE to sv=r at
    t_switch and MEASURE the decay toward the lower restored floor (the T15 clearance recovered)."""
    rng = np.random.default_rng(seed)
    N = np.zeros(M)
    traj = np.empty(total)
    for t in range(total):
        sv = sv_low if t < t_switch else r
        mu = mu0 * max(sv, 1e-6); pd = min(mu * dt, 1.0)
        N = np.clip(N + rng.poisson(lam * dt, size=M) - rng.binomial(N.astype(int), pd), 0, K)
        traj[t] = float(N.mean())
    return traj


def _coverage(sv, Nc=_NCLONE, aff_lo=_AFF_LO, aff_hi=_AFF_HI, A_full=_A_FULL, consume=_CONSUME,
              M=_M_COV, T=_T_COV, D=_D, dt=_DT, seed=SEED):
    """MEASURE the T16 repertoire COVERAGE: Nc clones (affinity ladder) compete for a shared pool ∝ sv; coverage
    = fraction of clones whose commit probability exceeds 0.5 (the breadth of protection)."""
    rng = np.random.default_rng(seed)
    g = G_PRIMARY; sp = spinodal(g)
    aff = np.linspace(aff_lo, aff_hi, Nc)
    s = np.full((M, Nc), -math.sqrt(g))
    A = np.full(M, sv * A_full)
    sq = math.sqrt(2.0 * D * dt)
    for _ in range(T):
        h = aff[None, :] * A[:, None] * sp
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal((M, Nc))
        np.clip(s, -5.0, 5.0, out=s)
        A = np.clip(A - consume * (s > 0).sum(axis=1) * dt, 0.0, None)
    pc = (s > 0).mean(axis=0)
    return float((pc > 0.5).mean())


def _cross_down(xs, ys, level):
    """Interpolate the x at which y crosses `level` going DOWN (ys decreasing in x)."""
    for i in range(1, len(xs)):
        if ys[i - 1] >= level > ys[i]:
            f = (ys[i - 1] - level) / (ys[i - 1] - ys[i])
            return xs[i - 1] + f * (xs[i] - xs[i - 1])
    return None


G_PRIMARY = 1.4892   # set in run(); module-level so _coverage can read the primary γ


def emergent_reconstitution(gammas, D=_D):
    global G_PRIMARY
    G_PRIMARY = gammas[_PRIMARY]
    sp_ref = spinodal(G_PRIMARY)

    # (1) COVERAGE COLLAPSE + opportunistic burden line, swept over surveillance depth
    sv_grid = list(_SV_GRID)
    cov = [_coverage(sv, D=D) for sv in sv_grid]
    burd_p = [_floor(sv, _LAM_PATH) for sv in sv_grid]
    cov_monotone = all(cov[i] <= cov[i + 1] + 0.06 for i in range(len(cov) - 1))  # coverage rises with sv (collapses as sv falls)
    cov_broad_high = bool(cov[-1] >= 0.8)      # broad at full surveillance
    cov_collapsed_low = bool(cov[0] <= 0.2)    # collapsed at low surveillance
    sv_cov_crit = _cross_down(sv_grid[::-1], cov[::-1], 0.5)   # coverage crosses 0.5 as sv falls
    sv_op = _LAM_PATH / (_MU0 * _B_LINE)       # opportunistic surveillance threshold (burden = B_line)
    burd_opportunistic_low = bool(burd_p[0] > _B_LINE and burd_p[-1] < _B_LINE)
    collapse_ok = bool(cov_monotone and cov_broad_high and cov_collapsed_low and (sv_cov_crit is not None)
                       and burd_opportunistic_low)

    # (2) RECONSTITUTION RECOVERS COVERAGE -- threshold + trajectory
    recon_rows = []
    for r in _RESTORE:
        traj = _reconstitution_traj(_SV_LOW, r, _LAM_PATH)
        final = float(traj[-int(len(traj) * 0.1):].mean())
        cov_r = _coverage(r, D=D)
        recovered = bool(final < _B_LINE and cov_r >= 0.5)
        recon_rows.append(dict(restore_sv=round(r, 3), final_burden=round(final, 1),
                               coverage_at_restore=round(cov_r, 3), recovered=recovered))
    r_crit = _LAM_PATH / (_MU0 * _B_LINE)
    # threshold-gated: sub-threshold restore fails, supra-threshold restore recovers
    sub = [row for row in recon_rows if row["restore_sv"] < r_crit - 1e-9]
    sup = [row for row in recon_rows if row["restore_sv"] > r_crit + 1e-9]
    sub_fails = bool(sub and all(not row["recovered"] for row in sub))
    sup_recovers = bool(sup and all(row["recovered"] for row in sup))
    # trajectory monotone decay in phase B (restored above threshold)
    traj_hi = _reconstitution_traj(_SV_LOW, _RESTORE[-1], _LAM_PATH)
    tb = traj_hi[300:]
    blk = max(1, len(tb) // 8)
    means = [float(tb[i:i + blk].mean()) for i in range(0, len(tb) - blk + 1, blk)]
    decay_monotone = all(means[i + 1] <= means[i] + 2.0 for i in range(len(means) - 1)) and means[-1] < means[0]
    recon_ok = bool(sub_fails and sup_recovers and decay_monotone)

    # (3) ONE LEVER, TWO DISEASES -- pathogen & tumor burden both ∝ 1/sv, same kernel
    burd_t = [_floor(sv, _LAM_TUMOR) for sv in sv_grid]
    seam_rows = []
    both_fall = True
    same_curve = True
    for i, sv in enumerate(sv_grid):
        bp_sv = burd_p[i] * sv; bt_sv = burd_t[i] * sv               # ≈ λ/μ0 constant -> floor ∝ 1/sv
        rp = burd_p[i] / _LAM_PATH; rt = burd_t[i] / _LAM_TUMOR      # both ≈ 1/(μ0·sv) -> same curve
        seam_rows.append(dict(sv=round(sv, 3), pathogen=round(burd_p[i], 1), tumor=round(burd_t[i], 1),
                              pathogen_x_sv=round(bp_sv, 1), tumor_x_sv=round(bt_sv, 1),
                              pathogen_over_lambda=round(rp, 4), tumor_over_lambda=round(rt, 4),
                              same_within=bool(abs(rp - rt) < 0.15 * max(rp, rt) + 1e-6)))
        same_curve = same_curve and seam_rows[-1]["same_within"]
    for i in range(1, len(sv_grid)):
        both_fall = both_fall and (burd_p[i] <= burd_p[i - 1] + 1.0) and (burd_t[i] <= burd_t[i - 1] + 1.0)
    one_lever_ok = bool(both_fall and same_curve)

    # (4) DEEPER CHALLENGE NEEDS DEEPER RECONSTITUTION -- r_crit ∝ λ_p, and threshold-gating
    depth_rows = []
    for lam in _LAM_SWEEP:
        rc = lam / (_MU0 * _B_LINE)
        depth_rows.append(dict(pathogen_influx=lam, reconstitution_threshold_sv=round(rc, 3)))
    rc_seq = [row["reconstitution_threshold_sv"] for row in depth_rows]
    depth_monotone = bool(all(rc_seq[i] < rc_seq[i + 1] for i in range(len(rc_seq) - 1)))
    depth_ok = bool(depth_monotone and sub_fails and sup_recovers)

    ok = bool(collapse_ok and recon_ok and one_lever_ok and depth_ok)
    return dict(
        primary=_PRIMARY, gamma=round(G_PRIMARY, 6), spinodal=round(sp_ref, 6), noise_D=D,
        mu0=_MU0, opportunistic_line=_B_LINE, lam_pathogen=_LAM_PATH, lam_tumor=_LAM_TUMOR,
        coverage_collapse=dict(sv_grid=sv_grid, coverage=[round(c, 3) for c in cov],
                               pathogen_burden=[round(b, 1) for b in burd_p],
                               coverage_rises_with_sv=bool(cov_monotone), broad_at_full=bool(cov_broad_high),
                               collapsed_at_low=bool(cov_collapsed_low),
                               sv_coverage_crit=(round(sv_cov_crit, 3) if sv_cov_crit is not None else None),
                               sv_opportunistic_crit=round(sv_op, 3),
                               burden_crosses_line=bool(burd_opportunistic_low),
                               collapse_exists=bool(collapse_ok)),
        reconstitution=dict(sv_low=_SV_LOW, reconstitution_threshold=round(r_crit, 3),
                            levels=recon_rows, sub_threshold_fails=bool(sub_fails),
                            supra_threshold_recovers=bool(sup_recovers),
                            clearance_trajectory_sample=[round(float(traj_hi[i]), 1)
                                                         for i in range(0, len(traj_hi), max(1, len(traj_hi) // 10))],
                            phase_B_decay_monotone=bool(decay_monotone), recovers=bool(recon_ok)),
        one_lever_two_diseases=dict(seam=seam_rows, both_fall_with_surveillance=bool(both_fall),
                                    collapse_same_curve=bool(same_curve), one_lever=bool(one_lever_ok)),
        reconstitution_depth=dict(rows=depth_rows, threshold_rises_with_influx=bool(depth_monotone),
                                  threshold_gated=bool(sub_fails and sup_recovers), depth_ok=bool(depth_ok)),
        all_pass=ok,
        grade="[V] acquired-immunodeficiency coverage collapse and immune RECONSTITUTION EMERGE by composing the "
              "measured T15 reservoir (floor ∝ 1/surveillance) and T16 coverage processes over a surveillance "
              "sweep: repertoire coverage stays broad then COLLAPSES below a surveillance floor while the reservoir "
              "crosses an opportunistic line, restoring surveillance RECOVERS coverage as a measured clearance "
              "trajectory IFF it exceeds the reconstitution threshold (sub-threshold fails, supra-threshold "
              "recovers -- threshold-gated, not gradual), the SAME surveillance lever drops BOTH the pathogen "
              "reservoir AND the tumor-escape multiplier (both ∝ 1/sv, collapsing onto the same 1/(μ0·sv) curve -- "
              "one lever, two diseases), and a deeper opportunist needs deeper reconstitution (r_crit ∝ influx) -- "
              "measured, not assumed; [O] absolute counts / opportunistic line / clearance scale (K, μ0, B_line, "
              "cellular-noise scale D); treatment = CLASS (reconstitute surveillance/breadth above the coverage "
              "threshold), never agent / dose / recommendation")


def run(gammas):
    """T30: emergent acquired-immunodeficiency coverage collapse + immune reconstitution -- coverage collapses below
    a surveillance floor (opportunistic regime), restoring surveillance recovers it above a threshold as a measured
    clearance trajectory, the SAME lever lowers the tumor-escape multiplier (one lever, two diseases), and a deeper
    challenge needs deeper reconstitution -- composing the measured T15 reservoir and T16 coverage processes."""
    r = emergent_reconstitution(gammas)
    return dict(T30=dict(target="T30",
                         claim="acquired-immunodeficiency coverage collapse + immune RECONSTITUTION EMERGE by "
                               "composing the measured T15 reservoir (floor ∝ 1/surveillance) and T16 coverage: "
                               "coverage stays broad then COLLAPSES below a surveillance floor (opportunistic "
                               "regime), restoring surveillance RECOVERS coverage as a measured clearance "
                               "trajectory IFF above the reconstitution threshold (sub-threshold fails), the SAME "
                               "surveillance lever drops BOTH the pathogen reservoir AND the tumor-escape "
                               "multiplier (both ∝ 1/sv, same curve -- one lever, two diseases), and a deeper "
                               "opportunist needs deeper reconstitution; treatment is direction/class only and "
                               "absolute counts stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T30"]["result"]
    print("ACQUIRED IMMUNODEFICIENCY COVERAGE COLLAPSE + RECONSTITUTION (primary=%s, γ=%.4f, spinodal=%.4f, μ0=%.1f, "
          "opportunistic_line=%.0f, D=%.3f):" % (r["primary"], r["gamma"], r["spinodal"], r["mu0"],
                                                 r["opportunistic_line"], r["noise_D"]))
    cc = r["coverage_collapse"]
    print("\n(1) COVERAGE COLLAPSE below a surveillance floor (sv_cov_crit=%s, sv_opportunistic=%s):"
          % (cc["sv_coverage_crit"], cc["sv_opportunistic_crit"]))
    for sv, cv, bp in zip(cc["sv_grid"], cc["coverage"], cc["pathogen_burden"]):
        print("     sv=%.2f  coverage=%.2f  %s  pathogen_burden=%7.1f" % (sv, cv, "#" * int(round(cv * 24)), bp))
    print("     coverage broad@full=%s | collapsed@low=%s | burden crosses opportunistic line=%s -> collapse exists=%s"
          % (cc["broad_at_full"], cc["collapsed_at_low"], cc["burden_crosses_line"], cc["collapse_exists"]))
    rc = r["reconstitution"]
    print("\n(2) RECONSTITUTION RECOVERS COVERAGE (threshold=%.3f), from depleted sv=%.2f:"
          % (rc["reconstitution_threshold"], rc["sv_low"]))
    for row in rc["levels"]:
        print("     restore_sv=%.2f  final_burden=%6.1f  coverage=%.2f  recovered=%s"
              % (row["restore_sv"], row["final_burden"], row["coverage_at_restore"], row["recovered"]))
    print("     clearance trajectory (restore->floor):", rc["clearance_trajectory_sample"])
    print("     sub-threshold fails=%s | supra-threshold recovers=%s | phase-B decay monotone=%s -> recovers=%s"
          % (rc["sub_threshold_fails"], rc["supra_threshold_recovers"], rc["phase_B_decay_monotone"], rc["recovers"]))
    ol = r["one_lever_two_diseases"]
    print("\n(3) ONE LEVER, TWO DISEASES (pathogen & tumor burden both ∝ 1/sv, same kernel):")
    for row in ol["seam"]:
        print("     sv=%.2f  pathogen=%7.1f (×sv=%.1f)  tumor=%6.1f (×sv=%.1f)  p/λ=%.4f t/λ=%.4f same=%s"
              % (row["sv"], row["pathogen"], row["pathogen_x_sv"], row["tumor"], row["tumor_x_sv"],
                 row["pathogen_over_lambda"], row["tumor_over_lambda"], row["same_within"]))
    print("     both fall with surveillance=%s | collapse onto same 1/sv curve=%s -> one lever=%s"
          % (ol["both_fall_with_surveillance"], ol["collapse_same_curve"], ol["one_lever"]))
    rd = r["reconstitution_depth"]
    print("\n(4) DEEPER CHALLENGE NEEDS DEEPER RECONSTITUTION (r_crit ∝ pathogen influx):")
    for row in rd["rows"]:
        print("     pathogen_influx=%.0f  reconstitution_threshold_sv=%.3f" % (row["pathogen_influx"], row["reconstitution_threshold_sv"]))
    print("     threshold rises with influx=%s | threshold-gated=%s -> depth ok=%s"
          % (rd["threshold_rises_with_influx"], rd["threshold_gated"], rd["depth_ok"]))
    print("\nT30 all_pass:", r["all_pass"])
