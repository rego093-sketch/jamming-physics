#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R7 stage -- PMC open-access survival / natural-history FETCH (open M source).

The R6 limitation was that Orphadata carries no age-of-death field, so the 18 [O]
mortality (M) axes could not be lifted from the registry. The open path is the
PUBLISHED survival literature in PubMed Central. This stage fetches, PER DISEASE,
one entity-verified open-access natural-history / survival article and caches its
full text with a pinned sha, so the offline apply stage can read an explicit,
QUANTITATIVE, disease-anchored survival statement (median survival / age of death /
explicit normal-life-expectancy) and map it to the R3 MORT_VAL tier -- cited.

Why this does NOT repeat the over-trigger R5 withheld: R5's risk was a first-match
over a whole chapter picking up any stray mention. Here (a) the article is accepted
only if a distinctive disease token appears in its OA <article-title>, and (b) the
apply stage lifts M only from a sentence that contains BOTH a disease token AND a
fixed QUANTITATIVE survival pattern -- a far narrower signal than "a word appears
somewhere". Where no qualifying sentence exists, M is left unchanged (honest null).

Progression (P) is deliberately NOT lifted from free text here: typical-course
adjectives are too context-dependent to extract safely without the structured
OMIM synopsis; that lift stays deferred (obstacle recorded by the apply stage).

Network: only this stage touches the network (NCBI E-utilities, no key, <3 req/s).
Idempotent: an article already cached whose recorded PMCID+sha still verify is not
re-fetched. INVESTIGATION/AUTHORING support -- NOT in the frozen engine pin.

Out: data/raw/litsurvival/<cui>.json  (one OA article snapshot per disease)
     data/raw/litsurvival/_fetch_log.json
"""
import os, sys, re, json, time, hashlib, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
CACHE = os.path.join(ROOT, "data", "raw", "litsurvival")
LOG = os.path.join(CACHE, "_fetch_log.json")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
RETRIEVED = "2026-06-18"
UA = {"User-Agent": "disease_wp/0.9 PMC-survival-NH (research; ORCID 0009-0002-7535-8245)"}
SLEEP = 0.34

GENERIC = {"disease", "syndrome", "type", "deficiency", "disorder", "congenital", "classic",
           "hereditary", "i", "ii", "iii", "iv", "1", "2", "3", "4", "and", "of", "the", "a", "an"}


def get(url, retries=3):
    last = None
    for i in range(retries):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=45).read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(1.0 + i)
    raise last


def esearch_pmc(term, retmax=20):
    q = urllib.parse.quote(term)
    r = get(f"{EUTILS}/esearch.fcgi?db=pmc&term={q}&retmax={retmax}&retmode=json")
    time.sleep(SLEEP)
    return json.loads(r)["esearchresult"].get("idlist", [])


def efetch_pmc(pmcid):
    r = get(f"{EUTILS}/efetch.fcgi?db=pmc&id={pmcid}&rettype=full&retmode=xml")
    time.sleep(SLEEP)
    return r


def strip_xml(x):
    x = re.sub(r"<(table-wrap|fig|ref-list|back)\b.*?</\1>", " ", x, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", x)
    t = (t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          .replace("&#x2013;", "-").replace("&#x2014;", "-").replace("&#x2019;", "'")
          .replace("&#x3b1;", "alpha").replace("&#x3b2;", "beta").replace("&nbsp;", " "))
    return re.sub(r"\s+", " ", t).strip()


def article_title(xml):
    m = re.search(r"<article-title>(.*?)</article-title>", xml, re.S | re.I)
    return strip_xml(m.group(1)) if m else ""


def pmcid_of(xml):
    m = re.search(r'<article-id pub-id-type="pmc(?:id)?">\s*(?:PMC)?(\d+)', xml, re.I)
    return ("PMC" + m.group(1)) if m else None


def disease_tokens(entity):
    return [t for t in re.findall(r"[a-z0-9]+", entity.lower()) if t not in GENERIC and len(t) > 2]


def load_cohort():
    base = json.load(open(os.path.join(CUR, "burden_scores_registry.json")))
    return [{"entity": r["entity"], "cui": r["cui"], "genes": r.get("genes", [])} for r in base["records"]]


def best_article(entity, dtoks):
    """Find one OA full-text article whose <article-title> contains a disease token.
       Query is title-anchored + natural-history/survival-scoped + OA-filtered."""
    primary = entity.split(",")[0].strip()
    queries = [
        f'"{primary}"[Title] AND open access[filter] AND ("natural history"[tiab] OR survival[tiab] OR prognosis[tiab] OR "life expectancy"[tiab])',
        f'"{primary}"[Title] AND open access[filter] AND review[pt]',
        f'"{primary}"[Title] AND open access[filter]',
    ]
    for q in queries:
        for pmcid in esearch_pmc(q, retmax=15):
            pid = "PMC" + pmcid if not pmcid.startswith("PMC") else pmcid
            try:
                xml = efetch_pmc(pmcid)
            except Exception:
                continue
            title = article_title(xml)
            if title and any(t in title.lower() for t in dtoks):
                return pid, title, xml, q
    return None, None, None, None


def main():
    os.makedirs(CACHE, exist_ok=True)
    cohort = load_cohort()
    log = {"source": "PubMed Central open-access (eutils.ncbi.nlm.nih.gov), full-text XML",
           "retrieved": RETRIEVED, "articles": {}}
    found = 0
    for c in cohort:
        cui, entity = c["cui"], c["entity"]
        path = os.path.join(CACHE, f"{cui}.json")
        if os.path.exists(path):
            prev = json.load(open(path))
            if prev.get("found") and prev.get("text_sha256"):
                log["articles"][cui] = {"entity": entity, "action": "cached",
                                        "pmcid": prev.get("pmcid"), "title": prev.get("title")}
                found += 1
                continue
        dtoks = disease_tokens(entity)
        try:
            pmcid, title, xml, q = best_article(entity, dtoks)
        except Exception as e:
            json.dump({"entity": entity, "cui": cui, "found": False, "error": str(e),
                       "retrieved": RETRIEVED}, open(path, "w"), indent=2, ensure_ascii=False)
            log["articles"][cui] = {"entity": entity, "action": "error", "error": str(e)}
            continue
        if not pmcid:
            json.dump({"entity": entity, "cui": cui, "found": False,
                       "reason": "no OA article with a disease token in <article-title>",
                       "retrieved": RETRIEVED}, open(path, "w"), indent=2, ensure_ascii=False)
            log["articles"][cui] = {"entity": entity, "action": "not_found"}
            continue
        body = strip_xml(xml)
        snap = {"entity": entity, "cui": cui, "found": True, "pmcid": pmcid, "title": title,
                "query": q, "retrieved": RETRIEVED,
                "text_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "text": body[:200000]}
        json.dump(snap, open(path, "w"), indent=2, ensure_ascii=False)
        log["articles"][cui] = {"entity": entity, "action": "fetched", "pmcid": pmcid, "title": title}
        found += 1
        print(f"  {entity[:40]:40s} {pmcid}  {title[:60]}")

    log["found"] = found
    log["cohort"] = len(cohort)
    json.dump(log, open(LOG, "w"), indent=2, ensure_ascii=False)
    print(f"\n  OA articles cached for {found}/{len(cohort)} diseases -> data/raw/litsurvival/")


if __name__ == "__main__":
    main()
