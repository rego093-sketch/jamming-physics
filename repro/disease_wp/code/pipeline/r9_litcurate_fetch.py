#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R9 stage 1 -- curated SEVERITY / PROGRESSION literature FETCH (open M/S/P source).

R8 lifted SEVERITY for the one cohort disease whose obligate dominant sequela is
annotated in the open HPO Severity subtree, and recorded that the *remaining*
severity/progression lift -- where it exists at all -- is via deliberate,
human-in-the-loop curation from citeable published functional & survival
literature. This stage is the FETCH half of that R9 curation pass.

For each disease the author has curated (methodology/severity_litcurate_join.csv
and ..._excluded.csv name the PMCIDs), this stage fetches the cited PubMed Central
OPEN-ACCESS article full text and caches it with a pinned sha256, so the offline
apply stage (r9_severity_litcurate.py) and the gate (r9_gate.py) can RE-FIND the
exact curated disease-level magnitude sentence in the pinned text -- the citation
cannot drift. Only PMC open-access (CC-licensed, redistributable) articles are
cached; the snapshot stores the stripped article text and both the PMCID and PMID.

This does NOT decide tiers and does NOT touch the registry. It only pins the
sources the curation cites. The tier is DERIVED downstream by applying the FROZEN
R3 progression/severity tier function to the curated sentence (no new cut-points).

Network: only this stage touches the network (NCBI E-utilities, no key, <3 req/s).
Idempotent: an article already cached whose recorded PMCID + text_sha256 still
verify is not re-fetched. INVESTIGATION/AUTHORING support -- NOT in the engine pin.

Out: data/raw/litcurate/<PMCID>.json   (one OA article snapshot per cited source)
     data/raw/litcurate/_fetch_log.json
"""
import os, sys, re, csv, json, time, hashlib, urllib.request, urllib.parse, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
METH = os.path.join(ROOT, "methodology")
CACHE = os.path.join(ROOT, "data", "raw", "litcurate")
LOG = os.path.join(CACHE, "_fetch_log.json")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RETRIEVED = "2026-06-18"
UA = {"User-Agent": "disease_wp/0.11 R9-litcurate-NH (research; ORCID 0009-0002-7535-8245)"}
SLEEP = 0.34


def get(url, retries=3):
    last = None
    for i in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45).read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(1.0 + i)
    raise last


def efetch_pmc(pmcid):
    pid = pmcid[3:] if pmcid.upper().startswith("PMC") else pmcid
    r = get(f"{EUTILS}/efetch.fcgi?db=pmc&id={pid}&rettype=full&retmode=xml")
    time.sleep(SLEEP)
    return r


def strip_xml(x):
    x = re.sub(r"<(table-wrap|fig|ref-list|back)\b.*?</\1>", " ", x, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", x)
    for a, b in [("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"), ("&#x2013;", "-"),
                 ("&#x2014;", "-"), ("&#x2019;", "'"), ("&#x3b1;", "alpha"),
                 ("&#x3b2;", "beta"), ("&nbsp;", " ")]:
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def article_title(xml):
    m = re.search(r"<article-title>(.*?)</article-title>", xml, re.S | re.I)
    return strip_xml(m.group(1)) if m else ""


def id_of(xml, kind):
    m = re.search(rf'<article-id pub-id-type="{kind}">\s*(?:PMC)?(\d+)', xml, re.I)
    return m.group(1) if m else None


def is_open_access(xml):
    # PMC OA subset is flagged in the license / open-access tags; accept when an
    # open-access or CC license marker is present in the article metadata.
    return bool(re.search(r'license[^>]*license-type="open-access"', xml, re.I)
                or re.search(r"creativecommons\.org", xml, re.I)
                or re.search(r"\bopen access\b", xml, re.I))


def cited_pmcids():
    """Union of PMCIDs referenced by the join and excluded curation CSVs."""
    ids = collections.OrderedDict()
    for fn, col in (("severity_litcurate_join.csv", "pmcid"),
                    ("severity_litcurate_excluded.csv", "considered_pmcid")):
        p = os.path.join(METH, fn)
        if not os.path.exists(p):
            continue
        with open(p, newline="") as fh:
            for r in csv.DictReader(fh):
                pm = (r.get(col) or "").strip()
                if pm:
                    ids.setdefault(pm.upper(), []).append(r.get("entity", ""))
    return ids


def main():
    os.makedirs(CACHE, exist_ok=True)
    ids = cited_pmcids()
    if not ids:
        print("  (no curation CSVs yet; nothing to fetch)")
        json.dump({"retrieved": RETRIEVED, "articles": {}, "found": 0, "cited": 0},
                  open(LOG, "w"), indent=2, ensure_ascii=False)
        return
    log = {"source": "PubMed Central open-access (eutils.ncbi.nlm.nih.gov), full-text XML",
           "retrieved": RETRIEVED, "articles": {}}
    found = 0
    for pmcid in ids:
        path = os.path.join(CACHE, f"{pmcid}.json")
        if os.path.exists(path):
            prev = json.load(open(path))
            if prev.get("found") and prev.get("text_sha256") and \
               hashlib.sha256(prev["text"].encode("utf-8")).hexdigest() == prev["text_sha256"]:
                log["articles"][pmcid] = {"action": "cached", "pmid": prev.get("pmid"),
                                          "title": prev.get("title")}
                found += 1
                continue
        try:
            xml = efetch_pmc(pmcid)
        except Exception as e:
            json.dump({"pmcid": pmcid, "found": False, "error": str(e), "retrieved": RETRIEVED},
                      open(path, "w"), indent=2, ensure_ascii=False)
            log["articles"][pmcid] = {"action": "error", "error": str(e)}
            continue
        oa = is_open_access(xml)
        body = strip_xml(xml)
        title = article_title(xml)
        pmid = id_of(xml, "pmid")
        rec_pmcid = id_of(xml, "pmc") or id_of(xml, "pmcid")
        snap = {"pmcid": pmcid, "resolved_pmcid": ("PMC" + rec_pmcid) if rec_pmcid else None,
                "pmid": pmid, "title": title, "open_access": oa, "found": True,
                "retrieved": RETRIEVED,
                "text_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "text": body[:300000]}
        json.dump(snap, open(path, "w"), indent=2, ensure_ascii=False)
        log["articles"][pmcid] = {"action": "fetched", "pmid": pmid, "open_access": oa,
                                  "title": title}
        found += 1
        print(f"  {pmcid}  PMID:{pmid}  OA={oa}  {title[:62]}")
    log["found"] = found
    log["cited"] = len(ids)
    json.dump(log, open(LOG, "w"), indent=2, ensure_ascii=False)
    print(f"\n  OA articles cached for {found}/{len(ids)} cited PMCIDs -> data/raw/litcurate/")


if __name__ == "__main__":
    main()
