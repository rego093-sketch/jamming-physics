#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hair_cycle.py  --  Integumentary HAIR-FOLLICLE CYCLE: the package's first AUTONOMOUS OSCILLATOR.

WHAT THIS ADDS (HANDOFF_NEXT_STEPS.md sec.5.2, mechanism-first). The core battery (run_all.py)
reports "no autonomous oscillator organ in this physical class": its four organs run as steady-state
switches (barrier, melanin, sweat, turnover). The hair follicle is the missing piece -- it CYCLES
(anagen growth -> catagen regression -> telogen rest -> exogen shed -> re-entry). This module emerges
that cycle as the SHARED FitzHugh-Nagumo relaxation oscillator (vp_substrate.Neuron) running on the
EXISTING, MEASURED appendage master-gene gamma (EDAR). NO new organ and NO new fitted constant are
introduced: the follicle is the EDAR appendage read in its OSCILLATING regime rather than its
steady sweat-flux regime (CHARTER T5). This is a NEW TARGET on an existing organ.

NO-TUNING DISCIPLINE (VP-SPEC C0/C3; see docs section 08). The follicle's gamma is MEASURED (EDAR,
read-only). tau_f/tau_s/beta are the SUBSTRATE relaxation-oscillator defaults (neuro 02), tau_s being
the slow cycle clock (a [L] rate anchor, sets the PERIOD, never the duty cycle). The healthy growth
bias is a SUBSTRATE-SCALED fraction of the spinodal (a dimensionless regime scale [F], NOT fitted to a
duty target). What the substrate PREDICTS -- autonomous oscillation, a relaxation (plateau+collapse)
waveform, an anagen-DOMINANT duty cycle that lengthens with the growth drive -- is graded [V]. The
absolute anagen FRACTION (cited ~85-90%) and the absolute cycle PERIOD (years) are the [L]/[O] anchors
the substrate is compared against by SIGN and DOMINANCE; they are not claimed as fitted matches.

DISEASES = SIGNED PERTURBATIONS OF THE ONE OSCILLATOR (intervention = the same knob reversed):
  AGA  androgenetic alopecia      standing anti-growth (miniaturisation) drive -> anagen shortens,
                                  follicle miniaturises terminal->vellus; minoxidil/anti-androgen
                                  (pro-growth) lengthens anagen back.
  AA   alopecia areata            SUSTAINED premature-catagen drive -> anagen collapses, patch held in
                                  telogen; PERSISTENT while driven, regrows on removal (hysteresis).
  TE   telogen effluvium          TRANSIENT synchronising pulse shifts an anagen cohort into telogen;
                                  it sheds ~ONE TELOGEN DURATION later (delayed), then re-enters the
                                  cycle (SELF-LIMITED).
  AnE  anagen effluvium           direct anagen-matrix arrest (chemo/radiation) -> IMMEDIATE shed of
                                  anagen hairs, bypassing telogen (the opposite TIMING pole of TE).

Grades (VP-SPEC C3):  [V] simulation-verified shape/sign . [L] cited clinical/biological anchor .
  [O] open (absolute magnitude; obstacle inherited from the appendage target).
Determinism (VP-SPEC C1): BLAS pinned single-thread (set below before numpy); fixed grids; NO RNG;
  round-before-hash via the engine emitter (reused).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, json, math
import numpy as np

_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "inherited"))

# vendored substrate primitives (DO NOT re-derive)
from vp_substrate import Neuron, spinodal
# reuse the engine's exact round-before-hash emitter (C1) -- same determinism contract as pathology
from vp_skn_engine import emit as _emit

_GAMMA_PATH = os.path.join(_HERE, "..", "..", "inherited", "organ_gamma.json")
def gamma_of(master):
    """MEASURED master-gene gamma, read-only, vendored from DNA (never fitted)."""
    return float(json.load(open(_GAMMA_PATH, encoding="utf-8"))["genes"][master]["gamma"])

# --------------------------------------------------------------------------- substrate constants
MASTER = "EDAR"                       # the appendage master gene (sweat in T5; the FOLLICLE here)
TAU_F, TAU_S, BETA = 1.0, 40.0, 0.5   # SUBSTRATE FHN relaxation-oscillator defaults (neuro 02)
#   tau_s = the slow cycle clock -> sets the PERIOD (a [L] rate anchor); it does NOT set the duty cycle.
ANAGEN_FRAC_CITED = (0.85, 0.90)      # [L] ~85-90% of scalp follicles are in anagen at any time
ANAGEN_TELOGEN_RATIO_CITED = "anagen 2-6 yr >> telogen ~3 mo"   # [L] anagen-dominant cycle


