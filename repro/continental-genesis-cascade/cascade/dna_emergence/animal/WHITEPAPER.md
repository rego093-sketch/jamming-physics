# The VP Recent-Sequence DNA Emergence
### Reading real NCBI genomes through the inherited material engine — a *present-tense, material* reading that doubts the average theory

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245
**License:** CC BY 4.0 · **Site:** https://jamming-physics.org/
**Inherits:** VP physics foundation (DOI 10.5281/zenodo.17932566) · Atlantic-opening geodynamics volume (DOI 10.5281/zenodo.17978934) · **VP DNA interpretation method** (DOI 10.5281/zenodo.20471407) · archaic/modern aging-promoter precedent (DOI 10.5281/zenodo.20756155)
**Sibling of:** the VP Recent-Sequence **Cascade** (the geophysical face); this is the **biological / DNA face** of the same recent-sequence question.
**Governance:** VP-SPEC — no-tuning · LOCK→Derive→Gate · graded verdicts [F]/[V]/[L]/[O] · **bidirectional chronology firewall** · single-substrate (R19 bistable switch).

---

## How to read this document

This is a **construction**, not a claim about history. It inherits one specific instrument — the VP DNA *material reading* — applies it to **real, fetchable NCBI genomes**, and asks a single empirical question:

> **When the same genes of "a past animal and a present animal" (mammoth/elephant; Neanderthal/modern human) are read through the inherited material engine, what does the *material* say — and is the molecular clock (the axis the average theory turns into deep-time trees) the same channel as the material, or a different one?**

The instrument is fixed in advance and is **not ours to tune**. The inherited DNA method (DOI 10.5281/zenodo.20471407) reads any locus into measured channels with **one deterministic rule** and is **explicitly silent on evolution / phylogeny** — it reads *present-tense material*, nothing about descent or age. Its central inherited thesis is the hinge of everything below:

> *The readable material (γ) barely changes across taxa; the difference lives in the **inventory** (which loci are present), the **state** (which switch is set), and the **dwell** (how long it is held) — over which the **environment** sets and remembers.*

**The governing firewall.** Every statement about a **past occurrence** — a flood between the two animals, *or* a deep-time gradual descent between them — is capped at grade **[O] (open)** in **both** directions. This document neither smuggles in "recent / a flood" nor "deep time." What can be graded **[F]/[V]** is *mechanism* and *present-tense measurement*; **[L]** marks a well-anchored inference; **[O]** marks what stays open. **The win claimed here is not a chronology.** It is an empirical, reproducible result about *which channel carries what* — and that result is what "doubting the average theory" looks like when it is made to face data.

**"Doubt the average theory" — what that means operationally.** The DNA method is an achievement *made by prohibiting evolution-as-default*: it refuses to read a sequence as a point on an averaged descent-gradient and instead reads the present material directly. So the test we run is exactly the one that prohibition implies: **take the average theory's own instrument (the substitution count / molecular clock) and the material instrument, run both on the same genes, and measure whether they are one channel or two.** If they are decoupled, the clock is — in the cascade's own words — *"an internal technicality"* that cannot, by itself, carry a history decision.

---

## 1. The inherited instrument (fixed, not tuned)

The VP DNA reading is vendored faithfully from the inherited method and re-run here (`repro/vp_gamma_engine.py`). One deterministic function maps any locus to its **material stacking stiffness**:

**γ = −mean(NN stacking ΔG)** over the SantaLucia (1998) unified nearest-neighbour table (kcal/mol), strand-symmetric, bit-for-bit. From γ alone the locus's own **R19 bistable switch** scale follows with no further input: spinodal threshold = (2/3√3)·γ^1.5, barrier = γ²/4. **Nothing is fitted.** Changing any LOCK constant would define a new version, not a tuning of this one.

This γ is the **material channel**. It is the *same* engine the inherited method uses to read promoters, and it is the *same* R19 switch that the physics foundation derives as the universal jammed ⇄ unjammed bistable. We do not modify it; we *feed it real genomes*.

