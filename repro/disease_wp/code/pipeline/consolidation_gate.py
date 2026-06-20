#!/usr/bin/env python3
"""
CONSOLIDATION GATE -- "stop investigating, start writing".

This is the meta-gate that certifies the R1-R4 investigation is ready to pivot to
VP-SPEC-governed Phase W1 authoring (ROADMAP.md "CONSOLIDATION GATE"). It does NOT
introduce new facts and writes NO whitepaper prose. It re-derives, independently of any
recorded digest, that the four R-phase datasets jointly satisfy the four ROADMAP gate
criteria, plus the handover's Erratum-E1 confirmation sweep and the governed engine pin.

ROADMAP criteria certified here:
  1. Provenance-complete -- every fact carries source DB + accession + retrieval date
     (non-[O] field -> non-empty source; [O] field -> named obstacle; [L]/[V] dossier
     sources carry a date or accession token).
  2. Internally consistent -- inheritance / mechanism / gene classes agree across
     disease_index, dossiers, treatments, and burden; the 35-disease cohort identity is
     the same CUI set in all four curated artifacts.
  3. Grade-complete -- every quantitative/factual field carries a grade from the
     vocabulary; unavailable values are [O] (with obstacle), never guessed; the
     _cohort_index field_grades summary matches the actual dossier grades (no drift).
  4. Scope-clean -- no excluded entity leaked into the cohort; every cohort entity is
     in_scope in both its dossier and the index; cohort primary systems in the OUT set
     carry a recorded cross-reference; every index exclusion is logged with a reason.

It also SUBSUMES the four investigation gates: it re-runs r1/r2/r3/r4 gates as
subprocesses and asserts each prints PASS, so a single green consolidation gate means the
whole investigation is reproducibly green at the pivot point. Writes
reports/consolidation.gate.json.

INVESTIGATION-CONSOLIDATION ONLY -- no prose, no new claims, no scoring of hypotheses.
Mirrors r4_gate.py conventions. Run after r4_treatment_survey.py + r4_burden_residual.py.
"""
import os, re, json, csv, hashlib, datetime, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
DOSS = os.path.join(CUR, "dossiers")
COHORT_IX = os.path.join(DOSS, "_cohort_index.json")
DINDEX = os.path.join(CUR, "disease_index.csv")
TREAT_JSON = os.path.join(CUR, "treatments.json")
BSC_JSON = os.path.join(CUR, "burden_scores.json")
BRES_JSON = os.path.join(CUR, "burden_residual.json")
MANIFEST = os.path.join(ROOT, "MANIFEST_governed.sha256")
OUT = os.path.join(ROOT, "reports", "consolidation.gate.json")

R_GATES = ["r1_gate.py", "r2_gate.py", "r3_gate.py", "r4_gate.py"]
COHORT_N = 35
VALID_GRADES = {"[L]", "[O]", "[H]", "[V]", "[F]"}
VALID_STATUS = {"curative", "disease-modifying (substantial)",
                "disease-modifying (partial)", "symptomatic", "none"}
# primary-system tokens owned by the sibling neuro/mind whitepapers (SCOPE.md OUT list)
OUT_PRIMARY = ("brain", "nerve", "neuro", "neurological", "neurodegenerat",
               "cardiac", "heart", "channelopath", "cardiomyopath",
               "psychiatric", "affect", "mood")
DATE = re.compile(r"20\d\d-\d\d-\d\d|v20\d\d-\d\d-\d\d")
ACC = re.compile(r"OMIM|MedGen|ClinVar|HPO|hpoa|NCBI|PMID|Gene:|RefSeq|conceptmeta|"
                 r"esummary|clingen|ClinGen|GeneReviews|FDA|Orphanet|hp\.obo|"
                 r"phenotype\.hpoa|ModeOfInheritance|inference", re.I)


def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def S(x):
    return x if isinstance(x, str) else ("" if x is None else str(x))


def load_dossiers():
    out = {}
    for fn in os.listdir(DOSS):
        if not fn.endswith(".json") or fn.startswith("_"):
            continue
        d = json.load(open(os.path.join(DOSS, fn), encoding="utf-8"))
        out[d["identity"]["medgen_cui"]] = (fn, d)
    return out


