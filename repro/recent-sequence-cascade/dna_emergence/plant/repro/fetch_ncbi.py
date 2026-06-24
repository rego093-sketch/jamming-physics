#!/usr/bin/env python3
"""fetch_ncbi.py -- (re)fetch every sequence in data/accessions.json from NCBI nuccore.
   The package ships with the GenBank records already frozen under data/plastid and data/stress,
   so this is only needed to re-verify provenance against the live database. The analysis is
   deterministic from the frozen .gb files and does not depend on the network.
"""
import json, os, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def efetch(acc, rettype="gbwithparts"):
    url = BASE + "efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "nuccore", "id": acc, "rettype": rettype, "retmode": "text"})
    for _ in range(4):
        try:
            return urllib.request.urlopen(url, timeout=120).read().decode()
        except Exception:
            time.sleep(3)
    raise RuntimeError("NCBI fetch failed: " + acc)

def main():
    man = json.load(open(os.path.join(DATA, "accessions.json")))
    for name, rec in man["plastid_genomes"].items():
        open(os.path.join(DATA, "plastid", name + ".gb"), "w").write(efetch(rec["accession"]))
        print("plastid", name, rec["accession"]); time.sleep(0.4)
    for name, rec in man["stress_loci"].items():
        open(os.path.join(DATA, "stress", name + ".gb"), "w").write(efetch(rec["accession"]))
        print("stress ", name, rec["accession"]); time.sleep(0.4)
    print("fetched all records from NCBI")

if __name__ == "__main__":
    main()
