#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seb_verify.py  --  Sebaceous-duct STRESS BATTERY + gate (analogue of cycle_verify.py for the new
jamming target T7, and of pathology_verify.py for its diseases).

Two layers of check, each auditable (a silent pass is not allowed):
  (A) MECHANISM suite -- does the pilosebaceous duct, run as the shared R19 jamming switch on the
      MEASURED PRDM1 gamma, actually become a HYSTERETIC TWO-STATE OCCLUSION JAM? It must snap shut
      DISCONTINUOUSLY at the upper spinodal (patent -> comedo), reopen only at a LOWER spinodal on the
      way down (a true hysteresis loop, not a reversible threshold), and sit PATENT at the healthy
      net-occlusion set-point (the [V]/[F] substrate claim).
  (B) DISEASE suites -- each lesion is a clinical-sign + intervention-reversal test on that one jam,
      plus the opposite-mode discriminant: superficial REVERSIBLE acne vs deep IRREVERSIBLE-rupture HS,
      and the C. acnes amplifier toggling inflammatory <-> comedonal at a fixed jam (the headline check).
  (C) PROVENANCE -- the PRDM1 gamma must reproduce from the cached NCBI promoter offline (no fit).

seb_gate() is GREEN iff the mechanism suite passes, every disease passes, the discriminant holds, the
gamma reproduces offline, AND the layer is bit-reproducible (2x sha256). This gate is the sebaceous
layer's own research-first lock: its disease section is written only when this is green. It does NOT
touch the core run_all.py gate (repro/_verify/gates.py) -- the core T1..T5+ONCO battery is left frozen.
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(__file__))
import sebaceous_duct as S


def _mechanism_suite(summary):
    c = summary["_mechanism"]
    ok = bool(c["jams_discontinuously"] and c["hysteretic"]
              and c["jam_at_spinodal"] and c["clears_at_lower_spinodal"]
              and c["healthy_patent"])
    return dict(target="T7 (sebaceous-duct occlusion jam)", status="PASS" if ok else "FAIL",
                description="the pilosebaceous duct, run as the shared R19 jamming switch on its MEASURED PRDM1 gamma, becomes a hysteretic two-state occlusion jam: it snaps patent->comedo DISCONTINUOUSLY at the upper spinodal, reopens only at a LOWER spinodal on the way down (a hysteresis loop of finite width, not a reversible threshold), and sits PATENT at the healthy net-occlusion set-point",
                value={"gamma": c["gamma"], "spinodal": c["spinodal"],
                       "occ_jam_up": c["occ_jam_up"], "occ_clear_down": c["occ_clear_down"],
                       "up_jump_magnitude": c["up_jump_magnitude"], "hysteresis_width": c["hysteresis_width"],
                       "healthy_net_occlusion": c["healthy_net_occlusion"]},
                grade="shape [V]; regime-scale occlusion thresholds [F]",
                obstacle_if_open="absolute comedo/lesion counts and the sebum excretion rate are [O]: the jam is graded on discontinuity+hysteresis+direction, not as a fitted match; absolutes need a per-gland sebaceous calibration (parent target's obstacle)")


def _disease_suite(d):
    ok = bool(d.get("sign_matches_clinic") and d.get("intervention_reverses"))
    return dict(disease=d["disease"], target=d["target"], organ=d["organ"], status="PASS" if ok else "FAIL",
                mechanism=d["mechanism"], anchor=d["anchor"],
                sign_matches_clinic=d.get("sign_matches_clinic"), intervention_reverses=d.get("intervention_reverses"),
                grade=d["grade_shape"], obstacle_if_open=d["grade_absolute"])


def run_battery(summary=None):
    res = summary if summary is not None else S.sebaceous_summary()
    mech = _mechanism_suite(res)
    dis = [_disease_suite(v) for k, v in res.items() if not k.startswith("_")]
    disc = res["_opposite_sign_discriminant"]
    prov = res["_gamma_provenance"]
    all_pass = bool(mech["status"] == "PASS"
                    and all(s["status"] == "PASS" for s in dis)
                    and disc["all_opposite_pairs_reproduced"]
                    and prov["offline_reproduces"])
    return dict(mechanism_suite=mech, n_diseases=res["_n_diseases"], disease_suites=dis,
                opposite_sign_discriminant=disc, gamma_provenance=prov, all_pass=all_pass)


def determinism_ok():
    _, h1 = S._emit(S.sebaceous_summary()); _, h2 = S._emit(S.sebaceous_summary())
    return h1 == h2, h1


def seb_gate():
    """The sebaceous layer's research-first gate (its analogue of gates.research_gate())."""
    det, h = determinism_ok()
    b = run_battery()
    green = bool(det and b["all_pass"])
    return {"determinism_2xsha256_identical": det, "result_sha256": h,
            "mechanism_ok": b["mechanism_suite"]["status"] == "PASS",
            "all_diseases_pass": all(s["status"] == "PASS" for s in b["disease_suites"]),
            "discriminant_ok": b["opposite_sign_discriminant"]["all_opposite_pairs_reproduced"],
            "gamma_offline_reproduces": b["gamma_provenance"]["offline_reproduces"],
            "all_green": green}


if __name__ == "__main__":
    b = run_battery(); g = seb_gate()
    print(json.dumps(b, ensure_ascii=False, indent=2))
    print("\nseb_gate:", json.dumps(g, ensure_ascii=False))
    print("ALL PASS:", b["all_pass"], "(the sebaceous-duct section is written only when this is green)")
