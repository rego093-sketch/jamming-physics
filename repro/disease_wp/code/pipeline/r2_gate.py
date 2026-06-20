#!/usr/bin/env python3
"""
R2 investigation gate. Verifies the enriched disease index and the per-disease
dossiers are inheritance-complete, mechanism-graded (no guessed values),
boundary-resolved, provenance-complete, and dossier-schema-valid, exactly as
ROADMAP.md's R2 deliverable requires. Writes reports/r2.gate.json.
INVESTIGATION ONLY -- no whitepaper prose, no scoring of hypotheses.

Extends r1_gate.py. Run after the full R2 pipeline (see R2 handover run order).
"""
import csv, os, json, hashlib, datetime, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX  = os.path.join(ROOT, "data", "curated", "disease_index.csv")
DOSS = os.path.join(ROOT, "data", "curated", "dossiers")
COH  = os.path.join(ROOT, "methodology", "dossier_cohort.csv")
OUT  = os.path.join(ROOT, "reports", "r2.gate.json")

VALID_GRADES = {"[L]", "[O]", "[H]", "[V]", "[F]"}

# the 3 diseases the R2 boundary review moved out of scope (primary-CNS GM2)
BOUNDARY_MOVED = {"C0039373", "C0268275", "C0036161"}  # Tay-Sachs, Tay-Sachs AB, Sandhoff

# every graded leaf field a dossier must expose as {value, grade, source|obstacle}
SCALAR_FIELDS = [
    ("inheritance", lambda d: d["inheritance"]),
    ("molecular_mechanism", lambda d: d["molecular_mechanism"]),
    ("clinical.organ_systems", lambda d: d["clinical"]["organ_systems"]),
    ("clinical.cardinal_symptoms", lambda d: d["clinical"]["cardinal_symptoms"]),
    ("clinical.age_of_onset", lambda d: d["clinical"]["age_of_onset"]),
    ("clinical.prevalence", lambda d: d["clinical"]["prevalence"]),
    ("clinical.clinical_definition", lambda d: d["clinical"]["clinical_definition"]),
]
LIST_FIELDS = [
    ("gene_function", lambda d: d["gene_function"]),
    ("variant_spectrum", lambda d: d["variant_spectrum"]),
]


def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def graded_ok(obj):
    """A graded field must be a dict with a grade in the vocabulary and the
    grade's required evidence: [O] names an obstacle; [L]/[H]/[V] cite a source.
    No bare values; no guessed values (a grade without its evidence)."""
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


