#!/usr/bin/env python3
"""
GUARD VALIDATION (out-of-sample) — does GC_FLOOR=0.25 generalize, or was it fit to
the discovery set?

The 0.25 floor was chosen from the clean GC gap among the organisms that *found* the
Test C false positive (Plasmodium 20.4%, Dictyostelium 22.3%, Tetrahymena 23.5%,
tomato 30.9%). That is in-sample. Here we test the floor on 7 organisms that were
NOT used to set it (frozen `inputs/`, provenance + sha256):

  group (a) real global methylators: soybean, moss (Physcomitrium), brassica
  group (b) AT-rich non-methylators: theileria, cryptosporidium, entamoeba, trichomonas

Three out-of-sample questions:
  Q1 FALSIFICATION — does any real global methylator (group a) sit BELOW 25% GC?
     If yes, the guard wrongly suppresses a real signal -> floor falsified.
  Q2 BELOW-FLOOR    — entamoeba (expected <25%): does the guard correctly catch a
     NEW below-floor non-methylator?
  Q3 ABOVE-FLOOR    — non-methylators ABOVE 25% (theileria/crypto/trichomonas): does
     the RAW detector stay correct (no_global)? Any PLANT call there is a failure the
     guard does NOT catch (floor too low, or problem not purely GC).

Verdict logic:
  floor GENERALIZES if: (Q1) no group-a methylator < 25%, AND (Q2) below-floor
  non-methylators are suppressed/correct, AND (Q3) every above-floor organism is
  correctly classified by the RAW engine (guard not even needed there).
  floor is MIS-SET if: a real methylator < 25% (too high) OR an above-floor
  non-methylator is raw-misclassified as a methylation class (too low).

Deterministic; guards imported single-source + sha256-pinned via guards.py.
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..")))  # chapter 14 dir -> guards.py
import guards as G

GC_FLOOR = G.GC_FLOOR


def read_seq(p):
    return "".join(l.strip() for l in open(p) if not l.startswith(">")).upper()


def has_meth_class(regime):
    return ("PLANT" in regime or "VERTEBRATE" in regime or "INSECT_targeted" in regime)


def is_correct(regime, group):
    # group a -> should be a methylation class (PLANT here); group b -> should NOT be
    if group == "a":
        return has_meth_class(regime)
    return not has_meth_class(regime)


def main():
    prov = json.load(open(os.path.join(HERE, "inputs", "_provenance.json")))
    rows = {}
    for o in prov["organisms"]:
        lbl = o["label"]; grp = o["group"]
        seq = read_seq(os.path.join(HERE, "inputs", f"{lbl}.fa"))
        cg, chg, chh = G.bulk_contexts_raw(seq)
        raw = G.detect_regime_raw(cg, chg)
        guarded = G.detect_regime_safe(seq)
        rows[lbl] = {
            "group": grp, "gc": guarded["gc"], "cg_oe": round(cg, 4), "chg_oe": round(chg, 4),
            "raw_regime": raw, "guarded_regime": guarded["regime"], "guard": guarded["guard"],
            "below_floor": guarded["gc"] < GC_FLOOR,
            "raw_correct": is_correct(raw, grp),
            "guarded_correct": is_correct(guarded["regime"], grp),
            "known_biology": o["known_biology"]}

    # Q1: any real methylator (group a) below the floor?
    a_below = [l for l, v in rows.items() if v["group"] == "a" and v["below_floor"]]
    a_min_gc_pct = round(min((v["gc"] for v in rows.values() if v["group"] == "a"), default=0) * 100, 1)
    # Q2: below-floor non-methylators handled?
    b_below = {l: v for l, v in rows.items() if v["group"] == "b" and v["below_floor"]}
    q2_ok = all(v["guarded_correct"] for v in b_below.values())
    # Q3: above-floor organisms correct under the RAW engine (guard not needed)?
    above = {l: v for l, v in rows.items() if not v["below_floor"]}
    q3_raw_fail = [l for l, v in above.items() if not v["raw_correct"]]

    q1_pass = (len(a_below) == 0)
    q2_pass = q2_ok
    q3_pass = (len(q3_raw_fail) == 0)
    floor_generalizes = q1_pass and q2_pass and q3_pass

    # margin: lowest real methylator vs floor
    margin_pts = round(a_min_gc_pct - GC_FLOOR * 100, 1)

    results = {
        "gc_floor": GC_FLOOR, "rows": rows,
        "Q1_falsification_real_methylator_below_floor": {
            "offenders": a_below, "lowest_group_a_GC_pct": a_min_gc_pct,
            "margin_pts_above_floor": margin_pts, "PASS": q1_pass},
        "Q2_below_floor_nonmethylators_handled": {
            "below_floor_group_b": list(b_below), "all_correct": q2_ok, "PASS": q2_pass},
        "Q3_above_floor_raw_engine_correct": {
            "raw_misclassified_above_floor": q3_raw_fail, "PASS": q3_pass},
        "VERDICT": {
            "floor_generalizes_out_of_sample": floor_generalizes,
            "guarded_correct_total": f"{sum(1 for v in rows.values() if v['guarded_correct'])}/{len(rows)}",
            "raw_correct_total": f"{sum(1 for v in rows.values() if v['raw_correct'])}/{len(rows)}"}}

    outp = os.path.join(HERE, "stress_guard_validation_results.json")
    json.dump(results, open(outp, "w"), indent=2, sort_keys=True)

    print("--- out-of-sample organisms (raw vs guarded) ---")
    for lbl, v in sorted(rows.items(), key=lambda kv: kv[1]["gc"]):
        fl = "<FLOOR" if v["below_floor"] else "      "
        rc = "ok" if v["raw_correct"] else "WRONG"
        print(f"{lbl:16}[{v['group']}] GC={v['gc']*100:>4.1f}% {fl} CHG={v['chg_oe']:>5.2f} "
              f"raw={v['raw_regime']:34}({rc:5}) -> guarded={v['guarded_regime']:36}"
              f"{('['+v['guard']+']') if v['guard'] else ''}")
    print()
    print(f"Q1 no real methylator below {GC_FLOOR*100:.0f}%?  lowest group-a GC = {a_min_gc_pct:.1f}% "
          f"(margin +{margin_pts} pts above floor)  -> PASS={q1_pass}")
    print(f"Q2 below-floor non-methylators handled ({list(b_below)})  -> PASS={q2_pass}")
    print(f"Q3 above-floor organisms correct under RAW engine?  raw failures={q3_raw_fail}  -> PASS={q3_pass}")
    print(f"\nVERDICT: floor generalizes out-of-sample = {floor_generalizes}  "
          f"(guarded {results['VERDICT']['guarded_correct_total']} correct)")
    print(f"wrote {outp}")


if __name__ == "__main__":
    main()
