# FUTURE WORK — Immune / Hematologic (immune_hematologic_vp_site)

Forward roadmap for the next session. Read together with `IRREPRODUCIBILITY_LEDGER.md` (the canonical list
of every open `[O]` item with its obstacle) and `START_HERE.md` (current status). This file is planning only;
it states honestly what is attackable inside the deterministic substrate and what is not.

Discipline reminder (VP-SPEC, this package): **emerge, do not assume, do not fit.** A result is only
promoted to `[V]` if it is MEASURED from a direct stochastic substrate simulation (as T6/T7 were in v0.4.0),
never by calibrating to outside data. Anything that requires an external real-world number to pin an
ABSOLUTE scale is, by this discipline, permanently `[O]` in-package.

---

## ✓ DELIVERED in v0.20.0 — integumentary (skin) barrier seam LIVE-VERIFIED + reciprocal handshake; identity holds as closed-form (engine hash byte-identical)

The **second live cross-package verification against a real sibling engine**, and a **third distinct
cross-package outcome**. `INTEGRATED_ROADMAP §5` follow-up #2 (promote the skin barrier-immunity candidate) is
**RESOLVED** — and the answer is the honest middle: the adjacency is live-verified and reciprocally recognised,
but the identity stays immune-owned closed-form (not over-claimed as engine-verified, not retired). Hard
guarantee: **the determinism hash `e7a2a5b8…` is byte-identical** (the live verification is out-of-gate; the
immune-side contract is byte-identical with or without the sibling), battery 35/35, discipline 6/6 drift 0, **0
sibling imports** across 52 files.

1. **The barrier surface is real and shares the substrate (drift 0).** integumentary_vp_site v1.0.0 (concept DOI
   10.5281/zenodo.20754541) was loaded into the §18 live harness (`VP_SIBLING_INTEGUMENTARY=…`). Measured
   cross-volume substrate drift = **0** over γ∈{1.0, 1.3225, 1.4892} — the epidermal barrier and the immune
   tolerance machinery share one byte-identical R19 substrate, and the barrier surface the v0.18.0 candidate
   posited is real (epidermis TP63 spinodal 0.61335644, keratinocyte KRT14 spinodal 0.69962471).
2. **Reciprocal immune-seam handshake.** The skin volume, written independently, declares an immune out-seam in
   the other direction: its own seam manifest carries `out__immune_hematologic__urticaria` (mast-cell / histamine
   effector → immune_hematologic). Both volumes recognise the same barrier↔immune adjacency from opposite sides —
   a bidirectional cross-reference, now closeable.
3. **The identity stays immune-owned closed-form — not engine-verified, not contradicted.** The skin volume models
   the barrier structure, physical/thermal insult tolerance, pigment, appendages, and (notably) autoantibody-driven
   adhesion saddle-nodes (pemphigus/pemphigoid — the same R19 saddle-node formalism on a different compartment),
   but does NOT implement the immune tolerance switch (it names immune effects as un-modelled out-seams). So there
   is no epidermal tolerance threshold in the skin engine to equate; the epidermal-tolerance identity (induction =
   epidermal-antigen + spinodal(1.0)) remains the immune-owned closed-form result of barrier-surface agnosticism,
   now with a confirmed real surface. The absolute epidermal-antigen scale stays skin-owned [O]. **Three sibling
   volumes, three outcomes: gut = verified identity; musculoskeletal = retired identity; skin = adjacency-verified
   + reciprocal handshake (identity closed-form).**
4. **Seam layer + harness + docs** updated: `cross_references.json` skin record gains a `live_verification` block
   (drift 0, real epidermal surface TP63/KRT14, reciprocal immune out-seam, skin defers tolerance) and an
   `identity_disposition` block (was `identity_candidate`); the skin owner DOI is RESOLVED (10.5281/zenodo.20754541,
   no longer a placeholder). `seam_wiring.py` skin validator now checks `pointer_live_verified` +
   `reciprocal_immune_seam_present` + `real_epidermal_barrier_surface_confirmed` +
   `identity_immune_owned_closed_form_not_contradicted`, seam digest `11244fe4…`→`9357f23b…`; the harness gains an
   integumentary `SIBLINGS` entry (CONFIRMED), an integumentary live-check (substrate drift 0 + reciprocal-seam
   text check), and a live-verified skin block in the immune-side contract (byte-identical w/wo sibling), harness
   digest `3b26fd35…`→`2b07d4d5…`. New chapter 21 `21-integumentary-barrier-seam-live-verified` (answer-first 55
   words, D5-clean, grade [V]), rebuild → 22 pages. No new `[O]` (the epidermal-antigen-scale row is updated, not
   added); the absolute epidermal-antigen scale remains [O].

**Next:**
- **Respiratory barrier immunity** — still a NAMED candidate; promote when a respiratory/lung VP volume exists
  (add to the §18 live harness, confirm drift 0 + reciprocal seam / airway threshold == airway-antigen ± spinodal).
- **If the skin volume later adds an epidermal tolerance module** — re-test: if its epidermal threshold reduces to
  epidermal-antigen + spinodal(1.0), promote the skin identity to engine-verified; if not, retire it (the
  barrier-agnosticism proof + the gut seam survive either way).
- **Reconcile the musculoskeletal owner concept DOI** — the MSK volume (v0.7.0) has not registered its own concept
  DOI; reconcile when it does. (The skin volume's DOI is now resolved.)
- **Neuro-immune magnitude anchor** — the cortisol→T24-suppressor IN direction is sign-only [O]; a principled
  external [L] could pin its magnitude, ONLY if found without fitting.

---

## ✓ DELIVERED in v0.19.0 — musculoskeletal seam LIVE-VERIFIED, identity candidate RETIRED (honest negative, engine hash byte-identical)

The **first live cross-package verification against a real sibling engine**, and the **first recorded honest
negative on a cross-package identity**. `INTEGRATED_ROADMAP §5` follow-up #1 (promote the musculoskeletal niche
pointer to a verified identity) is **RESOLVED** — and the answer is that the identity does **not** hold, recorded
honestly rather than forced. Hard guarantee: **the determinism hash `e7a2a5b8…` is byte-identical** (the live
verification is out-of-gate; the immune-side contract is byte-identical with or without the sibling), battery
35/35, discipline 6/6 drift 0, **0 sibling imports** across 52 files.

1. **The pointer is LIVE-VERIFIED.** musculoskeletal_vp_site v0.7.0 was loaded into the §18 live harness
   (`VP_SIBLING_MUSCULOSKELETAL=…`). Measured cross-volume substrate drift = **0** over γ∈{1.0, 1.3225, 1.4892} —
   the immune hematopoietic root (RUNX1, spinodal 0.58538506) and the MSK bone-marrow niche sit on one
   byte-identical R19 substrate, so the one-way niche-housing pointer is now verified against the **real** MSK
   engine (no refit), upgraded from "verified against this volume's own substrate."
