# ANALGESIC AXIS — Musculoskeletal (v0.7.0)

Every painful musculoskeletal disease this package owns now also carries its **non-opioid analgesic logic**,
documented as a four-page canonical cluster (§25–§28) on the **same DNA-grounded substrate** as the disease and
treatment axes. This axis **inherits the three-lever non-opioid analgesic technique** from the VP non-opioid
analgesic volume (**concept DOI 10.5281/zenodo.20733420**) and applies it actively to the owned diseases — it is
not a restatement of that volume but its application on this package's measured switches.

## This adds no new physics — it is the inherited technique on a switch the genome built

The analgesic axis introduces **no new free parameters and no new organ**. Pain is modelled as a
**threshold-crossing rate on the same R19 escape barrier ΔV = γ²/4** the diseases already perturb:

> A nociceptor terminal is an excitable R19 element. A noxious drive **h** erodes its escape barrier and it fires
> at a Kramers rate, rate ≈ exp(−ΔV_eff/D), with ΔV_eff = max(0, γ²/4 + ΔV_L1 − κ·h). The perceived signal is a
> downstream gain g times that rate.

For bone, RUNX2 gives **γ = 1.2414**, read (not fitted) from assembly **NC_000006.12** by the identical DNA
pipeline used across the VP body-physiology program. The noxious drive **h is READ from each disease kernel's own
cited severity** (single source) — never invented, never tuned to a pain score.

## The three levers (inherited verbatim, exactly as the R19/FHN primitives are vendored)

Every non-opioid analgesic pulls exactly one of three levers:

- **L1 — raise the peripheral threshold** (ΔV_L1 ↑ → rate ↓). Anchors: local anaesthetics / Na_v blockers,
  topical agents. **Structure-DECOUPLED.**
- **L2 — lower the noxious drive** (h ↓ → rate ↓). Anchors: NSAIDs/coxibs and — the musculoskeletal special case
  — mechanical unloading. **Structure-COUPLED.**
- **L3 — reduce the central gain** (g ↓ → signal ↓). Anchors: gabapentinoids, SNRIs. This is **CENTRAL gain,
  owned by neuro / mind** — reached only as a NAMED SEAM, never re-emerged here (SSOT).

Opioids act on a fourth, descending / μ-receptor lever; that is outside the non-opioid logic and is not modelled.

## The conceptual contribution: in this volume, analgesia and disease-modification converge on one knob

The musculoskeletal signature is that **the noxious drive IS the mechanical load knob the disease kernel already
perturbs.** So the L2 sweep that lowers the nociceptive crossing rate is the *same operation* that arrests the
lesion — analgesia and disease-modification converge on one knob. The **decisive, falsifiable discriminant** is the
contrast with L1:

> **L2 (lower drive)** lowers BOTH the crossing rate AND the disease's own structural loss (**coupled**).
> **L1 (peripheral block)** lowers the crossing rate but leaves the lesion FLAT (**decoupled**).

That coupled-vs-decoupled contrast is a real prediction the kernel makes and could fail — a lidocaine patch
quietens an arthritic knee without changing the cartilage, exactly as the model predicts. It is the proof that the
axis is a grounded kernel, not a relabelling.

## How each lever is verified (No-Tuning)

Each lever is a monotone sweep, intensity 0 → 1. It PASSes when the crossing rate (L1/L2) moves **monotonically
down**; the intensity is never tuned to a pain score, the **DIRECTION** is the result, and the real drug or load is
the cited **[L]** anchor for WHICH lever it pulls. Where a structural lesion term exists, the L2-coupled /
L1-decoupled cross-check must also hold.

## Documentation (VP-SPEC v1.8, answer-first, AI-search / Google ready)
- **§25** `25-analgesic-three-lever-threshold-logic/` — methodology + DNA grounding + scope ([V]).
- **§26** `26-analgesic-l2-drive-load-bearing-convergence/` — L2 on osteoarthritis, tendinopathy, stress fracture:
  the analgesia / disease-modification convergence ([V]).
- **§27** `27-analgesic-l1-threshold-coupled-decoupled-discriminant/` — the falsifiable coupled/decoupled test,
  plus osteolytic / myeloma bone pain ([V]).
