#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mechanisms.py  --  NON-RARE reproductive / gonadal-endocrine disease layer.

Per VP_FRAMEWORK_MAP s6 the split is by ETIOLOGY, not body part: this package owns the COMMON,
DYNAMICS-DEFINED disorders of the HPG axis (rare / monogenic subtypes cross-reference to disease_wp).
Each disorder is mapped to the SAME substrate the dynamics modules verified:

    ONE drive variable (sex-hormone drive h)  --  TWO failure modes  --  ONE temporal-pattern lever.

  * too little / wrong-pattern drive  -> the HPG OSCILLATOR fails  (T1/T2/T3/T5 broken) -> this file
  * barrier-lowering drive            -> the R19 ONCOGENIC switch crosses               -> _oncology
  * the cure for one is the side-effect of the other, because it is the SAME h moved opposite ways;
    the resolution is the temporal-pattern lever (pulsatile / cycling)                   -> _therapy

For every disorder we give (i) the substrate failure mode, (ii) how the current treatment reads as a
substrate move, (iii) a model-derived BETTER-treatment HYPOTHESIS. Hypotheses are FALSIFIABLE model
statements, NOT clinical advice; retrodictions of established practice are graded [V]/[L], genuinely
novel suggestions [O] with the obstacle stated. Computational checks confirm the substrate actually
shows each claimed failure mode (no hand-waving).

