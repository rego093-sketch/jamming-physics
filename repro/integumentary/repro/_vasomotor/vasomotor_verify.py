#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vasomotor_verify.py  --  Neurovascular-reactivity STRESS BATTERY + gate (analogue of adhesion_verify.py
for the new vasomotor target T9, and of pathology_verify.py for its diseases).

Two layers of check, each auditable (a silent pass is not allowed):
  (A) MECHANISM suite -- does cutaneous vasomotor tone, run as the shared R19 switch on the MEASURED EDAR
      gamma, actually become a HYSTERETIC TWO-LOCK reactivity jam? It must LOCK DILATED discontinuously at
      the upper spinodal and LOCK CONSTRICTED discontinuously at the lower spinodal (a true hysteresis
      loop of width ~2*spinodal, not a reversible threshold), and sit RESPONSIVE in the reversible middle
      at the healthy resting tone (the [V]/[F] substrate claim).
  (B) DISEASE suites -- each lesion is a clinical-sign + intervention-reversal test on that one switch,
      plus the opposite-property discriminant: the SAME vasomotor switch and the SAME spinodals, driven in
      OPPOSITE directions, give two clinically opposite diseases (vasodilation rosacea vs vasoconstriction
      Raynaud), reversibility is a uniform consequence of WHETHER a drive crosses its lock (fixed
      telangiectasia vs reversible vasospasm), and the within-rosacea vascular-vs-inflammatory axis comes
      from the papulopustular amplifier -- the headline check.
  (C) PROVENANCE + SEAM -- the vasomotor target rides the ALREADY-MEASURED EDAR gamma (no new gamma fetched,
      none fitted; the hair-cycle / adhesion pattern), and the dermal-perfusion magnitude stays an inherited
      circulatory citation (only the reactivity dynamics is added -- the SSOT seam is not crossed).

vasomotor_gate() is GREEN iff the mechanism suite passes, every disease passes, the discriminant holds,
the gamma is the existing measured EDAR (no new fit), AND the layer is bit-reproducible (2x sha256). This
gate is the vasomotor layer's own research-first lock: its disease section is written only when this is
green. It does NOT touch the core run_all.py gate (repro/_verify/gates.py) -- the core T1..T5+ONCO battery
is left frozen, and so are the pathology, hair-cycle, sebaceous and cell-adhesion layers.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import vasomotor_switch as V


def _mechanism_suite(summary):
    c = summary["_mechanism"]
    ok = bool(c["locks_discontinuously"] and c["hysteretic"]
              and c["dilate_lock_at_spinodal"] and c["constrict_lock_at_spinodal"]
              and c["healthy_responsive"])
    return dict(target="T9 (neurovascular reactivity jam)", status="PASS" if ok else "FAIL",
                description="cutaneous vasomotor tone, run as the shared R19 switch on its MEASURED EDAR gamma, becomes a hysteretic two-lock reactivity jam: the vessel LOCKS DILATED discontinuously at the upper spinodal and LOCKS CONSTRICTED discontinuously at the lower spinodal (a hysteresis loop of finite width, not a reversible threshold), and sits RESPONSIVE in the reversible middle at the healthy resting tone",
                value={"gamma": c["gamma"], "spinodal": c["spinodal"],
                       "v_dilate_lock_up": c["v_dilate_lock_up"], "v_constrict_lock_down": c["v_constrict_lock_down"],
                       "dilate_jump_magnitude": c["dilate_jump_magnitude"], "hysteresis_width": c["hysteresis_width"],
                       "healthy_net_vasodilator": c["healthy_net_vasodilator"]},
                grade="shape [V]; regime-scale tone/reactivity/constrictor thresholds [F]",
                obstacle_if_open="absolute erythema index, vessel density, flush magnitude, digital temperature, attack frequency and involved body-surface area are [O]: the jam is graded on discontinuity+hysteresis+direction, not as a fitted match; absolutes need a per-vessel calibration and the perfusion magnitude is an inherited circulatory seam (parent target's obstacle)")


def _disease_suite(d):
    ok = bool(d.get("sign_matches_clinic") and d.get("intervention_reverses"))
    return dict(disease=d["disease"], target=d["target"], organ=d["organ"], status="PASS" if ok else "FAIL",
                mechanism=d["mechanism"], anchor=d["anchor"],
                sign_matches_clinic=d.get("sign_matches_clinic"), intervention_reverses=d.get("intervention_reverses"),
                grade=d["grade_shape"], obstacle_if_open=d["grade_absolute"])


def run_battery(summary=None):
    res = summary if summary is not None else V.vasomotor_summary()
    mech = _mechanism_suite(res)
    dis = [_disease_suite(v) for k, v in res.items() if not k.startswith("_")]
    disc = res["_opposite_sign_discriminant"]
    prov = res["_gamma_provenance"]
    gamma_ok = bool(prov["new_gamma_fetched"] is False and prov["master"] == "EDAR")
    all_pass = bool(mech["status"] == "PASS"
                    and all(s["status"] == "PASS" for s in dis)
                    and disc["all_opposite_pairs_reproduced"]
                    and gamma_ok)
    return dict(mechanism_suite=mech, n_diseases=res["_n_diseases"], disease_suites=dis,
                opposite_sign_discriminant=disc, gamma_provenance=prov, gamma_is_existing_measured=gamma_ok,
                all_pass=all_pass)


def determinism_ok():
    _, h1 = V._emit(V.vasomotor_summary()); _, h2 = V._emit(V.vasomotor_summary())
    return h1 == h2, h1


def vasomotor_gate():
    """The vasomotor layer's research-first gate (its analogue of gates.research_gate())."""
    det, h = determinism_ok()
    b = run_battery()
    green = bool(det and b["all_pass"])
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "mechanism_ok": b["mechanism_suite"]["status"] == "PASS",
            "all_diseases_pass": all(s["status"] == "PASS" for s in b["disease_suites"]),
            "discriminant_ok": b["opposite_sign_discriminant"]["all_opposite_pairs_reproduced"],
            "gamma_is_existing_measured": b["gamma_is_existing_measured"],
            "all_green": green}


if __name__ == "__main__":
    b = run_battery(); g = vasomotor_gate()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\nvasomotor_gate:", json.dumps(g, ensure_ascii=False))
    print("ALL PASS:", b["all_pass"], "(the neurovascular-reactivity section is written only when this is green)")
