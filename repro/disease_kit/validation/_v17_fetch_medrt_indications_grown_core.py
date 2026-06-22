#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v17_fetch_medrt_indications_grown_core.py  --  ADDITIVE vendoring fetcher for round V17.

  WHAT.  V8 vendored MED-RT may_treat INDICATION edges for the 105 agents present in the
  approved_repurposing_corpus at 128-core time. Track-A growth (e7a/e7b/e7c) took the corpus
  to 130 agents (128 distinct agent strings in the prior-art specific_pairs). This fetcher
  pulls may_treat edges for ONLY the agents that are NEW vs the frozen V8 snapshot, then
  merges them ON TOP of the V8 snapshot's edges (the 105 V8 agents are copied verbatim,
  byte-for-byte; the V8 snapshot file is left untouched). The result is the grown-core
  may_treat snapshot used by V17 -- exactly the additive-snapshot pattern V14 used for the
  OpenTargets chaperone source and V15 for ClinicalTrials.gov.

  WHY ADDITIVE, NOT A FRESH PULL.  The inheritance discipline forbids perturbing a frozen
  substrate. V8's snapshot (snapshot_sha256 in V8_PREREGISTRATION.json) must stay byte-
  identical so the 128-core V8 audit remains reproducible. So V17 inherits V8's 105 agent
  edges verbatim and only ADDS the new agents' edges -- never re-pulls or mutates the old.

  API CONTRACT (identical to _v8_fetch_medrt_indications.py).  NLM RxClass class/byDrugName,
  relaSource=MEDRT, rela=may_treat, keep classType=='DISEASE'. Base-name query = text before
  first '(' or '['; single in-paren fallback only when the base yields zero edges. Edge set
  stored under the FULL corpus agent string (exact downstream join key). Agents resolving
  under neither carry an empty may_treat set -- logged, never guessed.

  MAGNITUDE FIREWALL.  Categorical only: agent name, MeSH D-number, MeSH disease name. No
  dose / percent / efficacy / p-value / n-of-m is fetched or written (may_treat carries none).

  Run:  python3 validation/_v17_fetch_medrt_indications_grown_core.py
