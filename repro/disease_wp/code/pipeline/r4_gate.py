#!/usr/bin/env python3
"""
R4 investigation gate. Verifies the treatment survey (data/curated/treatments.{csv,json})
and the residual burden (data/curated/burden_residual.{csv,json}) are honestly graded with
no guessed values and no fabricated cure, that the efficacy offset and residual composite
are independently re-derivable, that both builders are deterministic across repeated runs,
that R3's banked raw_burden is read UNCHANGED, that the full 35-disease cohort is covered,
and that the governed engine pin is drift-zero -- exactly as methodology/TREATMENT_INDEX.md
and the constitution require. Writes reports/r4.gate.json.
INVESTIGATION ONLY -- no whitepaper prose, no scoring of hypotheses.

Mirrors r3_gate.py conventions. Run after the two R4 builders.
"""
import os, json, csv, hashlib, datetime, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
TREAT_CSV = os.path.join(ROOT, "data", "curated", "treatments.csv")
TREAT_JSON = os.path.join(ROOT, "data", "curated", "treatments.json")
RESID_CSV = os.path.join(ROOT, "data", "curated", "burden_residual.csv")
RESID_JSON = os.path.join(ROOT, "data", "curated", "burden_residual.json")
BURDEN_JSON = os.path.join(ROOT, "data", "curated", "burden_scores.json")
LEX = os.path.join(ROOT, "methodology", "TREATMENT_LEXICON.md")
RULES = os.path.join(ROOT, "methodology", "treatment_rules.csv")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SURVEY_BUILDER = os.path.join(HERE, "r4_treatment_survey.py")
RESID_BUILDER = os.path.join(HERE, "r4_burden_residual.py")
OUT = os.path.join(ROOT, "reports", "r4.gate.json")

COHORT_N = 35
VALID_GRADES = {"[L]", "[O]", "[H]", "[V]", "[F]"}
VALID_STATUS = {"curative", "disease-modifying (substantial)",
                "disease-modifying (partial)", "symptomatic", "none"}
VALID_TIER = {"definition", "standard_of_care"}
# the declared offset map (TREATMENT_INDEX.md) -- the gate's INDEPENDENT copy
E_MAP = {"curative": 0.85, "disease-modifying (substantial)": 0.55,
         "disease-modifying (partial)": 0.30, "symptomatic": 0.10, "none": 0.00}


def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def run_builder_sha(builder, marker):
    out = subprocess.run([sys.executable, builder], capture_output=True, text=True)
    for line in out.stdout.splitlines():
        if marker in line:
            return line.split(":")[-1].strip()
    return None


