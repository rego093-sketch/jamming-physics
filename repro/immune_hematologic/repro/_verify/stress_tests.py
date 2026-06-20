#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stress_tests.py  --  Immune / Hematologic STRESS BATTERY (wired). Very high bar: each target swept WIDE,
no per-target tuning, failures honest, [O]+obstacle acceptable, silent pass not. Writing stays LOCKED
until run_battery() is all PASS and gates.write_research_complete() is called.

Wires the real research modules:
    T1/T2/T4  repro/_dynamics/clonal_inflammation.py     (run)
    T3        repro/_dynamics/lineage_order.py            (run)
    T5        repro/_oncology/carcinogen_dose_response.py (oncology_report)
    THERAPY   repro/_therapy/fundamental_therapy.py       (therapy_report)  -- 4 fundamental levers
Every target's status is derived from the module's own all_pass; nothing is hand-set.
"""
import os, sys, json
_HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, os.path.join(_HERE, "..", "_dynamics"))
sys.path.insert(0, os.path.join(_HERE, "..", "_oncology"))
sys.path.insert(0, os.path.join(_HERE, "..", "_therapy"))
import importlib
eng     = importlib.import_module("vp_imm_engine")
clonal  = importlib.import_module("clonal_inflammation")
lineage = importlib.import_module("lineage_order")
onc     = importlib.import_module("carcinogen_dose_response")
therapy = importlib.import_module("fundamental_therapy")
emg_lin = importlib.import_module("emergent_lineage")        # T6: emergent developmental order (sim)
emg_kra = importlib.import_module("emergent_kramers")        # T7: emergent carcinogenesis (sim)
emg_mem = importlib.import_module("emergent_memory")         # T8: emergent memory lifetime (sim)
emg_chr = importlib.import_module("emergent_chronicity")     # T9: emergent acute/chronic boundary (sim)
emg_sea = importlib.import_module("emergent_seam")           # T10: emergent surveillance seam (sim)
emg_sel = importlib.import_module("emergent_selection")      # T11: emergent clonal-selection threshold (sim)
emg_cmp = importlib.import_module("emergent_competition")    # T12: emergent immunodominance / clonal competition (sim)
emg_thr = importlib.import_module("emergent_therapy")        # T13: emergent therapy trajectories (Levers A & C) (sim)
emg_bar = importlib.import_module("emergent_barrier_restoration")    # T14: emergent Lever B barrier restoration (sim)
emg_clr = importlib.import_module("emergent_surveillance_clearance") # T15: emergent Lever D surveillance clearance (sim)
emg_rep = importlib.import_module("emergent_repertoire")            # T16: emergent N-clone repertoire dominance (sim)
emg_reg = importlib.import_module("emergent_regrowth")             # T17: emergent cytotoxic relapse regrowth (sim)
emg_mat = importlib.import_module("emergent_maturation")          # T18: emergent affinity maturation / germinal-center loop (sim)
emg_cmb = importlib.import_module("emergent_combination")         # T19: emergent combination-therapy relapse->cure conversion (sim)
emg_xr  = importlib.import_module("emergent_crossreactivity")     # T20: emergent original-antigenic-sin / imprinting (sim)
emg_neg = importlib.import_module("emergent_negative_selection")  # T21: emergent central tolerance / clonal deletion (sim)
emg_pb  = importlib.import_module("emergent_prime_boost")         # T22: emergent prime-boost scheduling (sim)
emg_aut = importlib.import_module("emergent_autoimmunity")        # T23: emergent autoimmune tolerance break (sim)
emg_per = importlib.import_module("emergent_peripheral_tolerance") # T24: emergent peripheral tolerance / regulatory suppression (sim)
emg_exh = importlib.import_module("emergent_exhaustion")          # T25: emergent immune exhaustion / chronic-antigen hyporesponsiveness (sim)
emg_hor = importlib.import_module("emergent_hormesis")            # T26: emergent tolerance-immunity dose window (sim)
emg_ret = importlib.import_module("emergent_retolerization")      # T27: emergent therapeutic re-tolerization (sim)
emg_spr = importlib.import_module("emergent_spreading")           # T28: emergent epitope spreading (sim)
emg_sen = importlib.import_module("emergent_sensitization")       # T29: emergent allergic sensitization / desensitization (sim)
emg_rec = importlib.import_module("emergent_reconstitution")      # T30: emergent immunodeficiency reconstitution threshold (sim)
emg_sep = importlib.import_module("emergent_sepsis_latch")        # T31: emergent systemic inflammatory latch / break window (sim)
emg_alo = importlib.import_module("emergent_allotolerance")       # T32: emergent transplant allo-tolerance induction (sim)
emg_cyt = importlib.import_module("emergent_cytopenia")           # T33: emergent lineage-targeted autoimmune cytopenia (sim)
emg_isn = importlib.import_module("emergent_immunosenescence")    # T34: emergent thymic involution / immunosenescence (sim)
emg_dbr = importlib.import_module("emergent_durable_boost")       # T35: emergent durability-optimal re-boosting (sim)


def _gammas_from_engine(base):
    """Build {organ: gamma} for the 4 MEASURED organs off the emergence output."""
    return {o["organ"]: o["gamma"] for o in base["organs"]["organs"] if o.get("gamma") is not None}


_BATTERY_CACHE = None

def run_battery():
    # the battery is pure + deterministic; cache per-process so callers (run_all + research_gate) don't
    # re-run the stochastic T6/T7 simulations twice in one invocation.
    global _BATTERY_CACHE
    if _BATTERY_CACHE is not None:
        return _BATTERY_CACHE
    base = eng.circulate()
    G = _gammas_from_engine(base)

    cl   = clonal.run(G)                 # T1, T2, T4
    ln   = lineage.run(G)                # T3
    orep = onc.oncology_report(G)        # T5 (+ AML/lymphoma dose-response)
    trep = therapy.therapy_report(G)     # fundamental levers A/B/C/D + cytotoxic contrast
    el   = emg_lin.run(G)                # T6 emergent developmental order (shared-drive race)
    ek   = emg_kra.run(G)                # T7 emergent carcinogenesis (stochastic barrier crossing)
    em   = emg_mem.run(G)                # T8 emergent memory lifetime (stochastic ON->OFF escape)
    ec   = emg_chr.run(G)                # T9 emergent acute/chronic boundary (stochastic pulses)
    es   = emg_sea.run(G)                # T10 emergent surveillance seam (coupled influx-clearance)
    esel = emg_sel.run(G)                # T11 emergent clonal-selection threshold (rising-affinity ramp)
    ecmp = emg_cmp.run(G)                # T12 emergent immunodominance (coupled shared-antigen competition)
    ethr = emg_thr.run(G)                # T13 emergent therapy trajectories (Levers A & C basin-occupancy)
    ebar = emg_bar.run(G)                # T14 emergent Lever B barrier restoration (crossing-rate vs restored barrier)
    eclr = emg_clr.run(G)                # T15 emergent Lever D surveillance clearance (time-domain reservoir decay)
    erep = emg_rep.run(G)                # T16 emergent N-clone repertoire dominance (coupled competition)
    ereg = emg_reg.run(G)                # T17 emergent cytotoxic relapse regrowth (basin-gated population layer)
    emat = emg_mat.run(G)                # T18 emergent affinity maturation (iterated mutation+selection germinal-center loop)
    ecmb = emg_cmb.run(G)                # T19 emergent combination therapy (cull + basin-acting lever -> cure conversion)
    exr  = emg_xr.run(G)                 # T20 emergent original-antigenic-sin (memory-vs-naive recall imprinting)
    eneg = emg_neg.run(G)                # T21 emergent central tolerance / clonal deletion (negative-selection ramp)
    epb  = emg_pb.run(G)                 # T22 emergent prime-boost scheduling (fixed-length campaign, antigen depot)
    eaut = emg_aut.run(G)                # T23 emergent autoimmune tolerance break (escaped-clone bistable latch)
    eper = emg_per.run(G)                # T24 emergent peripheral tolerance (subtractive regulatory suppressor field)
    eexh = emg_exh.run(G)                # T25 emergent immune exhaustion (accumulating antigen-gated negative feedback)
    ehor = emg_hor.run(G)                # T26 emergent tolerance-immunity dose window (T21 deletion x T23 break over a dose sweep)
    eret = emg_ret.run(G)                # T27 emergent therapeutic re-tolerization (latched autoreactive clone re-flipped across the negative saddle-node)
    espr = emg_spr.run(G)                # T28 emergent epitope spreading (count-coupled clone cascade past a recruitment threshold)
    esen = emg_sen.run(G)                # T29 emergent allergic sensitization / desensitization (priming-vs-tolerance accumulators on an R19 effector)
    erec = emg_rec.run(G)                # T30 emergent immunodeficiency reconstitution (coverage collapse + threshold-gated reconstitution)
    esep = emg_sep.run(G)                # T31 emergent systemic inflammatory latch (cytokine-tone field + time-critical break window)
    ealo = emg_alo.run(G)                # T32 emergent transplant allo-tolerance induction (T27 at a larger, time-deepening allo-load + induction window)
    ecyt = emg_cyt.run(G)                # T33 emergent lineage-targeted autoimmune cytopenia (T23 break attacking a produced lineage; T27 restores; T19 combination)
    eisn = emg_isn.run(G)                # T34 emergent thymic involution / immunosenescence (T21 thymic education run over a slowly shrinking window)
    edbr = emg_dbr.run(G)                # T35 emergent durability-optimal re-boosting (T8 decay curve under a fixed boost budget over a finite horizon)

    def st(passed): return "PASS" if passed else "FAIL"

    suites = [
        dict(target="T1", description="affinity drive past spinodal flips the cell ON (clonal selection = saddle-node) [V]",
             status=st(cl["T1"]["all_pass"]), value=cl["T1"]["all_pass"], grade=cl["T1"]["grade"], obstacle_if_open=None),
        dict(target="T2", description="acute (sub-spinodal) resolves, chronic (supra-spinodal) latches [V]",
             status=st(cl["T2"]["all_pass"]), value=cl["T2"]["all_pass"], grade=cl["T2"]["grade"], obstacle_if_open=None),
        dict(target="T3", description="developmental lineage order is a gamma readout; endpoints sign-validated vs embryology [V]/[L]",
             status=st(ln["T3"]["all_pass"]), value=ln["T3"]["all_pass"], grade=ln["T3"]["grade"],
             obstacle_if_open="middle pair (spleen<->thymus) not independently anchored -> [O]"),
        dict(target="T4", description="memory persists after antigen clears; erase-drive = spinodal; stability ranks by barrier [V]",
             status=st(cl["T4"]["all_pass"]), value=cl["T4"]["all_pass"], grade=cl["T4"]["grade"], obstacle_if_open=None),
        dict(target="T5", description="immune_escape_factor scales tumor net burden in the shared kernel (cross-cutting) [V]",
             status=st(orep["T5"]["all_pass"]), value=orep["T5"]["all_pass"], grade=orep["T5"]["grade"],
             obstacle_if_open="absolute incidence uncalibrated (kT, rate0) -> [O]"),
        dict(target="THERAPY", description="four fundamental levers (re-flip / barrier / drive-removal / surveillance) "
                                           "+ cytotoxic relapse contrast, all derived from the R19 kernel [V]/[L]",
             status=st(trep["all_pass"]), value=trep["all_pass"], grade="[V] mechanisms / [L] clinical anchors",
             obstacle_if_open="molecule/dose/patient-response calibration outside the substrate -> [O]"),
        dict(target="T6", description="developmental order EMERGES from a shared-drive race (organs commit in spinodal "
                                      "order; commit-h spacing = spinodal spacing); earliest endpoint + gap-ordered "
                                      "robustness [V] (simulation-measured)",
             status=st(el["T6"]["all_pass"]), value=el["T6"]["all_pass"], grade=el["T6"]["grade"],
             obstacle_if_open="spleen<->thymus middle pair: smallest spinodal gap ~ emergence jitter, washes out -> [O] (quantified)"),
        dict(target="T7", description="carcinogen dose-response (convex super-linear) and the Kramers rate law itself "
                                      "EMERGE from direct stochastic barrier-crossing simulation [V] (measured, not assumed)",
             status=st(ek["T7"]["all_pass"]), value=ek["T7"]["all_pass"], grade=ek["T7"]["grade"],
             obstacle_if_open="absolute steepness / cellular-noise scale D uncalibrated -> [O]"),
        dict(target="T8", description="immune-memory lifetime EMERGES from a stochastic ON->OFF escape simulation: "
                                      "measured mean first-passage time ranks ascending γ + Kramers law (log-rate linear "
                                      "in barrier, slope recovers -1/D) [V] (measured, not asserted from γ²/4)",
             status=st(em["T8"]["all_pass"]), value=em["T8"]["all_pass"], grade=em["T8"]["grade"],
             obstacle_if_open="absolute lifetime / cellular-noise scale D uncalibrated -> [O]"),
        dict(target="T9", description="the acute/chronic boundary EMERGES in the (insult amplitude × duration) plane "
                                      "from stochastic pulse simulation: critical amplitude = each organ's spinodal, "
                                      "sub-spinodal never chronic, monotone dose×time tradeoff [V] (measured)",
             status=st(ec["T9"]["all_pass"]), value=ec["T9"]["all_pass"], grade=ec["T9"]["grade"],
             obstacle_if_open="absolute noise scale D (transition sharpness / exact d_crit) uncalibrated -> [O]"),
        dict(target="T10", description="the immunosurveillance seam EMERGES from a coupled stochastic influx(R19-crossing)"
                                       "-clearance model: measured burden is monotone in escape and, rescaled by influx, "
                                       "collapses onto the SAME 1/(1−escape) curve at both sites [V] (common multiplier, measured)",
             status=st(es["T10"]["all_pass"]), value=es["T10"]["all_pass"], grade=es["T10"]["grade"],
             obstacle_if_open="absolute burden scale (population constant K, clearance scale μ0) uncalibrated -> [O]"),
        dict(target="T11", description="clonal-selection activation EMERGES from a stochastic rising-affinity simulation: "
                                       "the measured commit-drive equals each organ's spinodal (from below, by thermal "
                                       "activation), orders by γ, and sub-spinodal stays tolerant while supra-spinodal "
                                       "commits [V] (measured, not asserted from the closed-form spinodal)",
             status=st(esel["T11"]["all_pass"]), value=esel["T11"]["all_pass"], grade=esel["T11"]["grade"],
             obstacle_if_open="absolute noise scale D (sub-spinodal deficit / transition sharpness) uncalibrated -> [O]"),
        dict(target="T12", description="immunodominance EMERGES from a coupled stochastic shared-antigen competition: the "
                                       "higher-affinity clone commits first and depletes the pool, competitively excluding "
                                       "a subdominant clone (P≈1 alone); dominance sharpens monotonically with the affinity "
                                       "gap and is symmetric at zero gap [V] (measured)",
             status=st(ecmp["T12"]["all_pass"]), value=ecmp["T12"]["all_pass"], grade=ecmp["T12"]["grade"],
             obstacle_if_open="absolute hierarchy depth (consumption rate, pool size, noise scale D) uncalibrated -> [O]"),
        dict(target="T13", description="fundamental-therapy Levers A (differentiation re-flip) & C (drive removal) EMERGE as "
                                       "measured stochastic basin-occupancy trajectories: re-flip threshold = spinodal (no "
                                       "cytotoxicity), drive removal is preventive-not-curative, and differentiation empties "
                                       "the malignant basin while drive-removal/cytotoxic leaves it occupied (relapse) [V] (measured)",
             status=st(ethr["T13"]["all_pass"]), value=ethr["T13"]["all_pass"], grade=ethr["T13"]["grade"],
             obstacle_if_open="absolute agent dose/schedule (clinical) and noise scale D uncalibrated -> [O]"),
        dict(target="T14", description="fundamental-therapy Lever B (barrier restoration) EMERGES as a measured crossing-rate-"
                                       "vs-restored-barrier trajectory: as the carcinogen-eroded barrier is stepped back up, "
                                       "the counted malignant crossing rate collapses monotonically (large multiplicative drop) "
                                       "and log-rate is linear in the restored barrier (Kramers law emerges in the therapeutic "
                                       "direction, slope recovers -1/D) [V] (measured, not asserted from the closed form)",
             status=st(ebar["T14"]["all_pass"]), value=ebar["T14"]["all_pass"], grade=ebar["T14"]["grade"],
             obstacle_if_open="absolute multiplicative factor / cellular-noise scale D uncalibrated -> [O]"),
        dict(target="T15", description="fundamental-therapy Lever D (surveillance restoration) EMERGES as a measured time-domain "
                                       "reservoir-clearance trajectory: after surveillance is restored the counted committed "
                                       "reservoir decays monotonically toward a floor that falls with deeper surveillance "
                                       "(floor x surveillance ~ const -> floor ~ 1/(1-escape), the T10 seam recovered as an "
                                       "endpoint, site-independent when rescaled by influx) and clears faster the deeper the "
                                       "surveillance [V] (measured, not read off the steady formula)",
             status=st(eclr["T15"]["all_pass"]), value=eclr["T15"]["all_pass"], grade=eclr["T15"]["grade"],
             obstacle_if_open="absolute reservoir scale / clearance rate (K, mu0, noise scale D) uncalibrated -> [O]"),
        dict(target="T16", description="repertoire-level immunodominance EMERGES from a coupled stochastic competition of N "
                                       "clones for one shared antigen pool: the response concentrates on a few high-affinity "
                                       "clones (measured participation ratio N_eff << N, commit probability monotone in affinity "
                                       "rank), the concentration sharpens with the affinity spread and, relative to N, with "
                                       "repertoire size, and is symmetric at zero spread [V] (measured)",
             status=st(erep["T16"]["all_pass"]), value=erep["T16"]["all_pass"], grade=erep["T16"]["grade"],
             obstacle_if_open="absolute hierarchy depth (consumption rate, pool size, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T17", description="the cytotoxic relapse failure mode EMERGES as a measured regrowth time-course of a "
                                       "basin-gated population layer: cytotoxic killing leaves the malignant basin intact so the "
                                       "malignant fraction regrows toward carrying capacity (>=90% K, relapse) while a "
                                       "differentiating re-flip empties the basin so it decays to ~0 (<=10% K, cure), and a "
                                       "deeper kill only lengthens the delay while every depth fully recovers -> relapse is "
                                       "basin-determined, not kill-depth-determined [V] (measured)",
             status=st(ereg["T17"]["all_pass"]), value=ereg["T17"]["all_pass"], grade=ereg["T17"]["grade"],
             obstacle_if_open="absolute growth rate / conversion rate / clinical schedule uncalibrated -> [O]"),
        dict(target="T18", description="affinity maturation EMERGES from an iterated germinal-center loop wrapped around the "
                                       "coupled clonal competition: each round the higher-affinity clones commit first and "
                                       "deplete the shared pool (excluding slow clones), the committed parents are reseeded "
                                       "with symmetric somatic hypermutation, and the measured mean affinity of the responding "
                                       "set rises round over round; the rise needs mutation (zero mutation stalls), speeds up "
                                       "with mutation rate, needs competition (an unlimited pool gives no gain), and pool "
                                       "pressure strengthens maturation out of the weak regime with an honest intermediate "
                                       "optimum [V] (measured)",
             status=st(emat["T18"]["all_pass"]), value=emat["T18"]["all_pass"], grade=emat["T18"]["grade"],
             obstacle_if_open="absolute maturation rate (mutation scale, pool pressure, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T19", description="the combination-therapy advantage EMERGES as a measured regrowth contrast: a cytotoxic "
                                       "cull alone leaves the malignant basin occupied so the fraction regrows (relapse) while "
                                       "adding a basin-acting lever (differentiation re-flip OR restored surveillance) converts "
                                       "the same relapse curve into a cure curve; the cull does not change the destination but "
                                       "accelerates the approach (lower AUC), cull-alone is insufficient at every depth, and the "
                                       "surveillance channel reproduces the exact interior fixed point N*=K(1-mu/r) -> cure is "
                                       "basin-acting, not kill-driven [V] (measured)",
             status=st(ecmb["T19"]["all_pass"]), value=ecmb["T19"]["all_pass"], grade=ecmb["T19"]["grade"],
             obstacle_if_open="absolute rates / clinical dosing schedule (kill rate, conversion rate, surveillance depth) uncalibrated -> [O]"),
        dict(target="T20", description="original antigenic sin (imprinting) EMERGES from a coupled stochastic memory-vs-naive "
                                       "competition for one shared antigen pool: at intermediate antigenic distance the "
                                       "experienced memory clone is preferentially recalled even though the naive clone is "
                                       "strictly better-matched (measured P(memory)>1/2 -- the recall head-start commits first "
                                       "and excludes the better naive clone), the bias decays monotonically with antigenic "
                                       "distance until the better-matched naive clone wins, and removing the head-start abolishes "
                                       "the bias entirely (experience-driven, not affinity-driven) [V] (measured)",
             status=st(exr["T20"]["all_pass"]), value=exr["T20"]["all_pass"], grade=exr["T20"]["grade"],
             obstacle_if_open="absolute imprinting magnitude (recall head-start, degradation slope, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T21", description="central tolerance / clonal deletion EMERGES as the mirror of clonal selection: a "
                                       "self-reactive clone driven above the spinodal in the thymic context is DELETED, not "
                                       "activated (measured deletion threshold = the organ's spinodal via a quasi-static drive "
                                       "ramp, ordering by gamma across organs), the exported repertoire's self-affinity is capped "
                                       "at the spinodal (a central-tolerance ceiling), and turning the deletion channel off lets "
                                       "autoreactive clones leak into the export -- deletion required, measured not assumed [V]",
             status=st(eneg["T21"]["all_pass"]), value=eneg["T21"]["all_pass"], grade=eneg["T21"]["grade"],
             obstacle_if_open="absolute deletion rate and the width of the escaped near-threshold fraction (cellular-noise scale D, education window) uncalibrated -> [O]"),
        dict(target="T22", description="prime-boost scheduling EMERGES from the T18 maturation loop run as a fixed-length "
                                       "vaccination campaign with a slowly clearing antigen depot: the measured matured-affinity "
                                       "gain is an inverted-U in the boost interval with an INTERIOR optimum (too-frequent boosts "
                                       "over-supply the depot into T18's weak/large-pool regime and starve selection, too-spaced "
                                       "boosts under-use the fixed campaign), and clamping the depot cap to the productive pool "
                                       "removes the over-supply penalty and moves the optimum to the most-frequent boundary -- "
                                       "measured not assumed [V]",
             status=st(epb["T22"]["all_pass"]), value=epb["T22"]["all_pass"], grade=epb["T22"]["grade"],
             obstacle_if_open="absolute optimal interval / timing (depot clearance, boost dose / carrying cap, campaign length, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T23", description="autoimmune tolerance break EMERGES by combining the T9 inflammatory latch with a T21 "
                                       "escaped self-clone (sub-spinodal residual self-drive, so bistable): an inflammatory insult "
                                       "breaks tolerance past a saddle-node boundary (measured total drive = spinodal across a "
                                       "residual-drive sweep, self-antigen and inflammation interchangeable), the break is "
                                       "irreversible -- it latches ON and persists after the insult clears (the pathological mirror "
                                       "of immune memory) with a dose×time tradeoff, and the critical insult falls as the residual "
                                       "self-drive nears the deletion threshold, so deeper central tolerance (T21) lowers "
                                       "susceptibility -- measured not assumed [V]",
             status=st(eaut["T23"]["all_pass"]), value=eaut["T23"]["all_pass"], grade=eaut["T23"]["grade"],
             obstacle_if_open="absolute break rate / boundary timing (residual-drive depth, insult amplitude / duration, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T24", description="peripheral tolerance / regulatory suppression EMERGES as a subtractive suppressor "
                                       "field on an escaped (T23) self-clone: the suppression at which the clone is re-contained "
                                       "is the saddle-node COMPLEMENT (measured σ_crit = (residual + insult) − spinodal, organ by "
                                       "organ -- the regulatory field cancels exactly the total-drive overshoot of the switch), the "
                                       "required suppression rises one-for-one (slope ≈ 1) with the escaped residual so central "
                                       "deletion (T21) and peripheral suppression ADD, and suppression is required (σ=0 breaks, "
                                       "sufficient σ contains) -- measured not assumed [V]",
             status=st(eper["T24"]["all_pass"]), value=eper["T24"]["all_pass"], grade=eper["T24"]["grade"],
             obstacle_if_open="absolute suppression strength (σ->regulatory-cell mapping), escaped-sliver width, cellular-noise scale D uncalibrated -> [O]"),
        dict(target="T25", description="immune exhaustion EMERGES as an accumulating, antigen-gated negative-feedback variable on "
                                       "a committed R19 repertoire (the dynamical mirror of T18 maturation): under chronic antigen the "
                                       "responding fraction rises then collapses to a hyporesponsive floor (measured peak->floor, "
                                       "monotone), the collapse REQUIRES the feedback (κ=0 holds the response up), it is REVERSIBLE -- "
                                       "antigen withdrawal lets the feedback decay so a re-challenge recovers the response while "
                                       "continued stimulation stays extinguished (functional silencing, not deletion) -- and its onset "
                                       "is the switch's NEGATIVE saddle-node (exhausted fraction monotone in the coupling, crossing near "
                                       "sp·(aff_mean·drive+1)) -- measured not assumed [V]",
             status=st(eexh["T25"]["all_pass"]), value=eexh["T25"]["all_pass"], grade=eexh["T25"]["grade"],
             obstacle_if_open="absolute exhaustion rate / timing (accumulation time τ_up, coupling κ, cellular-noise scale D) uncalibrated -> [O]"),
        dict(target="T26", description="the tolerance-immunity dose window EMERGES by composing the T21 central-deletion process with "
                                       "the T23 escaped-clone break over a self-antigen dose sweep: the substrate gives an INTERIOR DANGER "
                                       "band (escape ∧ break) flanked by two SAFE regimes -- ignorance (low dose) and central deletion (high "
                                       "dose); the lower (break) edge = spinodal − insult so it tracks the insult one-for-one (measured slope "
                                       "−1, and d_lo + insult = spinodal, the T11/T18 commit threshold), the upper (deletion) edge is "
                                       "insult-independent (fixed by central tolerance, slope 0), the band width grows one-for-one with the "
                                       "insult (slope +1), the window COLLAPSES as the insult -> 0 (no insult, no danger band), and the window "
                                       "position tracks each organ's spinodal -- measured not assumed [V]",
             status=st(ehor["T26"]["all_pass"]), value=ehor["T26"]["all_pass"], grade=ehor["T26"]["grade"],
             obstacle_if_open="absolute band edges / width (thermal lowering of the deletion edge, insult amplitude, cellular-noise scale D) uncalibrated; slopes are the clean invariants -> [O]"),
        dict(target="T27", description="therapeutic re-tolerization EMERGES as the MIRROR of the T23 break: a latched autoreactive clone is "
                                       "re-flipped across the NEGATIVE saddle-node (total pulse drive = −spinodal, suppress_crit = 1 + residual "
                                       "self-drive, invariant across a residual sweep) by a deep TRANSIENT pulse and STAYS tolerant after "
                                       "withdrawal (basin-acting, durable -- a therapeutic memory), whereas a sub-critical suppressor held "
                                       "continuously only CONTAINS the clone and RELAPSES on withdrawal; basin-acting cure is the durable class "
                                       "and drive-suppression-only is preventive-not-curative, and because central tolerance (T21) deletes the "
                                       "near-threshold clones, deeper deletion EASES re-tolerization -- measured not assumed [V]",
             status=st(eret["T27"]["all_pass"]), value=eret["T27"]["all_pass"], grade=eret["T27"]["grade"],
             obstacle_if_open="absolute suppression depth / pulse duration / population rates / cellular-noise scale D uncalibrated; the −spinodal threshold invariant (suppress_crit = 1 + residual) and the durable-vs-relapsing contrast are the clean results -> [O]"),
        dict(target="T28", description="epitope spreading EMERGES from a COUNT-coupled autoreactive clone cascade: each newly committed clone "
                                       "adds drive to its neighbours (h_i = (base + κ·n_ON − σ)·spinodal), so past a recruitment threshold κ_crit "
                                       "a single seeded clone triggers a SELF-AMPLIFYING cascade that recruits the repertoire (the "
                                       "determinant-spreading that broadens an autoimmune response from one epitope to many), while below κ_crit "
                                       "the seed stays contained and no cascade forms -- a measured recruitment threshold and cascade [V]",
             status=st(espr["T28"]["all_pass"]), value=espr["T28"]["all_pass"], grade=espr["T28"]["grade"],
             obstacle_if_open="absolute inter-clone coupling κ / suppressor σ / clone count / cellular-noise scale D uncalibrated; the recruitment-threshold cascade structure is the clean result -> [O]"),
        dict(target="T29", description="allergic sensitization + controlled DESENSITIZATION EMERGE from an R19 effector under an antigen-exposure "
                                       "protocol with competing priming (∝ d², superlinear) and tolerance (∝ d, linear) accumulators: a SINGLE "
                                       "exposure commits only past the spinodal but a sub-threshold supra-crossover dose REPEATED accumulates "
                                       "priming and sensitizes after a measured N_crit that FALLS with dose (allergy = failure of the T26 ignorance "
                                       "regime) and LATCHES, a controlled below-crossover protocol accumulates tolerance that RAISES the challenge "
                                       "threshold (the T27 re-tolerization reached through the exposure axis, threshold-raise growing with protocol "
                                       "length), and the controlled window is REAL -- an over-aggressive protocol SENSITIZES instead -- measured not "
                                       "assumed [V]",
             status=st(esen["T29"]["all_pass"]), value=esen["T29"]["all_pass"], grade=esen["T29"]["grade"],
             obstacle_if_open="absolute dose units / crossover dose / number of exposures (priming gain a, tolerance gain b, decay, cellular-noise scale D) uncalibrated; the threshold-at-spinodal + dose×repetition + controlled-desensitization structure is the clean result -> [O]"),
        dict(target="T30", description="acquired-immunodeficiency reconstitution EMERGES by composing the T15 surveillance floor with the T16 "
                                       "coverage and the T5/T10 tumor layer on a SINGLE surveillance-strength lever sv: below a coverage threshold "
                                       "broad protection COLLAPSES (pathogen burden ∝ 1/sv) and a tumor escapes on the SAME lever (one lever, two "
                                       "diseases), and reconstitution is THRESHOLD-GATED -- restoring sv past a critical r_crit re-establishes "
                                       "coverage and CLEARS the burden while sub-threshold restoration fails -- with r_crit scaling with the DEPTH of "
                                       "the deficit -- measured not assumed [V]",
             status=st(erec["T30"]["all_pass"]), value=erec["T30"]["all_pass"], grade=erec["T30"]["grade"],
             obstacle_if_open="absolute surveillance units / immigration & death rates / reconstitution threshold / cellular-noise scale D uncalibrated; the coverage-collapse + threshold-gated reconstitution + one-lever-two-diseases structure is the clean result -> [O]"),
        dict(target="T31", description="the systemic inflammatory latch EMERGES from a cytokine-tone field coupling many responders "
                                       "(dM = (α·frac_ON − M/τ)dt, h_i = a_ext·spinodal + M − counter·spinodal): past a critical insult the "
                                       "population SELF-SUSTAINS after the external trigger is REMOVED (the cytokine feed-forward holds itself ON -- "
                                       "the cytokine-storm latch, a_crit near the spinodal), so removing the trigger ALONE is insufficient, and the "
                                       "break is TIME-CRITICAL -- an early counter-pulse breaks the latch but the SAME pulse applied too late fails "
                                       "(a measured intervention window, monotone in delay) -- while the α=0 (no cytokine coupling) control stays "
                                       "flat -- measured not assumed [V]",
             status=st(esep["T31"]["all_pass"]), value=esep["T31"]["all_pass"], grade=esep["T31"]["grade"],
             obstacle_if_open="absolute cytokine gain α / tone timescale τ / insult & counter amplitudes / break-window timing / cellular-noise scale D uncalibrated; the self-sustaining latch + time-critical break-window structure is the clean result -> [O]"),
        dict(target="T32", description="transplant (allo-)tolerance INDUCTION EMERGES as the T27 re-tolerization at a LARGER, time-deepening "
                                       "allo-load: the induction threshold is the NEGATIVE saddle-node shifted by the graft load (suppress_crit = "
                                       "1 + base_allo, measured per-organ and INVARIANT across an allo-load sweep -- a heavier graft needs a deeper "
                                       "induction), a deep TRANSIENT pulse yields DURABLE operational tolerance whereas continuous SUB-critical "
                                       "immunosuppression only CONTAINS rejection and REJECTS on withdrawal, and tolerance is EASIER EARLY before "
                                       "alloreactive CONSOLIDATION (measured P(tolerate) falls with delay-to-induction and suppress_crit rises -- an "
                                       "induction window); the mechanism is direction-symmetric (HvG/GvH) -- measured not assumed [V]",
             status=st(ealo["T32"]["all_pass"]), value=ealo["T32"]["all_pass"], grade=ealo["T32"]["grade"],
             obstacle_if_open="absolute allo-load / suppression depth / consolidation gain & timescale / induction-window length / cellular-noise scale D uncalibrated; the (1 + base_allo) threshold invariant + consolidation induction window are the clean results -> [O]"),
        dict(target="T33", description="lineage-targeted autoimmune CYTOPENIA and its basin-acting restoration EMERGE from a clone+lineage coupling: "
                                       "a latched autoreactive clone (T23) raises the clearance of a PRODUCED lineage so the output COLLAPSES to a "
                                       "cytopenic floor -- gated by the +spinodal break (a sub-spinodal insult leaves the output healthy, a "
                                       "supra-spinodal one collapses it); a deep TRANSIENT re-tolerization (T27) restores the output DURABLY whereas "
                                       "a sub-critical suppressor only contains it and RE-COLLAPSES on withdrawal; lineage SUPPORT alone is "
                                       "insufficient (the ongoing attack clears the supported output) while the COMBINATION reaches the SAME healthy "
                                       "destination FASTER (T19 -- the cure sets the destination, support sets the rate) -- measured not assumed [V]",
             status=st(ecyt["T33"]["all_pass"]), value=ecyt["T33"]["all_pass"], grade=ecyt["T33"]["grade"],
             obstacle_if_open="absolute counts / clearance rates / recovery times (production & clearance scales, support boost, cellular-noise scale D) uncalibrated; the break-gated collapse + durable-vs-relapsing restoration + combination structure are the clean results -> [O]"),
        dict(target="T34", description="thymic involution / IMMUNOSENESCENCE EMERGES from the T21 thymic-education run repeated over a SLOWLY "
                                       "SHRINKING education window: positive selection (survival, a cumulative-engagement quota) and negative "
                                       "selection (deletion, an ON-crossing) are BOTH time-costed crossings of the one R19 field, so a shorter "
                                       "(older) window truncates them in OPPOSITE directions -- near-threshold supra-spinodal clones miss deletion "
                                       "so the escaped-autoreactive fraction RISES while marginal clones miss the engagement quota and die by "
                                       "neglect so the healthy naive-export rate FALLS; the two outputs DIVERGE (ageing repertoire drift), the "
                                       "youngest window is clean and productive (control), and the escapees are near-threshold (T21's escaped "
                                       "sliver widened by age) -- measured not assumed [V]",
             status=st(eisn["T34"]["all_pass"]), value=eisn["T34"]["all_pass"], grade=eisn["T34"]["grade"],
             obstacle_if_open="absolute education-window length in real units / positive-selection engagement quota tau_pos / signalling threshold s_pos / cellular-noise scale D uncalibrated; the escape-rises + naive-export-falls divergence, the young-clean control, and the near-threshold concentration are the clean results -> [O]"),
        dict(target="T35", description="a durability-optimal RE-BOOSTING interval EMERGES from the MEASURED memory-decay curve (the SAME R19 "
                                       "ON-basin escape as T8) under a FIXED booster budget over a finite protection horizon: the protected "
                                       "fraction of the horizon is an INTERIOR-peaked (inverted-U) function of the re-boost interval, maximised "
                                       "when the interval equals the MEASURED protection half-life t_theta (re-boost as protection wanes); boosting "
                                       "TOO FREQUENTLY exhausts the fixed budget early and leaves the late horizon unprotected, boosting TOO "
                                       "SPARSELY opens susceptible gaps, and because the optimal multiple r* ~ 1 for every compartment the absolute "
                                       "optimal interval inherits the T8 durability ranking (longer-memory compartment -> longer optimal interval); "
                                       "a no-decay control is FLAT, proving the optimum is decay-driven; distinct from T22's affinity-maturation "
                                       "optimum -- measured not assumed [V]",
             status=st(edbr["T35"]["all_pass"]), value=edbr["T35"]["all_pass"], grade=edbr["T35"]["grade"],
             obstacle_if_open="absolute re-boost interval / protection half-life in real time units / protection threshold theta / cellular-noise scale D uncalibrated; the interior inverted-U, the optimum-at-measured-half-life, the two failure modes, the cross-organ durability tracking, and the decay-driven (flat no-decay) control are the clean results -> [O]"),
    ]

    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values()) if base["oscillators"] else None),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "gammas_used": {k: round(v, 6) for k, v in sorted(G.items())},
        "suites": suites,
    }
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in suites)
    _BATTERY_CACHE = results
    return results


if __name__ == "__main__":
    r = run_battery()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
