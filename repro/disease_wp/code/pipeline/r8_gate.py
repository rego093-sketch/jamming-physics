#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R8 gate -- verifies the open-source SEVERITY pass independently of any recorded
digest. It:
  * proves the r5->r6->r7->r8 chain is deterministic (2x identical registry-set sha);
  * re-anchors every severity-join row in the PINNED phenotype.hpoa (the cited
    phenotype + Severity modifier + frequency + reference must be re-found under one
    of the record's OMIM phenotype MIMs) and confirms the audit binds the a-priori
    modifier->tier cut-point;
  * confirms every declined annotation is recorded with a per-disease reason and did
    NOT lift that disease's S to [L];
  * confirms add-only (no grade weakened / no scored value removed vs the R7 base)
    and that the ONLY axis touched by R8 is S, changed ONLY for joined diseases
    (zero illicit S lifts; O/P/M/D byte-identical to R7);
  * proves the new order-lock: Achondrogenesis type II becomes order_locked at R8
    (it was NOT at R7), taking the locked count 1 -> 2;
  * re-derives composites/rankability/residual/order-lock-rule/sensitivity;
  * confirms the OMIM clinical-synopsis path is recorded as REMOVED (API key
    unobtainable for an individual researcher), not used;
  * confirms the R3/R4 BANKED files stay byte-identical and the engine pin is
    drift-zero.

Living code, NOT in the frozen engine pin.  Out: reports/r8.gate.json
"""
import os, re, csv, json, sys, gzip, hashlib, subprocess, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
HPO = os.path.join(ROOT, "data", "raw", "hpo")
HPOA = os.path.join(HPO, "phenotype.hpoa.gz")
OMIM = os.path.join(ROOT, "data", "raw", "omim")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
RESID_J = os.path.join(CUR, "burden_residual_registry.json")
RESID_C = os.path.join(CUR, "burden_residual_registry.csv")
R5 = os.path.join(HERE, "r5_accession_apply.py")
R6 = os.path.join(HERE, "r6_naturalhistory_registry.py")
R7 = os.path.join(HERE, "r7_naturalhistory_registry2.py")
R8 = os.path.join(HERE, "r8_severity_registry.py")

BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
}
# a-priori HPO Severity-modifier -> S tier (must match the builder's declared map)
SEV_TIER_DECL = {"HP:0012825 Mild": 0.25, "HP:0012826 Moderate": 0.5,
                 "HP:0012828 Severe": 0.75, "HP:0012829 Profound": 1.0,
                 "HP:0012827 Borderline": None}
MOD_TIER = {"HP:0012825": 0.25, "HP:0012826": 0.5, "HP:0012828": 0.75, "HP:0012829": 1.0}
OBLIGATE_TERM = "HP:0040280"


def is_obligate(freq):
    import re as _re
    f = (freq or "").strip()
    if OBLIGATE_TERM in f or f in ("100%", "1/1"):
        return True
    m = _re.fullmatch(r"(\d+)\s*/\s*(\d+)", f)
    if m and int(m.group(1)) == int(m.group(2)) and int(m.group(2)) > 0:
        return True
    m = _re.fullmatch(r"(\d+(?:\.\d+)?)%", f)
    return bool(m and abs(float(m.group(1)) - 100.0) < 1e-9)
GR = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3}
W = ["O", "P", "S", "M", "D"]


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


def lock_state(payload):
    return {r["cui"]: bool(r.get("order_locked")) for r in payload["records"]}


def parse_hpoa():
    """independent re-parse: (OMIM_mim, hpo_id) -> list of (modifier, frequency, reference); + sha."""
    idx = collections.defaultdict(list)
    s = sha(HPOA)
    with gzip.open(HPOA, "rt") as f:
        header = None
        for line in f:
            if line.startswith("#"):
                continue
            if header is None:
                header = line.rstrip("\n").split("\t")
                ci = {c: i for i, c in enumerate(header)}
                continue
            p = line.rstrip("\n").split("\t")
            if not p[ci["database_id"]].startswith("OMIM:"):
                continue
            mim = p[ci["database_id"]].split(":")[1]
            idx[(mim, p[ci["hpo_id"]])].append(
                (p[ci["modifier"]], p[ci["frequency"]].strip(), p[ci["reference"]].strip()))
    return idx, s


def main():
    checks = []

    # ---- 1) determinism: r5 -> r6 -> r7 -> r8 chain twice -> identical registry-set sha ----
    run(R5); run(R6); run(R7); run(R8); s1 = registry_set_sha()
    run(R5); run(R6); run(R7); run(R8); s2 = registry_set_sha()
    checks.append(("determinism_chain_2x", s1 == s2,
                   f"r5->r6->r7->r8 chain registry-set sha {s1} == {s2}"))

    # capture R7 base (pre-severity), then R8
    run(R5); run(R6); run(R7); P7 = json.load(open(SCORES_J))
    r7_state = axis_state(P7); r7_lock = lock_state(P7)
    run(R8); P = json.load(open(SCORES_J)); r8_state = axis_state(P); r8_lock = lock_state(P)
    recs = P["records"]
    resid = json.load(open(RESID_J))
    cohort_cuis = {r["cui"] for r in recs}
    rec_by_cui = {r["cui"]: r for r in recs}

    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = (float(r["efficacy_offset_e"]), float(r["R_treat"]), r["grade"])

    # ---- 2) banked R3/R4 byte-identical ----
    bad_bank = [f for f, want in BANKED_PINS.items() if sha(os.path.join(CUR, f)) != want]
    checks.append(("banked_unchanged", not bad_bank,
                   "burden_scores/burden_residual/treatments banked digests unchanged"
                   + ("" if not bad_bank else f"; CHANGED: {bad_bank}")))

    # ---- 3) R8 builds on a real R7 base ----
    passes = P.get("registry_passes", [])
    base_ok = passes[-1] == "R8_open_severity" and "R7_open_naturalhistory" in passes \
        and "R6_orphanet_natural_history" in passes
    checks.append(("cumulative_over_r7", base_ok,
                   f"registry_passes = {passes}"))

    # ---- 4) severity join re-anchored in the PINNED hpoa + cited + a-priori tier ----
    hpoa_idx, hpoa_sha = parse_hpoa()
    join_rows = {r["cui"]: r for r in csv.DictReader(open(os.path.join(METH, "severity_hpo_join.csv"), newline=""))}
    excl_csv = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(METH, "severity_hpo_excluded.csv"), newline="")):
        excl_csv[r["cui"]].append(r)
    audit = {a["cui"]: a for a in P["severity_hpo_join"]}
    jbad = []
    # the recorded hpo source sha must equal the file we just hashed (no drift)
    if P.get("hpo_severity_source", {}).get("sha256") != hpoa_sha:
        jbad.append("recorded hpoa sha != re-hashed phenotype.hpoa")
    for cui, jr in join_rows.items():
        if cui not in cohort_cuis:
            jbad.append(f"{cui} not in cohort"); continue
        if cui in excl_csv:
            jbad.append(f"{cui} in BOTH join and excluded")
        if not jr.get("dominant_sequela_basis", "").strip():
            jbad.append(f"{jr['entity']} no dominant_sequela_basis")
        rec_omims = set(str(x) for x in (rec_by_cui[cui].get("omim_codes") or []))
        pheno, modi = jr["hpo_phenotype"], jr["severity_modifier"]
        freq, ref = jr["frequency"].strip(), jr["reference"].strip()
        found = any(modi in m and fr == freq and rf == ref
                    for mim in rec_omims for (m, fr, rf) in hpoa_idx.get((mim, pheno), []))
        if not found:
            jbad.append(f"{jr['entity']} {pheno}/{modi}/{freq}/{ref} NOT in pinned hpoa")
        # a-priori tier
        want = MOD_TIER.get(modi)
        if want is None or abs(float(jr["severity_tier"]) - want) > 1e-9:
            jbad.append(f"{jr['entity']} tier {jr['severity_tier']} != a-priori {modi}->{want}")
        # audit mirrors the join + binds tier
        a = audit.get(cui)
        if not a:
            jbad.append(f"{jr['entity']} missing from severity_hpo_join audit")
        elif abs(a["severity_tier"] - want) > 1e-9 or a["severity_modifier"] != modi:
            jbad.append(f"{jr['entity']} audit tier/modifier mismatch")
    checks.append(("severity_join_anchored_cited", not jbad,
                   f"{len(join_rows)} severity join(s): re-found in pinned hpoa (pheno+modifier+freq+ref), "
                   f"cited basis present, tier from a-priori cut-points, audit binds tier ({len(jbad)} bad)"))

    # ---- 4b) a-priori INCLUSION criterion: every lifted feature is OBLIGATE in the pinned hpoa ----
    ob_bad = []
    if not P.get("severity_inclusion_criterion"):
        ob_bad.append("severity_inclusion_criterion not declared in registry")
    for cui, jr in join_rows.items():
        if not is_obligate(jr["frequency"]):
            ob_bad.append(f"{jr['entity']} join frequency {jr['frequency']!r} not obligate")
        rec_omims = set(str(x) for x in (rec_by_cui[cui].get("omim_codes") or []))
        pheno, modi = jr["hpo_phenotype"], jr["severity_modifier"]
        # the obligate frequency must be the one actually carried in the pinned source for this modifier
        if not any(modi in m and is_obligate(fr)
                   for mim in rec_omims for (m, fr, rf) in hpoa_idx.get((mim, pheno), [])):
            ob_bad.append(f"{jr['entity']} pinned hpoa carries no obligate severity annotation for {modi}")
    checks.append(("severity_annotation_obligate", not ob_bad,
                   f"declared a-priori criterion present; every lifted severity feature is OBLIGATE "
                   f"(HPO frequency 100%/Obligate) in the pinned source ({len(ob_bad)} bad)"))

    # ---- 5) declared a-priori severity cut-points + every HPO-sourced S == modifier tier ----
    cut_ok = ({k: v for k, v in P["severity_modifier_cutpoints"].items()} == SEV_TIER_DECL)
    scut_bad = []
    for r in recs:
        s_ax = r["components"]["S"]
        if s_ax["grade"] == "[L]" and "HPO Severity modifier" in (s_ax.get("source", "") or ""):
            if r["cui"] not in join_rows:
                scut_bad.append(f"{r['entity']} HPO-sourced S but not in join CSV"); continue
            want = MOD_TIER[join_rows[r["cui"]]["severity_modifier"]]
            prior = r7_state[r["cui"]]["S"][0] or 0.0
            if s_ax["value"] not in (want, max(want, prior)):
                scut_bad.append(f"{r['entity']} S={s_ax['value']} != tier {want} (or max w/ prior {prior})")
    checks.append(("severity_cutpoints_a_priori", cut_ok and not scut_bad,
                   f"declared modifier cut-points match fixed map; every HPO-sourced S == binned tier "
                   f"({len(scut_bad)} bad)"))

    # ---- 6) declined annotations recorded + not lifted to [L] via HPO ----
    ebad = []
    rec_excl = {(e["cui"], e["considered_phenotype"]) for e in P["severity_hpo_excluded"]}
    for cui, rows in excl_csv.items():
        if cui not in cohort_cuis:
            ebad.append(f"{cui} not in cohort")
        for x in rows:
            if not x.get("exclusion_reason", "").strip():
                ebad.append(f"{cui} no reason")
            if (cui, x["considered_phenotype"]) not in rec_excl:
                ebad.append(f"{x['entity']} {x['considered_phenotype']} missing from excluded audit")
        s_src = rec_by_cui[cui]["components"]["S"].get("source", "") or ""
        if "HPO Severity modifier" in s_src:
            ebad.append(f"{rows[0]['entity']} declined but S lifted via HPO")
    checks.append(("severity_excluded_recorded", not ebad,
                   f"{sum(len(v) for v in excl_csv.values())} declined annotations: in cohort, reason present, "
                   f"in audit, S not HPO-lifted ({len(ebad)} bad)"))

    # ---- 7) add-only: no grade weakened, no scored value removed, vs R7 ----
    downgrade = []
    for cui in r8_state:
        for ax in W:
            v7, g7, _ = r7_state[cui][ax]; v8, g8, _ = r8_state[cui][ax]
            if GR[g8] < GR[g7]:
                downgrade.append(f"{cui}/{ax} {g7}->{g8}")
            if v7 is not None and v8 is None:
                downgrade.append(f"{cui}/{ax} value dropped")
    checks.append(("addonly_no_downgrade", not downgrade,
                   f"no axis grade weakened and no scored value removed vs R7 ({len(downgrade)} violations)"))

    # ---- 8) R8 touches ONLY S, and S changes ONLY for joined diseases (0 illicit lifts) ----
    illicit = []
    for cui in r8_state:
        for ax in ("O", "P", "M", "D"):
            if (r7_state[cui][ax][0], r7_state[cui][ax][1]) != (r8_state[cui][ax][0], r8_state[cui][ax][1]):
                illicit.append(f"{cui}/{ax} changed (R8 must touch only S)")
        s7 = (r7_state[cui]["S"][0], r7_state[cui]["S"][1])
        s8 = (r8_state[cui]["S"][0], r8_state[cui]["S"][1])
        if s7 != s8 and cui not in join_rows:
            illicit.append(f"{cui}/S changed but not in join")
    checks.append(("s_lift_only_where_joined", not illicit,
                   f"O/P/M/D identical to R7; S changed only for the {len(join_rows)} joined disease(s) "
                   f"({len(illicit)} illicit)"))

    # ---- 9) new order-lock proven: Achondrogenesis II locks at R8 (not at R7); count 1->2 ----
    ACG2 = "C0220685"
    r7_lockn = sum(1 for v in r7_lock.values() if v)
    r8_lockn = sum(1 for v in r8_lock.values() if v)
    locked_entities = {rec_by_cui[c]["entity"] for c, v in r8_lock.items() if v}
    lock_ok = (r7_lock.get(ACG2) is False and r8_lock.get(ACG2) is True
               and r8_lockn == r7_lockn + 1 and r8_lockn == 2
               and "Achondrogenesis type II" in locked_entities
               and "Tyrosinemia type II" in locked_entities)
    checks.append(("new_order_lock_proven", lock_ok,
                   f"Achondrogenesis II order_locked R7={r7_lock.get(ACG2)} -> R8={r8_lock.get(ACG2)}; "
                   f"locked count {r7_lockn} -> {r8_lockn}; locked = {sorted(locked_entities)}"))

    # ---- 10) raw_burden re-derived (renormalised mean over present axes) ----
    raw_bad = []
    for r in recs:
        present = [r["components"][ax]["value"] for ax in W if r["components"][ax]["value"] is not None]
        exp = (sum(present) / len(present)) if present else None
        got = r["raw_burden"]
        if (exp is None) != (got is None) or (exp is not None and abs(exp - got) > 1e-9):
            raw_bad.append(r["entity"])
    checks.append(("raw_burden_rederived", not raw_bad,
                   f"renormalised-mean recompute matches stored raw_burden ({len(raw_bad)} mismatch)"))

    # ---- 11) rankability + promotions ----
    rank_bad = [r["entity"] for r in recs if r["rankable"] != (r["axes_scored"] >= 3)]
    banked = {x["cui"]: x for x in json.load(open(os.path.join(CUR, "burden_scores.json")))["records"]}
    promo_calc = sorted(r["cui"] for r in recs if r["rankable"] and not banked[r["cui"]]["rankable"])
    promo_rec = sorted(p["cui"] for p in P["promotions_from_not_placed"])
    checks.append(("rankability_and_promotions", not rank_bad and promo_calc == promo_rec,
                   f"rankable == (axes>=3) for all ({len(rank_bad)} bad); promotions recompute matches "
                   f"({len(promo_rec)} promoted)"))

    # ---- 12) residual correct ----
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

    # ---- 13) order-lock rule holds globally + sensitivity ----
    lock_bad = []
    for r in recs:
        present = [r["components"][ax]["grade"] for ax in W if r["components"][ax]["value"] is not None]
        exp = bool(r["rankable"] and present and all(GR[g] >= GR["[L]"] for g in present))
        if exp != r["order_locked"]:
            lock_bad.append(r["entity"])
    sens = P["sensitivity"]
    eq = sens.get("equal_default", {}).get("spearman_vs_default")
    checks.append(("order_lock_rule_and_sensitivity", not lock_bad and eq == 1.0 and len(sens) >= 5,
                   f"order_locked rule holds for all ({len(lock_bad)} bad); {len(sens)} weightings, "
                   f"equal_default rho={eq}"))

    # ---- 14) OMIM clinical-synopsis path RECORDED AS REMOVED (key unobtainable), not used ----
    omim_log = json.load(open(os.path.join(OMIM, "_fetch_log.json")))
    policy = P.get("lift_policy", "")
    omim_ok = (omim_log.get("status") == "SKIPPED" and "OMIM_API_KEY" in omim_log.get("obstacle", "")
               and "OMIM clinical synopsis path REMOVED" in policy
               and not any("OMIM" in (r["components"]["S"].get("source", "") or "") for r in recs))
    checks.append(("omim_path_removed_documented", omim_ok,
                   f"OMIM synopsis status={omim_log.get('status')}, path documented REMOVED (key unobtainable), "
                   f"no S value sourced from OMIM"))

    # ---- 15) engine pin drift zero ----
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
        "phase": "R8", "kind": "investigation_gate",
        "title": "open-source severity pass (HPO Severity-modifier dominant-sequela join) — S lift / new order-lock",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
            "burden_scores_registry_csv": {"path": "data/curated/burden_scores_registry.csv", "sha12": sha12(SCORES_C)},
            "burden_residual_registry_json": {"path": "data/curated/burden_residual_registry.json", "sha12": sha12(RESID_J)},
            "phenotype_hpoa": {"path": "data/raw/hpo/phenotype.hpoa.gz", "sha12": hpoa_sha[:12]},
            "severity_join_csv": {"path": "methodology/severity_hpo_join.csv", "sha12": sha12(os.path.join(METH, "severity_hpo_join.csv"))},
            "severity_excluded_csv": {"path": "methodology/severity_hpo_excluded.csv", "sha12": sha12(os.path.join(METH, "severity_hpo_excluded.csv"))},
            "omim_log": {"path": "data/raw/omim/_fetch_log.json", "sha12": sha12(os.path.join(OMIM, "_fetch_log.json"))},
        },
        "lift_counts": P.get("lift_counts"),
        "axis_grade_coverage_registry": P.get("axis_grade_coverage_registry"),
        "severity_hpo_join": P.get("severity_hpo_join"),
        "severity_hpo_excluded": P.get("severity_hpo_excluded"),
        "axis_value_changes": P.get("axis_value_changes"),
        "order_locked": P.get("order_locked_diseases"),
        "registry_set_sha12": registry_set_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "r8.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"R8 GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:30s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
