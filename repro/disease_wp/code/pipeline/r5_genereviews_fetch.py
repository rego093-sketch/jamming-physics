#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R5 stage 1 -- GeneReviews accession & natural-history FETCH (the deferred [L] source).

INVESTIGATION ONLY. This is the network stage that pulls the accession-dated [L]
source named throughout the R3/R4 handovers: the GeneReviews chapter (NCBI Bookshelf)
for each cohort disease. ONE chapter fetch anchors BOTH deferred passes:
  * treatment accession-dating  -> the chapter's Management / Treatment section
  * natural-history registry     -> the chapter's Clinical Description / Natural
                                    History / Prognosis section

It writes NO grades and NO whitepaper prose. It only CACHES, per disease, a snapshot
{NBK accession, initial-posting + last-revision dates, retrieval date, full-page
sha256, and the extracted Management / natural-history section text}. The deterministic
apply stage (r5_accession_apply.py) reads ONLY this cache (no network) and lifts grades.

Honest matching (no false [L]): a chapter is accepted ONLY if a gene symbol or a
distinctive disease token appears in the chapter page <title>/<h1>. Unmatched diseases
are cached as {found:false} and STAY [H] downstream -- never fabricated.

Cache: data/raw/genereviews/<cui>.json    (one snapshot per disease)
       data/raw/genereviews/_fetch_log.json
