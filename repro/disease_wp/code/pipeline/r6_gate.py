#!/usr/bin/env python3
"""
R6 gate -- verifies the natural-history registry pass (Orphanet) independently of
any recorded digest. Re-derives composites, rankability, residual, and the order
lock; confirms the lift is Exact-mapped, entity-anchored, frequency-gated, and
ADD-ONLY (Orphanet absence never downgrades a banked value); confirms the R3/R4
BANKED files stay byte-identical and the engine pin is drift-zero; and proves the
r5 -> r6 chain is deterministic (2x identical).

Living code, NOT in the frozen engine pin.
Out: reports/r6.gate.json
"""
import os, csv, json, sys, hashlib, subprocess, importlib.util, datetime, collections
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
ORPHA = os.path.join(ROOT, "data", "raw", "orphanet")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
SCORES_C = os.path.join(CUR, "burden_scores_registry.csv")
RESID_J = os.path.join(CUR, "burden_residual_registry.json")
R5 = os.path.join(HERE, "r5_accession_apply.py")
R6 = os.path.join(HERE, "r6_naturalhistory_registry.py")

# banked R3/R4 digests (immutable baseline; must not move under the registry layer)
BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
}
ONSET_TIER_VALUES = {1.0, 0.85, 0.7, 0.55, 0.35, 0.2}
FREQ_OK = {"Obligate (100%)", "Very frequent (99-80%)", "Frequent (79-30%)"}
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
    for p in (SCORES_C, SCORES_J, os.path.join(CUR, "burden_residual_registry.csv"), RESID_J):
        h.update(open(p, "rb").read())
    return h.hexdigest()[:12]


def axis_state(payload):
    """cui -> {axis: (value, grade, source_has_orphanet)}"""
    st = {}
    for r in payload["records"]:
        st[r["cui"]] = {ax: (r["components"][ax]["value"], r["components"][ax]["grade"],
                             "Orphanet" in (r["components"][ax].get("source", "")))
                        for ax in W}
    return st