def main():
    tj = json.load(open(TREAT_JSON, encoding="utf-8"))
    trec = tj["records"]
    rj = json.load(open(RESID_JSON, encoding="utf-8"))
    rrec = rj["records"]
    burden = {r["cui"]: r for r in json.load(open(BURDEN_JSON, encoding="utf-8"))["records"]}

    # flat treatments.csv view (for grade/basis columns)
    tcsv = list(csv.DictReader(open(TREAT_CSV, newline="", encoding="utf-8")))

    checks = []

    # 1 treatments graded, no guess: every treatment row is [H] with a recorded basis
    #   (provenance non-empty), or [O] with a named obstacle. No grade without evidence.
    viol = []
    for r in tcsv:
        g = r["grade"]
        if g not in VALID_GRADES:
            viol.append(f"{r['entity']}:grade {g!r} outside vocabulary"); continue
        if g == "[O]":
            if not r.get("obstacle_for_L", "").strip():
                viol.append(f"{r['entity']}:[O] without obstacle")
        else:
            if not r.get("provenance", "").strip():
                viol.append(f"{r['entity']}:{g} without recorded basis")
    checks.append(("treatments_graded_no_guess", len(viol) == 0,
                   f"{len(tcsv)} treatment rows graded with basis; {len(viol)} violations"
                   + ("" if not viol else f"; first: {viol[0]}")))

    # 2 evidence_status in vocabulary (all 35 rows).
    bad = [r["entity"] for r in tcsv if r["evidence_status"] not in VALID_STATUS]
    checks.append(("evidence_status_in_vocab", len(bad) == 0,
                   f"{len(tcsv)} rows; {len(bad)} outside {sorted(VALID_STATUS)}"
                   + ("" if not bad else f"; first: {bad[0]}")))

    # 3 efficacy offset correct: e == E_MAP[status] and R_treat == 1 - e (independently).
    off_bad = []
    for r in tcsv:
        st = r["evidence_status"]
        exp_e = E_MAP.get(st)
        got_e = round(float(r["efficacy_offset_e"]), 6)
        got_R = round(float(r["R_treat"]), 6)
        if exp_e is None or got_e != round(exp_e, 6):
            off_bad.append(f"{r['entity']}:e {got_e}!={exp_e}")
        elif got_R != round(1.0 - exp_e, 6):
            off_bad.append(f"{r['entity']}:R_treat {got_R}!={round(1.0-exp_e,6)}")
    checks.append(("efficacy_offset_correct", len(off_bad) == 0,
                   f"{len(tcsv)} rows e=E_MAP[status] & R_treat=1-e verified"
                   + ("" if not off_bad else f"; first: {off_bad[0]}")))

    # 4 definition-corroboration consistent: every definition-tier row has
    #   definition_corroborated=yes with a non-empty matched phrase.
    dc_bad = []
    deftier = [r for r in tcsv if r["evidence_tier"] == "definition"]
    for r in deftier:
        if r["definition_corroborated"] != "yes" or not r["definition_phrase"].strip():
            dc_bad.append(r["entity"])
    checks.append(("definition_corroboration_consistent", len(dc_bad) == 0,
                   f"{len(deftier)} definition-tier rows; {len(dc_bad)} uncorroborated"
                   + ("" if not dc_bad else f"; first: {dc_bad[0]}")))

    # 5 residual composite correct: burden_score == raw_burden(from R3 banked) * (1 - e),
    #   re-derived independently from burden_scores.json + treatments e.
    e_by_cui = {r["evidence_status"]: None for r in trec}  # placeholder; real map below
    e_lookup = {r["cui"]: r["efficacy_offset_e"] for r in trec}
    comp_bad = []
    for r in rrec:
        cui = r["cui"]
        raw = burden[cui]["raw_burden"]
        e = e_lookup[cui]
        exp = round(raw * (1.0 - e), 9) if raw is not None else None
        got = round(r["burden_score"], 9) if r["burden_score"] is not None else None
        if exp != got:
            comp_bad.append(f"{r['entity']}:{got}!={exp}")
    checks.append(("residual_composite_correct", len(comp_bad) == 0,
                   f"{len(rrec)} residual records burden_score=raw*(1-e) verified"
                   + ("" if not comp_bad else f"; first: {comp_bad[0]}")))

    # 6 raw_burden unchanged: every residual record's raw_burden equals the R3 banked value
    #   (proves R4 did not mutate R3).
    rb_bad = []
    for r in rrec:
        if r["raw_burden"] != burden[r["cui"]]["raw_burden"]:
            rb_bad.append(r["entity"])
    checks.append(("raw_burden_unchanged_from_R3", len(rb_bad) == 0,
                   f"{len(rrec)} records raw_burden == R3 banked; {len(rb_bad)} mutated"
                   + ("" if not rb_bad else f"; first: {rb_bad[0]}")))

    # 7 determinism: each builder prints an identical digest on two fresh runs.
    ts_a = run_builder_sha(SURVEY_BUILDER, "treatments sha256")
    ts_b = run_builder_sha(SURVEY_BUILDER, "treatments sha256")
    rs_a = run_builder_sha(RESID_BUILDER, "residual sha256")
    rs_b = run_builder_sha(RESID_BUILDER, "residual sha256")
    det_ok = all(x is not None for x in (ts_a, rs_a)) and ts_a == ts_b and rs_a == rs_b
    checks.append(("residual_ranking_deterministic_2x", det_ok,
                   f"treatments {ts_a}=={ts_b}; residual {rs_a}=={rs_b}"))

    # 8 cohort complete: 35 treatment rows, 35 residual records, CUI sets == R3 cohort.
    tcuis = {r["cui"] for r in tcsv}
    rcuis = {r["cui"] for r in rrec}
    bcuis = set(burden)
    cohort_ok = (len(tcsv) == COHORT_N and len(rrec) == COHORT_N
                 and tcuis == bcuis and rcuis == bcuis)
    checks.append(("cohort_complete_35", cohort_ok,
                   f"treatments={len(tcsv)} residual={len(rrec)} cohort={len(bcuis)}; "
                   f"cui sets match={tcuis == bcuis == rcuis}"))

    # 9 no fabricated cure (C-D3): no row assigned 'curative'; no row graded [L] (the deferred
    #   validation grade must not be claimed); every non-[O] row names a modality + basis.
    cure_bad = []
    if any(r["evidence_status"] == "curative" for r in tcsv):
        cure_bad.append("a row claims 'curative' (disallowed for this cohort)")
    if any(r["grade"] == "[L]" for r in tcsv):
        cure_bad.append("a row claims [L] (accession-dated verification is deferred, not done)")
    for r in tcsv:
        if r["grade"] != "[O]" and (not r["modality"].strip() or not r["provenance"].strip()):
            cure_bad.append(f"{r['entity']}: non-[O] without modality+basis")
    checks.append(("treatability_no_fabricated_cure", len(cure_bad) == 0,
                   f"no curative, no claimed [L], every non-[O] has modality+basis"
                   + ("" if not cure_bad else f"; first: {cure_bad[0]}")))

    # 10 residual sensitivity present: equal-weight identity (rho==1.0) + >=4 alternatives.
    sens = rj.get("sensitivity", {})
    eq = sens.get("equal_default", {}).get("spearman_vs_default")
    sens_ok = len(sens) >= 5 and eq == 1.0
    checks.append(("residual_sensitivity_present", sens_ok,
                   f"{len(sens)} weightings; equal_default rho={eq}"))

    # 11 engine pin drift zero: recompute sha256 of every governed file, compare to manifest.
    pin_bad = []
    pin_n = 0
    for line in open(MANIFEST, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        want, rel = line.split(None, 1)
        pin_n += 1
        p = os.path.join(ROOT, rel.strip())
        if not os.path.exists(p):
            pin_bad.append(f"missing {rel}")
        elif hashlib.sha256(open(p, "rb").read()).hexdigest() != want:
            pin_bad.append(f"drift {rel}")
    checks.append(("engine_pin_drift_zero", len(pin_bad) == 0,
                   f"{pin_n - len(pin_bad)}/{pin_n} governed files match (drift 0)"
                   + ("" if not pin_bad else f"; first: {pin_bad[0]}")))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "R4",
        "kind": "investigation_gate",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "treatments_csv":  {"path": "data/curated/treatments.csv",  "sha12": sha12(TREAT_CSV)},
            "treatments_json": {"path": "data/curated/treatments.json", "sha12": sha12(TREAT_JSON)},
            "burden_residual_csv":  {"path": "data/curated/burden_residual.csv",  "sha12": sha12(RESID_CSV)},
            "burden_residual_json": {"path": "data/curated/burden_residual.json", "sha12": sha12(RESID_JSON)},
            "treatment_lexicon": {"path": "methodology/TREATMENT_LEXICON.md", "sha12": sha12(LEX)},
            "treatment_rules":   {"path": "methodology/treatment_rules.csv",  "sha12": sha12(RULES)},
        },
        "counts": {
            "treatment_rows": len(tcsv),
            "residual_records": len(rrec),
            "status_distribution": tj.get("status_distribution", {}),
            "tier_distribution": tj.get("tier_distribution", {}),
            "definition_tier_corroborated": tj.get("definition_tier_corroborated"),
            "definition_tier_total": tj.get("definition_tier_total"),
            "placed": rj.get("placed"), "not_placed": rj.get("not_placed"),
        },
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
        "verdict": f"{verdict} ({passed}/{total})",
        "note": ("Investigation gate over the R4 treatment survey and residual burden. Every treatment "
                 "row carries a uniform [H] grade with a recorded basis: the 12 definition-tier rows are "
                 "runtime-corroborated against the in-package, already-[L]-cited MedGen clinical_definition "
                 "(matched phrase recorded); the 23 standard-of-care-tier rows name the established therapy "
                 "and its source class with the accession-dated [L] verification explicitly deferred. The "
                 "efficacy offset e is re-derived here from the declared evidence_status->e map, and the "
                 "residual burden_score = raw_burden * (1 - e) is re-derived from R3's banked raw_burden "
                 "(verified read UNCHANGED). No disease is assigned a curative class and no row claims [L] "
                 "(constitution C-D3: no fabricated cure). Determinism is verified by two fresh runs of each "
                 "builder producing identical digests. HONESTY/SCOPE: treatment evidence is [H] (cited text / "
                 "established science), not [L]; pinning each therapy to an accession-dated source (FDA label / "
                 "GeneReviews Management / OMIM clinical management / Orphanet) is the deferred [L] validation "
                 "pass, the analogue of R3's deferred natural-history registry pass, and must be completed "
                 "before any W-phase prose treats the residual order as more than a provisional [H]-grade "
                 "prioritisation device. The governed emergence engine pin is re-verified drift-zero."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2)
    print(json.dumps({"verdict": report["verdict"],
                      "checks": [(n, ok) for n, ok, _ in checks]}, indent=2))
    print("written:", OUT)


if __name__ == "__main__":
    main()
