#!/usr/bin/env python3
"""
R1 pipeline — build the disease enumeration scaffold from NCBI ClinVar's
gene_condition_source_id, aggregated by MedGen CUI, with the SCOPE.md
in/out classifier applied.

INVESTIGATION ONLY. Produces provenance-tagged data, no whitepaper prose.

Inputs  (data/raw/clinvar/gene_condition_source_id.tsv, pulled from
         https://ftp.ncbi.nlm.nih.gov/pub/clinvar/gene_condition_source_id)
Outputs (data/curated/disease_index_base.csv)

Deterministic: same input file -> same output (sorted, stable).
"""
import csv, os, re, sys, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
SRC  = os.path.join(ROOT, "data", "raw", "clinvar", "gene_condition_source_id.tsv")
OUT  = os.path.join(ROOT, "data", "curated", "disease_index_base.csv")

# Retrieval date of the source file (recorded for provenance).
RETRIEVED = "2026-06-17"

# ---- SCOPE.md classifier ---------------------------------------------------
# Match on the DISEASE NAME as a proxy for the PRIMARY/DEFINING system.
# A name centred on a brain/nerve/heart/mood term -> excluded (sibling whitepaper).
# Everything else -> candidate in-scope (systemic). R2 verifies multi-system cases.
# Conservative: excluded entities are FLAGGED with a reason, never dropped.

EXCLUDE = {
    "neuro": [
        r"\bataxia", r"\bataxic\b", r"neuropath", r"leukodystroph",
        r"leukoencephalopath", r"encephalopath", r"\bepilep", r"\bseizure",
        r"spastic parapleg", r"parkinson", r"\bdementia", r"alzheimer",
        r"neurodegener", r"motor neuron", r"demyelinat", r"spinocerebellar",
        r"myoclon", r"\bcerebral\b", r"\bcerebellar\b", r"\bbrain\b",
        r"charcot-marie-tooth", r"amyotroph", r"\bchorea", r"dystonia",
        r"\bneuronal\b", r"white matter", r"\bmyelin\b", r"polyneuropath",
        r"\baphasia", r"\bmigraine", r"narcoleps", r"restless legs",
        r"\bparesis\b", r"\bpalsy\b", r"intellectual disabilit",
        r"mental retardation",
        # named primary-neuro eponyms that lack a system keyword:
        r"huntington", r"\brett\b", r"angelman", r"canavan", r"\bkrabbe",
        r"alexander disease", r"pelizaeus", r"lesch-nyhan", r"\btourette",
        r"\bpitt-hopkins", r"\bdravet", r"\bohtahara", r"\bwest syndrome\b",
    ],
    "cardiac": [
        r"cardiomyopath", r"\blong qt", r"\bshort qt", r"\bbrugada",
        r"\barrhythmi", r"heart block", r"sick sinus", r"ventricular tachycard",
        r"atrial fibrillat", r"cardiac conduction", r"\bqt syndrome",
        r"sinoatrial", r"av block", r"sudden cardiac",
    ],
    "psych": [
        r"schizophren", r"\bautis", r"bipolar", r"major depress",
        r"\bpsychiatr", r"attention deficit", r"\badhd\b",
        r"obsessive-compuls", r"\banxiety\b",
    ],
}
EXCLUDE_RE = {k: [re.compile(p, re.I) for p in v] for k, v in EXCLUDE.items()}

