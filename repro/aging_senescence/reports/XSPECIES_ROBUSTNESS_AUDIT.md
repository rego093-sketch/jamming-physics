# Cross-species longevity discriminant — robustness / bias audit

**Package:** Aging & Senescence (`aging`) · **Phase:** writing · **Version introduced:** 1.2.0
**Module (SSOT):** `repro/_verify/xspecies_robustness_audit.py` · **Audit artifact sha256:** `c771cf7ee871f99d0a8d8ad0e994bc46c9679644187153d8265b5bf4c170531e`
**Engine result hash (unchanged):** `d6506074f9f9ae61375b5c127b637aa6df4dc49eea821801749011a3fa66aae9`
**Determinism:** SEED=19, PERM_ITERS=20000, LOOCV_PERM_ITERS=5000 — two runs byte-identical.

## 1. Why this audit exists

§9 ("Are human aging genes special?") concluded **human-not-special, no discontinuous γ longevity switch, TERT-not-a-switch** using three *per-gene* tests only: a human z-score, a single short/long threshold, and a per-gene Spearman + permutation trend (`xspecies_discriminant.py`). That design leaves four confounds untested, each able to **manufacture or mask** a signal in a 10-species panel:

1. **γ is a GC-content proxy** — the SantaLucia 1998 NN ΔG37 stacking energies are GC-weighted (CG/GC ≈ −2.2; AT/TA ≈ −0.6..−0.9), so "the γ axis" is really "the GC axis";
2. **maximum lifespan is allometric** — larger mammals live longer, so a raw γ–lifespan trend may be a body-mass artifact;
3. **the 10 species are not phylogenetically independent** — rodents cluster, primates cluster — so a naïve permutation over-counts; the correct test is independent contrasts on a dated tree;
4. **genes were tested one at a time** — a weak *shared* lean across the four masters would be invisible per-gene.

The audit re-derives γ bit-for-bit from the cached promoters (identical to the atlas) and runs the confound-corrected battery. It does **not** touch the locked emergence engine; it is an independent verification layer with its own artifact hash.

**Stance:** the conclusion was not pushed in either direction. Every test below was pre-specified and every result is reported, including the ones that *do* show a (weak) signal.

## 2. Data provenance (measured inputs, never tuned)

| Input | Source |
|---|---|
| promoter γ | re-derived here (SantaLucia 1998 NN ΔG37, TSS−2000..+500), identical to the atlas |
| maximum lifespan (MLSP) | AnAge, already in the package atlas |
| adult body mass (g) | AnAge build 14 reference weights; **dog flagged** (breed-variable; representative 25 kg, reported as a leave-one-out case) |
| divergence times (Myr) | TimeTree node ages, for the ultrametric tree used by Felsenstein (1985) independent contrasts |

## 3. Reproduction check

The audit re-derives the exact §9 per-gene numbers (human z; permutation p): TP53 z=+0.09 (p=0.114), CDKN2A z=+0.02 (p=0.352), FOXO3 z=+0.31 (p=0.073), TERT z=+0.64 (p=0.126). The offline-reproduce loop matches the stored atlas to <1e−6. The audit is therefore re-analysing the *same* numbers, not a different pipeline.

## 4. Results

### 4.1 GC confound — γ *is* GC, and GC carries no lifespan signal either

| gene | ρ(γ, GC) | ρ(GC, logMLSP) | perm p |
|---|---|---|---|
| TP53 | 0.964 | 0.394 | 0.264 |
| CDKN2A | 1.000 | 0.429 | 0.352 |
| FOXO3 | 0.988 | 0.576 | 0.089 |
| TERT | 0.988 | 0.576 | 0.090 |

γ ≈ GC content (ρ = 0.96–1.00). Crucially, **GC↔lifespan shows the same null as γ↔lifespan** — so the null is *not* an artifact of the γ transform. The γ-axis question is a GC-axis question, and the GC axis is null after the corrections below.