2. **The identity candidate is RETIRED on live evidence (honest negative).** The v0.17.0 named upgrade — "the
   niche hematopoietic-commit threshold == 0.58538506" — is **not** supported: the MSK volume builds the niche via
   OSTEOBLASTS (RUNX2, γ=1.2414, spinodal **0.53237264**), a different master gene and spinodal from the
   hematopoietic RUNX1 (0.58538506) — 0.53237264 ≠ 0.58538506 (gap 0.05301242), and the MSK engine exposes no
   marrow-niche hematopoietic-commit threshold. The niche **houses** hematopoiesis but is not the same R19 switch;
   the threshold-equality identity does not reduce. **The v0.17.0 falsifier fired exactly as written; nothing was
   tuned to rescue it; the pointer survives.** Biologically correct (the osteoblastic niche supports but is
   distinct from the HSC — different master regulators).
3. **Seam layer + harness + docs** updated: `cross_references.json` MSK record gains a `live_verification` block
   (drift 0, vendored MSK bone snapshot RUNX2) and an `identity_upgrade_RETIRED` block (was
   `identity_upgrade_candidate`); `seam_wiring.py` MSK validator now checks `pointer_live_verified` +
   `identity_upgrade_retired_on_live_evidence` (recomputing both spinodals from the substrate to confirm they
   differ), seam digest `95bcde4d…`→`11244fe4…`; the harness immune-side contract MSK block gains the vendored
   live-verification + retired-identity verdict (byte-identical w/wo sibling), harness digest `a9d92643…`→
   `3b26fd35…`; the harness MSK `SIBLINGS` entry is marked CONFIRMED (no longer provisional). New chapter 20
   `20-musculoskeletal-seam-live-verified` (answer-first 56 words, D5-clean, grade [V]), rebuild → 21 pages. No
   new `[O]` (the bone-niche scale row is updated, not added); the absolute bone-niche scale remains [O].

**Next:**
- **Promote respiratory / skin from named candidates to VERIFIED identities** — when a respiratory or skin VP
  volume exists, add it to the §18 live harness and confirm substrate drift 0 + its barrier threshold ==
  barrier-antigen ± spinodal; on success, promote from named candidate to declared shared-substrate identity.
  (The same live-harness machinery just exercised on the MSK volume applies directly.)
- **Reconcile the musculoskeletal owner concept DOI** — the MSK volume (now confirmed on disk at v0.7.0) inherits
  only the analgesic-technique DOI and has not registered its own concept DOI; reconcile the TO-RECONCILE
  placeholder when it does. Never fabricate one.
- **Neuro-immune magnitude anchor** — the cortisol→T24-suppressor IN direction is sign-only [O]; a *principled
  external [L]* could pin its magnitude, ONLY if found without fitting (else it stays sign-only [O] by discipline).

---

## ✓ DELIVERED in v0.18.0 — barrier-surface mucosal immunity (5 declared seams + 2 named candidates, engine hash byte-identical)

`INTEGRATED_ROADMAP §5` candidates **#1 (respiratory)** and **#2 (skin)** are **DONE as named candidates**: the
gut–immune shared-substrate identity is shown to GENERALISE to other barrier surfaces, and the first two beyond
the gut are named (not claimed). Hard guarantee: **the determinism hash `e7a2a5b8…` is byte-identical** (the
barrier-surface result is closed-form and feeds nothing hashed-core; the seam layer carries its OWN 2×sha256),
battery 35/35, discipline 6/6 drift 0, **0 sibling imports** across 52 files.

1. **Barrier-surface agnosticism** (the structural footing, owned + verified here). The gut saddle-node identity
   (induction = antigen + spinodal(1.0); maintenance = antigen − spinodal(1.0)) is BARRIER-SURFACE-AGNOSTIC: across an
   illustrative 5-point antigen sweep ({0.30, 0.40, 0.50, 0.60, 0.70}) at g=1.0, the surface-independent OFFSET from a
   surface's own antigen baseline is INVARIANT == ±spinodal(1.0) = ±0.38490018 to the eighth decimal. The gut (antigen
   0.50 → induction 0.8849, maintenance 0.1151) is the ONE vendored, live-verified point on a barrier-agnostic line.
   CLOSED-FORM [F], resting on the MEASURED [V] T23 saddle-node + T24 suppressor complement.
2. **Respiratory — airway-mucosa tolerance** (NAMED candidate). A future respiratory/lung VP volume would localise
   this volume's T23/T24 switch to the airway mucosa; by agnosticism its airway induction threshold would equal
   airway-antigen + spinodal(1.0) in closed form. NAMED candidate, NOT a declared seam — it needs the live respiratory
   volume + that volume's OWNED absolute airway-antigen scale [O]. Owner DOI a TO-RECONCILE placeholder (never fabricated).
3. **Skin — epidermal-barrier tolerance** (NAMED candidate). Likewise for the epidermal barrier, the third surface on
   the same barrier-agnostic line; epidermal induction == epidermal-antigen + spinodal(1.0). NAMED candidate, not a
   declared seam — needs the live skin volume + its OWNED absolute epidermal-antigen scale [O]. Owner DOI TO-RECONCILE.
4. **Seam layer + harness + docs** extended: `seam_wiring.py` gains three functions (`barrier_surface_agnostic`,
   `respiratory_barrier_immunity_candidate`, `skin_barrier_immunity_candidate`) + 8 firewall tokens (`respirat`/`airway`/
   `pulmonary`/`vp_resp`/`epiderm`/`cutaneous`/`vp_skin`/`dermat`; still 0 imports), seam digest `9d3c0c87…`→`95bcde4d…`;
   the §17 harness gains a barrier-surface block in the immune-side contract (closed-form, no sibling added to SIBLINGS),
   harness digest `b0bef325…`→`a9d92643…`. New chapter 19 `19-barrier-surface-mucosal-immunity` (answer-first 50 words,
   D5-clean), rebuild → 20 pages.

Two new `[O]` items recorded in the ledger: the absolute airway-antigen scale (respiratory-owned, future volume) and the
absolute epidermal-antigen scale (skin-owned, future volume).

**Next:**
- **Promote the musculoskeletal marrow-niche pointer to a VERIFIED shared-substrate identity** — still BLOCKED on the
  musculoskeletal volume (not on disk this session); add it to the §17 live harness `SIBLINGS`, reconcile the provisional
  engine path, and confirm substrate drift 0 + niche threshold == bone_marrow_hematopoiesis spinodal 0.585385.
- **Promote respiratory / skin from named candidates to VERIFIED identities** — when a respiratory or skin VP volume
  exists, add it to the live harness and confirm substrate drift 0 + its barrier threshold == barrier-antigen ± spinodal;
  on success, upgrade the seam type from named candidate to declared shared-substrate identity.
- **Neuro-immune magnitude anchor** — the cortisol→T24-suppressor IN direction is sign-only [O]; a *principled external
  [L]* could pin its magnitude, but ONLY if found without fitting (else it stays sign-only [O] by discipline).

---

## ✓ DELIVERED in v0.17.0 — circulatory + musculoskeletal spokes (hub 3→5, engine hash byte-identical)

`INTEGRATED_ROADMAP §5` candidate #3 is **DONE**: the two inherited adjacencies are promoted from §4 to declared
one-way-pointer seams in `cross_references.json` (now §3), so the immune hub has **five spokes**, not three.
Hard guarantee: **the determinism hash `e7a2a5b8…` is byte-identical** (both pointers READ engine output and never
feed the hashed core; the seam layer carries its OWN 2×sha256), battery 35/35, discipline 6/6 drift 0, **0 sibling
imports** across 52 files.

