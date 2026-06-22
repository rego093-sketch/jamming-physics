# LEDGER — Unified deterministic interpreter (§13)

**Chapter:** `13-unified-deterministic-interpreter`
**Grade:** principle-demonstration
**Append-only** on `dna_vp_site_INTEGRATED_v1_8_ch01-12`. No chapter 01–12 body, no
locked grammar, no NN table, and no γ value is modified. The locked A4 grammar and the
§12 methylation engine are **imported** (single source, VP-SPEC §1.1) and **sha256-pinned**
(`expected/grammar_pins.sha256`, and `_provenance.pinned_sha256` inside the results JSON).

---

## What this chapter does

It unites three reads that, until now, lived in different modules, into **one deterministic
interpreter** that reads a locus in five layers:

| Layer | Source (imported, unchanged) | Status here |
|---|---|---|
| MATERIAL γ = −mean(NN ΔG) | `dna_interpreter.gamma` / `gamma_lib_v10` | **immutable** (proven; see below) |
| SWITCH (R19 double-well) | `dna_interpreter.switch_params` | unchanged |
| COORDINATE (shell·anchor·loop·anchor-relative helix) | `key_pipeline_full.run_key` + `dna_interpreter.interpret_element` + `parse_ft_motors` | **RESTORED** |
| ENVIRONMENT (methylation) | `clade_reader_engine` (CpG O/E, CHG/CHH, per-gene, auto-detector) | **KEPT** (more accurate than A4) |
| LAYER-2 (sign·φ·role) | `dna_interpreter.interpret_element` | flagged, never assigned |

γ identity (immutable): `human_SOX2` (302,512 bp) → γ = **1.287315** (round 6), byte-identical
from `gamma_lib_v10` and `dna_interpreter`; their NN tables are identical. Re-checked by a gate
every run. **γ is not touched by this chapter.**

---

## Delta 1 — COORDINATE grammar **RESTORED** (additive, reversible)

The §11/§12 modules computed γ and global O/E statistics only; they did **not** read the A4
arrangement of an element (which shell, which anchor, how far, how many co-anchored loops, and
the anchor-relative helical phase). This chapter restores that read for every locus via the
locked A4 pipeline, using **real motors** parsed from re-acquired NCBI feature tables
(`rettype=ft`, region-relative; `inputs_annot/`, frozen with provenance + sha256).

- Demonstrated on the LCT promoter (the §10 headline locus): mid-shell, nearest anchor 1065 bp,
  1 co-anchored loop of 5 region motors, anchor-relative face 0.441 → `contact_competent=False`.
- Plant (Arabidopsis) and insect (honeybee) frozen regions read coordinate **and** methylation
  regime simultaneously.
- **Honesty (C3):** where a 120 kb window is gene-poor (human chr1 §11 region: 2 edge motors)
  the loop read is marked **[O]**, naming its closing dataset (full RefSeq genomic.gff for the
  region). No silent gray zone.

This delta adds information; it removes nothing and retires no prior claim.

## Delta 2 — helical claim **CORRECTED** (a prior claim is retired)

**Retired claim (irreversible):** §10/§11 reported that a *global* WW-ACF(10–11) periodicity is
"elevated above a composition-matched shuffle in all genomes" — an absolute ~10.4 bp
nucleosome-spacing percentile read from an arbitrary window edge.

**Why it was a surrogate:** an absolute periodicity from an arbitrary edge is a *composition*
surrogate for nucleosome spacing, not a statement about whether a specific element can contact a
specific partner. The whitepaper's own grammar says so: the physically meaningful quantity is the
phase **between two loci**, not an absolute phase from a window edge.

**Correct read (this chapter):** the anchor-relative phase `contact_competent` — whether a motor
(TSS) and its nearest anchor sit on the **same rotational helical face** (face ≈ 0 or ≈ 1, within
~60°) and can contact, versus opposite faces (≈ 0.5). Constants RISE = 3.4 Å/bp, TWIST =
34.29°/bp (locked). Present in every panel locus (gate-checked).

### Retired register (this chapter's authoritative entry)

> **RETIRED — global WW-ACF(10–11) "helical signal elevated above shuffle" as an element-level
> structural claim.** Superseded by the anchor-relative `contact_competent` read. Irreversible:
> the global periodicity percentile is not reinstated as a structural statement about an element.
> The global statistic remains a valid *descriptive* composition fact about a genome; it is only
> retired as a *coordinate/contact* claim.