### 4.2 All four masters lean the **same** way — and the combined lean reaches borderline raw significance

Every per-gene rank correlation with lifespan is positive (TP53 +0.54, CDKN2A +0.43, FOXO3 +0.60, TERT +0.53); none individually significant. The **combined 4-gene mean-z** (a test the original never ran) vs **raw** log(MLSP):

- **ρ = +0.636, permutation p = 0.054** — borderline.

So the original "no trend" wording was slightly too strong. **But it does not survive correction** (§4.3–4.4).

The per-species combined z exposes *why* the raw trend is fragile: the **top** species is the **dog** (z̄ = +1.62) — only 24 yr and a *negative* body-size-corrected longevity residual — while the genuinely long-lived, intrinsically exceptional species (bat z̄ = +0.11, naked mole rat z̄ = +0.26) have ordinary γ. The bottom is brown rat (−1.32) and opossum (−1.42). The "trend" is short-lived GC-poor rodents at the bottom + a GC-rich short-lived outlier at the top, not a longevity gradient.

### 4.3 Body-mass correction — the lean weakens to non-significance

Allometry on the panel: log₁₀(MLSP) = 0.826 + 0.145·log₁₀(mass), r = 0.555. Body-size-corrected longevity residuals (higher = lives longer than its size predicts) are biologically sensible — bat +0.574, human +0.566, naked mole rat +0.441 at the top; brown rat −0.606, mouse −0.416, opossum −0.409 at the bottom.

| test | vs raw logMLSP | vs size-corrected longevity |
|---|---|---|
| TP53 | ρ=+0.54 (p=0.11) | ρ=+0.52 (p=0.13) |
| CDKN2A | ρ=+0.43 (p=0.35) | ρ=+0.25 (p=0.59) |
| FOXO3 | ρ=+0.60 (p=0.07) | ρ=+0.42 (p=0.23) |
| TERT | ρ=+0.53 (p=0.12) | ρ=+0.54 (p=0.12) |
| **combined** | **ρ=+0.64 (p=0.054)** | **ρ=+0.48 (p=0.16)** |

The combined lean drops from p=0.054 to **p=0.16** once body size is removed. The species that are *intrinsically* exceptional for longevity (bat, NMR) do not have exceptional γ.

### 4.4 Phylogenetic independent contrasts — the lean **collapses**

Felsenstein (1985) contrasts on the dated mammal tree (marsupial outgroup; rodents and primates as clades):

| trait | PIC corr(contrasts, logMLSP) | sign-flip perm p |
|---|---|---|
| **combined-z** | **+0.171** | **0.55** |
| TP53 | +0.193 | 0.46 |
| FOXO3 | +0.314 | 0.12 |
| TERT | +0.582 | 0.13 |

The borderline raw combined p=0.054 **collapses to p=0.55** under phylogenetic correction. The short-lived rodents are a single clade, so the raw lean was **phylogenetic pseudoreplication**. This is decisive: the confounds the original [O] grade *named* (GC, phylogeny) are exactly what produced the apparent lean.

### 4.5 Leave-one-species-out — the raw trend is unstable, not robust

Base raw combined ρ=+0.64 (p=0.054). Dropping single species moves it across 0.05 in **both** directions: drop **dog** → p=0.021 (the high-γ short-lived counterexample was *weakening* the trend), drop **human** → p=0.044, drop naked mole rat → p=0.051, others 0.06–0.16. An unstable, outlier-dependent p≈0.05 is not evidence for a real effect.

### 4.6 Switch threshold — a "clean gap" is manufacturable, not real

A clean γ gap between short- and long-lived appears **only** under aggressive cutoffs that exclude the middle: TP53 and FOXO3 at short<6 / long>40 yr, TERT at short<6 / long>25 yr (CDKN2A never). Those cutoffs compare 3 small short-lived species (mouse, rat, opossum) against large long-lived ones (human, chimp, elephant) — a body-size and phylogeny contrast with the mid-lifespan species (dog, cattle, bat, NMR) deleted. It is a threshold artifact, not a discontinuity.

