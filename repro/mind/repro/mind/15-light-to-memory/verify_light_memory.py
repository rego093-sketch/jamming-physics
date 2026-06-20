#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_light_memory.py  --  gate for M11 light -> brainwave -> rectified information
                            -> engram write -> multi-info roll -> downstream read (v1.13).
================================================================================
Re-runs the engine's emerge_light_memory_binding() and asserts:
  (A) bit-for-bit reproduction of the frozen M11 digest (determinism, SEED=19),
  (B) the rectification constants are FORCED, not fitted: single alpha = <|cos|> = 2/pi,
      double delta = <[cos]+[cos]+> = 1/pi^2, and the identity 2*pi = alpha/delta -- the
      cited VP angle theory (DOI 10.5281/zenodo.17932566), computed by quadrature here,
  (C) a brainwave IS emerged light: on the same lattice the per-step carrier angle goes
      ~10^13x finer than the optical step (the "angle below the point"), so information
      cannot live in the angle magnitude -- it lives in the relative PHASE,
  (D) superposition -> rectification -> information: the raw signed phase overlap averages
      to ~0; rectified, a BOUND (phase-locked) pair gives coincidence 1/4, an ANTIPHASE
      pair gives 0, and UNBOUND (unrelated) inputs sit at the double-rectification floor
      (1/pi)^2 = delta; the bound - unbound information contrast is strictly positive,
  (E) bound light WRITES a persisting engram (rectified drive clears the R19 fold) while
      unbound input does NOT write; the theta brainwave is the write clock (write/read on
      separated phases interfere at 0, mixed phase interferes more); several informations
      rolled into gamma slots within one theta frame ALL recover (fidelity 1.0),
  (F) a downstream neuron FEELS the rolled field: cancel < measured < augment (strictly
      monotone), field-mediated and non-circular; honesty markers: the coupling is the
      MEASURED kappa = 0.5496 (no new constant) and biological functional use stays OPEN
      (medium_efficacy_tested == 0).

