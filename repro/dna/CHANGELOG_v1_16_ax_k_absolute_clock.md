# CHANGELOG — v1.16 · Appendix K (the absolute clock)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

This release is **strictly add-only**. Chapters §0–§13 and Appendices A–F, H, I, **J** — every prior page,
number, grade, equation, and DOI — are **unchanged**. One appendix is added to the multi-page site with its
own fail-closed reproduction package, and the section count rises from 25 to **26**.

The only edit to a prior page is **navigational**: Appendix J's prev/next bar gains a forward link to
Appendix K. No prior body text, claim, or number was altered.

## What was added

### Appendix K — The absolute clock: pinning the global zero-point from two measured anchors
`docs/dna/ax-k-absolute-clock/` · `repro/dna/ax-k-absolute-clock/`

Appendix J closed four obstacles the order grammar left open, but **deliberately halved the fourth**: it
converted the somite *cadence* to days via the measured segmentation clock (`O2`), yet left **one global
zero-point** — a single absolute origin pinning every gene to an absolute embryonic day — explicitly `[O]`,
because that needs a **second independently measured anchor**. Appendix K closes **exactly that one piece
(B1)** with a **parameter-free two-anchor calibration validated out of sample**, and nothing more.

- **B1 — the global zero-point `[O] → [L]`.** The clock is a straight line `day(s) = a + b·s`, with its
  **slope and intercept each supplied by a different real measurement** so that **nothing is fitted**:
  - **SLOPE (segmentation modality, in vitro):** period **5.0 h** (Diaz-Cuadros 2020 *Nature* 580:113;
    Matsuda 2020 *Science* 369:1450) × **42** somite pairs (O'Rahilly & Müller) = **8.75 d**, spread over
    the cited **CS9 → CS13** bracket ⇒ **b = 2.1875 d/stage**.
  - **INTERCEPT (cardiac modality, in vivo):** first heart contraction = a **CS10** event at **22 ± 1 d**
    (O'Rahilly & Müller 1987; Moore, Persaud & Torchia, *The Developing Human*) ⇒ **a = 0.125 d**.
  - **Neither anchor consumes a tabulated stage-day**, so every cited Carnegie day and gene day is
    **held-out**: **5 held-out stages** (CS8–13, the CS10 intercept excluded) reproduced to **max 0.562 d**;
    **31 anchored genes** in the somite-clock window land inside the **±1.5 d** band (worst TBX5, 0.562 d);
    the cardiac anchor **independently corroborates** the tabulated CS10 day (recorded, not fitted).
    **Zero free parameters.**
  - **Honest bound (reported, not hidden):** the single somite-rate **drifts** after somitogenesis (CS14+),
    up to **6.56 d** at the latest stages, because the oscillator no longer sets the pace there. Unifying
    the somite and post-somite tempos into one *derived* rate law, and explaining the **origin** of the
    rates (why ~5 h, why ~42), are **firewall-permanent ceilings** — magnitude/origin questions excluded
    exactly as the absolute *strength* of the order prediction is (B3).

Everything else — the filled 63-gene / 62-edge cascade, the null, edge concordance, depth-beats-γ, the OR
wavefront and quorum/AND threshold-k gate, sequence-drive order-preservation, the O1 floor and its jitter
band, and the segmentation sub-clock — is **inherited from Appendix J and re-audited byte-for-byte on the
identical atlas**. **Appendix K introduces NO new γ.**

**Gate:** `python3 -m completion.gate` PASS **17/17** (`sha=49bbaa2a0ea2971f`); reading hash (2×SHA-256)
`f443a05f709b70e4437bb0acf629905eac09a7d750367ebb6e2694bd2d3bde55`; grades **V=10 L=4 F=1 O=1**
(the global-zero-point `[O]` is closed; only B5's declared clinical scope remains `[O]`);
`physical_complete=False`.

## Inheritance discipline (re-locked, byte-identical)

Appendix K inherits the substrate and parameters without retuning. **All 63 inherited driver-γ are
gate-checked digit-for-digit against the parent Appendix-J `param_db.json` read off disk** (`K1`, 0
mismatches), merging J's `driver_gamma_inherited` (38) and `driver_gamma_new` (25) blocks into the full
63 — and **K adds 0 new γ** (`driver_gamma_new = {}`), laying a *measurement* over the identical atlas. The
four skeletal drivers (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) are re-locked
byte-for-byte; the `(LEVEL, SHAPE) = (γ, A4 = robust_z)` operator and `spinodal(γ) = 2·(γ/3)^1.5` are
character-identical across appendices. The README carries the binding **§INHERIT** section *and* the binding
**BLUEPRINT for 100% completion**, now updated: **B1 is CLOSED**; the remaining path is **B2** (a cis-code →
drive map *derived* from sequence), **B4** (broader cited coverage to lift the jitter p5 above the floor),
and **B5** (a built/simulated organ, declared out of scope). The permanent ceiling stands: O1's absolute
strength — and the origin of the developmental rates — can never become `[V]`.

## Site

- New page `docs/dna/ax-k-absolute-clock/index.html` (long-form, JSON-LD `ScholarlyArticle` +
  `BreadcrumbList`, the four `vp-card` asides, the precision≠accuracy discipline card, prev nav to
  Appendix J).
- `docs/dna/_meta.json`: version **1.15 → 1.16**; the Appendix-K entry appended to `appendices`; the layout
  note extended (additive).
- `docs/dna/index.html`: Appendix K added to the JSON-LD `hasPart`, the appendix list, and the cross-links;
  the only change to the J page is its forward nav link.
- `docs/sitemap.xml`: `/dna/ax-k-absolute-clock/` added.
- `gate_multipage.py`: section count expectation **25 → 26**. Site gate **PASS** (296 PASS / 1 expected WARN
  — the source monolith is not bundled / 0 FAIL).

## Determinism

`python3 run.py` re-emits `expected/` byte-identically across runs (2×SHA-256), now including
`expected/absolute_clock.csv` (the held-out stage-day validation table). The figure
`figures/absolute_clock_overview.png` (the two-anchor clock + the held-out gene days) regenerates from the
locked data.

---

*Add-only. LOCK → Derive → Gate. precision (정밀) ≠ accuracy (정확). 영점은 측정되는 것이다.*
*The global zero-point Appendix J left `[O]` is closed by two independent measured anchors, 0 free*
*parameters, held-out days reproduced ≤ 0.56 d in the somite window — but it stays `[L]`, a measurement,*
*never `[V]`. physical_complete = False; remaining to 100% = B2 + B4 (+ B5 declared scope).*
