# CHANGELOG — v1.15 · Appendix J (the order-grammar completion)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

This release is **strictly add-only**. Chapters §0–§13 and Appendices A–F, H, I — every prior page,
number, grade, equation, and DOI — are **unchanged**. One appendix is added to the multi-page site with
its own fail-closed reproduction package, and the section count rises from 24 to **25**.

The only edit to a prior page is **navigational**: Appendix I's prev/next bar gains a forward link to
Appendix J. No prior body text, claim, or number was altered (the gate's paragraph-completeness check is
unaffected).

## What was added

### Appendix J — The order-grammar COMPLETION: the kit, the clock, the drive, the gate
`docs/dna/ax-j-order-grammar-completion/` · `repro/dna/ax-j-order-grammar-completion/`

Appendix I identified the developmental ORDER grammar — *emergence order = toposort(regulatory cascade)
modulated by the local barrier γ²/4*, i.e. cascade **DEPTH**, the G3 wiring grammar read on the time axis —
and was **honest about four open obstacles**. Appendix J closes all four with **real data and no
retuning**, each only as far as the firewall permits:

- **O1 — gene-set fill.** The named dilutors are filled with **25 new real GRCh38 driver-γ** (7 limb FGF/Wnt
  inducers: WNT2B / ALDH1A2 / ISL1 / PITX1 / FGF10 / WNT3A / FGF8; 18 HOXA/HOXD collinear genes spanning the
  cluster, **not** the terminal group alone) and the pre-registered **0.70 floor is re-tested** under a
  nested-scope ablation: inherited 38-kit **0.475** (reproduces Appendix I) → + limb inducers **0.700** →
  + full HOX **0.755 (floor MET globally)** → HOX-only, limb-ablated **0.657 (below floor)**. ⇒ **both
  fixes are required**, the lift localised to the two named gaps. A ±1 rank-jitter test (seed = **19**, the
  R19 constant; 4000 draws) gives mean **0.694**, p5 **0.625** < floor ⇒ the floor is cleared by the cited
  ranks but **marginal at the lower edge of citation uncertainty**, so the strength claim is graded **`[L]`**
  (empirical, on cited anatomy) and is **never** promoted to `[V]`; the gate **fails closed** on any `[V]`
  upgrade.
- **O2 — absolute timing.** The real measured segmentation-clock period (**5.0 h**, Diaz-Cuadros 2020 /
  Matsuda 2020) × the cited somite count (**42 pairs**, O'Rahilly & Müller) predicts an **8.75 d**
  somitogenesis span, consistent ±2 d with the cited CS9–CS13 window → **`[L]`**. A single global
  zero-point pinning the whole atlas to absolute days needs a second measured anchor → left **`[O]`**.
- **O3 — sequence → drive.** Per-edge drive is read from the promoter as the R19 ON-branch amplitude
  **√γ** of the parent (a stiffer regulator delivers proportionally more drive) instead of a uniform W = 1;
  firing order is **preserved** (Spearman(uniform, sequence) = **0.988**, 0 wavefront violations) ⇒ a
  declared modelling choice **`[F]`** whose order-invariance is **`[V]`**.
- **GATE — quorum realisation.** The OR-gate wavefront generalises to a **quorum / AND threshold-k** gate
  (a gene fires once ≥ k_i = max(1, ⌈α·indegree⌉) regulators are ON); at full conjunction the cascade order
  still holds with **0 violations**, convergent nodes never fire earlier than under OR, and the OR-gate is
  exactly the **k = 1** special case → **`[V]`**.

**Gate:** `python3 -m completion.gate` PASS **16/16** (`sha=8f04f931d51d3526`); reading hash (2×SHA-256)
`5d366e7e405f367758a2dc7f18cdf5ce7debce2fcbc730ad5f73330eea63092b`; grades **V=10 L=3 F=1 O=2**;
`physical_complete=False`.

## Inheritance discipline (re-locked, byte-identical)

Appendix J inherits the substrate and parameters without retuning. **All 38 inherited driver-γ are
gate-checked digit-for-digit against the parent Appendix-I `param_db.json` read off disk** (`J1`, 0
mismatches) — a stronger inheritance check than the 4-driver byte-match of prior appendices. The four
skeletal drivers (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) are re-locked
byte-for-byte; the `(LEVEL, SHAPE) = (γ, A4=robust_z)` operator and `spinodal(γ) = 2·(γ/3)^1.5` are
character-identical across appendices. The README carries the binding **§INHERIT** section *and* a binding
**BLUEPRINT for 100% completion** (the path that would retire the remaining `[O]`: a second measured
absolute anchor for the global clock; a cis-code → drive map *derived* from sequence; broader cited
coverage to lift the jitter p5 above the floor; and the permanent statement that O1's absolute strength can
never become `[V]`). `inline_magic_numbers: 0`, including a provenance string on the floor-robustness seed.

## What this does NOT claim

The absolute-strength floor is **reached on the filled kit but `[L]`** (jitter-marginal), never a verified
invariant. The absolute developmental clock is **not** solved — the single global zero-point is `[O]`. The
cis-to-drive map is a declared choice `[F]`, not derived from sequence. No body is built or simulated;
`physical_complete=False`. The honest jitter fragility and the open zero-point are **disclosed, not
hidden** — *반증을 메우니 발견이 선다.*

## Note on Appendix G

Appendix G (skeletal/limb) is a sibling volume of the broader program and is **not bundled in this site
export**; it is referenced only as the source of the four byte-identical driver-γ values. Its absence is
why the site's appendix lettering reads A–F, H, I, J.

## Gate

`python3 gate_multipage.py` → **PASS 285, FAIL 0** (1 expected WARN: source monolith not present for the
optional diff). Section count **25** = meta rows; every section linked from the hub; sitemap **26** URLs
(hub + 25 sections); no `.tex`/`txt`/`__pycache__` sources in the package; deterministic (re-run reproduces
the identical gate-report SHA-256).

---

*LOCK → Derive → Gate. No fitted parameters. precision (정밀) ≠ accuracy (정확). 반증을 메우니 발견이 선다.*
*Add-only: Chapters §0–§13 and Appendices A–F, H, I are unchanged; all 38 inherited driver-γ are re-locked*
*byte-for-byte against the parent param_db. The Appendix-I floor miss was a diagnosis — fill the named gaps*
*and the 0.70 floor is reached (0.755), requiring both fixes, but it stays `[L]`, never `[V]`. Order → days*
*is `[L]` with the global zero-point `[O]`; drive from sequence is `[F]` + order-preserving `[V]`; the gate*
*generalises to a quorum gate `[V]`. No body is claimed; physical_complete = False.*
