# CHARTER — Immune and Hematologic Emergence: Clonal Selection, Inflammation Bistability, and Immunosurveillance

**paper_id:** `immune_hematologic_vp_site`  ·  **code:** `imm`  ·  **branch:** jamming (population-threshold / clonal selection)  ·  **version:** 0.10.0-research

## Scope (one line)
Thymus, spleen, marrow hematopoiesis and the adaptive lymphoid compartment emerge as a population of R19 switches: a cell is ON/OFF activated, inflammation is a bistable latch, and immunosurveillance modulates every other package's cancer kernel.

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental order*
are owned by the DNA morphogenesis gene-clock and CITED here (measured γ, never fitted). All four master-gene γ are now **measured** via the validated SantaLucia-1998 nearest-neighbour
pipeline (the two previously known values, FOXN1/TLX1, are reproduced bit-exact from cache, validating
the method/window/strand convention; RUNX1=1.3225, PAX5=1.4892 were then measured identically). γ is
measured input, never fitted. **v0.3.0 — primary-source verified:** all four promoter windows were
re-fetched LIVE from NCBI nuccore by their exact accession + 1-based window + efetch strand and verified
byte-for-byte (sha256) against the cache (assembly GRCh38.p14), with γ recomputed identical; NCBI-Gene
RefSeq corroborates each gene→organ master and chromosome. The core science object is byte-identical to
v0.2.0 (circulate() sha unchanged) — this is an added verification layer, not a re-fit. Frozen proof +
offline gate: `inherited/ncbi_verification.json`, `inherited/ncbi_gene_refseq.json`,
`inherited/ncbi_verify.py` (OFFLINE_check / ONLINE_reverify).

### Organs
- **thymus** (`FOXN1`) — γ=1.4533 (vendored, measured [V]) — T-cell positive/negative selection (threshold gating) — *dyn:* population — *rate anchor:* thymic selection threshold [L]
- **spleen** (`TLX1`) — γ=1.4228 (vendored, measured [V]) — blood filtration + lymphoid white pulp — *dyn:* population — *rate anchor:* spleen identity [V] (visceral atlas)
- **bone_marrow_hematopoiesis** (`RUNX1`) — γ=1.3225 (measured [V], SantaLucia-1998 pipeline) — HSC -> lineage branching (clonal) — *dyn:* population — *rate anchor:* lowest γ ⇒ earliest emergence (T3 endpoint, matches yolk-sac/AGM)
- **lymphoid_adaptive** (`PAX5`) — γ=1.4892 (measured [V], SantaLucia-1998 pipeline) — B/T clonal selection + immune memory — *dyn:* population — *rate anchor:* highest γ ⇒ latest emergence + most stable memory (largest barrier)

## Physical-class boundary (why these organs are one package)
Decomposition is by **physical regime / coupling topology**, not textbook organ-system labels. This
package is the **jamming (population-threshold / clonal selection)** class. Anything outside that class belongs to a sibling package and
is reached only through the cited seam variables — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- circulatory: leukocyte trafficking / transport (cited)
- musculoskeletal: marrow cavity (hematopoiesis site)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- immune_escape_factor -> ALL oncology modules (cross-cutting immunosurveillance modulator)

