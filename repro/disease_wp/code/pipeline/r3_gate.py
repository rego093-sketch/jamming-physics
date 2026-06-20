#!/usr/bin/env python3
"""
R3 investigation gate. Verifies the reproducible burden ordering
(data/curated/burden_scores.{csv,json}) is component-graded with no guessed
values, applies the declared floor and renormalised-composite rules correctly,
defers treatability to R4, records its weights, is deterministic across repeated
runs, ships a sensitivity pass, and covers the full 35-disease cohort -- exactly
as methodology/BURDEN_INDEX.md requires. Writes reports/r3.gate.json.
INVESTIGATION ONLY -- no whitepaper prose, no scoring of hypotheses.

Mirrors r2_gate.py conventions. Run after code/pipeline/r3_burden_index.py.
"""
import os, json, hashlib, datetime, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CSV  = os.path.join(ROOT, "data", "curated", "burden_scores.csv")
JSON = os.path.join(ROOT, "data", "curated", "burden_scores.json")
LEX  = os.path.join(ROOT, "methodology", "BURDEN_LEXICON.md")
BUILDER = os.path.join(HERE, "r3_burden_index.py")
OUT  = os.path.join(ROOT, "reports", "r3.gate.json")

VALID_GRADES = {"[L]", "[O]", "[H]", "[V]", "[F]"}
GRADE_RANK   = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3, "[F]": 4}  # floor order O<H<L<V<F
AXES = ["O", "P", "S", "M", "D"]
COHORT_N = 35
RANK_MIN_AXES = 3


def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def graded_ok(obj):
    """A component must be {value, grade, source|obstacle}: grade in vocabulary,
    [O] names an obstacle, [L]/[H]/[V] cite a source. No grade without evidence."""
    if not isinstance(obj, dict):
        return False, "not a graded object"
    if "value" not in obj:
        return False, "missing value key"
    g = obj.get("grade")
    if g not in VALID_GRADES:
        return False, f"grade {g!r} outside vocabulary"
    if g == "[O]":
        if not str(obj.get("obstacle", "")).strip():
            return False, "[O] without named obstacle"
    else:
        if not str(obj.get("source", "")).strip():
            return False, f"{g} without cited source"
    return True, ""


def floor(grades):
    gs = [g for g in grades if g in GRADE_RANK]
    return min(gs, key=lambda g: GRADE_RANK[g]) if gs else "[O]"


def run_builder_sha():
    """Execute the builder and return the burden-set sha it prints."""
    out = subprocess.run([sys.executable, BUILDER], capture_output=True, text=True)
    for line in out.stdout.splitlines():
        if "burden-set sha256" in line:
            return line.split(":")[-1].strip()
    return None


