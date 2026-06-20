# IRREPRODUCIBILITY LEDGER — 17-spinal-cord-locomotor-cpg (VP-SPEC C3; DNA-volume 5-grade)

This chapter adopts the DNA volume's **exhaustive 5-grade discipline**: every quantity of the
interpretation is graded, so **nothing is silent or vague** (this does *not* mean zero unknowns).
The engine enumerates **21** quantities and grades each, then gates that the enumeration is complete
(no ungraded item; every item carries a stated basis/obstacle; no silent [O]).

**Grades.** `[F]` read from γ-structure · `[V]` verified/reproduced in-package · `[L]` peer-reviewed
(cited, not re-derived) · `[O]` empirically open but **dataset-named** · `[B]` framework category boundary.

**Counts:** 21 total — **10 [F] · 3 [V] · 3 [L] · 3 [O] · 2 [B]**; **16/21 positively evidenced**; 0 ungraded.

## The reproducible core (not in this ledger because it reproduces)

- **γ of 19 master-gene promoters** recomputed in-package from NCBI FASTA (GRCh38, 2501 bp), 0 drift vs frozen. [F]
- **one material class:** γ-band width 0.182; cardinal D-V-TF γ-span 0.115; 12/19 promoters are CpG islands →
  identity is **combinatorial** (one R19 switch, different wiring), not material. [F]
- **dorsoventral order p3, pMN, p2, p1, p0** derived from a monotonic Shh drive + four cross-repressive
  **bistable** R19 switches (sharp domains, count = switches+1 = 5), order **matches measured** (Briscoe 2000). [F]/[V]
- **CPG wiring** from the neuron-class code — V0(DBX1/EVX1) left-right, V2a(VSX2) high-freq left-right,
  V1(EN1)+V2b(GATA3) flexor-extensor, V3(NKX2-2→SIM1) rhythm robustness, MN(ISL1/MNX1/LHX3) output —
  all four CPG functions present. [V]/[L]
- **honest [F]:** γ is **flat** across the code, so the **order is the morphogen spinodal, not γ-ranking**.
  (Layer-1 γ is identity; spatial position is the Shh threshold.)

## The open and boundary items

| # | item | grade | obstacle / reason (and closing dataset, if [O]) | location |
|---|------|-------|--------------------------------------------------|----------|
| O1 | **exact framework γ-window per gene** | `[O]` | This engine uses the reproducible window `[TSS−2000, TSS+500] = 2501 bp` (the LCT window length). The framework's **exact** per-gene promoter window is undocumented — the **same provenance gap** as neuro §16's MYOD1 γ-window. **Closes with:** the framework's published window spec. A provenance gap, not a physics gap (γ on any fixed window is deterministic and reproduced here). | engine header LOCK; `inputs/*.fa` |
| O2 | **absolute neuron numbers per class** | `[O]` | The structure (order, classes, modules) is derived; the **count** of each class is not. **Closes with:** a single-cell census (mouse spinal scRNA-seq / stereology). A count, not a structure. | engine `[O]` block |
| O3 | **Shh absolute concentration profile** | `[O]` | The threshold **order** is measured and the discrete ordered pattern is derived; the **absolute** morphogen concentrations are not. **Closes with:** quantitative morphogen imaging (Shh-GFP gradient dataset). Refines the threshold values, not the order. | `spinodal_order()`; threshold values |
| B1 | **relative neuron counts / domain sizes (DWELL ∝ γ^1.5)** | `[B]` | A **Layer-2** illustrative-rate quantity — the quantity layer (φ) is, by construction, not read from the γ window. Forcing it to [F] would be dishonest. | data `_boundary`; engine `[B]` block |
| B2 | **firing-rate / force magnitudes** | `[B]` | The **above-γ biophysical layers** — rate coding and muscle force are the R19 / EM / cross-bridge layers (neuro §2, §14, §16), not the γ identity layer. A category boundary, not a gap. | data `_boundary`; engine `[B]` block |

## What "no gray zone" means here

Every quantity is addressed: the reproducible core is `[F]`/`[V]`/`[L]`; the three `[O]` items each **name a
closing dataset** and refine an already-evidenced claim; the two `[B]` items are the framework's defining
boundaries. **17/21 are positively evidenced or measured; 0 are ungraded.**

## Cross-references to sibling reproductions

- **DNA volume (γ → M → E).** The γ metric here is **identical** to the DNA volume's and was validated
  bit-for-bit against its frozen LCT values (human 1.3153 / mouse 1.3496, |Δγ| = 0.034 "same material").
  This chapter is the neural-tissue application of the same Layer-1 reading.
- **neuro §2 (R19 switch).** Each cross-repressive domain boundary **is** an R19 bistable switch settling on
  the local Shh drive; the spinal D-V pattern is a *stack* of those switches — the same substrate, in space.
- **neuro §12 (organ emergence, 4D).** Same method (master-gene γ + spinodal order + DWELL∝γ^1.5 quantity);
  §12 did sensory organs, this does the spinal motor circuit.
- **neuro §14 / §16 (motor quantification / force).** This chapter ends at the motor-neuron **identity** and the
  CPG **wiring**; §14 quantifies the MN output (Ohm/size principle) and §16 the muscle force — the **B2** boundary
  here is exactly the handoff to those biophysical layers.
