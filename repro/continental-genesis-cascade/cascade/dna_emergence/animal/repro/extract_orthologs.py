#!/usr/bin/env python3
"""extract_orthologs.py -- pull the 13 orthologous mito protein-coding genes from each
   frozen GenBank record, normalising gene names so the same gene lines up across taxa.
   data/mito/*.gb  ->  results/orthologs.json"""
import json, os
from Bio import SeqIO
HERE = os.path.dirname(os.path.abspath(__file__))
MITO = os.path.join(HERE, "data", "mito")
RES  = os.path.join(HERE, "..", "results")
GENOMES = ["mammoth", "asian_elephant", "african_elephant", "human", "neanderthal", "denisovan"]
CANON = {
 "ND1":["ND1","NAD1"], "ND2":["ND2","NAD2"], "COX1":["COX1","COI","CO1"],
 "COX2":["COX2","COII","CO2"], "ATP8":["ATP8","ATPASE8"], "ATP6":["ATP6","ATPASE6"],
 "COX3":["COX3","COIII","CO3"], "ND3":["ND3","NAD3"], "ND4L":["ND4L","NAD4L"],
 "ND4":["ND4","NAD4"], "ND5":["ND5","NAD5"], "ND6":["ND6","NAD6"], "CYTB":["CYTB","COB","CYB"],
}
def canon_name(raw):
    r = raw.upper().replace("MT-", "").replace("-", "").replace("_", "")
    for c, syn in CANON.items():
        if r in [s.replace("-", "") for s in syn]:
            return c
    return None

def main():
    out = {}
    for g in GENOMES:
        rec = SeqIO.read(os.path.join(MITO, g + ".gb"), "genbank")
        genes = {}
        for f in rec.features:
            if f.type != "CDS":
                continue
            nm = None
            for key in ("gene", "product"):
                if key in f.qualifiers:
                    nm = canon_name(f.qualifiers[key][0])
                    if nm:
                        break
            if not nm or nm in genes:
                continue
            genes[nm] = str(f.extract(rec.seq)).upper()
        out[g] = {"accession": rec.id, "length": len(rec.seq), "genes": genes}
        print(f"{g:18s} {rec.id:14s} CDS={len(genes):2d}")
    common = set(CANON)
    for g in GENOMES:
        common &= set(out[g]["genes"])
    print("genes in all six:", sorted(common), f"(n={len(common)})")
    os.makedirs(RES, exist_ok=True)
    json.dump(out, open(os.path.join(RES, "orthologs.json"), "w"))

if __name__ == "__main__":
    main()