- **§28** `28-analgesic-limits-and-central-gain-seam/` — L3 routed out to neuro/mind, opioid lever out of scope,
  exertional muscle pain (DIRECTION-only), neuropathic / fibromyalgia routing ([O] / scope).

Each page is answer-first (self-contained ≤60-word direct answer), carries a `ScholarlyArticle` + breadcrumb
JSON-LD with a page-specific `knowsAbout` keyword set, keeps paragraphs ≤3 sentences, links the technique back to
the inherited DOI, and passes the VP-SPEC subj45 (≤45), description (80–160), DOM (≤3000) and size (≤300 KB) limits.

## Applied to the EXISTING research cases (requirement: not only the new axis)

Each owned painful disease chapter now carries an **"Analgesic lever map (cross-reference)"** block that names its
lever classification and links to §25–§27 (SSOT: the levers are emerged once in §25–§28; the disease chapters only
cross-reference, never re-derive):

| disease chapter | lever classification | links to |
|---|---|---|
| §12 Osteoarthritis | primary **L2-coupled** (load = lesion); L1 decoupled | §26, §27 |
| §16 Stress fracture | **L2-coupled** (offload below endurance limit) | §26 |
| §17 Tendinopathy | **L2-coupled** (deload); eccentric rebuild is a separate up-step | §26 |
| §19 Osteolytic / myeloma bone | **L2-coupled** on resorptive drive (antiresorptive = mirror = analgesic) | §27 |
| §14 Dystrophy / sarcopenia (exertional muscle pain) | L1 + L2 **DIRECTION-only** (no discrete lesion to cross-check) | §28 |

## Where the axis lives (code)
- **Inherited primitive:** `inherited/analgesic_levers.py` (the three-lever threshold logic on the vendored R19
  substrate; constant `ANALGESIC_SOURCE_DOI = "10.5281/zenodo.20733420"`). Self-test passes.
- **Engine of the axis:** `repro/_disease/vp_msk_analgesia.py` (reuses `vp_msk_disease.py` verbatim — single source
  of truth; never touches the engine).
- **Gate/docs reshaper:** `repro/_verify/stress_tests.py::run_analgesia_suite()`.
- **Gate:** `repro/_verify/gates.py::research_gate()` requires `analgesia_all_inscope_levers_direction_ok`.
- **Runner:** `repro/run_all.py` section `[3d]`.
- **Open items:** analgesic-axis `[O]` entries in `IRREPRODUCIBILITY_LEDGER.md` (each names its obstacle).

## Result
- **4 scored painful diseases PASS by DIRECTION**, each with the L2-coupled / L1-decoupled cross-check holding:
  osteoarthritis, tendinopathy, stress fracture, osteolytic bone disease. In every case the in-scope L1 and L2
  levers lower the nociceptive crossing rate monotonically, and the L2 sweep also lowers the disease's own
  structural loss while the L1 sweep leaves it flat.
- **1 honest partial, graded with a stated obstacle (results, not failures):** exertional / overuse muscle pain
  (sarcopenia / myopathy context) has both an L1 and an L2 lever that lower the crossing rate by DIRECTION, but
  there is **no discrete contact-loss lesion** to run the coupled/decoupled cross-check, so it is graded
  DIRECTION-only and excluded from the hard gate (logged, never dropped).
- **Honestly out of scope (results, not failures):** **L3 central gain** (a neuro / mind property — named as a seam,
  not re-emerged); the **opioid descending / μ lever** (outside the non-opioid three-lever technique); and
  **neuropathic pain / fibromyalgia / central sensitisation** (routed to sibling volumes, as in §20).

## Determinism
The analgesic battery is a **separate module that reuses the disease kernels and never touches the engine**, so the
engine determinism hash is unchanged:
**`7cf99d3baa263c8029224af9f197e2ce2e4c0b957a4b5d3729c6b5c71757a126`** (2×sha256 identical). Research gate
`all_green: True`; writing unlocked; the build reproduces `docs/` byte-identically (idempotent).

Scope note: this is the *musculoskeletal* (mechanical-dynamics) volume of the broader VP body-physiology program
(see `VP_FRAMEWORK_MAP`). The analgesic axis stays strictly inside that boundary: L2 is fully owned (it is the load
knob the disease kernel perturbs), L1 is a DIRECTION result on the vendored substrate, and L3 central gain is
deferred to neuro / mind by named seam — pain is never re-emerged as a new organ.