Uses only inherited/vp_substrate.py + the package dynamics. Deterministic.
"""
import os
for _v in ("OMP_NUM_THREADS","OPENBLAS_NUM_THREADS","MKL_NUM_THREADS","NUMEXPR_NUM_THREADS","VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"
import sys, math, json
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "inherited"))
from vp_substrate import Neuron, spinodal, settle, seed_everything

# ---------------------------------------------------------------------------------------------------
# Computational consistency checks: does the substrate actually exhibit each failure mode?
# ---------------------------------------------------------------------------------------------------

def _pulse_count(tau_s, drive, T=4000.0, dt=0.05):
    seed_everything()
    n = Neuron(gamma=1.0, tau_f=1.0, tau_s=tau_s, beta=0.5)
    S, _ = n.run(drive=drive, T=T, dt=dt, s0=0.0, w0=0.0)
    return int(len(Neuron.spikes(S))), S

def check_pcos():
    """PCOS = pulse generator stuck FAST -> LH-favouring -> no FSH-driven follicle selection / no surge.
    Substrate check: a faster generator (smaller tau_s) produces a HIGHER pulse rate (LH bias)."""
    n_fast, _ = _pulse_count(30.0, 0.35)
    n_slow, _ = _pulse_count(150.0, 0.35)
    rate_fast = n_fast / 4000.0; rate_slow = n_slow / 4000.0
    return dict(failure="GnRH pulse frequency too high -> LH:FSH balance tips to LH; follicle stalls",
                fast_tau_rate=round(rate_fast, 5), slow_tau_rate=round(rate_slow, 5),
                fast_is_LH_biased=bool(rate_fast > rate_slow), grade="[V]")

def check_fha():
    """Functional hypothalamic amenorrhoea = the GnRH pulse generator SLOWED (energy deficit / stress
    reduce pulse frequency) below the rate needed to drive ovulatory cycling. PCOS and FHA are the two
    ENDS of the SAME verified pulse-frequency axis (PCOS too fast, FHA too slow). Substrate check: a
    slowed generator (larger tau_s) gives a LOWER pulse rate than normal; reversible by restoring tone."""
    n_fha, _ = _pulse_count(200.0, 0.35)        # slowed generator (FHA)
    n_norm, _ = _pulse_count(60.0, 0.35)        # normal follicular generator
    rate_fha = n_fha / 4000.0; rate_norm = n_norm / 4000.0
    return dict(failure="GnRH pulse frequency suppressed below ovulatory threshold (generator intact)",
                fha_slow_rate=round(rate_fha, 5), normal_rate=round(rate_norm, 5),
                fha_rate_below_normal=bool(rate_fha < rate_norm),
                note="same pulse-frequency axis as PCOS, opposite end; reversible (restore energy/tone)",
                grade="[V]")

def check_menopause():
    """Menopause = ovarian RESPONDER substrate (follicle pool) exhausted. The sustained secretory (ON)
    state is a property of the bistable R19 WELL; an intact ovary LATCHES into the ON state and holds it
    when drive is withdrawn (luteal/secretory memory). Substrate depletion removes the well, so the
    latched ON state is abolished -- and, unlike FHA, it does NOT recover (the hardware is gone; in fact
    gonadotropins rise post-menopause as ovarian negative feedback is lost). Substrate check: with the
    well intact the responder holds ON at zero drive; with the well depleted it collapses toward off."""
    s_intact = settle(1.0, 0.0, s0=1.0)         # intact ovary: latched ON (sustained secretion)
    s_depleted = settle(0.05, 0.0, s0=1.0)      # follicle pool gone: no bistable latch -> collapses
    return dict(failure="follicle-pool exhaustion removes the bistable secretory latch; irreversible",
                intact_latched_on=round(float(s_intact), 4), depleted_state=round(float(s_depleted), 4),
                latch_lost_on_depletion=bool(abs(s_intact) > 0.5 and abs(s_depleted) < 0.3),
                note="REPLACEMENT (HRT), not restoration -- the secretory substrate is depleted",
                grade="[V] latch loss; [O] irreversibility (no in-package follicle regeneration)")

def check_puberty_timing():
    """Central precocious vs delayed puberty = the T5 spinodal crossing happening EARLY vs NOT YET.
    Substrate check: below the spinodal the axis is OFF (juvenile); above it the axis is ON (pulsing).
    The SAME threshold governs both -- precocious = crossed early, delayed = not yet crossed."""
    sp = spinodal(1.0)
    s_off = settle(1.0, 0.8 * sp, s0=-1.0)      # drive below spinodal -> juvenile OFF
    s_on = settle(1.0, 1.2 * sp, s0=-1.0)       # drive above spinodal -> pubertal ON
    return dict(failure="T5 threshold crossed early (precocious) or not yet (delayed) -- one spinodal",
                state_below_threshold=round(float(s_off), 4), state_above_threshold=round(float(s_on), 4),
                off_below_on_above=bool(s_off < 0 < s_on), grade="[V] mechanism; [O] chronological age")

def check_anovulation_hcg():
    """Anovulatory infertility = the mid-cycle surge switch (T3) fails to flip. The hCG trigger is an
    exogenous SPINODAL KICK that forces the flip. Substrate check: a sub-threshold oestradiol state
    stays in the low (no-surge) basin; adding an hCG-like impulse past the spinodal forces the surge."""
    sp = spinodal(1.0)
    s_stall = settle(1.0, 0.8 * sp, s0=-1.0)        # follicle mature but surge not triggered
    s_trigger = settle(1.0, 1.15 * sp, s0=-1.0)     # hCG kick across the spinodal -> surge/ovulation
    return dict(failure="LH-surge switch fails to flip (stuck in negative-feedback basin)",
                stalled_state=round(float(s_stall), 4), after_hcg_kick=round(float(s_trigger), 4),
                hcg_kick_triggers_surge=bool(s_stall < 0 < s_trigger),
                note="hCG trigger = single spinodal kick onto the ON branch", grade="[V]")

# ---------------------------------------------------------------------------------------------------
# Disease -> mechanism -> current treatment -> model-derived better-treatment hypothesis
# ---------------------------------------------------------------------------------------------------

DISORDERS = [
    dict(name="PCOS (anovulatory phenotype)", target="T1+T3",
         mechanism="GnRH pulse generator runs too FAST -> chronic LH excess, low FSH -> follicles "
                   "recruited but none selected, no dominant follicle, no surge (chronic anovulation)",
         current="OCP masks symptoms; letrozole/clomiphene raise FSH drive; metformin (insulin); "
                 "in VP terms: push the LH:FSH balance back toward FSH",
         better_hypothesis="restore the SLOW pulse pattern itself -- low-frequency PULSATILE GnRH "
                           "(not continuous, not fast) to re-establish the FSH-favouring rhythm and "
                           "physiological follicle selection",
         grade="[O] novel pattern-restoration; FSH-raising drugs are the [L]/[V] retrodiction"),
    dict(name="Functional hypothalamic amenorrhoea (FHA)", target="T1",
         mechanism="energy deficit / stress SLOW the GnRH pulse generator below the ovulatory pulse "
                   "frequency (PCOS and FHA are opposite ends of one pulse-frequency axis); reversible",
         current="restore energy balance / reduce stress (first line, restores pulse tone); "
                 "pulsatile GnRH or gonadotropins to induce ovulation when fertility is wanted",
         better_hypothesis="pulsatile GnRH at PHYSIOLOGICAL frequency restores the generator's rate -- "
                           "the model says the missing thing is the pulse PATTERN/rate, not the molecule",
         grade="[V]/[L] retrodicts pulsatile-GnRH; energy restoration is the primary lever"),
    dict(name="Menopause / perimenopause", target="T2",
         mechanism="follicle pool (ovarian responder substrate) exhausted -> the bistable secretory "
                   "latch is lost; irreversible substrate depletion, NOT detuning",
         current="MHT/HRT REPLACES the missing output (oestrogen +/- progestin) -- symptom control",
         better_hypothesis="the model is explicit that this is REPLACEMENT, not restoration: the "
                           "oscillator hardware is gone, so the honest in-framework lever is replacement "
                           "with the cancer-risk trade-off made explicit (same h that lowers the breast "
                           "barrier) -- restoration would need follicle regeneration (out of scope)",
         grade="[O] irreversibility is the obstacle; HRT-as-replacement is [L]"),
    dict(name="Age-related male hypogonadism", target="androgen drive",
         mechanism="sustained androgen drive decays with age -> hypogonadal symptoms",
         current="testosterone replacement (TRT) restores drive",
         better_hypothesis="TRT re-supplies the SAME androgen drive that lowers the prostate R19 "
                           "barrier (trade-off). The temporal-pattern lever predicts that PULSATILE or "
                           "cycled delivery might separate the wanted androgenic tone from the unwanted "
                           "sustained proliferative drive",
         grade="[O] novel; the trade-off itself is the [V] structural prediction"),
    dict(name="Central precocious puberty", target="T5",
         mechanism="the GnRH axis crosses the T5 spinodal too EARLY -> premature pulsatile reactivation",
         current="continuous (depot) GnRH agonist suppresses the axis by desensitisation",
         better_hypothesis="retrodiction: continuous GnRH agonist = depolarisation block of the "
                           "generator (same mechanism the therapy module shows) -> axis switched OFF; "
                           "the standard of care is exactly the substrate-predicted move",
         grade="[V] retrodiction (continuous = suppression)"),
    dict(name="Delayed puberty (functional / constitutional)", target="T5",
         mechanism="drive has not yet crossed the T5 spinodal -> axis still OFF",
         current="low-dose sex steroids or pulsatile GnRH / gonadotropins to push across threshold",
         better_hypothesis="supply drive to cross the spinodal; pulsatile GnRH drives the generator "
                           "(activation pattern) where continuous would block it",
         grade="[V] retrodiction (pulsatile = activation)"),
    dict(name="Anovulatory infertility (surge failure)", target="T2+T3",
         mechanism="the mid-cycle LH-surge switch fails to flip -> no ovulation",
         current="clomiphene/letrozole block negative feedback (raise FSH drive); gonadotropins + hCG "
                 "trigger, where hCG is the ovulation trigger",
         better_hypothesis="retrodiction: the hCG trigger is a single SPINODAL KICK forcing the surge "
                           "switch onto the ON branch -- the model identifies why a one-shot trigger "
                           "(not sustained drive) is the right move at that moment",
         grade="[V]/[L] retrodicts the hCG trigger as a spinodal kick"),
    dict(name="Endometriosis (oestrogen-dependent)", target="oncogenic-analogue drive",
         mechanism="oestrogen-driven ECTOPIC proliferation -- SAME drive variable as breast carcinoma, "
                   "benign but in the wrong location (one drive, different outcome)",
         current="continuous GnRH agonist / progestins suppress oestrogen drive; surgery for lesions",
         better_hypothesis="suppression is the goal here, so the model says CONTINUOUS (block) is "
                           "correct and warns that a cycling/pulsatile schedule would RE-stimulate -- "
                           "the same lever, read in the opposite direction from the cancer case",
         grade="[V] retrodiction (continuous suppression is correct for a suppression goal)"),
]

def run_disease():
    checks = dict(
        pcos=check_pcos(),
        fha=check_fha(),
        menopause=check_menopause(),
        puberty_timing=check_puberty_timing(),
        anovulation_hcg=check_anovulation_hcg(),
    )
    passed_checks = dict(
        pcos=checks["pcos"]["fast_is_LH_biased"],
        fha=checks["fha"]["fha_rate_below_normal"],
        menopause=checks["menopause"]["latch_lost_on_depletion"],
        puberty=checks["puberty_timing"]["off_below_on_above"],
        anovulation=checks["anovulation_hcg"]["hcg_kick_triggers_surge"],
    )
    passed = all(passed_checks.values())
    return dict(thesis="one sex-hormone drive; two failure modes (oscillator vs oncogenic switch); "
                       "one temporal-pattern lever (pulsatile/cycling)",
                substrate_checks=checks, checks_pass=passed_checks,
                disorders=DISORDERS, status=("PASS" if passed else "FAIL"),
                grades="mechanisms [V]; retrodictions [V]/[L]; novel hypotheses [O] (clinical validation needed)")

def status():
    return run_disease()

if __name__ == "__main__":
    print(json.dumps(run_disease(), ensure_ascii=False, indent=2))
