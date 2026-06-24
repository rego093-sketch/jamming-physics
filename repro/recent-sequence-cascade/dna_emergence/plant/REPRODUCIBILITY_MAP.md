# REPRODUCIBILITY MAP — VP Plant Environment DNA Emergence

Every load-bearing claim maps to a **runnable script in this package** (SEED-fixed, no tuning, run from frozen NCBI records) or a **real, fetchable NCBI accession**. Record-only items (trees, calibrated clocks, dates) are excluded from load-bearing claims by the firewall (GOVERNANCE Art. 2–3).

Legend: **[pkg]** = script in this package · **[ncbi]** = fetchable NCBI accession · **[lit]** = annotation/literature label only · **[O]** = open (firewall / occurrence cap).

---

## A. The inherited instrument — §1

| Claim | Grade | Reproduction path |
|---|---|---|
| Material engine γ = −mean(NN ΔG), R19 scale from γ, no fitted constant | [V] | **[pkg]** `repro/vp_gamma_engine.py` (SantaLucia 1998 LOCK; self-test) |
| Instrument is evolution-/phylogeny-silent (a property, not an added assumption) | (posture) | inherited method **DOI 10.5281/zenodo.20471407** |

## B. Emergence I — plastid material conserved across kinds (H1′) — §2

| Claim | Grade | Reproduction path |
|---|---|---|
| 62 orthologous plastid CDS extracted from all six real plastomes | [V] | **[pkg]** `repro/plastid_partition.py` → `results/plastid_orthologs.json` · **[ncbi]** NC_001320.1, NC_001666.2, NC_002762.1, NC_001879.2, NC_007898.3, NC_008096.2 |
| Grass and nightshade band centres nearly coincide (1.2821 vs 1.2809, |diff| 0.0012) | [V] | **[pkg]** `repro/plastid_partition.py` |
| Weak partition (median 2.69×) — strong two-kind partition NOT present (cf. animal ~17×) | [V]/honest | **[pkg]** `repro/plastid_partition.py` |
| rbcL γ range across six habitats = 0.0082 (one gene, nearly identical) | [V] | **[pkg]** `repro/plastid_partition.py` |
| Any past history producing the kinds | **[O]** | — (occurrence cap, both directions) |

## C. Emergence II — clock/material decoupling (H2) — §3

| Claim | Grade | Reproduction path |
|---|---|---|
| Two channels on 372 within-kind gene-pairs (|Δγ| vs substitutions) | [V] | **[pkg]** `repro/clock_decoupling.py` → `results/plant_channel_records.json` |
| **r(substitutions, |Δγ|) = +0.089 ≈ 0** (n = 372, 9245 substitutions) | [V] | **[pkg]** `repro/clock_decoupling.py` |
| Clock cannot be promoted to a material / age claim | [F] (from H2) | follows from the decoupling + GOVERNANCE Art. 2–3 |

## D. Emergence III — cold-vs-UV STATE face (H3) — §4

| Claim | Grade | Reproduction path |
|---|---|---|
| Cold switch (CBF/DREB1) and UV switch (CHS, UVR8) are different loci (inventory) | [V]+[lit] | **[pkg]** `repro/state_face_cold_uv.py` · **[ncbi]** NM_118680.2, NM_118678.1, NM_118679.2, NM_121396.4, NM_125594.1 |
| CHS γ tracks LINEAGE not environment: cold barley (1.596) & warm maize (1.645) both high; dicots ~1.31–1.45 any habitat | [V] | **[pkg]** `repro/state_face_cold_uv.py` · **[ncbi]** X58339.1, X60204.1, X75969.1, X03710.1, OQ458726.1, NM_121396.4 |
| Within Arabidopsis, cold & UV switch genes share material scale (1.352–1.437) | [V] | **[pkg]** `repro/state_face_cold_uv.py` |
| The environment writes to STATE/inventory/dwell, not the material | [V] | **[pkg]** `repro/state_face_cold_uv.py` (the three reads together) |
| "Any cold gene = any UV gene" | **refused** | honest caveat: cross-lineage CHS varies (composition-driven) |

## E. Composition honesty — §5

| Claim | Grade | Reproduction path |
|---|---|---|
| **r(γ, GC) = 0.979** (plastid, n=372); **0.998** (CHS across 6 species) | [V] | **[pkg]** `repro/length_composition.py` |
| γ is a composition measure → a lineage property the environment cannot rewrite | [V] | **[pkg]** `repro/length_composition.py` |

## F. Synthesis & standing — §6–7

| Claim | Grade | Path |
|---|---|---|
| Core plant material conserved across very different plants | [V] | §B |
| Clock and material are different channels (plants too) | [V] | §C |
| Cold-vs-UV adaptation lives in STATE/inventory/dwell | [V] | §D |
| Any "past environment" / history | **[O]** | occurrence cap, both directions |
| Forward predictions DP1–DP5 | [L]/[F-leaning] | §7; each falsifiable, none promotes [O] |

---

## Integrity & verification status (this build)

- Whole spine reproduced in build environment: `repro/run_all.py` → `results/RESULTS.txt` + `figures/fig_plant_emergence.png`, **no network, no tuning**.
- Material engine self-test: `repro/vp_gamma_engine.py` runs clean.
- 16 NCBI accessions frozen under `repro/data/` (6 plastomes + 10 stress loci); `repro/fetch_ncbi.py` re-fetches them.
- Inherited method: DOI 10.5281/zenodo.20471407.

## External-verification checklist

1. `python3 repro/vp_gamma_engine.py` → deterministic γ (instrument intact).
2. `python3 repro/run_all.py` → regenerates every number in the whitepaper.
3. Confirm **H1′**: plastid band centres coincide (1.2821 vs 1.2809); partition weak (2.69×).
4. Confirm **H2**: r(subs, |Δγ|) = +0.09, n = 372.
5. Confirm **H3**: CHS γ — barley & maize high (grasses), dicots lower regardless of habitat.
6. Confirm the composition link: r(γ, GC) = 0.979 / 0.998.
7. Re-fetch any accession with `repro/fetch_ncbi.py` and re-run — bit-for-bit (LOCK, SEED = 19).
8. Confirm no absolute date / tree / calibrated clock is a premise anywhere (firewall).

---

*Every grade above traces to a script in this package run over a real NCBI accession. The environment is shown to act on STATE, not on the material; every past-environment / history claim is held open by construction.*
