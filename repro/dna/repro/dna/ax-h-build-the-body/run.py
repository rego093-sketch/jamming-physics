# -*- coding: utf-8 -*-
"""
run.py -- top-level runner for the BUILD package (Appendix H).

Produces (deterministically) under expected/:
  lock_manifest.json     every locked input, grade, provenance (no magic)
  manifest.json          the module inventory summary + example addresses
  count_grammar.json     the G7 count grammar (clock, count null, inverse lever, serial counts)
  size_switch.json       the size switch (relative sizes, monotone lever)
  assembly.json          the assembly graph + connectivity (one connected rooted tree)
  schedule.json          the 4D build schedule (program order, fill curve, resort lever)
  compiler.json          the renormalization compile (per-system rollup, semigroup, examples)
  declaration.json       the THREE-axis build declaration
  build_reading.json     the full interpret_build() reading
  gate_report.json       the fail-closed H1..H12 report (+ 2x-SHA witness)
  RESULT.txt             a human-readable honest summary

Usage:  python3 run.py
"""
import os
import json

from build import (lock, inventory, count, size, assembly, schedule,
                   compiler, declaration, interpreter, grading, gate)

_HERE = os.path.dirname(os.path.abspath(__file__))
_OUT = os.path.join(_HERE, "expected")


def _write(name, obj):
    os.makedirs(_OUT, exist_ok=True)
    with open(os.path.join(_OUT, name), "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=True, ensure_ascii=False)


def main():
    _write("lock_manifest.json", lock.lock_manifest())

    summ = inventory.summary()
    _write("manifest.json", {
        "summary": summ,
        "examples": {n: inventory.address(n)
                     for n in ("femur_L", "C1_atlas", "heart", "molar_UL_1",
                               "incisor_UL_1", "biceps_brachii")},
    })

    cgr = count.read()
    _write("count_grammar.json", cgr)
    _write("size_switch.json", size.read())
    _write("assembly.json", assembly.read())
    sch = schedule.read()
    _write("schedule.json", sch)
    cmp = compiler.read()
    _write("compiler.json", cmp)

    decl = declaration.build_declaration()
    _write("declaration.json", decl)

    reading = interpreter.interpret_build()
    rhash = interpreter.reading_hash(reading)
    _write("build_reading.json", reading)

    gate_report = gate.run_gate(verbose=False)
    _write("gate_report.json", gate_report)

    comp = grading.completion_status()

    # ---- human-readable RESULT ------------------------------------------------
    L = []
    L.append("=" * 78)
    L.append("  BUILD THE BODY -- from the readable blueprint to a BUILD-SPECIFIED body")
    L.append("  (Appendix F read the blueprint; here the house is specified, brick by brick)")
    L.append("=" * 78)
    L.append("")
    L.append("THE MODULE MANIFEST (the body as hundreds of addressed parts):")
    L.append("  named modules: %d   (%s)"
             % (summ["n_modules_named"],
                ", ".join("%s %d" % (k, v) for k, v in summ["by_kind"].items())))
    L.append("  bones EXPANDED from program group counts = %d  (matches 206: %s)"
             % (summ["bone_count_named"], summ["bone_count_matches_206"]))
    L.append("  driver programs used: %d   distinct driver gammas: %d"
             % (summ["n_driver_programs_used"], summ["n_distinct_gammas"]))
    fem = inventory.address("femur_L")
    L.append("  example address  femur_L: program=%s driver=%s gamma=%.6f L=%s parent=%s"
             % (fem["group"], fem["driver"], fem["gamma"], fem["renorm_level"], fem["parent"]))
    L.append("")
    sb = cgr["somite_budget"]
    cn = cgr["count_null"]
    lv = cgr["lever_invariant"]
    L.append("THE COUNT GRAMMAR G7 (갯수): the segmentation clock sets serial NUMBER")
    L.append("  law: N_serial ~ T_window / P_clock  (clock period P, axis-elongation window T)")
    L.append("  human clock period = %g min; recovered somite pairs = %g; presacral vertebrae(real) = %s"
             % (sb["clock_period_min"], sb["recovered_somite_pairs"], sb["presacral_vertebrae_real"]))
    L.append("  COUNT NULL: |corr(driver gamma, serial index)| = %.3f (ceiling %.2f) -> count is the "
             "clock's integral, not gamma [V]"
             % (cn["abs_corr_gamma_vs_serial_index"], cn["ceiling"]))
    L.append("  INVERSE LEVER: halve P -> x%.2f count ; double P -> x%.2f count (exact) [V]"
             % (lv["fast_ratio"], lv["slow_ratio"]))
    sc = cgr["serial_counts"]["realized_serial_counts"]
    L.append("  realized counts: vertebrae presacral=%s, ribs/thoracic=%s, digits/limb=%s, teeth=%s"
             % (sc.get("presacral_vertebrae"), sc.get("thoracic_vertebrae_and_rib_pairs"),
                sc.get("digits_per_limb"), sc.get("permanent_teeth")))
    L.append("")
    sz = size.read()
    sl = sz["lever_monotone"]
    L.append("THE SIZE SWITCH (장기 문법 + 크기 스위치): relative magnitude from a dosage lever")
    L.append("  law: SIZE = base(system) * dosage^%g ; gamma fixes program, NOT magnitude (size null)"
             % sl["exponent"])
    L.append("  monotone in dosage: %s ; ranking preserved across dosage: %s (a switch, not a refit) [V]"
             % (sl["monotone_in_dosage"], sl["ranking_preserved_across_dosage"]))
    L.append("")
    ac = assembly.connectivity()
    L.append("THE ASSEMBLY GRAMMAR (a body, not a pile of bricks):")
    L.append("  part-to-part tree rooted at %s ; %d nodes ; all modules reach root: %s ; max depth %d"
             % (ac["root"], ac["n_nodes"], ac["all_modules_reach_root"], ac["max_assembly_depth"]))
    L.append("  single connected rooted tree: %s (the joinery makes one body) [V]"
             % ac["single_connected_rooted_tree"])
    L.append("")
    rl = sch["resort_lever"]
    fc = sch["fill_curve"]
    half = next((r for r in fc if r["fraction_present"] >= 0.5), fc[-1])
    L.append("THE 4D BUILD SCHEDULE (조금씩 조금씩 발달): modules appear in spinodal-gamma order")
    L.append("  order = argsort(spinodal(gamma)) (Appendix A, verbatim); body fills over tau in [0,1]")
    L.append("  half the modules present by tau ~ %.2f ; perturb a gamma -> fill order resorts: %s [V]"
             % (half["tau"], rl["schedule_resorts_on_gamma_change"]))
    L.append("")
    bd = cmp["body"]
    tc = cmp["tower_composition"]
    L.append("THE RENORMALIZATION COMPILER (강성화: rigidify finished modules, climb the tower):")
    L.append("  R (Appendix C, verbatim): rho'=phi*rho ; B'=phi*B*J(phi) in [Reuss=0, Voigt=phi*B] ; "
             "c'=c*sqrt(J)")
    L.append("  compiled %d modules at phi=%.2f ; ALL inside exact [Reuss,Voigt] bracket: %s [V]"
             % (bd["n_modules_compiled"], bd["phi"], bd["all_within_exact_bracket"]))
    L.append("  body LEVEL (mean effective rel-modulus) = %.4f ; R composes (semigroup): %s [V]"
             % (bd["body_LEVEL_mean_Beff_rel"], tc["composes_exactly"]))
    L.append("  => a module BECOMES volume + stiffness by the act of packing; the tower is climbed at")
    L.append("     the MODULE level (hundreds of rigid parts), not the impossible cell level")
    L.append("")
    L.append("THE BUILD DECLARATION (해독 선언) -- THREE axes, honest")
    L.append("  STRUCTURAL  / read the blueprint   : %s  (Appendix F; G1..G6 unchanged)"
             % ("COMPLETE (100%)" if decl["structural_complete"] else "NOT COMPLETE"))
    L.append("  CONSTRUCTIVE/ specify the build     : %s  (this appendix: addressed/counted/sized/"
             "assembled/scheduled/compiled)"
             % ("COMPLETE (100%)" if decl["constructive_complete"] else "NOT COMPLETE"))
    L.append("  PHYSICAL    / instantiate real tissue: OPEN")
    for ob in decl["physical"]["open_obstacles"]:
        L.append("    [O] %s -> %s" % (ob["level"], ob["obstacle"]))
    L.append("  => 100% means the blueprint is fully READ and fully BUILD-SPECIFIED;")
    L.append("     what remains is MATTER, not grammar and not a missing build rule")
    L.append("")
    L.append("HONEST STATUS (precision != accuracy)")
    L.append("  structural_complete = %s   constructive_complete = %s   physical_complete = %s"
             % (comp["structural_complete"], comp["constructive_complete"],
                comp["physical_complete"]))
    L.append("")
    gate_ok = gate_report["_all_pass"]
    n_pass = sum(1 for k, v in gate_report.items() if isinstance(v, dict) and v.get("pass"))
    L.append("-" * 78)
    L.append("  GATE: %s (%d/%d)   gate sha=%s   reading hash=%s"
             % ("PASS" if gate_ok else "FAIL", n_pass, len(gate.CHECKS),
                gate_report["_sha256"], rhash))
    L.append("  LOCK -> Derive -> Gate. No fitted parameters. precision != accuracy. 반증=발견. 집.")
    L.append("-" * 78)
    txt = "\n".join(L)
    with open(os.path.join(_OUT, "RESULT.txt"), "w", encoding="utf-8") as fh:
        fh.write(txt + "\n")
    print(txt)
    print()
    print("[wrote] %s/ (lock_manifest, manifest, count_grammar, size_switch, assembly, schedule, "
          "compiler, declaration, build_reading, gate_report, RESULT.txt)" % _OUT)
    return 0 if gate_ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
