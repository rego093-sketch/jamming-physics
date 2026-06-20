#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
THETA (SLOW-INDEX) PACING ANCHOR -- STATUS DECISION-CHECK  (v1.19, Task 2B)
===========================================================================
THE QUESTION (handover sec 5).  The main carrier (M16) is grounded on the MEASURED GABA_A
decay tau = 6.0 ms (Destexhe 1998), so the FAST leg of the capacity ratio is measurement-
based. The SLOW leg -- the theta pacing the carrier:slow ratio rides on -- is still the
engine's tau_inh = 60.0 ms, an absolute pacing that is NOT a measured anchor: it is [O].
The task is to find a MEASURED, single-sourced anchor for the theta pacing and, if one
exists, promote the slow leg [O] -> [L]; otherwise state the obstacle and keep [O].

THE HONEST OUTCOME OF THIS SESSION: OBSTACLE -> the slow leg STAYS [O].  Reasons, by the
governance's own rules:

  (1) The anchors the handover names for theta PACING are the medial-septum GABAergic
      pacemaker dynamics and the Ih (HCN) h-current time constant. Neither is present as a
      numeric, cited, single-canonical value anywhere in THIS package's locked data. (A
      full scan of the engine data atlases finds theta as an OBSERVABLE -- frontal-midline
      ~6.5 Hz, Tort/Lega MI->recall -- but no locked septal/HCN PACING time-constant.)

  (2) VP-SPEC C1 single-source: an anchor that lives in the neuro object-layer must be
      CITED VERBATIM from the neuro package (no re-derivation), with the source sha256
      recorded. The neuro package is NOT included in this upload, so no such verbatim
      citation can be made here. Re-deriving or inventing a septal/HCN tau would violate
      the non-tuning and single-source rules -- exactly what the governance forbids.

  (3) A measured SLOW-INHIBITION constant IS in-package: GABA_B tau = 180.0 ms
      (synaptic_kinetics_measured, same atlas as the GABA_A carrier). It is reported below
      as a CANDIDATE for the next session, but it is NOT adopted as the theta pacing anchor,
      because GABA_B is a post-synaptic DECAY constant (it shapes the LFP aperiodic floor via
      synaptic charge, M13), NOT the septo-hippocampal theta PACEMAKER the handover specifies.
      Substituting it would be a DIFFERENT physical claim, made unilaterally -- so it is held
      as evidence, not promoted. (This mirrors gate (b) "no single canonical region" handling.)

ANTI-P-HACKING (handover sec 5 / 6-7).  We do NOT pick a slow tau to reproduce the carrier:
slow ratio 6.125. To make that concrete, the emergent ratio under the GABA_B candidate is
COMPUTED and reported AS-IS: it is NOT 6.125, which is the point -- the ratio is an emergent
quantity of whatever measured constants ground the two legs, never a target. Reporting it
keeps the reasoning honest and shows the 6.125 figure is not being back-fitted.

SCOPE: this is a measured-status record, not a consciousness claim. efficacy 0, hard problem
OPEN, consciousness_claim 0. Engine imported READ-ONLY; nothing here changes the engine.