## Discriminant targets (ALL PASS — writing unlocked)
- T1 clonal activation: affinity drive past spinodal flips the cell ON (R19 saddle-node) [V] — PASS
- T2 inflammation hysteresis: acute resolves, chronic latches (bistable hysteresis, loop=2×spinodal) [V] — PASS
- T3 lineage order: developmental order is a γ readout; endpoints sign-validated vs embryology [V]/[L], middle pair [O] — PASS
- T4 immune memory: persists after antigen clears; erase-drive=spinodal; stability∝barrier (=γ order) [V] — PASS
- T5 immunosurveillance: immune_escape_factor scales tumor net burden in the shared kernel (cross-cutting) [V] — PASS
- **T6 emergent lineage (v0.4.0)**: order EMERGES from a shared-drive race (not a γ-sort) — 4 R19 switches under one rising drive commit in spinodal order; measured commit-h spacing = forced spinodal spacing; bone-marrow first robust (P=1.0) [V]; spleen↔thymus middle pair stays [O], now QUANTIFIED (smallest gap ≈ jitter; washes out under noise) — PASS
- **T7 emergent carcinogenesis (v0.4.0)**: the convex super-linear dose-response AND the Kramers rate law EMERGE from a direct stochastic Langevin barrier-crossing simulation (measured, not assumed; log-rate∝barrier R²≈0.98, slope recovers −1/D) [V]; absolute steepness/noise scale D [O] — PASS
- **T8 emergent memory lifetime (v0.5.0)**: durability EMERGES from a direct stochastic ON→OFF escape simulation (drive removed) — measured mean first-passage lifetime ranks ascending γ (37.5 < 55.8 < 64.0 < 76.9) and the Kramers escape law emerges (log-rate∝barrier R²≈0.998, slope recovers −1/D) [V]; absolute lifetime/noise scale D [O] — PASS
- **T9 emergent acute/chronic boundary (v0.5.0)**: the chronicity boundary EMERGES in the (insult amplitude × duration) plane from a stochastic pulse simulation — measured critical amplitude = each organ's spinodal (within 1%), sub-spinodal never latches (P≈0.03), monotone dose×duration tradeoff (dwell 550→400→300→150) [V]; noise scale D [O] — PASS
- **T10 emergent surveillance seam (v0.5.0)**: the multiplicative seam EMERGES from a coupled stochastic influx(R19-crossing)–clearance simulation — measured burden is monotone in escape and, rescaled by influx, AML and lymphoma collapse onto the SAME 1/(1−escape) multiplier (max cross-site gap 0.0043) [V]; absolute scale K, μ0 [O] — PASS
- **T11 emergent clonal-selection threshold (v0.6.0)**: the activation threshold EMERGES from a direct stochastic rising-affinity ramp — the measured commit-drive equals each organ's spinodal (ratio ≈ 0.98–1.00, approached from below by thermal activation), orders by γ, and a sub-spinodal drive stays tolerant while a supra-spinodal drive commits [V] (measured, not asserted from the closed-form spinodal); absolute noise scale D [O] — PASS
- **T12 emergent immunodominance (v0.6.0)**: clonal competition for one shared antigen pool EMERGES into a winner-take-all hierarchy — the higher-affinity clone commits first and depletes the pool, competitively excluding a subdominant clone (P≈1 alone, suppressed to ≈0.21), dominance sharpening monotonically with the affinity gap and symmetric at zero gap [V] (measured); absolute hierarchy depth [O] — PASS
- **T13 emergent therapy trajectories (v0.6.0)**: Levers A (differentiation re-flip) & C (drive removal) EMERGE as measured stochastic basin-occupancy trajectories — re-flip threshold = spinodal (non-cytotoxic), drive removal preventive-not-curative (committed persists, healthy prevented), and differentiation empties the malignant basin while drive-removal/cytotoxic leaves it occupied (relapse) [V] (measured); absolute dose/schedule + noise D [O] — PASS
- **T14 emergent Lever B barrier restoration (v0.7.0)**: the barrier-restoration rate collapse EMERGES as a measured crossing-rate-vs-restored-barrier trajectory (was the closed-form `exp(−barrier/kT)`) — as the carcinogen-eroded barrier is stepped back up the counted malignant crossing rate collapses monotonically (≈7.9× drop at full restoration) and log(rate) is linear in the restored barrier (R²≈0.99, slope recovers −1/D), the Kramers collapse measured in the therapeutic direction [V]; absolute factor / noise D [O] — PASS
- **T15 emergent Lever D surveillance restoration (v0.7.0)**: the surveillance clearance EMERGES as a measured time-domain reservoir-clearance trajectory (was the steady closed form) — from a high-escape reservoir, restoring surveillance makes the counted committed reservoir decay monotonically toward a floor that falls with deeper surveillance (floor × surveillance ≈ const → floor ∝ 1/(1−escape) = the T10 seam recovered as a trajectory endpoint; floors site-independent when rescaled by influx, gap ≈0.03) and clears faster the deeper the surveillance [V]; absolute scale K, μ0, D [O] — PASS
- **T16 emergent N-clone repertoire dominance (v0.7.0)**: repertoire-level immunodominance EMERGES from a coupled stochastic competition of N clones for one shared pool — a few high-affinity clones capture the response (measured participation ratio N_eff ≪ N; at N=12, N_eff≈5.9; commit probability monotone in affinity rank), the concentration sharpening with the affinity spread (N_eff 11.9→6.1) and, relative to N, with repertoire size, and symmetric at zero spread [V] (measured); absolute hierarchy depth [O] — PASS
- **T17 emergent cytotoxic relapse regrowth (v0.7.0)**: the relapse failure mode EMERGES as a measured regrowth time-course of a basin-gated population layer — cytotoxic killing leaves the basin intact so the malignant fraction regrows to ≥90% K (relapse) while a differentiating re-flip empties the basin so it decays to ≈0 (cure), and a deeper kill only lengthens the regrowth delay (time-to-half 0.0→4.7) while every depth fully recovers (relapse is basin-determined, not kill-depth-determined) [V] (measured); absolute growth rate / schedule [O] — PASS

