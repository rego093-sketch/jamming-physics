# §12 — Clade-specific methylation readers (plant / insect) + auto-detector

> Follows directly from §11/U3: the M-layer's CpG-O/E substrate is **vertebrate-shaped**.
> This builds the **plant** and **insect** readers, on real NCBI data, and unifies them under
> a methylation-regime **auto-detector**. The key finding that shapes the design: methylation
> has three **architectures**, each needing a different reading **strategy** — read the wrong
> way and you get a false negative.

**Verify:** `python3 run.py` → `SLUG VERIFICATION: PASS` (gate + determinism + fidelity).

## The three architectures (why one reader can't do all)

| architecture | who | where the signal lives | how to read |
|---|---|---|---|
| **global CG blanket** | vertebrates | genome-wide CG depletion | **bulk** windows (human CG O/E 0.13) |
| **global CG+CHG+CHH** | plants (RdDM) | genome-wide CG **and** CHG depletion | **bulk** windows, all contexts |
| **targeted gene-body** | insects (Hymenoptera) | a **gene subset** only | **per-gene** (bulk shows nothing!) |
| **none** | insects (Diptera) | — | substrate inert; regulation is methylation-independent |

## Plant reader — CG + CHG + CHH, validated on 6 plants

| plant | clade | GC% | CG O/E | CHG O/E | CHH O/E | regime |
|---|---|---:|---:|---:|---:|---|
| arabidopsis | Dicot | 34 | 0.771 | 0.85 | 1.08 | PLANT global CG CHG CHH |
| rice | Monocot | 44 | 0.720 | 0.94 | 1.11 | PLANT global CG CHG CHH |
| maize | Monocot | 44 | 0.651 | 0.91 | 1.12 | PLANT global CG CHG CHH |
| soybean | Dicot(legume) | 41 | 0.619 | 0.68 | 1.20 | PLANT global CG CHG CHH |
| tomato | Dicot(solanaceae) | 35 | 0.564 | 0.75 | 1.15 | PLANT global CG CHG CHH |
| moss | Bryophyte(basal) | 35 | 0.520 | 0.69 | 1.17 | PLANT global CG CHG CHH |

All 6 — including the **basal moss** (*Physcomitrium*) — show CG **and** CHG depletion (the RdDM
non-CG signature); CHH stays ~1.1 (the sparse asymmetric context). The vertebrate CpG-only
reader would miss the entire CHG axis.

## Insect reader — two parts

**(A) bulk shows NO global methylation** (the architecture difference): no insect's bulk genome
is CG-depleted — even the methylating bee/wasp sit at CG O/E ~1.4, versus vertebrate 0.13.

**(B) per-gene reveals targeted gene-body methylation** where it exists:

| insect | order | bulk CG | per-gene median | per-gene **spread** | %low-CpG | regime |
|---|---|---:|---:|---:|---:|---|
| fly | Insect | 0.95 | 0.96 | **0.13** | 0% | INSECT none substrate inert |
| mosquito | Diptera(none/low) | 1.06 | 1.14 | **0.10** | 0% | INSECT none substrate inert |
| silkmoth | Lepidoptera(low) | 1.21 | 1.00 | **0.23** | 7% | INSECT none substrate inert |
| beetle | Coleoptera(very low) | 0.95 | 1.03 | **0.18** | 2% | INSECT none substrate inert |
| honeybee | Hymenoptera(methylates) | 1.38 | 1.08 | **0.31** | 12% | INSECT targeted gene body |
| wasp | Hymenoptera(methylates) | 1.35 | 1.08 | **0.19** | 2% | INSECT none substrate inert |

**Honeybee** crosses the targeted-methylation threshold cleanly (per-gene spread 0.31, 12% of
genes in the low-CpG body-methylated class — the Elango/Lyko bimodal signature). **Diptera**
(fly, mosquito) show a tight unimodal ~1, no methylated class → substrate inert.

**Honest gradient [O]:** wasp/silkmoth/beetle sit *below* the detection threshold at this gene-
sample size, consistent with weaker/sparser methylation; resolving them needs larger RefSeq
mRNA panels or direct WGBS (named [O], not silent).

## Auto-detector — one router, all regimes

Reads **bulk CG/CHG first**; only when there is no global signal does it **escalate to per-gene**.
This is the universal M-layer: it matches the reading to the architecture.

- human (vertebrate) → `VERTEBRATE_global_CG` ✓
- arabidopsis (plant) → `PLANT_global_CG_CHG_CHH` ✓
- moss (basal plant) → `PLANT_global_CG_CHG_CHH` ✓
- honeybee (targeted) → `INSECT_targeted_gene_body` ✓
- fly (none) → `INSECT_none_substrate_inert` ✓

## What "no gray zone" means here

16 quantities graded, **14/16 positively evidenced** [F]/[L];
2 [O] each name a closing dataset (per-context WGBS β; larger insect gene panels); 0 silent.
The principle is explicit: **read the substrate the way the clade writes it.**

## Files
```
clade_reader_engine.py        plant reader + insect reader + auto-detector + gate + ledger
run.py                        verifier
inputs_plant/*.fa             6 plant genomic regions (120kb) + _provenance.json
inputs_insect_genomic/*.fa    6 insect genomic regions (120kb, bulk) + _provenance.json
inputs_insect/*.mrna.fa       6 insect RefSeq mRNA sets (per-gene, 3kb cap) + _provenance.json
inputs_ref/human.fa           vertebrate genomic reference
expected/clade_reader_results.json   frozen reference output
clade_readers_4d.png          4-panel figure
LEDGER_clade_readers.md       exhaustive [F]/[V]/[L]/[O]/[B] ledger
```