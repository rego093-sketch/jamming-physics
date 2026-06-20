# CHANGELOG — Hemodynamic Homeostasis (`homeostasis_hemodynamic_vp_site`)

All notable changes to this package. Grades: `[V]` sim-reproduced shape/direction · `[L]` cited ·
`[O]` absolute scale open · `[F]` forced/declared · `[CAL]` calibrated to clinical units.

---

## v0.7.0 — Comfort-logic intervention layer (analgesic three-lever technique, ported)

**Concept DOI:** `10.5281/zenodo.20756801` (Zenodo, registered and hardcoded across the site).
**Engine research hash:** `08a11846d481a849034a5d97ca8b8d4e43280f6965738d5e93e40caea4f65ce4`
(2× sha256 identical). **Stress battery:** 26/26 PASS (was 21/21). **Docs:** 21 pages (was 13),
byte-identical across 2 builds. **PHASE:** writing (research signed off, `all_green=true`).

### Added — the comfort-logic layer (`repro/_intervention/`)
This release ports the three-lever intervention technique from the non-opioid analgesic whitepaper
(`analgesic_threshold_logic_v2.0`, concept DOI `10.5281/zenodo.20733420`) and applies it to the
defended arterial-pressure setpoint. The scientific anchor is a result this package already proved:
the MAP loop is an integral controller that **rejects** an operating-point push back to its reference
(RP4 `opposed_back`) while a **reference reset** is durable (T1). That asymmetry — not any safety
assertion — is read as the structural origin of the antihypertensive side-effect class.

- **`intervention_logic.py`** — `comfort_map()` builds a 6-axis, three-lever map whose directions are
  READ off the proven RP4/T1/T2 loop results (no new substrate mathematics):
  - **H1** (reset the integrator reference down; analgesic L3 analogue): `renal_sympathetic`,
    `raas_ren` (DNA-grounded, REN γ = 1.3634), `sodium_volume_reference` (DNA-grounded, SIX2 γ =
    1.5556). Counter-regulation-free, structurally.
  - **H2** (restore the fast baroreflex buffer; analgesic L2 analogue): `baroreflex_piezo`.
    Counter-regulation low.
  - **H3** (unload the effector, PAIRED-ONLY; analgesic L1 analogue): `svr_effector`. Rejected alone
    (RP4 → the side-effect class), not rejected when paired with H1.
  - Plus an HF H1-analogue axis (`hf_margin_fourpillar`, T2: load-reduce + cycle-break grows the basin
    margin M = spinodal(κ) − |load|; inotrope flogging shrinks it).
  - **Cross-package finding:** the nociceptor gate has no integral controller, so the analgesic L1
    works alone; the MAP loop HAS one, so the H3 analogue is paired-only. Same lever frame; the
    integrator is the difference.
  - `all_intervention()` — deterministic, **docs-independent** aggregate of the whole layer, folded
    into the engine's `circulate()` hash.
- **`comfort_proposal.json`** — HP1–HP7 hypothesis-only proposals + explicit non-claims. Every item is
  a structural/directional hypothesis read off the proven loop, graded `[F]`; clinical outcomes `[O]`.
- **`forbidden_claim_scan.py`** — fail-closed firewall ported from the analgesic M5. Scans the proposal
  claims, the built comfort/proposal doc sections, and the intervention-module assertions for
  dosing / synthesis / efficacy-as-fact / safety-as-fact phrasing; a hit refuses the build. The
  self-test fires and the `no side effects` / `side-effect-free` / `is safe` family is never
  negation-suppressed.
- **`counterreg_honesty.py`** — fail-closed honesty gate: every per-axis molecular mechanism is graded
  `[O]` cited biology (never derived from the loop read); lever placement is `[V]` structural; the
  measured γ is carried for provenance and never presented as the mechanism.
- **`burden_prioritisation.py`** — ranks target **axes** (never molecules, exposures, or regimens) by
  DECLARED weights (burden 0.35 / unmet need 0.25 / counter-regulation-freedom 0.25 / grounding 0.15).
  γ is carried, never folded into the score. Reference-reset axes lead.
- **`falsification.py`** — a named falsifier for every HP1–HP7 plus a framework-level falsifier aimed
  at the load-bearing RP4/T1 asymmetry.

### Added — engine + battery integration
- `vp_hmd_engine.py` `circulate()` now folds `intervention = all_intervention()` into the single
  deterministic hash (docs-independent, so the hash never depends on built HTML).
- `stress_tests.py` gains **IV1–IV5** (comfort map / firewall / honesty / falsification / prioritisation),
  taking the battery from 21 to **26 suites**. `forbidden_claim_scan` runs with `scan_docs=False` inside
  the battery so the determinism check is HTML-independent.
- `reports/research_complete.json` re-signed: hash `08a11846…`, 26/26, `all_green=true`.

### Added — documentation (split, not crammed: one page per idea)
Eight new chapters (§13–§20), one HTML page each, per the "split the HTML" requirement:
- **§13 hmd-comfort-logic** — the comfort principle (counter-regulation is the structural side-effect
  class); `data-claim="comfort"` (firewall-scanned).
- **§14 hmd-lever-reset-reference** — lever H1.
- **§15 hmd-lever-restore-buffer** — lever H2.
- **§16 hmd-lever-unload-effector** — lever H3 + the integrator caveat / side-effect reading.
- **§17 hmd-comfort-proposal** — HP1–HP7; `data-claim="proposal"` (firewall-scanned).
- **§18 hmd-comfort-prioritisation** — declared-weight axis ranking.
- **§19 hmd-comfort-falsification** — a named falsifier per hypothesis + framework.
- **§20 hmd-comfort-firewall** — the fail-closed firewall, explicit non-claims, no medical
  responsibility; `data-claim="disclaimer"`.

The forbidden-claim scanner is wired into the build path (`scan_docs=True` over the built docs) and the
build now fails closed on any forbidden phrasing. All 20 sections pass the writing gate (answer 40–60
words, no `<h1>` in body, vp-card present, description 80–160 chars). `llms.txt` stays under 5 KB.

### Changed
- **Concept DOI hardcoded.** All previous "DOI pending (ORCID)" / "Concept DOI pending Zenodo" strings
  are replaced by `10.5281/zenodo.20756801` across the claim-strip, hub footer, `llms.txt`, `_meta.json`
  and `BUILD_NOTES.md`. The ported technique cites its source concept DOI `10.5281/zenodo.20733420`.
- **VERSION** → `0.7.0`.

### Invariants preserved
- The pre-existing engine science is byte-unchanged where untouched; the research-hash change is
  entirely attributable to the new, intentional comfort-logic layer.
- DNA emergence remains inherited and actively applied (REN γ = 1.3634, SIX2 γ = 1.5556 measured from
  real human promoters; the two reference axes are grounded on them).
- No-tuning discipline, SEED determinism, and honest grading retained throughout.

### Open (firewalled, by design)
- Per-axis molecular mechanism (receptor / transporter / channel pharmacology): `[O]` cited biology,
  never derived from the loop read.
- Any molecule, exposure schedule, regimen, efficacy, tolerability or safety result: `[O]`, outside
  what a structural loop reading can establish. "Counter-regulation-free" is structural, not clinical.

---

## v0.6.0 — Writing finalized (baseline this release builds on)
Absolute-scale calibration (CAL1–CAL7) closed the open mmHg / Hz / GFR / effect-size scales to clinical
units; the hypotension node-decomposition (RP6–RP9) and the cross-organism universality chapter (C1)
were added; REN γ was promoted from to-measure to DNA-measured. Battery 21/21, 13 canonical pages.
