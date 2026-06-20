# ANCHORS VERIFIED — the cited `[L]` literature anchors, checked against current sources (v1.0.0)

**Package:** `integumentary_vp_site` v1.0.0 · **author:** Young Jae Lee (ORCID 0009-0002-7535-8245)
**Scope of this file:** a **documentation** artifact. It records a v1.0.0 pass over the package's
cited `[L]` anchors against current authoritative literature (network access available this session).
It changes **no computation**: every determinism hash is byte-frozen (see `COMPLETION_LEDGER.md`). The
`[V]` shapes are derived and were never fitted to these numbers; the `[O]` magnitudes remain open with
their stated obstacle. This file's job is only to make each `[L]` citation explicit and to flag, with
the framework's own "name it, don't hide it" discipline, the one place where a model quantity must not be
read as a literal epidemiological incidence.

The grade key is unchanged: **`[V]`** simulation-verified shape · **`[L]`** cited literature anchor ·
**`[F]`** regime-scale set-point · **`[O]`** absolute magnitude, open, obstacle stated.

---

## A1 · Epidermal turnover (target T4) — resolves the CHARTER `TO-ANCHOR` flag

**Package claim.** T4 reads epidermal turnover as the sum of comparable substrate-dwell phases (viable
epidermis + stratum corneum, equal `gamma_TP63` dwell); with the stratum-corneum transit calibrated to
~14 d the total lands ~28 d, stated to sit "inside the cited 28–40 d window." Shape `[V]`; rate/window
`[L]`; absolute days `[O]`.

**Verified against literature.**
- Classic radiolabel/marker work (Weinstein and successors) puts whole-epidermis turnover at roughly
  **39–48 days**, partitioned into a proliferative compartment (~22 d), a differentiated compartment
  (~12 d), and a stratum-corneum transit (~14 d); the dansyl-chloride marker gives a stratum-corneum
  transit of **~20 days** in young adults, lengthening >10 d with age.
- More recent density-based models extend the whole-epidermis figure to **~45–59 days**, and reviews
  note the widely-quoted "28-day renewal" is a **lower-bound simplification**, with realistic
  whole-epidermis turnover commonly **~40–56 days**.

**Resolution and honest note.** The anchor is now explicit `[L]`: stratum-corneum transit **~14–20 d**;
whole-epidermis turnover **~28–48 d** (classic) extending to **~56 d** in newer estimates. The package's
modelled ~28 d total therefore sits at the **conservative lower edge** of the literature, not its centre.
This is recorded rather than tuned: the `[V]` content is the *additive dwell-cascade structure* (equal
`gamma_TP63` dwell across the two epidermal compartments), which is unchanged; only the cited window is
now stated with its full breadth, and the absolute total remains `[O]`. Stating the window as "28–40 d"
was defensible but narrow; "≈28–48 d, lower-bound simplification near 28 d" is the faithful anchor.

## A2 · UV carcinogenesis dichotomy (oncology kernel) — melanoma vs SCC

**Package claim.** One convex multistage rate splits the UV cancers: **SCC near-linear in cumulative
dose**; **melanoma intermittent/burst-sensitive** (Jensen on the multistage rate) with a
**chronic-exposure "tan paradox"** (sustained exposure protective against melanoma). Shapes `[V]`;
epidemiological direction `[L]`; absolute incidence `[O]`.

**Verified against literature.**
- **Melanoma ← intermittent/recreational + sunburn.** The Gandini meta-analysis (57 studies) reports a
  summary relative risk for **intermittent** sun exposure of **~1.6** (≈1.3–2.0), with **no** association
  — indeed an **inverse** association — for **chronic/occupational** exposure. Severe blistering sunburns,
  especially in childhood/adolescence, are a consistent melanoma risk factor. This is exactly the
  package's intermittent-sensitive + chronic-protective (paradox) dichotomy.
- **SCC ← cumulative/chronic UV.** SCC develops after years of cumulative exposure; pooled occupational
  (outdoor-worker) odds ratio **~1.77** (≈1.40–2.22). Near-linear in cumulative dose, as the package's
  showcase asserts.
- **BCC ← excessive intermittent exposure** (closer to the melanoma pattern than SCC). The package groups
  SCC/BCC; the literature separates BCC (more intermittent) from SCC (cumulative). Noted below.

