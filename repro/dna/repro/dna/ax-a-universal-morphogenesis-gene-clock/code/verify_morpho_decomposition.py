"""
verify_morpho_decomposition.py -- neuro-VP-SPEC-style gate for the v9 SHAPE-decomposition capstone.

This gate certifies the project's headline claim in its honest form: measured DNA is the FIRST CAUSE of
form, fixing a core that environment then fills in around -- not 100% of the shape. It enforces that the
decomposition is computed on the package's already-gated gene x environment machinery and that every claim
matches the measured evidence and the locked, cited twin-study anchor (to which the model is never tuned).

PASS means: (1) over a genetic-propensity x environment grid the variance of body shape splits into a
substantial genetic fraction AND a substantial environmental fraction (shape is neither all-DNA nor
all-environment); (2) the genetic fraction H^2 sits in the published twin-heritability REGIME -- the
reference H^2 lies in the published band, the model's achievable H^2 range overlaps it, and H^2 FALLS as
the environmental range widens (reproducing the published population-dependence of heritability), a regime
match rather than a tuned decimal; (3) the identical-twin decomposition holds -- one genome at the shared
lean reference is bit-identical between the twins (the DNA-fixed resemblance) and two different lives give a
larger, rounder body+face for the surplus twin (the environmental envelope), with the face moving in the
cheek/jowl band the twin literature flags as environmental; (4) the genetic axis is a real measured-gamma
readout (raising a pro-storage gene's gamma raises propensity; raising a satiety gene's lowers it), the fat
fold IS the body fold (one switch), the lean baseline is preserved (alpha=0 -> field == lean target), and the
explicit alpha used equals the gated model's activation; the anchor file is the locked cited input; (5)
determinism. With the real model all of this holds -- and this gate passes precisely because it does. Honest
[O] recorded in the ledger: the model's facial BONE has no non-adiposity environmental axis (aging, gravity),
so for those it trivially attributes 100% to DNA, which real faces do not -- the clearest remaining open slot.

Checks (PASS = 5/5):
  1. DECOMPOSITION SUBSTANTIAL   at the reference range H^2+E^2+GxE = 1, with H^2 >= 0.15 AND E^2 >= 0.10
                                 (both DNA and environment contribute materially to shape).
  2. HERITABILITY REGIME         reference H^2 in the published band; model H^2 range overlaps the band; and
                                 H^2(narrow env) > H^2(ref) > H^2(wide env) (population-dependence reproduced).
  3. TWIN DECOMPOSITION          same genome at the shared lean reference is bit-identical (resemblance); the
                                 surplus twin has larger body volume AND higher lower-face W:H than the active
                                 twin (the environmental envelope, correct direction).
  4. GAMMA READOUT + BASELINE    gene effect is a measured-gamma readout; one-switch < 1e-12; alpha(lean) ~ 0
                                 (lean baseline preserved); explicit alpha == model.activation; anchor sha frozen.
  5. DETERMINISM                 two independent analyze() runs -> identical sha256 of the result.
"""
import os, json, hashlib
import numpy as np
import gene_clock as GC
import morpho_decomposition as MD


def _result_sha(res):
    pop = res["population_decomposition"]; tw = res["twin_demo"]
    keep = {"Href": round(pop["reference"]["H2_genetic"], 6),
            "Hnar": round(pop["narrow_env"]["H2_genetic"], 6),
            "Hwid": round(pop["wide_env"]["H2_genetic"], 6),
            "falls": pop["H2_falls_as_env_widens"],
            "core": tw["shared_core_bit_identical"],
            "volB": round(tw["body_volume"]["twinB"], 3),
            "volA": round(tw["body_volume"]["twinA"], 3),
            "whB": round(tw["face_width_height"]["twinB"], 6),
            "whA": round(tw["face_width_height"]["twinA"], 6),
            "anchor_sha256": res["anchor_sha256"]}
    return hashlib.sha256(json.dumps(keep, sort_keys=True).encode()).hexdigest()


# ----------------------------------------------------------------- check 1
def check_decomposition_substantial(res):
    r = res["population_decomposition"]["reference"]
    s = r["H2_genetic"] + r["E2_environment"] + r["GxE_resid"]
    sums_to_one = abs(s - 1.0) < 1e-9
    both = (r["H2_genetic"] >= 0.15) and (r["E2_environment"] >= 0.10)
    ok = bool(sums_to_one and both)
    return ok, (f"reference H2(DNA)={r['H2_genetic']:.3f} E2(env)={r['E2_environment']:.3f} "
                f"GxE+res={r['GxE_resid']:.3f} (sum={s:.4f}); both substantial={both}")


# ----------------------------------------------------------------- check 2
def check_heritability_regime(res):
    rg = res["heritability_regime"]
    ok = bool(rg["reference_in_published_band"] and rg["model_range_overlaps_published_band"]
              and rg["H2_falls_as_env_widens"])
    pop = res["population_decomposition"]
    return ok, (f"reference H2={rg['reference_H2']:.3f} in published band {rg['published_band']}="
                f"{rg['reference_in_published_band']}; model range "
                f"{pop['H2_achievable_range'][0]:.2f}..{pop['H2_achievable_range'][1]:.2f} overlaps band="
                f"{rg['model_range_overlaps_published_band']}; H2 falls as env widens="
                f"{rg['H2_falls_as_env_widens']} (pop-dependence reproduced)")


