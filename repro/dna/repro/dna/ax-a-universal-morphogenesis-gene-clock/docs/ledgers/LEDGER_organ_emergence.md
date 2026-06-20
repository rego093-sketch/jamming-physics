# LEDGER — visceral-organ emergence (v10)

Honest, per-quantity grading for the v10 internal-organ addition, in the neuro VP-SPEC C3
discipline (every quantity graded; no silent gap). Grades: **[V]** validated/derived,
**[F]** forced modelling choice (representative; documented), **[L]** locked + cited measured
input, **[O]** open (named obstacle; not claimed).

## The claims, graded

| # | quantity | grade | basis / why this grade |
|---|---|---|---|
| 1 | one switch (organ gene-clock fold == body fold) | **[V]** | `spinodal(g)=2*(g/3)^1.5` identical to `morpho_core.spinodal` to **2.2e-16** over γ∈[1.2,1.8] (`assert_one_switch`). The organ clock is literally the same R19 fold as the face clock and the neuro ch17 spinodal — not a bolt-on. |
| 2 | visceral-organ **emergence ORDER** is a measured-γ readout | **[V]** | `order == argsort(spinodal(γ))` (`order_is_gamma_readout=True`); perturb a γ and the order resorts. No hand-typed order. Same mechanism that gives the kit's face order and the neuro spinal ventral→dorsal order, here in the TIME axis. |
| 3 | measured γ for the 8 organ masters | **[L]** | `data/organ_gamma.json`, fetched by the **identical** NCBI→SantaLucia pipeline (`fetch_organ_gamma.py`): exact human TSS → promoter TSS-2000..+500 → γ=−mean(NN ΔG37, SantaLucia 1998). All from `NC_` (GRCh38) accessions; corr(γ,GC)=**0.994** (kit ~0.99). Read-only, never fitted; sequences cached so γ reproduces offline bit-for-bit. |
| 4 | gene → organ map (the masters) | **[V]** | heart=NKX2-5, liver=HHEX, stomach=BARX1, lung=NKX2-1, pancreas=PDX1, kidney=SIX2, spleen=TLX1, midgut=CDX2 — each a genuine specification master for its organ primordium. **Notes:** HHEX is also a thyroid/forebrain factor (used here as the canonical liver-bud specifier); NKX2-1 is the lung **and** thyroid master (locked here for the lung bud). These multi-tissue notes are recorded, not hidden. |
| 5 | sign convention (higher spinodal → later) + τ window [τ0,τ1] | **[F]** | forced modelling choices, documented. Flipping the sign flips the order (exactly as a flipped Shh threshold flips the neuro spinal order). The absolute τ window is display-only; only the order + relative spacing are read from γ. |
| 6 | observed first-appearance **Carnegie stages** | **[L]** | `data/organ_timing.json`: ordinal CS from O'Rahilly & Müller (Carnegie Publ. 637), Larsen's, Moore, UNSW Embryology. Read-only, integer, γ-independent, sha256-frozen. **Never adjusted to move a correlation.** |
| 7 | **does γ predict organ timing?** | **[O]** | **NO — honest null.** Spearman ρ(spinodal, observed CS) = **−0.414** (exact permutation p = **0.360**, n!=5040); Pearson r = −0.447. If anything weakly **anti**-correlated (spleen is γ-earliest but biologically latest at CS15; stomach is γ-latest but CS12). A positive claim needs perm p<0.05 **and** ρ>0; neither holds. Promoter stiffness is **not** the organ-timing correlate — fully consistent with the external-feature dev-timing null (v5–v8). Reported, not tuned. |
| 8 | organ **size / shape / 3D placement** from dwell | **[O]** | only relative `dwell ∝ γ^1.5` is given. The 3D coupling of this schedule into the actual Layer-2 anatomy volume fill (`assemble.anatomy_spec`) is **not done in v10** — it is the documented next step (see HANDOFF). v10 claims the order/schedule, not the grown organ geometry. |

## Scope decision recorded (not silent)

- **midgut/intestine (CDX2) is EXCLUDED from the locked timing test**, carried in `organ_atlas.py`
  for the emergence geometry only. Reason: intestinal first-appearance is **progressive** (the gut
  tube forms over CS10–13 with body folding) with no crisp single "intestine at CS X" — the same
  soft-staging reason **MYF5/myotome** was excluded from the v8 dev-timing line. Including it would
  mean choosing one stage from a range (disguised tuning).

## Why a null is the correct, honest outcome here

The v10 gate (`verify_organ_timing.py`) **does not require any correlation value** — that would be
the tuning anti-pattern. It enforces **grade == evidence**: the schedule is a pure γ readout, the
input is locked/cited/γ-independent, the apparatus is provably non-blind (synthetic γ ordered to
the stages → ρ=+1.000; shuffle → ρ=−0.291), and the recorded grade is [V] iff a significant
positive rank correlation exists, else [O]. With the real data it is [O], and the gate passes
**because** the package reports that honestly. This **extends the project's central methodological
result** — γ fixes *what emerges* (order is a deterministic DNA readout) but does **not** predict
*when, vs. biology* — from external features to internal organs.

## Open levers (each DATA-blocked, not effort-blocked)

1. **Couple the schedule to Layer-2 anatomy** (`assemble.anatomy_spec`): drive the organ ellipsoids'
   appearance/size by `tau_on`/`dwell` so a grown organism fills with structure in γ-order. This is
   geometry (addable now), still **not** a timing-validation claim.
2. **A different measured modality** for organ timing (expression-onset / chromatin accessibility at
   the organ master loci) — the only honest lever left to test "DNA predicts organ timing", and it
   is **[O] data-blocked** (needs an external organogenesis atlas as a locked input; none in package),
   exactly as for the external-feature line.
3. **Widen the crisp-staged organ set** (e.g. thyroid, adrenal, gonad) to lift permutation power —
   blocked by input quality (clean [V] master + crisp single-CS staging), like the n=10 external set.
