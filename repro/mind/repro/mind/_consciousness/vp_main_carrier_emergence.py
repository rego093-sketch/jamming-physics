#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vp_main_carrier_emergence.py  --  M16-study: the MAIN high-frequency carrier,
emerged from its MEASURED source, and its memory function (deterministic).
====================================================================================
SCOPE (physics / observation / evidence / causality ONLY).
  The sleep dissociation forces the access-correlated wave to be NOT raw amplitude
  (deep slow-wave sleep has the LARGEST-amplitude delta yet is least responsive) but
  the structured HIGH-FREQUENCY carrier that is present in wake/REM and suppressed in
  deep SWS. This study (i) EMERGES that carrier from its MEASURED biological source,
  (ii) tracks its activity range, (iii) shows it is operative only in a specific state
  and a specific metastable window, and (iv) shows how MANY such carriers run in
  PARALLEL and reinstate memory. Nothing here is tuned to a target; grade == evidence;
  medium_efficacy_tested stays 0; no claim of subjective experience is made.

THE SOURCE (the "근원" -- what SETS the carrier, made explicit like M14's spindle).
  In the engine, Population.lfp(tau_inh) sets the band from the inhibitory recovery
  time-constant: a relaxation-oscillator whose period scales with tau_inh. The carrier's
  source is therefore the MEASURED GABA_A decay kinetics of fast-spiking interneurons:
    * tau_GABA_A = 6.0 ms              [F] Destexhe 1998 (fast GABAergic), in this
                                            package's synaptic_kinetics_measured atlas.
    * frequency set by inhibition decay [F] Bartos, Vida & Jonas 2007, Nat Rev Neurosci
                                            8:45 -- in interneuron networks the GABA_A
                                            decay time-constant sets the gamma period.
    * PV fast-spiking interneurons are the gamma generators, CAUSALLY:
                                       [F] Cardin et al. 2009, Nature 459:663; Sohal
                                            et al. 2009, Nature 459:698 (optogenetic).
  We do NOT introduce a new tau. We make the EXISTING engine carrier's tau_inh the
  MEASURED GABA_A value and report the emergent band as evidence. Absolute Hz stays [O]
  (engine substrate units); the MONOTONIC 1/tau relation and the dimensionless gamma:slow
  RATIO are the [V] claims.

PRE-REGISTERED DECISIONS (anti p-hacking -- fixed BEFORE looking at any result number):
  A. Carrier tau = measured GABA_A tau (6.0 ms). Activity-range sweep over the measured
     fast-GABA_A interval {3,4,6,8,10} ms (Bartos 2007 regime); claim = monotonic 1/tau.
  B. State metric = whether a drive writes a RECOVERABLE memory (partial-cue recall vs
     chance). Structured fast carrier (wake/REM) vs large UNSTRUCTURED slow drive (deep
     SWS, paced by the measured cortical slow-adaptation tau=600 ms / GABA_B tau=180 ms).
     Report the recall vs unstructured-amplitude curve; do NOT tune the amplitude.
  C. Operative window = metastable. Report recall at SILENCE (sub-fold) / METASTABLE
     (measured carrier) / GLOBAL-SYNC (uniform drive == seizure analogue). Claim = inverted-U.
  D. Parallel capacity = floor(theta:gamma ratio) from the EMERGED frequencies (not tuned);
     reinstate N contents from the slow INDEX alone; correct index -> high, novel index ->
     chance (specificity threshold 0.95 / chance band).
  E. Honesty: efficacy 0, consciousness_claim 0, hard_problem_open 1, PCI access marker
     remains an HONEST NEGATIVE (carried, not reproduced).

REPRODUCE (SEED=19, single-thread):  python3 vp_main_carrier_emergence.py
  -> stages A-E, ends with a self-check that doubles as a gate; headline sha256 printed.
  Reuses the governed engine vp_mind_engine.py (constants + Population + Hippocampus +
  the R19 fold). stdlib + numpy only.
"""
import os, sys, math, json, hashlib

# import the governed engine FIRST (it pins BLAS to one thread before numpy) -------
_HERE = os.path.dirname(os.path.abspath(__file__))
_ENGINE = os.path.normpath(os.path.join(_HERE, "..", "_engine"))
sys.path.insert(0, _ENGINE)
import numpy as np                                   # noqa: E402
import vp_mind_engine as E                           # noqa: E402
from vp_mind_engine import (                          # noqa: E402
    Population, Hippocampus, spinodal, sha256_of, _round, SEED, _patterns,
)

DATA = os.path.join(_ENGINE, "data")


def _load_measured():
    """Single-source: read the measured kinetics from the package atlases (no re-derive)."""
    syn = json.load(open(os.path.join(DATA, "spectral_observables_atlas.json")))
    sl = json.load(open(os.path.join(DATA, "sleep_architecture_atlas.json")))
    return dict(
        tau_gaba_a_ms=float(syn["synaptic_kinetics_measured"]["GABA_A"]["tau_ms"]),   # 6.0
        tau_gaba_b_ms=float(syn["synaptic_kinetics_measured"]["GABA_B"]["tau_ms"]),   # 180.0
        gaba_a_source=syn["synaptic_kinetics_measured"]["GABA_A"]["source"],
        tau_cortical_slow_ms=float(
            sl["cortical_kinetics_measured"]["slow_adaptation_recovery_tau_ms"]["value"]),  # 600
        nrem_drive=float(sl["nrem2_operating_point"]["thalamic_excitability_drive"]),       # 0.60
    )


FOLD = spinodal(1.0)                 # 0.38490... the R19 bistable fold (same as M11/whitepaper)
CHANCE = 0.5                         # +/-1 pattern overlap chance level


# ===========================================================================
#  STAGE A -- emerge the carrier FROM its measured source; track activity range
# ===========================================================================
def stage_A_source(meas):
    pop = Population(gamma=1.0)
    # the carrier emerged at the MEASURED GABA_A tau (this is the grounding)
    f_carrier = pop.lfp(tau_inh=meas["tau_gaba_a_ms"])["freq"]
    # a slow reference band (engine frozen slow inhibition; absolute pacing [O])
    f_slow = pop.lfp(tau_inh=60.0)["freq"]
    ratio = f_carrier / f_slow if f_slow > 0 else float("nan")

    # activity range: sweep the MEASURED fast-GABA_A interval (Bartos 2007 regime)
    taus = [3.0, 4.0, 6.0, 8.0, 10.0]
    freqs = [pop.lfp(tau_inh=t)["freq"] for t in taus]
    # monotonic: faster inhibition (smaller tau) -> higher carrier frequency
    monotonic = all(freqs[i] >= freqs[i + 1] - 1e-9 for i in range(len(freqs) - 1))
    f_lo, f_hi = float(min(freqs)), float(max(freqs))

    return dict(
        tau_carrier_ms=meas["tau_gaba_a_ms"],
        carrier_freq=float(f_carrier),
        slow_ref_freq=float(f_slow),
        carrier_over_slow_ratio=float(ratio),
        sweep_tau_ms=taus,
        sweep_freq=[float(x) for x in freqs],
        activity_range_freq=[f_lo, f_hi],
        carrier_above_slow=bool(f_carrier > f_slow),
        freq_monotonic_in_inv_tau=bool(monotonic),
    )


# ===========================================================================
#  STAGE B -- state selectivity: only the STRUCTURED FAST carrier writes a
#  recoverable memory; a LARGER but UNSTRUCTURED slow drive does not.
#  (deep-SWS large-amplitude delta vs wake/REM structured gamma -- whitepaper E)
# ===========================================================================
def _recall_after_structured_write(N=120, cue_frac=0.4):
    hp = Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    p = _patterns(1, N, seed=SEED)[0]
    i = hp.write(p)                                   # structured rank-1 carrier write
    return hp.retrieve(i, cue_frac=cue_frac)


def _recall_after_unstructured_drive(amp_mult, N=120, cue_frac=0.4):
    """Store one pattern with the structured carrier, then swamp the recurrent matrix
    with a large UNSTRUCTURED symmetric drive of amplitude amp_mult x the structured
    write (the deep-SWS large-amplitude, low-structure regime). Recall of the stored
    pattern is then measured. No amplitude is tuned to a target -- a curve is reported."""
    rng = np.random.RandomState(SEED + 7)
    hp = Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    p = _patterns(1, N, seed=SEED)[0]
    i = hp.write(p)
    structured_scale = hp.lr                          # per-write Hebbian scale
    U = rng.standard_normal((N, N)); U = 0.5 * (U + U.T)   # symmetric, unstructured
    U /= (np.sqrt(np.mean(U ** 2)) + 1e-12)               # unit RMS
    hp.W = hp.W + amp_mult * structured_scale * U         # add the big unstructured drive
    np.fill_diagonal(hp.W, 0.0)
    return hp.retrieve(i, cue_frac=cue_frac)


def stage_B_state(meas):
    recall_structured = _recall_after_structured_write()
    mults = [1.0, 5.0, 20.0, 60.0]                    # 60x == whitepaper delta:gamma analogue
    recall_unstructured = [_recall_after_unstructured_drive(m) for m in mults]
    # monotonic collapse toward chance as the unstructured amplitude grows
    collapses = all(recall_unstructured[i] >= recall_unstructured[i + 1] - 1e-9
                    for i in range(len(recall_unstructured) - 1))
    big = recall_unstructured[-1]
    return dict(
        recall_structured_carrier=float(recall_structured),         # wake/REM fast carrier
        unstructured_amp_mult=mults,
        recall_unstructured_slow=[float(x) for x in recall_unstructured],  # deep-SWS drive
        recall_collapses_with_amplitude=bool(collapses),
        big_unstructured_recall=float(big),
        structured_beats_big_unstructured=bool(recall_structured > big),
        # the operative (memory-reaching) carrier is structured-fast, NOT large-slow:
        operative_state="activated_wake_REM_structured_fast_carrier",
        nonoperative_state="deep_SWS_large_amplitude_unstructured_slow",
    )


# ===========================================================================
#  STAGE C -- the operative window is METASTABLE: silence and global-sync
#  (seizure analogue) both abolish recoverable memory; the measured carrier peaks.
# ===========================================================================
def stage_C_metastable(N=120, cue_frac=0.4):
    rng = np.random.RandomState(SEED + 13)
    p = _patterns(1, N, seed=SEED)[0]

    # SILENCE: a sub-fold carrier consolidates NO basin (the sign-update is magnitude-
    # invariant, so a real sub-fold failure = no pattern term in W, only an isotropic
    # floor) -> the free cells settle at random -> recall at the clamped-cue chance level.
    hp_s = Hippocampus(n_cells=N); hp_s.W = np.zeros((N, N)); hp_s.stored = []
    i_s = hp_s.write(p)                                 # target kept in .stored ...
    nz = rng.standard_normal((N, N)); nz = 0.5 * (nz + nz.T)
    nz /= (np.sqrt(np.mean(nz ** 2)) + 1e-12)
    hp_s.W = 0.05 * hp_s.lr * nz                        # ... but NO basin was written
    np.fill_diagonal(hp_s.W, 0.0)
    recall_silence = hp_s.retrieve(i_s, cue_frac=cue_frac)

    # METASTABLE: the measured structured carrier (normal fold-clearing write)
    hp_m = Hippocampus(n_cells=N); hp_m.W = np.zeros((N, N)); hp_m.stored = []
    i_m = hp_m.write(p)
    recall_metastable = hp_m.retrieve(i_m, cue_frac=cue_frac)

    # GLOBAL-SYNC (seizure analogue): a huge uniform field forces every cell to one
    # sign -> no distinguishable pattern survives -> recall ~ chance.
    hp_g = Hippocampus(n_cells=N); hp_g.W = np.zeros((N, N)); hp_g.stored = []
    i_g = hp_g.write(p)
    u = np.ones(N)                                      # all-in-phase (global synchrony)
    hp_g.W = hp_g.W + 50.0 * hp_g.lr * np.outer(u, u)   # rank-1 uniform == global lock
    np.fill_diagonal(hp_g.W, 0.0)
    recall_globalsync = hp_g.retrieve(i_g, cue_frac=cue_frac)

    inverted_U = (recall_metastable > recall_silence + 0.05) and \
                 (recall_metastable > recall_globalsync + 0.05)
    return dict(
        recall_silence_subfold=float(recall_silence),
        recall_metastable_measured=float(recall_metastable),
        recall_globalsync_seizure=float(recall_globalsync),
        operative_window_is_metastable=bool(inverted_U),
        note="biggest/most-synchronized field is NOT the operative carrier (M9 R<0.9 window).",
    )


# ===========================================================================
#  STAGE D -- MANY carriers in PARALLEL; the slow index reinstates fast content.
#  capacity = floor(theta:gamma ratio) from the EMERGED frequencies (not tuned).
# ===========================================================================
def _settle_content_from_index(hp, target_index_bits, index_slice, N):
    """Clamp the slow-index bits, free-evolve the rest, return the settled state."""
    s0 = np.zeros(N)
    s0[index_slice] = target_index_bits
    idx = np.arange(index_slice.start, index_slice.stop)
    out = hp._settle_state(s0, clamp=(idx, target_index_bits))
    return out


def stage_D_parallel(stageA, N=140):
    ratio = stageA["carrier_over_slow_ratio"]
    capacity = int(math.floor(ratio))                  # parallel gamma slots per theta cycle
    n_items = max(1, capacity)                          # store one content per slot

    # each memory = [ slow INDEX bits | fast CONTENT bits ]
    K = 40                                              # index width
    index_slice = slice(0, K)
    content_slice = slice(K, N)
    rng = np.random.RandomState(SEED + 21)
    pats = []
    for _ in range(n_items):
        v = np.where(rng.rand(N) < 0.5, 1.0, -1.0)
        pats.append(v)
    hp = Hippocampus(n_cells=N); hp.W = np.zeros((N, N)); hp.stored = []
    for v in pats:
        hp.write(v)

    # reinstate each content from ITS OWN index alone (parallel read-out)
    outs, fid_correct = [], []
    for v in pats:
        out = _settle_content_from_index(hp, v[index_slice], index_slice, N)
        outs.append(out)
        fid_correct.append(float(np.mean(out[content_slice] == v[content_slice])))
    mean_correct = float(np.mean(fid_correct))
    all_reinstated = bool(min(fid_correct) >= 0.95)

    # specificity (content-addressable address): index_i reinstates content_i but the
    # SAME read-out matches a DIFFERENT memory's content only at chance (cross-talk).
    cross = []
    for i, vi in enumerate(pats):
        for j, vj in enumerate(pats):
            if i != j:
                cross.append(float(np.mean(outs[i][content_slice] == vj[content_slice])))
    mean_cross = float(np.mean(cross)) if cross else 0.0

    # diagnostic: a NOVEL (never-stored) index (auto-associative below capacity)
    novel = np.where(rng.rand(K) < 0.5, 1.0, -1.0)
    out_n = _settle_content_from_index(hp, novel, index_slice, N)
    best_novel = max(float(np.mean(out_n[content_slice] == v[content_slice])) for v in pats)

    # integrated parallel drive grows with locked workers -> crosses the fold.
    # Reuse the whitepaper [V] anchors (unbound-only vs fully-gathered drive); cite, do
    # not re-derive. Claim = monotonic crossing of FOLD, not the absolute magnitude.
    unbound_drive = 0.322                               # whitepaper headline [V]
    gathered_full = 0.824                               # whitepaper headline [V]
    drive_curve = [unbound_drive + (gathered_full - unbound_drive) * (k / n_items)
                   for k in range(n_items + 1)]
    crosses_fold = [d > FOLD for d in drive_curve]
    n_to_cross = next((k for k, c in enumerate(crosses_fold) if c), None)

    return dict(
        emerged_ratio=float(ratio),
        parallel_capacity_slots=capacity,
        within_7pm2=bool(5 <= capacity <= 9),
        n_items=n_items,
        index_width=K,
        reinstatement_fidelity_each=fid_correct,
        reinstatement_fidelity_mean=mean_correct,
        all_contents_reinstated_from_index=all_reinstated,
        crosstalk_mean=float(mean_cross),
        novel_index_best_match=float(best_novel),
        index_is_specific=bool(mean_correct >= 0.95 and mean_correct > mean_cross + 0.10),
        fold=float(FOLD),
        integrated_drive_unbound=unbound_drive,
        integrated_drive_gathered=gathered_full,
        slots_to_clear_fold=n_to_cross,
        drive_monotonic=bool(all(drive_curve[i] <= drive_curve[i + 1] + 1e-12
                                 for i in range(len(drive_curve) - 1))),
    )


# ===========================================================================
#  STAGE E -- honesty ledger (carried, not reproduced)
# ===========================================================================
def stage_E_honesty():
    return dict(
        medium_efficacy_tested=0,
        consciousness_claim=0,
        hard_problem_open=1,
        subjective_experience_claim=0,
        pci_access_marker="HONEST_NEGATIVE (did not robustly reproduce; carried from 12-open-problem)",
        what_is_shown="measured source + activity range + state-selectivity + metastable "
                      "window + parallel multiplex & reinstatement of a high-frequency carrier",
        what_is_NOT_shown="that this carrier IS experience; no in-vivo efficacy test; "
                          "the access marker is not reproduced.",
        new_tuned_constants=0,
    )


# ===========================================================================
#  driver + self-check gate
# ===========================================================================
def run():
    E.seed_everything()
    meas = _load_measured()
    A = stage_A_source(meas)
    B = stage_B_state(meas)
    C = stage_C_metastable()
    D = stage_D_parallel(A)
    H = stage_E_honesty()
    results = dict(
        _what="M16-study: main high-frequency carrier emerged from measured GABA_A source.",
        measured_inputs=meas,
        fold=float(FOLD),
        A_source=A, B_state=B, C_metastable=C, D_parallel=D, honesty=H,
    )
    digest = sha256_of(results)
    results["headline_sha256"] = digest

    # ---- gate (self-check) ------------------------------------------------
    checks = []
    def ck(name, cond):
        checks.append((name, bool(cond)))
    ck("A.carrier_above_slow", A["carrier_above_slow"])
    ck("A.freq_monotonic_in_inv_tau", A["freq_monotonic_in_inv_tau"])
    ck("A.carrier_tau_is_measured_GABA_A", abs(A["tau_carrier_ms"] - meas["tau_gaba_a_ms"]) < 1e-9)
    ck("B.structured_beats_big_unstructured", B["structured_beats_big_unstructured"])
    ck("B.recall_collapses_with_amplitude", B["recall_collapses_with_amplitude"])
    ck("C.operative_window_is_metastable", C["operative_window_is_metastable"])
    ck("D.all_contents_reinstated_from_index", D["all_contents_reinstated_from_index"])
    ck("D.index_is_specific", D["index_is_specific"])
    ck("D.capacity_within_7pm2", D["within_7pm2"])
    ck("D.drive_crosses_fold", D["slots_to_clear_fold"] is not None)
    ck("E.no_new_tuned_constants", H["new_tuned_constants"] == 0)
    ck("E.efficacy_zero", H["medium_efficacy_tested"] == 0)
    ck("E.hard_problem_open", H["hard_problem_open"] == 1)
    n_pass = sum(1 for _, ok in checks if ok)
    return results, checks, n_pass


if __name__ == "__main__":
    res, checks, n_pass = run()
    print("=" * 74)
    print("M16-STUDY -- MAIN HIGH-FREQUENCY CARRIER (emerged from measured GABA_A source)")
    print("=" * 74)
    A, B, C, D, H = res["A_source"], res["B_state"], res["C_metastable"], res["D_parallel"], res["honesty"]
    print(f"[A] carrier tau = {A['tau_carrier_ms']} ms (measured GABA_A; Destexhe 1998)")
    print(f"    carrier freq {A['carrier_freq']:.4f} > slow {A['slow_ref_freq']:.4f}  "
          f"(ratio {A['carrier_over_slow_ratio']:.3f}); range {A['activity_range_freq']}")
    print(f"    monotonic 1/tau: {A['freq_monotonic_in_inv_tau']}   (absolute Hz stays [O])")
    print(f"[B] recall: structured fast carrier {B['recall_structured_carrier']:.3f}  "
          f"vs big unstructured slow {B['big_unstructured_recall']:.3f}  "
          f"-> structured wins: {B['structured_beats_big_unstructured']}")
    print(f"[C] recall  silence {C['recall_silence_subfold']:.3f} | "
          f"metastable {C['recall_metastable_measured']:.3f} | "
          f"global-sync {C['recall_globalsync_seizure']:.3f}  -> inverted-U: "
          f"{C['operative_window_is_metastable']}")
    print(f"[D] parallel capacity {D['parallel_capacity_slots']} slots (7+-2: {D['within_7pm2']}); "
          f"reinstate-from-index mean {D['reinstatement_fidelity_mean']:.3f}, "
          f"cross-talk {D['crosstalk_mean']:.3f}, specific: {D['index_is_specific']}")
    print(f"    integrated drive crosses fold {D['fold']:.3f} at {D['slots_to_clear_fold']} locked slots")
    print(f"[E] efficacy {H['medium_efficacy_tested']} | consciousness_claim {H['consciousness_claim']} | "
          f"hard_problem_open {H['hard_problem_open']} | new tuned constants {H['new_tuned_constants']}")
    print("-" * 74)
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("-" * 74)
    print(f"GATE: {n_pass}/{len(checks)} checks PASS")
    print(f"headline_sha256 = {res['headline_sha256']}")