# ----------------------------------------------------------------- check 3
def check_twin_decomposition(res):
    tw = res["twin_demo"]
    bv = tw["body_volume"]; fw = tw["face_width_height"]
    core_ok = tw["shared_core_bit_identical"]
    vol_dir = bv["twinB"] > bv["twinA"]          # surplus twin larger
    face_dir = fw["twinB"] > fw["twinA"]         # surplus twin rounder lower-face
    ok = bool(core_ok and vol_dir and face_dir)
    return ok, (f"shared DNA core bit-identical={core_ok}; surplus twin larger body ({bv['twinB']:.0f}>"
                f"{bv['twinA']:.0f})={vol_dir} & rounder face (W:H {fw['twinB']:.3f}>{fw['twinA']:.3f})="
                f"{face_dir}; envelope: +{tw['envelope_pct']['body_volume_added']:.0f}% volume, "
                f"+{tw['envelope_pct']['face_roundness_widened']:.0f}% face roundness from identical DNA")


# ----------------------------------------------------------------- check 4
def check_gamma_readout_and_baseline(res):
    fa = res["falsifiability"]
    ea = fa["explicit_alpha_matches_model"]["ok"]
    gr = fa["gene_effect_is_gamma_readout"]["ok"]
    sb = fa["one_switch_and_baseline"]
    sb_ok = sb["ok"]
    anchor_frozen = (MD.anchor_sha256() == res["anchor_sha256"])
    ok = bool(ea and gr and sb_ok and anchor_frozen)
    return ok, (f"explicit_alpha==model={ea}; gene_effect_is_gamma_readout={gr}; one_switch="
                f"{sb['assert_one_switch']:.1e} & alpha(lean)={sb['alpha_at_lean']:.1e} (baseline preserved); "
                f"anchor_sha_frozen={anchor_frozen}")


# ----------------------------------------------------------------- check 5
def check_determinism():
    r1 = MD.analyze(); r2 = MD.analyze()
    h1, h2 = _result_sha(r1), _result_sha(r2)
    return (h1 == h2), f"result sha {h1[:10]}=={h2[:10]} ({h1 == h2})"


def main():
    res = MD.analyze()
    checks = [
        ("1 DECOMPOSITION SUBSTANTIAL (shape is part DNA, part environment)", check_decomposition_substantial(res)),
        ("2 HERITABILITY REGIME (in published band; H2 falls as env widens)", check_heritability_regime(res)),
        ("3 TWIN DECOMPOSITION (shared DNA core + environmental envelope)", check_twin_decomposition(res)),
        ("4 GAMMA READOUT + LEAN BASELINE (gene axis measured; baseline preserved)", check_gamma_readout_and_baseline(res)),
        ("5 DETERMINISM (2x run identical)", check_determinism()),
    ]
    npass = 0
    pop = res["population_decomposition"]; tw = res["twin_demo"]
    print("=" * 86)
    print("  MORPHOGENESIS-DECOMPOSITION GATE  |  how much of SHAPE does measured DNA fix?")
    print("=" * 86)
    for name, (ok, msg) in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}]  {name}\n           {msg}")
        npass += int(ok)
    print("=" * 86)
    print(f"  HEADLINE: at a realistic environmental range the genetic fraction of body shape is "
          f"H2={pop['reference']['H2_genetic']:.2f} (published twin BMI/body-composition H2 ~ 0.48-0.63), and it")
    print(f"  falls to {pop['wide_env']['H2_genetic']:.2f} as environmental variation widens -- reproducing the "
          f"population-dependence of heritability. Identical twins share a bit-identical DNA core; a")
    print(f"  surplus life adds {tw['envelope_pct']['body_volume_added']:.0f}% body volume and "
          f"{tw['envelope_pct']['face_roundness_widened']:.0f}% face roundness. DNA is the first cause of form, not all of it.")
    print(f"OVERALL: {'PASS' if npass == len(checks) else 'FAIL'} ({npass}/{len(checks)} checks)")

    out = os.path.join(GC.HERE, "..", "results", "morpho_decomposition_verify.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    json.dump({name: dict(pass_=bool(ok), msg=msg) for name, (ok, msg) in checks}
              | {"overall": f"{npass}/{len(checks)}",
                 "headline": dict(reference_H2=pop["reference"]["H2_genetic"],
                                  wide_env_H2=pop["wide_env"]["H2_genetic"],
                                  H2_falls_as_env_widens=pop["H2_falls_as_env_widens"],
                                  twin_core_bit_identical=tw["shared_core_bit_identical"],
                                  body_volume_added_pct=tw["envelope_pct"]["body_volume_added"],
                                  face_roundness_widened_pct=tw["envelope_pct"]["face_roundness_widened"])},
              open(out, "w"), indent=2)
    return npass == len(checks)


if __name__ == "__main__":
    import sys
    sys.exit(0 if main() else 1)
