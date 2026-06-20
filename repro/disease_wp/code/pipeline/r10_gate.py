#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R10 gate -- verifies the curated SEVERITY / PROGRESSION literature pass, ROUND 2,
independently of any recorded digest. It:
  * proves the r5->r6->r7->r8->r9->r10 chain is deterministic (2x identical
    registry-set sha);
  * re-anchors every round-2 curation-join row in the PINNED PMC-OA cache (cited
    sentence re-found VERBATIM in pinned text that passes its own sha256), confirms
    the source is open-access, and confirms the tier is the one the FROZEN R3 tier
    function derives from that sentence -- not a hand-asserted number -- with the
    R3 spectrum override holding;
  * confirms every round-2 declined statement is recorded with a decline_class
    (declared vocabulary) + a per-disease reason, is itself re-found in the pinned
    cache, and did NOT lift that disease's S/P to [L];
  * confirms add-only (no grade weakened / no scored value removed vs the R9 base)
    and that the ONLY axes R10 touches are S and P, changed ONLY for the round-2
    joined diseases (O/M/D byte-identical to R9);
  * proves R10 introduces NO new order-lock (lock set unchanged vs R9, still 3) and
    that the grade-only P lifts (Fabry, Marfan) do NOT lock those diseases (their
    severity remains [H]);
  * re-derives composites / rankability / residual / order-lock-rule / sensitivity;
  * confirms every round-2 cited source is open-access and each lift is fully
    source-bound (no inference);
  * confirms the R3/R4 BANKED files stay byte-identical and the engine pin is drift-0;
  * confirms R9's OWN recorded artifacts are untouched (R9 join/excluded CSV digests
    and R9's recorded registry-set sha are preserved -- R10 is additive, not a mutation
    of R9).

