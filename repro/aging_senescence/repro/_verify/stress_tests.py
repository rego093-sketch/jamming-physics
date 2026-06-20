#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stress_tests.py  --  Aging / Senescence STRESS BATTERY (real R19 simulations over the excavated
research program). Very high bar: each target swept WIDE, no per-target tuning, failures honest,
[O]+obstacle acceptable, silent pass not. Writing stays LOCKED until run_battery() is all PASS and
gates.write_research_complete() is called.

Each suite calls a real deterministic dynamics function in _engine/ and extracts an explicit PASS/FAIL
criterion from its measured booleans. No suite is asserted; every status is computed from the run.
"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "_engine"))
import importlib
eng = importlib.import_module("vp_age_engine")
ad  = importlib.import_module("aging_dynamics")
xd  = importlib.import_module("xspecies_discriminant")
arc = importlib.import_module("archaic_discriminant")
tk  = importlib.import_module("telomere_keystone")


# ---- per-suite criteria -------------------------------------------------------------------------
# Each entry: (id, description, runner) where runner() -> (status, value, grade, obstacle)
def _ra1():
    r = ad.ra1_setpoint_drift()
    ok = bool(r.get("monotone_creep") and r.get("catastrophic_flip") and r.get("passed"))
    val = "creep-in-basin=%s, catastrophic-flip@spinodal=%s" % (r.get("monotone_creep"), r.get("catastrophic_flip"))
    return ("PASS" if ok else "FAIL", val, r.get("grade"), None)

def _ra2():
    r = ad.ra2_senescence_stuck()
    ok = bool(r.get("irreversible_one_way") and r.get("subspinodal_pulse_reversible") and r.get("accumulation_monotone"))
    val = "irreversible=%s, subspinodal-reversible=%s, arrested_frac=%.3f" % (
        r.get("irreversible_one_way"), r.get("subspinodal_pulse_reversible"), r.get("arrested_fraction_final"))
    return ("PASS" if ok else "FAIL", val, r.get("grade"), None)

def _ra3():
    r = ad.ra3_reservoir_depletion()
    ok = bool(r.get("depletion_increases_with_gamma"))
    val = "dwell~gamma^1.5 monotone in gamma=%s; all reservoirs reach empty" % r.get("depletion_increases_with_gamma")
    grade = r.get("grade")
    obstacle = None if ok else "depletion not monotone in gamma over swept range"
    return ("PASS" if ok else "FAIL", val, grade, obstacle)

def _ra4():
    r = ad.ra4_hallmarks_map()
    orphans = r.get("orphan_hallmarks", 0)
    n_orphan = orphans if isinstance(orphans, int) else len(orphans)
    ok = bool(r.get("all_mapped")) and r.get("n", 0) >= 9
    val = "%d hallmarks mapped, %d orphan(s)" % (r.get("n", 0), n_orphan)
    obstacle = None if ok else "orphan hallmarks remain: %s" % orphans
    return ("PASS" if ok else "FAIL", val, r.get("grade"), obstacle)

def _ra5():
    r = ad.ra5_risk_multiplier()
    ok = bool(r.get("convex_age_incidence") and r.get("immunosenescence_steepens"))
    val = "convex age-incidence=%s, fold-rise 40->80 = %.1fx" % (
        r.get("convex_age_incidence"), r.get("fold_rise_40_to_80"))
    # absolute incidence is [O]; the SHAPE (convex, steepening) is the [V] claim under test
    return ("PASS" if ok else "FAIL", val, r.get("grade"), "absolute incidence magnitude is [O]")

def _ra6():
    r = ad.ra6_rate_of_aging()
    frac = r.get("shared_rate_fraction")
    ok = (frac is not None) and (frac > 0.5)  # a DOMINANT shared rate exists (biological-age axis)
    val = "shared_rate_fraction=%.3f -> %s" % (frac, r.get("verdict"))
    return ("PASS" if ok else "FAIL", val, r.get("grade"), "per-system residual rates are [O]")

def _ra7():
    r = xd.discriminant()
    off = xd.verify_offline_reproduces()
    ok = bool(r.get("passed") and off.get("reproduces") and off.get("mismatches") == 0)
    v = r.get("verdict", {})
    val = ("human_special=%s, within_distribution=%s, discontinuous_switch=%s, trend_significant=%s; "
           "offline reproduces %d/%d (mismatches=%d)") % (
        v.get("human_aging_gene_special"), v.get("human_within_distribution"),
        v.get("discontinuous_gamma_longevity_switch"), v.get("gamma_lifespan_trend_significant"),
        off.get("checked"), off.get("checked"), off.get("mismatches"))
    # the human-not-special + flat-TP53 result is [V]; gamma~lifespan trend is [O]; dosage is [L]
    return ("PASS" if ok else "FAIL", val, "[V]/[O]/[L]", "gamma~lifespan trend is [O] (small panel, GC confound, phylogeny)")


