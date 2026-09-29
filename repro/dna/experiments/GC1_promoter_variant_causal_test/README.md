# GC1 — Is γ a cause? A single-variant intervention test (protocol only)

This test has **not been run**, for two reasons:
- The build environment cannot reach any variant or genome source (ClinVar, UCSC, Ensembl, NCBI).
- The repository holds no human promoter sequence for the target genes, and reconstructing one from memory would break the rule that we speak only with facts and code.

The protocol is fixed in advance in `PROTOCOL.json`:
- **Test:** whether the direction of Δγ predicts the measured direction of expression change, variant by variant.
- **Recorded expectation:** the γ *level* channel (GC content) agrees only at chance level, and any causal signal sits in the sequence-specific channels (A4 shape, CpG).

Run it once reference sequences and a measured variant set are available.
