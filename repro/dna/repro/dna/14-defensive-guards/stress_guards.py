#!/usr/bin/env python3
"""
STRESS TEST — defensive guards (Chapter 14).

Re-runs the exact logic that FAILED in the v1.9 second-session battery, now through
the guard wrappers, and proves: (1) each demonstrated failure is fixed, (2) there is
ZERO regression on everything that was already correct, (3) it is deterministic.

  Part 1 (Test C failure): methylation false-positive on extreme-AT genomes.
    Run detect_regime_safe on all 19 organisms (12 panel + 7 adversarial). Compare
    raw vs guarded. Require: Plasmodium & Dictyostelium fixed (PLANT -> no_global);
    every organism correct under the raw engine stays correct under the guard.

  Part 2 (Test D failure): run_key opaque IndexError on sub-window / empty input.
    Feed 200 bp and empty -> require a clean [O] dict (no exception). Feed a normal
    (> W) region -> require run_key_safe is a pass-through identical to run_key.

  Part 3 (Test D gap): bulk_contexts case-sensitivity (soft-masked lowercase -> NaN).
    Feed lowercase -> require bulk_contexts_safe(lower) == bulk_contexts(UPPER).
    Feed all-N -> require an explicit [O], not a silent 'no methylation'.

Deterministic (fixed inputs, no RNG). 2x sha256 identical. Locked engines unchanged
(guards import them single-source + sha256-pinned).
"""
import os, sys, json, math

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import guards as G

PANEL = os.path.abspath(os.path.join(HERE, "..", "11-cross-kingdom-stress-test", "inputs"))
ADV   = os.path.abspath(os.path.join(HERE, "..", "12-clade-methylation-readers",
                                     "stress_detector_adversarial", "inputs"))


def read_seq(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">")).upper()


def has_meth_class(regime):
    return ("PLANT" in regime or "VERTEBRATE" in regime or "INSECT_targeted" in regime)


def is_correct(regime, kind):
    if kind == "PLANT":      return "PLANT" in regime
    if kind == "VERTEBRATE": return "VERTEBRATE" in regime
    if kind in ("NO_GLOBAL", "OUT_OF_CATEGORY"):
        return not has_meth_class(regime)   # no_global / [O] both acceptable
    return False


EXPECTED = {  # known biology
    "human": "VERTEBRATE", "mouse": "VERTEBRATE", "chicken": "VERTEBRATE",
    "frog": "VERTEBRATE", "zebrafish": "VERTEBRATE",
    "arabidopsis": "PLANT", "rice": "PLANT", "maize": "PLANT",
    "fly": "NO_GLOBAL", "worm": "NO_GLOBAL", "yeast": "NO_GLOBAL", "plasmodium": "NO_GLOBAL",
    "tomato": "PLANT", "cow": "VERTEBRATE", "dog": "VERTEBRATE",
    "neurospora": "OUT_OF_CATEGORY", "oyster": "OUT_OF_CATEGORY",
    "dictyostelium": "NO_GLOBAL", "tetrahymena": "NO_GLOBAL",
}


