# Module 03 — Emergence II: the clock and the material are decoupled (H2)

**Author:** Young Jae Lee · ORCID 0009-0002-7535-8245 · CC BY 4.0 · https://jamming-physics.org/
**Tier:** 1 (emergence — the load-bearing one) · **Consumes:** Modules 01–02 · **Data:** the same 6 mitogenomes.
**Status:** BUILD + GRADE. Reproduces from `repro/compare_channels.py` → `results/channel_records.json`.
**Standing grade:** decoupling **[V]**; "the clock therefore cannot carry a material/age claim" **[F]** from the decoupling; "the clock instead supports a flood" **[O]**.

> **One line.** This is the "doubt the average theory" test made quantitative. On the same 13 genes, across **all 78 within-clade gene-pairs**, the molecular clock (substitution count — the average theory's deep-time axis) and the material (|Δγ|) have **Pearson r = −0.081 ≈ 0**. They are *different physical channels.* The clock counts edits; the material reads present stacking stiffness; the one does not predict the other.

---

## 1. The test

For every within-clade gene-pair (Elephantidae: 3 taxa × 13 genes × 3 pairs; Homo likewise → 78 pairs), read **both** channels on the *identical* window:

- **(A) material:** |Δγ| between the pair.
- **(B) clock:** substitutions over a global alignment (`PairwiseAligner`, match +1 / mismatch −1 / gap −5,−1) — the raw tally the average theory turns into branch lengths.

`repro/compare_channels.py` prints the full per-pair table and the summary.

## 2. The result

> **r(substitutions, |Δγ|) = −0.081  (n = 78 gene-pairs).**

- Total substitutions counted by the clock: **2656**.
- Mean |Δγ| per pair: **0.0057** (sd 0.0050; max 0.0222) on an operating scale γ ≈ **1.29** (range 1.221–1.361).
- Material movement per substitution: **~0.00017 γ / substitution** — i.e. the clock can tick hundreds of times while the material barely moves.

**Two diagnostic pairs:**
- mammoth vs Asian elephant **COX2: 33 substitutions → |Δγ| = 0.00012** (clock ticks hard, material still).
- Asian vs African elephant **ATP8: 5 substitutions → |Δγ| = 0.0144** (clock barely ticks, material moves most).

The rank order of the two channels does not even agree. A scatter of (B) against (A) is a flat cloud (figure Panel B).

## 3. What it means (and the firewall, both ways)

The average theory reads (B) as an age/descent axis. This result shows (B) **does not predict the material the locus is actually made of.** A near-zero correlation is exactly what the inherited method's evolution-silence predicts: the material is conserved within a kind, substitutions accumulate **orthogonally** to it, so **a clock distance cannot be promoted to a material or kind statement** ([F], from the decoupling + GOVERNANCE Art. 2.2 / 3). The clock is, in the Cascade's vocabulary, an *internal technicality* — degenerate as a history carrier, like magnetic stripes under uniform time-rescaling.

**The firewall cuts both ways (Art. 2.2).** The decoupling **demotes the clock** as a history instrument; it does **not** elevate any alternative history. It is *not* evidence that a flood occurred. It removes the clock's standing to assert deep-time descent *to the material*, and simultaneously denies itself the right to assert the opposite. Both histories stay **[O]**.

## 4. Grade

| Claim | Grade |
|---|---|
| Clock and material decoupled: r = −0.08, n = 78 | **[V]** |
| ~0.00017 γ per substitution; COX2/ATP8 diagnostics | **[V]** |
| The clock cannot be promoted to a material / age claim | **[F]** (from H2) |
| The clock instead supports a flood (or any specific history) | **[O]** |

**Verdict: the average theory's instrument and the material instrument are different channels. This is the package's central, defensible empirical contribution — a measured decoupling, not a louder assertion.**