1. **Circulatory — leukocyte trafficking** (one-way pointer OUT). This volume's leukocyte effector populations (R19
   ON-committed clones, rooted at `bone_marrow_hematopoiesis`, RUNX1, γ=1.3225, spinodal 0.585385) traffic through the
   circulatory vasculature — a one-way pointer that consumes no circulatory value and lands on a real in-package organ.
   Immune owns the effector populations [V]; circulatory owns the absolute vascular transport scale [O] (owner DOI
   10.5281/zenodo.20754354).
2. **Musculoskeletal — marrow niche** (one-way pointer + **named** identity-upgrade candidate). The hematopoietic root
   (`bone_marrow_hematopoiesis`, spinodal 0.585385, barrier 0.437252) is housed in the musculoskeletal marrow niche —
   declared as the weaker, verifiable-from-this-zip one-way pointer. The shared-substrate identity (niche threshold =
   0.585385, the gut-seam pattern) is NAMED with a promotion path + falsifier but NOT claimed, because verifying it
   needs the live musculoskeletal engine (absent in this zip). Owner DOI is a TO-RECONCILE placeholder (never fabricated).
3. **Seam layer + live harness** extended: `seam_wiring.py` gains two validators (firewall tokens `musculo`/`skelet`/
   `vp_msk`/`msk_engine` added; still 0 imports), seam digest `ead505bb…`→`9d3c0c87…`; the §17 harness gains
   circulatory/musculoskeletal `SIBLINGS` rows (provisional engine paths) + two pointer endpoints in the immune-side
   contract + live drift checks that SKIP cleanly when absent, harness digest `78f5696c…`→`b0bef325…`. New chapter 18
   `18-circulatory-musculoskeletal-spokes` (answer-first 51 words, D5-clean), rebuild → 19 pages.

Two new `[O]` items recorded in the ledger: the absolute vascular transport scale (circulatory-owned) and the absolute
bone-niche scale (musculoskeletal-owned).

**Next:**
- **Promote the musculoskeletal marrow-niche pointer to a VERIFIED shared-substrate identity** — add the musculoskeletal
  volume to the §17 live harness `SIBLINGS` (reconcile the provisional engine path) and confirm, against the live
  engine, substrate drift 0 AND the niche threshold == the bone_marrow_hematopoiesis spinodal 0.585385. On success,
  upgrade the seam type from one-way pointer to shared-substrate identity.
- **Respiratory mucosal immunity** spoke — a future respiratory/lung VP volume would localise the same T23/T24
  tolerance switch to the airway mucosa (the gut–immune seam pattern re-applied to a different barrier surface).
- **Skin barrier immunity** spoke — likewise for the epidermal barrier; both are the gut–immune *shared-substrate
  identity* seam type re-used, with the absolute barrier-antigen scale owned by the respective barrier volume.

---

## ✓ DELIVERED in v0.16.0 — cross-package SEAM layer + LIVE harness + integrated roadmap (engine hash byte-identical)

The intra-package roadmap (§A through §A⁶, T6–T35) is **EXHAUSTED**: thirty-five targets from clonal selection
through immunosenescence all read out one R19 substrate. The natural next growth is **OUTWARD** — the immune
system is where three other VP volumes physically meet. v0.16.0 wires those seams, verifies them live, and
re-frames the roadmap around the immune hub. Hard guarantee: **the determinism hash `e7a2a5b8…` is byte-identical**
(seam + harness READ engine output and never feed the hashed core; each carries its OWN 2×sha256), battery 35/35,
discipline 6/6 drift 0.

1. **Cross-package SEAM layer** (`repro/_seams/seam_wiring.py`, own digest `ead505bb…`; SSOT
   `inherited/cross_references.json`; chapter 16 `16-cross-system-seams-wired`). Three seams on the byte-identical
   substrate, **zero sibling imports** (52-file scan, 0 violations), emergence state mind-free:
   - **Gut–immune** (shared-substrate identity) — digestive's IBD mucosal latch IS this volume's tolerance switch
     localised: induction 0.8849 = antigen 0.50 + spinodal 0.3849 (T23 saddle-node), maintenance 0.1151 = antigen −
     spinodal (T24 suppressor complement), relapsing = T23 irreversibility, all closed-form. Immune owns the systemic
     tolerance primitive; digestive owns the mucosal localisation + absolute antigen scale [O].
   - **Neuro–immune** (two firewall-respecting directions) — IN: mind's HPA/cortisol → T24 suppressor σ as a SIGN
     only (magnitude [O], σ swept, no value imported); OUT: T31 cytokine tone M → one-way pointer to mind's
     inflammatory contributor to depression (mind §27), felt low mood behind mind's Axis-A firewall.
   - **Oncology hub spoke** — the existing immune_escape_factor 1/(1−escape) multiplier on every cancer kernel
     (chapter 5, T10) + Lever D (T15) therapy face; the hub's first and oldest spoke.

2. **LIVE cross-package harness** (`repro/_harness/cross_package_harness.py` + `repro/run_harness.py`, contract
   digest `78f5696c…`; chapter 17 `17-live-cross-package-harness`). Runs OUTSIDE every gate, SKIPS cleanly when
   siblings are absent, loads siblings by FILE PATH (collision-safe, not import). Five live checks all PASS:
   substrate drift 0 (immune↔digestive, immune↔mind), digestive's live `ibd_relapsing_course()` reproduces the
   vendored thresholds AND equals this volume's T23/T24 saddle-node, mind's §27 names the HPA-cortisol (IN) and
   inflammatory (OUT) endpoints. Digest hashes ONLY the immune-side contract → byte-identical with or without siblings.

3. **Integrated roadmap** (`INTEGRATED_ROADMAP.md`) — re-frames the exhausted §A roadmap as the immune
   immunosurveillance/tolerance/inflammation **hub** roadmap: current spokes (oncology, gut–immune, neuro–immune) +
   already-inherited adjacent spokes (circulatory leukocyte trafficking, musculoskeletal marrow) + potential future
   spokes (respiratory mucosal immunity, skin barrier immunity).

Two new `[O]` items recorded in the ledger (each with stated obstacle + owner): the absolute mucosal antigen scale
(digestive-owned) and the cortisol→σ magnitude (mind/anchor-owned).

**Next (the hub grows by spokes, not intra-package targets):**
- **Respiratory mucosal immunity** spoke — a future respiratory/lung VP volume would localise the same T23/T24
  tolerance switch to the airway mucosa (the gut–immune seam pattern re-applied to a different barrier surface).
- **Skin barrier immunity** spoke — likewise for the epidermal barrier; both are the gut–immune *shared-substrate
  identity* seam type re-used, with the absolute barrier-antigen scale owned by the respective barrier volume.
- **Circulatory / musculoskeletal** — ✅ **DONE in v0.17.0** (see the v0.17.0 delivered block above): leukocyte
  trafficking and the marrow niche, inherited adjacencies through v0.16.0, are now declared one-way-pointer seams in
  `cross_references.json`, with the firewall and the byte-identical engine hash kept. The musculoskeletal seam carries a
  named shared-substrate-identity upgrade candidate awaiting a live cross-package run.

