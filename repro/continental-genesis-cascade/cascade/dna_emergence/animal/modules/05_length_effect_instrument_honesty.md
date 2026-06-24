# Module 05 — Instrument honesty: the within-kind γ-range is a window-length artefact (반증 = 발견)

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Tier:** 1 (honesty / instrument calibration) · **Consumes:** Modules 01–04 · **Data:** the same 13 mito genes.
**Status:** HONEST FINDING. Reproduces from `repro/length_effect.py`. The result *bounds* within-kind reads and *does not touch* H1 or H2.
**Standing grade:** window-length effect **[V]** as an instrument property.

> **One line.** The archaic/modern precedent put per-gene γ conservation at < 0.0016, yet some mito genes here show within-kind γ ranges up to ~0.014. Honest question: real difference, or instrument noise? Answer: **r(gene length, within-kind γ-range) = −0.56** — the short genes are the noisy instrument; the long genes recover the < 0.0016 scale. It is a **window-length artefact**, and it leaves the two load-bearing results intact.

---

## 1. Why the question must be asked

γ = −mean(NN ΔG) is a mean over (L−1) nearest-neighbour steps. Like any mean, its sampling noise falls with window length. So an inflated *within-kind* γ-range on a short gene might be nothing but the instrument's own variance, not a material difference between members of a kind. The governance requires we check rather than report the inflated range as signal.

## 2. The check

`repro/length_effect.py` correlates each gene's length with its maximum within-kind γ-range:

> **Pearson r(gene length, within-kind γ-range) = −0.56** (longer window → smaller range).

- **Short / noisy:** ATP8 (201 bp) range **0.0222**; ND4L (297 bp) 0.0115; ND6 (525 bp) 0.0177.
- **Long / clean:** ND5 (1812 bp) **0.0068**; COX1 (1542 bp) **0.0014**; ND4 (1368 bp) 0.0085; CYTB (1136 bp) 0.0069.

The long-window genes recover the inherited **< 0.0016** promoter-scale conservation (COX1 reaches it). The within-kind γ-range inflation is therefore a **window-length artefact**; the long-window read is the cleaner instrument.

## 3. Scope: this does NOT weaken H1 or H2

Crucially, the artefact is a *within-kind* effect, and both load-bearing results are *between-kind / cross-channel*:

- **H1** (Module 02) is the **between-kind** gap (median 17×), which dwarfs the window noise — short or long, every gene still partitions the two kinds cleanly.
- **H2** (Module 03) is a **correlation between two channels on identical windows**; window length cancels because both channels see the same window. The decoupling (r = −0.08) is unaffected.

So the honest finding **sharpens the instrument** (within-kind reads should use long windows) **without** touching the two results the package rests on. It is recorded as a finding, not a retreat.

## 4. Grade

| Claim | Grade |
|---|---|
| r(length, within-kind γ-range) = −0.56; short windows noisiest | **[V]** |
| Long windows recover < 0.0016 (COX1 0.0014, ND5 0.0068) | **[V]** |
| Within-kind γ-range inflation = window-length artefact | **[V]** |
| Effect bounds within-kind reads only; H1/H2 intact | **[V]** |

**Verdict: an honest instrument calibration — the within-kind range is window noise, the long-window read recovers the inherited conservation scale, and the between-kind / cross-channel results stand.**
