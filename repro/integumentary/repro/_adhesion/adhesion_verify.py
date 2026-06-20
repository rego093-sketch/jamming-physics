#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
adhesion_verify.py  --  Cell-adhesion STRESS BATTERY + gate (analogue of seb_verify.py for the new
binding target T8, and of pathology_verify.py for its diseases).

Two layers of check, each auditable (a silent pass is not allowed):
  (A) MECHANISM suite -- does keratinocyte adhesion, run as the shared R19 switch on the MEASURED KRT14
      gamma, actually become a HYSTERETIC TWO-STATE BINDING JAM? It must DETACH discontinuously at the
      spinodal (adherent -> blister), re-adhere only on climbing back above the upper spinodal (a true
      hysteresis loop, not a reversible threshold), and sit ADHERENT at the healthy (zero-antibody)
      set-point above the upper spinodal (the [V]/[F] substrate claim).
  (B) DISEASE suites -- each lesion is a clinical-sign + intervention-reversal test on that one switch,
      plus the opposite-property discriminant: the SAME adhesion switch, the SAME spinodal and the SAME
      antibody magnitude, with ONLY the targeted compartment differing, flips the cleavage plane
      (intraepidermal vs subepidermal), the Nikolsky sign (positive vs negative) and the blister tension
      (flaccid vs tense) -- the headline check.
  (C) PROVENANCE -- the adhesion target rides the ALREADY-MEASURED KRT14 gamma; no new gamma is fetched
      and none is fitted (the hair-cycle pattern: a new target on an existing measured organ).

adhesion_gate() is GREEN iff the mechanism suite passes, every disease passes, the discriminant holds,
the gamma is the existing measured KRT14 (no new fit), AND the layer is bit-reproducible (2x sha256).
This gate is the adhesion layer's own research-first lock: its disease section is written only when this
is green. It does NOT touch the core run_all.py gate (repro/_verify/gates.py) -- the core T1..T5+ONCO
battery is left frozen, and so are the pathology, hair-cycle and sebaceous layers.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import adhesion_switch as A


def _mechanism_suite(summary):
    c = summary["_mechanism"]
    ok = bool(c["detaches_discontinuously"] and c["hysteretic"]
              and c["detach_at_spinodal"] and c["readhere_at_upper_spinodal"]
              and c["healthy_adherent"])
    return dict(target="T8 (cell-adhesion binding jam)", status="PASS" if ok else "FAIL",
                description="keratinocyte adhesion, run as the shared R19 switch on its MEASURED KRT14 gamma, becomes a hysteretic two-state binding jam: a bond DETACHES discontinuously at the spinodal (adherent -> blister), re-adheres only on climbing back above the UPPER spinodal on the way out (a hysteresis loop of finite width, not a reversible threshold), and sits ADHERENT at the healthy zero-antibody set-point above the upper spinodal",
                value={"gamma": c["gamma"], "spinodal": c["spinodal"],
                       "adh_detach_down": c["adh_detach_down"], "adh_readhere_up": c["adh_readhere_up"],
                       "detach_jump_magnitude": c["detach_jump_magnitude"], "hysteresis_width": c["hysteresis_width"],
                       "healthy_net_adhesion": c["healthy_net_adhesion"]},
                grade="shape [V]; regime-scale adhesion/antibody thresholds [F]",
                obstacle_if_open="absolute blister counts, antibody titre (IU/mL), micrometre cleavage depth and involved body-surface area are [O]: the jam is graded on discontinuity+hysteresis+direction, not as a fitted match; absolutes need a per-junction adhesion calibration (parent target's obstacle)")


def _disease_suite(d):
    ok = bool(d.get("sign_matches_clinic") and d.get("intervention_reverses"))
    return dict(disease=d["disease"], target=d["target"], organ=d["organ"], status="PASS" if ok else "FAIL",
                mechanism=d["mechanism"], anchor=d["anchor"],
                sign_matches_clinic=d.get("sign_matches_clinic"), intervention_reverses=d.get("intervention_reverses"),
                grade=d["grade_shape"], obstacle_if_open=d["grade_absolute"])


def run_battery(summary=None):
    res = summary if summary is not None else A.adhesion_summary()
    mech = _mechanism_suite(res)
    dis = [_disease_suite(v) for k, v in res.items() if not k.startswith("_")]
    disc = res["_opposite_sign_discriminant"]
    prov = res["_gamma_provenance"]
    gamma_ok = bool(prov["new_gamma_fetched"] is False and prov["master"] == "KRT14")
    all_pass = bool(mech["status"] == "PASS"
                    and all(s["status"] == "PASS" for s in dis)
                    and disc["all_opposite_pairs_reproduced"]
                    and gamma_ok)
    return dict(mechanism_suite=mech, n_diseases=res["_n_diseases"], disease_suites=dis,
                opposite_sign_discriminant=disc, gamma_provenance=prov, gamma_is_existing_measured=gamma_ok,
                all_pass=all_pass)


def determinism_ok():
    _, h1 = A._emit(A.adhesion_summary()); _, h2 = A._emit(A.adhesion_summary())
    return h1 == h2, h1


def adhesion_gate():
    """The adhesion layer's research-first gate (its analogue of gates.research_gate())."""
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
    b = run_battery(); g = adhesion_gate()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\nadhesion_gate:", json.dumps(g, ensure_ascii=False))
    print("ALL PASS:", b["all_pass"], "(the cell-adhesion section is written only when this is green)")
