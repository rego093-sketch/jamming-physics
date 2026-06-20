#!/usr/bin/env python3
"""
R6 stage 1 -- Orphanet (Orphadata) natural-history product fetch.

Pulls the three Orphadata free products needed for the deferred natural-history
registry pass and records a pinned-sha provenance log. Orphadata is published by
Orphanet under CC BY 4.0, so the structured fields are citeable observed inputs
(constitution C-D1): values attached to an ORPHAcode, not free text we parse.

Products (orphadata.org, en):
  * en_product1.xml       cross-references  -> OMIM <-> ORPHAcode mapping (with
                          DisorderMappingRelation: E = exact, BTNT/NTBT = broader/
                          narrower). Drives the cohort join.
  * en_product9_ages.xml  natural history   -> AverageAgeOfOnset + TypeOfInheritance
                          per ORPHAcode. Registry-grade ONSET source (axis O).
  * en_product4.xml       HPO phenotypes    -> HPO terms per ORPHAcode WITH Orphanet
                          frequency (Obligate/Very frequent/Frequent/Occasional/...).
                          Registry-grade MORTALITY (axis M) and CLINICAL-COURSE
                          (axis P) source via the HPO Mortality/Aging and Clinical-
                          course subtrees, frequency-gated.

This stage is the only one that touches the network. It is idempotent: a product
already on disk whose sha256 matches the recorded pin is NOT re-downloaded. The
apply stage (r6_naturalhistory_registry.py) runs offline against this cache.

INVESTIGATION/AUTHORING support -- living code, NOT in the frozen engine pin.

Out: data/raw/orphanet/<product>.xml + data/raw/orphanet/_fetch_log.json
"""
import os, sys, json, hashlib, datetime, urllib.request, xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ORPHA = os.path.join(ROOT, "data", "raw", "orphanet")
LOG = os.path.join(ORPHA, "_fetch_log.json")
BASE = "http://www.orphadata.org/data/xml"
RETRIEVED = "2026-06-17"

# Products + the sha256 pins recorded when first fetched this phase. A re-fetch that
# yields a different sha is reported (Orphadata is periodically re-released); the pin
# is what the apply stage and gate verify, so a snapshot change is never silent.
PRODUCTS = {
    "en_product1.xml":      "fb2fbe8cc3f04c2ffb3fac3c498bce75e56cfc46b5475e3da30e97f8349140db",
    "en_product9_ages.xml": "c8dba4d4a424527a3bda9e0d0e6701451afb372b693d1f19b507879d6bf155b8",
    "en_product4.xml":      "82079cfb9e6fdce0280001338618ecc8f4a5ae76d66f8e7c22e39fcdaebdebb7",
}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def disorder_count(p):
    try:
        root = ET.parse(p).getroot()
        return sum(1 for _ in root.iter("Disorder"))
    except Exception:
        return None


def main():
    os.makedirs(ORPHA, exist_ok=True)
    log = {"source": "Orphanet / Orphadata (orphadata.org), CC BY 4.0",
           "retrieved": RETRIEVED, "base": BASE, "products": {}}
    all_ok = True
    for fname, pin in PRODUCTS.items():
        path = os.path.join(ORPHA, fname)
        url = f"{BASE}/{fname}"
        cached_ok = os.path.exists(path) and sha256_file(path) == pin
        if cached_ok:
            action = "cached (sha matches pin)"
        else:
            print(f"  fetching {url} ...")
            req = urllib.request.Request(url, headers={"User-Agent": "disease_wp/0.8 (research)"})
            data = urllib.request.urlopen(req, timeout=180).read()
            with open(path, "wb") as fh:
                fh.write(data)
            action = "downloaded"
        sha = sha256_file(path)
        ok = (sha == pin)
        all_ok = all_ok and ok
        log["products"][fname] = {
            "url": url, "action": action, "bytes": os.path.getsize(path),
            "sha256": sha, "pin": pin, "sha_matches_pin": ok,
            "disorders": disorder_count(path),
        }
        flag = "OK" if ok else "SHA DIFFERS FROM PIN"
        print(f"  {fname:22s} {action:26s} {os.path.getsize(path):>10,} B  sha {sha[:12]}  [{flag}]")

    json.dump(log, open(LOG, "w"), indent=2)
    print(f"\n  provenance -> {os.path.relpath(LOG, ROOT)}")
    if not all_ok:
        print("  WARNING: at least one product sha differs from its recorded pin "
              "(Orphadata re-release). Update the pins + re-run the apply stage + gate.")
        sys.exit(2)
    print("  all products verify against recorded pins.")


if __name__ == "__main__":
    main()
