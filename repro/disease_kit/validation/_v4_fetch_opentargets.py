#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v4_fetch_opentargets.py -- one-time VENDORING fetch for V4 (second independent source).

Pulls, per disease gene symbol, the APPROVED-drug mechanism actionType (ChEMBL's own
mechanism annotation, surfaced via the OpenTargets Platform GraphQL API) acting ON THAT GENE.
Writes a dated, pinned snapshot the V4 harness reads deterministically.

WHY OpenTargets as the transport.  The V3 pre-registration named "a live ChEMBL action_type
pull" as the second independent source.  ChEMBL's own REST API was NOT reliably reachable in
this session (repeated read-timeouts / HTTP 500).  OpenTargets surfaces ChEMBL's mechanism
actionType verbatim (drug.mechanismsOfAction.rows[].actionType), so V4 obtains the
pre-registered ChEMBL directionality via a reachable transport.  Honestly: ChEMBL is a COMMON
upstream to both DGIdb (V3) and OpenTargets (V4), so V4 is a cross-ASSEMBLER consistency check
(independent assembly pipeline, overlapping primary annotation), NOT a fully orthogonal source.

Resumable: re-running fills only missing genes.  Per gene fetch_status:
  OK           query succeeded; approved_drugs may be [] (genuine coverage gap: no approved
               signed small-molecule drug on this gene) or non-empty (scorable)
  NO_ENSEMBL   the symbol did not resolve to an OpenTargets target (coverage gap, reported)
  FETCH_FAILED network/HTTP error after retries -> EXCLUDED from numerator AND denominator AND
               coverage; reported as fetch-incomplete (never conflated with "no drug")