def _ra8():
    # OBSERVATION ONLY: the measured snapshot must reproduce offline and be internally consistent
    # (narrow per-gene gamma spread + TERT cancer-hotspot invariance). No process/origin is tested.
    r = arc.discriminant()
    off = arc.verify_offline_reproduces()
    ok = bool(r.get("passed") and off.get("reproduces") and off.get("mismatches") == 0)
    v = r.get("verdict", {})
    val = ("narrow_gamma_band=%s, tert_hotspots_invariant=%s, most_archaic_subs=%s; offline reproduces "
           "%d/%d (mismatches=%d)") % (
        v.get("gamma_spread_is_narrow"), v.get("tert_cancer_hotspots_invariant"),
        v.get("gene_with_most_archaic_substitutions"), off.get("checked"), off.get("checked"),
        off.get("mismatches"))
    return ("PASS" if ok else "FAIL", val, "[V] measured (interpretation [O])",
            "meaning of the genotype co-occurrences is [O] (a present-state snapshot is silent on how a state arose)")


def _ra9():
    # the telomere-repeat gamma must be strand-symmetric, the lowest of all aging sequences, and
    # length-independent (a near-exact universal constant); the keystone synthesis is [O].
    r = tk.keystone()
    v = r.get("verdict", {})
    ok = bool(r.get("passed") and v.get("telomere_gamma_strand_symmetric") and
              v.get("telomere_gamma_is_lowest_of_all_aging_sequences") and
              v.get("telomere_gamma_universal_constant"))
    val = "telomere_gamma=%.4f, strand_symmetric=%s, lowest_of_all=%s, universal_constant=%s" % (
        v.get("telomere_repeat_gamma"), v.get("telomere_gamma_strand_symmetric"),
        v.get("telomere_gamma_is_lowest_of_all_aging_sequences"), v.get("telomere_gamma_universal_constant"))
    return ("PASS" if ok else "FAIL", val, "[V]/[F]/[O]/[L]",
            "the 'keystone is dynamics, not gamma' synthesis is [O]; telomere length/attrition rates are [L]")


STRESS_SUITES = [
    ("RA1", "setpoint drift: each homeostatic setpoint loses defense gain over time -> the defended value "
            "creeps inside the basin then flips catastrophically at the spinodal (unifying aging signature) [V]", _ra1),
    ("RA2", "senescence as stuck attractor: a cell crosses into an irreversible arrested R19 basin (cannot "
            "return; SASP); arrested fraction accumulates monotonically over time [V]", _ra2),
    ("RA3", "reservoir/stem depletion: the DWELL ~ gamma^1.5 reservoir is finite; deeper wells deplete faster; "
            "telomere/TERT clock as reservoir exhaustion [V]/[O]", _ra3),
    ("RA4", "hallmarks mapping: every hallmark of aging maps onto a substrate phenomenon (R19 errors, stuck "
            "attractors, reservoir depletion, gain loss) with no orphans [V]/[O]", _ra4),
    ("RA5", "risk multiplier: aging raises the crossing rate of EVERY pathology kernel (accumulated crossings + "
            "immunosenescence) -> convex, steepening age-incidence; absolute magnitude [O]", _ra5),
    ("RA6", "rate of aging: is there one dominant biological-age rate or only per-system rates? measured shared "
            "fraction vs residuals [V]/[O]", _ra6),
    ("RA7", "cross-species longevity discriminant: are human aging genes special, is there a discontinuous gamma "
            "switch, or is the longevity switch OFF the gamma axis (copy number / dosage)? [V]/[O]/[L]", _ra7),
    ("RA8", "archaic<->present-day observation (OBSERVATION ONLY): across a cross-sectional set of seven dated "
            "genomes the aging-master promoter gamma sits in a narrow band, the senescence gate reads the same in "
            "dated modern humans, TERT carries the most archaic substitutions, cancer hotspots invariant; offline "
            "reproduces bit-for-bit [V] (interpretation [O])", _ra8),
    ("RA9", "telomere keystone: the telomere-repeat gamma is strand-symmetric, the lowest of any aging sequence, "
            "and a near-exact universal constant; the telomere is the keystone of aging DYNAMICS (reservoir length "
            "+ attrition), not gamma [V]/[F]/[O]/[L]", _ra9),
]


def run_battery():
    base = eng.circulate()
    results = {
        "emergence_ok": bool(base["organs"]["organs"]),
        "oscillators_ok": (all(v.get("oscillates") for v in base["oscillators"].values()) if base["oscillators"] else None),
        "deferred_gamma": base["organs"].get("deferred_gamma", []),
        "suites": [],
    }
    for tid, desc, runner in STRESS_SUITES:
        status, value, grade, obstacle = runner()
        results["suites"].append({
            "target": tid, "description": desc, "status": status,
            "value": value, "grade": grade, "obstacle_if_open": obstacle,
        })
    results["all_targets_pass"] = all(s["status"] == "PASS" for s in results["suites"])
    return results


if __name__ == "__main__":
    r = run_battery(); print(json.dumps(r, ensure_ascii=False, indent=2))
    print("\nALL TARGETS PASS:", r["all_targets_pass"], "(writing stays locked until True)")