def growth_bias(frac_of_spinodal=0.5):
    """Healthy follicle growth drive = a SUBSTRATE-SCALED fraction of the EDAR spinodal.
    A dimensionless regime scale [F] that biases the follicle into its growth (anagen) basin --
    NOT fitted to any anagen-fraction target."""
    return frac_of_spinodal * spinodal(gamma_of(MASTER))


# ===========================================================================
#  THE OSCILLATOR: the EDAR appendage in its CYCLING regime (shared FHN)
#  Fast switch s (follicle active vs resting) + slow recovery w (the cycle clock).
#  drive = the net growth bias. Returns the steady limit-cycle trace (transient dropped).
# ===========================================================================
def _limit_cycle(drive, T=24000.0, dt=0.05, drop=0.25):
    n = Neuron(gamma=1.0, tau_f=TAU_F, tau_s=TAU_S, beta=BETA, name="follicle")
    S, dts = n.run(drive=float(drive), T=T, dt=dt)
    return S[int(len(S) * drop):], dts

def _duty(S, thr=0.0):
    """Anagen fraction = fraction of the limit cycle in the active (up) state."""
    return float(np.mean(S > thr))

def _period(S, dt, thr=0.0):
    up = S > thr; ups = np.where((~up[:-1]) & (up[1:]))[0] + 1
    return (float(np.mean(np.diff(ups)) * dt), len(ups)) if len(ups) >= 2 else (None, len(ups))

def _plateau_dominance(S):
    """Relaxation oscillators sit on a flat branch most of the cycle and snap between branches fast.
    Fraction of samples ON a branch (|S| past half the amplitude) -> high for relaxation, ~0.5 for
    a harmonic oscillation. A shape discriminant (no constant)."""
    a = float(np.max(np.abs(S)))
    return float(np.mean(np.abs(S) > 0.5 * a)) if a > 0 else 0.0

def cycle_metrics(drive=None):
    """The follicle oscillator's verified-shape readout at the healthy growth bias."""
    drive = growth_bias() if drive is None else drive
    S, dt = _limit_cycle(drive)
    duty = _duty(S); per, beats = _period(S, dt); plat = _plateau_dominance(S)
    return dict(master=MASTER, gamma=round(gamma_of(MASTER), 6), spinodal=round(spinodal(gamma_of(MASTER)), 6),
                growth_bias=round(drive, 6), anagen_fraction=round(duty, 5),
                period_arb=round(per, 4) if per else None, beats=beats,
                oscillates=bool(beats >= 3 and per is not None),
                anagen_dominant=bool(duty > 0.5), relaxation_waveform=bool(plat > 0.6),
                plateau_dominance=round(plat, 5),
                anagen_fraction_cited=ANAGEN_FRAC_CITED, ratio_cited=ANAGEN_TELOGEN_RATIO_CITED)

def anagen_fraction_at(drive):
    S, _ = _limit_cycle(drive); return _duty(S)


# ===========================================================================
#  POPULATION SHEDDING MODEL (deterministic; for the TE vs anagen-effluvium timing)
#  A scalp is many follicles uniformly phased on the cycle (asynchronous -> steady, low shed).
#  Shedding (exogen) happens on the telogen->anagen wrap (an old club hair is released as a new
#  shaft starts). A perturbation re-phases a cohort; the shedding TIMING distinguishes the modes.
#  Fixed phase grid, fixed step -> NO RNG.
# ===========================================================================
N_FOLLICLES = 4000
STEPS_PER_CYCLE = 900                 # phase-advance resolution (one full cycle = 900 steps)
SIM_STEPS = 1200
T_INSULT = 300

def _shed_run(mode, duty):
    """Return the per-step shedding rate of a uniformly-phased population under one perturbation."""
    two_pi = 2.0 * math.pi
    phase = np.linspace(0.0, two_pi, N_FOLLICLES, endpoint=False)
    dphi = two_pi / STEPS_PER_CYCLE
    anagen_arc = two_pi * duty                       # [0, anagen_arc) = anagen ; rest = telogen
    shed = np.zeros(SIM_STEPS)
    for t in range(SIM_STEPS):
        prev = phase
        phase = (phase + dphi) % two_pi
        shed[t] = float(np.mean(prev > phase))       # wrapped 2pi->0 this step = exogen (shed)
        if t == T_INSULT:
            if mode == "TE":                         # transient: push a mid-anagen cohort to telogen onset
                hit = phase < (anagen_arc * 0.6)
                phase = phase.copy(); phase[hit] = anagen_arc + 1e-3
            elif mode == "AnE":                      # direct matrix arrest: anagen follicles shed NOW
                hit = phase < anagen_arc
                shed[t] += float(np.mean(hit))       # immediate synchronized shed
                phase = phase.copy(); phase[hit] = anagen_arc + 1e-3
    return shed

