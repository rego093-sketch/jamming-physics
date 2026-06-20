#!/usr/bin/env python3
"""
R2 stage 3 — mechanism_class enrichment (honest, cited, no guessing).

Fills mechanism_class / mechanism_grade / mechanism_source for every in-scope
entity in disease_index.csv, using only verifiable, deterministic sources, in
priority order:

  1. CURATED CITED RULES (methodology/mechanism_rules.csv) — established
     molecular mechanisms for specific genes/classes (collagen dominant-negative,
     CFTR loss-of-function, HBB sickle gain-of-function, etc.). Grade [L];
     citation = the rule basis + the row's OMIM MIM.
  2. ClinGen DOSAGE SENSITIVITY (data/raw/clingen/...): Haploinsufficiency
     Score 3 -> haploinsufficiency; Triplosensitivity Score 3 -> dosage
     (triplosensitivity). Grade [L]; citation = ClinGen + the curated PMIDs.
  3. RECESSIVE => LOSS-OF-FUNCTION inference: when MedGen inheritance is purely
     recessive (autosomal- and/or X-linked-recessive, no dominant/GoF term),
     the protein-level mechanism is loss-of-function. This is a sound inference
     from established genetics, NOT a verbatim source claim, so it is graded
     [H] (inference) and the basis is recorded; ClinGen HI=30 (gene annotated
     to an AR phenotype) is added as corroboration when present.
  4. Otherwise -> "[O] not_curated" with the obstacle named (VP-SPEC C3):
     dominant or unspecified-inheritance entities whose mechanism (GoF vs
     dominant-negative vs haploinsufficiency) needs per-gene OMIM/PubMed
     curation are NOT guessed.

INVESTIGATION ONLY. Deterministic: pure function of (disease_index.csv,
ClinGen file, mechanism_rules.csv). No network.

In/Out: data/curated/disease_index.csv  (mechanism_* columns rewritten)
        reports/r2_mechanism_summary.json
"""
import csv, os, re, json, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX  = os.path.join(ROOT, "data", "curated", "disease_index.csv")
RULES = os.path.join(ROOT, "methodology", "mechanism_rules.csv")
CLINGEN = os.path.join(ROOT, "data", "raw", "clingen", "ClinGen_gene_curation_list_GRCh38.tsv")
OUTJSON = os.path.join(ROOT, "reports", "r2_mechanism_summary.json")
RETRIEVED = "2026-06-17"

