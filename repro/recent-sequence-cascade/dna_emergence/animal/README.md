# VP Recent-Sequence DNA Emergence — package README

**Reading real NCBI genomes through the inherited material engine — a present-tense, material reading that doubts the average theory.**
The biological / DNA sibling of the VP Recent-Sequence **Cascade**, built on the VP foundation and the inherited VP **DNA interpretation method**, with a fully reproducible spine that runs from frozen NCBI records.

- **Author:** Young Jae Lee · **ORCID** 0009-0002-7535-8245
- **License:** CC BY 4.0 · **Site:** https://jamming-physics.org/
- **Foundations inherited:** VP physics **DOI 10.5281/zenodo.17932566** · Atlantic-opening geodynamics **DOI 10.5281/zenodo.17978934** · VP **DNA interpretation method DOI 10.5281/zenodo.20471407** · archaic/modern aging-promoter precedent **DOI 10.5281/zenodo.20756155**

---

## What this is (and is not)

This package presents one question, built out in full on real data and graded honestly:

> **When the same genes of "a past animal and a present animal" (mammoth/elephant; Neanderthal/modern human) are read through the inherited material engine, what does the material say — and is the molecular clock the same channel as the material, or a different one?**

It **is**: an application of a *fixed, inherited, no-tuning* instrument — the VP DNA material reading, which is **evolution-silent by construction** — to **real, fetchable NCBI genomes**, producing three reproducible reads (a two-kind material partition, a clock/material decoupling, and a STATE-face result) with a closing synthesis and five falsifiable predictions.

It **is not**: a claim that any particular history occurred. Under the governing constitution, **every past-history statement — a flood between the two animals *or* a deep-time gradual descent between them — is capped at [O] (open), in both directions.** The central result is *not* a chronology; it is the measured fact that the average theory's clock and the material are **different channels** (r ≈ 0). That is what "doubt the average theory" looks like when it faces data.

---

## Governance (why the grades can be trusted)

Built under the VP-SPEC constitution, the same discipline as the inherited volumes (full text in `GOVERNANCE.md`):

- **No-tuning.** The material engine's only constants are the inherited SantaLucia (1998) LOCK table; γ and the R19 thresholds derive from it with no fitted parameter (SEED = 19).
- **Inherited-instrument integrity.** The DNA reading is **not re-tuned here** — it is vendored faithfully from the inherited method and reproduces its archaic/modern precedent (per-gene γ < 0.0016).
- **Graded verdicts.** **[F]** forced/derived · **[V]** verified (measured on a real accession / engine-reproduced) · **[L]** leaning · **[O]** open. Precedence forced > verified > leaning > open; nothing launders an [O] history claim upward.
- **Bidirectional chronology firewall.** Past history is capped at **[O]** in *both* directions; the decoupling result demotes the *clock* as a history instrument **without** elevating any alternative history (GOVERNANCE Art. 2.2).
- **Single substrate.** One engine — the R19 jammed ⇄ unjammed bistable switch — underlies every read (γ sets its threshold; the STATE face is the switch in two settings; MC1R is caught in both states).
- **반증 = 발견.** Two honest negatives — the *pooled* γ is **not** bimodal (only the per-gene partition is clean), and within-kind γ-range is inflated by a **window-length artefact** — are recorded openly and bounded, not hidden.

---

## Reproducibility status (verified in-environment)

Nothing here rests on assertion; the load-bearing spine reproduces from code over frozen NCBI records, with no network and no tuning.

| Component | Status |
|---|---|
| Material engine self-test (`repro/vp_gamma_engine.py`) | runs clean (deterministic γ, no fitted constant) |
| Whole spine (`repro/run_all.py`) | regenerates `results/RESULTS.txt` (285 lines) + the figure |
| H1 two-kind partition (`repro/bimodality.py`) | **13/13** clean per-gene gap; median **17×** separation; honest pooled-non-bimodality noted |
| H2 clock/material decoupling (`repro/compare_channels.py`) | **r = −0.08** over **n = 78** gene-pairs |
| H3 STATE face (`repro/state_face.py`) | recovers Campbell 2010 (A13T,S87A,Q102E) + Rømpler 2006 (T21A,R67C,R301S) |
| Window-length honesty (`repro/length_effect.py`) | **r = −0.56** (length vs γ-range); long windows recover < 0.0016 |
| NCBI accessions | 12 frozen under `repro/data/`; re-fetchable via `repro/fetch_ncbi.py` |

---

## Package contents

```
vp_recent_sequence_dna_emergence/
├── README.md                         ← this file
├── WHITEPAPER.md                     ← the unified DNA-emergence argument (read this first)
├── GOVERNANCE.md                     ← constitution: bidirectional firewall, grading, no-tuning, [O] cap
├── REPRODUCIBILITY_MAP.md            ← every claim → script → NCBI accession → grade
├── MANIFEST.sha256                   ← hash-chain over all files (SEED=19, 2×SHA-256)
├── modules/                          ← the detailed governed record, step by step
│   ├── 01_inheritance_dna_reading_confirmed.md
│   ├── 02_material_partition_two_kinds.md
│   ├── 03_clock_material_decoupling.md
│   ├── 04_state_face_adaptive_switches.md
│   ├── 05_length_effect_instrument_honesty.md
│   ├── 06_synthesis_and_chronology_firewall.md
│   └── 07_open_items_and_forward_experiments.md
├── repro/                            ← the reproducibility spine (runs from frozen NCBI data)
│   ├── vp_gamma_engine.py            ← inherited material engine (SantaLucia 1998 LOCK, no tuning)
│   ├── extract_orthologs.py          ← data/mito/*.gb → results/orthologs.json
│   ├── bimodality.py                 ← H1 two-kind partition
│   ├── compare_channels.py           ← H2 clock/material decoupling → results/channel_records.json
│   ├── state_face.py                 ← H3 STATE face (nuclear adaptive loci)
│   ├── length_effect.py              ← window-length honesty
│   ├── make_figure.py                ← figures/fig_dna_emergence.png
│   ├── run_all.py                    ← orchestrator → results/RESULTS.txt
│   ├── fetch_ncbi.py                 ← optional live re-fetch from NCBI
│   └── data/
│       ├── accessions.json           ← all 12 accessions + provenance
│       ├── mito/                     ← 6 frozen mitogenomes (.gb)
│       └── nuc/                      ← 6 frozen nuclear loci (.gb)
├── results/
│   ├── orthologs.json                ← extracted 13 orthologous CDS × 6 taxa
│   ├── channel_records.json          ← 78 gene-pairs, both channels
│   └── RESULTS.txt                   ← full console report of the spine
└── figures/
    └── fig_dna_emergence.png         ← A: two-kind partition · B: decoupling · C: STATE face
```

---

## How to verify in five minutes

```bash
# 1. the instrument is intact (deterministic γ, no fitted constant)
cd repro && python3 vp_gamma_engine.py

# 2. the whole spine reproduces from frozen NCBI records (no network, no tuning)
python3 run_all.py                 # → results/RESULTS.txt ; figures/fig_dna_emergence.png

# 3. (optional) re-fetch the real accessions live and re-run
python3 fetch_ncbi.py && python3 run_all.py
```

Read order: **WHITEPAPER.md** → **REPRODUCIBILITY_MAP.md** → **modules/** (for the step-by-step governed reading and every honest qualification).

---

*This package feeds a fixed, evolution-silent material instrument with real genomes and reports what it measures: the two kinds partition in the material, the molecular clock is decoupled from the material, and adaptive difference is a localized switch state. It claims a measured decoupling — not a history. The flood and the deep-time descent both stay open, by design.*