---


The cross-cutting speed pass flagged in v0.12.0 is now **done**, with a hard guarantee: **no frozen hash
changed and no gate was relaxed** (full battery determinism `e7a2a5b8…` byte-identical; discipline 6/6, drift 0).
Two changes, both targeting only the v0.12.0 discipline overhead — the dominant ~115 s stochastic stress
battery (T1–T33) is untouched (it owns the determinism hash and was already optimised in v0.11.0):

1. **Discipline gates run IN-PROCESS** (`repro/_discipline/run_discipline.py`). The harness now executes each
   gate's real `__main__` via `runpy.run_path(..., run_name="__main__")` instead of spawning five separate
   Python interpreters. Because it runs the *identical* `__main__` code, each `expected/*.json` is written
   byte-for-byte the same (frozen hashes verified unchanged), but the five interpreter startups are gone and
   the `inherited/` imports (`gamma_pipeline`, `vp_substrate`) load once and are reused across gates. Any
   non-`SystemExit` error fails closed (matches the old `returncode != 0`).
2. **`run()` memoises its result for the process**, and **`gamma_pipeline.recompute_all()` memoises the γ
   recompute** (returning a deep copy each call so no caller can corrupt the memo). A battery that asks for the
   discipline result from both `run_all.py §[7]` and `gates.research_gate()` (and again via
   `write_research_complete`) now pays for **one** discipline pass, not two or three; the γ recompute
   (SantaLucia dG37 over 2501 bp × 4 genes) runs once.

Measured: full battery ≈131 s → ≈126 s; the discipline layer's own overhead ≈16 s → ≈10 s. The wall-clock win
is modest *by design* — the discipline layer is a small fraction of the battery and the large scientific
compute must stay byte-identical — but the redundant interpreter startups and the v0.12.0 double-run are
removed. No new `[O]`; no science changed.

> **Cross-cutting (still open): battery-level speed.** The remaining large cost is the stochastic stress
> battery itself (≈115 s). It is already down from 295.6 s (v0.11.0) and any further reduction must keep the
> `e7a2a5b8…` determinism hash byte-identical, so it is bounded by what can be vectorised WITHOUT changing the
> RNG stream. Treat as a separate, carefully-gated task — not a correctness shortcut.

---

## ✓ DELIVERED in v0.12.0 — concept DOI registered + inherited analgesic threshold-logic DISCIPLINE layer

Two cross-cutting deliverables, no new disease target (battery unchanged, 34/34 PASS, emergence hash
`e7a2a5b8…` byte-identical):

1. **Concept DOI registered** — `10.5281/zenodo.20755280`. The previous honest "pending registration"
   placeholder is gone; the real DOI now appears in every page's claim-strip + footer, in the
   `ScholarlyArticle`/`CreativeWorkSeries` JSON-LD (`identifier` PropertyValue + `sameAs` doi.org URL),
   in `llms.txt`, and in `docs/_meta.json`. Single source: `DOI`/`DOI_URL` constants in `tools/build_docs.py`.

2. **Inherited the `analgesic_threshold_logic_v2_0` discipline kernel** (DOI `10.5281/zenodo.20733420`) as a
   fail-closed layer under `repro/_discipline/` — **this is the technique the roadmap was previously missing,
   now inherited and actively applied** (see `ANALGESIC_TECHNIQUE_INHERITANCE.md` at package root for the full
   kernel spec + drop-in procedure for the other physiological packages). Five gates, run D1→D5 (firewall last),
   determinism-frozen (5 hashes, drift 0), wired into `gates.research_gate()` and `repro/run_all.py` §[7] so the
   research battery now fails closed without them:
   - **D1 inherit_reverify** — re-derive the 4 master γ (FOXN1/PAX5/RUNX1/TLX1) offline + recompute the R19
     spinodal/barrier, drift 0 (immune analogue of analgesic M1).
   - **D2 burden_prioritisation** — DECLARED-weight prioritisation that ranks **disease targets only** (never
     drugs/doses); γ and |h_sp| are carried as context but NEVER folded into the score (analgesic M10).
   - **D3 external_mechanism_honesty** — asserts every therapy lever's clinical anchor is graded cited-`[L]`,
     never derived `[V]`/`[F]`, and that the honest-limit/open-obstacle `[O]` + "does not invent" language is
     present (analgesic M11).
   - **D4 falsification_register** — a named, measurable falsifier for all 14 load-bearing claims + the
     framework (analgesic M6).
   - **D5 forbidden_claim_scan** — fail-closed FIREWALL, immune-tuned: forbids numeric dose/regimen, synthesis
     routes, novel-VP-efficacy, and safety claims, with a negation guard; allows cited-`[L]` cures and
     dose-RESPONSE biology; requires the disclaimers to be present (analgesic M5).

   **Cross-suite plan (기존 연구사례 적용 계획):** the same five-gate kernel is package-agnostic. A portable
   template lives in `_inheritance_kit/`; `ANALGESIC_TECHNIQUE_INHERITANCE.md` gives the exact drop-in steps for
   `circulatory_vp_site` (v0.7), `musculoskeletal_vp_site` (v0.4), the hemodynamic/homeostasis package, the
   digestive/metabolic package, and any future physiological volume — each re-tuning only the firewall pattern
   list + the target table, keeping the gate logic byte-identical.

> **Cross-cutting (✓ DELIVERED in v0.13.0): speed optimisation.** The v0.12.0 discipline layer spawned five
> subprocesses and ran 2–3× per battery; v0.13.0 made the gates in-process (`runpy`) and memoised both the
> discipline result and `recompute_all()`, byte-identical (no frozen hash changed). See the v0.13.0 entry above.

---

## ✓ DELIVERED in v0.11.0 — Disease/Treatment axis (T27–T33), the `immune_hematologic_DISEASE_TREATMENT_ROADMAP`

The disease/treatment roadmap is now **fully implemented** (T27–T33, battery 34/34 PASS, determinism hash
`e7a2a5b8…` byte-identical). One organizing claim was measured across six disease classes: **basin-acting
interventions are the durable class; drive-suppression-only is preventive-not-curative and relapses on
withdrawal.** Treatment is stated as DIRECTION/CLASS only — never a drug, dose, schedule, or recommendation —
and is NOT a validation of VP and NOT medical advice.

- **T27** therapeutic re-tolerization — `repro/_therapy/emergent_retolerization.py` (T23 break's therapeutic
  mirror; suppress_crit = 1 + residual = the negative saddle-node; durable vs relapsing).
- **T28** epitope spreading — `repro/_dynamics/emergent_spreading.py` (count-coupled clone cascade past κ_crit).
- **T29** allergic sensitization / desensitization — `repro/_dynamics/emergent_sensitization.py` (allergy =
  failure of the T26 ignorance regime; desensitization = controlled re-tolerization through the exposure axis).
- **T30** immunodeficiency reconstitution threshold — `repro/_therapy/emergent_reconstitution.py` (one
  surveillance lever, two diseases; threshold-gated reconstitution).
- **T31** systemic inflammatory latch + time-critical break window — `repro/_dynamics/emergent_sepsis_latch.py`
  (cytokine-tone self-sustaining latch; trigger-removal insufficient; break is time-critical).
