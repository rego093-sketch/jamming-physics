"""
V10 source fetcher — vendor an independently-assembled gamma-RESTORE-mechanism snapshot.

WHY (V10 = exclusion calibration, blueprint §5.3):
  The kit excludes the gamma-RESTORE lever family on every LOF_null disease (86 of them).
  That exclusion is an assertion: "no corrector / pharmacological chaperone / read-through /
  potentiator is KNOWN for this gene" (else the kit would have called the lesion
  LOF_missense_residual and ADMITTED gamma-restore — see §3.1 residual_allele_evidence).
  V10 tests those 86 exclusions against an INDEPENDENTLY-ASSEMBLED pharmacology source and
  reports MISSES (a gene the kit called null for which a gamma-restore-type agent in fact exists).

WHAT THIS FETCHES (per gene, dated + pinned like every external source in this kit):
  OpenTargets Platform GraphQL, surfacing ChEMBL `mechanismsOfAction` on the GENE'S OWN edge:
  for each (drug, this-gene) we keep actionType + mechanismOfAction free text + maxClinicalStage.
  The gamma-restore CLASSIFIER (which mechanisms count) is FROZEN in the V10 prereg, NOT here —
  this fetcher only assembles the raw evidence, blind to the kit's lesion calls.

STATUS per gene:
  OK           query succeeded; chaperone_evidence may be [] (genuine: no corrector-type agent
               annotated on this gene) or non-empty (scorable)
  NO_ENSEMBL   the symbol did not resolve to an OpenTargets target (coverage gap, reported)
  FETCH_FAILED network/HTTP error after retries -> reported as fetch-incomplete, NEVER conflated
               with "no corrector" (excluded from the calibrated denominator)

Determinism: result is a vendored cache. The holdout NEVER live-fetches.
"""
import os, sys, json, time
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DI_PATH    = os.path.join(ROOT, "inputs", "disease_inputs.json")
CACHE_PATH = os.path.join(HERE, "v10_opentargets_chaperone_snapshot.cache.json")
URL = "https://api.platform.opentargets.org/api/v4/graphql"

Q_SEARCH = ('query($s:String!){search(queryString:$s,entityNames:["target"])'
            '{hits{id object{... on Target{approvedSymbol}}}}}')
# Pull actionType + free-text mechanismOfAction + clinical stage. Gene-edge filtered downstream.
Q_DRUGS = ('query($e:String!){target(ensemblId:$e){approvedSymbol '
           'drugAndClinicalCandidates{count rows{maxClinicalStage '
           'drug{id name mechanismsOfAction{rows{actionType mechanismOfAction targets{id}}}}}}}}')
Q_META = ('query{meta{apiVersion{x y z} dataVersion{year month}}}')

S = requests.Session()
S.headers.update({"Content-Type": "application/json"})


def gql(q, v=None, tries=4, tmo=45):
    last = "?"
    for i in range(tries):
        try:
            r = S.post(URL, json={"query": q, "variables": v or {}}, timeout=tmo)
            if r.status_code == 200:
                j = r.json()
                if "errors" in j and j.get("data") is None:
                    last = "graphql_errors:" + json.dumps(j["errors"])[:120]
                else:
                    return j
            else:
                last = f"HTTP {r.status_code}"
        except Exception as e:
            last = type(e).__name__
        time.sleep(1.0 * (i + 1))
    raise RuntimeError(f"GraphQL failed after {tries}: {last}")


def resolve_ensembl(sym):
    j = gql(Q_SEARCH, {"s": sym})
    hits = (j.get("data", {}).get("search", {}) or {}).get("hits", []) or []
    for h in hits:
        if (h.get("object") or {}).get("approvedSymbol") == sym:
            return h["id"]
    return None   # exact-symbol miss only; never a fuzzy fallback (wrong-gene risk)


