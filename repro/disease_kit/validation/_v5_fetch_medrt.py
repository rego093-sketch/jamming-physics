#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
_v5_fetch_medrt.py  --  ONE-SHOT vendoring fetcher for validation round V5.

  Pulls each approved drug (the SAME drug universe V4 resolved, read from the vendored
  OpenTargets snapshot) against the NLM RxClass API, relaSource=MEDRT, rela=has_moa, and
  reduces each drug's MED-RT Mechanism-of-Action class name(s) to a single direction sign in
  {INHIBITORY, ACTIVATING} (or None = no clean direction -> dropped, never guessed).

  WHY MED-RT.  MED-RT (NLM/VA Medication Reference Terminology, formerly NDF-RT) curates
  Mechanism-of-Action from FDA Structured Product Labels and pharmacology references. It is
  NOT ChEMBL and is NOT one of DGIdb's source databases -> a DIRECTION annotation with no
  ChEMBL/DGIdb lineage. (The bound V5 states openly: the drug<->gene MEMBERSHIP is inherited
  from V4 and is ChEMBL-derived; V5 orthogonalises the DIRECTION annotation, not the membership.)

  The result is VENDORED as a dated cache (v5_medrt_snapshot.cache.json) so the V5 metrics are
  2x byte-identical. A fresh live re-pull is a network AUDIT sidecar, off the byte-frozen manifest.

  Run:  python3 validation/_v5_fetch_medrt.py
"""
import os, sys, json, time, datetime, urllib.request, urllib.parse

HERE   = os.path.dirname(os.path.abspath(__file__))
ROOT   = os.path.normpath(os.path.join(HERE, ".."))
OT_CACHE = os.path.join(HERE, "v4_opentargets_snapshot.cache.json")
OUT      = os.path.join(HERE, "v5_medrt_snapshot.cache.json")

RXCLASS = "https://rxnav.nlm.nih.gov/REST/rxclass/class/byDrugName.json"
VERSION = "https://rxnav.nlm.nih.gov/REST/version.json"

# ---- direction reduction (frozen; identical copy lives in the harness + the prereg) ----
def reduce_moa(class_names):
    """Ordered reduction of MED-RT MoA class names -> 'INHIBITORY' | 'ACTIVATING' | None."""
    signs = set()
    for raw in class_names:
        n = " " + raw.upper() + " "
        if "INVERSE AGONIST" in n:
            signs.add("INHIBITORY"); continue
        if "MODULATOR" in n:
            if "NEGATIVE" in n: signs.add("INHIBITORY"); continue
            if "POSITIVE" in n: signs.add("ACTIVATING"); continue
            continue  # bare 'modulator' = ambiguous, contributes nothing
        inh = any(k in n for k in (" INHIBITOR", " ANTAGONIST", " BLOCKER", " DEGRADER", " BLOCKING"))
        act = any(k in n for k in (" ACTIVATOR", " AGONIST", " POTENTIATOR", " OPENER", " STIMULANT", " RELEASING"))
        if inh and not act: signs.add("INHIBITORY")
        elif act and not inh: signs.add("ACTIVATING")
        # else: class names a target but no directional token -> contributes nothing
    return next(iter(signs)) if len(signs) == 1 else None


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


def drug_universe():
    """The SAME approved-drug universe V4 resolved (read from the vendored OT snapshot)."""
    ot = json.load(open(OT_CACHE))
    drugs = set()
    for g, rec in ot["interactions_by_symbol"].items():
        if rec.get("fetch_status") != "OK":
            continue
        for d in rec.get("approved_drugs", []):
            if d.get("drug"):
                drugs.add(d["drug"])
    return sorted(drugs)


def main():
    drugs = drug_universe()
    ver = http_json(VERSION)
    rxnorm_version = ver.get("version") if isinstance(ver, dict) else None

    moa_by_drug = {}
    ok = res = 0
    for i, drug in enumerate(drugs):
        url = (f"{RXCLASS}?drugName={urllib.parse.quote(drug)}"
               f"&relaSource=MEDRT&relas=has_moa")
        j = http_json(url)
        if "_error" in j:
            moa_by_drug[drug] = {"fetch_status": "FETCH_FAILED", "error": j["_error"]}
        else:
            classes = []
            for item in j.get("rxclassDrugInfoList", {}).get("rxclassDrugInfo", []):
                mc = item.get("rxclassMinConceptItem", {})
                if mc.get("classType") == "MOA":
                    e = {"classId": mc.get("classId"), "className": mc.get("className")}
                    if e not in classes:
                        classes.append(e)
            direction = reduce_moa([c["className"] for c in classes])
            moa_by_drug[drug] = {"fetch_status": "OK", "moa_classes": classes, "direction": direction}
            ok += 1
            if direction in ("INHIBITORY", "ACTIVATING"):
                res += 1
        if (i + 1) % 50 == 0:
            print(f"  ...{i+1}/{len(drugs)}", file=sys.stderr)
        time.sleep(0.12)

    snapshot = dict(
        source="MED-RT (NLM/VA Medication Reference Terminology, formerly NDF-RT) Mechanism of Action, "
               "via the NLM RxClass API (class/byDrugName, relaSource=MEDRT, rela=has_moa)",
        api_base="https://rxnav.nlm.nih.gov/REST/rxclass",
        rela_source="MEDRT", rela="has_moa", class_type="MOA",
        rxnav_rxnorm_version=rxnorm_version,
        fetched_utc=datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        drug_universe_note="exactly the approved drugs V4 resolved (read from "
                           "v4_opentargets_snapshot.cache.json); membership inherited, direction re-read",
        n_drugs=len(drugs), n_fetched_ok=ok, n_with_direction=res,
        direction_reduction=dict(
            order="1) INVERSE AGONIST->INHIBITORY  2) NEGATIVE MODULATOR->INHIBITORY / "
                  "POSITIVE MODULATOR->ACTIVATING / bare MODULATOR->drop  3) token scan",
            inhibitory_tokens=["INHIBITOR", "ANTAGONIST", "BLOCKER", "DEGRADER", "BLOCKING"],
            activating_tokens=["ACTIVATOR", "AGONIST", "POTENTIATOR", "OPENER", "STIMULANT", "RELEASING"],
            note="single unambiguous sign per drug across its MoA classes; zero signs OR a conflict -> "
                 "None (dropped, never scored). Magnitude-free: class NAMES only, no potency token."),
        moa_by_drug=moa_by_drug)

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, indent=1, ensure_ascii=False, sort_keys=True)
    print(f"wrote {os.path.relpath(OUT, ROOT)}  (drugs {len(drugs)}, ok {ok}, with-direction {res})")


if __name__ == "__main__":
    main()