- **Inheritance confirmed [V].** The engine reproduces the inherited method's behaviour and the archaic/modern precedent: in the inherited aging volume, four aging-master promoters read across seven dated genomes (GRCh37 + three Neanderthal + one Denisovan + two ancient modern humans) gave a per-gene γ range **< 0.0016** — i.e. γ is *already known* to be near-invariant archaic↔modern human. We inherit that instrument and that precedent without alteration (Module 01).

*Grade: instrument inherited and reproduced [V]; its evolution-silence is a property of the method, not an assumption we add.*

---

## 2. Emergence I — the material partitions into two kinds (H1)

We fetched six **real mitogenomes** from NCBI — mammoth (NC_007596.2), Asian elephant (NC_005129.2), African elephant (NC_000934.1), human/rCRS (NC_012920.1), Neanderthal (KC879692.1), Denisovan (FN673705.1) — extracted the **13 orthologous protein-coding genes** present in all six, and read each through the material engine (`repro/extract_orthologs.py`, `repro/bimodality.py`).

**Result [V].** Read **gene by gene**, the material γ cleanly sorts the six taxa into two kinds:

- For **all 13 / 13 genes**, every Elephantidae value (mammoth, Asian, African) sits **strictly below** every Homo value (human, Neanderthal, Denisovan) — a real per-gene gap with **no overlap**.
- The between-kind gap exceeds the within-kind spread by a **median 17×** (range **4× at ATP8** to **28× at COX3**).
- *Within* each kind the spread is tiny — mammoth, Asian and African elephant read as **one material**; human, Neanderthal and Denisovan read as **one material**.

The two band centres are γ ≈ **1.2545** (Elephantidae) and γ ≈ **1.3229** (Homo); the global mean over all six taxa is γ ≈ **1.2887**, sitting **between** them. **Per gene, the midpoint of the two kinds lands in that gene's own empty gap — it matches no real kind.** This is the anti-average-theory point made concrete: the *average* of two materials corresponds to no material that exists.

**Honest qualification recorded in the open (반증 = 발견).** The partition is **per gene**, not in the *pooled* γ. Pooled across all 13 genes the two sets are **not** cleanly separated (elephant pooled max 1.2839 > homo pooled min 1.2608), because each gene has its own baseline γ and that baseline varies more than the between-kind gap (e.g. CYTB in elephants exceeds ATP8 in humans). The instrument that carries the kind distinction is therefore the **per-gene** comparison, and we state that rather than overselling a global bimodality. The per-gene result is robust; the pooled distribution is not the claim.

*Grade: per-gene two-kind material partition [V] (13/13, median 17×); pooled bimodality explicitly NOT claimed.*

---

## 3. Emergence II — the clock and the material are *decoupled* (H2, the core result)

This is the load-bearing experiment, and it is exactly the "doubt the average theory" test. On the **same** 13 genes, within each clade, for **all 78 within-clade gene-pairs**, we read both channels (`repro/compare_channels.py`):

- **(A) material channel:** |Δγ| between the two members of the pair;
- **(B) clock channel:** the number of **substitutions** over a global alignment — the quantity the average theory turns into branch lengths and deep-time trees.

**Result [V] — the channels are decoupled.** Across the 78 gene-pairs:

> **Pearson r(substitutions, |Δγ|) = −0.081 ≈ 0.**

The clock counts **2656 substitutions** in total; over those same pairs γ moves a mean of only **0.0057** on an operating scale of **1.29** (range 1.221–1.361) — and the movement it *does* make is **not in proportion** to the substitution count. The per-substitution material movement is **~0.00017 γ per substitution**. Concretely:

- mammoth vs Asian elephant **COX2: 33 substitutions, |Δγ| = 0.0001** — the clock ticks hard, the material does not move;
- Asian vs African elephant **ATP8: 5 substitutions, |Δγ| = 0.0144** — the clock barely ticks, the material moves *most*.