- **T32** transplant allo-tolerance induction — `repro/_therapy/emergent_allotolerance.py` (T27 at a larger,
  time-deepening allo-load; suppress_crit = 1 + allo-load; alloreactive-consolidation induction window).
- **T33** lineage-targeted autoimmune cytopenia — `repro/_therapy/emergent_cytopenia.py` (T23 break attacking a
  produced lineage; T27 restores durably; T19 combination — support alone insufficient, combination faster to the
  same destination).

Writing: new chapter 8 `08-disease-treatment-axis-basin-acting-cures` (the synthesis). Battery runtime optimized
(295.6 s → ~115 s) by reducing per-module N / grid / step counts; the determinism hash is computed from
`circulate()` alone, so it is unaffected (verified). Remaining `[O]` is only absolute scale (suppression depth,
dose, counts, rates, window lengths, noise D) — all listed in the ledger.

Residual next steps on this axis (optional, future): individual SEO chapters per disease class (currently one
synthesis chapter covers all six); a quantitative biomarker layer would require external calibration and stays
permanently `[O]` in-package.

---

## A. Attackable by emergent simulation — ✓ DELIVERED in v0.5.0 (T8/T9/T10)

The three v0.4.0 candidates below were all implemented as direct measured simulations in v0.5.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table.

1. ✓ **Emergent memory lifetime (upgraded T4)** → `repro/_dynamics/emergent_memory.py` (**T8**). The ON-state
   R19 switch is run under noise with the drive removed and the escape-time is MEASURED. Result: mean
   first-passage lifetime ranks in ascending-γ order (bone-marrow 37.5 < spleen 55.8 < thymus 64.0 < lymphoid
   76.9) and the Kramers law emerges (log-rate linear in barrier, R²≈0.998, fitted slope recovers −1/D).
   Grade **[V]** ranking + escape law; absolute lifetime / noise scale D stays [O].

2. ✓ **Emergent acute/chronic boundary (upgraded T2)** → `repro/_dynamics/emergent_chronicity.py` (**T9**).
   A single switch is driven with pulses of varying amplitude × duration under noise and the landed basin is
   MEASURED. Result: the critical amplitude equals each organ's spinodal (within 1%), sub-spinodal insults
   never latch (P≈0.03 at the longest duration), and the dose×duration tradeoff is monotone (critical dwell
   550→400→300→150 steps). Grade **[V]** boundary shape; noise scale D stays [O].

3. ✓ **Emergent surveillance seam (upgraded T5)** → `repro/_oncology/emergent_seam.py` (**T10**). A coupled
   stochastic influx(R19-crossing)–clearance process is simulated and net burden vs escape is MEASURED.
   Result: burden is monotone in escape at both sites and, rescaled by each site's measured influx, the AML and
   lymphoma curves collapse onto the SAME 1/(1−escape) multiplier (max cross-site gap 0.0043; ideal form to
   within 0.0027). Grade **[V]** monotone + multiplicative + site-independent; absolute scale K, μ0 stays [O].

## A′. Next emergent candidates (T11/T12/T13) — ✓ DELIVERED in v0.6.0

The three v0.5.0 candidates below were all implemented as direct measured simulations in v0.6.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table.

1. ✓ **Emergent clonal-selection threshold (upgraded T1)** → `repro/_dynamics/emergent_selection.py` (**T11**).
   A resting clone is driven by a slowly rising affinity signal under noise and the commit-drive is MEASURED.
   Result: the commit-drive equals each organ's spinodal (ratio ≈ 0.98–1.00, approached from just below by
   thermal activation), the measured threshold orders by γ, and a sub-spinodal drive stays tolerant
   (P(commit) ≈ 0) while a supra-spinodal drive commits (P ≈ 1). Grade **[V]** threshold; absolute noise scale
   D stays [O].

2. ✓ **Emergent immunodominance / clonal competition (new)** → `repro/_dynamics/emergent_competition.py`
   (**T12**). Two clones of the same γ but different affinity compete for one shared antigen pool that committed
   clones deplete; the commit fractions, order, and subdominant suppression are MEASURED. Result: the
   higher-affinity clone commits first and competitively excludes a subdominant clone that commits with
   probability ≈ 1 alone (suppressed to ≈ 0.21 at the largest gap); dominance sharpens monotonically with the
   affinity gap and is a symmetric coin-flip at zero gap. Grade **[V]** competition existence/direction/
   monotonicity; absolute hierarchy depth stays [O].

3. ✓ **Emergent therapy trajectories (upgraded Levers A & C)** → `repro/_therapy/emergent_therapy.py` (**T13**).
   Levers A (differentiation re-flip) and C (drive removal) are MEASURED as stochastic basin-occupancy
   trajectories. Result: the Lever-A residual malignant-basin occupancy collapses from ≈ 1 to ≈ 0 across the
   spinodal with no cytotoxicity (measured 0.5-crossing ≈ 0.81× spinodal), Lever C is preventive-not-curative
   (committed occupancy ≈ 1 after drive removal, healthy ≈ 0), and differentiation empties the basin while
   drive-removal / cytotoxic killing leaves it occupied (relapse). Grade **[V]** reversal/relapse contrast;
   absolute dose/schedule (clinical) and noise scale D stay [O].

## A″. Next emergent candidates (T14/T15/T16/T17) — ✓ DELIVERED in v0.7.0

The four v0.6.0 candidates below were all implemented as direct measured simulations in v0.7.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table. With
this batch all four therapy levers (A/B/C/D) are measured trajectories and the relapse failure mode is an
explicit measured regrowth curve.

1. ✓ **Emergent therapy trajectory for Lever B (barrier restoration)** → `repro/_therapy/emergent_barrier_restoration.py`
   (**T14**). The carcinogen-eroded barrier is stepped back up and the malignant crossing rate is MEASURED by
   counting OFF→ON crossings of the stochastic R19 field at each restoration level. Result: the counted rate
   collapses monotonically (≈7.9× multiplicative drop at full restoration) and log(rate) is linear in the
   restored barrier (R²≈0.99, fitted slope recovers −1/D) — the Kramers collapse emerges in the THERAPEUTIC
   direction (the time-domain twin of T7). Grade **[V]** rate collapse + Kramers law; absolute factor / noise
   scale D stays [O].

2. ✓ **Emergent therapy trajectory for Lever D (surveillance restoration)** → `repro/_therapy/emergent_surveillance_clearance.py`
   (**T15**). Starting from a high-escape reservoir, surveillance is restored and the committed reservoir N(t)
   is MEASURED as it decays (the time-domain twin of T10). Result: the reservoir clears monotonically toward a
   floor that falls with deeper surveillance (floor × surveillance ≈ const → floor ∝ 1/(1−escape): the T10 seam
   recovered as a trajectory ENDPOINT), the AML and lymphoma floors collapse onto the same 1/surveillance curve
   when rescaled by influx (cross-site gap ≈0.03), and deeper surveillance clears faster. Grade **[V]** clearance
   trajectory + seam endpoint + site-independence; absolute scale K, μ0, D stays [O].