> v0.4.0 discipline note: per the emergence principle, T6/T7 replace two previously-ASSUMED forms (a static
> γ-sort for order, a closed-form Kramers law for dose-response) with results MEASURED directly from
> stochastic substrate simulations. They live in the stress battery, not in `circulate()`, so the core
> determinism hash is byte-identical to v0.2.0/v0.3.0 — the emergent results are additive, never a re-fit.
>
> v0.5.0 discipline note: T8/T9/T10 extend the same principle to the last three still-analytic dynamical
> claims — memory durability (was asserted from the γ²/4 barrier), the acute/chronic boundary (was an
> asserted hysteresis loop), and the surveillance seam (was an asserted multiplicative factor). All three
> are now MEASURED from direct stochastic substrate simulations and likewise live only in the stress
> battery, so the core determinism hash is STILL byte-identical (`e7a2a5b8…`). What was promoted is the
> dynamical mechanism in each case; the absolute scales each leave behind (noise scale D, population
> constant K, clearance scale μ0) are stated [O] in the ledger — no fabricated absolute numbers.
>
> v0.6.0 discipline note: T11/T12/T13 complete the dynamical-mechanism programme. T11 promotes the clonal-selection threshold
> (was asserted as the closed-form spinodal) to a MEASURED rising-affinity ramp; T12 adds immunodominance as
> a genuinely new MEASURED result (coupled shared-antigen competition → winner-take-all); T13 promotes therapy
> Levers A & C (were evaluated by a deterministic settle) to MEASURED stochastic basin-occupancy trajectories.
> All three live only in the stress battery, so the core determinism hash is STILL byte-identical
> (`e7a2a5b8…`). With this, every dynamical MECHANISM in the package (T1–T13) is emergent; the only remaining
> [O] items are absolute scales (the cellular-noise scale D, population/clearance constants, hierarchy depth,
> and clinical dose/schedule) — each external to the no-tuning substrate and stated with its obstacle.
>
> v0.7.0 discipline note: T14/T15/T16/T17 finish FUTURE_WORK §A″ — they promote the last two therapy levers
> from closed forms to MEASURED trajectories and add two richer multi-body/temporal results. T14 emerges Lever B
> (barrier restoration) as a measured crossing-rate-vs-restored-barrier trajectory (Kramers collapse in the
> therapeutic direction); T15 emerges Lever D (surveillance restoration) as a measured time-domain reservoir-
> clearance trajectory (the dynamic twin of T10, recovering the seam as an endpoint); T16 generalises T12 to an
> N-clone repertoire and measures the dominance concentration and its scaling; T17 makes the relapse failure
> mode explicit as a measured basin-gated regrowth curve (relapse is basin-determined, not kill-depth-determined).
> All four live only in the stress battery, so the core determinism hash is STILL byte-identical (`e7a2a5b8…`).
> With this, all four therapy levers (A/B/C/D) are measured trajectories and relapse is an explicit measured
> curve; the only remaining [O] items are absolute scales (noise scale D, population/clearance/pool constants,
> growth/conversion rates, hierarchy depth, clinical dose/schedule) — each external to the no-tuning substrate
> and stated with its obstacle.

