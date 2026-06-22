#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v7_fetch_drugcentral.py  --  ONE-TIME vendoring fetcher for VALIDATION round V7 (membership-widening).

  WHAT THIS DOES.  Pulls the DrugCentral drug<->target interaction table (the public bulk TSV) and
  vendors a MAGNITUDE-FREE, ON-SCOPE snapshot for the kit's disease genes. DrugCentral is a PRIMARY,
  expert-curated drug<->target compendium of approved/marketed actives, maintained independently of the
  three direction sources already used (DGIdb V3, OpenTargets/ChEMBL V4, MED-RT V5) and of GtoPdb (V6).
  Its value to V7 is twofold:
    (1) DENOMINATOR WIDENING -- it resolves disease genes that NONE of the prior sources resolved
        (e.g. coagulation factors, lysosomal enzymes), at GENE granularity, with its OWN curated
        mechanism-of-action (MOA) edges -- the exact "drug-target primary-literature curation" the V6
        round pre-registered as the next membership source, "should it become reachable."
    (2) A FIFTH independent direction vote that, on the four standing four-source disagreements, lands
        with the molecular-target consensus -- feeding X_CROSS5 and the X_VOCAB taxonomy.

  THE BOUND, STATED HONESTLY.
    - DrugCentral INTEGRATES ChEMBL / DrugBank / IUPHAR among its upstream sources, so it is NOT fully
      orthogonal to the ChEMBL lineage either (same class of caveat as GtoPdb being a DGIdb upstream).
      What it adds is its OWN curated MOA edge assignments (MOA=1, with MOA_SOURCE provenance) and
      genes/edges the prior sources did not carry. X_MEMB_DC audits that overlap so the claim is
      inspectable, not asserted.
    - The newest interaction table DrugCentral hosts under this filename is the 2021-09-01 release; the
      snapshot is dated accordingly and pinned by hash. This is a vendored snapshot; a fresh live
      re-pull is an off-manifest AUDIT sidecar (the harness writes v7_external_refetch_audit.json).

  MAGNITUDE FIREWALL (the kit's discipline).  DrugCentral's interaction table carries AFFINITY columns
  (ACT_VALUE, ACT_UNIT, ACT_TYPE assay, ACT_COMMENT prose, RELATION operator). NONE of these is read or
  vendored. ONLY the categorical, direction-relevant fields enter the snapshot:
      GENE, DRUG_NAME, ACTION_TYPE (category), MOA (0/1 curated flag), MOA_SOURCE, ACT_SOURCE,
      TARGET_CLASS, TDL, ACCESSION, SWISSPROT, ORGANISM.
  So the vendored snapshot is magnitude-free BY CONSTRUCTION; the firewall passes.

  Run once:  python3 validation/_v7_fetch_drugcentral.py
  Output:    validation/v7_drugcentral_snapshot.cache.json   (vendored; hash pinned in V7 prereg)
"""
import os, sys, json, gzip, io, csv, hashlib, datetime, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DI_PATH  = os.path.join(ROOT, "inputs", "disease_inputs.json")
OUT_PATH = os.path.join(HERE, "v7_drugcentral_snapshot.cache.json")

# DrugCentral public bulk interaction table (newest hosted under this filename).
DC_URLS = [
    "https://unmtid-dbs.net/download/DrugCentral/2021_09_01/drug.target.interaction.tsv.gz",
    "https://unmtid-dbs.net/download/DrugCentral/2020_09_01/drug.target.interaction.tsv.gz",
]
DC_VERSION = "2021-09-01"   # the dated release this filename serves

# ---- columns we ALLOW into the snapshot (categorical / direction-relevant only) ----
KEEP_CATEGORICAL = ("DRUG_NAME", "GENE", "ACTION_TYPE", "MOA", "MOA_SOURCE",
                    "ACT_SOURCE", "TARGET_CLASS", "TDL", "ACCESSION", "SWISSPROT", "ORGANISM")
# ---- columns we REFUSE to read (affinity / magnitude) ----
FORBIDDEN_MAGNITUDE = ("ACT_VALUE", "ACT_UNIT", "ACT_TYPE", "ACT_COMMENT", "RELATION",
                       "ACT_SOURCE_URL", "MOA_SOURCE_URL", "STRUCT_ID")

# Direction reduction -- IDENTICAL copy re-derived in the harness (never trust a cached scalar).
INH_TOKENS = (" ANTAGONIST", " INHIBITOR", " BLOCKER", " NEGATIVE")
ACT_TOKENS = (" AGONIST", " ACTIVATOR", " OPENER", " POSITIVE", " RELEASING")

def reduce_dc(action_type):
    """DrugCentral ACTION_TYPE -> 'INHIBITORY' | 'ACTIVATING' | None. Categorical only; no affinity."""
    t = " " + (action_type or "").upper().strip() + " "
    if not t.strip():                                              return None
    if "INVERSE AGONIST" in t:                                     return "INHIBITORY"
    if "PARTIAL AGONIST" in t or "FULL AGONIST" in t:              return "ACTIVATING"
    if ("ANTIBODY BINDING" in t or "BINDING AGENT" in t
            or "SUBSTRATE" in t or "CHAPERONE" in t):              return None
    if "MODULATOR" in t:
        if "NEGATIVE" in t:                                        return "INHIBITORY"
        if "POSITIVE" in t:                                        return "ACTIVATING"
        return None
    inh = any(k in t for k in INH_TOKENS)
    act = any(k in t for k in ACT_TOKENS)
    if inh and not act:                                            return "INHIBITORY"
    if act and not inh:                                            return "ACTIVATING"
    return None


def http_gz_text(url, timeout=120):
    req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return gzip.decompress(r.read()).decode("utf-8", "replace")


def main():
    di = json.load(open(DI_PATH))
    disease_genes = sorted({g["gene"] for s, rec in di.items() for g in rec["genes"]})
    disease_set = set(disease_genes)

    text = None; used = None
    for u in DC_URLS:
        try:
            text = http_gz_text(u); used = u; break
        except Exception as e:
            print(f"  (fetch failed {u}: {type(e).__name__})")
    if text is None:
        print("ERROR: could not reach DrugCentral; snapshot not written."); return 1

    rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    # safety: confirm none of the forbidden magnitude columns leak into the snapshot
    header = set(rows[0].keys()) if rows else set()
    assert FORBIDDEN_MAGNITUDE  # documented
    by_symbol = {}
    n_kept = 0; n_signed = 0; n_moa = 0
    drugs_seen = set()
    for r in rows:
        if (r.get("ORGANISM") or "").strip() != "Homo sapiens":
            continue
        genes = [g.strip() for g in (r.get("GENE") or "").split("|") if g.strip()]
        hit = [g for g in genes if g in disease_set]
        if not hit:
            continue
        atype = (r.get("ACTION_TYPE") or "").strip()
        direction = reduce_dc(atype)
        drug = (r.get("DRUG_NAME") or "").strip()
        rec = dict(
            drug=drug,
            action_type=atype,
            direction=direction,                       # convenience; harness RE-derives, never trusts
            moa=(r.get("MOA") or "").strip(),           # '1' = DrugCentral-curated mechanism edge
            moa_source=(r.get("MOA_SOURCE") or "").strip(),
            act_source=(r.get("ACT_SOURCE") or "").strip(),
            target_class=(r.get("TARGET_CLASS") or "").strip(),
            tdl=(r.get("TDL") or "").strip(),
            accession=(r.get("ACCESSION") or "").strip(),
            swissprot=(r.get("SWISSPROT") or "").strip(),
        )
        # NOTE: ACT_VALUE / ACT_UNIT / ACT_TYPE / ACT_COMMENT / RELATION are NEVER copied. Firewall.
        for g in hit:
            by_symbol.setdefault(g, []).append(rec)
        n_kept += 1
        if direction in ("INHIBITORY", "ACTIVATING"):
            n_signed += 1
        if rec["moa"] == "1":
            n_moa += 1
        if drug:
            drugs_seen.add(drug.upper())

    # stable ordering for byte-identical snapshot
    for g in by_symbol:
        by_symbol[g] = sorted(by_symbol[g], key=lambda x: (x["drug"], x["action_type"], x["moa"]))

    snap = dict(
        source="DrugCentral drug<->target interaction table (bulk TSV), Homo sapiens, kit disease genes only.",
        download_url=used,
        drugcentral_version=DC_VERSION,
        fetched_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        filters=dict(organism="Homo sapiens", scope="kit disease genes only",
                     n_disease_genes_in_scope=len(disease_genes)),
        magnitude_firewall=dict(
            forbidden_columns_never_read=list(FORBIDDEN_MAGNITUDE),
            kept_categorical_columns=list(KEEP_CATEGORICAL),
            note="affinity/magnitude columns (ACT_VALUE/ACT_UNIT/ACT_TYPE assay/ACT_COMMENT/RELATION) "
                 "are NEVER read or vendored; only categorical direction fields enter the snapshot."),
        membership_note="(drug<->gene) edges are DrugCentral's OWN curation; MOA=1 rows are its expert "
                        "mechanism-of-action edges (MOA_SOURCE provenance). DrugCentral integrates "
                        "ChEMBL/DrugBank/IUPHAR upstream, so it is NOT fully orthogonal to the ChEMBL "
                        "lineage; what it adds is its own MOA edge assignments plus genes/edges the "
                        "prior sources did not carry. X_MEMB_DC audits the overlap.",
        direction_reduction=dict(inhibitory_tokens=[t.strip() for t in INH_TOKENS],
                                 activating_tokens=[t.strip() for t in ACT_TOKENS],
                                 overrides=["INVERSE AGONIST->INHIBITORY",
                                            "PARTIAL/FULL AGONIST->ACTIVATING",
                                            "ANTIBODY BINDING / BINDING AGENT / SUBSTRATE / CHAPERONE->None",
                                            "NEGATIVE (ALLOSTERIC) MODULATOR->INHIBITORY",
                                            "POSITIVE (ALLOSTERIC) MODULATOR->ACTIVATING",
                                            "bare MODULATOR->None"]),
        n_disease_genes=len(by_symbol),
        n_interaction_rows_kept=n_kept,
        n_rows_signed=n_signed,
        n_rows_moa_curated=n_moa,
        n_drugs_distinct=len(drugs_seen),
        interactions_by_symbol=by_symbol)

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1, ensure_ascii=False, sort_keys=True)
    h = hashlib.sha256(open(OUT_PATH, "rb").read()).hexdigest()
    print(f"vendored DrugCentral snapshot: {OUT_PATH}")
    print(f"  drugcentral_version : {DC_VERSION}  (from {used})")
    print(f"  disease genes w/ DC : {len(by_symbol)}/{len(disease_genes)}")
    print(f"  rows kept           : {n_kept}  (signed {n_signed}, MOA-curated {n_moa}, distinct drugs {len(drugs_seen)})")
    print(f"  snapshot_sha256     : {h}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