"""
import os, sys, json, time, datetime
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DI_PATH    = os.path.join(ROOT, "inputs", "disease_inputs.json")
CACHE_PATH = os.path.join(HERE, "v4_opentargets_snapshot.cache.json")
URL = "https://api.platform.opentargets.org/api/v4/graphql"

# FROZEN actionType -> direction reduction (ChEMBL mechanism actionType enum).
# Only unambiguous signs are scored; everything else is UNSIGNED and dropped (reported).
OT_INHIBITORY = {
    "INHIBITOR", "ANTAGONIST", "BLOCKER", "RNAI INHIBITOR", "ANTISENSE INHIBITOR",
    "NEGATIVE ALLOSTERIC MODULATOR", "NEGATIVE MODULATOR", "INVERSE AGONIST",
    "DEGRADER", "DISRUPTOR", "PROTEOLYSIS TARGETING CHIMERA",
}
OT_ACTIVATING = {
    "AGONIST", "ACTIVATOR", "PARTIAL AGONIST", "POSITIVE ALLOSTERIC MODULATOR",
    "POSITIVE MODULATOR", "OPENER",
}
APPROVED_STAGE = "APPROVAL"   # OpenTargets clinical-stage enum for marketed drugs


def reduce_sign(action_types):
    """A set of actionType strings on (drug,gene) -> a single sign or None (unsigned/ambiguous)."""
    signs = set()
    for a in action_types:
        u = (a or "").upper()
        if u in OT_INHIBITORY:
            signs.add("INHIBITORY")
        elif u in OT_ACTIVATING:
            signs.add("ACTIVATING")
    if len(signs) == 1:
        return next(iter(signs))
    return None   # none signed, or conflicting -> dropped


S = requests.Session()
S.headers.update({"User-Agent": "vp-disease-kit-validation/0.41 (ORCID 0009-0002-7535-8245)"})


def gql(q, v=None, tries=4, tmo=30):
    last = None
    for i in range(tries):
        try:
            r = S.post(URL, json={"query": q, "variables": v or {}}, timeout=tmo)
            if r.status_code == 200:
                j = r.json()
                if "errors" in j and j.get("data") is None:
                    last = "graphql_errors"
                else:
                    return j
            else:
                last = f"HTTP {r.status_code}"
        except Exception as e:
            last = type(e).__name__
        time.sleep(1.0 * (i + 1))
    raise RuntimeError(f"GraphQL failed after {tries}: {last}")


Q_SEARCH = ('query($s:String!){search(queryString:$s,entityNames:["target"])'
            '{hits{id object{... on Target{approvedSymbol}}}}}')
Q_DRUGS = ('query($e:String!){target(ensemblId:$e){approvedSymbol '
           'drugAndClinicalCandidates{count rows{maxClinicalStage '
           'drug{id name mechanismsOfAction{rows{actionType targets{id}}}}}}}}')
Q_META = ('query{meta{apiVersion{x y z} dataVersion{year month}}}')


def resolve_ensembl(sym):
    j = gql(Q_SEARCH, {"s": sym})
    hits = (j.get("data", {}).get("search", {}) or {}).get("hits", []) or []
    for h in hits:
        if (h.get("object") or {}).get("approvedSymbol") == sym:
            return h["id"]
    # exact-symbol miss: do NOT fall back to a fuzzy hit (would risk wrong gene)
    return None


def fetch_gene(sym):
    eid = resolve_ensembl(sym)
    if not eid:
        return dict(ensembl_id=None, fetch_status="NO_ENSEMBL", approved_drugs=[], n_act=0, n_inh=0)
    j = gql(Q_DRUGS, {"e": eid})
    rows = (((j.get("data", {}).get("target", {}) or {}).get("drugAndClinicalCandidates", {}) or {})
            .get("rows", []) or [])
    approved = []
    seen = set()
    for r in rows:
        if r.get("maxClinicalStage") != APPROVED_STAGE:
            continue
        d = r.get("drug") or {}
        did = d.get("id")
        # collect actionTypes annotated for THIS gene only
        acts = []
        for ma in ((d.get("mechanismsOfAction") or {}).get("rows", []) or []):
            tids = {t["id"] for t in (ma.get("targets") or [])}
            if eid in tids and ma.get("actionType"):
                acts.append(ma["actionType"])
        sign = reduce_sign(acts)
        key = (did, sign)
        if key in seen:
            continue
        seen.add(key)
        approved.append(dict(drug_id=did, drug=d.get("name"),
                             action_types=sorted(set(acts)), sign=sign))
    signed = [a for a in approved if a["sign"] in ("INHIBITORY", "ACTIVATING")]
    n_inh = sum(1 for a in signed if a["sign"] == "INHIBITORY")
    n_act = sum(1 for a in signed if a["sign"] == "ACTIVATING")
    return dict(ensembl_id=eid, fetch_status="OK", approved_drugs=approved,
                n_act=n_act, n_inh=n_inh)


def main():
    di = json.load(open(DI_PATH))
    genes = sorted({g["gene"] for rec in di.values() for g in rec["genes"]})

    if os.path.exists(CACHE_PATH):
        cache = json.load(open(CACHE_PATH))
    else:
        meta = {}
        try:
            mj = gql(Q_META)
            meta = mj.get("data", {}).get("meta", {})
        except Exception:
            meta = {}
        cache = dict(
            source="OpenTargets Platform GraphQL (surfacing ChEMBL mechanism actionType)",
            transport_note=("V3 pre-registered a ChEMBL action_type pull; ChEMBL's own REST API "
                            "was not reliably reachable this session, so ChEMBL's mechanism "
                            "actionType is surfaced via OpenTargets. ChEMBL is a common upstream "
                            "to both DGIdb (V3) and OpenTargets (V4): this is a cross-assembler "
                            "consistency check, not a fully orthogonal source."),
            opentargets_meta=meta,
            actionType_reduction=dict(inhibitory=sorted(OT_INHIBITORY),
                                      activating=sorted(OT_ACTIVATING),
                                      approved_stage=APPROVED_STAGE,
                                      note="single unambiguous sign per (drug,gene); else dropped"),
            interactions_by_symbol={})

    by = cache["interactions_by_symbol"]
    todo = [g for g in genes if g not in by or by[g].get("fetch_status") == "FETCH_FAILED"]
    print(f"genes total={len(genes)} already={len(genes)-len(todo)} todo={len(todo)}")
    t0 = time.time()
    for i, g in enumerate(todo):
        try:
            by[g] = fetch_gene(g)
            st = by[g]["fetch_status"]
            tag = (f"{by[g]['n_inh']}inh/{by[g]['n_act']}act"
                   if st == "OK" else st)
        except Exception as e:
            by[g] = dict(ensembl_id=None, fetch_status="FETCH_FAILED",
                         approved_drugs=[], n_act=0, n_inh=0, error=str(e)[:80])
            tag = "FETCH_FAILED"
        if (i + 1) % 10 == 0 or i == len(todo) - 1:
            # periodic checkpoint to disk (resumable)
            cache["fetched_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            json.dump(cache, open(CACHE_PATH, "w"), indent=1, sort_keys=True)
            print(f"  [{i+1}/{len(todo)}] {g}: {tag}  (chkpt, {time.time()-t0:.0f}s)")
    cache["fetched_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(cache, open(CACHE_PATH, "w"), indent=1, sort_keys=True)

    # summary
    from collections import Counter
    st = Counter(by[g]["fetch_status"] for g in genes)
    scorable = sum(1 for g in genes if by[g]["fetch_status"] == "OK" and (by[g]["n_inh"] + by[g]["n_act"]) > 0)
    print("status:", dict(st), "| scorable(>=1 signed approved drug):", scorable)


if __name__ == "__main__":
    main()
