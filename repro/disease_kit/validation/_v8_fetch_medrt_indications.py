#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v8_fetch_medrt_indications.py  --  ONE-SHOT vendoring fetcher for validation round V8.

  WHAT.  For every approved agent in the kit's repurposing corpus (engine/data/
  approved_repurposing_corpus.cache.json, 105 agents), pull its MED-RT *may_treat*
  INDICATION edges from the NLM RxClass API (class/byDrugName, relaSource=MEDRT,
  rela=may_treat), keep only items whose classType == 'DISEASE', and record each
  (agent -> {MeSH classId : className}) plus a flat classId->name MeSH lookup.

  WHY A NEW AXIS.  V1-V7 all tested the drug<->TARGET *direction* axis (does the
  geometry-derived sign match a pharmacology DB's mechanism annotation). The kit's
  "rediscovery" label, however, lives on a DIFFERENT axis -- the drug<->DISEASE
  *indication* axis -- which no prior round touched. MED-RT may_treat is an
  indication relation curated by NLM/VA from FDA Structured Product Labels: it is an
  INDEPENDENT, magnitude-free (categorical may_treat edge, no dose/efficacy/percent)
  ground truth for "does this agent have an approved/established indication for this
  disease". V5 used the SAME API for has_moa (mechanism); V8 uses may_treat
  (indication) -- a relation V5 never read.

  WHY may_treat AND classType==DISEASE.  may_treat is the indication relation (vs
  has_moa = mechanism, ci_with = contraindication, etc.). classType==DISEASE filters
  out non-disease RxClass buckets so every retained edge is (drug, MeSH disease).

  MAGNITUDE FIREWALL.  This snapshot stores only categorical strings: agent name,
  MeSH D-number, MeSH disease name. No dose, percent, efficacy number, p-value, or
  n-of-m patient count is ever fetched or written -- may_treat carries none.

  DRUG-NAME PARSING.  RxNav is queried on the agent's base name = text before the
  first '(' or '[', stripped (e.g. "sodium phenylbutyrate (4-PBA)" -> "sodium
  phenylbutyrate"). If the base name is a generic descriptor that yields NO may_treat
  edges AND the agent carries a parenthetical, a single fallback query is tried on the
  first parenthetical token (e.g. "L-type calcium channel blocker (verapamil) [Timothy
  syndrome]" -> base "L-type calcium channel blocker" resolves to nothing -> fallback
  "verapamil"). The base-name result wins whenever it is non-empty; the parenthetical
  is adopted only when the base yields nothing and the parenthetical yields DISEASE
  edges. The edge set is stored under the FULL corpus agent string so the downstream
  join key is exact. Agents that resolve under neither carry an empty may_treat set --
  logged, never guessed. The query string actually used is recorded per agent.

  PINNING.  The result is VENDORED + DATED + PINNED as v8_medrt_may_treat_snapshot.
  cache.json so the V8 metrics are 2x byte-identical and the build never touches the
  network. A fresh live re-pull is a NETWORK AUDIT sidecar (v8_external_refetch_audit
  .json), off the byte-frozen determinism manifest.

  Run:  python3 validation/_v8_fetch_medrt_indications.py
"""
import os, sys, json, time, re, datetime, urllib.request, urllib.parse

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.normpath(os.path.join(HERE, ".."))
CORPUS   = os.path.join(ROOT, "engine", "data", "approved_repurposing_corpus.cache.json")
OUT      = os.path.join(HERE, "v8_medrt_may_treat_snapshot.cache.json")

RXCLASS  = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json"
VERSION  = "https://rxnav.nlm.nih.gov/REST/version.json"


def base_name(agent):
    """Base drug name queried against RxNav = text before the first '(' or '['."""
    return re.split(r"[\(\[]", agent)[0].strip()


def paren_token(agent):
    """First parenthetical token, e.g. 'L-type ... (verapamil) [..]' -> 'verapamil'.
    Returns None if there is no parenthetical or it is empty."""
    m = re.search(r"\(([^)]*)\)", agent)
    if not m:
        return None
    tok = m.group(1).strip()
    # keep only the leading drug-like token (drop sub-notes after ';' or ',')
    tok = re.split(r"[;,]", tok)[0].strip()
    return tok or None


def http_json(url, tries=4, timeout=30):
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode())
        except Exception as e:
            last = type(e).__name__
            time.sleep(0.8 * (t + 1))
    return {"_error": last}


def corpus_agents():
    c = json.load(open(CORPUS))
    return [a["agent"] for a in c["agents"] if a.get("agent")]


def fetch_disease_edges(query):
    """Query RxClass may_treat for one drug name; return (status, {classId:className})."""
    url = (f"{RXCLASS}?drugName={urllib.parse.quote(query)}"
           f"&relaSource=MEDRT&relas=may_treat")
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


def main():
    agents = corpus_agents()
    ver = http_json(VERSION)
    rxnorm_version = ver.get("version") if isinstance(ver, dict) else None

    may_treat_by_agent = {}     # full agent string -> {classId: className}
    mesh = {}                   # classId -> className (flat lookup)
    resolved = with_edge = 0
    for i, agent in enumerate(agents):
        q = base_name(agent)
        status, edges = fetch_disease_edges(q)
        query_used = q
        # in-paren fallback: only when the base name yielded nothing
        if status == "OK" and not edges:
            pt = paren_token(agent)
            if pt and pt.lower() != q.lower():
                s2, e2 = fetch_disease_edges(pt)
                if s2 == "OK" and e2:
                    status, edges, query_used = s2, e2, f"{q} -> (fallback) {pt}"
        if status.startswith("OK"):
            resolved += 1
            if edges:
                with_edge += 1
        for cid, cname in edges.items():
            mesh[cid] = cname
        may_treat_by_agent[agent] = dict(query=query_used, fetch_status=status, may_treat=edges)
        if (i + 1) % 25 == 0:
            print(f"  ...{i+1}/{len(agents)}", file=sys.stderr)
        time.sleep(0.12)

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
        drug_universe_note="every agent in engine/data/approved_repurposing_corpus.cache.json; "
                           "queried on base name (text before first '(' or '['); edge stored under "
                           "the full corpus agent string for an exact downstream join key",
        magnitude_free="categorical only: agent name + MeSH D-number + MeSH disease name. No dose, "
                       "percent, efficacy, p-value, or n-of-m patient count is fetched or written.",
        n_agents=len(agents), n_resolved=resolved, n_with_may_treat=with_edge, n_disease_edges=n_edges,
        mesh=mesh,
        may_treat_by_agent=may_treat_by_agent)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=1, ensure_ascii=False, sort_keys=True)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  "
          f"(agents {len(agents)}, resolved {resolved}, with-may_treat {with_edge}, edges {n_edges})")


if __name__ == "__main__":
    main()