The molecular clock and the material measure **different physical channels.** The clock is counting *substitution events* (a history-of-edits axis); the material γ is reading *present stacking stiffness* (a here-and-now state). **The average theory reads (B) as an age/descent axis; this result shows (B) does not even predict the material the locus is actually made of.** A near-zero correlation is precisely what the inherited method's evolution-silence predicts: the material is conserved, the substitutions accumulate orthogonally to it, and **a clock distance therefore cannot be promoted to a material or kind statement.** In the cascade's vocabulary, the clock is an *internal technicality* — degenerate, like magnetic stripes under uniform time-rescaling — and cannot, alone, carry a history decision.

*Grade: clock/material decoupling [V] (r = −0.08, n = 78). This is the package's central, defensible empirical contribution.*

---

## 4. Emergence III — the STATE face: adaptive difference is a switch, not a material shift (H3)

If the material is conserved within a kind, where does a *real* adaptive difference between a past and present animal live? The inherited thesis says **STATE** — a localised set of coding changes the environment sets and holds. We tested this on the two best-known adaptive loci, reading **real nuclear coding sequences** through the same engine (`repro/state_face.py`).

**HBB/D — cold-tolerant haemoglobin (Campbell et al. 2010).** Across mammoth, Asian and African elephant the **material γ is conserved** (range **0.0052**). The mammoth-vs-Asian difference is **4 nt → exactly 3 amino-acid changes: A13T, S87A, Q102E** — *precisely* the cold-adaptation substitutions Campbell et al. identified. The adaptive difference is a **handful of coding substitutions on a materially conserved locus** — a switch STATE, not a material shift. The engine *recovers the known biology* without being told it.

**MC1R — the coat-colour switch, and a bistable in the act (Rømpler et al. 2006).** Material γ conserved across the three (range **0.0023**). The two mammoth haplotypes differ by **3 nt → 3 amino-acid changes: T21A, R67C, R301S**, with |Δγ| = **0.0019** — material identical, only the **STATE** differs. This is **one R19 bistable switch caught with its two states both present in the same kind**: a full-activity coat state and a reduced-activity coat state, exactly the bistable the foundation predicts as the universal substrate. One switch, one conserved material, two coat states — *the difference the environment sets lives in STATE, as the reading predicts.*

*Grade: STATE face [V] — material conserved on adaptive loci; difference is a localized, literature-confirmed switch state (and a bistable observed in both states).*

---

## 5. The honest instrument check — window length (반증 = 발견)

The archaic/modern precedent put per-gene γ conservation at **< 0.0016**, yet the mito genes here show within-kind γ ranges up to **~0.014**. Is that a real material difference, or an **instrument artefact**? We checked (`repro/length_effect.py`).

γ = −mean(NN ΔG) is a mean over (L−1) steps, so its sampling noise falls with window length. Empirically, **r(gene length, within-kind γ-range) = −0.56**: the short genes are the noisy instrument (**ATP8, 201 bp: range 0.022**) and the long genes recover the promoter-scale conservation (**ND5, 1812 bp: 0.0068; COX1, 1542 bp: 0.0014**). The within-kind γ-range inflation is therefore a **window-length artefact**, and the long-window read is the cleaner instrument — consistent with the inherited < 0.0016 precedent.

Crucially, **this does not touch H1 or H2.** Both are *between-kind* / *cross-channel* contrasts, not within-kind window noise: the two-kind gap (median 17×) dwarfs the window noise, and the clock/material decoupling is a correlation between two channels measured on identical windows. The honest finding sharpens the instrument; it does not weaken the two load-bearing results.

*Grade: window-length effect [V] as an instrument property; it bounds within-kind reads and leaves the between-kind/cross-channel results intact.*

---

## 6. Synthesis — what the material says, and what stays open

Putting the four reads together, **on present-tense material grounds**:

1. The material **partitions the two kinds** cleanly, gene by gene (H1, [V]). Mammoth reads as the same material as living elephants; Neanderthal and Denisovan read as the same material as living humans. *In the material channel, "past animal" and "present animal" of a kind read as one kind.*
2. The **clock is decoupled from the material** (H2, [V]). The substitution count — the average theory's deep-time axis — does **not** predict the material the locus is made of (r = −0.08). So the clock is a *different channel*, not a material/age read-out.
3. The **adaptive difference is a switch STATE**, not a material shift (H3, [V]), and one bistable is caught with both states present in the same kind.