"""
import os, sys, json, time, re, datetime, hashlib, urllib.request, urllib.parse

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
CORPUS = os.path.join(ROOT, "engine", "data", "approved_repurposing_corpus.cache.json")
PA     = os.path.join(ROOT, "engine", "data", "prior_art_status.cache.json")
V8SNAP = os.path.join(HERE, "v8_medrt_may_treat_snapshot.cache.json")
OUT    = os.path.join(HERE, "v17_medrt_may_treat_snapshot.cache.json")

RXCLASS = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json"
VERSION = "https://rxnav.nlm.nih.gov/REST/version.json"


def base_name(agent):  return re.split(r"[\(\[]", agent)[0].strip()
def paren_token(agent):
    m = re.search(r"\(([^)]*)\)", agent)
    if not m: return None
    tok = re.split(r"[;,]", m.group(1).strip())[0].strip()
    return tok or None
def sha_file(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()


def http_json(url, tries=4, timeout=30):
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = type(e).__name__; time.sleep(0.8 * (t + 1))
    return {"_error": last}


def fetch_disease_edges(query):
    url = f"{RXCLASS}?drugName={urllib.parse.quote(query)}&relaSource=MEDRT&relas=may_treat"
    j = http_json(url)
    if "_error" in j:
        return "FETCH_FAILED:" + str(j["_error"]), {}
    edges = {}
    for item in j.get("rxclassDrugInfoList", {}).get("rxclassDrugInfo", []):
        if item.get("rela") == "may_treat":
            mc = item.get("rxclassMinConceptItem", {})
            if mc.get("classType") == "DISEASE" and mc.get("classId"):
                edges[mc["classId"]] = mc.get("className")
    return "OK", edges


def fetch_one(agent):
    q = base_name(agent)
    status, edges = fetch_disease_edges(q)
    query_used = q
    if status == "OK" and not edges:
        pt = paren_token(agent)
        if pt and pt.lower() != q.lower():
            s2, e2 = fetch_disease_edges(pt)
            if s2 == "OK" and e2:
                status, edges, query_used = s2, e2, f"{q} -> (fallback) {pt}"
    return dict(query=query_used, fetch_status=status, may_treat=edges)


def main():
    v8 = json.load(open(V8SNAP))
    v8_agents = v8["may_treat_by_agent"]                 # 105 frozen agents (copied verbatim)
    v8_sha = sha_file(V8SNAP)

    # the grown-core agent universe = every agent string appearing in the prior-art pairs
    pa = json.load(open(PA))
    corpus_agents = sorted({e["agent"] for e in pa["specific_pairs"]})
    new_agents = [a for a in corpus_agents if a not in v8_agents]
    print(f"V8 frozen agents: {len(v8_agents)}  |  grown corpus agents: {len(corpus_agents)}  |  NEW to fetch: {len(new_agents)}", file=sys.stderr)

    ver = http_json(VERSION)
    rxnorm_version = ver.get("version") if isinstance(ver, dict) else None

    # start from V8's edges VERBATIM, then ADD the new agents
    may_treat_by_agent = dict(v8_agents)                 # inherit byte-identical content
    added = {}
    for i, agent in enumerate(new_agents):
        rec = fetch_one(agent)
        may_treat_by_agent[agent] = rec
        added[agent] = rec
        if (i + 1) % 10 == 0:
            print(f"  ...{i+1}/{len(new_agents)}", file=sys.stderr)
        time.sleep(0.12)

    # rebuild the flat mesh lookup over the UNION
    mesh = {}
    for v in may_treat_by_agent.values():
        for cid, cname in v["may_treat"].items():
            mesh[cid] = cname

    resolved = sum(1 for v in may_treat_by_agent.values() if str(v["fetch_status"]).startswith("OK"))
    with_edge = sum(1 for v in may_treat_by_agent.values() if v["may_treat"])
    n_edges = sum(len(v["may_treat"]) for v in may_treat_by_agent.values())

    snapshot = dict(
        source="MED-RT (NLM/VA Medication Reference Terminology, formerly NDF-RT) may_treat "
               "INDICATION edges, via the NLM RxClass API (class/byDrugName, relaSource=MEDRT, "
               "rela=may_treat), filtered to classType==DISEASE.",
        api_base="https://rxnav.nlm.nih.gov/REST/rxclass",
        rela_source="MEDRT", rela="may_treat", class_type="DISEASE",
        axis="drug<->DISEASE indication (NOT the drug<->target direction axis of V1-V7)",
        rxnav_rxnorm_version=rxnorm_version,
        fetched_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        lineage=dict(
            extends="v8_medrt_may_treat_snapshot.cache.json",
            v8_snapshot_sha256=v8_sha,
            policy="ADDITIVE: the 105 V8 agents' edges are copied byte-identical from the frozen V8 "
                   "snapshot; only the agents NEW to the grown corpus were freshly pulled. The V8 "
                   "snapshot file itself is left untouched.",
            n_v8_agents=len(v8_agents), n_new_agents=len(new_agents)),
        drug_universe_note="every agent string in engine/data/prior_art_status.cache.json::specific_pairs "
                           "(the grown Track-A corpus); queried on base name (text before first '(' or '['); "
                           "edge stored under the full corpus agent string for an exact downstream join key",
        magnitude_free="categorical only: agent name + MeSH D-number + MeSH disease name. No dose, percent, "
                       "efficacy, p-value, or n-of-m patient count is fetched or written.",
        n_agents=len(may_treat_by_agent), n_resolved=resolved, n_with_may_treat=with_edge, n_disease_edges=n_edges,
        newly_added_agents=sorted(added.keys()),
        mesh=mesh,
        may_treat_by_agent=may_treat_by_agent)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=1, ensure_ascii=False, sort_keys=True)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  (agents {len(may_treat_by_agent)} = {len(v8_agents)} V8 + "
          f"{len(new_agents)} new; resolved {resolved}; with-may_treat {with_edge}; edges {n_edges}; "
          f"MeSH {len(mesh)})")

    # quick echo of which new agents actually returned DISEASE edges (the rest are coverage gaps)
    hit = {a: list(r["may_treat"].items()) for a, r in added.items() if r["may_treat"]}
    print(f"\nnew agents WITH may_treat edges: {len(hit)}/{len(new_agents)}")
    for a, e in sorted(hit.items()):
        print(f"  {a}\n      -> {e}")


if __name__ == "__main__":
    main()