3. ✓ **Emergent N-clone repertoire dominance (extend T12)** → `repro/_dynamics/emergent_repertoire.py` (**T16**).
   The two-clone competition is generalised to N clones with a spread of affinities sharing one pool, and the
   dominance concentration is MEASURED from the per-clone commit probabilities. Result: a few high-affinity
   clones capture the response (participation ratio N_eff ≪ N; at N=12, N_eff≈5.9; commit probability monotone
   in affinity rank), the concentration sharpens monotonically with the affinity spread (N_eff 11.9→6.1) and,
   relative to N, with repertoire size (N_eff/N falls), and the zero-spread limit is symmetric (no spurious
   winner). Grade **[V]** concentration + spread/size scaling + symmetric zero-spread; absolute depth stays [O].

4. ✓ **Emergent cytotoxic relapse as a regrowth time-course (make relapse explicit)** → `repro/_oncology/emergent_regrowth.py`
   (**T17**). A population-growth layer gated by the MEASURED R19 basin fraction is added on top of T13. Result:
   after cytotoxic killing the malignant fraction regrows toward carrying capacity (≥90% K — relapse; basin
   intact, f≈1), after a differentiating re-flip it decays to ≈0 (≤10% K — cure; basin emptied, f≈0), and
   sweeping the kill fraction shows a deeper kill only lengthens the regrowth delay (time-to-half 0.0→4.7) while
   every depth still recovers fully — so relapse is basin-determined, not kill-depth-determined. Grade **[V]**
   relapse-vs-cure trajectory contrast + basin-determined relapse; absolute growth rate / schedule stays [O].

## A‴. Next emergent candidates (T18/T19/T20) — ✓ DELIVERED in v0.8.0

The three v0.7.0 candidates below were all implemented as direct measured simulations in v0.8.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table. With
this batch the adaptive compartment has a measured maturation trajectory, the relapse→cure conversion is
explicit, and antigenic imprinting emerges from the same shared-pool competition.

1. ✓ **Emergent affinity maturation (germinal-center selection)** → `repro/_dynamics/emergent_maturation.py`
   (**T18**). The repertoire (T16) is wrapped in an iterated mutation+reselection loop: each round the
   high-affinity clones commit first and deplete the shared pool, the committed parents are re-seeded with
   SYMMETRIC somatic hypermutation, and the mean affinity of the responding set is MEASURED round over round.
   Result: affinity rises monotonically (gain ≈0.20 / 7 rounds); the rise needs mutation (stalls ≈0.03 at zero,
   accelerates 0.07→0.22→0.39 with rate), needs competition (unlimited pool → neutral drift ≈0.0001), and pool
   pressure has an HONEST inverted-U optimum (peak ≈0.21 vs weak ≈0.04). Selection acts only on the competition
   outcome; nothing about improvement is imposed. Grade **[V]** direction / rate-shape / competition-required;
   absolute maturation rate stays [O].

2. ✓ **Emergent combination-therapy contrast (cytotoxic + differentiation / surveillance)** →
   `repro/_therapy/emergent_combination.py` (**T19**). The regrowth layer (T17) is extended to a five-arm
   contrast and the trajectory is MEASURED when a cytotoxic cull is combined with a basin-acting lever. Result:
   a cull that relapses ALONE (final 100% K) is converted to a cure (≈0) when paired with either differentiation
   re-flip or restored surveillance; the cull lowers the cumulative burden (area under N(t)/K 0.95→0.09 with
   differentiation, 0.64→0.09 with surveillance) but cannot cure on its own at any depth, and the surveillance
   channel reproduces the EXACT interior fixed point N*=K(1−μ/r) (70% K at μ=0.3 sub-threshold; cure above the
   growth-rate threshold). Cure is basin/niche-acting, not kill-driven. Grade **[V]** relapse→cure conversion /
   cull-accelerates / growth-rate threshold; absolute rates + schedule stays [O].

3. ✓ **Emergent cross-reactivity / original-antigenic-sin** → `repro/_dynamics/emergent_crossreactivity.py`
   (**T20**). A matured memory clone (recall head-start, still OFF, affinity degrading with antigenic distance)
   is re-stimulated against a fresh better-matched naïve clone on one shared pool and the recall bias is
   MEASURED vs antigenic distance. Result: at intermediate distance the experienced clone is preferentially
   recalled even though the naïve clone is strictly better-matched (P(memory)≈0.77), the bias decays
   monotonically (0.77→0.49→0.18) until the naïve clone wins (P(naïve)≈0.75 far), and removing the head-start
   abolishes the bias entirely (P(memory) 0.20/0.04/0.00) — the imprint is experience-driven, not
   affinity-driven. Grade **[V]** imprinting existence / decay-with-distance / recall-control; absolute
   magnitude stays [O].

## A⁗. Next emergent candidates (T21/T22/T23) — ✓ DELIVERED in v0.9.0

The three v0.8.0 candidates below were all implemented as direct measured simulations in v0.9.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table. With
this batch the adaptive compartment has measured central tolerance, a measured vaccination-scheduling optimum,
and a measured autoimmune tolerance break — the deletion mirror of selection and the pathological mirror of
memory now both emerge from the same one switch.

1. ✓ **Emergent central tolerance / clonal deletion (negative selection)** →
   `repro/_dynamics/emergent_negative_selection.py` (**T21**). The positive-selection ramp (T11) is run with the
   opposite sign: a self-reactive clone crossing ON in the thymic context is DELETED, and the deletion drive is
   MEASURED via a quasi-static ramp. Result: the deletion threshold equals each organ's spinodal (ratio
   0.998–1.003) and orders by γ; a sub-threshold self-drive is ignored (P(delete)≈0.00) and a supra-threshold one
   reliably deleted (P=1.0); educating a uniform self-affinity spread through the channel caps the exported
   self-affinity at the spinodal (max 1.016×) and empties the autoreactive tail (0.000 with the channel on vs
   0.450 off, 55.4% deleted) — deletion is REQUIRED, not incidental. Grade **[V]** deletion-threshold=spinodal /
   ceiling / channel-required; absolute deletion rate + escaped-sliver width stay [O].

2. ✓ **Emergent prime–boost vaccination scheduling** → `repro/_dynamics/emergent_prime_boost.py` (**T22**). The
   maturation loop (T18) is run as a fixed-length campaign with a slowly-clearing antigen depot; the matured
   affinity is MEASURED vs the boost interval. Result: an inverted-U with an INTERIOR optimum (gain peaks ≈0.42
   at interval 4) — boosting every round over-supplies the depot (mean pool ≈4.2) into T18's weak/large-pool
   regime and starves selection (≈0.15), spacing too far under-uses the fixed campaign (≈0.34); clamping the
   depot cap to the productive pool removes the over-supply penalty and moves the optimum to the most-frequent
   boundary (≈0.49 at interval 1), proving the optimum is depot-driven. The temporal face of the T18 inverted-U.
   Grade **[V]** interior-optimum / over-supply-mechanism / control; absolute optimal interval stays [O].