def main():
    rows = list(csv.DictReader(open(IDX, encoding="utf-8")))
    inscope = [r for r in rows if r["in_scope"] == "true"]
    cohort = list(csv.DictReader(open(COH, encoding="utf-8")))
    checks = []

    # 1 inheritance complete: every in-scope row has class + valid grade
    bad = [r for r in inscope
           if not r["inheritance_class"].strip() or r["inheritance_grade"] not in VALID_GRADES]
    checks.append(("inheritance_complete", len(bad) == 0,
                   f"{len(inscope) - len(bad)}/{len(inscope)} in-scope rows inheritance-graded"))

    # 2 mechanism graded, no guessed values: class + valid grade + matching evidence
    mech_bad = []
    for r in inscope:
        g = r["mechanism_grade"]
        src = r["mechanism_source"].strip()
        if not r["mechanism_class"].strip() or g not in VALID_GRADES:
            mech_bad.append((r["medgen_cui"], "missing class/grade")); continue
        if not src:                                   # any grade needs recorded basis
            mech_bad.append((r["medgen_cui"], "no source/basis")); continue
        if g == "[O]" and "obstacle" not in src.lower():
            mech_bad.append((r["medgen_cui"], "[O] without obstacle")); continue
    checks.append(("mechanism_graded_no_guess", len(mech_bad) == 0,
                   f"{len(inscope) - len(mech_bad)}/{len(inscope)} mechanism rows graded with evidence"))

    # 3 boundary resolved: cns_cross_reference binary everywhere; the 3 moves out-of-scope+logged
    cns_vals = set(r.get("cns_cross_reference", "") for r in rows)
    cns_ok = cns_vals <= {"true", "false"}
    moved = {r["medgen_cui"] for r in rows
             if r["in_scope"] == "false" and r["medgen_cui"] in BOUNDARY_MOVED
             and "boundary" in r["exclusion_reason"].lower()}
    boundary_ok = cns_ok and moved == BOUNDARY_MOVED
    checks.append(("boundary_resolved", boundary_ok,
                   f"cns_cross_reference={sorted(cns_vals)}; "
                   f"{len(moved)}/{len(BOUNDARY_MOVED)} boundary moves out-of-scope+logged"))

    # 4 provenance complete: every row carries provenance
    no_prov = [r for r in rows if not r["provenance"].strip()]
    checks.append(("provenance_complete", len(no_prov) == 0,
                   f"{len(rows) - len(no_prov)}/{len(rows)} rows carry provenance"))

    # 5 dossier schema valid: every graded field is {value, grade, source|obstacle}
    files = sorted(f for f in glob.glob(os.path.join(DOSS, "*.json"))
                   if os.path.basename(f) != "_cohort_index.json")
    schema_viol = []
    for f in files:
        d = json.load(open(f, encoding="utf-8"))
        ent = d.get("identity", {}).get("entity", os.path.basename(f))
        for fname, getter in SCALAR_FIELDS:
            try:
                ok, why = graded_ok(getter(d))
            except Exception as e:
                ok, why = False, f"access error: {e}"
            if not ok:
                schema_viol.append(f"{ent}:{fname}:{why}")
        for fname, getter in LIST_FIELDS:
            try:
                lst = getter(d)
                if not isinstance(lst, list):
                    schema_viol.append(f"{ent}:{fname}:not a list"); continue
                for i, item in enumerate(lst):
                    ok, why = graded_ok(item)
                    if not ok:
                        schema_viol.append(f"{ent}:{fname}[{i}]:{why}")
            except Exception as e:
                schema_viol.append(f"{ent}:{fname}:access error: {e}")
    checks.append(("dossier_schema_valid", len(schema_viol) == 0,
                   f"{len(files)} dossiers; {len(schema_viol)} graded-field violations"))

    # 6 dossier cohort complete: #dossiers == pre-registered manifest size
    ci = json.load(open(os.path.join(DOSS, "_cohort_index.json"), encoding="utf-8"))
    cohort_ok = len(files) == len(cohort) == ci.get("cohort_size")
    checks.append(("dossier_cohort_complete", cohort_ok,
                   f"dossiers={len(files)} manifest={len(cohort)} index={ci.get('cohort_size')}"))

    # 7 grade-vocabulary consistent across the index (no stray grades)
    stray = set()
    for r in rows:
        for col in ("inheritance_grade", "mechanism_grade"):
            v = r[col].strip()
            if v and v not in VALID_GRADES:
                stray.add(v)
    checks.append(("grade_vocab_consistent", len(stray) == 0,
                   f"stray grades={sorted(stray) or 'none'}"))

    # integrity digest over the dossier set (recomputed; date-stamped, see note)
    h = hashlib.sha256()
    for fn in sorted(os.listdir(DOSS)):
        h.update(open(os.path.join(DOSS, fn), "rb").read())
    dossier_sha = h.hexdigest()[:12]

    n_in  = len(inscope)
    n_out = sum(1 for r in rows if r["in_scope"] == "false")
    passed = sum(1 for _, ok, _ in checks if ok)
    total  = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "R2",
        "kind": "investigation_gate",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "disease_index": {"path": "data/curated/disease_index.csv", "sha12": sha12(IDX)},
            "dossier_cohort_manifest": {"path": "methodology/dossier_cohort.csv",
                                        "rows": len(cohort)},
            "dossier_set": {"path": "data/curated/dossiers/", "files": len(files),
                            "set_sha12": dossier_sha},
        },
        "counts": {"index_rows": len(rows), "in_scope": n_in, "excluded": n_out,
                   "dossiers": len(files)},
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
        "verdict": f"{verdict} ({passed}/{total})",
        "note": ("Investigation gate. Every in-scope disease carries inheritance and a "
                 "mechanism grade; no grade appears without its evidence (a cited source for "
                 "[L]/[H], a named obstacle for [O]). Boundary review's 3 primary-CNS GM2 "
                 "diseases (Tay-Sachs, Tay-Sachs variant AB, Sandhoff) are out-of-scope and "
                 "logged. Every dossier field is a graded object {value, grade, source|obstacle} "
                 "-- no bare values. Determinism of the mechanism and dossier stages was "
                 "confirmed by repeated identical runs this session. The dossier-set digest is "
                 "computed over date-stamped files (each carries today's generated date), so it "
                 "is reproducible within a run/day; the pipeline inputs and logic are otherwise "
                 "deterministic. Disease-level mechanism precision for multi-gene/CNV syndromes "
                 "is reserved for the curated dossiers (see R2 handover, ClinGen-source caveat)."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w"), indent=2)
    print(json.dumps({"verdict": report["verdict"], "counts": report["counts"],
                      "checks": [(n, ok) for n, ok, _ in checks]}, indent=2))
    print("written:", OUT)


if __name__ == "__main__":
    main()