def load_clingen():
    g = {}
    if not os.path.exists(CLINGEN):
        return g
    for line in open(CLINGEN, encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        f = line.rstrip("\n").split("\t")
        if len(f) < 13:
            continue
        sym = f[0].strip()
        hip = [p.strip() for p in f[6:12] if p.strip()]
        tsp = [p.strip() for p in f[14:20] if p.strip()] if len(f) >= 20 else []
        g[sym] = {"hi": f[4].strip(), "ts": f[12].strip(), "hipmids": hip, "tspmids": tsp}
    return g

def load_rules():
    rules = []
    for r in csv.DictReader(open(RULES, encoding="utf-8")):
        genes = [x.strip() for x in r["gene"].split(";") if x.strip()]
        namepat = re.compile(r["name_pattern"], re.I) if r["name_pattern"].strip() else None
        rules.append({**r, "_genes": set(genes), "_namepat": namepat})
    return rules

PURE_RECESSIVE = re.compile(r"recessive", re.I)
HAS_DOMINANT = re.compile(r"dominant", re.I)

def main():
    rows = list(csv.DictReader(open(IDX, encoding="utf-8")))
    clingen = load_clingen()
    rules = load_rules()

    counts = collections.Counter()
    grade_counts = collections.Counter()

    for r in rows:
        if r["in_scope"] != "true":
            r["mechanism_class"] = r.get("mechanism_class", "")
            r["mechanism_grade"] = r.get("mechanism_grade", "")
            r["mechanism_source"] = r.get("mechanism_source", "")
            continue

        name = r["entity"]
        genes = set(g.strip() for g in r["genes"].split(";") if g.strip())
        inh = r["inheritance_class"]
        mim = r["omim_mim"]

        mech = grade = src = None

        # --- (1) curated cited rules ---
        for rule in rules:
            ok = False
            if rule["match_type"] == "gene_exact":
                ok = bool(genes & rule["_genes"])
                if ok and rule["_namepat"] is not None:
                    ok = bool(rule["_namepat"].search(name))
            elif rule["match_type"] == "name_regex":
                ok = bool(rule["_namepat"] and rule["_namepat"].search(name))
            if ok:
                mech = rule["mechanism_class"]
                grade = rule["grade"]
                cite = rule["citation_basis"]
                src = f"curated_rule:{rule['rule_id']}; {cite}" + (f"; OMIM:{mim}" if mim else "")
                break

        # --- (2) ClinGen dosage ---
        if mech is None:
            hi3 = [g for g in genes if clingen.get(g, {}).get("hi") == "3"]
            ts3 = [g for g in genes if clingen.get(g, {}).get("ts") == "3"]
            if hi3:
                pmids = sorted({p for g in hi3 for p in clingen[g]["hipmids"]})
                mech = "haploinsufficiency"
                grade = "[L]"
                src = (f"clingen:HI_score_3:{RETRIEVED}; genes={','.join(sorted(hi3))}"
                       + (f"; PMID:{','.join(pmids[:6])}" if pmids else ""))
            elif ts3:
                pmids = sorted({p for g in ts3 for p in clingen[g]["tspmids"]})
                mech = "dosage (triplosensitivity)"
                grade = "[L]"
                src = (f"clingen:TS_score_3:{RETRIEVED}; genes={','.join(sorted(ts3))}"
                       + (f"; PMID:{','.join(pmids[:6])}" if pmids else ""))

        # --- (3) recessive => loss-of-function (inference, [H]) ---
        if mech is None:
            if PURE_RECESSIVE.search(inh) and not HAS_DOMINANT.search(inh):
                ar_genes = [g for g in genes if clingen.get(g, {}).get("hi") == "30"]
                mech = "loss-of-function (biallelic; recessive)"
                grade = "[H]"
                src = "inference:recessive=>loss_of_function; basis=medgen_inheritance(recessive)"
                if ar_genes:
                    src += f"; corrob=clingen_AR(HI30):{','.join(sorted(ar_genes))}"

        # --- (4) not curated -> [O] with obstacle ---
        if mech is None:
            mech = "[O] not_curated"
            grade = "[O]"
            inh_note = inh if inh and inh != "not_stated" else "inheritance not stated"
            src = (f"obstacle: molecular mechanism not yet curated from primary literature "
                   f"(non-recessive/unspecified: {inh_note}); candidate modes "
                   f"(haploinsufficiency / gain-of-function / dominant-negative) require per-gene "
                   f"OMIM allelic-variant + PubMed review; not guessed (constitution C-D3, VP-SPEC C3)")

        r["mechanism_class"] = mech
        r["mechanism_grade"] = grade
        r["mechanism_source"] = src
        counts[mech.split(" (")[0].replace("[O] ", "[O]:")] += 1
        grade_counts[grade] += 1

    cols = list(rows[0].keys())
    with open(IDX, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)

    n_in = sum(1 for r in rows if r["in_scope"] == "true")
    digest = hashlib.sha256(open(IDX, "rb").read()).hexdigest()[:12]
    summary = {
        "phase": "R2", "stage": "mechanism_class", "generated": RETRIEVED,
        "in_scope_rows": n_in,
        "mechanism_grade_distribution": dict(grade_counts),
        "mechanism_class_distribution": dict(counts.most_common()),
        "sources": {
            "curated_rules": "methodology/mechanism_rules.csv",
            "clingen": "data/raw/clingen/ClinGen_gene_curation_list_GRCh38.tsv (2026-06-17)",
            "inheritance": "data/curated/disease_index.csv (medgen esummary)",
        },
        "index_sha12": digest,
        "discipline_note": ("[L]=mechanism stated by a cited rule or ClinGen dosage curation; "
                            "[H]=loss-of-function inferred from purely-recessive inheritance "
                            "(established genetics, marked as inference); "
                            "[O]=not curated, obstacle named, NOT guessed."),
    }
    os.makedirs(os.path.dirname(OUTJSON), exist_ok=True)
    json.dump(summary, open(OUTJSON, "w"), indent=2)

    print("--- R2 mechanism_class enrichment ---")
    print(f"  in-scope rows: {n_in}")
    print("  grade distribution:", dict(grade_counts))
    print("  top mechanism classes:")
    for k, v in counts.most_common(12):
        print(f"    {v:5d}  {k}")
    print(f"  index sha256[:12]: {digest}")
    print(f"  summary: {OUTJSON}")

if __name__ == "__main__":
    main()