### 4.7 Multivariate out-of-sample — the four γ values do not classify lifespan above chance

Leave-one-out classification of long (MLSP≥30 yr) vs short (<30 yr) from the 4-gene γ vector: **80% accuracy, but label-permutation p = 0.115** — not above the 50% base rate. The 80% is driven by the easy short-lived rodents; dog (short, high γ) and bat (long, low γ) are misclassified.

### 4.8 TERT — the one honest caveat

Among the four masters, **TERT (telomere maintenance) is the most lifespan-leaning**, and it is the **only** gene whose lean is **not** removed by body-mass correction:

- TERT γ vs log(MLSP): ρ=+0.53 (p=0.12)
- TERT γ vs log(body mass): ρ=+0.32 (p=0.37) — *not* a pure size confound
- TERT γ vs size-corrected longevity: ρ=+0.54 (p=0.12)
- TERT PIC contrast: +0.58 (p=0.13) — the largest of the four

It **never reaches significance** (p≈0.12 everywhere, n=10), so it is a **lead for a larger panel, not a result — graded [O]**. It aligns with established biology: the telomere lever on lifespan is real but acts **off the promoter-γ axis** — large mammals suppress somatic telomerase to resist cancer (Gomes 2011), a regulatory/dosage effect, not a promoter-sequence one.

## 5. Conclusions and regrade

The §9 null is **robust**. Human aging-gene promoter γ is within the mammalian distribution on every gene, no discontinuous switch exists, and **no confound-corrected test** (body-mass, phylogenetic independent contrasts, or multivariate out-of-sample) yields a significant γ–lifespan signal.

Two corrections sharpen the chapter:

1. **"No trend" → "a weak shared lean that is fully confound-attributable."** All four masters lean the same way and the combined raw p≈0.054, but it vanishes under body-mass correction (p=0.16) and collapses under phylogenetic contrasts (p=0.55); it is unstable to leave-one-out.
2. **TERT is the suggestive exception [O].** Most lifespan-leaning, survives body-mass correction, largest PIC contrast — but never significant (p≈0.12).

**Scope (important):** "no longevity gene" means **"no signature on the promoter-γ (=GC) axis,"** *not* "no longevity genetics." The real cross-species longevity levers are **off this axis** — TP53 copy number (Abegglen 2015 JAMA; Sulak 2016 eLife) and somatic telomerase suppression in large mammals (Gomes 2011) — exactly the framework's *conserved-substrate / divergent-dynamics* thesis.

**Grades:** human-not-special, no-switch, null-after-confound-correction, and weak-lean-is-confound-attributable → **[V]**; residual TERT lean → **[O]** (n=10, p≈0.12); off-γ-axis levers → **[L]**.

## 6. References

- SantaLucia J (1998) *PNAS* 95:1460 — unified nearest-neighbour ΔG37.
- Felsenstein J (1985) *Am Nat* 125:1 — phylogenetic independent contrasts.
- Abegglen LM et al. (2015) *JAMA* 314:1850 — elephant TP53 copy number and cancer resistance.
- Sulak M et al. (2016) *eLife* 5:e11994 — TP53 retrogene expansion in elephants.
- Gomes NMV et al. (2011) *Aging Cell* 10:761 — comparative mammalian telomere biology; telomerase suppression with body size.
- AnAge (Human Ageing Genomic Resources) — maximum lifespan and adult body mass.
- TimeTree (Kumar et al.) — divergence times for the contrast tree.

## 7. Reproduce

```
python repro/_verify/xspecies_robustness_audit.py      # full JSON + artifact sha256
# expected artifact sha256: c771cf7ee871f99d0a8d8ad0e994bc46c9679644187153d8265b5bf4c170531e
```

The engine result hash is unchanged (`d6506074…`); §9 prose and the PDF are regenerated from this audit's numbers via `tools/build_docs.py` then `tools/build_pdf.py`.