def fetch_gene(sym):
    eid = resolve_ensembl(sym)
    if not eid:
        return dict(ensembl_id=None, fetch_status="NO_ENSEMBL", drug_edges=[])
    j = gql(Q_DRUGS, {"e": eid})
    rows = (((j.get("data", {}).get("target", {}) or {}).get("drugAndClinicalCandidates", {}) or {})
            .get("rows", []) or [])
    edges = []
    seen = set()
    for r in rows:
        stage = r.get("maxClinicalStage")
        d = r.get("drug") or {}
        did = d.get("id")
        for ma in ((d.get("mechanismsOfAction") or {}).get("rows", []) or []):
            tids = {t["id"] for t in (ma.get("targets") or [])}
            if eid not in tids:
                continue   # keep ONLY mechanisms annotated on THIS gene's own edge
            at = (ma.get("actionType") or "")
            moa = (ma.get("mechanismOfAction") or "")
            key = (did, at, moa)
            if key in seen:
                continue
            seen.add(key)
            edges.append(dict(drug_id=did, drug=d.get("name"),
                              action_type=at, mechanism_of_action=moa, max_clinical_stage=stage))
    return dict(ensembl_id=eid, fetch_status="OK", drug_edges=edges)


def main():
    di = json.load(open(DI_PATH))
    # every gene across every disease (primary + secondary) so the join is complete
    genes = sorted({g["gene"] for rec in di.values() for g in rec["genes"]})

    if os.path.exists(CACHE_PATH):
        cache = json.load(open(CACHE_PATH))
    else:
        meta = {}
        try:
            meta = gql(Q_META).get("data", {}).get("meta", {})
        except Exception:
            meta = {}
        cache = dict(
            source="OpenTargets Platform GraphQL (surfacing ChEMBL mechanismsOfAction on the gene's own edge)",
            purpose=("V10 exclusion calibration: independently-assembled evidence for whether a "
                     "gamma-restore-type agent (chaperone/corrector/potentiator/read-through) is "
                     "KNOWN for each gene. The classifier is frozen in V10_PREREGISTRATION.json, "
                     "NOT here; this snapshot is blind to the kit's lesion calls."),
            transport_note=("ChEMBL's own REST API returned HTTP 500 this session; ChEMBL mechanism "
                            "actionType + mechanismOfAction is therefore surfaced via OpenTargets "
                            "(same upstream curation as V4). Independence vs V4 is in the QUESTION "
                            "(corrector-existence, not direction), not a new assembler."),
            fetched_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            opentargets_meta=meta,
            edges_by_symbol={})

    by = cache["edges_by_symbol"]
    todo = [g for g in genes if g not in by or by[g].get("fetch_status") == "FETCH_FAILED"]
    print(f"genes total={len(genes)} already={len(genes)-len(todo)} todo={len(todo)}")
    t0 = time.time()
    for i, g in enumerate(todo):
        try:
            by[g] = fetch_gene(g)
        except Exception as e:
            by[g] = dict(ensembl_id=None, fetch_status="FETCH_FAILED", error=str(e)[:120], drug_edges=[])
        if (i + 1) % 10 == 0 or i == len(todo) - 1:
            json.dump(cache, open(CACHE_PATH, "w"), indent=2, sort_keys=True)
            print(f"  {i+1}/{len(todo)}  {g}  ({time.time()-t0:.0f}s)")
        time.sleep(0.15)
    json.dump(cache, open(CACHE_PATH, "w"), indent=2, sort_keys=True)
    ok = sum(1 for g in genes if by[g]["fetch_status"] == "OK")
    ne = sum(1 for g in genes if by[g]["fetch_status"] == "NO_ENSEMBL")
    ff = sum(1 for g in genes if by[g]["fetch_status"] == "FETCH_FAILED")
    print(f"DONE  OK={ok} NO_ENSEMBL={ne} FETCH_FAILED={ff}  -> {CACHE_PATH}")


if __name__ == "__main__":
    main()