3. ✓ **Emergent autoimmune bistable break (tolerance loss)** → `repro/_dynamics/emergent_autoimmunity.py`
   (**T23**). The chronicity latch (T9) is combined with a T21 escaped clone (sub-spinodal residual self-drive →
   bistable) and the tolerance-break boundary is MEASURED under an inflammatory insult pulse. Result: the break
   boundary is the switch saddle-node — across a residual-drive sweep the critical TOTAL drive (residual + insult)
   stays at the spinodal (sum 0.95–1.00×), so self-antigen and inflammation are interchangeable (critical insult
   falls 0.999→0.599→0.151× as the residual deepens); the break is IRREVERSIBLE (P(break)=0.977, unchanged at
   tripled settle; sub-threshold resolves 0.025; far-below safe 0.002) with a dose×time tradeoff (dwell
   550→300→150); and because the critical insult shrinks as the residual nears the deletion threshold, DEEPER
   negative selection (T21) lowers susceptibility — the T21→T23 link. Grade **[V]** saddle-node-boundary /
   irreversible-persistence / deletion-depth-susceptibility; absolute break rate stays [O].

## A⁵. Next emergent candidates (T24/T25/T26) — ✓ DELIVERED in v0.10.0

The three v0.9.0 candidates below were all implemented as direct measured simulations in v0.10.0. Each kept
`circulate()` untouched (new work lives in the stress battery → the core determinism hash stayed byte-identical
at `e7a2a5b8…`), each PASSES in the gated battery, and each is documented in the ledger RESOLVED table. With this
batch the adaptive compartment has, alongside central deletion, a measured PERIPHERAL tolerance layer that adds to
it, a measured dynamical EXHAUSTION mirror of maturation, and a measured tolerance–immunity DOSE WINDOW — the full
tolerance/immunity dose axis now emerges from the same one switch.

1. ✓ **Emergent peripheral tolerance / regulatory suppression** → `repro/_dynamics/emergent_peripheral_tolerance.py`
   (**T24**). A subtractive suppressor field is applied to an escaped (T23) self-clone and the suppression at which
   it is re-contained is MEASURED. Result: the containment threshold is the saddle-node COMPLEMENT — σ_crit =
   (residual + insult) − spinodal organ by organ (σ_crit 0.245–0.251 vs the 0.250× overshoot, ratio 0.98–1.01), so
   the regulatory field cancels exactly the total-drive overshoot of the switch; the required suppression rises
   one-for-one with the escaped residual (slope ≈0.93≈1), so central deletion (T21) and peripheral suppression
   ADD; and suppression is REQUIRED (P(break) 0.978 at σ=0 → 0.107 at σ=0.40). Grade **[V]** complement-threshold /
   one-for-one-with-residual / required; absolute suppression strength + escaped-sliver width stay [O].

2. ✓ **Emergent immune exhaustion (chronic-antigen drive)** → `repro/_dynamics/emergent_exhaustion.py` (**T25**).
   An accumulating, antigen-gated negative-feedback variable is coupled to a committed R19 repertoire (the
   dynamical mirror of T18 maturation) and the response is MEASURED under chronic antigen. Result: the responding
   fraction rises then collapses to a hyporesponsive floor (peak 1.000 → floor 0.000, monotone); the collapse
   REQUIRES the feedback (floor 1.000 at κ=0); it is REVERSIBLE — antigen withdrawal lets the feedback decay so a
   re-challenge recovers to 1.000 while continued stimulation stays 0.000 (functional silencing, not deletion); and
   the onset is the switch's NEGATIVE saddle-node (exhausted fraction monotone in κ, measured onset κ≈1.68 near the
   closed form sp·(aff_mean·drive+1)≈1.875). Grade **[V]** collapse / feedback-required / reversibility /
   negative-saddle-node; absolute exhaustion rate + timing stay [O].

3. ✓ **Emergent tolerance–immunity dose window (hormesis)** → `repro/_dynamics/emergent_hormesis.py` (**T26**). The
   T21 central-deletion process and the T23 escaped-clone break are composed over a self-antigen dose sweep and the
   window edges are MEASURED. **Honest sign:** the roadmap framed this as a productive "safe-dose band"; the
   substrate gives the DUAL and it is reported as measured — an INTERIOR *danger* band (escape ∧ break, NET
   single-peaked, peak at d≈0.70) flanked by two SAFE regimes (ignorance below, central deletion above). The lower
   (break) edge = spinodal − insult and tracks the insult one-for-one (d_lo 0.800→0.631→0.447, slope ≈−0.88, with
   d_lo+insult = spinodal — the T11/T18 commit threshold); the upper (deletion) edge is insult-independent (fixed
   0.816×); the band width grows one-for-one with the insult (0.016→0.369, slope ≈+0.88) and collapses as the
   insult→0; and the window position tracks each organ's spinodal (deletion edge a constant fraction 0.79–0.82). The
   SLOPES are the clean falsifiable invariants. Grade **[V]** interior-band / ±1 edge-slopes / insult-independent
   upper edge / collapse / spinodal-tracking position; absolute band edges + width stay [O] (thermal lowering of the
   deletion edge fixes the upper edge below the deterministic spinodal, so absolute width carries a thermal offset).

## A⁶. Next emergent candidates (T27+, same spirit — emerge, do not assume) — ✓ FULLY DELIVERED

> **Status:** all four §A⁶ items are now delivered — #1 re-tolerization → **T27** and #2 epitope spreading → **T28**
> (v0.11.0, Disease/Treatment axis), #3 immunosenescence → **T34** and #4 durability-optimal re-boosting → **T35**
> (v0.14.0, chapter 09). Battery is **35/35 PASS**, determinism hash unchanged (`e7a2a5b8…`), discipline 6/6 drift 0.

With T1–T26 the adaptive compartment has the full tolerance/immunity dose axis — selection and its deletion mirror,
peripheral suppression, the repertoire, maturation and its vaccination optimum, imprinting, exhaustion, chronicity
and its autoimmune break, the dose window, all four therapy levers, and the relapse→cure conversion — all measured.
The remaining attackable dynamics compose these same measured processes into higher-order behaviour, same discipline
(emerge, do not assume; promote to [V] only if MEASURED; absolute scales stay [O] with a stated obstacle). In rough
priority:

1. **Emergent therapeutic re-tolerization (the autoimmune basin dual of T13/T17/T19).** Take a broken autoreactive
   clone (T23, latched ON) and apply a transient deep-suppression pulse (the T24 field driven hard, or a barrier
   restoration). MEASURE whether it can be pushed back across the saddle-node into the tolerant basin and whether
   the cure is DURABLE (basin-acting, stays tolerant after the pulse clears) or RELAPSES (refills like the cytotoxic
   contrast). Predict a measured re-tolerization threshold + a durability contrast mirroring the cure/relapse logic.
   Grade target: [V] threshold / basin-acting-vs-relapse; absolute pulse dose [O].
2. **Emergent epitope spreading / bystander cascade.** Once one self-clone breaks (T23), couple it to neighbouring
   self-clones through the shared-pool competition (T12/T16): MEASURE whether the break recruits adjacent clones
   past a cascade threshold (a measured spreading boundary) or stays contained, and how peripheral suppression (T24)
   raises that threshold. Grade target: [V] cascade threshold / suppression-raises-it; absolute spread rate [O].
