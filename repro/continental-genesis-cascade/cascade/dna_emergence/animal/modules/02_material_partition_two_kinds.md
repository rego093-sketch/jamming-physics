# Module 02 — Emergence I: the material partitions into two kinds (H1)

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Tier:** 1 (emergence) · **Consumes:** Module 01 (the inherited engine) · **Data:** 6 real NCBI mitogenomes.
**Status:** BUILD + GRADE. Every number reproduces from `repro/extract_orthologs.py` + `repro/bimodality.py` over the frozen records.
**Standing grade:** per-gene two-kind partition **[V]**; any past history producing the kinds **[O]**.

> **One line.** Read gene by gene through the inherited engine, the material γ sorts the six real genomes into **two kinds with no overlap on all 13/13 genes** (mammoth with living elephants; Neanderthal + Denisovan with humans), the between-kind gap beating within-kind spread by a **median 17×**. The *average* of the two kinds lands, per gene, in an empty gap — it matches no real kind.

---

## 1. Data (real, fetchable)

Six mitogenomes, extracted to the 13 orthologous protein-coding genes present in all six:

| taxon | accession | role |
|---|---|---|
| mammoth | NC_007596.2 | "past" elephant-kind |
| Asian elephant | NC_005129.2 | present elephant-kind |
| African elephant | NC_000934.1 | present elephant-kind |
| human (rCRS) | NC_012920.1 | present human-kind |
| Neanderthal | KC879692.1 | "past" human-kind |
| Denisovan | FN673705.1 | "past" human-kind |

`repro/extract_orthologs.py` → `results/orthologs.json` (CDS normalised so the same gene lines up across taxa; 13 genes in all six).

## 2. The read

`repro/bimodality.py` reads γ for every gene × taxon and tests the partition.

**Per-gene clean gap.** For **all 13/13 genes**, max(Elephantidae γ) < min(Homo γ): a strictly empty gap, no overlap. Example values (γ):

- ND1: elephants 1.2680–1.2782 | homo 1.3469–1.3607
- ATP8: elephants 1.2210–1.2432 | homo 1.2608–1.2822
- CYTB: elephants 1.2813–1.2839 | homo 1.3425–1.3494

**Separation ratio** (between-kind gap ÷ within-kind sd): **median 17.1×**, min **4.0× (ATP8)**, max **28.4× (COX3)**. Within each kind, γ is conserved — the three elephants are one material, the three homo are one material.

**The "average is no kind" point.** Band centres γ ≈ **1.2545** (Elephantidae) and **1.3229** (Homo); global mean **1.2887** sits between them. Per gene, the midpoint of the two kinds lands in *that gene's* empty gap — so the averaged value corresponds to no real kind. This is the anti-average-theory hinge made concrete.

## 3. Honest qualification (반증 = 발견)

The partition is **per gene, not pooled.** Pooled across all 13 genes the two sets are **not** cleanly separated (elephant pooled max 1.2839 > homo pooled min 1.2608), because each gene has its own baseline γ and that baseline varies more than the between-kind gap (CYTB-in-elephants exceeds ATP8-in-homo). So the kind distinction is carried by the **per-gene** comparison, **not** by a global bimodality — and we say so rather than overselling. The robust claim is the per-gene one.

## 4. Grade

| Claim | Grade |
|---|---|
| 13/13 genes: clean per-gene material gap between the two kinds | **[V]** |
| Median 17× separation (4×–28×); within-kind γ conserved | **[V]** |
| Per-gene midpoint of the two kinds matches no real kind | **[V]** |
| Pooled γ is bimodal | **not claimed** (honest: it is not) |
| A flood / deep-time descent produced the two kinds | **[O]** (both directions) |

**Verdict: in the material channel, "past animal" and "present animal" of a kind read as one kind — per gene, cleanly, 13/13.**