**Author follow-up (not done here):** §08 ("Bounds, open questions, retired claims") carries the
standing retired register. Adding a one-line cross-reference there is an author edit; **§08 is
byte-locked in this integrated build and is deliberately left untouched.** This LEDGER is the
authoritative record until that author edit is made.

---

## Methylation **KEPT** (more accurate than A4 — not retired, promoted)

A4's raw `cpg_density` (CG count / (L−1)) conflates CpG content with GC content. The §12 reading
normalizes it: CpG **O/E** = (nCG·L)/(nC·nG). This chapter demotes raw `cpg_density` to a
secondary aux note and makes O/E the primary environment measure.

- Same LCT promoter: raw `cpg_density` = 0.0148 vs CpG **O/E** = 0.335 (the GC-normalized value).
- The full §12 layer is **reproduced bit-for-bit** by a retention gate: 52 quantities (human +
  6 plants + 6 insects, bulk CG/CHG/CHH + per-gene spread/low-fraction + regime) all match
  `12-…/expected/clade_reader_results.json`, and the 4-regime auto-detector stays all-correct.
- **Negative control (seed 19):** a mononucleotide-preserving shuffle of the LCT region erases the
  CpG depletion (promoter O/E 0.335 → 0.998) and the regime stops reading as a global CG blanket —
  confirming the signal is dinucleotide structure, not composition.

---

## Gates (all PASS; see `run.py`, `expected/run_gate.json`)

1. determinism — two runs byte-identical (2× sha256)
2. γ identity — human_SOX2 γ = 1.287315
3. A4 grammar gates — shells cover & contiguous, anchors in range & unique (every locus)
4. coordinate present — shell/anchor/contact read for every locus
5. methylation retention — reproduces §12 (52 quantities + auto-detector)
6. O/E replaces raw cpg_density as the primary environment measure
7. helical corrected — `contact_competent` present everywhere; old surrogate retired
8. negative control collapses — shuffle erases the O/E depletion and the regime
9. C3 — every [O] names a closing dataset; LAYER-2 flagged, never assigned

**Canonical reproduction:** `repro/dna/13-unified-deterministic-interpreter/run.py`
(reads only frozen inputs; the feature tables in `inputs_annot/` are frozen with provenance).

---

## Stress test — is `contact_competent` real signal or chance? (v1.9, honest result)

`stress_helical/stress_helical.py` asks the §11-style question the author raised: if we
elevate the helical read to a full grammar, does the anchor-relative `contact_competent` flag
carry element-level signal — a "100%" coordinate — or is it geometry at chance? It tests, across
the 12 cross-kingdom frozen regions, whether real TSS↔nearest-anchor same-face rates beat a
permutation null (random motor positions, 2000×) and the analytic chance of 0.34.

**Result — AT CHANCE.** Pooled over 246 motor–anchor pairs across 10 organisms (maize/human
skipped: <3 motors), the observed same-face rate is **0.337 vs chance 0.340, pooled z = −0.09** —
statistically indistinguishable from chance. Per-organism departures (zebrafish 0.86/n=7,
frog 0.0/n=4, fly 0.22/n=36) are small-n noise that washes out in the pool. Real TSS positions
are **not** helically phased to the composition-shell anchors.

**The honest three-way grading of "helical" (no gray zone):**
1. **Global WW-ACF(10–11) periodicity — REAL, descriptive.** Elevated above a composition-matched
   shuffle in all 12 genomes (frozen §11; WW global percentile 68–100). This is the
   nucleosome-positioning propensity and it stands as a *descriptive composition fact*. It was
   never retired as such — §13 retired only its use as an *element-level contact* claim.
2. **Anchor-relative `contact_competent` — DETERMINISTIC GEOMETRY, at chance biologically.** The
   grammar reads it for every locus (no [O] for the geometry), but this stress test shows it
   carries **no functional signal on its own** (pooled z = −0.09). It is therefore reported as a
   geometric quantity, **not** a functional-contact claim. Grading it by the test, not by
   assumption, is the C3-honest move.
3. **Realized functional contact — LAYER-2.** Whether two same-face loci actually loop depends on
   runtime factors (bound TFs, cohesin) the sequence does not encode. The stress test *vindicates*
   the two-layer thesis: the sequence gives geometry (Layer-1) but not realized contact (Layer-2).

