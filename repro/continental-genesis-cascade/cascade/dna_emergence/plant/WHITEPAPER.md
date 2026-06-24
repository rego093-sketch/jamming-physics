# The VP Plant Environment DNA Emergence
### Reading real NCBI plant genomes through the inherited material engine — the material is a *lineage* property, the environment writes only to STATE

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245
**License:** CC BY 4.0 · **Site:** https://jamming-physics.org/
**Inherits:** VP physics foundation (DOI 10.5281/zenodo.17932566) · **VP DNA interpretation method** (DOI 10.5281/zenodo.20471407)
**Sibling of:** the VP Recent-Sequence **DNA Emergence** (animals: mammoth/elephant, Neanderthal/human) and the **Cascade** (geophysics). This is the **plant** face of the same material reading.
**Governance:** VP-SPEC — no-tuning · LOCK→Derive→Gate · graded verdicts [F]/[V]/[L]/[O] · **bidirectional chronology firewall** · single-substrate (R19 bistable switch).

---

## How to read this document

The question, posed in the user's words:

> **A plant grown in a past cold (greenhouse) environment and one grown under a UV environment — will their genes be similar, even though they look different?**

In VP terms this is a precise, testable claim about *where the environment acts*. The inherited DNA method reads any locus into a **material** channel — **γ = −mean(NN stacking ΔG)** — and its central thesis is that the environment sets the **STATE / inventory / dwell**, not the readable material. So the prediction is: **the environment does not rewrite the material; appearance (phenotype) and habitat live in STATE.**

We tested this on **real NCBI plant genomes** and the answer is *yes, in a precise and slightly refined form*: **the readable gene material (γ) is a property of the LINEAGE/KIND, not of the environment.** Two plants in different habitats, with different appearances, share conserved core gene material; the environment changes which switch is deployed and how strongly, never the material itself. The instrument is fixed and inherited (it is **silent on evolution by construction**); we only fed it plants.

**The governing firewall.** As in the sibling volumes, any statement about a **past occurrence** (a "past cold greenhouse," a flood, a deep-time descent) is capped at **[O] (open)** in both directions. The claims graded **[F]/[V]** are *present-tense material measurements*; **[O]** is reserved for history.

---

## 1. The inherited instrument (fixed, not tuned)

The material engine is vendored faithfully from the inherited method (`repro/vp_gamma_engine.py`): **γ = −mean(NN stacking ΔG)** over the SantaLucia (1998) nearest-neighbour LOCK table, strand-symmetric, bit-for-bit, with the locus's **R19 bistable switch** scale derived from γ alone. **Nothing is fitted.** The method reads *present-tense material* and is explicitly evolution-/phylogeny-silent — exactly the property that lets it test *where the environment writes* without smuggling in a descent model. We do not modify the instrument; we apply it to real plants.

*Grade: instrument inherited and reproduced [V].*

---

## 2. Emergence I — plant plastid material is conserved *across* kinds (H1′)

We fetched **six real plastid genomes** — three grasses (rice NC_001320.1, maize NC_001666.2, wheat NC_002762.1) and three nightshades (tobacco NC_001879.2, tomato NC_007898.3, potato NC_008096.2) — extracted the **62 orthologous protein-coding genes** present in all six, and read each through the material engine (`repro/plastid_partition.py`).

**Result, and an honest contrast with animals.** In the animal volume, mtDNA γ *partitioned* the two kinds cleanly (median 17× separation; band centres ~0.07 apart). **In plants the plastid material does the opposite: it is conserved across the two kinds.**

- The grass and nightshade **band centres nearly coincide**: γ ≈ **1.2821** (grasses) vs **1.2809** (nightshades) — a difference of only **0.0012**.
- The per-gene separation ratio is weak (**median 2.69×** vs ~17× for animals); the 44/62 "clean" per-gene gaps are tiny and do not point consistently one way (which is why the centres coincide).
- **rbcL** — the gene that builds the carbon-fixing enzyme — reads γ ≈ 1.334–1.343 across all six wildly different plants in different habitats: a range of just **0.0082** for one gene across six species.

