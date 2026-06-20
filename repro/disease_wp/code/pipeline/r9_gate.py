#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R9 gate -- verifies the curated SEVERITY / PROGRESSION literature pass
independently of any recorded digest. It:
  * proves the r5->r6->r7->r8->r9 chain is deterministic (2x identical registry-set sha);
  * re-anchors every curation-join row in the PINNED PMC-OA cache (the cited
    sentence must be re-found VERBATIM in the pinned text, which must pass its own
    text sha256), confirms the source is open-access, and confirms the tier is the
    one the FROZEN R3 tier function (first_match over PATTERNS) derives from that
    sentence -- not a hand-asserted number -- with the R3 spectrum override holding;
  * confirms every declined statement is recorded with a decline_class (from the
    declared vocabulary) + a per-disease reason, is itself re-found in the pinned
    cache, and did NOT lift that disease's S/P to [L];
  * confirms add-only (no grade weakened / no scored value removed vs the R8 base)
    and that the ONLY axes R9 touches are S and P, changed ONLY for joined diseases
    (O/M/D byte-identical to R8; S unchanged since R9 has no S lift, only S declines);
  * proves the new order-lock (Niemann-Pick type A locks at R9, was not at R8;
    count 2 -> 3) and that the grade-only P lift on DMD does NOT lock it (its S was
    honestly declined at R8 and stays [H]);
  * re-derives composites / rankability / residual / order-lock-rule / sensitivity;
  * confirms every cited source is open-access and the lift is fully source-bound
    (no inference): the R9 analogue of the R8 OMIM-removed check;
  * confirms the R3/R4 BANKED files stay byte-identical and the engine pin is drift-0.

Living code, NOT in the frozen engine pin.  Out: reports/r9.gate.json
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

BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
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


def spectrum_P(low):
    pw = re.search(r"\bprogress", low)
    sp = re.search(r"continuum|ranges?\s+(?:from|over)|range\s+from|spectrum"
                   r"|from\s+[\w-]+[^.]*\bto\b|varying|variabilit", low)
    pf = re.search(r"rapidly\s+progressive|fulminant|aggressive\s+(?:course|progression)"
                   r"|\b(?:fatal|lethal)\b|\bdeath\b|\bdie[sd]?\b|perinatal", low)
    ps = re.search(r"slowly\s+progressive|non-?progressive|\bstatic\b|stable\s+course"
                   r"|attenuated|\bslight\b|normal\s+life|asymptomatic|\bmild\b", low)
    return bool(pw and sp and pf and ps)


def spectrum_S(low):
    hm = re.search(r"\bmild\b|asymptomatic|benign", low)
    hh = re.search(r"\bsevere\b|\bprofound\b|devastating|lethal|fatal", low)
    ev = re.search(
        r"variabl[ey]\s+(?:severity|phenotyp|expressi|presentation|clinical|disease)"
        r"|(?:severity|phenotyp|expressi|presentation)[^.]{0,30}\bvariab"
        r"|variabilit\w*[^.]{0,20}(?:severity|phenotyp|expressi|presentation|disease)"
        r"|vary\s+widely|varies\s+widely|wide\s+(?:range|spectrum)\s+of\s+severit"
        r"|ranges?\s+from\s+[\w-]+[^.]*\bto\b|broad\s+(?:phenotypic\s+|clinical\s+)?spectrum", low)
    return bool((hm and hh) or (ev and (hm or hh)))


