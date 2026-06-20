#!/usr/bin/env python3
# =============================================================================
# R14 fetch -- pin & verify the PMC open-access full text cited by the round-6
# severity/progression curation (methodology/severity_litcurate6_join.csv and
# severity_litcurate6_excluded.csv). This is the FETCH half of the R13 pass;
# it reuses the EXACT efetch / strip / open-access / id helpers of the R9 fetch
# stage (imported through R13 -> R12 -> R11 -> R10, not re-implemented) so the pinned-
# snapshot format and the OA determination cannot drift. Writes to the SAME
# pinned cache (data/raw/litcurate/) and is idempotent: a snapshot whose stored
# text still matches its own sha256 is left untouched. No tuning, no parsing
# changes -- only the set of cited PMCIDs (taken from the R14 CSVs) differs from
# R9/R10/R11/R12/R13.
# =============================================================================
import os, csv, json, hashlib, importlib.util, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
METH = os.path.join(ROOT, "methodology")

# reuse the R9 fetch helpers verbatim (via R13 -> R12 -> R11 -> R10's fetch module):
# efetch_pmc, strip_xml, is_open_access, article_title, id_of, CACHE, RETRIEVED
_s = importlib.util.spec_from_file_location("r13_fetch", os.path.join(HERE, "r13_litcurate_fetch.py"))
F13 = importlib.util.module_from_spec(_s); _s.loader.exec_module(F13)
F = F13.F                       # the underlying R9 fetch module (through R10/R11/R12/R13)

CACHE = F.CACHE
RETRIEVED = F.RETRIEVED
LOG = os.path.join(CACHE, "_fetch_log_r14.json")


def cited_pmcids():
    """Union of PMCIDs referenced by the R13 round-6 join and excluded CSVs."""
    ids = collections.OrderedDict()
    for fn, col in (("severity_litcurate6_join.csv", "pmcid"),
                    ("severity_litcurate6_excluded.csv", "considered_pmcid")):
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
        print("  (no R14 curation CSVs yet; nothing to fetch)")
        json.dump({"retrieved": RETRIEVED, "articles": {}, "found": 0, "cited": 0},
                  open(LOG, "w"), indent=2, ensure_ascii=False)
        return
    log = {"source": "PubMed Central open-access (eutils.ncbi.nlm.nih.gov), full-text XML",
           "retrieved": RETRIEVED, "round": "R14", "articles": {}}
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
            xml = F.efetch_pmc(pmcid)
        except Exception as e:
            json.dump({"pmcid": pmcid, "found": False, "error": str(e), "retrieved": RETRIEVED},
                      open(path, "w"), indent=2, ensure_ascii=False)
            log["articles"][pmcid] = {"action": "error", "error": str(e)}
            continue
        oa = F.is_open_access(xml)
        body = F.strip_xml(xml)
        title = F.article_title(xml)
        pmid = F.id_of(xml, "pmid")
        rec_pmcid = F.id_of(xml, "pmc") or F.id_of(xml, "pmcid")
        snap = {"pmcid": pmcid, "resolved_pmcid": ("PMC" + rec_pmcid) if rec_pmcid else None,
                "pmid": pmid, "title": title, "open_access": oa, "found": True,
                "retrieved": RETRIEVED,
                "text_sha256": hashlib.sha256(body.encode("utf-8")).hexdigest(),
                "text": body[:300000]}
        json.dump(snap, open(path, "w"), indent=2, ensure_ascii=False)
        log["articles"][pmcid] = {"action": "fetched", "pmid": pmid, "open_access": oa, "title": title}
        found += 1
        print(f"  {pmcid}  PMID:{pmid}  OA={oa}  {title[:62]}")
    log["found"] = found
    log["cited"] = len(ids)
    json.dump(log, open(LOG, "w"), indent=2, ensure_ascii=False)
    print(f"\n  OA articles cached for {found}/{len(ids)} R14-cited PMCIDs -> data/raw/litcurate/")


if __name__ == "__main__":
    main()