# Positive (in-scope) organ-system tagging — best-effort hint for R2.
SYSTEM_HINTS = [
    ("metabolic",        [r"metabol", r"aciduria", r"acidemia", r"deficiency", r"storage disease",
                          r"glycogen", r"mucopolysacchar", r"galactosem", r"phenylketon", r"tyrosinem",
                          r"homocystin", r"urea cycle", r"hyperammonem", r"oxidation"]),
    ("lysosomal",        [r"lysosom", r"gaucher", r"fabry", r"pompe", r"niemann-pick", r"tay-sachs",
                          r"mucolipid", r"sphingolipid", r"gangliosid"]),
    ("connective_skeletal",[r"collagen", r"fibrillin", r"marfan", r"ehlers-danlos", r"osteogenesis",
                          r"chondrodyspl", r"dysplasia", r"skeletal", r"achondropl", r"\bbone\b",
                          r"osteopetros", r"cutis laxa"]),
    ("hematologic",      [r"anemi", r"haemoglobin", r"hemoglobin", r"thalassem", r"sickle",
                          r"hemophil", r"haemophil", r"coagulat", r"thrombocyto", r"neutropen",
                          r"\bplatelet", r"porphyr", r"hemochromatos", r"bleeding"]),
    ("immunologic",      [r"immunodefic", r"immune defic", r"autoinflammat", r"agammaglobulin",
                          r"granulomat", r"complement defic", r"periodic fever", r"sever combined immun"]),
    ("renal",            [r"\brenal", r"\bkidney", r"nephro", r"polycystic kidney", r"nephrotic",
                          r"cystinos", r"\bbartter", r"\bgitelman", r"alport"]),
    ("hepatic",          [r"hepat", r"\bliver", r"wilson", r"cholestas", r"biliary"]),
    ("gastrointestinal", [r"intestin", r"\bbowel", r"\bcolon", r"pancreati", r"enteropath", r"\bcolitis"]),
    ("pulmonary_exocrine",[r"pulmonar", r"\blung", r"cystic fibrosis", r"\bciliary", r"surfactant",
                          r"bronchiect"]),
    ("endocrine_growth", [r"\bthyroid", r"\bdiabetes", r"adrenal", r"\bpituitar", r"\bgrowth",
                          r"\bdwarfism", r"hypogonad", r"androgen", r"congenital adrenal"]),
    ("dermatologic",     [r"\bskin\b", r"keratoderm", r"ichthyos", r"epidermolys", r"albinism",
                          r"\bnail\b", r"\bhair\b", r"ectodermal dyspl", r"palmoplantar"]),
    ("eye",              [r"\bretin", r"\bmacular", r"\bcornea", r"\bcataract", r"\bglaucoma",
                          r"\boptic\b", r"\bocular", r"\bvision", r"\bblind"]),
    ("ear",              [r"\bdeaf", r"hearing loss", r"\botitis", r"\bcochlea"]),
    ("cancer_predisp",   [r"\bcancer", r"\btumor", r"\btumour", r"neoplas", r"\bcarcinoma",
                          r"\bsarcoma", r"polyposis", r"\bleukemi", r"\blymphoma",
                          r"predisposition to", r"\bblastoma"]),
]
SYSTEM_RE = [(name, [re.compile(p, re.I) for p in pats]) for name, pats in SYSTEM_HINTS]


def classify_scope(name):
    """Return (in_scope: bool, exclusion_reason: str, system_hint: str)."""
    for bucket, pats in EXCLUDE_RE.items():
        for rx in pats:
            if rx.search(name):
                return (False, f"primary {bucket} -> sibling (neuro/mind)", bucket)
    # in-scope: best-effort system hint
    hints = [name_ for name_, pats in SYSTEM_RE if any(rx.search(name) for rx in pats)]
    return (True, "", "|".join(hints) if hints else "unclassified_systemic")


def main():
    if not os.path.exists(SRC):
        sys.exit(f"missing source: {SRC}")

    # aggregate by MedGen ConceptID
    by_cui = {}
    n_rows = 0
    with open(SRC, encoding="utf-8") as fh:
        reader = csv.reader(fh, delimiter="\t")
        header = next(reader)
        for row in reader:
            if not row or row[0].startswith("#"):
                continue
            n_rows += 1
            gene   = row[1].strip()
            cui    = row[3].strip()
            name   = row[4].strip()
            mim    = row[7].strip()
            if not cui:
                continue
            rec = by_cui.setdefault(cui, {"name": name, "genes": set(), "mims": set()})
            if gene:
                rec["genes"].add(gene)
            if mim:
                rec["mims"].add(mim)
            # keep the longest/most descriptive name seen
            if len(name) > len(rec["name"]):
                rec["name"] = name

    rows_out = []
    for cui, rec in by_cui.items():
        in_scope, reason, system = classify_scope(rec["name"])
        rows_out.append({
            "entity": rec["name"],
            "medgen_cui": cui,
            "omim_mim": ";".join(sorted(rec["mims"])),
            "genes": ";".join(sorted(rec["genes"])),
            "n_genes": len(rec["genes"]),
            "inheritance_class": "PENDING_R2",
            "mechanism_class": "PENDING_R2",
            "organ_system_hint": system,
            "in_scope": "true" if in_scope else "false",
            "exclusion_reason": reason,
            "provenance": f"clinvar:gene_condition_source_id:{RETRIEVED}",
        })

    rows_out.sort(key=lambda r: (r["in_scope"] == "false", r["entity"].lower()))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    cols = ["entity", "medgen_cui", "omim_mim", "genes", "n_genes",
            "inheritance_class", "mechanism_class", "organ_system_hint",
            "in_scope", "exclusion_reason", "provenance"]
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows_out)

    # summary
    n_total = len(rows_out)
    n_in    = sum(1 for r in rows_out if r["in_scope"] == "true")
    n_out   = n_total - n_in
    digest  = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:12]
    print(f"source associations : {n_rows}")
    print(f"unique diseases (CUI): {n_total}")
    print(f"  in-scope (systemic): {n_in}")
    print(f"  excluded (neuro/cardiac/psych, flagged): {n_out}")
    print(f"output: {OUT}")
    print(f"output sha256[:12]: {digest}")


if __name__ == "__main__":
    main()