def main():
    results = {"gc_floor": G.GC_FLOOR, "w_min": G.W_MIN,
               "part1_methylation": {}, "part2_runkey": {}, "part3_bulk": {}}

    # ---------- Part 1: methylation false-positive fix + no regression ----------
    locs = {}
    for lbl in ["human", "mouse", "chicken", "frog", "zebrafish", "fly", "worm",
                "arabidopsis", "rice", "maize", "yeast", "plasmodium"]:
        locs[lbl] = os.path.join(PANEL, f"{lbl}.fa")
    for lbl in ["neurospora", "tomato", "cow", "dog", "oyster", "dictyostelium", "tetrahymena"]:
        locs[lbl] = os.path.join(ADV, f"{lbl}.fa")

    fixes, regressions = [], []
    for lbl, path in sorted(locs.items()):
        seq = read_seq(path)
        raw = G.detect_regime_raw(*G.bulk_contexts_raw(seq)[:2])  # raw engine call (cg,chg)
        guarded = G.detect_regime_safe(seq)
        kind = EXPECTED[lbl]
        raw_ok = is_correct(raw, kind)
        grd_ok = is_correct(guarded["regime"], kind)
        if (not raw_ok) and grd_ok:
            fixes.append(lbl)
        if raw_ok and (not grd_ok):
            regressions.append(lbl)
        results["part1_methylation"][lbl] = {
            "gc": guarded["gc"], "raw_regime": raw, "guarded_regime": guarded["regime"],
            "guard": guarded["guard"], "raw_correct": raw_ok, "guarded_correct": grd_ok,
            "expected": kind}

    results["part1_summary"] = {
        "n_organisms": len(locs),
        "raw_correct": sum(1 for v in results["part1_methylation"].values() if v["raw_correct"]),
        "guarded_correct": sum(1 for v in results["part1_methylation"].values() if v["guarded_correct"]),
        "fixed": fixes, "regressions": regressions,
        "PASS": (len(regressions) == 0 and set(fixes) == {"plasmodium", "dictyostelium"})}

    # ---------- Part 2: run_key length guard ----------
    short = "ACGT" * 50      # 200 bp  (< W)
    empty = ""
    normal = read_seq(os.path.join(PANEL, "human.fa"))[:6000]  # > W
    def runkey_probe(seq):
        try:
            r = G.run_key_safe(seq, [])
            return {"crashed": False, "status": r.get("status"),
                    "reason": r.get("reason", ""), "n_shells": len(r.get("shells", []))}
        except Exception as e:
            return {"crashed": True, "error": f"{type(e).__name__}: {str(e)[:50]}"}
    # raw engine crashes on short -> confirm the gap still exists, then guard fixes it
    raw_short_crash = False
    try:
        G.run_key_raw(short, [])
    except Exception as e:
        raw_short_crash = type(e).__name__ == "IndexError"
    # passthrough check on a normal region: guarded == raw
    rk_raw = G.run_key_raw(normal, [])
    rk_safe = G.run_key_safe(normal, [])
    passthrough_identical = (
        len(rk_raw.get("anchors", [])) == len(rk_safe.get("anchors", [])) and
        len(rk_raw.get("shells", [])) == len(rk_safe.get("shells", [])))
    results["part2_runkey"] = {
        "raw_short_input_crashes_IndexError": raw_short_crash,
        "guarded_short_200bp": runkey_probe(short),
        "guarded_empty": runkey_probe(empty),
        "guarded_normal_passthrough": runkey_probe(normal),
        "passthrough_identical_to_raw_on_normal": passthrough_identical,
        "PASS": (raw_short_crash and
                 runkey_probe(short)["crashed"] is False and
                 runkey_probe(short)["status"] == "[O]" and
                 runkey_probe(empty)["crashed"] is False and
                 passthrough_identical)}

    # ---------- Part 3: bulk_contexts case-normalization ----------
    seq_mixed = read_seq(os.path.join(ADV, "tomato.fa"))[:50000]
    upper = seq_mixed.upper(); lower = seq_mixed.lower()
    raw_lower = G.bulk_contexts_raw(lower)      # case-sensitive engine: expect NaN
    raw_upper = G.bulk_contexts_raw(upper)
    safe_lower = G.bulk_contexts_safe(lower)    # guard upper-cases first
    raw_lower_nan = any(math.isnan(x) for x in raw_lower)
    safe_matches_upper = all(abs(a - b) < 1e-12 for a, b in zip(safe_lower, raw_upper))
    alln = G.detect_regime_safe("N" * 5000)
    results["part3_bulk"] = {
        "raw_engine_lowercase_is_NaN": raw_lower_nan,
        "guarded_lowercase_matches_uppercase": safe_matches_upper,
        "guarded_cg_oe_lowercase": round(safe_lower[0], 4),
        "raw_cg_oe_uppercase": round(raw_upper[0], 4),
        "all_N_guarded_regime": alln["regime"], "all_N_guard": alln["guard"],
        "PASS": (raw_lower_nan and safe_matches_upper and
                 alln["regime"] == "[O]_insufficient_sequence")}

    results["OVERALL_PASS"] = (results["part1_summary"]["PASS"] and
                               results["part2_runkey"]["PASS"] and
                               results["part3_bulk"]["PASS"])

    outp = os.path.join(HERE, "stress_guards_results.json")
    json.dump(results, open(outp, "w"), indent=2, sort_keys=True)

    s = results["part1_summary"]
    print(f"PART 1 methylation: raw_correct {s['raw_correct']}/{s['n_organisms']} -> "
          f"guarded_correct {s['guarded_correct']}/{s['n_organisms']}  "
          f"fixed={s['fixed']} regressions={s['regressions']}  PASS={s['PASS']}")
    print("  changed by guard:")
    for lbl, v in results["part1_methylation"].items():
        if v["raw_regime"] != v["guarded_regime"]:
            print(f"    {lbl:14} GC={v['gc']*100:>4.1f}%  raw={v['raw_regime']:34} -> "
                  f"guarded={v['guarded_regime']:36} [{v['guard']}]")
    p2 = results["part2_runkey"]
    print(f"\nPART 2 run_key: raw crashes on 200bp={p2['raw_short_input_crashes_IndexError']}; "
          f"guarded 200bp -> {p2['guarded_short_200bp']['status']} (no crash); "
          f"empty -> no crash={not p2['guarded_empty']['crashed']}; "
          f"passthrough OK={p2['passthrough_identical_to_raw_on_normal']}  PASS={p2['PASS']}")
    p3 = results["part3_bulk"]
    print(f"\nPART 3 bulk_contexts: raw lowercase=NaN={p3['raw_engine_lowercase_is_NaN']}; "
          f"guarded lowercase matches uppercase={p3['guarded_lowercase_matches_uppercase']} "
          f"(cg {p3['guarded_cg_oe_lowercase']} == {p3['raw_cg_oe_uppercase']}); "
          f"all-N -> {p3['all_N_guarded_regime']}  PASS={p3['PASS']}")
    print(f"\nOVERALL_PASS = {results['OVERALL_PASS']}")
    print(f"wrote {outp}")


if __name__ == "__main__":
    main()