def is_spectrum(axis, s):
    return spectrum_P(s.lower()) if axis == "P" else spectrum_S(s.lower())


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

    # ---- 1) determinism: r5..r9 chain twice -> identical registry-set sha ----
    run(R5); run(R6); run(R7); run(R8); run(R9); s1 = registry_set_sha()
    run(R5); run(R6); run(R7); run(R8); run(R9); s2 = registry_set_sha()
    checks.append(("determinism_chain_2x", s1 == s2,
                   f"r5->r6->r7->r8->r9 chain registry-set sha {s1} == {s2}"))

    # capture R8 base (pre-litcurate), then R9
    run(R5); run(R6); run(R7); run(R8); P8 = json.load(open(SCORES_J))
    r8_state = axis_state(P8); r8_lock = lock_state(P8)
    run(R9); P = json.load(open(SCORES_J)); r9_state = axis_state(P); r9_lock = lock_state(P)
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

    # ---- 3) R9 builds on a real R8 base ----
    passes = P.get("registry_passes", [])
    base_ok = (passes[-1] == "R9_litcurate_severity_progression"
               and "R8_open_severity" in passes and "R7_open_naturalhistory" in passes)
    checks.append(("cumulative_over_r8", base_ok, f"registry_passes = {passes}"))

    # ---- 4) curation join re-anchored in pinned OA cache + tier from frozen R3 + non-spectrum ----
    join_rows = list(csv.DictReader(open(os.path.join(METH, "severity_litcurate_join.csv"), newline="")))
    excl_csv = collections.defaultdict(list)
    for r in csv.DictReader(open(os.path.join(METH, "severity_litcurate_excluded.csv"), newline="")):
        excl_csv[r["cui"]].append(r)
    audit = {(a["cui"], a["axis"]): a for a in P.get("litcurate_join", [])}
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
        # tier DERIVED by frozen R3 (not hand-asserted)
        hit = first_match(jr["exact_sentence"], PATTERNS[AXIS_PATTERN[axis]])
        if not hit:
            jbad.append(f"{entity} sentence matches no R3 {axis} tier"); continue
        if is_spectrum(axis, jr["exact_sentence"]):
            jbad.append(f"{entity} sentence trips R3 spectrum override")
        if abs(float(jr["tier"]) - hit[0]) > 1e-9:
            jbad.append(f"{entity} declared tier {jr['tier']} != frozen-R3 {hit[0]}")
        a = audit.get((cui, axis))
        if not a:
            jbad.append(f"{entity}/{axis} missing from litcurate_join audit")
        elif abs(a["tier"] - hit[0]) > 1e-9:
            jbad.append(f"{entity}/{axis} audit tier mismatch")
    checks.append(("litcurate_join_anchored_cited", not jbad,
                   f"{len(join_rows)} curation join(s): cited sentence re-found verbatim in pinned OA cache, "
                   f"source open-access, basis present, tier == frozen-R3-derived, non-spectrum ({len(jbad)} bad)"))

    # ---- 5) tier cut-points are the BURDEN_INDEX a-priori map (recorded) + every lifted axis == derived tier ----
    pcut = P.get("litcurate_progression_cutpoints", {})
    scut = P.get("litcurate_severity_cutpoints", {})
    cut_ok = (pcut.get("progressive course with fatal outcome") == 1.0
              and pcut.get("rapidly progressive") == 0.8
              and pcut.get("slowly progressive / progressive") == 0.5
              and pcut.get("static/non-progressive") == 0.2
              and scut.get("severe / debilitating") == 0.75 and scut.get("profound / devastating") == 1.0
              and scut.get("moderate") == 0.5 and scut.get("mild / asymptomatic") == 0.25)
    scut_bad = []
    for r in recs:
        for axis in ("P", "S"):
            ax = r["components"][axis]
            if ax["grade"] == "[L]" and "curated literature" in (ax.get("basis", "") or ""):
                jr = next((j for j in join_rows if j["cui"] == r["cui"] and j["axis"] == axis), None)
                if not jr:
                    scut_bad.append(f"{r['entity']} curated-{axis} [L] but not in join CSV"); continue
                hit = first_match(jr["exact_sentence"], PATTERNS[AXIS_PATTERN[axis]])
                prior = r8_state[r["cui"]][axis][0] or 0.0
                if hit and ax["value"] not in (hit[0], max(hit[0], prior)):
                    scut_bad.append(f"{r['entity']} {axis}={ax['value']} != derived {hit[0]} (or max w/ prior {prior})")
    checks.append(("litcurate_cutpoints_a_priori", cut_ok and not scut_bad,
                   f"recorded P/S cut-points equal the BURDEN_INDEX map; every curated-sourced S/P == frozen-R3 "
                   f"derived tier ({len(scut_bad)} bad)"))

    # ---- 6) declines recorded + not lifted to [L] via curation ----
    ebad = []
    rec_excl = {(e["cui"], e["axis"], e["considered_pmcid"]) for e in P.get("litcurate_excluded", [])}
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
            # the declined disease must NOT have had THIS axis lifted via curation
            axsrc = rec_by_cui[cui]["components"][x["axis"]].get("basis", "") or ""
            if "curated literature" in axsrc and not any(
                    j["cui"] == cui and j["axis"] == x["axis"] for j in join_rows):
                ebad.append(f"{x['entity']} declined but {x['axis']} lifted via curation")
    checks.append(("litcurate_excluded_recorded", not ebad,
                   f"{sum(len(v) for v in excl_csv.values())} declined statement(s): in cohort, decline_class in "
                   f"vocab, reason present, statement re-found in pinned cache, axis not curation-lifted ({len(ebad)} bad)"))

    # ---- 7) add-only: no grade weakened, no scored value removed, vs R8 ----
    downgrade = []
    for cui in r9_state:
        for ax in W:
            v8, g8 = r8_state[cui][ax]; v9, g9 = r9_state[cui][ax]
            if GR[g9] < GR[g8]:
                downgrade.append(f"{cui}/{ax} {g8}->{g9}")
            if v8 is not None and v9 is None:
                downgrade.append(f"{cui}/{ax} value dropped")
    checks.append(("addonly_no_downgrade", not downgrade,
                   f"no axis grade weakened and no scored value removed vs R8 ({len(downgrade)} violations)"))

    # ---- 8) R9 touches ONLY S/P, changed ONLY for joined diseases (0 illicit) ----
    join_keys = {(j["cui"], j["axis"]) for j in join_rows}
    illicit = []
    for cui in r9_state:
        for ax in ("O", "M", "D"):
            if r8_state[cui][ax] != r9_state[cui][ax]:
                illicit.append(f"{cui}/{ax} changed (R9 must touch only S/P)")
        for ax in ("S", "P"):
            if r8_state[cui][ax] != r9_state[cui][ax] and (cui, ax) not in join_keys:
                illicit.append(f"{cui}/{ax} changed but not in join")
    checks.append(("sp_lift_only_where_joined", not illicit,
                   f"O/M/D identical to R8; S/P changed only for the {len(join_keys)} joined (disease,axis) pair(s) "
                   f"({len(illicit)} illicit)"))

    # ---- 9) new order-lock proven: NPD-A locks at R9 (not at R8); count 2->3; DMD does NOT lock ----
    NPDA = "C0268242"; DMD = "C0013264"
    r8_lockn = sum(1 for v in r8_lock.values() if v)
    r9_lockn = sum(1 for v in r9_lock.values() if v)
    locked_entities = {rec_by_cui[c]["entity"] for c, v in r9_lock.items() if v}
    lock_ok = (r8_lock.get(NPDA) is False and r9_lock.get(NPDA) is True
               and r9_lockn == r8_lockn + 1 and r9_lockn == 3
               and r9_lock.get(DMD) is False  # grade-only P lift; S still [H] (declined at R8)
               and {"Achondrogenesis type II", "Niemann-Pick disease, type A", "Tyrosinemia type II"} <= locked_entities)
    checks.append(("new_order_lock_proven", lock_ok,
                   f"NPD-A order_locked R8={r8_lock.get(NPDA)} -> R9={r9_lock.get(NPDA)}; locked count "
                   f"{r8_lockn} -> {r9_lockn}; DMD locked={r9_lock.get(DMD)} (S declined, stays [H]); "
                   f"locked = {sorted(locked_entities)}"))

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

    # ---- 14) every cited source open-access + lift fully source-bound (no inference) ----
    oa_bad = []
    cited = {a["pmcid"] for a in P.get("litcurate_join", [])} | {e["considered_pmcid"] for e in P.get("litcurate_excluded", [])}
    for pmcid in cited:
        art = load_pinned(pmcid)
        if art is None:
            oa_bad.append(f"{pmcid} pinned cache missing/corrupt")
        elif not art.get("open_access"):
            oa_bad.append(f"{pmcid} not open-access")
    # no S/P [L] value may carry a curated basis without a matching join row (source-bound)
    for r in recs:
        for axis in ("P", "S"):
            ax = r["components"][axis]
            if "curated literature" in (ax.get("basis", "") or "") and not any(
                    j["cui"] == r["cui"] and j["axis"] == axis for j in join_rows):
                oa_bad.append(f"{r['entity']}/{axis} curated basis without a join row")
    crit_ok = bool(P.get("litcurate_inclusion_criterion"))
    checks.append(("litcurate_sources_open_access_and_bound", not oa_bad and crit_ok,
                   f"all {len(cited)} cited sources open-access + sha-pinned; every curated S/P [L] is bound to a "
                   f"join row (no inference); inclusion criterion declared ({len(oa_bad)} bad)"))

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
        "phase": "R9", "kind": "investigation_gate",
        "title": "curated severity/progression literature pass (PMC-OA dominant-sequela join) — S/P lift / new order-lock",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
            "burden_scores_registry_csv": {"path": "data/curated/burden_scores_registry.csv", "sha12": sha12(SCORES_C)},
            "burden_residual_registry_json": {"path": "data/curated/burden_residual_registry.json", "sha12": sha12(RESID_J)},
            "litcurate_join_csv": {"path": "methodology/severity_litcurate_join.csv", "sha12": sha12(os.path.join(METH, "severity_litcurate_join.csv"))},
            "litcurate_excluded_csv": {"path": "methodology/severity_litcurate_excluded.csv", "sha12": sha12(os.path.join(METH, "severity_litcurate_excluded.csv"))},
            "litcurate_fetch_log": {"path": "data/raw/litcurate/_fetch_log.json", "sha12": sha12(os.path.join(LITC, "_fetch_log.json"))},
        },
        "lift_counts": P.get("lift_counts"),
        "axis_grade_coverage_registry": P.get("axis_grade_coverage_registry"),
        "litcurate_join": P.get("litcurate_join"),
        "litcurate_excluded": P.get("litcurate_excluded"),
        "axis_value_changes": P.get("axis_value_changes"),
        "order_locked": P.get("order_locked_diseases"),
        "registry_set_sha12": registry_set_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "r9.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"R9 GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:38s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
