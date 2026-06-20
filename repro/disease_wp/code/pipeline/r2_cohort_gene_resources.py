#!/usr/bin/env python3
"""
R2 dossier support — gene-level resources for the dossier cohort genes.

For each gene referenced by the cohort:
  (1) NCBI Gene: symbol -> GeneID, official full name, RefSeq Summary
      (the gene-function narrative).  [observed; cite NCBI Gene:GeneID]
  (2) ClinVar germline-classification distribution: counts of variant records
      classified Pathogenic / Likely pathogenic / Uncertain significance /
      Likely benign / Benign, plus the total record count.
      [observed; cite ClinVar gene query + retrieval date]

Counts are esearch result totals using the [Germline classification] filter;
categories overlap (a record can carry conflicting classifications) so they are
reported as-is, NOT forced to sum to the total.

Cached + resumable (per-gene). Network only for genes not already cached.
Deterministic given the cache.

Out: data/raw/clinvar/cohort_gene_resources.json
"""
import csv, os, json, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
IDX = os.path.join(ROOT, "data", "curated", "disease_index.csv")
COHORT = os.path.join(ROOT, "methodology", "dossier_cohort.csv")
OUT = os.path.join(ROOT, "data", "raw", "clinvar", "cohort_gene_resources.json")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
MIN_INTERVAL = 0.5
RETRIEVED = "2026-06-17"

SIGS = [
    ("pathogenic", "Pathogenic"),
    ("likely pathogenic", "Likely pathogenic"),
    ("uncertain significance", "Uncertain significance"),
    ("likely benign", "Likely benign"),
    ("benign", "Benign"),
]

_last = [0.0]
def _throttle():
    dt = time.time() - _last[0]
    if dt < MIN_INTERVAL:
        time.sleep(MIN_INTERVAL - dt)
    _last[0] = time.time()

def get(url):
    for attempt in range(5):
        _throttle()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "disease_wp/0.3 (research)"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8")
        except Exception:
            if attempt == 4:
                raise
            time.sleep(1.5 * (attempt + 1))

def esearch_count(db, term):
    url = f"{BASE}/esearch.fcgi?db={db}&term={urllib.parse.quote(term)}&retmode=json"
    d = json.loads(get(url))
    return int(d["esearchresult"].get("count", "0"))

def gene_info(sym):
    # symbol -> GeneID (human)
    term = f"{sym}[sym] AND Homo sapiens[orgn]"
    url = f"{BASE}/esearch.fcgi?db=gene&term={urllib.parse.quote(term)}&retmode=json"
    ids = json.loads(get(url))["esearchresult"].get("idlist", [])
    if not ids:
        return {"geneid": "", "description": "", "summary": "", "obstacle": "no human Gene record for symbol"}
    # A symbol query [sym] also matches historical aliases of OTHER genes
    # (e.g. FAH is an alias of FANCA), so esearch can return several candidates
    # and the first need not be the gene whose OFFICIAL symbol is `sym`.
    # Resolve by the esummary official symbol (`name`), exact case-insensitive
    # match; never blindly take ids[0]. If no candidate's official symbol equals
    # the query, record an obstacle rather than guess.
    chosen = None
    for gid in ids:
        url = f"{BASE}/esummary.fcgi?db=gene&id={gid}&retmode=json"
        g = json.loads(get(url))["result"].get(gid, {})
        if g.get("name", "").upper() == sym.upper():
            chosen = (gid, g)
            break
    if chosen is None:
        return {"geneid": "", "description": "", "summary": "",
                "obstacle": f"no Gene record whose official symbol equals {sym} "
                            f"(candidates by [sym]: {','.join(ids)} matched on alias only)"}
    gid, g = chosen
    return {"geneid": gid, "description": g.get("description", ""),
            "summary": g.get("summary", ""), "aliases": g.get("otheraliases", "")}

def clinvar_dist(sym):
    total = esearch_count("clinvar", f"{sym}[gene]")
    dist = {}
    for q, label in SIGS:
        dist[label] = esearch_count("clinvar", f'{sym}[gene] AND "{q}"[Germline classification]')
    return {"total_records": total, "germline_classification_counts": dist}

def main():
    idx = {r["medgen_cui"]: r for r in csv.DictReader(open(IDX, encoding="utf-8"))}
    cohort = list(csv.DictReader(open(COHORT, encoding="utf-8")))
    genes = sorted({x.strip() for m in cohort for x in idx[m["cui"]]["genes"].split(";") if x.strip()})

    cache = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}

    for sym in genes:
        if sym in cache:
            continue
        gi = gene_info(sym)
        cv = clinvar_dist(sym)
        cache[sym] = {"symbol": sym, **gi, "clinvar": cv, "retrieved": RETRIEVED}
        json.dump(cache, open(OUT, "w"), indent=1, ensure_ascii=False)  # checkpoint each gene
        c = cache[sym]["clinvar"]["germline_classification_counts"]
        print(f"  {sym:10s} GeneID={cache[sym]['geneid'] or '-':8s} "
              f"summary={'Y' if cache[sym]['summary'] else 'n'}  "
              f"ClinVar P={c['Pathogenic']} LP={c['Likely pathogenic']} "
              f"VUS={c['Uncertain significance']} tot={cache[sym]['clinvar']['total_records']}")

    print(f"--- cohort gene resources: {len(cache)}/{len(genes)} genes cached ---")

if __name__ == "__main__":
    main()