**Honest finding (반증 = 발견).** The clean two-kind partition seen in animal mtDNA **does not reproduce** in plant plastid genes — the photosynthesis machinery is *universally conserved*. This is a real difference between the kingdoms, recorded openly. And it supports the user's intuition even more strongly than a partition would: **very different-looking plants in different habitats share the same core gene material.**

*Grade: plastid material conserved within and across kinds [V]; the strong two-kind partition is explicitly NOT claimed for plants (it holds for animal mtDNA, not here).*

---

## 3. Emergence II — the clock and the material are decoupled in plants too (H2)

On the same plastid genes, within each kind, across **all 372 within-kind gene-pairs**, we read both channels (`repro/clock_decoupling.py`): |Δγ| (material) and substitution count (the molecular clock — the average theory's deep-time axis).

**Result [V].** **Pearson r(substitutions, |Δγ|) = +0.089 ≈ 0.** The clock counts **9245 substitutions** in total; γ moves a mean of only **0.0058** on the ~1.28 scale, and not in proportion. The molecular clock and the material are **different physical channels** — the same result the animal volume found, now reproduced in an independent kingdom. A clock distance cannot be promoted to a material or age statement here either.

*Grade: clock/material decoupling [V] (r = +0.09, n = 372). Independent-kingdom confirmation of the animal result.*

---

## 4. Emergence III — the cold-vs-UV STATE face: the environment does not write the material (H3)

This is the user's hypothesis, tested directly on **real cold- and UV-response genes** (`repro/state_face_cold_uv.py`). Three reads:

**(1) Inventory — the cold switch and the UV switch are different loci.** The cold-acclimation master switch is the **CBF/DREB1** family; the UV-protection switch is **CHS** (chalcone synthase, the flavonoid/UV-screen gene) with **UVR8** as the UV-B sensor. These are **different genes**. The environment deploys a *different switch* (inventory/STATE) — cold → CBF, UV → CHS/UVR8 — not a different material. (Arabidopsis CBF1/2/3 read γ ≈ 1.368–1.425; CHS γ ≈ 1.437; UVR8 γ ≈ 1.352.)

**(2) The environment does not set the material; the lineage does.** We read CHS — the UV switch — across six species in contrasting habitats:

- **Grasses:** barley (a **cold** cereal) γ = **1.596**; maize (a **warm**, high-light C4 grass) γ = **1.645** — *both high.*
- **Dicots:** Arabidopsis (temperate) 1.437; grape (**high-UV**) 1.450; snapdragon 1.442; petunia 1.316 — *all lower, whatever the habitat.*

**The cold / warm / UV environment does not sort CHS γ.** A cold grass and a warm grass both read high *because both are grasses*; a high-UV dicot reads with the other dicots. **γ tracks the lineage, not the environment** — so the environment does **not** write the readable material. This is the honest, correct form of the user's hypothesis: *same lineage → same material, in any habitat.*

**(3) Within one lineage, the cold and UV switch genes share a material scale.** Within Arabidopsis the cold-switch and UV-switch genes span γ ≈ 1.352–1.437 — a single material scale; the cold-vs-UV difference is *which switch is deployed* plus localized coding, not a material shift.

**Verdict on the hypothesis.** *"Cold-environment and UV-environment plants have similar genes, even though they look different"* is **TRUE in the precise sense that the readable gene material (γ) is set by the LINEAGE/KIND, not by the environment.** The environment leaves the material unchanged and instead sets **which switch is on** (inventory) and **how much** (dwell/expression). "They look different" lives in STATE; "their genes are similar" lives in the lineage-conserved material.

**Honest caveat (stated, not hidden).** γ is a *composition* measure, so we do **not** claim "any cold gene ≈ any UV gene." Cross-lineage CHS γ varies substantially (grass vs dicot). The defensible claim is the directional one: **the environment does not rewrite the material.**

*Grade: STATE face [V] — cold and UV are different loci; γ is a lineage property; the environment writes to STATE/inventory/dwell, not the material.*

---

## 5. The honest instrument note — γ is a composition measure (and that is the point)

Why is γ a *lineage* property? Because **γ = −mean(NN ΔG) is a base-composition measure**: GC-rich windows stack harder and read higher γ. We show this directly (`repro/length_composition.py`):

- plastid genes pooled across all six taxa: **r(γ, GC) = 0.979**;
- CHS across six species: **r(γ, GC) = 0.998** (grass CHS GC ≈ 0.66–0.70 → high γ; petunia GC ≈ 0.42 → low γ).

A lineage's genome GC content sets its γ scale, and **GC content is heritable lineage architecture, not something the cold or UV environment rewrites.** This is *exactly why* the material is a lineage/kind signature and the environment cannot write to it. It also bounds the reading: compare γ **within** a lineage, or control GC, before reading a difference as material. The composition link is a feature, not a flaw — it is the mechanism behind "the environment does not write the material."

*Grade: γ↔GC composition link [V]; it explains and bounds the H1′/H3 readings.*

---

## 6. Synthesis — what the plant material says

1. **Plant plastid core material is conserved within and across kinds (H1′, [V]).** Very different-looking plants in different habitats share the same core gene material — the user's "겉모양 달라도 유전자 비슷" holds for the conserved core. (Honest: unlike animal mtDNA, plants show no strong two-kind partition.)
2. **The clock is decoupled from the material in plants too (H2, [V]).** Independent-kingdom confirmation that the average theory's deep-time axis is a different channel from the material.
3. **The cold-vs-UV difference is STATE/inventory, not material (H3, [V]).** The environment deploys a different switch (CBF vs CHS/UVR8) and sets its dwell; γ is a lineage property the environment does not rewrite.

**What this establishes — and does not.** On present-tense material grounds, the environment does **not** write the readable material; appearance and habitat live in STATE/inventory/dwell, and the material is conserved by lineage. This is the user's hypothesis, confirmed in its correct form. It says nothing about *history*: any "past environment" claim, like the flood and deep-time claims in the sibling volumes, stays **[O]** in both directions.

This is the plant sibling of the animal result. Animals: each "past/present" pair reads as one material kind, clock decoupled. Plants: the core material is conserved across kinds, the clock is likewise decoupled, and the cold-vs-UV environment writes to STATE, not material. Same engine, same firewall, independent kingdom.

---

## 7. Graded predictions (falsifiable, forward)

- **DP1 — environment-independence of γ generalises [L].** For any stress-response gene read across lineages, γ should track lineage GC, not the stress environment. *Fails if* an environmental axis (cold/UV/drought) sorts γ after GC is controlled.
- **DP2 — within-lineage material conservation [L].** Within one lineage, cold-switch and UV-switch genes should read on one material scale. *Fails if* they separate materially after GC control.
- **DP3 — inventory, not material, carries adaptation [L].** Cold vs UV adaptation should map to *which* loci are deployed (CBF vs CHS/UVR8) and their dwell, not to a γ shift of a shared locus. *Fails if* a shared locus shows a kind-scale γ change between cold- and UV-adapted lineages.
- **DP4 — clock decoupling holds out-of-sample [L].** On new plant gene-pairs, r(substitutions, |Δγ|) ≈ 0 on length-matched windows. *Fails if* substitution count predicts |Δγ| (|r| ≳ 0.5).
- **DP5 — γ↔GC composition link [F-leaning].** γ should remain a near-deterministic function of GC across plant loci. *Fails if* γ and GC decouple on clean coding windows.
- **Occurrence / "past environment": [O], both directions.** No reading promotes a history claim.

---

## 8. Reproducibility

The whole spine runs from frozen NCBI records, no network, no tuning:

```bash
cd repro && python3 run_all.py     # -> results/RESULTS.txt ; figures/fig_plant_emergence.png
```

The five steps (plastid partition → clock decoupling → cold-vs-UV STATE face → composition honesty → figure) regenerate every number here. `REPRODUCIBILITY_MAP.md` maps each claim to its script and NCBI accession; `repro/data/accessions.json` freezes the 16 accessions and `repro/fetch_ncbi.py` re-fetches them live. The figure shows the three reads: plastid conservation across kinds (A), clock/material decoupling (B), and CHS-γ-tracks-lineage-not-environment (C).

---

*This volume feeds a fixed, evolution-silent material instrument with real plant genomes and reports what it measures: the core material is conserved across very different plants, the molecular clock is a different channel, and the cold-vs-UV environment writes to STATE/inventory/dwell — not to the material, which is a lineage property. The user's hypothesis holds in its precise form. Any "past environment" stays open, by design.*
