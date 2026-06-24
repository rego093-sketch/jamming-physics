# REPRODUCIBILITY MAP — VP Recent-Sequence DNA Emergence

Every load-bearing claim maps to one of: a **runnable script in this package** (SEED-fixed, no tuning, run from frozen NCBI records), or a **real, fetchable NCBI accession**. Record-only items (any descent tree, calibrated clock, or absolute date) are excluded from load-bearing claims by the firewall (GOVERNANCE Art. 2–3).

Legend: **[pkg]** = script in this package · **[ncbi]** = fetchable NCBI accession · **[lit]** = literature cross-reference used only to *confirm* a read · **[O]** = open (no reproduction can promote it; firewall / occurrence cap).

---

## A. The inherited instrument — §1 of the whitepaper

| Claim | Grade | Reproduction path |
|---|---|---|
| Material engine γ = −mean(NN ΔG), R19 spinodal/barrier from γ alone, no fitted constant | [V] | **[pkg]** `repro/vp_gamma_engine.py` (SantaLucia 1998 LOCK; `python3 vp_gamma_engine.py` self-test) |
| Engine reproduces the inherited method + archaic/modern precedent (per-gene γ < 0.0016) | [V] | **[pkg]** Module 01 · inherited method **DOI 10.5281/zenodo.20471407**; precedent **DOI 10.5281/zenodo.20756155** |
| The instrument is evolution-silent / phylogeny-out-of-scope (a property, not an added assumption) | (posture) | inherited method DOI 10.5281/zenodo.20471407 (its own scope statement) |

## B. Emergence I — two-kind material partition (H1) — §2

| Claim | Grade | Reproduction path |
|---|---|---|
| 13 orthologous mito CDS extracted from all six real mitogenomes | [V] | **[pkg]** `repro/extract_orthologs.py` → `results/orthologs.json` · **[ncbi]** NC_007596.2, NC_005129.2, NC_000934.1, NC_012920.1, KC879692.1, FN673705.1 |
| **13/13 genes**: every Elephantidae γ strictly below every Homo γ (clean per-gene gap) | [V] | **[pkg]** `repro/bimodality.py` |
| Between-kind gap / within-kind spread: **median 17×** (range 4×–28×) | [V] | **[pkg]** `repro/bimodality.py` |
| Global mean γ ≈ 1.2887 lies between band centres (1.2545 / 1.3229); per-gene midpoint matches no kind | [V] | **[pkg]** `repro/bimodality.py` |
| **Pooled** γ is NOT bimodal (honest: only the per-gene partition is clean) | [V]/honest | **[pkg]** `repro/bimodality.py` (HONEST NOTE block) |
| Any past history producing the two kinds | **[O]** | — (occurrence cap, both directions) |

## C. Emergence II — clock/material decoupling (H2, core) — §3

| Claim | Grade | Reproduction path |
|---|---|---|
| Two channels read on the same 78 within-clade gene-pairs (|Δγ| vs substitution count) | [V] | **[pkg]** `repro/compare_channels.py` → `results/channel_records.json` |
| **r(substitutions, |Δγ|) = −0.081 ≈ 0** (n = 78): the channels are decoupled | [V] | **[pkg]** `repro/compare_channels.py` |
| 2656 substitutions vs mean |Δγ| 0.0057 on scale 1.29; ~0.00017 γ per substitution | [V] | **[pkg]** `repro/compare_channels.py` |
| Examples: COX2 33 subs / |Δγ| 0.0001; ATP8 5 subs / |Δγ| 0.0144 | [V] | **[pkg]** `repro/compare_channels.py` (per-pair table) |
| Therefore the clock cannot be promoted to a material / age statement | [F] (from H2) | follows from the decoupling + GOVERNANCE Art. 2.2 / 3 |
| The clock instead supports a flood (or any specific history) | **[O]** | — (decoupling demotes the clock; it does not elevate any alternative) |

## D. Emergence III — STATE face (H3) — §4