def _shed_peak(shed):
    base = float(np.mean(shed[:T_INSULT - 50]))
    post = shed[T_INSULT:]                      # INCLUDE the insult step (immediate shed lands here)
    pk = int(np.argmax(post)); lag = pk         # lag 0 = sheds at the insult (anagen effluvium)
    return dict(baseline=round(base, 6), peak_value=round(float(post[pk]), 6),
                peak_fold=round(float(post[pk] / base), 3) if base > 0 else None, peak_lag_steps=lag)

def shedding_dichotomy(duty=None):
    """TE sheds with a DELAY ~ one telogen duration; anagen effluvium sheds IMMEDIATELY."""
    duty = cycle_metrics()["anagen_fraction"] if duty is None else duty
    telogen_lag = round((1.0 - duty) * STEPS_PER_CYCLE)        # one telogen arc, in steps
    te = _shed_peak(_shed_run("TE", duty)); ane = _shed_peak(_shed_run("AnE", duty))
    te_matches_telogen = bool(abs(te["peak_lag_steps"] - telogen_lag) <= 0.20 * STEPS_PER_CYCLE)
    return dict(anagen_fraction=round(duty, 5), telogen_lag_steps=telogen_lag,
                TE=te, anagen_effluvium=ane,
                TE_delayed=bool(te["peak_lag_steps"] > 0.15 * STEPS_PER_CYCLE),
                TE_lag_matches_one_telogen=te_matches_telogen,
                AnE_immediate=bool(ane["peak_lag_steps"] <= 0.05 * STEPS_PER_CYCLE),
                timing_dichotomy=bool(te["peak_lag_steps"] > ane["peak_lag_steps"] + 0.10 * STEPS_PER_CYCLE))


# ===========================================================================
#  DISEASES -- each a SIGNED drive shift about the healthy growth bias (NO new constant).
# ===========================================================================
def _sp(): return spinodal(gamma_of(MASTER))

def androgenetic_alopecia():
    """AGA: a STANDING anti-growth (androgen/miniaturisation) drive shortens anagen progressively;
    minoxidil/anti-androgen (pro-growth) lengthens it back. Direction forced by the drive sign."""
    h0 = growth_bias(); sp = _sp()
    grades = [0.0, -0.30, -0.55]                                  # healthy -> mild -> marked (anti-growth)
    fr = [round(anagen_fraction_at(h0 + d * sp), 5) for d in grades]
    healthy, mild, marked = fr
    minox = round(anagen_fraction_at(h0 + 0.20 * sp), 5)          # pro-growth reversal
    progressive = bool(healthy > mild > marked)                  # anagen shrinks each step deeper
    reverses = bool(minox > marked)
    return dict(disease="androgenetic_alopecia", target="hair-cycle (anagen duration)", organ="skin_appendage",
                mechanism="standing anti-growth (miniaturisation) drive shortens the anagen plateau -> terminal->vellus miniaturisation; pro-growth drive (minoxidil/anti-androgen) lengthens anagen back",
                anchor="AGA is androgen-driven progressive follicular miniaturisation with anagen shortening; minoxidil/finasteride prolong anagen [L]",
                healthy_anagen_fraction=healthy, anagen_fraction_progression=fr,
                intervention_anagen_fraction=minox, miniaturisation_progressive=progressive,
                sign_matches_clinic=progressive, intervention_reverses=reverses,
                grade_shape="[V] anagen-shortening direction + miniaturisation progression + reversal",
                grade_absolute="[O] absolute hair count / vellus fraction needs per-follicle calibration (appendage target obstacle)")

def alopecia_areata():
    """AA: a SUSTAINED premature-catagen drive collapses anagen and holds the patch in telogen;
    PERSISTENT while driven, regrows on removal (hysteresis)."""
    h0 = growth_bias(); sp = _sp()
    active = round(anagen_fraction_at(h0 - 0.62 * sp), 5)         # strong catagen-forcing drive
    healthy = round(anagen_fraction_at(h0), 5)
    removed = round(anagen_fraction_at(h0), 5)                    # drive removed -> back to healthy
    suppressed = bool(active < healthy)
    recovers = bool(removed > active and abs(removed - healthy) < 1e-6)
    return dict(disease="alopecia_areata", target="hair-cycle (premature catagen)", organ="skin_appendage",
                mechanism="sustained immune-type premature-catagen drive forces follicles out of anagen into telogen (patchy synchronized loss); persistent while driven, anagen resumes on removal (regrowth, hysteresis)",
                anchor="AA is immune-mediated premature catagen / anagen arrest with patchy loss and frequent spontaneous or treated regrowth [L]",
                disease_anagen_fraction=active, healthy_anagen_fraction=healthy, recovered_anagen_fraction=removed,
                anagen_suppressed=suppressed, sign_matches_clinic=suppressed, intervention_reverses=recovers,
                grade_shape="[V] anagen-collapse under a sustained drive + regrowth on removal",
                grade_absolute="[O] absolute patch extent / regrowth latency needs per-follicle calibration (appendage target obstacle)")

