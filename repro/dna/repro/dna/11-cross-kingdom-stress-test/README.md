# §11 — Cross-kingdom universality stress test (Workstream U)

> **The generality test the abstract promises but v1.9 never shipped.** The whitepaper
> claims γ "barely changes across species, kingdoms, and phyla (corr(γ,GC)=0.998,
> cross-species CV 0.1–2%)." v1.9 demonstrates the framework on **Homo + Mus only** — one
> locus, two mammals. A cross-**kingdom** claim cannot rest on two mammals. This chapter
> puts the three readable layers under a real cross-kingdom load and **maps where the
> reading holds and where it must be generalized** — closing the gray zone of *validity*.

**Regenerate / verify:** `python3 run.py` → `SLUG VERIFICATION: PASS`
(gate marker + determinism + numeric fidelity vs frozen `expected/`).

---

## The load (measured, READ-ONLY; NCBI efetch, 2026-06-16)

**12 organisms × 120 kb of real autosomal genomic DNA**, frozen in `inputs/` with full
provenance (`inputs/_provenance.json`: RefSeq accession + chromosome coordinates per organism):

| clade | organisms |
|---|---|
| vertebrates | human, mouse, chicken, frog (*Xenopus*), zebrafish |
| invertebrates | fly (*Drosophila*), worm (*C. elegans*) |
| plants | *Arabidopsis* (dicot), rice + maize (monocot) |
| fungus | yeast (*S. cerevisiae*) |
| protist (stress corner) | *Plasmodium falciparum* (~20 % GC, the AT-extremist) |

**Plus** the histone-**H4 ortholog** in all 12 (`inputs_ortholog/`) — the most conserved
eukaryotic protein (~identical yeast→human→maize) — to test the *same-switch* invariance
claim directly. γ is **recomputed in-package** from these FASTAs (Constitution C1).

---

## Three falsifiable stress tests

**U1 — Is γ a universal GC-restatement?** `corr(γ,GC)` per genome, windowed.
→ **YES: ≥0.97 in every kingdom** (min 0.985 zebrafish, max 0.998), holding even at 20 % GC
(*Plasmodium*). γ carries GC's information plus dinucleotide order; it is not an independent
material axis. **[F]**

**U2 — Is γ taxon-invariant?** Measured two ways: bulk-genome γ across kingdoms, and the
histone-H4 ortholog (same protein). → **NO.** Bulk γ CV **5.8 %**; H4-ortholog γ CV **8.3 %**
— both ≫ the abstract's "0.1–2 %". The *same protein*'s γ varies ~30 % and is **99 %-explained
by host-genome GC** (synonymous codon usage). The "0.1–2 %" claim holds **only among iso-GC
species**, not across kingdoms. This is the honest boundary the test exists to find — and it
**preserves the framework's deeper thesis** (γ adds no taxon-specific axis beyond GC, so
"the difference is not in the material" stands; only "γ is invariant" must become "γ tracks
GC"). **[F]** + a named-dataset **[O]** to pin the crossover.

**U3 — Is "CpG O/E" the universal methylation substrate?** The M-layer (§9) reads CpG O/E as
the environment-writable substrate. → **It is a substrate ONLY where the clade methylates CpG.**
CpG depletion cleanly separates methylating clades (vertebrate + plant, O/E 0.13–0.77) from
non-methylating ones (fly/worm/yeast, O/E 0.79–0.97 ≈ 1). The depletion **is the fingerprint of
CpG methylation** — established biology, here measured. Plants additionally deplete **CHG
(non-CG)** (0.85–0.94) absent in vertebrates (1.24–1.50), matching RdDM. **The universal M-layer
reads the clade's CONTEXT** (CG vs CG+CHG+CHH); CpG-only is the mammal special case. **[F]+[L]**.

**E — Helical (~10.4 bp) signal.** Elevated above composition-matched shuffle in **all 12**
genomes (γ-invisible), strong (≥90th pctl) in 9/12, weak/borderline in yeast + *Plasmodium* —
non-uniform, matching Segal/Trifonov. The non-uniformity is the honest finding, not forced. **[F]**.

---

## What "no gray zone" means here

Not that γ is magically universal — the test shows **precisely where it is not**. It means
**every universality question is answered and graded**: 16 questions, **13/16 positively
evidenced [F]/[L]**, 3 [O] each naming its closing dataset, 0 silent. The reading's **domain
of validity is mapped** (see `LEDGER_cross_kingdom.md`). Determinism: fixed arithmetic on
frozen FASTAs → 2× run bit-identical (sha256).

## Files

```
cross_kingdom_engine.py     the engine (recomputes γ/GC/CpG·CHG·CHH/helical; gates; ledger)
run.py                      verifier (gate + determinism + fidelity vs expected/)
inputs/*.fa                 12 frozen genomic regions (120 kb each) + _provenance.json
inputs_ortholog/*_H4.fa     12 frozen histone-H4 orthologs + _provenance.json
expected/cross_kingdom_results.json   frozen reference output
cross_kingdom_4d.png        4-panel figure (γ–GC line · H4 ortholog · CpG fingerprint · helical)
LEDGER_cross_kingdom.md     the exhaustive [F]/[V]/[L]/[O]/[B] ledger
```
