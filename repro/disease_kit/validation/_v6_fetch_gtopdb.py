#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v6_fetch_gtopdb.py  --  ONE-SHOT vendoring fetcher for validation round V6.

  WHY GtoPdb (the membership-orthogonal source V5 gated on).  V3 (DGIdb), V4 (OpenTargets/ChEMBL)
  and V5 (MED-RT) all scored a (drug<->gene) MEMBERSHIP that is ChEMBL-derived; V5 only orthogonalised
  the DIRECTION annotation, leaving the membership bound open (its fully-orthogonal X1B corner was a
  single gene, PCSK9). The IUPHAR/BPS Guide to PHARMACOLOGY (GtoPdb) is a PRIMARY, expert-curated
  pharmacology database whose drug<->target interactions AND their direction (agonist/antagonist/
  inhibitor/activator) are curated independently of ChEMBL. So GtoPdb supplies BOTH membership AND
  direction with no ChEMBL lineage -- the source that widens the membership-orthogonal corner from
  1 gene to the whole GtoPdb-resolvable disease-gene set.

  THE BOUND, STATED HONESTLY.  GtoPdb is ONE of DGIdb's ~45 upstream sources, so V6 is NOT orthogonal
  to V3's *aggregate*. What it IS: a primary source whose membership and direction are not derived
  from ChEMBL -- so it is orthogonal to the ChEMBL MEMBERSHIP lineage all scored arms (V3/V4/V5) used.
  GtoPdb's approved-drug coverage is also narrower than ChEMBL's (curated quantitative pharmacology,
  skewed to receptors / channels / enzymes), so the denominator is SMALLER -- reported honestly.

  MAGNITUDE FIREWALL (critical for this source).  GtoPdb interactions carry quantitative AFFINITY
  columns (Affinity Units / High / Median / Low / Original Affinity nM ...). Those columns are NEVER
  read and NEVER vendored: this fetcher keeps ONLY the qualitative {Target Gene Symbol, Ligand ID,
  Ligand, Type, Action, Approved, Endogenous, Primary Target, Target Species} projection. The vendored
  snapshot is magnitude-free BY CONSTRUCTION, so the kit's firewall passes trivially over it.

  The result is VENDORED as a dated cache (v6_gtopdb_snapshot.cache.json) so the V6 metrics are 2x
  byte-identical. A fresh live re-pull is a network AUDIT sidecar, off the byte-frozen manifest.

  Run:  python3 validation/_v6_fetch_gtopdb.py