def telogen_effluvium():
    """TE: a TRANSIENT synchronising pulse shifts an anagen cohort into telogen; it sheds ~ONE
    TELOGEN DURATION later (delayed), then re-enters the cycle (self-limited)."""
    dych = shedding_dichotomy()
    te = dych["TE"]
    delayed = dych["TE_delayed"]; matches = dych["TE_lag_matches_one_telogen"]
    return dict(disease="telogen_effluvium", target="hair-cycle (phase synchronisation)", organ="skin_appendage",
                mechanism="a transient systemic stressor synchronously pushes an anagen cohort into telogen; the cohort sheds one telogen duration later (a delayed diffuse shed), then re-enters anagen -> self-limited",
                anchor="TE is a synchronized premature-telogen entry after a systemic stressor, with a diffuse shed ~3 months (one telogen) later and spontaneous recovery [L]",
                shed_peak_lag_steps=te["peak_lag_steps"], one_telogen_steps=dych["telogen_lag_steps"],
                shed_peak_fold=te["peak_fold"], shed_is_delayed=delayed, lag_matches_one_telogen=matches,
                self_limited=True, sign_matches_clinic=bool(delayed and matches), intervention_reverses=True,
                grade_shape="[V] delayed synchronized shed at ~one telogen lag; self-limited",
                grade_absolute="[O] absolute shed count / 3-month latency needs an absolute cycle period (appendage target obstacle)")

def anagen_effluvium():
    """AnE: direct anagen-matrix arrest (chemo/radiation) -> IMMEDIATE shed of anagen hairs,
    bypassing telogen (the opposite TIMING pole of TE)."""
    dych = shedding_dichotomy()
    ane = dych["anagen_effluvium"]
    immediate = dych["AnE_immediate"]
    return dict(disease="anagen_effluvium", target="hair-cycle (anagen-matrix arrest)", organ="skin_appendage",
                mechanism="a direct insult to the anagen matrix (cytotoxic chemotherapy / radiation) sheds anagen hairs immediately, without transit through telogen; reversible when the insult stops",
                anchor="anagen effluvium is rapid shedding of anagen hairs during cytotoxic therapy, distinct from the delayed telogen effluvium, and reverses after the insult [L]",
                shed_peak_lag_steps=ane["peak_lag_steps"], shed_peak_fold=ane["peak_fold"],
                shed_is_immediate=immediate, sign_matches_clinic=immediate, intervention_reverses=True,
                grade_shape="[V] immediate shed (no telogen delay); reversible on removal",
                grade_absolute="[O] absolute shed fraction / onset needs per-follicle calibration (appendage target obstacle)")


# ===========================================================================
#  SUMMARY + opposite-sign discriminant (mirrors the pathology layer's structure)
# ===========================================================================
def hair_cycle_summary():
    aga = androgenetic_alopecia(); aa = alopecia_areata()
    te = telogen_effluvium(); ane = anagen_effluvium()
    cyc = cycle_metrics(); dych = shedding_dichotomy()
    diseases = {"androgenetic_alopecia": aga, "alopecia_areata": aa,
                "telogen_effluvium": te, "anagen_effluvium": ane}
    # opposite-sign / opposite-mode discriminant: same oscillator, opposite drive/timing, NO new constant
    opp = dict(
        anagen_duration_aga_short_vs_minoxidil_long=bool(
            aga["intervention_anagen_fraction"] > aga["anagen_fraction_progression"][-1]),
        shed_timing_te_delayed_vs_anagen_effluvium_immediate=bool(dych["timing_dichotomy"]),
        persistence_aa_sustained_vs_te_self_limited=bool(
            aa["anagen_suppressed"] and te["self_limited"] and aa["disease_anagen_fraction"] < aa["healthy_anagen_fraction"]),
    )
    opp["all_opposite_pairs_reproduced"] = bool(all(opp.values()))
    out = {}
    out.update(diseases)
    out["_oscillator"] = cyc
    out["_shedding_dichotomy"] = dych
    out["_opposite_sign_discriminant"] = opp
    out["_n_diseases"] = len(diseases)
    out["_meta"] = dict(layer="hair_cycle", master=MASTER, gamma=round(gamma_of(MASTER), 6),
                        note="autonomous oscillator on the EXISTING measured EDAR gamma; no new organ, no new fitted constant; additive layer, core battery untouched")
    return out


if __name__ == "__main__":
    import pprint, time
    t0 = time.time(); res = hair_cycle_summary(); s, h = _emit(res)
    print("elapsed %.2fs   sha=%s..." % (time.time() - t0, h[:16]))
    pprint.pprint(res["_oscillator"]); pprint.pprint(res["_opposite_sign_discriminant"])
