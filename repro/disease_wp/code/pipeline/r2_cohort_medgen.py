#!/usr/bin/env python3
"""
R2 dossier support — fetch a self-contained MedGen esummary cache for the
curated dossier cohort (methodology/dossier_cohort.csv).

For each cohort concept we keep:
  - the MedGen clinical definition (narrative clinical source),
  - every OMIM phenotype code cross-referenced in <conceptmeta> (SAB="OMIM"),
    used to join the authoritative HPO disease-phenotype annotations,
  - the ModeOfInheritance name if MedGen states one.

Small, targeted, cached, resumable. Network only for concepts not already cached.

Out: data/raw/medgen/dossier_cohort_esummary.json
"""
import csv, os, json, time, re, urllib.parse, urllib.request, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
COHORT = os.path.join(ROOT, "methodology", "dossier_cohort.csv")
IDX = os.path.join(ROOT, "data", "curated", "disease_index.csv")
OUT = os.path.join(ROOT, "data", "raw", "medgen", "dossier_cohort_esummary.json")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
MIN_INTERVAL = 0.5
RETRIEVED = "2026-06-17"

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
        except Exception as e:
            if attempt == 4:
                raise
            time.sleep(1.5 * (attempt + 1))

def parse_conceptmeta(meta_str):
    """Extract OMIM phenotype codes and MOI from the conceptmeta XML blob."""
    omims, moi = set(), ""
    if not meta_str:
        return sorted(omims), moi
    try:
        root = ET.fromstring("<root>" + meta_str + "</root>")
    except ET.ParseError:
        # fall back to regex on SAB="OMIM" ... CODE="######"
        for m in re.finditer(r'SAB="OMIM"[^>]*?(?:CODE|SDUI)="(\d{6})"', meta_str):
            omims.add(m.group(1))
        for m in re.finditer(r'CODE="(\d{6})"[^>]*?SAB="OMIM"', meta_str):
            omims.add(m.group(1))
        mm = re.search(r'<ModeOfInheritance[^>]*>.*?<Name[^>]*>([^<]+)</Name>', meta_str)
        if mm:
            moi = mm.group(1).strip()
        return sorted(omims), moi
    for nm in root.iter("Name"):
        if nm.get("SAB") == "OMIM":
            code = nm.get("CODE") or nm.get("SDUI") or ""
            if re.fullmatch(r"\d{6}", code or ""):
                omims.add(code)
    moi_el = root.find(".//ModeOfInheritance")
    if moi_el is not None:
        nm = moi_el.find(".//Name")
        if nm is not None and nm.text:
            moi = nm.text.strip()
    return sorted(omims), moi

def main():
    idx = {r["medgen_cui"]: r for r in csv.DictReader(open(IDX, encoding="utf-8"))}
    cohort = list(csv.DictReader(open(COHORT, encoding="utf-8")))
    uid_by_cui = {m["cui"]: idx[m["cui"]]["medgen_uid"] for m in cohort if m["cui"] in idx}

    cache = {}
    if os.path.exists(OUT):
        cache = json.load(open(OUT, encoding="utf-8"))

    todo = [(cui, uid) for cui, uid in uid_by_cui.items() if cui not in cache]
    if todo:
        ids = ",".join(uid for _, uid in todo)
        url = f"{BASE}/esummary.fcgi?db=medgen&id={ids}&retmode=json"
        data = json.loads(get(url))
        res = data.get("result", {})
        for cui, uid in todo:
            s = res.get(uid, {})
            meta = s.get("conceptmeta", "")
            omims, moi = parse_conceptmeta(meta)
            cache[cui] = {
                "cui": cui, "uid": uid,
                "title": s.get("title", ""),
                "definition": (s.get("definition", {}) or {}).get("value", "") if isinstance(s.get("definition"), dict) else (s.get("definition") or ""),
                "semantictype": s.get("semantictype", ""),
                "omim_codes": omims,
                "medgen_moi": moi,
                "retrieved": RETRIEVED,
            }
        json.dump(cache, open(OUT, "w"), indent=1, ensure_ascii=False)

    # report
    print("--- cohort MedGen esummary cache ---")
    print(f"  concepts: {len(cache)} (cohort size {len(cohort)})")
    nomim = sum(1 for c in cache.values() if c["omim_codes"])
    print(f"  with >=1 OMIM cross-ref: {nomim}")
    for cui in uid_by_cui:
        c = cache.get(cui, {})
        print(f"  {cui} {c.get('title','?')[:36]:36s} OMIM={','.join(c.get('omim_codes',[])) or '(none)':22s} MOI={c.get('medgen_moi','') or '-'}")

if __name__ == "__main__":
    main()
