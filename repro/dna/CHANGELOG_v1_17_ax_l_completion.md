# CHANGELOG — v1.17 · Appendix L (the blueprint close-out)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245

This release is **strictly add-only**. Chapters §0–§13 and Appendices A–F, H, I, J, **K** — every prior page,
number, grade, equation, and DOI — are **unchanged**. One appendix is added to the multi-page site with its
own fail-closed reproduction package, and the section count rises from 26 to **27**.

The only edit to a prior page is **navigational**: Appendix K's prev/next bar gains a forward link to
Appendix L. No prior body text, claim, or number was altered.

## What was added

### Appendix L — The blueprint close-out: the jitter floor closed, the cis-drive shown data-blocked
`docs/dna/ax-l-completion-closeout/` · `repro/dna/ax-l-completion-closeout/`

Appendix K closed **B1** (the global zero-point) and left a **binding BLUEPRINT** with two open items (**B2**,
**B4**), one permanent ceiling (**B3**), and one declared scope (**B5**). This appendix takes that blueprint to
its **honest terminus** — closing what can be closed and naming exactly what is missing where it cannot.

- **B4 — the jitter floor `[L]` (marginal) → `[L]` (jitter-robust). ✅ CLOSED.** In Appendix K, **PAX7** was an
  **artificial cascade source** (indegree 0, depth 0) despite Carnegie rank 4, which dragged the ±1 rank-jitter
  lower edge below the pre-registered 0.70 strength floor. The single cited edge **MEOX1 → PAX7** (somite/
  dermomyotome precedes & gives rise to Pax7⁺ myogenic progenitors; Buckingham & Relaix 2007 *Annu Rev Cell Dev
  Biol* 23:645; Mankoo 1999 *Nature* 400:69) — the **same source-fix class** already used for the limb/Hox
  founders — removes the artifact:
  - PAX7 cascade depth **0 → 3**; Spearman(depth, Carnegie) **0.7546 → 0.8575**.
  - ±1 rank-jitter (seed 19, n=4000): mean **0.6931 → 0.7854**, **p5 0.6245 → 0.7277 (≥ 0.70 floor)**,
    fraction ≥ floor **0.44 → 0.99**.
  - **0 new inversions** (MEOX1 rank 4 = PAX7 rank 4, a concordant tie); the cascade is still a **DAG**.
  - The strength is now **jitter-robust** but stays **`[L]`, NEVER `[V]`** — B3 forbids a verified absolute
    strength, and the gate fails closed on any such promotion.

- **B2 — cis-code → drive. ⛔ DATA-BLOCKED by measurement.** A deterministic, **parameter-free** probe
  (`completion/cis.py`; seed 19, **500 dinucleotide-shuffles**, both strands) scans each **child** promoter — the
  **same ±2 kb window the γ operator reads** — for the **parent** regulator's cited consensus motif vs a shuffle
  null. The per-edge drive is **not in the proximal window**: only **5/21** both-cached edges exceed background,
  mean z **0.82**, and decisively the **canonical SOX9 ⊣ RUNX2 edge is BELOW background (z ≈ −2.13)** —
  consistent with that repression acting through **distal enhancers**, not the proximal promoter (PAX1→SOX9 is
  likewise below background). Closing B2 would require **distal-enhancer + chromatin-accessibility** sequence the
  kit does not contain — **named as the unblock condition**. `W = √γ` stays **`[F]`, not `[L]`**. This is a
  **measurement limitation** (cf. the Inheritance-Kit FV5 data-blocked-by-measurement result), not a theory
  defect.

Everything else — the 63-gene atlas, the DAG/wavefront/order results, the two-anchor absolute clock (`B1`), the
null, edge concordance, depth-beats-γ, the OR wavefront and quorum/AND threshold-k gate, sequence-drive order-
preservation, the O1 floor, and the segmentation sub-clock — is **inherited from Appendix K and re-audited
byte-for-byte on the B4-extended cascade**. **Appendix L introduces NO new γ.**

**Gate:** `python3 -m completion.gate` PASS **18/18** (`sha=b0cf5eae7285b50a`); reading hash (2×SHA-256)
`a817287d1b57d84ea30a2c6ce7ade71f1333561205a4e1b4785abda78af37aca`; grades **V=10 L=5 F=2 O=1**;
`physical_complete=False`; `blueprint_fully_mapped=True`.

## Inheritance discipline (re-locked, byte-identical)

Appendix L inherits the substrate and parameters without retuning. **All 63 inherited driver-γ are gate-checked
digit-for-digit against the parent Appendix-K `param_db.json` read off disk** (`L1`, 0 mismatches) — and **L adds
0 new γ** (`driver_gamma_new = {}`), laying one cited edge and one measurement over the identical atlas. The four
skeletal drivers (**SOX9 1.459260, RUNX2 1.241556, PAX1 1.504372, GLI3 1.298352**) are re-locked byte-for-byte;
the `(LEVEL, SHAPE) = (γ, A4 = robust_z)` operator and `spinodal(γ) = 2·(γ/3)^1.5` are character-identical across
appendices. The README carries the binding **§INHERIT** section *and* the **BLUEPRINT**, now **FULLY MAPPED**:
**B1 ✅ CLOSED**, **B4 ✅ CLOSED**, **B2 ⛔ DATA-BLOCKED** (distal-enhancer data is the named unblock condition),
**B3** permanent ceiling (absolute strength; origin of the rates), **B5** declared scope. The completion
criterion (B2 **and** B4 both `[L]`) is **not** met because B2 is data-blocked → `physical_complete = False`.

## Site

- New page `docs/dna/ax-l-completion-closeout/index.html` (long-form, JSON-LD `ScholarlyArticle` +
  `BreadcrumbList`, the four `vp-card` asides, the precision≠accuracy discipline card, prev nav to Appendix K).
- `docs/dna/_meta.json`: version **1.16 → 1.17**; the Appendix-L entry appended to `appendices`.
- `docs/dna/index.html`: Appendix L added to the JSON-LD `hasPart`, the appendix list, and the cross-links; the
  only change to the K page is its forward nav link.
- `docs/sitemap.xml`: `/dna/ax-l-completion-closeout/` added.
- `gate_multipage.py`: section count expectation **26 → 27**. Site gate **PASS** (307 PASS / 1 expected WARN —
  the source monolith is not bundled / 0 FAIL).

## Determinism

`python3 run.py` re-emits `expected/` byte-identically across runs (2×SHA-256), now including
`expected/b4_jitter.csv` (the B4 closure: K terminus vs L, p5 vs floor) and `expected/b2_occupancy.csv` (the B2
per-edge motif-occupancy z-scores vs the dinucleotide-shuffle background). The figure
`figures/blueprint_closeout_overview.png` (the B4 jitter distribution shift + the B2 occupancy z-scores)
regenerates from the locked data.

---

*Add-only. LOCK → Derive → Gate. precision (정밀) ≠ accuracy (정확). 반증을 메우면 발견이 서고, 못 메우는 곳은*
*어디가 비었는지 말한다.*
*Appendix K's open blueprint is closed out: B4 is closed by one cited edge (MEOX1→PAX7; jitter p5 0.625 → 0.728*
*≥ floor, 0 new inversions, DAG preserved) — jitter-robust but [L], never [V]. B2 is data-blocked by measurement*
*(the per-edge drive is not in the ±2 kb promoter window; SOX9⊣RUNX2 below background) — [F], not [L]; distal-*
*enhancer data is the named unblock condition. The blueprint is fully mapped; physical_complete = False; no body*
*is claimed; remaining to 100% = B2 (distal-enhancer cis-drive data) + B5 (declared scope).*
