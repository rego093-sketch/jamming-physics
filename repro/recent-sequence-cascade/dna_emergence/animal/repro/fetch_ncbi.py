#!/usr/bin/env python3
"""
fetch_ncbi.py -- (re)fetch every sequence in data/accessions.json from NCBI nuccore.
The package ships with the GenBank records already frozen under data/mito and data/nuc,
so this is only needed to re-verify provenance against the live database. Determinism
of the analysis does not depend on the network: it reads the frozen .gb files.
"""
import json, os, time, urllib.request, urllib.parse
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

def efetch(acc, rettype="gb"):
    url = BASE + "efetch.fcgi?" + urllib.parse.urlencode(
        {"db": "nuccore", "id": acc, "rettype": rettype, "retmode": "text"})
    for _ in range(4):
        try:
            return urllib.request.urlopen(url, timeout=90).read().decode()
        except Exception:
            time.sleep(3)
    raise RuntimeError("NCBI fetch failed: " + acc)

def main():
    man = json.load(open(os.path.join(DATA, "accessions.json")))
    for name, rec in man["mitogenomes"].items():
        open(os.path.join(DATA, "mito", name + ".gb"), "w").write(efetch(rec["accession"]))
        print("mito", name, rec["accession"]); time.sleep(0.4)
    for name, rec in man["nuclear_state_loci"].items():
        open(os.path.join(DATA, "nuc", name + ".gb"), "w").write(efetch(rec["accession"]))
        print("nuc ", name, rec["accession"]); time.sleep(0.4)
    print("fetched all records from NCBI")

if __name__ == "__main__":
    main()
