#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_phenomenology.py  --  gate for M12: mapping the 4D-DNA emergence onto MEASURED
                             literature OBSERVABLES (phenomena, NOT interpretations), and
                             running the emitted brainwave into the hypothalamus loop (v1.14).
================================================================================
Re-runs emerge_brainwave_phenomenology() and asserts:
  (A) bit-for-bit reproduction of the frozen M12 digest (determinism, SEED=19),
  (B) every observable the atlas flags 'matched' is actually REPRODUCED by the emergence
      (all five EEG bands delta..gamma emerge from the measured-master-gene organ substrate;
      the 40-Hz canonical gamma is present; the emitted brainwave front travels at ~c; the
      theta/gamma working-memory slot count sits in the observed 5-9 window; the hypothalamus
      sits in the slow/delta band) -- NONE of these were fitted; they are TARGETS reproduced,
  (C) the overall concordance is honest: in (0,1] and (for now) < 1 -- the 'target'-status
      observables (exact theta-gamma MI, 1/f slope, spindle band, SWS amplitude, dream-recall
      theta magnitude, panic timing, ADHD coupling, P300) are OWED, not faked,
  (D) the emitted brainwave drives the HYPOTHALAMUS in a bounded loop and a stronger drive
      raises hypothalamic arousal (the loop closes -- circulation), at the MEASURED kappa,
  (E) honesty: reproducing a phenomenon makes NO claim about its interpretation
      (medium_efficacy_tested == 0); nothing here says gamma IS consciousness.

It asserts only what the emergence shows. The GOAL of the program is to drive the overall
concordance to 1.0 (100% of catalogued measured observables) -- the owed targets are the
research roadmap, not a present claim. Run from anywhere. Exit 0 = reproduces + honest.
"""
import os, sys, json, hashlib, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
EXP = os.path.join(HERE, "expected_phenomenology_sha256.json")

fails = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond: fails.append(name)

sys.path.insert(0, ENGINE)
import vp_mind_engine as E
ph = E.emerge_brainwave_phenomenology()

# (A) bit-for-bit reproduction --------------------------------------------------
rounded = E._round(ph)
canon = json.dumps(rounded, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
live = hashlib.sha256(canon).hexdigest()
exp = json.load(open(EXP))
chk("M12 reproduces frozen digest (bit-for-bit determinism)", live == exp["phenomenology_results.json"])
ph2 = E.emerge_brainwave_phenomenology()
canon2 = json.dumps(E._round(ph2), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
chk("M12 self-reproduces across two live emergences", hashlib.sha256(canon2).hexdigest() == live)

# (B) every 'matched'-status observable is reproduced (none fitted) -------------
chk("every claimed (matched-status) observable is reproduced", ph["matched_status_all_reproduced"] == 1.0)
chk("all five EEG bands (delta..gamma) emerge from the organ substrate", ph["bands_covered"] == 5.0)
chk("the emitted brainwave front propagates at ~c (EM observable)", abs(ph["front_speed_over_c"] - 1.0) <= 0.05)
chk("working-memory slot count in the observed 5-9 window", 5.0 <= ph["wm_capacity_slots"] <= 9.0)
po = ph["per_observable"]
for band in ("delta_band_hz", "theta_band_hz", "alpha_band_hz", "beta_band_hz", "gamma_band_hz"):
    chk(f"observable reproduced: {band}", po.get(band, 0.0) == 1.0)
chk("observable reproduced: gamma_canonical_40hz", po.get("gamma_canonical_40hz", 0.0) == 1.0)
chk("observable reproduced: hypothalamus_slow_delta_hz", po.get("hypothalamus_slow_delta_hz", 0.0) == 1.0)

# (C) the overall concordance is HONEST (in (0,1] and targets owed) -------------
chk("overall observable concordance in (0,1]", 0.0 < ph["overall_concordance"] <= 1.0)
chk("there ARE owed targets (concordance honestly < 1 for now)",
    ph["overall_concordance"] < 1.0 and ph["n_matched"] < ph["n_observables"])

# (D) the emitted brainwave -> hypothalamus loop ------------------------------
chk("brainwave->hypothalamus loop stays bounded (no blow-up)", ph["hypo_loop_bounded"] == 1.0)
chk("stronger brainwave drive raises hypothalamic arousal (loop closes)",
    ph["arousal_feedback_positive"] == 1.0 and ph["arousal_high_drive"] > ph["arousal_low_drive"])
chk("coupling is the MEASURED kappa = 0.5496 (no new constant)", abs(ph["kappa_ephaptic_measured"] - 0.5496) < 1e-9)

# (E) honesty: no interpretation claim -----------------------------------------
chk("HONEST: phenomenon-mapping makes NO interpretation claim (efficacy == 0)", ph["medium_efficacy_tested"] == 0.0)

if fails:
    print("PHENOMENOLOGY VERIFY FAIL:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print(f"PHENOMENOLOGY VERIFY PASS -- {n} checks (M12 reproduces + honest), SEED=19")
print(f"  observable concordance: {int(ph['n_matched'])}/{int(ph['n_observables'])} "
      f"= {ph['overall_concordance']:.3f}  (all {int(ph['n_matched_status'])} claimed observables reproduced;")
print(f"  the rest are OWED research targets -- the goal is to drive this to 1.000).")
print(f"  4D-DNA organ substrate emits all 5 EEG bands; brainwave front ~c; WM slots "
      f"{ph['wm_capacity_slots']:.3f}; brainwave->hypothalamus loop bounded, arousal feedback +.")
print("NOTE: reproducing a measured PHENOMENON is NOT a claim about its interpretation;")
print("      medium_efficacy_tested=0; nothing here says gamma IS consciousness.")
