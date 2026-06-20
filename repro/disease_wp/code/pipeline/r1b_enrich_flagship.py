#!/usr/bin/env python3
"""
R1->R2 bridge enrichment (DEMONSTRATION of the R2 path).
For a curated set of flagship in-scope systemic diseases, pull mode-of-inheritance
+ clinical definition + semantic type from NCBI MedGen esummary, grounded in the
base index (CUI taken from disease_index_base.csv). Caches raw responses.
Writes data/curated/disease_index_seed.csv. INVESTIGATION ONLY.

Inheritance is a clean NCBI pull (graded [L], cited MedGen). mechanism_class stays
PENDING_R2 here -- it needs per-disease OMIM/literature curation and is not guessed.
"""
import csv, os, re, json, time, urllib.request, urllib.parse, hashlib, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX  = os.path.join(ROOT, "data", "curated", "disease_index_base.csv")
CACHE= os.path.join(ROOT, "data", "raw", "medgen")
OUT  = os.path.join(ROOT, "data", "curated", "disease_index_seed.csv")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RETRIEVED = "2026-06-17"

# Flagship in-scope diseases across taxonomy categories (curated demo set).
FLAGSHIP = [
    "Cystic fibrosis", "Sickle cell", "beta-thalassemia", "Marfan syndrome",
    "Osteogenesis imperfecta", "Phenylketonuria", "Gaucher disease", "Fabry disease",
    "Wilson disease", "Hemochromatosis", "Hereditary factor VIII",  # hemophilia A
    "Duchenne muscular dystrophy", "Glucose-6-phosphate dehydrogenase deficiency",
    "alpha-1-antitrypsin", "Cystinosis", "Maple syrup urine disease",
    "Niemann-Pick", "Polycystic kidney", "glycogen storage disease, type II",  # Pompe
    "Tyrosinemia",
]


def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def best_index_match(rows, q):
    cands = [r for r in rows if q.lower() in r["entity"].lower()]
    if not cands:
        return None
    # prefer in-scope, then shortest (most canonical) name
    cands.sort(key=lambda r: (r["in_scope"] != "true", len(r["entity"])))
    return cands[0]


def medgen_uid(cui):
    url = f"{EUTILS}/esearch.fcgi?db=medgen&term={cui}&retmode=json"
    js = json.loads(get(url))
    ids = js["esearchresult"]["idlist"]
    return ids[0] if ids else None


def medgen_summary(uid):
    cache = os.path.join(CACHE, f"summary_{uid}.json")
    if os.path.exists(cache):
        return json.load(open(cache))
    js = json.loads(get(f"{EUTILS}/esummary.fcgi?db=medgen&id={uid}&retmode=json"))
    json.dump(js, open(cache, "w"))
    return js


def parse_moi(conceptmeta):
    names = re.findall(r"<ModeOfInheritance[^>]*>.*?<Name>(.*?)</Name>", conceptmeta, re.S)
    return sorted(set(n.strip() for n in names))


def short_def(conceptmeta_or_def):
    return ""


def main():
    rows = list(csv.DictReader(open(IDX, encoding="utf-8")))
    os.makedirs(CACHE, exist_ok=True)
    out = []
    for q in FLAGSHIP:
        m = best_index_match(rows, q)
        if not m:
            print(f"  [MISS] no index match: {q}")
            continue
        cui = m["medgen_cui"]
        try:
            uid = medgen_uid(cui); time.sleep(0.4)
            if not uid:
                print(f"  [no UID] {m['entity'][:40]} ({cui})"); continue
            js = medgen_summary(uid); time.sleep(0.34)
            r = js["result"][uid]
            cm = r.get("conceptmeta", "")
            moi = parse_moi(cm)
            defn = r.get("definition", {})
            defn = defn.get("value", "") if isinstance(defn, dict) else str(defn)
            sty = r.get("semantictype", "")
            out.append({
                "entity": r.get("title", m["entity"]),
                "medgen_cui": cui,
                "medgen_uid": uid,
                "omim_mim": m["omim_mim"],
                "genes": m["genes"],
                "inheritance_class": "; ".join(moi) if moi else "not_stated",
                "inheritance_source": f"medgen:esummary:ModeOfInheritance:{RETRIEVED}",
                "inheritance_grade": "[L]" if moi else "[O]",
                "mechanism_class": "PENDING_R2",
                "semantic_type": sty,
                "organ_system_hint": m["organ_system_hint"],
                "in_scope": m["in_scope"],
                "clinical_definition": defn.replace("\n", " ").strip(),
            })
            print(f"  [OK] {r.get('title', m['entity'])[:42]:42s} -> {('; '.join(moi))[:40] or 'not_stated'}")
        except Exception as e:
            print(f"  [ERR] {m['entity'][:40]}: {e}")

    cols = ["entity", "medgen_cui", "medgen_uid", "omim_mim", "genes",
            "inheritance_class", "inheritance_source", "inheritance_grade",
            "mechanism_class", "semantic_type", "organ_system_hint", "in_scope",
            "clinical_definition"]
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader(); w.writerows(out)
    print(f"\nenriched {len(out)} flagship diseases -> {OUT}")


if __name__ == "__main__":
    main()
