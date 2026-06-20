#!/usr/bin/env python3
"""
R1 investigation gate. Verifies the base index is provenance-complete,
deduplicated, and scope-logged, exactly as ROADMAP.md's R1 gate requires.
Writes reports/r1.gate.json. INVESTIGATION ONLY.
"""
import csv, os, json, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX  = os.path.join(ROOT, "data", "curated", "disease_index_base.csv")
RAW  = os.path.join(ROOT, "data", "raw", "clinvar", "gene_condition_source_id.tsv")
OUT  = os.path.join(ROOT, "reports", "r1.gate.json")


def sha12(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def main():
    rows = list(csv.DictReader(open(IDX, encoding="utf-8")))
    checks = []

    # 1 provenance complete
    no_prov = [r for r in rows if not r["provenance"].strip()]
    checks.append(("provenance_complete", len(no_prov) == 0,
                   f"{len(rows) - len(no_prov)}/{len(rows)} rows carry provenance"))

    # 2 dedup (unique MedGen CUI)
    cuis = [r["medgen_cui"] for r in rows]
    dup = len(cuis) - len(set(cuis))
    checks.append(("dedup_unique_cui", dup == 0, f"{dup} duplicate CUIs"))

    # 3 scope logged: excluded rows must have a reason; in-scope rows must not
    bad_excl = [r for r in rows if r["in_scope"] == "false" and not r["exclusion_reason"].strip()]
    bad_in   = [r for r in rows if r["in_scope"] == "true" and r["exclusion_reason"].strip()]
    checks.append(("scope_logged", len(bad_excl) == 0 and len(bad_in) == 0,
                   f"{len(bad_excl)} excluded-without-reason, {len(bad_in)} in-scope-with-reason"))

    # 4 in/false partition is total and consistent
    vals = set(r["in_scope"] for r in rows)
    checks.append(("in_scope_binary", vals <= {"true", "false"}, f"values={sorted(vals)}"))

    # 5 every row has an entity name
    no_name = [r for r in rows if not r["entity"].strip()]
    checks.append(("entity_present", len(no_name) == 0, f"{len(no_name)} rows missing entity"))

    n_in  = sum(1 for r in rows if r["in_scope"] == "true")
    n_out = sum(1 for r in rows if r["in_scope"] == "false")

    passed = sum(1 for _, ok, _ in checks if ok)
    total  = len(checks)
    verdict = "PASS" if passed == total else "FAIL"

    report = {
        "phase": "R1",
        "kind": "investigation_gate",
        "generated": datetime.date.today().isoformat(),
        "inputs": {
            "raw_gene_condition_source_id": {"path": "data/raw/clinvar/gene_condition_source_id.tsv",
                                             "sha12": sha12(RAW)},
            "disease_index_base": {"path": "data/curated/disease_index_base.csv",
                                   "sha12": sha12(IDX)},
        },
        "counts": {"unique_diseases": len(rows), "in_scope": n_in, "excluded": n_out},
        "checks": [{"name": n, "pass": ok, "detail": d} for n, ok, d in checks],
        "verdict": f"{verdict} ({passed}/{total})",
        "note": ("Scope filter is NAME-BASED and PROVISIONAL. Known boundary classes deferred to R2 "
                 "case-by-case review: lysosomal/storage diseases with primary CNS (e.g. Tay-Sachs, "
                 "neuronopathic Gaucher), neurocutaneous syndromes (e.g. tuberous sclerosis), and "
                 "metabolic disorders with primary CNS. inheritance_class / mechanism_class are "
                 "PENDING_R2. Some rows have empty genes where the source association is at a "
                 "phenotypic-series level; R2 fills gene from NCBI Gene."),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(report, open(OUT, "w"), indent=2)
    print(json.dumps({"verdict": report["verdict"], "counts": report["counts"],
                      "checks": [(n, ok) for n, ok, _ in checks]}, indent=2))
    print("written:", OUT)


if __name__ == "__main__":
    main()