Run:  PYTHONPATH=../_engine python3 theta_pacing_anchor_status.py     (from _consciousness/)
"""
import sys, os, json, hashlib
HERE   = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
sys.path.insert(0, ENGINE)
import vp_mind_engine as E  # READ-ONLY
from vp_mind_engine import Population

DATA = os.path.join(ENGINE, "data")
SPECTRAL = os.path.join(DATA, "spectral_observables_atlas.json")


def theta_anchor_status():
    syn = json.load(open(SPECTRAL, encoding="utf-8"))["synaptic_kinetics_measured"]
    tau_gaba_a = float(syn["GABA_A"]["tau_ms"])     # 6.0  -- the MEASURED fast carrier anchor
    tau_gaba_b = float(syn["GABA_B"]["tau_ms"])     # 180.0 -- a MEASURED slow-inhibition constant
    src_gaba_a = syn["GABA_A"]["source"]
    src_gaba_b = syn["GABA_B"]["source"]

    pop = Population(gamma=1.0)
    f_carrier  = pop.lfp(tau_inh=tau_gaba_a)["freq"]   # measured fast leg
    f_slow_eng = pop.lfp(tau_inh=60.0)["freq"]         # engine [O] slow reference (absolute pacing)
    f_slow_gbb = pop.lfp(tau_inh=tau_gaba_b)["freq"]   # GABA_B candidate slow leg (measured const)

    ratio_engine = f_carrier / f_slow_eng if f_slow_eng > 0 else float("nan")
    ratio_gaba_b = f_carrier / f_slow_gbb if f_slow_gbb > 0 else float("nan")

    return {
        "_meta": {
            "module": "theta_pacing_anchor_status_v1_19_task2B",
            "question": "is there a MEASURED, single-sourced theta-PACING anchor to promote the "
                        "carrier slow leg [O] -> [L]?",
            "outcome": "OBSTACLE -- slow leg STAYS [O] this session",
            "is_consciousness_claim": 0,
            "spectral_atlas_sha256": hashlib.sha256(open(SPECTRAL, "rb").read()).hexdigest(),
        },
        "measured_in_package": {
            "tau_gaba_a_ms": tau_gaba_a, "gaba_a_source": src_gaba_a,
            "tau_gaba_b_ms": tau_gaba_b, "gaba_b_source": src_gaba_b,
            "note": "GABA_A grounds the FAST carrier leg [F]. GABA_B is a measured slow-inhibition "
                    "DECAY constant (M13 aperiodic floor), present but NOT the theta pacemaker.",
        },
        "emergent_ratios_reported_as_is": {
            "carrier_freq": float(f_carrier),
            "slow_freq_engine_O_tau60": float(f_slow_eng),
            "slow_freq_gaba_b_candidate_tau180": float(f_slow_gbb),
            "carrier_over_slow_engine_O": float(ratio_engine),
            "carrier_over_slow_gaba_b_candidate": float(ratio_gaba_b),
            "note": "ratios are EMERGENT, not targets. The GABA_B-candidate ratio differs from the "
                    "engine-[O] ratio 6.125 -- demonstrating 6.125 is not back-fitted to any anchor.",
        },
        "obstacle": {
            "anchors_handover_names": ["medial_septum_GABAergic_pacemaker_dynamics",
                                       "Ih_HCN_h_current_time_constant"],
            "present_as_locked_numeric_canonical_in_package": False,
            "neuro_package_in_this_upload": False,
            "single_source_rule": "C1 -- a neuro-layer anchor must be cited VERBATIM from the neuro "
                                  "package with source sha256; not possible here (neuro absent).",
            "why_gaba_b_not_adopted": "GABA_B is a post-synaptic decay constant, not the septo-"
                                      "hippocampal theta PACEMAKER; adopting it would be a different, "
                                      "unilateral physical claim -> held as candidate, not promoted.",
        },
        "decision": {
            "slow_leg_grade": "O",
            "carrier_over_slow_ratio_grade": "O (slow leg) -- the dimensionless ratio is reported; "
                                             "ordering carrier>slow is [V], absolute pacing is [O]",
            "promotion_owed_to_next_session": "when the neuro package is available, cite the canonical "
                                              "septal-pacemaker / Ih(HCN) tau verbatim (record sha256), "
                                              "set the slow tau to it (or derive the ratio from two "
                                              "measured taus), and promote [O] -> [L].",
            "candidate_for_next_session": "GABA_B tau=180 ms (in-package, measured) IF research "
                                          "judgement accepts a synaptic-slow anchor; report emergent "
                                          "ratio as evidence, do not tune.",
        },
        "scope_flags": {"medium_efficacy_tested": 0.0, "hard_problem_open": 1.0, "consciousness_claim": 0.0},
    }


def _canon(obj):
    return json.dumps(E._round(obj), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def main():
    S = theta_anchor_status()
    blob = _canon(S); digest = hashlib.sha256(blob).hexdigest()
    with open(os.path.join(HERE, "theta_pacing_anchor_status.json"), "wb") as f:
        f.write(blob)
    exp = os.path.join(HERE, "expected_theta_anchor_sha256.json")
    if os.path.exists(exp):
        prev = json.load(open(exp)).get("theta_pacing_anchor_status.json")
        status = "MATCHES locked digest" if prev == digest else f"MISMATCH (locked={prev})"
    else:
        with open(exp, "w") as f:
            json.dump({"theta_pacing_anchor_status.json": digest,
                       "spectral_atlas_sha256": S["_meta"]["spectral_atlas_sha256"]}, f, indent=2)
        status = "WROTE expected_theta_anchor_sha256.json (first freeze)"

    er = S["emergent_ratios_reported_as_is"]; ob = S["obstacle"]; de = S["decision"]
    print("=" * 78)
    print("THETA (SLOW-INDEX) PACING ANCHOR -- STATUS (decision-check, v1.19 / Task 2B)")
    print("=" * 78)
    print(f"  carrier freq {er['carrier_freq']:.4f} (measured GABA_A 6.0 ms, [F])")
    print(f"  slow freq    engine-[O] tau60 {er['slow_freq_engine_O_tau60']:.4f}  ->  ratio "
          f"{er['carrier_over_slow_engine_O']:.3f}  (the M16 carrier:slow, slow leg [O])")
    print(f"  slow freq    GABA_B candidate tau180 {er['slow_freq_gaba_b_candidate_tau180']:.4f}  ->  ratio "
          f"{er['carrier_over_slow_gaba_b_candidate']:.3f}  (CANDIDATE, not adopted)")
    print("-" * 78)
    print(f"  OBSTACLE: canonical theta-PACING anchor (septal pacemaker / Ih(HCN) tau) present "
          f"as locked numeric? {ob['present_as_locked_numeric_canonical_in_package']}")
    print(f"            neuro package in this upload? {ob['neuro_package_in_this_upload']}  "
          f"-> single-source verbatim citation not possible here")
    print(f"            GABA_B not adopted: post-synaptic decay constant, not the theta pacemaker")
    print(f"  DECISION: slow leg grade = [{de['slow_leg_grade']}]  (promotion OWED to next session)")
    print(f"  ANTI-TUNING: emergent ratios reported as-is; 6.125 is not back-fitted to any anchor")
    print(f"  SCOPE: efficacy 0 | hard_problem_open 1 | consciousness_claim 0")
    print(f"  RESULTS DIGEST  {digest}")
    print(f"  {status}")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