def main():
    checks = []

    # ---- 1) determinism: r5 -> r6 chain twice -> identical registry-set sha ----
    run(R5); run(R6); s1 = registry_set_sha()
    run(R5); run(R6); s2 = registry_set_sha()
    checks.append(("determinism_chain_2x", s1 == s2,
                   f"r5->r6 chain registry-set sha {s1} == {s2}"))

    # capture R5 base then R6 (a third chain), for add-only / supersede comparison
    run(R5); r5_payload = json.load(open(SCORES_J)); r5_state = axis_state(r5_payload)
    run(R6); R6P = json.load(open(SCORES_J)); r6_state = axis_state(R6P)
    recs = R6P["records"]
    resid = json.load(open(RESID_J))

    # treatability offsets (R4/R5)
    treat = {}
    with open(os.path.join(CUR, "treatments_registry.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            treat[r["cui"]] = (float(r["efficacy_offset_e"]), float(r["R_treat"]), r["grade"])

    # ---- 2) orphanet sources pinned ----
    log = json.load(open(os.path.join(ORPHA, "_fetch_log.json")))
    prods = log.get("products", {})
    src_ok = len(prods) == 3 and all(v.get("sha_matches_pin") and v.get("disorders") for v in prods.values())
    checks.append(("orphanet_sources_pinned", src_ok,
                   f"{sum(1 for v in prods.values() if v.get('sha_matches_pin'))}/3 products match pin; "
                   + ", ".join(f"{k.split('.')[0]}={v.get('disorders')}" for k, v in prods.items())))

    # ---- 3) banked R3/R4 byte-identical ----
    bad_bank = [f for f, want in BANKED_PINS.items() if sha(os.path.join(CUR, f)) != want]
    checks.append(("banked_unchanged", not bad_bank,
                   "burden_scores/burden_residual/treatments banked digests unchanged"
                   + ("" if not bad_bank else f"; CHANGED: {bad_bank}")))

    # ---- 4) join exact only ----
    join_bad = []
    for r in recs:
        applied = r["orphanet"].get("applied")
        exact = r["orphanet"].get("exact_orphacodes") or []
        for ax in W:
            if r6_state[r["cui"]][ax][2]:  # source mentions Orphanet
                if not applied or not exact:
                    join_bad.append(f"{r['entity']}/{ax} Orphanet-sourced but no exact mapping")
    for ch in R6P.get("axis_value_changes", []):
        rr = next(x for x in recs if x["entity"] == ch["entity"])
        if not (rr["orphanet"].get("exact_orphacodes")):
            join_bad.append(f"{ch['entity']} value changed without exact mapping")
    checks.append(("join_exact_only", not join_bad,
                   f"every Orphanet-sourced axis carries an Exact OMIM<->ORPHA mapping ({len(join_bad)} bad)"))

    # ---- 5) onset tier map a-priori ----
    declared = {k: float(v) for k, v in R6P["onset_tier_map"].items()}
    map_ok = declared == {"Antenatal": 1.0, "Neonatal": 1.0, "Infancy": 0.85, "Childhood": 0.7,
                          "Adolescent": 0.55, "Adult": 0.35, "Elderly": 0.2}
    onset_val_bad = []
    for r in recs:
        o = r["components"]["O"]
        if o["grade"] == "[L]" and "Orphanet" in (o.get("source", "")):
            if o["value"] not in ONSET_TIER_VALUES:
                onset_val_bad.append(f"{r['entity']} O={o['value']}")
    checks.append(("onset_tier_map_a_priori", map_ok and not onset_val_bad,
                   f"declared map matches; every Orphanet-[L] onset value in the a-priori tier set ({len(onset_val_bad)} bad)"))

    # ---- 6) frequency gate enforced (re-derive from product4) ----
    root4 = ET.parse(os.path.join(ORPHA, "en_product4.xml")).getroot()
    hpo_by = {}
    for d in root4.iter("Disorder"):
        hpo_by[d.findtext("OrphaCode")] = {a.findtext(".//HPOId"): a.findtext(".//HPOFrequency/Name")
                                           for a in d.findall(".//HPODisorderAssociation")}
    # frozen R3 maps for the subtree check
    spec = importlib.util.spec_from_file_location("r3g", os.path.join(HERE, "r3_burden_index.py"))
    r3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r3)
    _, _, children = r3.load_obo()
    MORT = set(r3.subtree("HP:0040006", children)); COURSE = set(r3.subtree("HP:0031797", children))
    freq_bad = []
    for r in recs:
        exact = r["orphanet"].get("exact_orphacodes") or []
        for ax, sub, vmap in (("M", MORT, r3.MORT_VAL), ("P", COURSE, r3.PROG_VAL)):
            c = r["components"][ax]
            if c["grade"] == "[L]" and "Orphanet" in (c.get("source", "")):
                ok = any(fr in FREQ_OK and hid in sub and hid in vmap
                         for oc in exact for hid, fr in hpo_by.get(oc, {}).items())
                if not ok:
                    freq_bad.append(f"{r['entity']}/{ax}")
    gate_decl = set(R6P["frequency_gate"]) == FREQ_OK
    checks.append(("frequency_gate_enforced", gate_decl and not freq_bad,
                   f"declared gate = Obligate/Very frequent/Frequent; every Orphanet M/P-[L] has a "
                   f"qualifying term ({len(freq_bad)} bad)"))

    # ---- 7) add-only: no grade weakened, no scored value dropped, vs R5 base ----
    downgrade = []
    for cui in r6_state:
        for ax in W:
            v5, g5, _ = r5_state[cui][ax]; v6, g6, _ = r6_state[cui][ax]
            if GR[g6] < GR[g5]:
                downgrade.append(f"{cui}/{ax} {g5}->{g6}")
            if v5 is not None and v6 is None:
                downgrade.append(f"{cui}/{ax} value dropped")
    checks.append(("addonly_no_downgrade", not downgrade,
                   f"no axis grade weakened and no scored value removed vs R5 ({len(downgrade)} violations)"))

    # ---- 8) value changes only with Orphanet [L] backing ----
    change_bad = []
    for cui in r6_state:
        for ax in W:
            v5, g5, _ = r5_state[cui][ax]; v6, g6, o6 = r6_state[cui][ax]
            if v5 != v6:
                if not (g6 == "[L]" and o6):
                    change_bad.append(f"{cui}/{ax} {v5}->{v6} without Orphanet [L] backing")
    checks.append(("supersede_only_on_registry", not change_bad,
                   f"every axis value change is registry [L] Orphanet-backed ({len(change_bad)} bad)"))

    # ---- 9) raw_burden re-derived ----
    raw_bad = []
    for r in recs:
        present = [(ax, r["components"][ax]["value"]) for ax in W if r["components"][ax]["value"] is not None]
        exp = (sum(v for _, v in present) / len(present)) if present else None
        got = r["raw_burden"]
        if (exp is None) != (got is None) or (exp is not None and abs(exp - got) > 1e-9):
            raw_bad.append(r["entity"])
    checks.append(("raw_burden_rederived", not raw_bad,
                   f"renormalised-mean recompute matches stored raw_burden ({len(raw_bad)} mismatch)"))

    # ---- 10) rankability recomputed + promotions consistent ----
    rank_bad = [r["entity"] for r in recs if r["rankable"] != (r["axes_scored"] >= 3)]
    banked = {x["cui"]: x for x in json.load(open(os.path.join(CUR, "burden_scores.json")))["records"]}
    promo_calc = sorted(r["cui"] for r in recs if r["rankable"] and not banked[r["cui"]]["rankable"])
    promo_rec = sorted(p["cui"] for p in R6P["promotions_from_not_placed"])
    checks.append(("rankability_and_promotions", not rank_bad and promo_calc == promo_rec,
                   f"rankable == (axes>=3) for all ({len(rank_bad)} bad); promotions recompute matches "
                   f"({len(promo_rec)} promoted)"))

    # ---- 11) residual correct ----
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

    # ---- 12) order lock rule ----
    lock_bad = []
    lock_n = 0
    for r in recs:
        present = [r["components"][ax]["grade"] for ax in W if r["components"][ax]["value"] is not None]
        exp = bool(r["rankable"] and present and all(GR[g] >= GR["[L]"] for g in present))
        if exp != r["order_locked"]:
            lock_bad.append(r["entity"])
        lock_n += int(r["order_locked"])
    checks.append(("order_lock_rule", not lock_bad,
                   f"order_locked == (rankable & all scored axes [L]/[V]) for all ({lock_n} locked; {len(lock_bad)} bad)"))

    # ---- 13) sensitivity present ----
    sens = R6P["sensitivity"]
    eq = sens.get("equal_default", {}).get("spearman_vs_default")
    checks.append(("sensitivity_present", len(sens) == 5 and eq == 1.0,
                   f"{len(sens)} weightings; equal_default rho = {eq}"))

    # ---- 14) engine pin drift zero ----
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
        "phase": "R6", "kind": "investigation_gate",
        "title": "natural-history registry pass (Orphanet) — onset/mortality/progression lift",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
            "burden_scores_registry_csv":  {"path": "data/curated/burden_scores_registry.csv", "sha12": sha12(SCORES_C)},
            "burden_residual_registry_json": {"path": "data/curated/burden_residual_registry.json", "sha12": sha12(RESID_J)},
            "orphanet_fetch_log": {"path": "data/raw/orphanet/_fetch_log.json", "sha12": sha12(os.path.join(ORPHA, "_fetch_log.json"))},
        },
        "lift_counts": R6P.get("lift_counts"),
        "axis_grade_coverage_registry": R6P.get("axis_grade_coverage_registry"),
        "promotions": R6P.get("promotions_from_not_placed"),
        "order_locked": R6P.get("order_locked_diseases"),
        "registry_set_sha12": registry_set_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "r6.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"R6 GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:28s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