3. **Emergent immunosenescence (thymic involution).** ✓ **DELIVERED in v0.14.0 as T34** —
   `repro/_dynamics/emergent_immunosenescence.py`. Runs the T21 thymic education over a slowly SHRINKING window;
   because positive selection (survival, a cumulative-engagement quota) and negative selection (deletion, an
   ON-crossing) are both time-costed crossings of the one R19 field, a shorter window truncates them in OPPOSITE
   directions. MEASURED: the escaped-autoreactive fraction RISES (0.29%→3.71%) while the naive-export rate FALLS
   (32.9%→15.9%), the two DIVERGE, the youngest window is clean+productive (control), and the escapees are
   near-threshold (T21's sliver widened by age). Grade [V] direction (escape ↑, output ↓) coupling; absolute
   timescale / engagement quota / s_pos / noise D [O]. (Chapter 09; battery 35/35; determinism hash unchanged.)
4. **Emergent durability-optimal re-boosting under waning.** ✓ **DELIVERED in v0.14.0 as T35** —
   `repro/_dynamics/emergent_durable_boost.py`. Measures the memory survival curve directly from the T8 ON-basin
   escape, reads the protection half-life t_θ, then marches a FIXED booster budget over a finite horizon at a
   sweep of intervals. MEASURED: the protected fraction is an INTERIOR-peaked function of the re-boost interval,
   maximised at interval ≈ the measured half-life (r*≈1 for every compartment); too-frequent boosting wastes the
   budget early, too-spaced opens gaps, the optimal interval TRACKS durability across compartments, and a
   no-decay control is flat (optimum is decay-driven). Distinct from the T22 maturation optimum. Grade [V]
   durability-optimum tied to the measured half-life; absolute interval / half-life / threshold θ / noise D [O].
   (Chapter 09; battery 35/35; determinism hash unchanged.)

## B. Could close a current [O] — but only if a principled in-substrate value exists

4. **The cellular-noise scale D — absolute steepness stays [O]; the "derive D from the physics substrate"
   route is RETIRED (v0.15.0, symbol-clash category error).** Today the immune noise term D is a free
   *dimensionless* amplitude, so the dose-response *shape* and the Kramers *law* are [V] but the absolute
   *steepness* is [O]. An earlier note proposed closing this by mapping D onto the parent physics volume's
   intrinsic fluctuation scale. **That route is now DISCARDED** — it was a category error from a reused
   symbol. physics's `D = 4.852620477 pm` is the *quantum diameter* (the jammed-sphere diameter, a LENGTH
   that fixes light geometry: integer dent-chain, sin χ = λ/(mD), physics §10.9; source physics
   `verification_dossier/GROUNDING_LEDGER.md`), whereas the immune package's "noise scale D" is the
   *dimensionless amplitude* of the Langevin stochastic drive on the R19 bistable switch — the mesoscopic
   cellular fluctuation that sets the thermal activation rate over the spinodal barrier. The two carry
   DIFFERENT UNITS (dimensionless amplitude vs pm length): cellular noise comes from molecular copy-number
   statistics (√N, ~nm–µm scale), not from the vacuum particle diameter (pm). There is therefore no clean
   map to force, so the immune noise's absolute steepness is left honestly [O] (every shape and law is
   already [V]). *(User note: this small a scale is not needed — 4.85 pm is the value used for
   electromagnetic waves / light.)*

## C. Permanently open in-package (need an external anchor — do NOT fabricate)

Listed so they are never mistaken for unfinished work. Each needs a real-world number that the no-tuning
substrate cannot supply; the package already states each as [O] with its obstacle in the ledger.

- **Absolute organ size / mass** — DWELL ∝ γ^1.5 fixes RELATIVE size/order [F]; the absolute scale needs one
  external calibration point.
- **Absolute cancer incidence (population rate)** — the dose-response SHAPE is now emergent [V]; an absolute
  rate needs epidemiological data, which is outside the substrate by discipline.
- **lineage middle pair (spleen ↔ thymus)** — already resolved *as far as the substrate allows*: the v0.4.0
  emergent race shows the spinodal gap (≈0.021) is comparable to the commitment jitter, so the ordering does
  not robustly resolve. Closing it further would require sub-gap structure that γ alone does not contain — a
  genuine limit, not a missing computation. Keep [O], quantified.
- **Therapy molecule / dose / patient response** — the kernel predicts the intervention CLASS and the
  cytotoxic-relapse failure mode [V]/[L]; mapping to a specific agent/dose/schedule/individual needs clinical
  pharmacology and biomarkers outside the deterministic substrate.

## D. Publication / housekeeping (non-research)

- **✓ DELIVERED in v0.15.0 — per-disease SEO page split (docs-only).** The combined disease/treatment axis
  page (former ch08, six disease classes on one page) was split per VP-SPEC v1.8 (C4 / chapter 6-R) into an
  axis OVERVIEW (ch08) + one self-contained, answer-first page per disease class — ch09 autoimmunity
  (T23+T27), ch10 transplant (T32), ch11 allergy (T29, newly wired into the build), ch12 immunodeficiency
  (T30), ch13 autoimmune cytopenia (T33), ch14 systemic inflammation (T31) — and the former ch09 repertoire
  ageing (T34/T35) moved to ch15 (slug `15-`), body and numbers unchanged. 15 chapters + hub = 16 pages.
  Bodies were transferred verbatim with numbers spliced from the already-pulled result dicts (only allergy is
  a new body, from `emergent_sensitization`); every disease page keeps [V] dynamics, [O] absolute scale and
  the direction/class + not-medical-advice disclaimer plus a self-contained back-link to the axis overview.
  Docs-only: `repro/` untouched, determinism hash `e7a2a5b8…` byte-identical (run_all output byte-diff 0 vs
  baseline), battery 35/35, NCBI provenance, discipline 6/6 drift 0; all answer-first 40–60 words, JSON-LD
  valid, sitemap 16 URLs, DOI 128 / pending 0, llms.txt < 5 KB, `_meta.json` chapters 15. No new `[O]`,
  ledger unchanged; stale directory (old `09-repertoire-…`) removed.
- **✓ DELIVERED in v0.14.1 — answer-first length compliance (C4 §6), docs-only.** Four pages exceeded the
  40–60-word answer-first rule (ch01 69 / ch02 64 / ch08 109 / ch09 161); the four `answer=` strings in
  `tools/build_docs.py` were trimmed into range (57/52/53/60) preserving the measured framing, the [V] grade
  and the direction/class + not-medical-advice disclaimer. Answer-first is prose, independent of the
  determinism hash (`e7a2a5b8…`, from `circulate()` only), so the full battery stays GREEN and byte-identical;
  no new `[O]`, ledger unchanged. On any future answer edit, keep each page's `<p class="answer">` at 40–60 words.
- **DOI**: ✓ concept DOI `10.5281/zenodo.20755280` registered in v0.12.0 and wired through `tools/build_docs.py`
  (`DOI`/`DOI_URL` constants → claim-strip, footers, JSON-LD `identifier`+`sameAs`, `llms.txt`, `_meta.json`).
  On a new version DOI, change only the two constants.
- On any new T21+ target: wire it into `repro/_verify/stress_tests.py`, regenerate
  `reports/research_complete.json`, splice the measured numbers into the relevant `docs/` section via
  `tools/build_docs.py` (keep answer-first 40–60 words, JSON-LD valid), update this file + the ledger, bump
  VERSION, re-zip, fresh-extract test, hand off the single zip.