## Domain diseases + oncology scope (carcinogen → incidence)
Covers this physical class's diseases; the carcinogen-exposure mechanism (how much MORE cancer with
exposure) uses the shared R19 kernel (barrier-lowering → Kramers crossing → RR(dose)) with per-site
CITED epidemiological anchors. Grades: anchor [L] / dose-response shape [V] / absolute incidence [O].
- **acute myeloid leukemia** ← benzene (well-quantified); ionizing radiation; alkylating chemo
  - anchor/grade: benzene dose-response RR for AML (clean occupational anchor) [L]; shape [V]
- **lymphoma** ← ionizing radiation; immunosuppression; oncoviruses (EBV)
  - anchor/grade: RR vs exposure [L]; infection x immune-escape synergy [V]
- **immune-escape (cross-cutting)** ← chronic immunosuppression raises ALL-site crossing
  - anchor/grade: escape_factor modulates other packages' RR [V]; absolute incidence [O]

## Fundamental treatment levers (beyond visible mechanism — `repro/_therapy/`)
Reframing malignancy as an **attractor fact** (a lowered R19 barrier let the cell settle in an aberrant
basin), not a cell-count fact, forces four fundamental levers, each simulated deterministically against
the vendored substrate:
- **Lever A — basin re-flip (differentiation):** re-flip the malignant cell to a healthy basin at drive =
  spinodal, with NO cytotoxicity. Anchor [L]: APL (ATRA + arsenic trioxide), first non-cytotoxic cure of
  an acute leukemia.
- **Lever B — barrier restoration:** raise the barrier → Kramers crossing rate collapses exponentially; v0.7.0
  MEASURED as a crossing-rate-vs-restored-barrier trajectory (≈7.9× drop at full restoration, log-rate linear in
  restored barrier, Kramers collapse emerges in the therapeutic direction, T14) [V].
- **Lever C — drive removal (etiologic):** removing the carcinogen drive prevents un-committed crossings
  but, by hysteresis, does NOT reverse a committed cell → preventive, not curative alone [V]/[L].
- **Lever D — surveillance restoration (this package's seam):** lower immune_escape_factor → clear the
  committed reservoir at fixed crossing-rate; a common multiplier across every site; v0.7.0 MEASURED as a
  time-domain reservoir-clearance trajectory (reservoir decays to a floor ∝ 1/(1−escape) = the T10 seam recovered
  as a trajectory endpoint, faster clearance with deeper surveillance, T15). Anchor [L]: CAR-T /
  checkpoint blockade, curative in refractory leukemia/lymphoma.
- **Cytotoxic-only contrast:** killing cells leaves barrier+basin unchanged → the basin refills →
  hysteretic relapse. The kernel predicts fundamental cures are attractor/field-level and non-cytotoxic;
  the two cleanest real hematologic cures (differentiation in APL = A, surveillance in CAR-T = D) are
  exactly the two strongest predicted levers (falsifiable). HONESTY: VP does not invent these therapies;
  it re-derives why they are the fundamental class and names the cytotoxic relapse failure mode. Molecule/
  dose/patient response is [O] (outside the deterministic substrate).

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and C1/C3 in research.
  Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and
  research signed off (START_HERE §5). **(Satisfied this session: full T1–T17 + 4 therapy levers battery
  all_green=True, research_complete.json written (hash e7a2a5b8…), PHASE=writing, docs/ rebuilt — hub + 7
  chapters with the T16 repertoire (chapter 1) and the T14 Lever B / T15 Lever D / T17 relapse-regrowth
  measured numbers (chapter 7) spliced in.)**
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state
  passes by files only, next session resumes from the single zip (C0, §1, §5).
