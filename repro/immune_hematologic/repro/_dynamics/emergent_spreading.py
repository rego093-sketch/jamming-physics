#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergent_spreading.py  --  EMERGENT epitope spreading / flare cascade as a MEASURED recruitment threshold of a
COUPLED population of escaped self-clones (the autoimmune disease made systemic, not asserted, not fitted).
[DISEASE/TREATMENT axis: roadmap D1, target T28.]

WHY THIS EXISTS (v0.11.0). T23 (emergent_autoimmunity.py) MEASURED that ONE escaped self-clone breaks tolerance
under an insult and latches ON. T12/T16 (emergent_competition / emergent_repertoire) MEASURED that clones sharing
an antigen pool are COUPLED. Real autoimmune disease is not one clone: once one self-epitope's tolerance breaks,
the released inflammation and self-antigen can recruit NEIGHBOURING self-clones past their own break thresholds --
epitope spreading, the relapsing-remitting flare cascade of established autoimmunity (one breaks, the disease
broadens). The VP discipline is emergence: whether one break STAYS local or AVALANCHES through the repertoire,
and what sets the boundary, must come OUT of the coupled substrate, MEASURED.

This module builds Nc escaped self-clones (each an R19 switch carrying a sub-spinodal residual self-drive, so each
is individually BISTABLE -- T23's escaped clones), with residuals spread evenly across a tolerant band, all
coupled through a shared inflammatory field: every clone that is ON raises the drive on EVERY clone by κ·(fraction
ON). A subtractive peripheral suppressor field σ (the T24 regulatory tone) is applied to all clones. The system
starts fully tolerant (all OFF); a localized insult SEEDS the least-tolerant clone ON; the insult is withdrawn and
the coupled field is allowed to settle under noise,

    ds_i = (γ s_i − s_i³ + h_i) dt + sqrt(2 D dt)·ξ,   h_i = (base_i + κ·frac_ON − σ)·spinodal,

and the FINAL recruited fraction (clones that ended ON) is MEASURED. Sweeping the coupling κ (and σ) MEASURES the
cascade boundary. Nothing about it is assumed.

WHAT EMERGES (measured, deterministic seed=19):
  1. A CASCADE (RECRUITMENT) THRESHOLD EXISTS. Below a critical coupling κ the seeded break stays LOCAL -- the
     recruited fraction sits near the seed alone (1/Nc); above κ_crit it AVALANCHES -- each newly broken clone
     raises the shared field enough to break the next-most-tolerant clone, so the recruited fraction jumps toward
     the whole repertoire. The measured final recruited fraction is a sharp, monotone increasing function of κ
     with a threshold (it crosses 1/2 at κ_crit): epitope spreading is a coupling-driven avalanche, MEASURED.
  2. PERIPHERAL SUPPRESSION RAISES THE THRESHOLD (the T24 → T28 link). Adding the subtractive suppressor field σ
     shifts κ_crit UP, monotonically: with more regulatory tone, a STRONGER coupling is needed before the cascade
     becomes self-sustaining. Regulatory suppression does not just contain one clone (T24) -- it raises the bar for
     the whole repertoire to broaden, MEASURED.
  3. SPREADING REQUIRES A SEED (honest control). With NO seeded break, the escaped repertoire sits sub-threshold
     and NOTHING cascades even at the highest coupling (measured recruited fraction ≈ 0): the coupling term is
     κ·frac_ON, and with frac_ON = 0 there is no drive to propagate -- the cascade is triggered, not spontaneous.
  4. DEEPER TOLERANCE RAISES THE THRESHOLD (the T21 → T28 link). Shifting the whole residual band DOWN
     (deeper-tolerant neighbours, the survivors of deeper central deletion) raises κ_crit: a more deeply tolerant
     repertoire resists spreading -- so deeper central tolerance (T21) protects against epitope spreading just as
     it lowers single-clone break susceptibility (T23), MEASURED.

TREATMENT DIRECTION (roadmap discipline -- CLASS only). The dynamics say flare-broadening is an avalanche with a
suppression-tunable threshold: raising regulatory tone (σ) or deepening tolerance (T21) raises the spreading
threshold, and -- combined with T27 -- re-tolerizing the seed before it recruits is the basin-acting move. This is
a re-description of epitope spreading in the coupled R19 formalism and a treatment DIRECTION; it is NOT a drug,
dose, schedule, recommendation, or VP validation, and NOT medical advice.

GRADES (C3): the existence of a recruitment threshold, its rise with peripheral suppression, the seed-required
control, and its rise with deeper tolerance are [V] emergent (measured from the coupled stochastic population).
The ABSOLUTE coupling / spread rate / clone number -- set by the coupling κ, the suppressor σ, the residual band,
the repertoire size Nc, and the free cellular-noise scale D -- is [O], no fabricated numbers. Determinism: fixed
seed, BLAS pinned upstream, round-before-report.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import spinodal, SEED

_ORGANS  = ["bone_marrow_hematopoiesis", "spleen", "thymus", "lymphoid_adaptive"]
_PRIMARY = "lymphoid_adaptive"        # the adaptive compartment where the escaped self-repertoire resides

# --- deterministic simulation size (fixed; no per-condition tuning) -----------------------------------
_NC     = 10        # self-clones in the coupled repertoire
_R      = 48        # independent realizations (for the recruited-fraction probability)
_DT     = 0.01      # integration timestep
_D      = 0.02      # cellular-noise scale (absolute value is [O])
_SEED_DUR = 300     # seeding-insult duration (break the least-tolerant clone)
_SETTLE   = 800     # coupled settle after the seed insult is withdrawn (decide the cascade)
_SEED_INSULT = 1.6  # seeding insult amplitude on clone 0 (× spinodal; supra-threshold for the seed clone)

# each ON clone adds a FIXED increment κ to the shared inflammatory tone (count-based mean field): a broken clone's
# inflammatory burst raises every clone's drive, so the cascade bottleneck is the seed bridging the gap to its
# nearest neighbour (κ·1 ≥ 1 − base_neighbour) and κ_crit ≈ 1 − (least-tolerant residual).
_BASE_LO_REF = 0.30     # most-tolerant neighbour residual (× spinodal)
_BASE_HI_REF = 0.70     # least-tolerant neighbour residual = the seed clone (× spinodal; sub-spinodal)
_KAPPA_GRID  = (0.05, 0.12, 0.20, 0.26, 0.30, 0.34, 0.40, 0.48, 0.60, 0.72, 0.85)  # per-ON-clone coupling grid (× spinodal)
_SIGMA_SWEEP = (0.00, 0.15, 0.30)                                                  # peripheral suppression sweep (coarsened)
_BAND_SHIFT  = (0.00, 0.10, 0.20)                                                  # deepen the whole band (T21 depth)


def _bases(nc=_NC, lo=_BASE_LO_REF, hi=_BASE_HI_REF):
    """Residual self-drives spread evenly across the tolerant band; clone 0 = least-tolerant (the seed)."""
    return np.linspace(hi, lo, nc)


def recruited_fraction(g, kappa, sigma=0.0, lo=_BASE_LO_REF, hi=_BASE_HI_REF, seed_on=True,
                       D=_D, nc=_NC, R=_R, dt=_DT, seed=SEED):
    """MEASURED final recruited fraction of a coupled escaped repertoire: seed the least-tolerant clone ON (if
    seed_on), withdraw the seed insult, settle the count-coupled population under noise, report the mean fraction
    of clones that ended ON (averaged over realizations). h_i = (base_i + κ·n_ON − σ)·spinodal, n_ON = count ON."""
    rng = np.random.default_rng(seed)
    sp = spinodal(g)
    base = _bases(nc, lo, hi)[None, :]                    # (1, nc)
    s = np.full((R, nc), -math.sqrt(g))                   # all clones start tolerant (OFF)
    sq = math.sqrt(2.0 * D * dt)
    # --- seeding window: localized insult on clone 0 (the least-tolerant) ---
    if seed_on:
        seed_col = np.concatenate([np.full((R, 1), _SEED_INSULT * sp), np.zeros((R, nc - 1))], axis=1)
        for _ in range(_SEED_DUR):
            h = (base - sigma) * sp + seed_col
            s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal((R, nc))
            np.clip(s, -5.0, 5.0, out=s)
    # --- coupled settle: withdraw the seed insult, count-based shared inflammation propagates ---
    for _ in range(_SETTLE):
        n_on = (s > 0.0).sum(axis=1, keepdims=True)       # (R, 1) NUMBER of clones ON per realization
        h = (base + kappa * n_on - sigma) * sp
        s += (g * s - s ** 3 + h) * dt + sq * rng.standard_normal((R, nc))
        np.clip(s, -5.0, 5.0, out=s)
    return float((s > 0.0).mean())


def _kappa_threshold(g, sigma=0.0, lo=_BASE_LO_REF, hi=_BASE_HI_REF, grid=_KAPPA_GRID, D=_D, seed=SEED):
    """Interpolate the coupling κ (× spinodal) at which the recruited fraction crosses 1/2 (rising in κ)."""
    fs = [recruited_fraction(g, k, sigma=sigma, lo=lo, hi=hi, D=D, seed=seed) for k in grid]
    if fs[0] >= 0.5:
        return grid[0], fs
    for i in range(1, len(fs)):
        if fs[i - 1] < 0.5 <= fs[i]:
            f = (0.5 - fs[i - 1]) / (fs[i] - fs[i - 1])
            return grid[i - 1] + f * (grid[i] - grid[i - 1]), fs
    return (grid[-1] if fs[-1] >= 0.5 else float("inf")), fs


def emergent_spreading(gammas, D=_D):
    g_ref = gammas[_PRIMARY]; sp_ref = spinodal(g_ref)

    # (1) CASCADE THRESHOLD EXISTS: recruited fraction is monotone in κ and crosses 1/2 at κ_crit
    k_crit, fs = _kappa_threshold(g_ref, sigma=0.0, D=D)
    kappa_curve = [dict(kappa=round(k, 3), recruited_fraction=round(f, 3)) for k, f in zip(_KAPPA_GRID, fs)]
    monotone_in_kappa = bool(all(fs[i + 1] >= fs[i] - 0.05 for i in range(len(fs) - 1)))
    has_threshold = bool(fs[0] < 0.5 and fs[-1] > 0.5 and math.isfinite(k_crit))
    low_stays_local = bool(fs[0] <= 0.25)          # below threshold: near the seed alone (1/Nc small)
    high_cascades   = bool(fs[-1] >= 0.85)         # above threshold: whole repertoire recruited
    cascade_ok = bool(monotone_in_kappa and has_threshold and low_stays_local and high_cascades)

    # (2) PERIPHERAL SUPPRESSION RAISES THE THRESHOLD (T24 -> T28)
    supp_rows = []
    for sg in _SIGMA_SWEEP:
        kc, _ = _kappa_threshold(g_ref, sigma=sg, D=D)
        supp_rows.append(dict(sigma=round(sg, 3), kappa_crit=(round(kc, 3) if math.isfinite(kc) else None)))
    kc_seq = [r["kappa_crit"] for r in supp_rows if r["kappa_crit"] is not None]
    suppression_raises = bool(len(kc_seq) == len(supp_rows)
                              and all(kc_seq[i] <= kc_seq[i + 1] + 1e-9 for i in range(len(kc_seq) - 1))
                              and kc_seq[-1] > kc_seq[0])

    # (3) SPREADING REQUIRES A SEED (control): no seed -> no cascade even at the highest coupling
    f_noseed_hi = recruited_fraction(g_ref, _KAPPA_GRID[-1], sigma=0.0, seed_on=False, D=D)
    seed_required = bool(f_noseed_hi < 0.10)

    # (4) DEEPER TOLERANCE RAISES THE THRESHOLD (T21 -> T28): shift the whole band down
    band_rows = []
    for d in _BAND_SHIFT:
        kc, _ = _kappa_threshold(g_ref, sigma=0.0, lo=_BASE_LO_REF - d, hi=_BASE_HI_REF - d, D=D)
        band_rows.append(dict(band_shift_down=round(d, 3),
                              kappa_crit=(round(kc, 3) if math.isfinite(kc) else None)))
    bc_seq = [r["kappa_crit"] for r in band_rows if r["kappa_crit"] is not None]
    deeper_tolerance_raises = bool(len(bc_seq) == len(band_rows)
                                   and all(bc_seq[i] <= bc_seq[i + 1] + 1e-9 for i in range(len(bc_seq) - 1))
                                   and bc_seq[-1] > bc_seq[0])

    ok = bool(cascade_ok and suppression_raises and seed_required and deeper_tolerance_raises)
    return dict(
        primary=_PRIMARY, gamma=round(g_ref, 6), spinodal=round(sp_ref, 6), noise_D=D,
        n_clones=_NC, residual_band=dict(most_tolerant=_BASE_LO_REF, least_tolerant_seed=_BASE_HI_REF),
        cascade_threshold=dict(kappa_crit=(round(k_crit, 3) if math.isfinite(k_crit) else None),
                               kappa_curve=kappa_curve, monotone_in_kappa=bool(monotone_in_kappa),
                               has_threshold=bool(has_threshold), low_kappa_stays_local=bool(low_stays_local),
                               high_kappa_cascades=bool(high_cascades), cascade_ok=bool(cascade_ok)),
        suppression_raises_threshold=dict(rows=supp_rows, holds=bool(suppression_raises)),
        seed_required=dict(no_seed_high_kappa_recruited=round(f_noseed_hi, 3), holds=bool(seed_required)),
        deeper_tolerance_raises_threshold=dict(rows=band_rows, holds=bool(deeper_tolerance_raises)),
        all_pass=ok,
        grade="[V] epitope spreading / the flare cascade EMERGES from a mean-field-coupled escaped self-repertoire: "
              "a seeded single break stays LOCAL below a critical coupling and AVALANCHES through the repertoire "
              "above it (measured recruited fraction monotone in κ, crossing 1/2 at κ_crit), peripheral regulatory "
              "suppression σ raises κ_crit (the T24 containment generalized to the whole repertoire), the cascade "
              "REQUIRES a seeded break (no seed → no spreading even at maximal coupling, κ·frac_ON with frac_ON=0), "
              "and a deeper-tolerant residual band raises κ_crit so deeper central tolerance (T21) resists spreading "
              "-- measured, not assumed; [O] absolute coupling / spread rate / clone number (κ, σ, residual band, "
              "repertoire size, cellular-noise scale D); treatment = CLASS/DIRECTION, never agent / dose")


def run(gammas):
    """T28: emergent epitope spreading / flare cascade -- a coupled escaped self-repertoire in which a seeded
    single break avalanches past a measured coupling threshold, raised by peripheral suppression (T24) and by
    deeper central tolerance (T21), and requiring a seed -- the systemic broadening dual of the T23 single break."""
    r = emergent_spreading(gammas)
    return dict(T28=dict(target="T28",
                         claim="epitope spreading / the relapsing-remitting flare cascade EMERGES from a mean-field-"
                               "coupled population of escaped self-clones: a seeded single break (T23) stays local "
                               "below a critical coupling κ and avalanches through the repertoire above it (measured "
                               "recruited fraction monotone in κ, threshold at κ_crit), peripheral regulatory "
                               "suppression (T24) raises κ_crit, the cascade requires a seed (no break → no "
                               "spreading), and deeper central tolerance (T21) raises κ_crit -- measured, not "
                               "assumed; absolute coupling / spread rate stay [O]",
                         result=r, all_pass=r["all_pass"], grade=r["grade"]))


if __name__ == "__main__":
    G = {"bone_marrow_hematopoiesis": 1.3225, "spleen": 1.4228, "thymus": 1.4533, "lymphoid_adaptive": 1.4892}
    r = run(G)["T28"]["result"]
    print("EPITOPE SPREADING / FLARE CASCADE of a coupled escaped self-repertoire (primary=%s, γ=%.4f, spinodal=%.4f, Nc=%d, D=%.3f):"
          % (r["primary"], r["gamma"], r["spinodal"], r["n_clones"], r["noise_D"]))
    ct = r["cascade_threshold"]
    print("\n(1) CASCADE THRESHOLD (recruited fraction vs coupling κ), κ_crit=%s:" % ct["kappa_crit"])
    for row in ct["kappa_curve"]:
        bar = "#" * int(round(row["recruited_fraction"] * 30))
        print("     κ=%.2f×sp  recruited=%.3f  %s" % (row["kappa"], row["recruited_fraction"], bar))
    print("     monotone=%s | threshold=%s | low stays local=%s | high cascades=%s -> cascade_ok=%s"
          % (ct["monotone_in_kappa"], ct["has_threshold"], ct["low_kappa_stays_local"],
             ct["high_kappa_cascades"], ct["cascade_ok"]))
    print("\n(2) PERIPHERAL SUPPRESSION RAISES κ_crit (T24 -> T28):")
    for row in r["suppression_raises_threshold"]["rows"]:
        print("     σ=%.2f×sp  κ_crit=%s" % (row["sigma"], row["kappa_crit"]))
    print("     -> monotone rising: %s" % r["suppression_raises_threshold"]["holds"])
    sr = r["seed_required"]
    print("\n(3) SPREADING REQUIRES A SEED (control): no seed, max κ -> recruited=%.3f -> seed required=%s"
          % (sr["no_seed_high_kappa_recruited"], sr["holds"]))
    print("\n(4) DEEPER TOLERANCE RAISES κ_crit (T21 -> T28; shift band down):")
    for row in r["deeper_tolerance_raises_threshold"]["rows"]:
        print("     band_shift_down=%.2f  κ_crit=%s" % (row["band_shift_down"], row["kappa_crit"]))
    print("     -> monotone rising: %s" % r["deeper_tolerance_raises_threshold"]["holds"])
    print("\nT28 all_pass:", r["all_pass"])