**On "100%".** A 100% read is achievable for the *geometry* (every locus gets a phasing read) but
not for the *realized functional contact* (Layer-2). Conflating the two would violate the paper's
core discipline. The real, gradeable helical signal that *could* be promoted to a richer coordinate
axis is the **local nucleosome propensity** (the WW periodicity localized to elements), which gates
the environment channel (accessibility) — not the anchor-contact flag, which is chance.

**Canonical reproduction:** `stress_helical/stress_helical.py` → `stress_helical_results.json`
(feature tables frozen in `stress_helical/inputs_ft/` with provenance + sha256; deterministic,
fixed seed 19).

---

## Stress battery v1.9 (second session) — four cross-layer probes, honest grades

Four new stress tests, one per grammar layer plus engine robustness, in the §11/§13
style (observed vs permutation/shuffle null → pooled judgment → grade the limit, do not
change a locked threshold). All deterministic (seed 19, 2×sha256 identical), all locked
files re-verified **byte-identical to the original zip (153/153)**. Outputs live only in
new `stress_*/` dirs. No γ, NN table, threshold, or frozen expected was modified.

### A — MATERIAL: "γ is a restatement of GC" — refined, not rejected
`02-material-threshold-scale/stress_gamma_vs_gc/`. Per-window GC-preserving permutation
(60×) isolates the dinucleotide-order term beyond GC. **γ≈GC holds within-genome too**
(pooled corr 0.9949; per-organism 0.987–0.998) — the settled claim strengthens. The
dinucleotide residual is **small but structured, not noise**: only ~1.07% of γ variance,
yet pooled corr(Δγ, CpG O/E) = **+0.572** (partial|GC = 0.572, so *not* a GC confound),
mechanistically driven by stiff CG steps (ΔG −2.17; corr(Δγ, CG-step excess) = 0.576).
This **quantifies §11's qualitative "γ and CpG O/E are two projections of one history"**
payoff. **Boundary:** at GC ≈ 20% (Plasmodium) the mapping **inverts** (corr −0.29,
now TA-step driven); CpG O/E is uninformative at GC extremes.
→ Grade: "γ = GC restatement" **refined to** "γ = GC + a small (~1%) CpG-coupled
dinucleotide term, GC-dependent and inverting below ~20% GC."

### B — COORDINATE: A4 anchors — positions robust, count is a resolution choice
`13-unified-deterministic-interpreter/stress_coordinate_stability/`. Re-runs `run_key` at
neighboring LOCK settings (W, step, smooth_radius, min_shell_bp) and edge crops (probe
only; locked params unchanged). **93% of interior anchors recur within 2 kb** under
neighbor settings and crops — positions are a real ~kb-scale property, not a window
artifact (W/step/smooth neighbors 0.83–0.94; only smooth_radius=0 drops to 0.72; crops
0.87–0.98). At min_shell_bp=10000 recall falls to 0.28 **but precision stays 0.88** — the
survivors land on baseline positions (a consistent **nested subset**, not relocation;
anchor-count ratio 0.31×). → Grade: coordinate read is a **robust multi-scale skeleton
whose anchor *positions* carry ~kb uncertainty and whose anchor *count/inventory* is set
by resolution** (min_shell_bp), not an absolute. "Nearest anchor 1065 bp" is ~1 kb-binned.

### C — ENVIRONMENT: methylation auto-detector — generalizes within regimes; false-positives at GC ≲ 23%
`12-clade-methylation-readers/stress_detector_adversarial/`. Seven frozen 120 kb
out-of-panel organisms + 12-panel re-check. **Within-regime generalization is robust:**
unseen species classify correctly (tomato→PLANT; cow,dog→VERTEBRATE). **Out-of-category
biology is handled honestly:** Neurospora (fungal RIP) and oyster (mollusk gene-body)
return `no_global` [O] rather than a forced class. **Real false-positive boundary:** two
AT-extreme genomes with *no global 5mC* are **misclassified as PLANT** — Plasmodium
(GC 20.4%, CHG O/E 0.878) and Dictyostelium (GC 22.3%, CHG O/E 0.938); Tetrahymena
(GC 23.5%, CHG O/E 0.9959) is a knife-edge pass (0.004 above the 0.96 boundary).
Matched-composition nulls (iid-random and mono-shuffle, 40× each) return CHG O/E ≈ 0.99
and **never** a methylation class — proving the depletion driving the misclassification is
**real di/tri-nucleotide sequence structure (not an O/E estimator artifact) but is not
methylation** (these genomes lack 5mC; the depletion is AT-rich compositional/codon
avoidance). **This surfaces a latent error in the v1.9 panel itself: the Plasmodium call
`PLANT_global_CG_CHG_CHH` is a false positive of this mode.** Converges with Test A —
the same GC ≈ 20–23% region breaks the "CpG depletion ⇒ methylation" inference.
→ Grade: methylation auto-detector **bounded** — reliable within trained plant/vertebrate
regimes and honest out-of-category, but its "depletion ⇒ regime" inference is **unreliable
for extreme-AT genomes (GC ≲ ~23%) absent independent methylation evidence**; default to
`no_global`/[O] there. The panel's Plasmodium regime is **deprecated** to a known
false-positive (not deleted; a GC-conditioned threshold would be a new version).