**What this does — and does not — establish.** The material reading supports the *present-tense* statement that each pair is **one kind** ([V]). It does **not**, and under the firewall **cannot**, decide *history*. Because the clock is decoupled from the material (H2), the clock cannot carry a deep-time descent claim *to the material* — but neither does any result here establish that a flood occurred between the two animals. **Both "a flood between them" and "a deep-time gradual descent between them" remain [O]**, exactly as the bidirectional firewall requires. The genuine, defensible contribution is **not** a chronology; it is the empirical demonstration that *the average theory's instrument and the material instrument are different channels*, plus the clean two-kind material partition and the literature-confirmed STATE face. That is what "doubt the average theory" yields when it is made to face NCBI data: **a measured decoupling, not a louder assertion.**

This is the biological sibling of the Cascade's geophysical result. The Cascade showed a recent-sequence relaxation is *physically permitted, occurrence-open*; this volume shows the recent-sequence biology reads as *one material kind per pair, with the clock decoupled from that material* — and likewise leaves occurrence open.

---

## 7. Graded predictions (falsifiable, forward)

Stated so they can fail. None promotes an [O] occurrence claim.

- **DP1 — two-kind material partition generalises [L].** Read any further orthologous gene set across these six taxa (or add taxa within each kind): the per-gene material should keep partitioning the two kinds with within-kind spread ≪ between-kind gap. *Fails if* a gene shows within-kind spread comparable to the between-kind gap on long (>1 kb) windows.
- **DP2 — decoupling holds out-of-sample [L].** On new gene-pairs (other clades, other loci), r(substitutions, |Δγ|) should stay ≈ 0 on length-matched windows. *Fails if* substitution count predicts |Δγ| (|r| ≳ 0.5) on a clean, length-controlled sample.
- **DP3 — adaptation is STATE-localised [L].** Other known adaptive differences between a "past" and "present" member of a kind should read as a *small, localised* set of coding/state changes on a materially conserved locus, not a global γ shift. *Fails if* a documented within-kind adaptation requires a kind-scale γ change.
- **DP4 — bistable states recur [L].** Where a phenotype is switch-like (coat colour, etc.), the alternative states should read as two settings of one R19 bistable (small |Δγ|, localised coding changes), occasionally both present in one kind. *Fails if* such alternatives demand materially distinct loci.
- **DP5 — long-window convergence [F-leaning].** As read-window length grows, within-kind γ-range should fall toward the inherited < 0.0016 promoter scale. *Fails if* long windows retain inflated within-kind range.
- **Occurrence (flood / deep-time descent): [O], both directions.** No reading here can promote either; the decision is reserved for independent evidence, exactly as in the Cascade.

---

## 8. Reproducibility

Nothing above rests on assertion. The whole spine runs from frozen NCBI records with no network and no tuning:

```bash
cd repro && python3 run_all.py        # -> results/RESULTS.txt ; figures/fig_dna_emergence.png
```

The six steps (extract → H1 → H2 → H3 → window-honesty → figure) regenerate every number in this document. `REPRODUCIBILITY_MAP.md` maps each claim to its script and its NCBI accession; `repro/data/accessions.json` freezes the accessions, and `repro/fetch_ncbi.py` re-fetches them live on demand. The material engine is `repro/vp_gamma_engine.py` (SantaLucia 1998 LOCK, no fitted constant). The figure (`figures/fig_dna_emergence.png`) shows the three reads: the two-kind partition (A), the channel decoupling (B), and the STATE face (C).

---

*This volume inherits a present-tense material instrument that is silent on evolution by construction, feeds it real genomes, and reports what it measures: the two kinds partition in the material, the molecular clock is decoupled from the material, and adaptive difference is a localized switch state. It claims a measured decoupling — not a history. The flood and the deep-time descent both stay open, by design.*
