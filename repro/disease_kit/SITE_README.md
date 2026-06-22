# VP Disease Kit — static site (build artifact)

**From a Single Bistable Switch to a Falsifiable Corrective Direction: the VP Disease Emergence Kit**

This `docs/` tree is a deterministic, canonical, multi-page HTML rendering of the VP Disease
Emergence Kit, built to VP-SPEC v1.8 (Constitution C1/C2/C4). It is generated entirely from the
kit's pinned JSON outputs and contains **no invented numbers**.

## The one thing to understand
Every disease page offers a **theoretical corrective direction to experts for evaluation** — it is
**never a prescription**. There is **no dose anywhere**. An English-language safety firewall is
repeated **three times** on each disease page: a top banner, a banner beside the agent names, and a
bottom banner that explains *why* no dose is given (unvalidated; to be set by a licensed physician or
national authority; not an approved method). A short inline notice also rides on every candidate card.

## Contents
- `839` rare-disease pages under `docs/disease/dz/<slug>/index.html`
- 6 front-matter chapters under `docs/disease/<NN-slug>/index.html`
- A–Z disease indexes under `docs/disease/index-<X>/index.html`
- Contents hub `docs/disease/index.html`; site landing `docs/index.html`
- `sitemap.xml`, `robots.txt` (7 retrieval bots allowed), `llms.txt`, `docs/disease/_meta.json`

## Headline results
- Recover an existing standard (MATCH): **322**  ·  Novel direction-only (NOVEL): **29**  ·  Honest holds (HOLD): **488**
- Surfaced candidate rows: **233** (147 rediscoveries, 86 novel)

## Build / reproduce
```
python3 tools/build_disease_site.py
```
Deterministic: same inputs → same bytes (SEED-fixed, 2× SHA-256 hash chain).
Register chain-head: `fc8598ec13f74a9e` · release `0.42.1-trackA.merged_3of3`.

## Inputs (read-only)
`outputs/actionability_index.json`, `outputs/mapped_levers.json`,
`outputs/surfaced_candidates.json`, `outputs/candidate_register.json`.

Author: Young Jae Lee (ORCID 0009-0002-7535-8245) · License: CC BY 4.0 · DOI: 10.5281/zenodo.20755262
Reproduction code: https://github.com/rego093-sketch/jamming-physics/tree/main/repro/disease
