#!/usr/bin/env python3
"""
R2 stage 4 — per-disease dossier builder.

For every disease in the curated cohort (methodology/dossier_cohort.csv) assemble
a structured dossier with each field provenance- and grade-tagged, per ROADMAP R2:

  gene_function        - NCBI Gene RefSeq Summary per gene          [L] / [O]
  variant_spectrum     - ClinVar germline-classification counts     [L] / [O]
  molecular_mechanism  - from disease_index.csv (R2 stage 3)         [L]/[H]/[O]
  inheritance          - from disease_index.csv (MedGen MOI)         [L] / [O]
  organ_systems        - HPO P-aspect terms rolled up to HP:0000118
                         organ-system categories                     [L] / [O]
  cardinal_symptoms    - top HPO P-aspect phenotypes (by frequency)  [L] / [O]
  age_of_onset         - HPO onset annotations                       [L] / [O]
  prevalence           - mined from the MedGen definition if stated  [L] / [O]
  clinical_definition  - MedGen narrative                            [L] / [O]

INVESTIGATION ONLY (no whitepaper prose). Deterministic: pure function of the
cached inputs (disease_index.csv, cohort MedGen cache, gene resources cache,
phenotype.hpoa, hp.obo, mechanism + OMIM-join curation artifacts). No network.

Grade vocabulary (constitution C-D): [L] source-stated & cited (observed);
[H] inference from established science (basis recorded); [O] open/unavailable,
obstacle named; never guessed.

Out: data/curated/dossiers/<slug>.json  (one per cohort disease)
     data/curated/dossiers/_cohort_index.json
"""
import csv, os, re, json, gzip, hashlib, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX = os.path.join(ROOT, "data", "curated", "disease_index.csv")
COHORT = os.path.join(ROOT, "methodology", "dossier_cohort.csv")
MEDGEN = os.path.join(ROOT, "data", "raw", "medgen", "dossier_cohort_esummary.json")
GENES = os.path.join(ROOT, "data", "raw", "clinvar", "cohort_gene_resources.json")
SUPPL = os.path.join(ROOT, "methodology", "omim_join_supplement.csv")
HPOA = os.path.join(ROOT, "data", "raw", "hpo", "phenotype.hpoa.gz")
HPOBO = os.path.join(ROOT, "data", "raw", "hpo", "hp.obo.gz")
OUTDIR = os.path.join(ROOT, "data", "curated", "dossiers")
RETRIEVED = "2026-06-17"
HPOA_VERSION = "2026-06-06"
PHENO_ROOT = "HP:0000118"
ONSET_ROOT = "HP:0003674"

# ---------- HPO ontology ----------
def load_obo():
    txt = gzip.open(HPOBO, "rt", encoding="utf-8").read()
    name, parents = {}, {}
    for block in txt.split("\n[Term]\n"):
        mid = re.search(r"^id: (HP:\d+)", block, re.M)
        if not mid:
            continue
        tid = mid.group(1)
        mn = re.search(r"^name: (.+)$", block, re.M)
        name[tid] = mn.group(1).strip() if mn else tid
        parents[tid] = re.findall(r"^is_a: (HP:\d+)", block, re.M)
    return name, parents

def ancestors(tid, parents, cache):
    if tid in cache:
        return cache[tid]
    seen, stack = set(), list(parents.get(tid, []))
    while stack:
        p = stack.pop()
        if p in seen:
            continue
        seen.add(p)
        stack.extend(parents.get(p, []))
    cache[tid] = seen
    return seen