It asserts only what the simulation shows -- a verified IN-SILICO mechanism for how
emerged light COULD write a memory. It does NOT claim biology uses light-rectified
binding to remember (OPEN, strongly inferred from the cited physics), and makes NO
claim of experience. Run from anywhere. Exit 0 = reproduces and the honest invariants hold.
"""
import os, sys, json, hashlib, math

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.normpath(os.path.join(HERE, "..", "_engine"))
RES = os.path.join(HERE, "light_memory_results.json")
EXP = os.path.join(HERE, "expected_lm_sha256.json")

fails = []; n = 0
def chk(name, cond):
    global n; n += 1
    if not cond: fails.append(name)

# load the engine and RE-RUN the module so assertions are on LIVE output ----------
sys.path.insert(0, ENGINE)
import vp_mind_engine as E
lm = E.emerge_light_memory_binding()

# (A) bit-for-bit reproduction of the frozen digest -------------------------------
rounded = E._round(lm)
canon = json.dumps(rounded, sort_keys=True, separators=(",", ":"),
                   ensure_ascii=False).encode("utf-8")
live = hashlib.sha256(canon).hexdigest()
exp = json.load(open(EXP))
chk("M11 reproduces frozen digest (bit-for-bit determinism)",
    live == exp["light_memory_results.json"])

# also: a second emerge gives identical digest (no hidden state) -------------------
lm2 = E.emerge_light_memory_binding()
canon2 = json.dumps(E._round(lm2), sort_keys=True, separators=(",", ":"),
                    ensure_ascii=False).encode("utf-8")
chk("M11 self-reproduces across two live emergences",
    hashlib.sha256(canon2).hexdigest() == live)

# (B) rectification constants are FORCED (cited angle theory, not fitted) ----------
chk("single rectification alpha = 2/pi (forced)",
    abs(lm["alpha_rect"] - 2.0 / math.pi) < 1e-9)
chk("double rectification delta = 1/pi^2 (forced)",
    abs(lm["delta_rect"] - 1.0 / math.pi**2) < 1e-9)
chk("identity 2*pi = alpha/delta (recovered, not assumed)",
    abs(lm["two_pi_from_alpha_over_delta"] - 2.0 * math.pi) < 1e-6)
chk("quadrature alpha matches closed form",
    abs(lm["alpha_quad"] - lm["alpha_rect"]) < 1e-6)

# (C) a brainwave is emerged light -- the carrier angle goes below the point -------
chk("brainwave per-step angle ~10^13x finer than optical (angle below the point)",
    lm["per_step_angle_ratio_optical_over_gamma"] > 1e13 * 0.5 and
    lm["per_step_angle_ratio_optical_over_gamma"] < 1e14)

# (D) superposition -> rectification -> information --------------------------------
chk("raw signed phase overlap averages to ~0 (cannot write unrectified)",
    abs(lm["raw_signed_overlap"]) < 1e-6)
chk("BOUND (phase-locked) coincidence = 1/4",
    abs(lm["coincidence_bound"] - 0.25) < 1e-9)
chk("UNBOUND coincidence floor = (1/pi)^2 = delta (NOT alpha^2)",
    abs(lm["coincidence_unbound_floor"] - 1.0 / math.pi**2) < 1e-9)
chk("information contrast (bound - unbound) is strictly positive",
    lm["information_contrast"] > 0.1 and
    abs(lm["information_contrast"] - (0.25 - 1.0 / math.pi**2)) < 1e-6)

# (E) bound light writes an engram; unbound does not; theta clock; rolled recover --
chk("bound, aligned drive clears the R19 engram fold and persists (a written memory)",
    lm["bound_input_writes_and_persists"] == 1.0 and
    lm["write_drive_bound"] > lm["engram_fold_threshold"])
chk("weak/antiphase (unbound) drive does NOT write",
    lm["unbound_input_no_write"] == 1.0)
chk("theta brainwave is the write clock: separated phases protect (interfere less)",
    lm["theta_phase_protects"] == 1.0 and
    lm["interference_phase_separated"] < lm["interference_phase_mixed"])
chk("several informations rolled into gamma slots in one theta frame ALL recover",
    lm["rolled_all_recovered"] == 1.0 and lm["rolled_mean_fidelity"] >= 0.999 and
    lm["rolled_slots"] >= 2.0)

# (F) a downstream neuron feels the rolled FIELD (non-circular) + honesty ----------
chk("downstream reader entrains: cancel < measured < augment (strictly monotone)",
    lm["reader_feels_field"] == 1.0 and
    lm["reader_lock_cancel"] < lm["reader_lock_measured"] < lm["reader_lock_augment"])
chk("reader response is field-mediated (positive field contribution)",
    lm["reader_field_contribution"] > 0.0)
chk("the coupling is the MEASURED kappa = 0.5496 (no new constant)",
    abs(lm["kappa_ephaptic_measured"] - 0.5496) < 1e-9)
chk("HONEST: biological functional use stays OPEN (medium_efficacy_tested == 0)",
    lm["medium_efficacy_tested"] == 0.0)

# ---------------------------------------------------------------------------------
if fails:
    print("LIGHT->MEMORY VERIFY FAIL:")
    for f in fails:
        print("  -", f)
    raise SystemExit(1)
print(f"LIGHT->MEMORY VERIFY PASS -- {n} checks (M11 reproduces + honest invariants), SEED=19")
print("  emerged light -> brainwave (same lattice) -> superpose with sensory EM ->")
print("  angle rectification (alpha=2/pi, delta=1/pi^2) -> sign-surviving INFORMATION bit ->")
print("  bound input writes a PERSISTING engram (unbound does not) -> multi-info roll ->")
print("  a downstream neuron FEELS the field (cancel<measured<augment).")
print("NOTE: verified IN-SILICO mechanism only -- biological USE is OPEN (medium_efficacy=0);")
print("      no claim of experience. Theory does not yet exist; built on the cited VP physics.")