"""
import os, sys, json, csv, io, datetime, urllib.request

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
DI     = os.path.join(ROOT, "inputs", "disease_inputs.json")
OUT    = os.path.join(HERE, "v6_gtopdb_snapshot.cache.json")

LIG_URL = "https://www.guidetopharmacology.org/DATA/ligands.csv"
INT_URL = "https://www.guidetopharmacology.org/DATA/interactions.csv"

csv.field_size_limit(1 << 24)

# ---- direction reduction (frozen; identical copy lives in the harness + the prereg) ----
INH_TOKENS = (" ANTAGONIST", " INHIBITOR", " INHIBITION", " BLOCKER", " BLOCKADE", " NEGATIVE")
ACT_TOKENS = (" AGONIST", " ACTIVATOR", " ACTIVATION", " POTENTIATION", " OPENER", " POSITIVE",
              " STIMULANT", " STIMULATION")

def reduce_gtopdb(itype, action):
    """GtoPdb interaction Type + Action -> 'INHIBITORY' | 'ACTIVATING' | None (dropped, never guessed).
       Ordered overrides first (specific), then a leading-space token scan that, like V5, keeps the
       'AGONIST'/'ANTAGONIST' tokens disjoint. Magnitude-free: only the categorical fields are read."""
    text = " " + (itype or "").upper().strip() + " | " + (action or "").upper().strip() + " "
    if "INVERSE AGONIST" in text:        return "INHIBITORY"     # inverse agonist = negative direction
    if "PARTIAL AGONIST" in text:        return "ACTIVATING"     # net-activating direction
    if "FULL AGONIST" in text:           return "ACTIVATING"
    if "MODULATOR" in text or "ALLOSTERIC" in text:
        if "NEGATIVE" in text:           return "INHIBITORY"
        if "POSITIVE" in text:           return "ACTIVATING"
        # bare allosteric / modulator: fall through (Action may still carry a sign, e.g. Potentiation)
    inh = any(k in text for k in INH_TOKENS)
    act = any(k in text for k in ACT_TOKENS)
    if inh and not act:                  return "INHIBITORY"
    if act and not inh:                  return "ACTIVATING"
    return None                                                  # binding / neutral / ambiguous -> drop


def http_text(url, tries=4, timeout=90):
    last = None
    for t in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "vp-disease-kit-validation/0.41"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:
            last = type(e).__name__
            import time; time.sleep(1.0 * (t + 1))
    raise RuntimeError(f"fetch failed for {url}: {last}")


def parse_csv_with_version(text):
    """GtoPdb CSVs start with a '# GtoPdb Version: ...' comment line, then a normal header row."""
    lines = text.splitlines()
    version = None
    if lines and lines[0].lstrip('"').startswith("# GtoPdb Version"):
        version = lines[0].strip().strip('"').replace("# GtoPdb Version:", "").strip()
        body = "\n".join(lines[1:])
    else:
        body = text
    rows = list(csv.DictReader(io.StringIO(body)))
    return version, rows


def main():
    di = json.load(open(DI))
    disease_genes = sorted({g["gene"] for s in di for g in di[s]["genes"]})
    dg_set = set(disease_genes)

    # ---- 1) approved-ligand set (ligands.csv is the authoritative approval flag) ----
    lig_version, lig_rows = parse_csv_with_version(http_text(LIG_URL))
    approved_ids, chembl_of = set(), {}
    for r in lig_rows:
        lid = (r.get("Ligand ID") or "").strip()
        if (r.get("Approved") or "").strip().lower() == "yes" and lid:
            approved_ids.add(lid)
            ch = (r.get("ChEMBL ID") or "").strip()
            if ch:
                chembl_of[lid] = ch
    print(f"  ligands.csv {lig_version}: approved ligands = {len(approved_ids)}", file=sys.stderr)

    # ---- 2) interactions.csv, filtered to Human + disease-gene + approved ligand ----
    int_version, int_rows = parse_csv_with_version(http_text(INT_URL))
    by_gene = {}
    n_kept = 0
    for r in int_rows:
        gene = (r.get("Target Gene Symbol") or "").strip()
        if gene not in dg_set:
            continue
        if (r.get("Target Species") or "").strip().lower() != "human":
            continue
        lid = (r.get("Ligand ID") or "").strip()
        approved_flag = (r.get("Approved") or "").strip().lower() == "yes"
        if not (approved_flag or lid in approved_ids):
            continue
        itype  = (r.get("Type") or "").strip()
        action = (r.get("Action") or "").strip()
        direction = reduce_gtopdb(itype, action)
        rec = dict(
            ligand_id=lid,
            ligand=(r.get("Ligand") or "").strip().upper(),
            type=itype,
            action=action,                       # categorical only -- NO affinity column is read
            endogenous=(r.get("Endogenous") or "").strip().lower() == "true"
                       or (r.get("Endogenous") or "").strip().lower() == "yes",
            primary_target=(r.get("Primary Target") or "").strip().lower() == "true"
                       or (r.get("Primary Target") or "").strip().lower() == "yes",
            direction=direction,
            chembl_id=chembl_of.get(lid, ""),     # disclosed for transparency, NOT used for membership
        )
        by_gene.setdefault(gene, []).append(rec)
        n_kept += 1

    # de-duplicate identical (gene, ligand, type, action) rows; keep deterministic order
    for g in by_gene:
        seen, ded = set(), []
        for rec in sorted(by_gene[g], key=lambda x: (x["ligand"], x["type"], x["action"], x["ligand_id"])):
            key = (rec["ligand"], rec["type"], rec["action"])
            if key in seen:
                continue
            seen.add(key); ded.append(rec)
        by_gene[g] = ded

    genes_with_signed = sum(
        1 for g, rows in by_gene.items()
        if any(x["direction"] in ("INHIBITORY", "ACTIVATING") for x in rows))

    snapshot = dict(
        source="IUPHAR/BPS Guide to PHARMACOLOGY (GtoPdb) -- approved-drug interactions, bulk CSV "
               "(ligands.csv + interactions.csv). Primary expert curation; membership AND direction "
               "are independent of ChEMBL.",
        api_base="https://www.guidetopharmacology.org/DATA",
        gtopdb_version=int_version, ligands_version=lig_version,
        fetched_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        membership_note="A (drug<->gene) edge exists iff GtoPdb curates an interaction between an "
                        "APPROVED ligand and the disease gene's human target. Membership is GtoPdb's, "
                        "NOT inherited from V4/ChEMBL -- this is the orthogonal-membership arm.",
        magnitude_firewall="affinity columns (Affinity Units/High/Median/Low, Original Affinity nM, "
                           "concentration Range) are NEVER read or vendored; only the categorical "
                           "Type/Action fields are kept. Snapshot is magnitude-free by construction.",
        filters=dict(target_species="Human", approved="ligands.csv Approved==yes (or interaction "
                     "Approved==yes)", disease_genes=len(disease_genes)),
        direction_reduction=dict(
            order="1) INVERSE AGONIST->INHIBITORY  2) PARTIAL/FULL AGONIST->ACTIVATING  "
                  "3) (ALLOSTERIC) MODULATOR: NEGATIVE->INHIBITORY / POSITIVE->ACTIVATING / "
                  "bare->fall-through  4) token scan over Type|Action",
            inhibitory_tokens=[t.strip() for t in INH_TOKENS],
            activating_tokens=[t.strip() for t in ACT_TOKENS],
            note="single unambiguous sign per (drug,gene) from Type+Action; binding/neutral/ambiguous "
                 "-> None (dropped, never scored). Read from class words only, no potency token."),
        n_disease_genes=len(disease_genes),
        n_genes_with_any_interaction=len(by_gene),
        n_genes_with_signed_interaction=genes_with_signed,
        n_interaction_rows_kept=n_kept,
        n_approved_ligands_total=len(approved_ids),
        interactions_by_symbol=by_gene)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=1, ensure_ascii=False, sort_keys=True)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  (GtoPdb {int_version}; genes-with-interaction "
          f"{len(by_gene)}/{len(disease_genes)}; signed {genes_with_signed}; rows {n_kept})")


if __name__ == "__main__":
    main()
