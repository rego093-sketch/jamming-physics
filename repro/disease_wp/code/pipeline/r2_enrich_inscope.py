#!/usr/bin/env python3
"""
R2 stage 1 — BULK enrichment over the full in-scope set.

Extends r1b_enrich_flagship.py (which proved the path on 18 diseases) to every
in-scope MedGen CUI in disease_index_base.csv. For each CUI it pulls
mode-of-inheritance + clinical definition + semantic type from NCBI MedGen
esummary, grounded in the base index.

INVESTIGATION ONLY — provenance-tagged data, no whitepaper prose.

Efficiency: CUIs are batched. esearch is issued as an OR query per chunk
(CUI -> MedGen UID, 1:1); esummary is issued in batches and each result is
mapped back to its CUI via the returned `conceptid`. Every response is cached
to data/raw/medgen/inscope_esummary.jsonl.gz, so re-runs do not re-hit NCBI.
NCBI politeness: <= 3 requests/second.

Grading (disease-project convention):
  inheritance_grade = [L]  MedGen states a ModeOfInheritance  (observed, cited)
                    = [O]  MedGen has no ModeOfInheritance     (obstacle named)
mechanism_class is left PENDING_MECH here — filled by r2_mechanism.py, never guessed.

Output: data/curated/disease_index.csv  (the ROADMAP R1 deliverable, completed in R2).
Deterministic given the cache: same cache -> same CSV (sorted, stable).
"""
import csv, os, re, sys, json, gzip, time, hashlib, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
BASE = os.path.join(ROOT, "data", "curated", "disease_index_base.csv")
CACHE_DIR = os.path.join(ROOT, "data", "raw", "medgen")
CACHE = os.path.join(CACHE_DIR, "inscope_esummary.jsonl.gz")
OUT = os.path.join(ROOT, "data", "curated", "disease_index.csv")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RETRIEVED = "2026-06-17"
TOOL = "disease_wp_r2"            # NCBI tool identifier (politeness)
CHUNK = 100                       # CUIs per esearch OR-query
SUMM_BATCH = 200                  # UIDs per esummary call
MIN_INTERVAL = 0.50              # ~2 req/s (conservative; NCBI 429s on bursts w/o key)

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
            req = urllib.request.Request(url, headers={"User-Agent": TOOL})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read().decode("utf-8", "replace")
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 4:
                time.sleep(2.0 * (attempt + 1))   # backoff on rate limit
                continue
            raise

def load_cache():
    """uid -> summary dict (the esummary result[uid] object)."""
    cache = {}
    if os.path.exists(CACHE):
        with gzip.open(CACHE, "rt", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                cache[rec["uid"]] = rec["summary"]
    # also fold in any legacy per-uid summary_<uid>.json (the flagship 18)
    for fn in os.listdir(CACHE_DIR):
        m = re.fullmatch(r"summary_(\d+)\.json", fn)
        if not m:
            continue
        uid = m.group(1)
        if uid in cache:
            continue
        try:
            js = json.load(open(os.path.join(CACHE_DIR, fn)))
            res = js.get("result", {})
            if uid in res:
                cache[uid] = res[uid]
        except Exception:
            pass
    return cache

def append_cache(new_items):
    """new_items: list of (uid, summary_dict)."""
    with gzip.open(CACHE, "at", encoding="utf-8") as fh:
        for uid, summ in new_items:
            fh.write(json.dumps({"uid": uid, "summary": summ}, ensure_ascii=False) + "\n")

def parse_moi(conceptmeta):
    names = re.findall(r"<ModeOfInheritance[^>]*>.*?<Name>(.*?)</Name>", conceptmeta or "", re.S)
    return sorted(set(n.strip() for n in names))

def get_def(summ):
    d = summ.get("definition", "")
    if isinstance(d, dict):
        d = d.get("value", "")
    return str(d).replace("\n", " ").strip()

def get_sty(summ):
    s = summ.get("semantictype", "")
    if isinstance(s, dict):
        s = s.get("value", "")
    return str(s).strip()

def chunks(xs, n):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]

