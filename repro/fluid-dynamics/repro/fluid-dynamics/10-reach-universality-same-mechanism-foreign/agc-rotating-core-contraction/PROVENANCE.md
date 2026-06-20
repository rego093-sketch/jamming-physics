# Provenance — AGC: anomalous geometric contraction of hyper-rotating cores
# (§10 Reach and universality — foreign-domain exhibit)

This folder is folded in from the author's standalone package `AGC_DOI_v3`
for the manuscript

> "Anomalous Geometric Contraction of Hyper-Rotating Cores via Shockwave
>  Confinement in High-Density Stiff Media"  (Young Jae Lee, 2025-11-24)

(former standalone reproducibility package; not registered as a separate
paper). Keywords: compressible Euler, HLLC, Tait EOS, shock confinement,
anomalous geometric contraction, negative centrifugal effect.

## Why it sits under §10 (reach / same mechanism in foreign domains)

The whitepaper's rotation-arrangement thesis (rotation forces structure, §4;
geometric arrangement fixes length, §7) is here exercised in a *foreign
domain*: a hyper-rotating core inside a shock-confined, high-density stiff
medium (water / Tait EOS vs air / ideal gas). The result is an **anomalous
geometric contraction** — shock confinement turns the usual centrifugal
expansion into a net inward (negative-centrifugal) contraction. That is a
reach exhibit of the same arrangement mechanism, which is what §10 collects.

This phenomenon is **not covered anywhere else** in the whitepaper (Tait EOS,
HLLC, negative-centrifugal, stiff-media contraction were all absent), so this
fills a genuine gap rather than duplicating existing content.

## Contents
- `src/solver/euler2d_solver_template.py` — Euler–HLLC solver template.
- `cases/` — verification cases (shocktube, cylinder air M2) and the main
  water M1.5/α1 case.
- `data/processed_for_figures/`, `data/tables/`, `data/verification/`,
  `data/sensitivity/`, `data/toy_model/` — per-figure / per-table CSVs.
- `figures_v2/`, `figures_v3/` — grid-convergence and toy-contraction figures.
- `docs/ReproGuide.md`, `docs/Analogues_ExtremePhysics.md` — reproduction +
  analogue notes. `metadata/figure_table_mapping.json` — case↔data↔figure map.

## Status note (the solver is a TEMPLATE)
Per the package README, `src/solver/euler2d_solver_template.py` is a
*template*; the heavy water/Tait-EOS runs were produced by the author's own
code and are represented here by the processed CSVs + figures. The bundled
v3 additions (ideal-gas grid-convergence, 0D toy contraction model) are
self-contained sanity checks, not the full FSI simulation.

## Editorial hook (author action — see MERGE_NOTE)
This is staged as ready reproduction evidence. To make it a *cited* reach
example, add one sentence in §10 body (or a dedicated appendix) pointing to
this folder. That edit touches word-count-gated body text, so it is left as
the author's editorial decision; the §10 claim-strip already deep-links to
this section's repro folder, so the link path is valid as soon as prose
references it.
