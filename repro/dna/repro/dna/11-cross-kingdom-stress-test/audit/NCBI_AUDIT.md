# NCBI data-integrity audit (v1.9 frozen constants + v1.10 inputs)

The user asked for NCBI verification ("ncbi에서 data 을 받아서 검수"). Two audits were run.

## A. v1.9 frozen constants reproduce exactly from live NCBI

The three measured loci frozen in `_engine/data/lactase_interpretation.json` were re-fetched
live from NCBI eutils on **2026-06-16** at their stated coordinates, and γ/GC/CpG O/E recomputed:

| locus | NCBI region | γ frozen | γ re-fetch | Δγ | verdict |
|---|---|---:|---:|---:|:---:|
| LCT_human | NC_000002.12:135836683-135839183 | 1.3153 | 1.3153 | **0.0000** | MATCH |
| MCM6_enh_human | NC_000002.12:135849933-135852433 | 1.2581 | 1.2581 | **0.0000** | MATCH |
| LCT_mouse | NC_000067.7:128255554-128258054 | 1.3496 | 1.3496 | **0.0000** | MATCH |

GC and CpG O/E likewise match to 4 decimals. **The v1.9 frozen constants are reproducible
from the primary database — real, fetched, and audited, not merely internally consistent.**

Re-verify offline (the LCT re-fetch is frozen in `audit/LCT_human_refetch.fa`):
`python3 audit/audit.py` → PASS. (The full 3-locus live audit requires network.)

## B. v1.10 cross-kingdom inputs are freshly fetched with frozen provenance

The 12 genomic regions (`inputs/*.fa`) and 12 histone-H4 orthologs (`inputs_ortholog/*_H4.fa`)
were fetched from NCBI RefSeq reference assemblies on 2026-06-16; each carries its accession +
coordinates in `inputs/_provenance.json` / `inputs_ortholog/_provenance.json`. They are frozen
READ-ONLY; γ is recomputed from them in-package (`run.py` → fidelity 254/254, determinism PASS).

**Note on gene-identity rigor:** an initial fuzzy product-name search returned mis-identified
hits (e.g. "histamine receptor H4" for histone H4, "alpha-tubulin acetyltransferase" for
tubulin). Those were rejected; the shipped inputs use (a) curated RefSeq **chromosome**
accessions for the genomic regions (no gene-family ambiguity) and (b) **validated** histone-H4
records (enzyme/TF/reader hits filtered out). Provenance headers preserve the exact source.
