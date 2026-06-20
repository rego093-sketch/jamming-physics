#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R7 gate -- verifies the open-source natural-history pass (GBD disability weights +
PMC survival) independently of any recorded digest. Re-derives composites,
rankability, residual and the order lock; re-parses the pinned GBD disability-
weights PDF and reproduces the GBD2013-column anchors; confirms every D lift is a
cited, entity-anchored GBD-health-state join binned by the a-priori cut-points;
re-verifies each PMC mortality corroboration against the cached article text;
confirms S/P are not lifted (no open source); confirms the R3/R4 BANKED files stay
byte-identical and the engine pin is drift-zero; and proves the r5->r6->r7 chain is
deterministic (2x identical).

Living code, NOT in the frozen engine pin.
Out: reports/r7.gate.json
"""
import os, re, csv, json, sys, hashlib, subprocess, importlib.util, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
GBD = os.path.join(ROOT, "data", "raw", "gbd")
LITS = os.path.join(ROOT, "data", "raw", "litsurvival")
OMIM = os.path.join(ROOT, "data", "raw", "omim")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
RESID_J = os.path.join(CUR, "burden_residual_registry.json")
RESID_C = os.path.join(CUR, "burden_residual_registry.csv")
R5 = os.path.join(HERE, "r5_accession_apply.py")
R6 = os.path.join(HERE, "r6_naturalhistory_registry.py")
R7 = os.path.join(HERE, "r7_naturalhistory_registry2.py")
GBD_FETCH = os.path.join(HERE, "r7_gbd_dw_fetch.py")

BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
}
GBD_PDF_PIN = "c7d22442bad82f7ff5a0b63353a6591d769d2d88a959a5c2bac960ede179bdf4"
ANCHORS = {  # GBD2013 (left) value that the parse must reproduce; GBD2010 (right) for contrast
    "Anemia: severe": (0.149, 0.164), "Anemia: moderate": (0.052, 0.058),
    "Motor impairment: severe": (0.402, 0.377),
    "Musculoskeletal problems: generalised, moderate": (0.317, 0.292),
    "Intellectual disability: severe": (0.160, 0.135),
    "Motor plus cognitive impairments: severe": (0.542, 0.453),
}
CUTPOINTS_DECL = {"dw<0.10": 0.2, "0.10<=dw<0.30": 0.5, "0.30<=dw<=0.55": 0.75, "dw>0.55": 1.0}
GR = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3}
W = ["O", "P", "S", "M", "D"]


def dw_to_tier(dw):
    if dw < 0.10:
        return 0.2
    if dw < 0.30:
        return 0.5
    if dw <= 0.55:
        return 0.75
    return 1.0


# --- PMC corroboration re-verification (identical patterns to the apply stage) ---
DOT = "\u2024"
ABBR = ["e.g.", "i.e.", "vs.", "cf.", "al.", "Dr.", "approx.", "no.", "Fig.", "ca."]
SIG = re.compile(r"\b(median survival|life expectanc|lifespan|life span|survival rate|"
                 r"\d+-year survival|age of death|die[ds]? (?:at|by|in|before|during)|"
                 r"fatal|lethal|premature death|reduced (?:life|surviv)|"
                 r"normal (?:life|lifespan|survival)|shortened (?:life|surviv))\b", re.I)
NUM = re.compile(r"\b\d{1,3}(?:\.\d+)?\s*(?:year|yr|month|week|day|decade)s?\b", re.I)
AGEWORD = re.compile(r"\b(in utero|neonat|perinat|infancy|early infancy|childhood)\b", re.I)
EXCLUDE = re.compile(r"\b(assum|model|qaly|hazard ratio|transplant|operative|interquartile|"
                     r"recipient|post-?operative|follow-up|surgical|surgery|stimulation test|"
                     r"growth hormone|parkinson|cohort of hospitalised|cohort of hospitalized|"
                     r"recruited|participants (?:were|between)|underwent)\b", re.I)


def mortality_direction(sent):
    s = sent.lower()
    if re.search(r"normal life ?expectanc|not reduced|does not (?:affect|reduce) (?:life|lifespan)|"
                 r"normal lifespan|normal survival", s):
        return ("normal", 0.0)
    if (re.search(r"\b(in utero|neonat|perinat)\b", s) and re.search(r"fatal|lethal|death|die", s)) \
       or re.search(r"fatal .*(?:infancy|childhood)|death .*(?:infancy|childhood)", s) \
       or re.search(r"(?:lifespan|survival) .*under (?:5|6|7|8|9|10) years", s) \
       or re.search(r"under (?:5|6|7|8|9|10) years\b.*(?:lifespan|survival|life)", s):
        return ("early_lethal", 1.0)
    if re.search(r"slightly reduced|mildly reduced|marginally reduced", s):
        return ("qualified", 0.4)
    if re.search(r"reduced (?:life ?expectanc|lifespan|survival)|premature death|shortened (?:life|lifespan)|"
                 r"median survival", s):
        return ("reduced", 0.7)
    return None


def m_band_agrees(banked_v, cand_tier):
    bands = {0.0: {0.0}, 0.4: {0.0, 0.4, 0.7}, 0.7: {0.4, 0.7, 1.0}, 1.0: {0.7, 1.0}}
    return cand_tier in bands.get(banked_v, set())


def sentences(t):
    s = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + DOT + m.group(2), t)
    for a in ABBR:
        s = s.replace(a, a.replace(".", DOT))
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\u2022])", s)
    return [p.replace(DOT, ".").strip() for p in parts]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sha12(p):
    return sha(p)[:12] if os.path.exists(p) else None


def run(stage):
    subprocess.run([sys.executable, stage], check=True, stdout=subprocess.DEVNULL)


def registry_set_sha():
    h = hashlib.sha256()
    for p in (SCORES_C, SCORES_J, RESID_C, RESID_J):
        h.update(open(p, "rb").read())
    return h.hexdigest()[:12]


def axis_state(payload):
    st = {}
    for r in payload["records"]:
        st[r["cui"]] = {ax: (r["components"][ax]["value"], r["components"][ax]["grade"],
                             r["components"][ax].get("source", ""))
                        for ax in W}
    return st


def parse_gbd_table():
    """Re-parse the pinned PDF (via the fetch stage) and return the weights dict."""
    run(GBD_FETCH)
    return json.load(open(os.path.join(GBD, "gbd_disability_weights.json")))["weights"]


def main():
    checks = []

    # ---- 1) determinism: r5 -> r6 -> r7 chain twice -> identical registry-set sha ----
    run(R5); run(R6); run(R7); s1 = registry_set_sha()
    run(R5); run(R6); run(R7); s2 = registry_set_sha()
    checks.append(("determinism_chain_2x", s1 == s2,
                   f"r5->r6->r7 chain registry-set sha {s1} == {s2}"))

    # capture R6 base then R7 for add-only / supersede comparison
    run(R5); run(R6); r6_payload = json.load(open(SCORES_J)); r6_state = axis_state(r6_payload)
    run(R7); P = json.load(open(SCORES_J)); r7_state = axis_state(P)
    recs = P["records"]
    resid = json.load(open(RESID_J))
    cohort_cuis = {r["cui"] for r in recs}

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = (float(r["efficacy_offset_e"]), float(r["R_treat"]), r["grade"])

    # ---- 2) banked R3/R4 byte-identical ----
    bad_bank = [f for f, want in BANKED_PINS.items() if sha(os.path.join(CUR, f)) != want]
    checks.append(("banked_unchanged", not bad_bank,
                   "burden_scores/burden_residual/treatments banked digests unchanged"
                   + ("" if not bad_bank else f"; CHANGED: {bad_bank}")))

    # ---- 3) GBD source pinned + anchors reproduce GBD2013 column ----
    pdf_ok = os.path.exists(os.path.join(GBD, "salomon2015_mmc1.pdf")) and \
        sha(os.path.join(GBD, "salomon2015_mmc1.pdf")) == GBD_PDF_PIN
    dw_table = parse_gbd_table()
    anchor_bad = []
    for st, (want13, gbd10) in ANCHORS.items():
        got = dw_table.get(st, {}).get("dw2013")
        if got is None or abs(got - want13) > 1e-9:
            anchor_bad.append(f"{st}={got} (want {want13})")
    checks.append(("gbd_source_pinned_anchored", pdf_ok and not anchor_bad and len(dw_table) > 100,
                   f"PDF sha==pin; {len(ANCHORS) - len(anchor_bad)}/{len(ANCHORS)} GBD2013 anchors reproduced; "
                   f"{len(dw_table)} states parsed"))

    # ---- 4) GBD join entity-anchored + cited + tier from a-priori cut-points ----
    join_rows = {r["cui"]: r for r in csv.DictReader(open(os.path.join(METH, "gbd_dw_join.csv"), newline=""))}
    excl_rows = {r["cui"]: r for r in csv.DictReader(open(os.path.join(METH, "gbd_dw_excluded.csv"), newline=""))}
    join_bad = []
    for cui, jr in join_rows.items():
        if cui not in cohort_cuis:
            join_bad.append(f"{cui} not in cohort"); continue
        st = jr["gbd_health_state"]
        if st not in dw_table:
            join_bad.append(f"{jr['entity']} state {st!r} not in DW table"); continue
        if not jr.get("evidence_basis", "").strip():
            join_bad.append(f"{jr['entity']} no evidence_basis")
        if not jr.get("dominant_untreated_sequela", "").strip():
            join_bad.append(f"{jr['entity']} no sequela rationale")
        if cui in excl_rows:
            join_bad.append(f"{cui} in BOTH join and excluded")
    # audit block must mirror the join and bind the correct tier
    audit = {a["cui"]: a for a in P["gbd_disability_join"]}
    for cui, jr in join_rows.items():
        if cui not in audit:
            join_bad.append(f"{jr['entity']} missing from gbd_disability_join audit"); continue
        a = audit[cui]
        dw = dw_table[jr["gbd_health_state"]]["dw2013"]
        if abs(a["dw2013"] - dw) > 1e-9:
            join_bad.append(f"{jr['entity']} audit dw {a['dw2013']} != table {dw}")
        if abs(a["disability_tier"] - dw_to_tier(dw)) > 1e-9:
            join_bad.append(f"{jr['entity']} audit tier != cut-point tier")
    checks.append(("gbd_join_anchored_cited", not join_bad,
                   f"{len(join_rows)} GBD joins: cui in cohort, state in pinned DW table, evidence_basis + "
                   f"sequela present, tier from a-priori cut-points ({len(join_bad)} bad)"))

    # ---- 5) a-priori disability cut-points + every GBD-sourced D == cut-point tier ----
    cut_ok = {k: float(v) for k, v in P["disability_tier_cutpoints"].items()} == CUTPOINTS_DECL
    dcut_bad = []
    for r in recs:
        d = r["components"]["D"]
        if d["grade"] == "[L]" and "GBD" in (d.get("source", "")):
            if r["cui"] in join_rows:
                dw = dw_table[join_rows[r["cui"]]["gbd_health_state"]]["dw2013"]
                # corroboration of an existing [L] keeps max(prior, tier); fills/supersedes == tier
                want = dw_to_tier(dw)
                if d["value"] not in (want, max(want, r6_state[r["cui"]]["D"][0] or 0.0)):
                    dcut_bad.append(f"{r['entity']} D={d['value']} != cut-point tier {want}")
    checks.append(("disability_cutpoints_a_priori", cut_ok and not dcut_bad,
                   f"declared cut-points match fixed map; every GBD-sourced D == binned tier ({len(dcut_bad)} bad)"))

    # ---- 6) excluded set recorded, in cohort, not lifted to [L] via GBD ----
    excl_bad = []
    for cui, er in excl_rows.items():
        if cui not in cohort_cuis:
            excl_bad.append(f"{cui} not in cohort")
        if not er.get("exclusion_reason", "").strip():
            excl_bad.append(f"{cui} no reason")
        r = next((x for x in recs if x["cui"] == cui), None)
        if r and "GBD disability weight:" in (r["components"]["D"].get("source", "") or ""):
            excl_bad.append(f"{er['entity']} excluded but D lifted via GBD")
    checks.append(("gbd_excluded_recorded", not excl_bad,
                   f"{len(excl_rows)} declined mappings: in cohort, reason present, D not GBD-lifted ({len(excl_bad)} bad)"))

    # ---- 7) add-only: no grade weakened, no scored value removed, vs R6 ----
    downgrade = []
    for cui in r7_state:
        for ax in W:
            v6, g6, _ = r6_state[cui][ax]; v7, g7, _ = r7_state[cui][ax]
            if GR[g7] < GR[g6]:
                downgrade.append(f"{cui}/{ax} {g6}->{g7}")
            if v6 is not None and v7 is None:
                downgrade.append(f"{cui}/{ax} value dropped")
    checks.append(("addonly_no_downgrade", not downgrade,
                   f"no axis grade weakened and no scored value removed vs R6 ({len(downgrade)} violations)"))

    # ---- 8) supersede/corroborate only: D value changes are GBD-[L]-backed; existing-[L] D only rises;
    #         M values unchanged vs R6 ----
    sup_bad = []
    for cui in r7_state:
        # D
        v6, g6, _ = r6_state[cui]["D"]; v7, g7, s7 = r7_state[cui]["D"]
        if v6 != v7:
            if not (g7 == "[L]" and "GBD" in s7):
                sup_bad.append(f"{cui}/D {v6}->{v7} without GBD [L] backing")
            if g6 == "[L]" and v6 is not None and v7 < v6:
                sup_bad.append(f"{cui}/D existing-[L] value decreased {v6}->{v7}")
        # M values must not change (corroboration is grade/source only)
        mv6 = r6_state[cui]["M"][0]; mv7 = r7_state[cui]["M"][0]
        if mv6 != mv7:
            sup_bad.append(f"{cui}/M value changed {mv6}->{mv7} (corroboration must not move value)")
    checks.append(("supersede_corroborate_only", not sup_bad,
                   f"D changes GBD-[L]-backed & existing-[L] D non-decreasing; M values unchanged ({len(sup_bad)} bad)"))

    # ---- 9) PMC mortality corroborations re-verified against cached text ----
    corr_bad = []
    filled_o = 0
    rec_corr = P["pmc_mortality_corroborations"]
    for c in rec_corr:
        path = os.path.join(LITS, f"{c['cui']}.json")
        if not os.path.exists(path):
            corr_bad.append(f"{c['entity']} no cache"); continue
        art = json.load(open(path))
        if art.get("pmcid") != c["pmcid"]:
            corr_bad.append(f"{c['entity']} pmcid mismatch")
        if c["sentence"] not in art.get("text", ""):
            corr_bad.append(f"{c['entity']} sentence not in cached text")
        s = c["sentence"]
        if EXCLUDE.search(s) or not SIG.search(s) or not (NUM.search(s) or AGEWORD.search(s)):
            corr_bad.append(f"{c['entity']} sentence fails signal/exclude filter")
        d = mortality_direction(s)
        if not d or not m_band_agrees(c["banked_value"], d[1]):
            corr_bad.append(f"{c['entity']} direction disagrees with banked band")
    # no [O] mortality may have been filled by PMC
    for cui in r7_state:
        if r6_state[cui]["M"][1] == "[O]" and r7_state[cui]["M"][1] != "[O]":
            filled_o += 1
    checks.append(("pmc_corroboration_verified", not corr_bad and filled_o == 0,
                   f"{len(rec_corr)} PMC corroborations verified in cached text (signal+exclude+direction); "
                   f"0 [O] mortality filled from free text ({len(corr_bad)} bad, {filled_o} illicit fills)"))

    # ---- 10) S / P not lifted (no open structured source) ----
    sp_bad = []
    for cui in r7_state:
        for ax in ("S", "P"):
            if (r6_state[cui][ax][0], r6_state[cui][ax][1]) != (r7_state[cui][ax][0], r7_state[cui][ax][1]):
                sp_bad.append(f"{cui}/{ax} changed")
    checks.append(("s_p_not_lifted", not sp_bad,
                   f"S and P axis value+grade identical to R6 (no open source; obstacle-only) ({len(sp_bad)} changed)"))

    # ---- 11) OMIM skip recorded ----
    omim_log = json.load(open(os.path.join(OMIM, "_fetch_log.json")))
    omim_ok = omim_log.get("status") == "SKIPPED" and "OMIM_API_KEY" in omim_log.get("obstacle", "")
    checks.append(("omim_skip_recorded", omim_ok,
                   f"OMIM clinical-synopsis pass status = {omim_log.get('status')} (obstacle named, S not guessed)"))

    # ---- 12) raw_burden re-derived ----
    raw_bad = []
    for r in recs:
        present = [r["components"][ax]["value"] for ax in W if r["components"][ax]["value"] is not None]
        exp = (sum(present) / len(present)) if present else None
        got = r["raw_burden"]
        if (exp is None) != (got is None) or (exp is not None and abs(exp - got) > 1e-9):
            raw_bad.append(r["entity"])
    checks.append(("raw_burden_rederived", not raw_bad,
                   f"renormalised-mean recompute matches stored raw_burden ({len(raw_bad)} mismatch)"))

    # ---- 13) rankability + promotions ----
    rank_bad = [r["entity"] for r in recs if r["rankable"] != (r["axes_scored"] >= 3)]
    banked = {x["cui"]: x for x in json.load(open(os.path.join(CUR, "burden_scores.json")))["records"]}
    promo_calc = sorted(r["cui"] for r in recs if r["rankable"] and not banked[r["cui"]]["rankable"])
    promo_rec = sorted(p["cui"] for p in P["promotions_from_not_placed"])
    checks.append(("rankability_and_promotions", not rank_bad and promo_calc == promo_rec,
                   f"rankable == (axes>=3) for all ({len(rank_bad)} bad); promotions recompute matches "
                   f"({len(promo_rec)} promoted)"))

    # ---- 14) residual correct ----
    res_bad = []
    for r in recs:
        if r["raw_burden"] is None:
            continue
        e, Rt, _ = treat.get(r["cui"], (0.0, 1.0, "[O]"))
        exp = round(r["raw_burden"] * round(Rt, 12), 12)
        if abs(exp - r["burden_score"]) > 1e-9:
            res_bad.append(r["entity"])
    placed_res = [x for x in resid["records"] if x["rankable"]]
    mono = all(placed_res[i]["burden_score"] >= placed_res[i + 1]["burden_score"] - 1e-12
               for i in range(len(placed_res) - 1))
    checks.append(("residual_correct", not res_bad and mono,
                   f"burden_score == raw*(1-e) ({len(res_bad)} bad); residual order monotone non-increasing"))

    # ---- 15) order lock rule + sensitivity ----
    lock_bad, lock_n = [], 0
    for r in recs:
        present = [r["components"][ax]["grade"] for ax in W if r["components"][ax]["value"] is not None]
        exp = bool(r["rankable"] and present and all(GR[g] >= GR["[L]"] for g in present))
        if exp != r["order_locked"]:
            lock_bad.append(r["entity"])
        lock_n += int(r["order_locked"])
    sens = P["sensitivity"]
    eq = sens.get("equal_default", {}).get("spearman_vs_default")
    checks.append(("order_lock_and_sensitivity", not lock_bad and eq == 1.0 and len(sens) >= 5,
                   f"order_locked rule holds ({lock_n} locked; {len(lock_bad)} bad); {len(sens)} weightings, "
                   f"equal_default rho={eq}"))

    # ---- 16) engine pin drift zero ----
    pin_bad, pin_n = [], 0
    for line in open(MANIFEST, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        want, rel = line.split(None, 1); pin_n += 1
        p = os.path.join(ROOT, rel.strip())
        if not os.path.exists(p):
            pin_bad.append(f"missing {rel}")
        elif sha(p) != want:
            pin_bad.append(f"drift {rel}")
    checks.append(("engine_pin_drift_zero", not pin_bad,
                   f"{pin_n - len(pin_bad)}/{pin_n} governed files match (drift 0)"))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "R7", "kind": "investigation_gate",
        "title": "open-source natural-history pass (GBD disability weights + PMC survival) — D lift / M corroboration",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
            "burden_scores_registry_csv": {"path": "data/curated/burden_scores_registry.csv", "sha12": sha12(SCORES_C)},
            "burden_residual_registry_json": {"path": "data/curated/burden_residual_registry.json", "sha12": sha12(RESID_J)},
            "gbd_dw_pdf": {"path": "data/raw/gbd/salomon2015_mmc1.pdf", "sha12": sha12(os.path.join(GBD, "salomon2015_mmc1.pdf"))},
            "gbd_dw_table": {"path": "data/raw/gbd/gbd_disability_weights.json", "sha12": sha12(os.path.join(GBD, "gbd_disability_weights.json"))},
            "litsurvival_log": {"path": "data/raw/litsurvival/_fetch_log.json", "sha12": sha12(os.path.join(LITS, "_fetch_log.json"))},
            "omim_log": {"path": "data/raw/omim/_fetch_log.json", "sha12": sha12(os.path.join(OMIM, "_fetch_log.json"))},
        },
        "lift_counts": P.get("lift_counts"),
        "axis_grade_coverage_registry": P.get("axis_grade_coverage_registry"),
        "gbd_disability_join": P.get("gbd_disability_join"),
        "gbd_excluded": P.get("gbd_excluded"),
        "pmc_mortality_corroborations": P.get("pmc_mortality_corroborations"),
        "promotions": P.get("promotions_from_not_placed"),
        "order_locked": P.get("order_locked_diseases"),
        "registry_set_sha12": registry_set_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "r7.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"R7 GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:28s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