def field_provenance_problem(entity, fld, obj, require_token=False):
    """Return a problem string for one {value, grade, source/obstacle} field, else None."""
    g = obj.get("grade")
    if g not in VALID_GRADES:
        return f"{entity}:{fld}:grade {g!r} outside vocabulary"
    if g == "[O]":
        if not (S(obj.get("obstacle")).strip() or S(obj.get("basis")).strip()):
            return f"{entity}:{fld}:[O] without named obstacle"
        return None
    src = S(obj.get("source")).strip() or S(obj.get("basis")).strip()
    if not src:
        return f"{entity}:{fld}:{g} without recorded source/basis"
    if require_token and g in ("[L]", "[V]") and not (DATE.search(src) or ACC.search(src)):
        return f"{entity}:{fld}:{g} source lacks date/accession ({src[:48]!r})"
    return None


def main():
    dossiers = load_dossiers()
    ci = json.load(open(COHORT_IX, encoding="utf-8"))
    cohort_ix = {d["cui"]: d for d in ci["dossiers"]}
    treat = {r["cui"]: r for r in json.load(open(TREAT_JSON, encoding="utf-8"))["records"]}
    bsc = {r["cui"]: r for r in json.load(open(BSC_JSON, encoding="utf-8"))["records"]}
    bres = {r["cui"]: r for r in json.load(open(BRES_JSON, encoding="utf-8"))["records"]}
    idx_rows = list(csv.DictReader(open(DINDEX, newline="", encoding="utf-8")))
    idx = {r["medgen_cui"]: r for r in idx_rows}

    checks = []

    # 0 SUBSUME: re-run the four investigation gates; each must print PASS.
    gate_status = []
    for g in R_GATES:
        r = subprocess.run([sys.executable, os.path.join(HERE, g)],
                           capture_output=True, text=True)
        ok = ("PASS" in r.stdout) and ("FAIL" not in r.stdout.split("verdict")[-1][:40] if "verdict" in r.stdout else "PASS" in r.stdout)
        # robust verdict read from the gate's own report file
        rep = os.path.join(ROOT, "reports", g.replace("_gate.py", ".gate.json"))
        verdict = json.load(open(rep, encoding="utf-8")).get("verdict", "?") if os.path.exists(rep) else "?"
        gate_status.append((g, verdict))
        ok = verdict.startswith("PASS")
        if not ok:
            gate_status.append((g, "NON-PASS"))
    all_green = all(v.startswith("PASS") for _, v in gate_status)
    checks.append(("r_phase_gates_all_pass", all_green,
                   "R1-R4 gates re-run: " + ", ".join(f"{g.split('_')[0]}={v}" for g, v in gate_status)))

    # 1 COHORT IDENTITY CONSISTENT: same 35 CUI set across all four curated artifacts,
    #   all present in disease_index.
    sets = {"dossiers": set(dossiers), "cohort_index": set(cohort_ix),
            "treatments": set(treat), "burden_scores": set(bsc), "burden_residual": set(bres)}
    base = set(dossiers)
    same = all(s == base for s in sets.values())
    sizes_ok = all(len(s) == COHORT_N for s in sets.values())
    in_index = [c for c in base if c not in idx]
    checks.append(("cohort_identity_consistent_35",
                   same and sizes_ok and not in_index,
                   f"{COHORT_N}-disease cohort CUI set identical across dossiers/cohort_index/"
                   f"treatments/burden_scores/burden_residual={same}; all n={COHORT_N}={sizes_ok}; "
                   f"all present in disease_index={not in_index}"
                   + ("" if not in_index else f"; missing {in_index[:3]}")))

    # 2 PROVENANCE-COMPLETE (ROADMAP #1): every graded field in every dossier, treatment,
    #   and burden axis carries source(non-[O]) / obstacle([O]); [L]/[V] dossier sources
    #   carry a date or accession token.
    prob = []
    for cui, (fn, d) in dossiers.items():
        e = d["identity"]["entity"]
        for fld in ("inheritance", "molecular_mechanism"):
            p = field_provenance_problem(e, fld, d[fld], require_token=True)
            if p: prob.append(p)
        for i, gf in enumerate(d.get("gene_function", [])):
            p = field_provenance_problem(e, f"gene_function[{i}]", gf, require_token=True)
            if p: prob.append(p)
        for i, vs in enumerate(d.get("variant_spectrum", [])):
            p = field_provenance_problem(e, f"variant_spectrum[{i}]", vs, require_token=True)
            if p: prob.append(p)
        cl = d.get("clinical", {})
        for fld in ("organ_systems", "cardinal_symptoms", "age_of_onset",
                    "prevalence", "clinical_definition"):
            if fld in cl:
                p = field_provenance_problem(e, f"clinical.{fld}", cl[fld], require_token=True)
                if p: prob.append(p)
    for cui, r in treat.items():
        for fld in ("modality", "mechanism"):
            p = field_provenance_problem(r["entity"], f"treat.{fld}", r[fld])
            if p: prob.append(p)
    for cui, r in bsc.items():
        for ax, obj in r.get("components", {}).items():
            p = field_provenance_problem(r["entity"], f"burden.{ax}", obj)
            if p: prob.append(p)
    checks.append(("provenance_complete", len(prob) == 0,
                   f"every graded field across {len(dossiers)} dossiers + {len(treat)} treatments "
                   f"+ burden axes carries source/obstacle (and [L]/[V] dossier sources carry a "
                   f"date/accession token); {len(prob)} violations"
                   + ("" if not prob else f"; first: {prob[0]}")))

    # 3 GRADE-COMPLETE (ROADMAP #3): every field grade in vocabulary; the _cohort_index
    #   field_grades summary matches the actual dossier grades (no summary drift).
    drift = []
    summary_map = {"inheritance": ("inheritance", "grade"),
                   "mechanism": ("molecular_mechanism", "grade"),
                   "gene_function": ("gene_function", None),
                   "variant_spectrum": ("variant_spectrum", None),
                   "organ_systems": ("clinical", "organ_systems"),
                   "cardinal_symptoms": ("clinical", "cardinal_symptoms"),
                   "age_of_onset": ("clinical", "age_of_onset"),
                   "prevalence": ("clinical", "prevalence")}
    for cui, c in cohort_ix.items():
        _, d = dossiers[cui]
        for fld, want in c.get("field_grades", {}).items():
            if want not in VALID_GRADES:
                drift.append(f"{c['entity']}:{fld}:summary grade {want!r} outside vocabulary"); continue
            path = summary_map.get(fld)
            if not path:
                continue
            top, sub = path
            node = d.get(top)
            if isinstance(node, list):  # gene_function / variant_spectrum: list of graded records
                got = node[0].get("grade") if node else None
            elif sub in (None,):
                got = node.get("grade") if isinstance(node, dict) else None
            elif top == "clinical":
                got = node.get(sub, {}).get("grade")
            else:
                got = node.get(sub)
            if got != want:
                drift.append(f"{c['entity']}:{fld}: summary {want} != dossier {got}")
    checks.append(("grade_complete_no_summary_drift", len(drift) == 0,
                   f"all field grades in vocabulary and _cohort_index field_grades match the "
                   f"dossiers; {len(drift)} drifts"
                   + ("" if not drift else f"; first: {drift[0]}")))

    # 4 INTERNALLY CONSISTENT (ROADMAP #2): inheritance / mechanism / gene agree across
    #   disease_index <-> dossier (where the index value is curated, not [O]/not_stated);
    #   gene set agrees dossier <-> treatments <-> burden.
    inc = []
    for cui, (fn, d) in dossiers.items():
        e = d["identity"]["entity"]; row = idx.get(cui, {})
        inh_d = S(d["inheritance"]["value"]).strip().lower()
        inh_i = S(row.get("inheritance_class")).strip().lower()
        if inh_i and inh_i not in ("not_stated",) and not inh_i.startswith("[o]") and inh_d and inh_i != inh_d:
            inc.append(f"{e}: inheritance index({inh_i!r}) != dossier({inh_d!r})")
        mech_d = S(d["molecular_mechanism"]["value"]).strip().lower()
        mech_i = S(row.get("mechanism_class")).strip().lower()
        if mech_i and "not_curated" not in mech_i and not mech_i.startswith("[o]") and mech_d and mech_i != mech_d:
            inc.append(f"{e}: mechanism index({mech_i!r}) != dossier({mech_d!r})")
        genes_d = set(S(g).strip() for g in d["identity"].get("genes", []) if S(g).strip())
        genes_i = set(g.strip() for g in re.split(r"[;,]", S(row.get("genes"))) if g.strip())
        if genes_i and genes_d and genes_i != genes_d:
            inc.append(f"{e}: gene-set index({sorted(genes_i)}) != dossier({sorted(genes_d)})")
        gene_t = S(treat.get(cui, {}).get("gene")).strip()
        if gene_t and genes_d and gene_t not in genes_d:
            inc.append(f"{e}: treatments gene({gene_t!r}) not in dossier gene-set {sorted(genes_d)}")
        genes_b = set(S(g).strip() for g in bsc.get(cui, {}).get("genes", []) if S(g).strip())
        if genes_b and genes_d and genes_b != genes_d:
            inc.append(f"{e}: burden gene-set({sorted(genes_b)}) != dossier({sorted(genes_d)})")
    checks.append(("class_consistency_cross_artifact", len(inc) == 0,
                   f"inheritance/mechanism/gene agree across disease_index, dossiers, treatments, "
                   f"burden for all {len(dossiers)} cohort entities; {len(inc)} inconsistencies"
                   + ("" if not inc else f"; first: {inc[0]}")))

    # 5 SCOPE-CLEAN (ROADMAP #4): every cohort entity in_scope in dossier AND index;
    #   cohort primary systems in the OUT set carry a recorded cross-reference.
    sc = []
    for cui, (fn, d) in dossiers.items():
        e = d["identity"]["entity"]
        if d["identity"].get("in_scope") is not True:
            sc.append(f"{e}: dossier in_scope != true")
        if S(idx.get(cui, {}).get("in_scope")).strip().lower() != "true":
            sc.append(f"{e}: disease_index in_scope != true")
        sysc = S(d["identity"].get("system_class")).lower()
        xref = S(d["identity"].get("cns_cross_reference")).strip().lower()
        if any(tok in sysc for tok in OUT_PRIMARY) and xref in ("", "false"):
            sc.append(f"{e}: primary system {sysc!r} in OUT list without cross-reference")
    checks.append(("scope_clean_cohort", len(sc) == 0,
                   f"all {len(dossiers)} cohort entities in_scope in dossier+index, no OUT primary "
                   f"system leaked without cross-reference; {len(sc)} violations"
                   + ("" if not sc else f"; first: {sc[0]}")))

    # 6 EXCLUSIONS LOGGED (SCOPE.md "name it, don't hide it"): every disease_index row with
    #   in_scope=false carries a non-empty exclusion_reason -- no silent drops.
    exc_missing = [r["entity"] for r in idx_rows
                   if S(r.get("in_scope")).strip().lower() == "false"
                   and not S(r.get("exclusion_reason")).strip()]
    n_false = sum(1 for r in idx_rows if S(r.get("in_scope")).strip().lower() == "false")
    checks.append(("exclusions_logged_not_dropped", len(exc_missing) == 0,
                   f"{n_false} disease_index in_scope=false rows, all carry an exclusion_reason; "
                   f"{len(exc_missing)} unlogged"
                   + ("" if not exc_missing else f"; first: {exc_missing[0]}")))

    # 7 ERRATUM-E1 CONFIRMATION SWEEP: every dossier gene_function official symbol is in
    #   that dossier's cohort gene set (the FAH/FANCA alias-collision class; the new
    #   gene_info() guard enforces this on rebuild -- here it is a standing confirmation).
    gf = []
    for cui, (fn, d) in dossiers.items():
        e = d["identity"]["entity"]
        cohort_genes = set(S(g).strip() for g in d["identity"].get("genes", []) if S(g).strip())
        for entry in d.get("gene_function", []):
            sym = S(entry.get("value", {}).get("gene")).strip()
            if sym and sym not in cohort_genes:
                gf.append(f"{e}: gene_function symbol {sym!r} not in cohort gene set {sorted(cohort_genes)}")
    checks.append(("gene_function_symbol_sweep", len(gf) == 0,
                   f"every dossier gene_function official symbol matches its cohort gene symbol "
                   f"(Erratum-E1 alias-collision guard, confirmation sweep); {len(gf)} mismatches"
                   + ("" if not gf else f"; first: {gf[0]}")))

    # 8 NO FABRICATED CURE (constitution C-D3), re-asserted at consolidation: no treatments
    #   row claims a curative class at the disease level, no row claims [L] (still [H]),
    #   and the residual grade is [H] (not overclaimed).
    cure = []
    for cui, r in treat.items():
        st = S(r.get("evidence_status")).strip()
        if st not in VALID_STATUS:
            cure.append(f"{r['entity']}: evidence_status {st!r} outside vocabulary")
        if st == "curative":
            cure.append(f"{r['entity']}: disease-level curative class assigned (C-D3 forbids)")
        for fld in ("modality", "mechanism"):
            if r[fld].get("grade") == "[L]":
                cure.append(f"{r['entity']}:{fld} claims [L] (treatment evidence is still [H]; "
                            "accession-dated [L] pass deferred)")
    for cui, r in bres.items():
        g = r.get("burden_score_grade")
        if g not in (None, "[H]", "[O]"):
            cure.append(f"{r['entity']}: residual grade {g!r} overclaimed (expected [H]/[O])")
    checks.append(("treatability_no_fabricated_cure", len(cure) == 0,
                   f"no disease-level curative class, no treatment row claims [L], residual grade "
                   f"is [H] (provisional); {len(cure)} violations"
                   + ("" if not cure else f"; first: {cure[0]}")))

    # 9 ENGINE PIN DRIFT ZERO: re-verify the governed emergence-engine manifest.
    pin_bad, pin_n = [], 0
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
        "phase": "CONSOLIDATION",
        "kind": "consolidation_gate",
        "generated": datetime.date.today().isoformat(),
        "subsumes": ["r1.gate.json", "r2.gate.json", "r3.gate.json", "r4.gate.json"],
        "inputs": {
            "disease_index":   {"path": "data/curated/disease_index.csv",        "sha12": sha12(DINDEX)},
            "cohort_index":    {"path": "data/curated/dossiers/_cohort_index.json","sha12": sha12(COHORT_IX)},
            "treatments_json": {"path": "data/curated/treatments.json",           "sha12": sha12(TREAT_JSON)},
            "burden_scores":   {"path": "data/curated/burden_scores.json",        "sha12": sha12(BSC_JSON)},
            "burden_residual": {"path": "data/curated/burden_residual.json",      "sha12": sha12(BRES_JSON)},
        },
        "counts": {
            "cohort_size": len(dossiers),
            "disease_index_rows": len(idx_rows),
            "disease_index_excluded_rows": n_false,
            "r_phase_gate_verdicts": {g.split("_")[0]: v for g, v in gate_status},
        },
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
        "verdict": f"{verdict} ({passed}/{total})",
        "w1_readiness_decision": (
            "READY to enter Phase W1. The two deferred [L] passes are NOT consolidation "
            "prerequisites -- they are accuracy UPGRADES, not gate criteria. They are scheduled as "
            "EARLY-W1 tasks: (1) treatment accession-dating (pin each of the 35 therapies to an FDA "
            "label / GeneReviews Management / OMIM clinical management / Orphanet accession+date, "
            "lifting treatments.csv grades [H]->[L] where confirmed) and (2) the natural-history "
            "registry pass (lift burden P/S/M/D axes [H]->[L]/[V]). UNTIL both land, any W-phase prose "
            "MUST carry the burden and residual ORDER as a provisional [H]-grade prioritisation device, "
            "not a registry-locked ranking. This is the explicit, recorded W1-entry condition."
        ),
        "note": (
            "Consolidation gate -- the explicit R->W pivot. It writes no whitepaper prose and "
            "introduces no new facts; it re-derives, independently of any recorded digest, that the "
            "R1-R4 datasets jointly meet the four ROADMAP criteria (provenance-complete, internally "
            "consistent, grade-complete, scope-clean), plus the Erratum-E1 gene_function official-symbol "
            "confirmation sweep and constitution C-D3 (no fabricated cure). It SUBSUMES the four "
            "investigation gates by re-running them and asserting each PASSes, and re-verifies the "
            "governed emergence-engine pin drift-zero. HONESTY/SCOPE: clinical facts from NCBI are "
            "observed inputs (C-D1) -- respected and cited, never 'reproduced'; the reproducible layer "
            "is the analysis (classification, burden index, residual offset). Treatment evidence is [H] "
            "(cited text / established science), and the burden order is [H]-grade provisional, until "
            "the two deferred [L] passes (the W1-readiness decision above) complete."
        ),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2)
    print(json.dumps({"verdict": report["verdict"],
                      "checks": [(n, ok) for n, ok, _ in checks]}, indent=2))
    print("written:", OUT)


if __name__ == "__main__":
    main()