**Resolution and honest note.** The dichotomy direction is strongly anchored `[L]` and matches the
model's `[V]` shapes. One refinement worth recording: lumping **BCC with SCC** under "cumulative" is a
simplification — BCC's epidemiology is more intermittent-like. The package's clean cumulative-dose
showcase is properly **SCC**; BCC is carried along as a non-melanoma neighbour, and a future split could
place BCC nearer the melanoma/intermittent pole. Absolute incidences stay `[O]` (population baseline +
dose calibration obstacle).

## A3 · Pigment-loss → oncology (the INTERNAL-LIVE seam) — albinism / OCA

**Package claim (seam, re-exported verbatim from the pathology layer).** A melanocyte-target (T3) lesion
that removes the melanin screen raises the shared oncology-kernel hazard: an albinism-type screen-loss
raises the **SCC cumulative-hazard RR to ≈2.58×** (incidence RR ≈2.24×) and the **melanoma burst RR to
≈10.59×**, while an exogenous sunscreen lowers the SCC hazard RR back to **≈1.13×** — the screen is the
**causal lever**. Coupling shape `[V]`; cited epidemiology `[L]`; absolute RR `[O]`.

**Verified against literature.**
- **OCA → dramatically elevated SCC.** In oculocutaneous albinism the lack of eumelanin removes
  photoprotection; **squamous cell carcinoma is the dominant skin cancer (≈75–88 % of cases)**, followed
  by BCC (≈9–23 %). In sub-Saharan-African albinos the SCC risk is reported on the order of **up to
  ~1000-fold** above the general (darkly-pigmented) population, with an aggressive, recurrence-prone
  course. Sunscreen / sun-avoidance is the established preventive (screen restored).
- **Melanoma is RARE in OCA.** Multiple series report **no or very few melanomas** in albino cohorts —
  because OCA *removes the melanocytic/melanin substrate itself*, so there is little eumelanin-bearing
  tissue to transform. The dominant malignancy is keratinocyte-derived (SCC).

**Resolution and the one honesty flag (master map §6.3).** The package's **SCC** side is strongly
anchored `[L]`: pigment-loss → large SCC-hazard rise, sunscreen as the causal lever — direction and
lever confirmed; absolute multiplier `[O]`. The **"melanoma burst RR ≈10.59×"** must **not** be read as
"albinos have ~10.6× the melanoma incidence" — the OCA epidemiology says the opposite (melanoma is rare
in OCA). The figure is a **property of the shared oncology kernel**: with the photoprotective screen
removed (delivered-UV attenuation → 1.00), the **burst-sensitivity of the multistage rate** rises by that
factor. It is a `[O]`/`[V]` kernel-sensitivity quantity, not a cited OCA incidence `[L]`. Crucially this
is **consistent**, not contradictory: OCA's clinical melanoma-rarity follows from substrate removal, a
*different* axis from the kernel's dose-burst sensitivity, and the package already grades the burst RR as
`[O]` (never as a cited incidence). Recorded here so the seam output is read correctly by any one-body
runner that consumes it.

---

## Summary table

| anchor | package grade | literature (verified) | status |
|---|---|---|---|
| epidermal turnover window (T4) | `[L]`/`[O]` | SC transit ~14–20 d; whole-epidermis ~28–48 d (→~56 d) | resolved; package sits at conservative lower edge |
| melanoma ← intermittent/sunburn; chronic protective | `[L]`/`[V]` | SRR ~1.6 intermittent; chronic inverse; sunburn risk | confirmed, matches dichotomy |
| SCC ← cumulative UV (near-linear) | `[L]`/`[V]` | occupational pooled OR ~1.77; cumulative | confirmed |
| BCC grouped with SCC | simplification | BCC more intermittent-like | noted; future SCC/BCC split |
| OCA → SCC hazard (screen-loss; sunscreen lever) | `[L]`/`[O]` | SCC dominant (75–88 %), up to ~1000× in African albinos | confirmed (direction + lever); magnitude `[O]` |
| "melanoma burst RR ≈10.59×" | `[O]`/`[V]` kernel | melanoma RARE in OCA (substrate removed) | **flagged**: kernel-sensitivity, *not* OCA incidence — consistent |

**Net effect on the release.** No hash changed; no constant added; no shape re-fitted. The `[L]` anchors
are now explicit and current, the `TO-ANCHOR` flag is cleared, and the single place where a model number
could be mis-read epidemiologically is named and bounded. This is the "name it, don't hide it" pass the
framework asks for before a 1.0 release.
