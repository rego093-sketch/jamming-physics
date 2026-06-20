#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stress_tests.py  --  Chronobiology (Circadian) STRESS BATTERY, wired to the live discriminants in
_engine/vp_clk_engine.py. Very high bar: each target is swept WIDE (no per-target tuning), failures are
reported honestly, an [O] grade is acceptable ONLY with a stated obstacle, a silently-green stub is not.
Writing stays LOCKED until run_battery()['all_targets_pass'] is True AND gates.write_research_complete()
has been called (research-first gate).

Each suite below pulls the REAL discriminant result and copies its `passes` flag verbatim -- there is no
independent re-judgement here, so the battery cannot drift away from the engine that produced the numbers."""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
eng = importlib.import_module("vp_clk_engine")

# (target id, what the WIDE sweep proves, engine-findings key, fn(result)->headline value, grade, obstacle-if-[O])
SUITE_SPEC = [
    ("RC1", "free-running clock: the molecular TTFL self-sustains a regular rhythm with ZERO external drive "
            "(FHN limit cycle); a STRONG tonic drive pins the switch high (depolarisation block) and silences it, "
            "proving the rhythm lives in a limit-cycle window, not trivially always-on.",
     "RC1", lambda r: f"free beats={r['free_running_beats']}, cv={r['free_running_cv']}, block beats={r['control_block_beats']}",
     "oscillator mechanism [V] / period 24h [L] / absolute phase [O]",
     "absolute circadian phase has no zero in the arb-time substrate (period is a cited [L] anchor)"),

    ("RC2a", "phase-response curve: a brief pulse swept across 18 phases produces BOTH advance and delay regions "
             "with a dead zone (the canonical biphasic circadian light PRC); sign flips across phase.",
     "RC2a", lambda r: f"max advance={r['max_advance']}, max delay={r['max_delay']}, biphasic={r['biphasic_prc']}",
     "PRC shape [V] / absolute phase reference [O]",
     "the phase axis is referenced to a spike, not to solar noon (no absolute zeitgeber zero in-substrate)"),

    ("RC2b", "entrainment / Arnold tongue: a periodic zeitgeber is swept over 15 detunings (0.65-1.35x natural) x 5 "
             "amplitudes (incl. very weak); the LOCKING RANGE widens monotonically with zeitgeber strength.",
     "RC2b", lambda r: f"locking range counts={r['locking_range_count']} over {r['n_detunings']} detunings",
     "entrainment + tongue [V] / absolute period [L]", None),

    ("RC3", "master vs network: N=8 coupled oscillators over coupling K=0..0.5; coherence rises monotonically with K "
            "(a synchronisation transition), AND a stronger SCN master gain pulls peripheral clocks into phase "
            "(drift falls) -- one network, master-led, not a single clock.",
     "RC3", lambda r: f"coherence_R={r['coherence_R']}, peripheral drift vs master={r['peripheral_phase_drift_vs_master']}",
     "synchronisation transition + master-led entrainment [V] / absolute phase lags [O]",
     "absolute SCN->periphery phase lags depend on un-modelled tissue conduction (only the ordering is claimed)"),

    ("RC4", "setpoint gating: the clock modulates the HPA cortisol DRIVE (mind M18 biexponential cascade, cited) over "
            "5 simulated days; the gated axis develops a strong daily cortisol rhythm while an ablated (constant-drive) "
            "clock is essentially flat (amp ratio > 50x). The clock IMPOSES rhythm on a defended setpoint.",
     "RC4", lambda r: f"gated amp={r['gated_cortisol_amplitude']} vs ablated amp={r['ablated_cortisol_amplitude']} (>50x)",
     "gating mechanism [V] / cortisol kinetics + window [L] / absolute cortisol level [O]",
     "absolute plasma cortisol concentration is not set here (only the clock-imposed modulation depth is claimed)"),

    ("RC5", "misalignment (shift work / jet lag): phase shift swept 0-12 h; re-entrainment time grows with the shift "
            "(PRC-limited ~1 h/day), and the SIGNED projection of cortisol onto external demand falls monotonically "
            "from +max through 0 (orthogonal) to -max (antiphase) -- the defended setpoint is dysregulated = disease.",
     "RC5", lambda r: f"reentrain cycles={r['reentrainment_cycles']}, demand-aligned cortisol={r['externally_aligned_cortisol_amp']}",
     "re-entrainment + degradation SIGN [V] / shift-work RR [L] / absolute incidence [O]",
     "absolute shift-work disease incidence needs an epidemiological dose model (only the dysregulation SIGN is claimed)"),

    ("RC6", "the MIND SEAM: circadian misalignment flattens the gated HPA cortisol rhythm; the flattening index grows "
            "monotonically with misalignment (0 aligned -> 2 antiphase). This sustained HPA dysregulation IS the "
            "CIRCADIAN depression contributor mind 27 explicitly LOCKED (the withdrawal-bias handle b<0). SIGN exported "
            "to mind; efficacy=0; the FELT quality of low mood stays in mind (consciousness_claim=0, hard problem OPEN).",
     "RC6", lambda r: f"HPA flattening index={r['hpa_flattening_index']}, sign matches mind={r['sign_consistent_with_mind_depression_handle']}",
     "flattening SIGN + mind-direction consistency [V] / magnitude of the handle [O]",
     "the MAGNITUDE of the depression handle is owned by mind; this package asserts only the direction/sign of the perturbation"),

    ("TX1", "chronotherapy (treatment): a PRC-correct zeitgeber (light / melatonin / wake therapy) re-aligns a "
            "phase-delayed clock while the SAME pulse at the WRONG phase worsens it; melatonin's PRC is ~antiphase to "
            "light (evening melatonin advances, morning light advances). Derived from the RC2 PRC -- NO new constant. "
            "efficacy=0; not medical advice; direction/timescale only.",
     "TX1", lambda r: f"corrected delay (correct phase)={r['corrected_delay_h_correct_phase']}, "
                      f"worsened (wrong phase)={r['resulting_delay_h_wrong_phase']}, light/melatonin antiphase={r['light_melatonin_antiphase']}",
     "re-alignment direction + antiphase PRCs [V] / clinical timing windows [L] / efficacy [O]=0",
     "clinical efficacy is set to 0 by firewall (this is the clock's control law, the PRC, not a dose-response claim)"),
]

def run_battery():
    base = eng.circulate()
    findings = base["findings"]
    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values())
                           if base["oscillators"] else None),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "suites": [],
    }
    for tid, desc, key, headline, grade, obstacle in SUITE_SPEC:
        r = findings[key]
        passed = bool(r.get("passes"))
        results["suites"].append({
            "target": tid,
            "description": desc,
            "status": "PASS" if passed else "FAIL",
            "value": headline(r),
            "grade": grade,
            "obstacle_if_open": obstacle,             # MUST be non-null for any [O] (else gate FAIL)
        })
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in results["suites"])
    results["n_targets"] = len(results["suites"])
    results["n_pass"] = sum(1 for s in results["suites"] if s["status"] == "PASS")
    return results

if __name__ == "__main__":
    r = run_battery()
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nTARGETS:", r["n_pass"], "/", r["n_targets"], "PASS")
    print("ALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