def main():
    payload = json.load(open(JSON, encoding="utf-8"))
    records = payload["records"]
    checks = []

    # 1 components graded, no guessed values: every axis of every record is a
    #   {value, grade, source|obstacle} object with a vocabulary grade + evidence.
    viol = []
    for r in records:
        for ax in AXES:
            ok, why = graded_ok(r["components"].get(ax, {}))
            if not ok:
                viol.append(f"{r['entity']}:{ax}:{why}")
    checks.append(("components_graded_no_guess", len(viol) == 0,
                   f"{len(records)*len(AXES)} components; {len(viol)} graded-field violations"
                   + ("" if not viol else f"; first: {viol[0]}")))

    # 2 floor rule correct: stored grade_floor == min over ALL 5 axis grades (missing -> [O]);
    #   grade_present == floor over the SCORED axes only.
    floor_bad = []
    for r in records:
        all_g  = [r["components"][ax]["grade"] for ax in AXES]
        pres_g = [r["components"][ax]["grade"] for ax in AXES
                  if r["components"][ax]["value"] is not None]
        exp_floor   = floor(all_g)
        exp_present = floor(pres_g) if pres_g else "[O]"
        if r["raw_burden_grade_floor"] != exp_floor:
            floor_bad.append(f"{r['entity']}:floor {r['raw_burden_grade_floor']}!={exp_floor}")
        if r["raw_burden_grade_present"] != exp_present:
            floor_bad.append(f"{r['entity']}:present {r['raw_burden_grade_present']}!={exp_present}")
    checks.append(("floor_rule_correct", len(floor_bad) == 0,
                   f"{len(records)} records floor/present-grade verified"
                   + ("" if not floor_bad else f"; {len(floor_bad)} mismatch, first: {floor_bad[0]}")))

    # 3 composite rule correct: raw_burden == renormalised mean of present axis values
    #   (missing excluded, not imputed); null iff no axis scored.
    comp_bad = []
    for r in records:
        vals = [r["components"][ax]["value"] for ax in AXES
                if r["components"][ax]["value"] is not None]
        exp = round(sum(vals) / len(vals), 12) if vals else None
        got = round(r["raw_burden"], 12) if r["raw_burden"] is not None else None
        if exp != got:
            comp_bad.append(f"{r['entity']}:{got}!={exp}")
    checks.append(("composite_renormalised_mean", len(comp_bad) == 0,
                   f"{len(records)} records raw_burden = mean(present axes) verified"
                   + ("" if not comp_bad else f"; first: {comp_bad[0]}")))

    # 4 treatability deferred to R4: every record R_treat == 1.0, grade [O], obstacle names R4.
    treat_bad = []
    for r in records:
        t = r["treatability"]
        if t.get("value") != 1.0 or t.get("grade") != "[O]" or "r4" not in str(t.get("obstacle", "")).lower():
            treat_bad.append(r["entity"])
    checks.append(("treatability_deferred_R4", len(treat_bad) == 0,
                   f"{len(records)-len(treat_bad)}/{len(records)} records defer R_treat=1.0 [O] to R4"))

    # 5 weights recorded and normalised.
    W = payload.get("weights_default", {})
    w_ok = set(W) == set(AXES) and abs(sum(W.values()) - 1.0) < 1e-9
    checks.append(("weights_recorded", w_ok,
                   f"weights={W}; sum={round(sum(W.values()),6) if W else None}"))

    # 6 ranking deterministic: builder prints an identical burden-set sha on two fresh runs.
    sha_a = run_builder_sha()
    sha_b = run_builder_sha()
    det_ok = sha_a is not None and sha_a == sha_b
    checks.append(("ranking_deterministic_2x", det_ok,
                   f"run1={sha_a} run2={sha_b}"))

    # 7 sensitivity present: >=4 alternative weightings + equal-weight identity (rho==1.0).
    sens = payload.get("sensitivity", {})
    eq = sens.get("equal_default", {}).get("spearman_vs_default")
    sens_ok = len(sens) >= 5 and eq == 1.0
    checks.append(("sensitivity_present", sens_ok,
                   f"{len(sens)} weightings; equal_default rho={eq}"))

    # 8 cohort complete: exactly 35 records.
    checks.append(("cohort_complete_35", len(records) == COHORT_N,
                   f"records={len(records)} expected={COHORT_N}"))

    # 9 rankability consistent: rankable iff axes_scored>=3; placed have int rank (contiguous
    #   1..N, raw_burden non-increasing); not-placed have rank null.
    rk_bad = []
    placed = [r for r in records if r["rankable"]]
    notpl  = [r for r in records if not r["rankable"]]
    for r in records:
        if r["rankable"] != (r["axes_scored"] >= RANK_MIN_AXES):
            rk_bad.append(f"{r['entity']}:flag!=({r['axes_scored']}>={RANK_MIN_AXES})")
    if [r["rank"] for r in placed] != list(range(1, len(placed) + 1)):
        rk_bad.append("placed ranks not contiguous 1..N")
    if any(r["rank"] is not None for r in notpl):
        rk_bad.append("not-placed has non-null rank")
    rb = [r["raw_burden"] for r in placed]
    if any(a is not None and b is not None and a < b - 1e-12 for a, b in zip(rb, rb[1:])):
        rk_bad.append("placed raw_burden not non-increasing")
    checks.append(("rankability_consistent", len(rk_bad) == 0,
                   f"placed={len(placed)} not_placed={len(notpl)} (rule: >= {RANK_MIN_AXES} axes)"
                   + ("" if not rk_bad else f"; first: {rk_bad[0]}")))

    passed = sum(1 for _, ok, _ in checks if ok)
    total  = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "R3",
        "kind": "investigation_gate",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_csv":  {"path": "data/curated/burden_scores.csv",  "sha12": sha12(CSV)},
            "burden_scores_json": {"path": "data/curated/burden_scores.json", "sha12": sha12(JSON)},
            "burden_lexicon":     {"path": "methodology/BURDEN_LEXICON.md",   "sha12": sha12(LEX)},
        },
        "counts": {
            "records": len(records),
            "rankable_placed": len(placed),
            "not_placed": len(notpl),
            "axis_grade_coverage": payload.get("axis_grade_coverage", {}),
        },
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
        "verdict": f"{verdict} ({passed}/{total})",
        "note": ("Investigation gate over the R3 burden ordering. Every disease carries five graded "
                 "burden components {value, grade, source|obstacle}; no grade appears without its "
                 "evidence (cited source for [L]/[H], named obstacle for [O]). The composite is the "
                 "renormalised mean of the axes actually scored (missing axes excluded, never imputed); "
                 "its floor grade is the min over all five axis grades (any missing axis -> [O]), and a "
                 "second grade_present floors over the scored axes only. Treatability is deferred to R4 "
                 "(R_treat=1.0, [O]); the primary order is the pre-treatment raw_burden. Determinism is "
                 "verified here by two fresh builder runs producing an identical burden-set digest. Only "
                 "majority-coverage diseases (>=3 of 5 axes) are placed in the order; sparser diseases "
                 "are reported with rank=null. SCOPE/HONESTY: four of five axes (P,S,M,D) are, for most "
                 "diseases, inferences from the cited MedGen definition ([H]) because the HPO clinical-"
                 "course/mortality branches are sparse; the order is therefore an [H]-grade provisional "
                 "prioritisation device, not a registry-locked ranking. A dedicated natural-history "
                 "registry pass (Orphanet/OMIM clinical synopsis, survival literature) to lift these to "
                 "[L]/[V] is recommended before any W-phase prose locks the order (see R3 handover)."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w"), indent=2)
    print(json.dumps({"verdict": report["verdict"], "counts": {
        "records": len(records), "placed": len(placed), "not_placed": len(notpl)},
        "checks": [(n, ok) for n, ok, _ in checks]}, indent=2))
    print("written:", OUT)


if __name__ == "__main__":
    main()