# ---------- HPO disease annotations ----------
def load_hpoa():
    """OMIM-id -> list of annotation dicts."""
    ann = collections.defaultdict(list)
    with gzip.open(HPOA, "rt", encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#") or line.startswith("database_id"):
                continue
            f = line.rstrip("\n").split("\t")
            if len(f) < 12 or not f[0].startswith("OMIM:"):
                continue
            ann[f[0].split(":")[1]].append({
                "hpo_id": f[3], "reference": f[4], "evidence": f[5],
                "onset": f[6], "frequency": f[7], "aspect": f[10],
            })
    return ann

FREQ_ORDER = {  # HPO frequency terms -> rank weight (higher = more frequent)
    "HP:0040280": 6, "HP:0040281": 5, "HP:0040282": 4,
    "HP:0040283": 3, "HP:0040284": 2, "HP:0040285": 1,
}
def freq_weight(fr):
    if not fr:
        return 0.0
    if fr in FREQ_ORDER:
        return float(FREQ_ORDER[fr]) / 6.0 + 1.0  # 1..2 band for ordinal terms
    m = re.match(r"(\d+)\s*/\s*(\d+)", fr)
    if m and int(m.group(2)):
        return int(m.group(1)) / int(m.group(2))
    m = re.match(r"(\d+(?:\.\d+)?)%", fr)
    if m:
        return float(m.group(1)) / 100.0
    return 0.0

# ---------- prevalence mining from MedGen definition ----------
PREV_PAT = re.compile(
    r"([^.]*?\b(?:prevalence|incidence|affects?|occurs?\s+in|estimated\s+(?:to\s+)?(?:affect|occur)|"
    r"1\s+in\s+[\d,]+|[\d.]+\s*(?:per|in)\s*[\d,]+|[\d.]+%|[\d,]+\s+(?:births|individuals|people|live births))\b[^.]*\.)",
    re.I)
def mine_prevalence(text):
    if not text:
        return None
    for sent in PREV_PAT.findall(text):
        s = sent.strip()
        # require an actual number to avoid vague matches
        if re.search(r"\d", s) and re.search(r"(prevalence|incidence|1\s+in\s+\d|per\s+[\d,]+|%|births|affect)", s, re.I):
            return re.sub(r"\s+", " ", s)[:400]
    return None

def slug(name):
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return re.sub(r"_+", "_", s)[:80]

def graded(value, grade, source=None, obstacle=None):
    o = {"value": value, "grade": grade}
    if source:
        o["source"] = source
    if obstacle:
        o["obstacle"] = obstacle
    return o

def main():
    idx = {r["medgen_cui"]: r for r in csv.DictReader(open(IDX, encoding="utf-8"))}
    cohort = list(csv.DictReader(open(COHORT, encoding="utf-8")))
    medgen = json.load(open(MEDGEN, encoding="utf-8"))
    generes = json.load(open(GENES, encoding="utf-8"))

    name, parents = load_obo()
    hpoa = load_hpoa()
    anc_cache = {}

    # organ-system categories = direct children of HP:0000118
    organ_cat = {t for t, ps in parents.items() if PHENO_ROOT in ps}

    # OMIM-join supplement (validate each row against the HPO file)
    suppl = collections.defaultdict(list)
    suppl_audit = []
    for row in csv.DictReader(open(SUPPL, encoding="utf-8")):
        omim = row["omim"].strip()
        ok = omim in hpoa
        suppl_audit.append({**row, "validated_present_in_hpoa": ok})
        if ok:
            suppl[row["cui"]].append(omim)

    os.makedirs(OUTDIR, exist_ok=True)
    cohort_index = []

    for m in cohort:
        cui = m["cui"]
        r = idx[cui]
        entity = r["entity"]
        genes = [g.strip() for g in r["genes"].split(";") if g.strip()]
        mc = medgen.get(cui, {})

        # OMIM set = MedGen conceptmeta cross-refs + validated supplement
        omims = sorted(set(mc.get("omim_codes", [])) | set(suppl.get(cui, [])))
        omim_source = "MedGen conceptmeta (SAB=OMIM)"
        if suppl.get(cui):
            omim_source += " + omim_join_supplement.csv (HPO-name-verified)"

        # ----- gene_function -----
        gf = []
        for g in genes:
            gr = generes.get(g, {})
            if gr.get("summary"):
                gf.append(graded(
                    {"gene": g, "geneid": gr.get("geneid", ""),
                     "full_name": gr.get("description", ""), "summary": gr["summary"]},
                    "[L]", source=f"NCBI Gene:{gr.get('geneid','')} RefSeq Summary; retrieved {RETRIEVED}"))
            else:
                gf.append(graded({"gene": g, "geneid": gr.get("geneid", "")},
                                 "[O]", obstacle=f"no RefSeq Summary available for {g} in NCBI Gene"))
        if not genes:
            gf.append(graded({"gene": None}, "[O]",
                             obstacle="causative gene not annotated at this MedGen aggregate concept; "
                                      "see gene-resolved subtype dossier(s)"))

        # ----- variant_spectrum (ClinVar) -----
        vs = []
        for g in genes:
            gr = generes.get(g, {})
            cv = gr.get("clinvar")
            if cv and cv.get("total_records", 0) > 0:
                vs.append(graded(
                    {"gene": g, "total_records": cv["total_records"],
                     "germline_classification_counts": cv["germline_classification_counts"]},
                    "[L]", source=(f"ClinVar gene query '{g}[gene]' with [Germline classification] "
                                   f"filters; retrieved {RETRIEVED}; categories overlap, not summed")))
            else:
                vs.append(graded({"gene": g}, "[O]",
                                 obstacle=f"no ClinVar germline records retrieved for {g}"))
        if not genes:
            vs.append(graded({"gene": None}, "[O]",
                             obstacle="causative gene not annotated at this MedGen aggregate concept; "
                                      "no ClinVar gene query possible; see gene-resolved subtype dossier(s)"))

        # ----- molecular_mechanism (from index) -----
        # For [O] the index source column already holds the named obstacle; route it
        # to obstacle so the dossier field is self-describing per the grade vocabulary.
        if r["mechanism_grade"] == "[O]":
            mech = graded(r["mechanism_class"], "[O]", obstacle=r["mechanism_source"])
        else:
            mech = graded(r["mechanism_class"], r["mechanism_grade"], source=r["mechanism_source"])

        # ----- inheritance (from index) -----
        if r["inheritance_grade"] == "[O]":
            inh = graded(r["inheritance_class"], "[O]",
                         obstacle=("MedGen esummary returned no ModeOfInheritance for this "
                                   f"concept; provenance {r['inheritance_source']}"))
        else:
            inh = graded(r["inheritance_class"], r["inheritance_grade"],
                         source=r["inheritance_source"])

        # ----- HPO-derived clinical fields -----
        anns = [a for o in omims for a in hpoa.get(o, [])]
        p_anns = [a for a in anns if a["aspect"] == "P"]

        # organ systems
        sys_support = collections.Counter()
        for a in p_anns:
            tid = a["hpo_id"]
            anc = ancestors(tid, parents, anc_cache) | {tid}
            for cat in (anc & organ_cat):
                sys_support[cat] += 1
        if sys_support:
            systems = [{"system": name.get(c, c), "hpo_id": c, "supporting_term_count": n}
                       for c, n in sorted(sys_support.items(), key=lambda kv: (-kv[1], kv[0]))]
            organ_systems = graded(systems, "[L]",
                source=f"HPO phenotype.hpoa v{HPOA_VERSION} (OMIM {','.join(omims)}); "
                       f"P-aspect terms rolled up to HP:0000118 organ-system categories via hp.obo")
        else:
            organ_systems = graded([], "[O]",
                obstacle=("no HPO phenotypic-abnormality annotations joinable for this concept "
                          f"(OMIM cross-ref: {','.join(omims) or 'none'})"))

        # cardinal symptoms: rank P-aspect terms by max frequency weight, dedup by hpo_id
        best = {}
        for a in p_anns:
            w = freq_weight(a["frequency"])
            cur = best.get(a["hpo_id"])
            if cur is None or w > cur["_w"]:
                best[a["hpo_id"]] = {"hpo_id": a["hpo_id"], "name": name.get(a["hpo_id"], a["hpo_id"]),
                                     "frequency": a["frequency"] or None, "reference": a["reference"],
                                     "_w": w}
        ranked = sorted(best.values(), key=lambda d: (-d["_w"], d["name"]))[:15]
        for d in ranked:
            d.pop("_w", None)
        if ranked:
            cardinal = graded(ranked, "[L]",
                source=f"HPO phenotype.hpoa v{HPOA_VERSION} (OMIM {','.join(omims)}); "
                       f"top P-aspect phenotypes by annotated frequency; reference = HPO source citation")
        else:
            cardinal = graded([], "[O]",
                obstacle=f"no HPO phenotype annotations joinable (OMIM cross-ref: {','.join(omims) or 'none'})")

        # age of onset: onset column values + C-aspect onset terms
        onset_ids = collections.Counter()
        onset_ref = {}
        onset_subtree = lambda t: ONSET_ROOT in (ancestors(t, parents, anc_cache) | {t})
        for a in anns:
            if a["onset"] and a["onset"].startswith("HP:"):
                onset_ids[a["onset"]] += 1
                onset_ref.setdefault(a["onset"], a["reference"])
            if a["aspect"] == "C" and a["hpo_id"].startswith("HP:") and onset_subtree(a["hpo_id"]):
                onset_ids[a["hpo_id"]] += 1
                onset_ref.setdefault(a["hpo_id"], a["reference"])
        if onset_ids:
            onsets = [{"hpo_id": t, "name": name.get(t, t), "annotation_count": n,
                       "reference": onset_ref.get(t, "")}
                      for t, n in sorted(onset_ids.items(), key=lambda kv: (-kv[1], kv[0]))]
            age_of_onset = graded(onsets, "[L]",
                source=f"HPO phenotype.hpoa v{HPOA_VERSION} (OMIM {','.join(omims)}); onset annotations")
        else:
            age_of_onset = graded([], "[O]",
                obstacle=f"no HPO onset annotation joinable (OMIM cross-ref: {','.join(omims) or 'none'})")

        # prevalence: mine MedGen definition
        defn = mc.get("definition", "") or r.get("clinical_definition", "")
        prev = mine_prevalence(defn)
        if prev:
            prevalence = graded(prev, "[L]",
                source=f"MedGen concept {cui} definition (NCBI MedGen); retrieved {RETRIEVED}")
        else:
            prevalence = graded(None, "[O]",
                obstacle=("prevalence/incidence not stated in the MedGen definition; epidemiological "
                          "magnitude requires a dedicated source (e.g. Orphanet/GBD), deferred — not guessed"))

        # clinical definition
        if defn:
            clinical_definition = graded(re.sub(r"\s+", " ", defn).strip(), "[L]",
                source=f"MedGen concept {cui} (NCBI MedGen); retrieved {RETRIEVED}")
        else:
            clinical_definition = graded(None, "[O]", obstacle="no MedGen narrative definition available")

        dossier = {
            "schema": "disease_wp.dossier/v1",
            "phase": "R2",
            "investigation_only": True,
            "identity": {
                "entity": entity,
                "medgen_cui": cui,
                "medgen_uid": r["medgen_uid"],
                "omim_codes": omims,
                "omim_code_source": omim_source,
                "genes": genes,
                "semantic_type": r.get("semantic_type", "") or mc.get("semantictype", ""),
                "tier": m["tier"],
                "system_class": m["system_class"],
                "in_scope": r["in_scope"] == "true",
                "cns_cross_reference": r.get("cns_cross_reference", ""),
            },
            "inheritance": inh,
            "molecular_mechanism": mech,
            "gene_function": gf,
            "variant_spectrum": vs,
            "clinical": {
                "organ_systems": organ_systems,
                "cardinal_symptoms": cardinal,
                "age_of_onset": age_of_onset,
                "prevalence": prevalence,
                "clinical_definition": clinical_definition,
            },
            "provenance": {
                "disease_index": "data/curated/disease_index.csv",
                "medgen_cohort_cache": "data/raw/medgen/dossier_cohort_esummary.json",
                "gene_resources_cache": "data/raw/clinvar/cohort_gene_resources.json",
                "hpo_annotations": f"data/raw/hpo/phenotype.hpoa.gz (v{HPOA_VERSION})",
                "hpo_ontology": "data/raw/hpo/hp.obo.gz",
                "mechanism_rules": "methodology/mechanism_rules.csv",
                "omim_join_supplement": "methodology/omim_join_supplement.csv",
                "retrieved": RETRIEVED,
            },
            "grade_vocabulary": {
                "[L]": "source-stated and cited (observed input)",
                "[H]": "inference from established science; basis recorded",
                "[O]": "open/unavailable; obstacle named; not guessed",
            },
        }

        sl = slug(entity)
        path = os.path.join(OUTDIR, sl + ".json")
        json.dump(dossier, open(path, "w"), indent=2, ensure_ascii=False)

        # cohort-index row + grade tally
        field_grades = {
            "inheritance": inh["grade"], "mechanism": mech["grade"],
            "gene_function": "/".join(sorted({x["grade"] for x in gf})),
            "variant_spectrum": "/".join(sorted({x["grade"] for x in vs})),
            "organ_systems": organ_systems["grade"], "cardinal_symptoms": cardinal["grade"],
            "age_of_onset": age_of_onset["grade"], "prevalence": prevalence["grade"],
        }
        cohort_index.append({
            "entity": entity, "cui": cui, "tier": m["tier"], "slug": sl,
            "file": f"data/curated/dossiers/{sl}.json",
            "n_omim": len(omims), "n_genes": len(genes),
            "n_cardinal_symptoms": len(cardinal["value"]),
            "n_organ_systems": len(organ_systems["value"]),
            "field_grades": field_grades,
        })

    cohort_index.sort(key=lambda d: (d["tier"] != "flagship", d["entity"]))
    json.dump({
        "schema": "disease_wp.dossier_cohort_index/v1",
        "generated": RETRIEVED, "cohort_size": len(cohort_index),
        "omim_join_supplement_audit": suppl_audit,
        "dossiers": cohort_index,
    }, open(os.path.join(OUTDIR, "_cohort_index.json"), "w"), indent=2, ensure_ascii=False)

    # ---- report ----
    print("--- R2 dossiers built ---")
    print(f"  cohort: {len(cohort_index)}  ->  {OUTDIR}")
    gtally = collections.Counter()
    for d in cohort_index:
        for fg in d["field_grades"].values():
            for g in fg.split("/"):
                gtally[g] += 1
    print("  field-grade tally (all fields x diseases):", dict(gtally))
    print("  per-disease clinical coverage:")
    for d in cohort_index:
        fg = d["field_grades"]
        print(f"    [{d['tier'][:4]}] {d['entity'][:40]:40s} "
              f"sym={d['n_cardinal_symptoms']:2d} org={d['n_organ_systems']:2d} "
              f"inh={fg['inheritance']} mech={fg['mechanism']} prev={fg['prevalence']}")

    # determinism digest over all dossier files
    h = hashlib.sha256()
    for fn in sorted(os.listdir(OUTDIR)):
        h.update(open(os.path.join(OUTDIR, fn), "rb").read())
    print(f"  dossier-set sha256[:12]: {h.hexdigest()[:12]}")

if __name__ == "__main__":
    main()