| Claim | Grade | Reproduction path |
|---|---|---|
| HBB/D material γ conserved across mammoth/Asian/African (range 0.0052) | [V] | **[pkg]** `repro/state_face.py` · **[ncbi]** FJ716094.1, FJ716086.1, NM_001280882.1 |
| Mammoth-vs-Asian HBB/D = 4 nt → **3 AA: A13T, S87A, Q102E** (recovers Campbell 2010) | [V]+[lit] | **[pkg]** `repro/state_face.py` · **[lit]** Campbell et al. 2010 |
| MC1R material γ conserved (range 0.0023); two mammoth haplotypes = one R19 bistable, both states present | [V] | **[pkg]** `repro/state_face.py` · **[ncbi]** DQ648860.1, DQ648859.1, DQ648866.1 |
| Mammoth hap1-vs-hap2 = 3 nt → **3 AA: T21A, R67C, R301S**, |Δγ| = 0.0019 (recovers Rømpler 2006) | [V]+[lit] | **[pkg]** `repro/state_face.py` · **[lit]** Rømpler et al. 2006 |
| Adaptive difference is a localized switch STATE, not a material shift | [V] | **[pkg]** `repro/state_face.py` (γ conserved + AA-localised) |

## E. Instrument honesty — window length — §5

| Claim | Grade | Reproduction path |
|---|---|---|
| **r(gene length, within-kind γ-range) = −0.56**; short windows noisiest | [V] | **[pkg]** `repro/length_effect.py` |
| Long windows recover the < 0.0016 scale (ND5 0.0068, COX1 0.0014) | [V] | **[pkg]** `repro/length_effect.py` |
| Within-kind γ-range inflation is a window-length artefact; bounds within-kind reads only | [V]/honest | **[pkg]** `repro/length_effect.py` (does NOT touch H1/H2) |

## F. Synthesis & standing — §6–7

| Claim | Grade | Path |
|---|---|---|
| Each pair reads as **one material kind** in the present tense | [V] | §B (per-gene partition) |
| The average theory's clock and the material are **different channels** | [V] | §C (r = −0.08) |
| Adaptive difference lives in **STATE** | [V] | §D |
| **Flood between the two animals** | **[O]** | occurrence cap, both directions |
| **Deep-time gradual descent between them** | **[O]** | occurrence cap, both directions |
| Forward predictions DP1–DP5 | [L]/[F-leaning] | §7; each is falsifiable, none promotes [O] |

---

## Integrity & verification status (this build)

- Whole spine reproduced in build environment: `repro/run_all.py` → `results/RESULTS.txt` (285 lines) + `figures/fig_dna_emergence.png`, **no network, no tuning**.
- Material engine self-test: `repro/vp_gamma_engine.py` runs clean (deterministic γ).
- All 12 NCBI accessions frozen under `repro/data/` (6 mitogenomes + 6 nuclear loci); `repro/fetch_ncbi.py` re-fetches them live.
- Inherited method + precedent: DOI 10.5281/zenodo.20471407 (engine) · DOI 10.5281/zenodo.20756155 (archaic/modern < 0.0016).

## External-verification checklist

1. `python3 repro/vp_gamma_engine.py` → prints a deterministic γ (instrument intact, no fitted constant).
2. `python3 repro/run_all.py` → regenerates every number in the whitepaper into `results/RESULTS.txt`.
3. Confirm **H1**: `bimodality.py` reports 13/13 clean per-gene partition AND the honest pooled-non-bimodality note.
4. Confirm **H2**: `compare_channels.py` reports r(subs, |Δγ|) = −0.08 over n = 78 pairs.
5. Confirm **H3**: `state_face.py` recovers A13T/S87A/Q102E (HBB/D) and T21A/R67C/R301S (MC1R) on materially conserved loci.
6. Confirm the honest **window-length** result: `length_effect.py` reports r ≈ −0.56 and the long-window recovery.
7. Re-fetch any accession with `repro/fetch_ncbi.py` and re-run — results should be bit-for-bit (SantaLucia LOCK, SEED = 19).
8. Confirm no absolute date / tree / calibrated clock is used as a premise anywhere in the load-bearing path (firewall, GOVERNANCE Art. 2–3).

---

*Nothing in the load-bearing path rests on assertion, on a tree, or on a clock-as-age. Every grade above traces to a script in this package run over a real NCBI accession — and every past-history claim, in both directions, is held open by construction.*