def main():
    rows = list(csv.DictReader(open(BASE, encoding="utf-8")))
    by_cui = {r["medgen_cui"]: r for r in rows}
    inscope_cuis = [r["medgen_cui"] for r in rows if r["in_scope"] == "true"]
    print(f"in-scope CUIs to enrich: {len(inscope_cuis)}")

    cache = load_cache()
    cui_to_uid = {}
    for uid, summ in cache.items():
        cid = summ.get("conceptid", "")
        if cid:
            cui_to_uid[cid] = uid
    have = sum(1 for c in inscope_cuis if c in cui_to_uid)
    print(f"already cached (CUI->summary): {have}/{len(inscope_cuis)}")

    # ---- map missing CUIs -> UIDs via OR-batched esearch ----
    missing = [c for c in inscope_cuis if c not in cui_to_uid]
    new_uids = []
    if missing:
        print(f"resolving {len(missing)} CUIs via esearch ({len(list(chunks(missing,CHUNK)))} chunks)...")
        for ci, ch in enumerate(chunks(missing, CHUNK), 1):
            term = " OR ".join(ch)
            url = f"{EUTILS}/esearch.fcgi?db=medgen&retmax=600&retmode=json&term={urllib.parse.quote(term)}&tool={TOOL}"
            try:
                js = json.loads(get(url))
                uids = js["esearchresult"]["idlist"]
                new_uids.extend(uids)
            except Exception as e:
                print(f"  [esearch ERR chunk {ci}] {e}")
            if ci % 10 == 0:
                print(f"  esearch chunk {ci} ... pooled {len(new_uids)} UIDs")
        new_uids = sorted(set(new_uids) - set(cache.keys()), key=int)

    # ---- batch esummary the new UIDs, cache each ----
    if new_uids:
        print(f"fetching {len(new_uids)} new summaries ({len(list(chunks(new_uids,SUMM_BATCH)))} batches)...")
        for bi, ch in enumerate(chunks(new_uids, SUMM_BATCH), 1):
            idlist = ",".join(ch)
            try:
                js = json.loads(get(f"{EUTILS}/esummary.fcgi?db=medgen&retmode=json&id={idlist}&tool={TOOL}"))
                res = js.get("result", {})
                fresh = []
                for uid in res.get("uids", []):
                    summ = res[uid]
                    cache[uid] = summ
                    cid = summ.get("conceptid", "")
                    if cid:
                        cui_to_uid[cid] = uid
                    fresh.append((uid, summ))
                append_cache(fresh)
            except Exception as e:
                print(f"  [esummary ERR batch {bi}] {e}")
            if bi % 5 == 0:
                print(f"  esummary batch {bi} ... cached {len(cache)} total")

    # ---- assemble disease_index.csv over the in-scope set ----
    out = []
    n_moi = n_nomoi = n_nomedgen = 0
    for cui in inscope_cuis:
        b = by_cui[cui]
        uid = cui_to_uid.get(cui, "")
        summ = cache.get(uid, {}) if uid else {}
        if not summ:
            n_nomedgen += 1
            moi, defn, sty = [], "", ""
        else:
            moi = parse_moi(summ.get("conceptmeta", ""))
            defn = get_def(summ)
            sty = get_sty(summ)
        if moi:
            n_moi += 1
            inh_grade = "[L]"
            inh = "; ".join(moi)
            inh_src = f"medgen:esummary:ModeOfInheritance:{RETRIEVED}"
        else:
            n_nomoi += 1
            inh_grade = "[O]"
            inh = "not_stated"
            inh_src = (f"medgen:esummary:no_ModeOfInheritance:{RETRIEVED}"
                       if summ else f"medgen:no_concept_for_CUI:{RETRIEVED}")
        out.append({
            "entity": summ.get("title", b["entity"]) if summ else b["entity"],
            "medgen_cui": cui,
            "medgen_uid": uid,
            "omim_mim": b["omim_mim"],
            "genes": b["genes"],
            "n_genes": b["n_genes"],
            "inheritance_class": inh,
            "inheritance_grade": inh_grade,
            "inheritance_source": inh_src,
            "mechanism_class": "PENDING_MECH",
            "mechanism_grade": "",
            "mechanism_source": "",
            "semantic_type": sty,
            "organ_system_hint": b["organ_system_hint"],
            "in_scope": b["in_scope"],
            "exclusion_reason": b["exclusion_reason"],
            "clinical_definition": defn,
            "provenance": b["provenance"],
        })

    out.sort(key=lambda r: r["entity"].lower())
    cols = ["entity", "medgen_cui", "medgen_uid", "omim_mim", "genes", "n_genes",
            "inheritance_class", "inheritance_grade", "inheritance_source",
            "mechanism_class", "mechanism_grade", "mechanism_source",
            "semantic_type", "organ_system_hint", "in_scope", "exclusion_reason",
            "clinical_definition", "provenance"]
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    digest = hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:12]
    print("\n--- R2 stage-1 enrichment summary ---")
    print(f"  in-scope rows written : {len(out)}")
    print(f"  inheritance stated [L]: {n_moi}")
    print(f"  no inheritance     [O]: {n_nomoi}")
    print(f"    of which no MedGen concept for CUI: {n_nomedgen}")
    print(f"  cache entries (UIDs)  : {len(cache)}")
    print(f"  output: {OUT}")
    print(f"  output sha256[:12]: {digest}")

if __name__ == "__main__":
    main()
