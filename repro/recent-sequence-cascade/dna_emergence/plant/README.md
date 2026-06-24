# VP Plant Environment DNA Emergence — package README

**Reading real NCBI plant genomes through the inherited material engine: the readable material (γ) is a *lineage* property; the environment writes only to STATE.**
The plant sibling of the VP DNA-Emergence (animals) and Cascade (geophysics) volumes, built on the VP foundation and the inherited VP **DNA interpretation method**, with a fully reproducible spine that runs from frozen NCBI records.

- **Author:** Young Jae Lee · **ORCID** 0009-0002-7535-8245
- **License:** CC BY 4.0 · **Site:** https://jamming-physics.org/
- **Foundations inherited:** VP physics **DOI 10.5281/zenodo.17932566** · VP **DNA interpretation method DOI 10.5281/zenodo.20471407**

---

## The question (the user's words)

> **A plant grown in a past cold (greenhouse) environment and one grown under a UV environment — will their genes be similar, even though they look different?**

**Answer, from real data, in its precise form: yes.** The readable gene material (γ) is set by the **LINEAGE/KIND, not by the environment.** Two plants in different habitats with different appearances share conserved core gene material; the environment changes **which switch is deployed** (cold → CBF; UV → CHS/UVR8) and **how strongly** (dwell/expression) — never the material itself. "They look different" lives in STATE; "their genes are similar" lives in the lineage-conserved material.

The instrument is **fixed and inherited** (evolution-silent by construction); we only fed it real plants.

---

## What this is (and is not)

It **is**: an application of a *fixed, inherited, no-tuning, evolution-silent* instrument to **real NCBI plant genomes**, producing three reproducible reads — plastid material conserved across kinds, clock/material decoupling, and a cold-vs-UV STATE face — with an honest synthesis and five falsifiable predictions.

It **is not**: a claim that any past environment or history occurred. Every past-environment / history statement is capped at **[O] (open)**, both directions. It also does **not** claim "any cold gene = any UV gene" — γ is a composition measure, so that over-claim is explicitly refused; the defensible claim is directional: *the environment does not rewrite the material.*

---

## Governance (why the grades can be trusted)

Built under VP-SPEC (full text in `GOVERNANCE.md`):

- **No-tuning.** The engine's only constants are the inherited SantaLucia (1998) LOCK table; γ and the R19 thresholds derive from it with no fitted parameter (SEED = 19).
- **Inherited-instrument integrity.** The DNA reading is **not re-tuned here** — it is vendored faithfully from the inherited method.
- **Graded verdicts.** **[F]/[V]/[L]/[O]**; nothing launders an [O] history claim upward.
- **Bidirectional chronology firewall.** Past environment / history capped at **[O]** in both directions.
- **Single substrate.** One engine — the R19 jammed ⇄ unjammed bistable switch (γ sets its threshold; CBF/CHS/UVR8 are the inventory the environment deploys).
- **반증 = 발견.** Three honest findings recorded openly: the plant plastid material does **not** strongly partition the two kinds (unlike animal mtDNA); cross-lineage CHS γ varies (so "any cold = any UV gene" is refused); γ is a GC-composition measure (which is *why* it is a lineage property).

---

## Reproducibility status (verified in-environment)

| Component | Status |
|---|---|
| Material engine self-test (`repro/vp_gamma_engine.py`) | runs clean (deterministic γ, no fitted constant) |
| Whole spine (`repro/run_all.py`) | regenerates `results/RESULTS.txt` + the figure, no network, no tuning |
| H1′ plastid (`repro/plastid_partition.py`) | grass/nightshade band centres **1.2821 / 1.2809** (|diff| 0.0012); partition weak (2.69×) |
| H2 decoupling (`repro/clock_decoupling.py`) | **r = +0.09** over **n = 372** gene-pairs |
| H3 cold-vs-UV (`repro/state_face_cold_uv.py`) | CHS γ tracks lineage: cold barley 1.596 & warm maize 1.645 both high; dicots ~1.31–1.45 |
| Composition (`repro/length_composition.py`) | **r(γ, GC) = 0.979 / 0.998** |
| NCBI accessions | 16 frozen under `repro/data/`; re-fetchable via `repro/fetch_ncbi.py` |

---

## Package contents

```
vp_plant_environment_dna_emergence/
├── README.md                         ← this file
├── WHITEPAPER.md                     ← the unified argument (read this first)
├── GOVERNANCE.md                     ← constitution: firewall, grading, no-tuning, [O] cap
├── REPRODUCIBILITY_MAP.md            ← every claim → script → NCBI accession → grade
├── MANIFEST.sha256                   ← hash-chain over all files (SEED=19, 2×SHA-256)
├── modules/                          ← the governed record, step by step (01–06)
├── repro/                            ← the spine (runs from frozen NCBI data)
│   ├── vp_gamma_engine.py            ← inherited material engine (SantaLucia 1998 LOCK, no tuning)
│   ├── plastid_partition.py          ← H1′ plastid material across kinds
│   ├── clock_decoupling.py           ← H2 clock/material decoupling
│   ├── state_face_cold_uv.py         ← H3 the cold-vs-UV hypothesis
│   ├── length_composition.py         ← γ↔GC composition honesty
│   ├── make_figure.py                ← figures/fig_plant_emergence.png
│   ├── run_all.py                    ← orchestrator → results/RESULTS.txt
│   ├── fetch_ncbi.py                 ← optional live re-fetch
│   └── data/
│       ├── accessions.json           ← all 16 accessions + provenance
│       ├── plastid/                  ← 6 frozen plastomes (.gb)
│       └── stress/                   ← 10 frozen stress loci (.gb)
├── results/                          ← orthologs, channel records, RESULTS.txt
└── figures/                          ← fig_plant_emergence.png
```

---

## How to verify in five minutes

```bash
cd repro && python3 vp_gamma_engine.py     # 1. instrument intact (deterministic γ)
python3 run_all.py                          # 2. whole spine reproduces (no network, no tuning)
python3 fetch_ncbi.py && python3 run_all.py # 3. (optional) re-fetch live and re-run
```

Read order: **WHITEPAPER.md** → **REPRODUCIBILITY_MAP.md** → **modules/**.

---

*This package feeds a fixed, evolution-silent material instrument with real plant genomes and reports what it measures: very different plants share conserved core material, the molecular clock is a different channel, and the cold-vs-UV environment writes to STATE — not to the material, which is a lineage property. The user's hypothesis holds in its precise form. Any past environment stays open, by design.*