Living code, NOT in the frozen engine pin.  Out: reports/r10.gate.json
"""
import os, re, csv, json, sys, hashlib, subprocess, datetime, collections, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
METH = os.path.join(ROOT, "methodology")
LITC = os.path.join(ROOT, "data", "raw", "litcurate")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
RESID_J = os.path.join(CUR, "burden_residual_registry.json")
RESID_C = os.path.join(CUR, "burden_residual_registry.csv")
R5 = os.path.join(HERE, "r5_accession_apply.py")
R6 = os.path.join(HERE, "r6_naturalhistory_registry.py")
R7 = os.path.join(HERE, "r7_naturalhistory_registry2.py")
R8 = os.path.join(HERE, "r8_severity_registry.py")
R9 = os.path.join(HERE, "r9_severity_litcurate.py")
R10 = os.path.join(HERE, "r10_severity_litcurate.py")

JOIN2 = os.path.join(METH, "severity_litcurate2_join.csv")
EXCL2 = os.path.join(METH, "severity_litcurate2_excluded.csv")

BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
}
# R9's own recorded artifacts -- R10 must NOT modify these (additive, not a mutation)
R9_RECORDED = {
    "methodology/severity_litcurate_join.csv":     "59b2721fc7623a6216b1a4d9079d879980146462064ecabc45cfcd980f494081",
    "methodology/severity_litcurate_excluded.csv": "e3ad0cdd610d5f4359e08ff82c8b1a0fd9af5a7f3918d67aeba16d57f1093dcf",
}
DECLINE_VOCAB = {"spectrum", "comparative", "umbrella_spectrum", "historical",
                 "form_specific", "treated_cohort", "non_dominant", "sub_phenotype"}
GR = {"[O]": 0, "[H]": 1, "[L]": 2, "[V]": 3}
W = ["O", "P", "S", "M", "D"]

# frozen R3 tier function (the SAME a-priori cut-points the pipeline derives from)
_spec = importlib.util.spec_from_file_location("r3g", os.path.join(HERE, "r3_burden_index.py"))
r3 = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(r3)
first_match = r3.first_match
PATTERNS = r3.PATTERNS
AXIS_PATTERN = {"P": "P_progression", "S": "S_severity"}

# spectrum overrides: import from R9 so the gate uses the SAME definition the stage does
_s9 = importlib.util.spec_from_file_location("r9g", os.path.join(HERE, "r9_severity_litcurate.py"))
r9mod = importlib.util.module_from_spec(_s9); _s9.loader.exec_module(r9mod)
is_spectrum = r9mod.is_spectrum


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
        st[r["cui"]] = {ax: (r["components"][ax]["value"], r["components"][ax]["grade"])
                        for ax in W}
    return st


def lock_state(payload):
    return {r["cui"]: bool(r.get("order_locked")) for r in payload["records"]}


def load_pinned(pmcid):
    p = os.path.join(LITC, f"{pmcid}.json")
    if not os.path.exists(p):
        return None
    art = json.load(open(p))
    if not art.get("found") or hashlib.sha256(art["text"].encode("utf-8")).hexdigest() != art.get("text_sha256"):
        return None
    return art


def main():
    checks = []

    # ---- 1) determinism: r5..r10 chain twice -> identical registry-set sha ----
    run(R5); run(R6); run(R7); run(R8); run(R9); run(R10); s1 = registry_set_sha()
    run(R5); run(R6); run(R7); run(R8); run(R9); run(R10); s2 = registry_set_sha()
    checks.append(("determinism_chain_2x", s1 == s2,
                   f"r5->...->r9->r10 chain registry-set sha {s1} == {s2}"))

    # capture R9 base (pre round-2), then R10
    run(R5); run(R6); run(R7); run(R8); run(R9); P9 = json.load(open(SCORES_J))
    r9_state = axis_state(P9); r9_lock = lock_state(P9)
    run(R10); P = json.load(open(SCORES_J)); r10_state = axis_state(P); r10_lock = lock_state(P)
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

    # ---- 3) R10 builds on a real R9 base (cumulative) ----
    passes = P.get("registry_passes", [])
    base_ok = (passes[-1] == "R10_litcurate2"
               and "R9_litcurate_severity_progression" in passes
               and "R8_open_severity" in passes and "R7_open_naturalhistory" in passes)
    checks.append(("cumulative_over_r9", base_ok, f"registry_passes = {passes}"))

    # ---- 4) round-2 curation join re-anchored in pinned OA cache + tier from frozen R3 + non-spectrum ----
    join_rows = list(csv.DictReader(open(JOIN2, newline="")))
    excl_csv = collections.defaultdict(list)
    for r in csv.DictReader(open(EXCL2, newline="")):
        excl_csv[r["cui"]].append(r)
    audit = {(a["cui"], a["axis"]): a for a in P.get("litcurate2_join", [])}
    jbad = []
    for jr in join_rows:
        cui, axis, entity = jr["cui"], jr["axis"], jr["entity"]
        if cui not in cohort_cuis:
            jbad.append(f"{entity} not in cohort"); continue
        if axis not in AXIS_PATTERN:
            jbad.append(f"{entity} axis {axis} not S/P")
        if any(e["cui"] == cui and e["axis"] == axis for e in
               [row for rows in excl_csv.values() for row in rows]):
            jbad.append(f"{entity}/{axis} in BOTH join and excluded")
        if not (jr.get("dominant_sequela_basis") or "").strip():
            jbad.append(f"{entity} no dominant_sequela_basis")
        art = load_pinned(jr["pmcid"])
        if art is None:
            jbad.append(f"{entity} pinned OA cache {jr['pmcid']} missing/corrupt"); continue
        if not art.get("open_access"):
            jbad.append(f"{entity} cited {jr['pmcid']} not open-access")
        if jr["exact_sentence"] not in art["text"]:
            jbad.append(f"{entity} cited sentence NOT re-found in pinned {jr['pmcid']}"); continue
        hit = first_match(jr["exact_sentence"], PATTERNS[AXIS_PATTERN[axis]])
        if not hit:
            jbad.append(f"{entity} sentence matches no R3 {axis} tier"); continue
        if is_spectrum(axis, jr["exact_sentence"]):
            jbad.append(f"{entity} sentence trips R3 spectrum override")
        if abs(float(jr["tier"]) - hit[0]) > 1e-9:
            jbad.append(f"{entity} declared tier {jr['tier']} != frozen-R3 {hit[0]}")
        a = audit.get((cui, axis))
        if not a:
            jbad.append(f"{entity}/{axis} missing from litcurate2_join audit")
        elif abs(a["tier"] - hit[0]) > 1e-9:
            jbad.append(f"{entity}/{axis} audit tier mismatch")
    checks.append(("litcurate2_join_anchored_cited", not jbad,
                   f"{len(join_rows)} round-2 join(s): cited sentence re-found verbatim in pinned OA cache, "
                   f"source open-access, basis present, tier == frozen-R3-derived, non-spectrum ({len(jbad)} bad)"))

    # ---- 5) tier cut-points are the BURDEN_INDEX a-priori map (recorded) + every round-2 lifted axis == derived ----
    pcut = P.get("litcurate_progression_cutpoints", {})
    scut = P.get("litcurate_severity_cutpoints", {})
    cut_ok = (pcut.get("progressive course with fatal outcome") == 1.0
              and pcut.get("rapidly progressive") == 0.8
              and pcut.get("slowly progressive / progressive") == 0.5
              and pcut.get("static/non-progressive") == 0.2
              and scut.get("severe / debilitating") == 0.75 and scut.get("profound / devastating") == 1.0
              and scut.get("moderate") == 0.5 and scut.get("mild / asymptomatic") == 0.25)
    scut_bad = []
    join_keys = {(j["cui"], j["axis"]) for j in join_rows}
    for (cui, axis) in join_keys:
        jr = next(j for j in join_rows if j["cui"] == cui and j["axis"] == axis)
        hit = first_match(jr["exact_sentence"], PATTERNS[AXIS_PATTERN[axis]])
        ax = rec_by_cui[cui]["components"][axis]
        prior = (r9_state[cui][axis][0] or 0.0)
        if ax["grade"] != "[L]":
            scut_bad.append(f"{jr['entity']} {axis} not [L] after round-2 lift")
        if hit and ax["value"] not in (hit[0], max(hit[0], prior)):
            scut_bad.append(f"{jr['entity']} {axis}={ax['value']} != derived {hit[0]} (or max w/ prior {prior})")
    checks.append(("litcurate2_cutpoints_a_priori", cut_ok and not scut_bad,
                   f"recorded P/S cut-points equal the BURDEN_INDEX map; every round-2 curated S/P == frozen-R3 "
                   f"derived tier ({len(scut_bad)} bad)"))

    # ---- 6) round-2 declines recorded + not lifted to [L] via curation ----
    ebad = []
    rec_excl = {(e["cui"], e["axis"], e["considered_pmcid"]) for e in P.get("litcurate2_excluded", [])}
    for cui, rows in excl_csv.items():
        if cui not in cohort_cuis:
            ebad.append(f"{cui} not in cohort")
        for x in rows:
            if x.get("decline_class") not in DECLINE_VOCAB:
                ebad.append(f"{x['entity']} decline_class {x.get('decline_class')!r} not in vocab")
            if not (x.get("exclusion_reason") or "").strip():
                ebad.append(f"{x['entity']} no reason")
            if (cui, x["axis"], x["considered_pmcid"]) not in rec_excl:
                ebad.append(f"{x['entity']} {x['considered_pmcid']} missing from excluded audit")
            art = load_pinned(x["considered_pmcid"])
            if art is None or x["considered_statement"] not in art["text"]:
                ebad.append(f"{x['entity']} considered statement not in pinned {x['considered_pmcid']}")
            # the declined disease must NOT have had THIS axis lifted via round-2 curation
            if (cui, x["axis"]) in join_keys:
                ebad.append(f"{x['entity']} declined but {x['axis']} lifted via round-2 curation")
    checks.append(("litcurate2_excluded_recorded", not ebad,
                   f"{sum(len(v) for v in excl_csv.values())} round-2 decline(s): in cohort, decline_class in "
                   f"vocab, reason present, statement re-found in pinned cache, axis not curation-lifted ({len(ebad)} bad)"))

    # ---- 7) add-only: no grade weakened, no scored value removed, vs R9 ----
    downgrade = []
    for cui in r10_state:
        for ax in W:
            v9, g9 = r9_state[cui][ax]; v10, g10 = r10_state[cui][ax]
            if GR[g10] < GR[g9]:
                downgrade.append(f"{cui}/{ax} {g9}->{g10}")
            if v9 is not None and v10 is None:
                downgrade.append(f"{cui}/{ax} value dropped")
    checks.append(("addonly_no_downgrade", not downgrade,
                   f"no axis grade weakened and no scored value removed vs R9 ({len(downgrade)} violations)"))

    # ---- 8) R10 touches ONLY S/P, changed ONLY for round-2 joined diseases (0 illicit) ----
    illicit = []
    for cui in r10_state:
        for ax in ("O", "M", "D"):
            if r9_state[cui][ax] != r10_state[cui][ax]:
                illicit.append(f"{cui}/{ax} changed (R10 must touch only S/P)")
        for ax in ("S", "P"):
            if r9_state[cui][ax] != r10_state[cui][ax] and (cui, ax) not in join_keys:
                illicit.append(f"{cui}/{ax} changed but not in round-2 join")
    checks.append(("sp_lift_only_where_joined", not illicit,
                   f"O/M/D identical to R9; S/P changed only for the {len(join_keys)} round-2 joined "
                   f"(disease,axis) pair(s) ({len(illicit)} illicit)"))

    # ---- 9) NO new order-lock: lock set unchanged vs R9 (still 3); grade-only P lifts do NOT lock ----
    FAB = "C0002986"; MAR = "C0024796"
    r9_lockn = sum(1 for v in r9_lock.values() if v)
    r10_lockn = sum(1 for v in r10_lock.values() if v)
    locked9 = {rec_by_cui[c]["entity"] for c, v in r9_lock.items() if v}
    locked10 = {rec_by_cui[c]["entity"] for c, v in r10_lock.items() if v}
    lock_ok = (r9_lockn == r10_lockn == 3 and locked9 == locked10
               and r10_lock.get(FAB) is False and r10_lock.get(MAR) is False
               # prove the grade-only P lift DID land (P: [H]->[L]) yet did not lock
               and r9_state[FAB]["P"][1] == "[H]" and r10_state[FAB]["P"][1] == "[L]"
               and r9_state[MAR]["P"][1] == "[H]" and r10_state[MAR]["P"][1] == "[L]")
    checks.append(("no_new_order_lock", lock_ok,
                   f"lock set unchanged R9={r9_lockn} -> R10={r10_lockn} ({sorted(locked10)}); Fabry/Marfan P "
                   f"[H]->[L] grade-only lifts do NOT lock (severity remains [H])"))

    # ---- 10) raw_burden re-derived ----
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

    # ---- 14) every round-2 cited source open-access + lift fully source-bound (no inference) ----
    oa_bad = []
    cited = {a["pmcid"] for a in P.get("litcurate2_join", [])} | {e["considered_pmcid"] for e in P.get("litcurate2_excluded", [])}
    for pmcid in cited:
        art = load_pinned(pmcid)
        if art is None:
            oa_bad.append(f"{pmcid} pinned cache missing/corrupt")
        elif not art.get("open_access"):
            oa_bad.append(f"{pmcid} not open-access")
    # every round-2 [L] lift must be bound to a round-2 join row
    for (cui, axis) in join_keys:
        ax = rec_by_cui[cui]["components"][axis]
        if ax["grade"] != "[L]":
            oa_bad.append(f"{rec_by_cui[cui]['entity']}/{axis} round-2 join but not [L]")
    crit_ok = bool(P.get("litcurate_inclusion_criterion"))
    checks.append(("litcurate2_sources_open_access_and_bound", not oa_bad and crit_ok,
                   f"all {len(cited)} round-2 cited sources open-access + sha-pinned; every round-2 S/P [L] is bound "
                   f"to a join row (no inference); inclusion criterion declared ({len(oa_bad)} bad)"))

    # ---- 15) R9's OWN recorded artifacts preserved (R10 additive, not a mutation of R9) ----
    r9_preserved = []
    for rel, want in R9_RECORDED.items():
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            r9_preserved.append(f"missing {rel}")
        elif sha(p) != want:
            r9_preserved.append(f"R9 artifact MODIFIED: {rel}")
    checks.append(("r9_artifacts_preserved", not r9_preserved,
                   f"R9 recorded join/excluded CSVs byte-identical to their R9 digests "
                   f"({len(r9_preserved)} modified) -- R10 is additive"))

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
        "phase": "R10", "kind": "investigation_gate",
        "title": "curated severity/progression literature pass, round 2 (PMC-OA dominant-sequela join) — S/P corroboration, no new lock",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
            "burden_scores_registry_csv": {"path": "data/curated/burden_scores_registry.csv", "sha12": sha12(SCORES_C)},
            "burden_residual_registry_json": {"path": "data/curated/burden_residual_registry.json", "sha12": sha12(RESID_J)},
            "litcurate2_join_csv": {"path": "methodology/severity_litcurate2_join.csv", "sha12": sha12(JOIN2)},
            "litcurate2_excluded_csv": {"path": "methodology/severity_litcurate2_excluded.csv", "sha12": sha12(EXCL2)},
            "litcurate_fetch_log_r10": {"path": "data/raw/litcurate/_fetch_log_r10.json", "sha12": sha12(os.path.join(LITC, "_fetch_log_r10.json"))},
        },
        "lift_counts": P.get("lift_counts"),
        "axis_grade_coverage_registry": P.get("axis_grade_coverage_registry"),
        "litcurate2_join": P.get("litcurate2_join"),
        "litcurate2_excluded": P.get("litcurate2_excluded"),
        "axis_value_changes": P.get("axis_value_changes"),
        "order_locked": P.get("order_locked_diseases"),
        "registry_set_sha12": registry_set_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "r10.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"R10 GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:38s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
