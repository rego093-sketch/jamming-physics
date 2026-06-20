#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unmet-need / treatment-gap surface gate -- proves the surface is a PURE VIEW over
the R9 registry that cannot drift from it. It:
  * rebuilds the surface deterministically (2x identical sha);
  * re-derives EVERY cell from the registry independently: residual_unmet_need ==
    raw_burden * (1 - efficacy_offset_e); treatment_gap_class from evidence_status;
    burden_order_provisional == NOT order_locked; grades carried verbatim;
  * confirms the surface is sorted by residual (unmet-need) descending among placed;
  * confirms the HONEST HEADLINE set == {burden grade [L] AND evidence_status none};
  * confirms NO cure/outcome claim leaks in (the surface stores only burden,
    treatability, residual, grades, and flags -- no prognosis/timeline fields);
  * confirms the banked R3/R4 files and the engine pin are untouched (this is a
    read-only view: it must change nothing upstream).

Living code, NOT in the frozen engine pin.  Out: reports/unmet_need.gate.json
"""
import os, csv, json, sys, hashlib, subprocess, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
SCORES_J = os.path.join(CUR, "burden_scores_registry.json")
RESID_C = os.path.join(CUR, "burden_residual_registry.csv")
SURF_J = os.path.join(CUR, "unmet_need_surface.json")
SURF_C = os.path.join(CUR, "unmet_need_surface.csv")
BUILD = os.path.join(HERE, "w_unmet_need_surface.py")

BANKED_PINS = {
    "burden_scores.json":   "f8792286838c6ca2dad5a63ca301daadcbe9e26fe2710d37389dbafc324d12ee",
    "burden_residual.json": "46755e1a0d7f95877e4204e5dac6f8ba80ab8400c9e4d2e27b9b03aad4142ece",
    "treatments.json":      "0f6de1a24e2eb2a890ab0cb574317f6ba46aadd3a09b84ddce52a6470f8dddb5",
}
GAP_CLASS = {
    "none": "no_disease_directed_therapy",
    "symptomatic": "symptomatic_only",
    "disease-modifying (partial)": "partial_disease_modifying",
    "disease-modifying (substantial)": "substantial_disease_modifying",
    "curative / effectively normalizing": "curative_or_normalizing",
    "curative": "curative_or_normalizing",
}
# fields that would betray a forbidden cure/outcome/prognosis claim
FORBIDDEN_FIELDS = {"cure", "cured", "prognosis", "outcome", "timeline", "survival_prediction",
                    "will_cure", "expected_outcome", "individual_prognosis"}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def sha12(p):
    return sha(p)[:12] if os.path.exists(p) else None


def surface_sha():
    h = hashlib.sha256()
    for p in (SURF_C, SURF_J):
        h.update(open(p, "rb").read())
    return h.hexdigest()[:12]


def main():
    checks = []

    # ---- 1) determinism: build twice -> identical ----
    subprocess.run([sys.executable, BUILD], check=True, stdout=subprocess.DEVNULL)
    s1 = surface_sha()
    subprocess.run([sys.executable, BUILD], check=True, stdout=subprocess.DEVNULL)
    s2 = surface_sha()
    checks.append(("determinism_2x", s1 == s2, f"surface sha {s1} == {s2}"))

    surf = json.load(open(SURF_J))
    rows = surf["records"]
    scores = json.load(open(SCORES_J))
    locked = {r["cui"]: bool(r.get("order_locked")) for r in scores["records"]}
    reg_by_cui = {r["cui"]: r for r in scores["records"]}
    resid = {r["cui"]: r for r in csv.DictReader(open(RESID_C, newline=""))}

    # ---- 2) every cell re-derived from the registry ----
    cell_bad = []
    for x in rows:
        cui = x["cui"]
        sc = reg_by_cui[cui]
        rr = resid[cui]
        raw = sc["raw_burden"]
        Rt = round(sc["treatability"]["value"], 12)
        e = round(1.0 - Rt, 12)
        exp_resid = round(raw * (1 - e), 12) if raw is not None else None
        got = x["residual_unmet_need"]
        # residual must equal raw*(1-e) AND the registry burden_score (pure view, no drift)
        if (exp_resid is None) != (got is None) or (exp_resid is not None and abs(exp_resid - got) > 1e-9):
            cell_bad.append(f"{x['entity']} residual {got} != raw*(1-e) {exp_resid}")
        if sc["burden_score"] is not None and got is not None and abs(sc["burden_score"] - got) > 1e-9:
            cell_bad.append(f"{x['entity']} residual {got} != registry burden_score {sc['burden_score']}")
        if x["treatment_gap_class"] != GAP_CLASS.get(x["evidence_status"], "unknown"):
            cell_bad.append(f"{x['entity']} gap_class wrong for evidence_status {x['evidence_status']}")
        if x["burden_order_provisional"] == locked[cui]:
            cell_bad.append(f"{x['entity']} provisional flag != (not order_locked)")
        if x["order_locked"] != locked[cui]:
            cell_bad.append(f"{x['entity']} order_locked mismatch vs registry")
        if x["burden_grade"] != sc["raw_burden_grade_present"]:
            cell_bad.append(f"{x['entity']} burden_grade != registry")
        if x["residual_grade"] != sc["burden_score_grade"]:
            cell_bad.append(f"{x['entity']} residual_grade != registry")
        if x["treatment_grade"] != sc["treatment_grade"]:
            cell_bad.append(f"{x['entity']} treatment_grade != registry")
        if x["evidence_status"] != rr["evidence_status"]:
            cell_bad.append(f"{x['entity']} evidence_status != residual registry")
    checks.append(("cells_rederived_from_registry", not cell_bad,
                   f"residual=raw*(1-e)=registry burden_score, gap_class, provisional flag, and all grades "
                   f"re-derived from the registry for all {len(rows)} rows ({len(cell_bad)} bad)"))

    # ---- 3) sorted by residual (unmet-need) descending among placed ----
    placed = [x for x in rows if x["rankable"]]
    mono = all((placed[i]["residual_unmet_need"] or -1) >= (placed[i + 1]["residual_unmet_need"] or -1) - 1e-12
               for i in range(len(placed) - 1))
    ranks_ok = all(placed[i]["unmet_rank"] == i + 1 for i in range(len(placed)))
    checks.append(("sorted_by_residual_desc", mono and ranks_ok,
                   f"placed surface monotone non-increasing in residual unmet-need; unmet_rank contiguous "
                   f"({len(placed)} placed)"))

    # ---- 4) honest headline == {burden [L] AND evidence_status none} ----
    exp_headline = sorted(x["entity"] for x in rows
                          if x["burden_grade"] == "[L]" and x["evidence_status"] == "none")
    got_headline = sorted(x["entity"] for x in rows if x["headline_unmet_need"])
    rec_headline = sorted(surf["headline_unmet_need_diseases"])
    checks.append(("headline_rule_exact", exp_headline == got_headline == rec_headline,
                   f"headline (burden [L] + no disease-directed therapy) = {got_headline}"))

    # ---- 5) no forbidden cure/outcome/prognosis field leaks in ----
    keys = set()
    for x in rows:
        keys |= {k.lower() for k in x.keys()}
    leak = sorted(keys & FORBIDDEN_FIELDS)
    text_blob = json.dumps(surf).lower()
    claim_leak = any(p in text_blob for p in ("will cure", "guaranteed", "we cured", "promise a cure"))
    checks.append(("no_cure_or_outcome_claim", not leak and not claim_leak,
                   f"surface carries only burden/treatability/residual/grades/flags; no prognosis/outcome field "
                   f"({'leak: ' + ', '.join(leak) if leak else 'none'})"))

    # ---- 6) read-only: banked files + engine pin untouched ----
    bad_bank = [f for f, want in BANKED_PINS.items() if sha(os.path.join(CUR, f)) != want]
    pin_bad, pin_n = [], 0
    for line in open(MANIFEST, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        want, rel = line.split(None, 1); pin_n += 1
        p = os.path.join(ROOT, rel.strip())
        if not os.path.exists(p) or sha(p) != want:
            pin_bad.append(rel)
    checks.append(("read_only_no_upstream_change", not bad_bank and not pin_bad,
                   f"banked R3/R4 byte-identical ({len(bad_bank)} changed); engine pin drift 0 "
                   f"({pin_n - len(pin_bad)}/{pin_n})"))

    passed = sum(1 for _, ok, _ in checks if ok)
    total = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "W-unmet-need", "kind": "view_gate",
        "title": "unmet-need / treatment-gap surface — pure graded view over the R9 registry",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "unmet_need_surface_json": {"path": "data/curated/unmet_need_surface.json", "sha12": sha12(SURF_J)},
            "unmet_need_surface_csv": {"path": "data/curated/unmet_need_surface.csv", "sha12": sha12(SURF_C)},
            "burden_scores_registry_json": {"path": "data/curated/burden_scores_registry.json", "sha12": sha12(SCORES_J)},
        },
        "headline_unmet_need_diseases": surf.get("headline_unmet_need_diseases"),
        "surface_sha12": surface_sha(),
        "summary": f"{passed}/{total} checks PASS",
        "verdict": verdict,
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
    }
    os.makedirs(os.path.join(ROOT, "reports"), exist_ok=True)
    json.dump(report, open(os.path.join(ROOT, "reports", "unmet_need.gate.json"), "w"), indent=2, ensure_ascii=False)

    print(f"UNMET-NEED SURFACE GATE: {verdict}  ({passed}/{total})")
    for n, ok, d in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {n:34s} {d}")
    if verdict != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