### D — ENGINE: abnormal-input robustness — no silent-wrong; one run_key gap
`_verify/stress_abnormal_inputs/`. Battery of N-heavy/sub-window/single-base/lowercase/
IUPAC/empty inputs across the three locked engines. **No engine is ever silently wrong**
(worst case is a *loud* crash, not a fabricated number). `gamma()` and `bulk_contexts()`
are **graceful** (return NaN on the uncomputable; gamma upper-cases and skips non-NN
dinucleotides). **`run_key()` has one gap:** sub-window input (`len < W = 2000`) or empty
raises an **opaque `IndexError`** instead of a clean [O]/ValueError ("region shorter than
window"). Consistency note: `bulk_contexts()` is case-sensitive — lowercase (soft-masked)
input returns NaN, so **soft-masked FASTA must be upper-cased before methylation calls**
(`gamma()` does not need this). → Grade: engines robust; one actionable `run_key`
sub-window guard + one case-normalization note (both would be new versions, not done here).

**Net for the grammar book:** the three layers survive as *refined* reads, not rejections —
γ = GC + small structured CpG term (with a GC-extreme inversion); coordinate = robust
positions / resolution-set count; methylation = within-regime-reliable with a characterized
GC ≲ 23% false-positive boundary (and one latent panel misclassification, Plasmodium, now
deprecated). One engine robustness gap (run_key sub-window). Nothing silently wrong; every
limit is named with its closing condition.

---

## Chapter 14 — defensive guards **IMPLEMENTED** (the deferred new-version work)

The four stress probes above flagged three fixes as "new-version work, deliberately
left undone." They are now implemented in `repro/dna/14-defensive-guards/` as a
**wrapper layer** that imports the locked engines single-source + sha256-pinned and
adds guards *around* them. **No locked engine, threshold, γ, NN table, or frozen
`expected/` is modified** (152/153 byte-identical; the one diff is this LEDGER). The
design target is explicitly *not* zero-exception — it is "stop the demonstrated
failures, stay honest at the edges, with a declared residual risk."

- **`detect_regime_safe`** — fixes the Test C false positive. Below `GC_FLOOR=0.25`
  the CpG/CpHpG-depletion→regime inference is not trusted: the call is overridden to
  `no_global` and flagged `low_GC_composition_confounded` (raw call preserved in
  `raw_regime`, never hidden). NaN contexts → explicit `[O]_insufficient_sequence`.
  Floor justified empirically by the clean (22.3%, 30.9%) GC gap between the two
  misclassified genomes and the lowest real methylator (tomato).
- **`run_key_safe`** — fixes the Test D opaque crash: returns a clean `[O]` naming the
  closing condition when `len < W=2000`, instead of an `IndexError`.
- **`bulk_contexts_safe`** — fixes the Test D case gap: upper-cases first so soft-masked
  (lowercase) FASTA reads correctly.

**Stress result (`14-defensive-guards/stress_guards.py`, OVERALL_PASS=True, 2×sha256):**
methylation raw **17/19 → guarded 19/19**, fixing Plasmodium and Dictyostelium with
**zero regressions** (the guard changes exactly those two calls); `run_key_safe`
returns `[O]` on 200 bp/empty and is an identical pass-through on a normal region;
`bulk_contexts_safe` on lowercase equals the raw engine on uppercase (CpG O/E
0.7205==0.7205), and all-N → `[O]_insufficient_sequence`.

**Deprecation update.** The panel's Plasmodium regime — deprecated above to a known
false positive — is now **corrected at the guard layer** to `no_global` +
`low_GC_composition_confounded`. The locked panel value is unchanged; callers using
`detect_regime_safe` get the corrected, flagged result.

**Declared residual risk (not zero by design):** a hypothetical GC<25% genome with
genuine global 5mC would be wrongly down-graded; no such organism is known, and the
raw call is always retained for per-locus audit/reversal. Adopting the guards as
canonical is a caller-side import of `14-defensive-guards/guards.py`; chapters 1–13
are untouched.

---

## Chapter 14 — guard **VALIDATED out-of-sample** (GC_FLOOR=0.25 generalizes)

The 0.25 floor was set in-sample (from the organisms that found the Test C false
positive). It is now tested on **7 organisms not used to set it**
(`14-defensive-guards/stress_guard_validation/`): real plant methylators
soybean/moss/brassica and AT-rich non-methylators theileria/cryptosporidium/
entamoeba/trichomonas (frozen, provenance + sha256). **Result: floor generalizes,
guarded 7/7 correct, 2×sha256 identical.**

- **Headline:** **entamoeba (24.5% GC) is raw-misclassified PLANT and the guard catches
  it** — a *third* extreme-AT false positive (after Plasmodium, Dictyostelium) the floor
  was never tuned on. Genuine out-of-sample catch, not just no-regression.
- **Q1 falsification PASS** — no real methylator below the floor; lowest is soybean
  31.6% (+6.6 pt margin); all three real methylators classify PLANT, untouched.
- **Q2 below-floor PASS** — entamoeba (24.5%) correctly suppressed.
- **Q3 above-floor PASS** — every non-methylator in 25–31% (crypto 30.9%, trichomonas
  33.4%, theileria 33.8%) is raw-correct `no_global`; the floor is not too low.
  Cryptosporidium is AT-rich yet raw-correct (CHG O/E 1.06 > 0.96), showing the false
  positive is *extreme CHG depletion co-occurring with GC ≲ 25%*, not GC% alone.

Tally across all sessions: the GC≲25% false-positive mode is now demonstrated on **3
independent extreme-AT non-methylators** (Plasmodium, Dictyostelium, Entamoeba), all
caught by the guard, while **6 real methylators all sit ≥ 31.6% GC**. The declared
residual risk (GC<25% genome with genuine global 5mC) remains unobserved. No threshold
changed; locked set still byte-identical (the only diff is this LEDGER).

---

## v1.13 — γ↔A4 stated as LEVEL vs SHAPE (clarification, append-only)

This chapter's abstract previously said the earlier chapters "split the read in two"
without naming the relationship between γ and the A4 coordinate, which left room for the
**"γ ⊂ A4" misconception**. v1.13 names the relationship exactly, in this chapter and at
§I/§2/§8, and retires the misconception in the §8 register.

**The relationship (verified [V]).** γ = `−mean(NN ΔG)` is the **LEVEL** (window-mean) of the
stiffness signal. The A4 coordinate is the **SHAPE** of that *same* signal with its mean
removed: `key_pipeline_full.run_key` applies `robust_z`, which subtracts the per-locus median —
exactly the level γ is — and keeps only the within-locus relative structure (shells, anchors,
loops, anchor-relative phase). So **A4 = "the signal minus γ," and "γ ⊂ A4" is impossible.**

**Evidence** (`vp_session_gamma_a4_verified`, 4 phases, 2×SHA-256,
`prereg.sha256 ff04aa7b…3901`): same field (per-locus ρ = 0.939; identical coarse anchors,
0.0 bp offset across all 37 loci) yet the A4 coordinate carries **none of γ**
(max |corr(axis, γ)| = 0.327). Shared input ≠ nested output.

**Edits (all append-only; no number/grade/equation/DOI changed):** §13 abstract opening
replaced with the level/shape statement (same numbers); a one-sentence `robust_z` mechanism
note added to *The coordinate grammar, restored*; a reusable "γ vs A4 level vs shape" vp-card
added to §I and §13; §2 and the §8 closure gain a level/shape clause; the §8 retired register
gains the irreversible **"γ ⊂ A4" framing tombstone**. Full spec: `GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md`.

**Standing [O] preserved (do not over-claim the other direction).** "The γ-**level** is
orthogonal to developmental timing" is earned [V] (heart ρ = +0.071, p = 0.882). Whether the
A4-**shape** carries timing the level cannot is **[O]** — the one fair test (heart/organ timing
re-run with 25–50 kb windows so A4 has real shell/anchor resolution) has not been run; the
single Phase-3b attempt was on degenerate 2501 bp promoters < min_shell_bp. "γ-level ⊥ timing"
must not be read as "sequence ⊥ timing."