"""
import urllib.request, urllib.parse, json, os, re, time, hashlib, csv, sys, gzip

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
DOSS = os.path.join(ROOT, "data", "curated", "dossiers")
CACHE = os.path.join(ROOT, "data", "raw", "genereviews")
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
BOOKURL = "https://www.ncbi.nlm.nih.gov/books"
RETRIEVED = "2026-06-17"
UA = {"User-Agent": "disease_wp/0.6 GeneReviews-accession-verification (research; ORCID 0009-0002-7535-8245)"}
SLEEP = 0.34   # < 3 req/s (NCBI courtesy, no key)

os.makedirs(CACHE, exist_ok=True)

def get(url, retries=3):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            return urllib.request.urlopen(req, timeout=45).read().decode("utf-8", "replace")
        except Exception as e:
            last = e; time.sleep(1.0 + i)
    raise last

def esearch_books(term, retmax=60):
    q = urllib.parse.quote(term)
    r = get(f"{EUTILS}/esearch.fcgi?db=books&term={q}&retmax={retmax}&retmode=json")
    time.sleep(SLEEP)
    return json.loads(r)["esearchresult"]["idlist"]

def esummary_books(ids):
    if not ids: return {}
    r = get(f"{EUTILS}/esummary.fcgi?db=books&id={','.join(ids)}&retmode=json")
    time.sleep(SLEEP)
    return json.loads(r).get("result", {})

# ---- section + date extraction from a GeneReviews chapter page ----
DATE_RE = re.compile(r"Initial Posting[^<:]*:\s*([A-Za-z]+ \d{1,2}, \d{4})"
                     r"(?:[^<]*?Last (?:Revision|Update)[^<:]*:\s*([A-Za-z]+ \d{1,2}, \d{4}))?", re.S)

# canonical GeneReviews section headings we care about
MGMT_HEADS = ["Treatment of Manifestations", "Management", "Targeted Therapies",
              "Agents/Circumstances to Avoid", "Therapies Under Investigation"]
NH_HEADS   = ["Clinical Description", "Natural History", "Prognosis",
              "Phenotype Correlations", "Genotype-Phenotype Correlations"]
# the GeneReviews Summary box always carries a one-line "Management" statement naming the
# established therapy; captured so treatment corroboration is not defeated when the deep
# Management section renders the drug under an unmatched sub-heading.
SUMMARY_HEADS = ["Summary"]

def strip_tags(html):
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    txt = re.sub(r"<[^>]+>", " ", html)
    txt = (txt.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
              .replace("&#x2019;", "'").replace("&#x2013;", "-").replace("&nbsp;", " ")
              .replace("&#x3b1;", "alpha").replace("&#x3b2;", "beta"))
    return re.sub(r"\s+", " ", txt).strip()

def extract_section(html, head_titles):
    """Grab the text under any <h2/h3> whose visible text matches one of head_titles,
       up to the next same-or-higher heading. Returns concatenated plain text."""
    chunks = []
    # find heading anchors; GeneReviews uses <h2 ...>Title</h2> ... or section divs
    for m in re.finditer(r"<(h[23])[^>]*>(.*?)</\1>", html, re.S | re.I):
        htext = strip_tags(m.group(2))
        for want in head_titles:
            if want.lower() in htext.lower():
                start = m.end()
                # next heading of same/higher level
                nxt = re.search(r"<h[123][^>]*>", html[start:], re.I)
                seg = html[start: start + (nxt.start() if nxt else 4000)]
                chunks.append(strip_tags(seg)[:2500])
                break
    return " ".join(chunks)[:6000]

def present_headings(html, head_titles):
    found = []
    heads = [strip_tags(m.group(2)) for m in re.finditer(r"<(h[23])[^>]*>(.*?)</\1>", html, re.S | re.I)]
    for want in head_titles:
        if any(want.lower() in h.lower() for h in heads):
            found.append(want)
    return found

def chapter_meta(html):
    # title: prefer citation_title meta, then <title> (trim the GeneReviews/NCBI suffix), then h1
    title = ""
    mc = re.search(r'<meta name="citation_title" content="([^"]+)"', html)
    if mc:
        title = mc.group(1).strip()
    else:
        mt = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        if mt:
            title = re.split(r"\s+-\s+GeneReviews", strip_tags(mt.group(1)))[0].strip()
    h1 = ""
    mh = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S | re.I)
    if mh:
        cand = strip_tags(mh.group(1))
        if cand and cand.lower() not in ("bookshelf", "ncbi bookshelf"):
            h1 = cand
    # dates: find the label, then the first "Month DD, YYYY" within the next ~160 chars of
    # tag-stripped text (GeneReviews renders the date in a following <span>, not inline).
    def date_after(label):
        m = re.search(label, html)
        if not m: return None
        window = strip_tags(html[m.end(): m.end() + 400])
        d = re.search(r"([A-Za-z]+ \d{1,2}, \d{4})", window)
        return d.group(1) if d else None
    posted = date_after(r"Initial Posting")
    revised = date_after(r"Last Revision") or date_after(r"Last Update")
    return title, h1, posted, revised

def load_cohort():
    rows = list(csv.DictReader(open(os.path.join(ROOT, "data", "curated", "treatments.csv"), newline="")))
    cohort = []
    doss_by_cui = {}
    for fn in os.listdir(DOSS):
        if fn.startswith("_") or not fn.endswith(".json"): continue
        d = json.load(open(os.path.join(DOSS, fn)))
        doss_by_cui[d["identity"]["medgen_cui"]] = d
    for r in rows:
        cui = r["cui"]; d = doss_by_cui.get(cui, {})
        genes = d.get("identity", {}).get("genes", []) or []
        cohort.append({"entity": r["entity"], "cui": cui, "genes": genes,
                       "source_class": r["source_class"]})
    return cohort

# distinctive disease tokens for title verification (drop generic words)
GENERIC = {"disease", "syndrome", "type", "deficiency", "disorder", "congenital",
           "classic", "hereditary", "i", "ii", "iii", "1", "2", "3", "4", "and", "of",
           "the", "a", "an"}
def disease_tokens(entity):
    toks = re.findall(r"[a-z0-9]+", entity.lower())
    return [t for t in toks if t not in GENERIC and len(t) > 2]

# --- Curated cui -> NBK map (the GeneReviews chapter for clinically-named diseases whose
# chapter title is NOT the gene symbol or our MedGen entity string, so title/gene auto-
# discovery cannot reach it, OR whose gene is shared by several chapters so a gene query is
# ambiguous -- e.g. HBB covers both sickle cell NBK1377 and beta-thalassemia NBK1426).
# Each NBK below was confirmed by direct fetch (citation_title + gene-in-body + a Management
# section present) on the retrieval date. This is TRANSPARENT, RECORDED curation -- the exact
# analogue of methodology/omim_join_supplement.csv -- not a blind hard-code: the apply stage
# still verifies the cached gene-in-body cross-check before using the chapter, and the fetch
# records match_basis="curated cui->NBK; verify(...)". A wrong NBK would fail the cross-check.
# Tuple: (NBK, note, overview_multi_phenotype). overview chapters cover several phenotypes of
# one gene, so the apply stage must NOT promote an [O] axis to [L] from them (contamination
# risk from sibling-phenotype text); they corroborate existing [H] axes only.
GENEREVIEWS_CURATED = {
    "C0917713": ("NBK1119", "Dystrophinopathies (Becker MD; DMD)", False),
    "C0013264": ("NBK1119", "Dystrophinopathies (Duchenne MD; DMD)", False),
    "C0268335": ("NBK1244", "Classic Ehlers-Danlos Syndrome (COL5A1)", False),
    "C0268338": ("NBK1494", "Vascular Ehlers-Danlos Syndrome (COL3A1)", False),
    "C0002895": ("NBK1377", "Sickle Cell Disease (HBB; shared-gene disambiguation vs beta-thal NBK1426)", False),
    "C0086795": ("NBK1162", "Mucopolysaccharidosis Type I (IDUA; Hurler)", False),
    "C0031485": ("NBK1504", "Phenylalanine Hydroxylase Deficiency (PAH; PKU)", False),
    "C0268242": ("NBK1370", "Acid Sphingomyelinase Deficiency (SMPD1; Niemann-Pick A)", False),
    "C0008533": ("NBK1495", "Hemophilia B (F9; factor IX deficiency)", False),
    "C0019069": ("NBK1404", "Hemophilia A (F8; factor VIII deficiency)", False),
    "C0017205": ("NBK1269", "Gaucher Disease (aggregate concept; no single causative gene annotated)", False),
    "C0017921": ("NBK1261", "Pompe Disease (GAA; shared-symbol disambiguation vs GAA-FGF14 ataxia NBK599589)", False),
    "C0220685": ("NBK540447", "Type II Collagen Disorders Overview (achondrogenesis type II; COL2A1)", True),
}

def verify_chapter(html, genes, dtoks):
    """Title + body verification signals for a candidate chapter."""
    title, h1, _, _ = chapter_meta(html)
    hay = (title + " " + h1).lower()
    gene_title = any(g.lower() in hay for g in genes if g and g != "-")
    tok_title = sum(1 for t in dtoks if t in hay)
    body = strip_tags(html).lower()
    gene_body = any(re.search(r"\b" + re.escape(g.lower()) + r"\b", body)
                    for g in genes if g and g != "-")
    return gene_title, tok_title, gene_body

def find_chapter(item):
    """Return (nbk, page_html, match_basis) or (None, None, reason).

    Two disjoint paths:
      (a) CURATED cui -> NBK : direct fetch of the confirmed chapter, recorded with a
          gene-in-body (or distinctive-title-token, for gene-less aggregates) cross-check.
      (b) AUTO discovery     : esearch by gene[Title] then disease name, accept a candidate
          ONLY if a gene symbol or a distinctive disease token appears in the chapter TITLE
          (title-only; no permissive gene-in-body, which over-matched shared-gene chapters).
    """
    genes = item["genes"]; entity = item["entity"]; cui = item["cui"]
    dtoks = disease_tokens(entity)

    # (a) curated direct fetch -------------------------------------------------
    if cui in GENEREVIEWS_CURATED:
        nbk, note, _ = GENEREVIEWS_CURATED[cui]
        try:
            html = get(f"{BOOKURL}/{nbk}/")
            time.sleep(SLEEP)
        except Exception as e:
            return None, None, f"curated NBK {nbk} fetch failed: {e}"
        gene_title, tok_title, gene_body = verify_chapter(html, genes, dtoks)
        has_gene = any(g and g != "-" for g in genes)
        # gene-less aggregate (Gaucher): verify by a distinctive title token instead
        ok = gene_body if has_gene else (tok_title >= 1)
        if not ok:
            return None, None, (f"curated NBK {nbk} failed cross-check "
                                f"(gene_in_body={gene_body}, title_tokens={tok_title})")
        basis = (f"curated cui->NBK [{note}]; verify(gene_title={gene_title}, "
                 f"title_tokens={tok_title}, gene_in_body={gene_body})")
        return nbk, html, basis

    # (b) auto discovery, title-only verification ------------------------------
    queries = []
    for g in genes:
        if g and g != "-":
            queries.append((f'{g}[Title] AND gene[book]', f"gene:{g}"))
    short = " ".join(entity.split()[:4])
    queries.append((f'{short} AND gene[book]', "disease-name"))
    queries.append((f'{entity} AND gene[book]', "disease-name-full"))

    tried = set()
    for term, qlabel in queries:
        try:
            ids = esearch_books(term)
        except Exception:
            continue
        if not ids: continue
        summ = esummary_books(ids[:50])
        tally = {}
        for uid, rec in summ.items():
            if not isinstance(rec, dict):  # skip the 'uids' list entry
                continue
            nbk = rec.get("chapteraccessionid") or rec.get("accessionid")
            if nbk and nbk.startswith("NBK"):
                tally[nbk] = tally.get(nbk, 0) + 1
        for nbk, _ in sorted(tally.items(), key=lambda kv: -kv[1]):
            if nbk in tried: continue
            tried.add(nbk)
            try:
                html = get(f"{BOOKURL}/{nbk}/")
                time.sleep(SLEEP)
            except Exception:
                continue
            gene_title, tok_title, _ = verify_chapter(html, genes, dtoks)
            if gene_title or tok_title >= 1:   # TITLE-ONLY (no permissive gene-in-body)
                basis = f"{qlabel}; verify(gene_title={gene_title}, title_tokens={tok_title})"
                return nbk, html, basis
    return None, None, "no GeneReviews chapter matched (gene/disease token absent from chapter title)"

def main():
    cohort = load_cohort()
    log = []
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for item in cohort:
        cui = item["cui"]
        if only and cui not in only: continue
        nbk, html, basis = find_chapter(item)
        rec = {"schema": "disease_wp.genereviews_snapshot/v1", "phase": "R5",
               "entity": item["entity"], "cui": cui, "genes": item["genes"],
               "retrieved": RETRIEVED, "found": bool(nbk)}
        if nbk:
            title, h1, posted, revised = chapter_meta(html)
            page_sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
            mgmt_text = extract_section(html, MGMT_HEADS)
            nh_text   = extract_section(html, NH_HEADS)
            curated = cui in GENEREVIEWS_CURATED
            overview = GENEREVIEWS_CURATED[cui][2] if curated else False
            rec.update({
                "nbk": nbk,
                "chapter_title": title or h1,
                "url": f"{BOOKURL}/{nbk}/",
                "date_initial_posting": posted,
                "date_last_revision": revised,
                "page_sha256": page_sha,
                "match_basis": basis,
                "curated": curated,
                "overview_multi_phenotype": overview,
                "management_sections_present": present_headings(html, MGMT_HEADS),
                "naturalhistory_sections_present": present_headings(html, NH_HEADS),
                "management_text": mgmt_text,
                "summary_text": extract_section(html, SUMMARY_HEADS),
                "naturalhistory_text": nh_text,
            })
            print(f"[OK ] {item['entity'][:40]:40} {nbk:9} posted={posted} revised={revised} "
                  f"mgmt={len(rec['management_sections_present'])} nh={len(rec['naturalhistory_sections_present'])}")
        else:
            rec["obstacle"] = basis
            print(f"[ -- ] {item['entity'][:40]:40} {basis}")
        json.dump(rec, open(os.path.join(CACHE, f"{cui}.json"), "w"),
                  ensure_ascii=False, indent=2)
        log.append({"cui": cui, "entity": item["entity"], "found": bool(nbk),
                    "nbk": rec.get("nbk"), "revised": rec.get("date_last_revision")})
    json.dump({"retrieved": RETRIEVED, "n": len(log),
               "found": sum(1 for x in log if x["found"]), "items": log},
              open(os.path.join(CACHE, "_fetch_log.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\nGeneReviews fetch: {sum(1 for x in log if x['found'])}/{len(log)} chapters matched.")

if __name__ == "__main__":
    main()
