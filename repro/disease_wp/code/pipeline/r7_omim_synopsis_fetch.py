#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R7 stage -- OMIM clinical-synopsis FETCH (credentialed S / prognosis enhancement).

OMIM's clinical synopsis (structured Clinical Features / Inheritance / prognosis
per MIM) is the cleanest independent source for the SEVERITY (S) axis and for
corroborating PROGRESSION (P) / mortality (M). The OMIM API requires a registered
key (free research licence at omim.org/api); the public site blocks automated
access. So this stage is GATED on an environment key, exactly like R6's frequency
gate skips an axis with no qualifying term:

  * OMIM_API_KEY present -> fetch each cohort MIM's clinicalSynopsis from
    api.omim.org, cache under data/raw/omim/, sha-pin, exit 0.
  * OMIM_API_KEY absent  -> write a _fetch_log.json recording the named obstacle
    ("OMIM key not provided -- S / prognosis lift skipped"), touch no axis, exit 0.

The apply stage treats a missing OMIM cache as "S not lifted from OMIM (obstacle
named)"; S is never guessed. This keeps the run reproducible with OR without the
credential, and honest either way.

INVESTIGATION/AUTHORING support -- living code, NOT in the frozen engine pin.

Out: data/raw/omim/<mim>.json (+ _fetch_log.json)   [key present]
     data/raw/omim/_fetch_log.json                  [key absent: obstacle only]
"""
import os, sys, json, time, hashlib, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUR = os.path.join(ROOT, "data", "curated")
OMIM = os.path.join(ROOT, "data", "raw", "omim")
LOG = os.path.join(OMIM, "_fetch_log.json")
API = "https://api.omim.org/api/entry"
RETRIEVED = "2026-06-18"
UA = {"User-Agent": "disease_wp/0.9 OMIM-clinical-synopsis (research; ORCID 0009-0002-7535-8245)"}
SLEEP = 0.30


def cohort_mims():
    """Every type-level MIM in the cohort (from the R6 registry records)."""
    base = json.load(open(os.path.join(CUR, "burden_scores_registry.json")))
    mims = {}
    for r in base["records"]:
        for m in r.get("omim_codes", []):
            mims.setdefault(m, []).append(r["entity"])
    return mims


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    os.makedirs(OMIM, exist_ok=True)
    key = os.environ.get("OMIM_API_KEY", "").strip()
    mims = cohort_mims()

    if not key:
        log = {
            "source": "OMIM clinical synopsis (api.omim.org)",
            "retrieved": RETRIEVED,
            "status": "SKIPPED",
            "obstacle": ("OMIM_API_KEY not provided in the environment (and the public OMIM site "
                         "blocks automated access: HTTP 403 from datacenter IPs). The OMIM-anchored "
                         "S (severity) / prognosis lift is skipped; the S axis is NOT guessed. "
                         "Register a free research key at omim.org/api and set OMIM_API_KEY to enable "
                         "this pass. PMC published-literature fallback (r7_litsurvival_fetch.py) still "
                         "runs for M/P."),
            "cohort_mims": len(mims),
            "fetched": 0,
        }
        json.dump(log, open(LOG, "w"), indent=2, ensure_ascii=False)
        print("  OMIM_API_KEY absent -> clinical-synopsis pass SKIPPED (obstacle recorded, S not guessed).")
        print(f"  cohort MIMs that WOULD be queried with a key: {len(mims)}")
        print(f"  -> {os.path.relpath(LOG, ROOT)}")
        return

    # ---- key present: fetch each MIM's clinical synopsis ----
    log = {"source": "OMIM clinical synopsis (api.omim.org)", "retrieved": RETRIEVED,
           "status": "FETCHED", "cohort_mims": len(mims), "entries": {}}
    fetched = 0
    for mim in sorted(mims):
        q = urllib.parse.urlencode({"mimNumber": mim, "include": "clinicalSynopsis",
                                    "format": "json", "apiKey": key})
        url = f"{API}?{q}"
        try:
            req = urllib.request.Request(url, headers=UA)
            raw = urllib.request.urlopen(req, timeout=45).read()
        except Exception as e:
            log["entries"][mim] = {"ok": False, "error": str(e)}
            time.sleep(SLEEP)
            continue
        path = os.path.join(OMIM, f"{mim}.json")
        with open(path, "wb") as fh:
            fh.write(raw)
        log["entries"][mim] = {"ok": True, "bytes": len(raw), "sha256": sha256_bytes(raw),
                               "entities": mims[mim]}
        fetched += 1
        time.sleep(SLEEP)
    log["fetched"] = fetched
    json.dump(log, open(LOG, "w"), indent=2, ensure_ascii=False)
    print(f"  OMIM clinical synopsis fetched for {fetched}/{len(mims)} MIMs -> data/raw/omim/")


if __name__ == "__main__":
    main()
