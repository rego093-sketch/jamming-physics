## Summary
This volume reads hearing as a chain: wave → cochlear place map → R19 switch → congenital deafness. It inherits the following:
- the wave substrate from `physics`;
- the R19 cubic, the γ reader and node identity from `dna`;
- the Hopf cube-root amplifier from `sensory_organ` §7 (this seam is now declared).

The one added module is the ear's own chain: the place map, the cube-root cochlear amplifier and the otoferlin readout. The headline "ṡ = g·s − s³ + h → cube-root amplification" (exponent 0.333333) is unchanged in wording. It is an **identity** in the claims ledger: the integrator converges to its own analytic fixed point, and the cube root at a Hopf bifurcation is prior work (Eguíluz 2000; Camalet 2000). Against observation, 1/3 sits at or above the top of the measured basilar-membrane compression range (~0.2–0.33; Ruggero 1997).

New in this version is EM1, a pre-registered **independent prediction** that builds a single hair bundle from observed molecular elements:
- the compression exponent emerges at 0.22–0.32 (PASS), covering the observed range the page had assumed to be 1/3;
- self-sustained oscillation emerges only about 1 pN below the published motor force, and is quiescent at the published value (FAIL, recorded).

The biology reading rule applies. The volume accepts existing observations and uses them. Each statement is an observation (cited), a code output (reproducible from `repro/ear/`, with its input dependence stated) or a consistency check (holds by algebra). DNA/VP mappings are interpretation, and [O] marks what the volume does not supply.

## What changed in this version (2026-09-29)
**Corrections**
- §2: the compression 1/3 is compared with the measured BM compression (~0.2–0.33), and the Hopf prior work is cited (Eguíluz 2000; Camalet 2000). "Compression uniform across frequency" is relabelled interpretation. It is a model assumption, and it conflicts with the weaker apical compression that is observed (Robles & Ruggero 2001). The ~120 dB span is labelled an observation, not a model output.
- §6: "Why we hear 20 Hz–20 kHz is derived" is restated as a code output from Greenwood's observed calibration. The band edges stay [O]. The ~10⁶ stiffness ratio is back-computed, not measured.
- §1: the identity checks (the Greenwood ratio to 2e−16 and the inverse round-trips) are labelled consistency. The emergence order TMC1 < PCDH15 < CDH23 < TMIE by spinodal(γ) is labelled a reading. As a developmental order it belongs to building, which is [O] per dna §RB.
- §3–§5: model outputs are relabelled as code output rather than [V], and "proves structure only" wording was adjusted.
- The concept pages (γ level/A4 shape, Greenwood place map, R19 bistable switch) carry the reading-rule labels.

**New experiments and results**
- EM1 (pre-registered, with a pre-run amendment) built a single hair bundle from observed elements: gating springs, transduction channels, adaptation motors and Ca feedback (Nadrowski, Martin & Jülicher 2004 constants).
  - Self-sustained oscillation emerges at 37 nm peak-to-peak and 5.8–6.7 Hz, inside the observed 5–50 Hz and 20–80 nm (Martin & Hudspeth 2001). It appears only for F_max 48–49.5 pN, and the bundle is quiescent at the published 50.3 pN: P1/P2 FAIL, recorded.
  - The compression exponent emerges at 0.22 (1–10 pN) to 0.32 (1–32 pN), with a local range of 0.12–0.58: P3 PASS. The author's own expectation that one bundle cannot reach 0.2 failed (P4 FAIL).
  - Run 1, which placed γ on the motor term with Po = 0 at rest, is kept on record as an implementation error.
- Eye and nose unit-level emergence was not run; the missing coupling constants are named, and it stays [O].

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub, and all seven chapters were relabelled. The manifest counts went from forced 35 / verified 15 to 0 / 0.

**Reproduction package changes**
- `repro/ear/experiments/EM1_hair_bundle_emergence/` was added: PREREG.json, PREREG_AMENDMENT.json, em1_run.py, RESULT.json, RESULT_run1_gamma_in_motor_term.json and a README.
- `repro/ear/tools/verify_seed.py` and `repro/ear/volume/tools/gate_volume.py` now fall back to `docs/ear`. They previously looked for `repro/ear/docs` and crashed.

**Site/metadata**
- The volume was integrated into the corpus site and repository (docs + repro, 2026-09-29).
- The header DOI badge now shows the ear DOI; it had shown the DNA DOI.
- `seams.json` was added. `_decl.json` inherits were updated: dna:R19-cubic, and the sensory_organ §7 Hopf seam is declared. Hashes and lineage were refreshed; the gate is CLEAN.
- Highwire citation meta was added to the hub.
- Earlier site-assembly snapshot commits ("11111", "1111111", June 2026) included concept-register additions. No claim changed.

## Claim status (claims ledger)
Counts: identity 2 · independent-prediction 2 · anchor-restatement 1 · interpretation 1 · open 1.
- Cube-root cochlear amplification, exponent 0.333333 (gain exponent −0.666667) — identity — at or above the top of the observed 0.2–0.3 range.
- EM1: hair-bundle oscillation emerges at the reported F_max — independent-prediction — **FAIL**: the bundle is quiescent at 50.3 pN (~1 pN outside the window). Inside the window, amplitude and frequency match observation.
- EM1: local compression exponent from elements — independent-prediction — P3 PASS (0.22–0.32 brackets BM 0.2–0.33); P4 FAIL. The average depends on the chosen force window.
- Greenwood map reproduced to 2e−16; inverse round-trips — identity — the ratio is 1 by algebra.
- Audible band 19.848 Hz – 20677.07 Hz; stiffness ratio ~1e6 — anchor-restatement — the edges are CF(0) and CF(1) of Greenwood constants chosen to span the audible range.
- Compression uniform across frequency — interpretation — contradicted at the apex.
- Emergence order TMC1 < PCDH15 < CDH23 < TMIE by spinodal(γ) — open — a reading; as developmental order it is building, [O].

## Open items
Author decisions from the review:
- Retire or keep the argsort(spinodal(γ)) emergence order, given the DNA cascade-depth rule (R1-1).
- Test the exponent 1/3 against data, or regrade it (R1-3). EM1 now supplies 0.22–0.32 from elements.
- The apex conflict of uniform compression (R1-4).
- The CF_max grade, and the fact that the band is calibrated rather than derived (R1-5).
- Ungraded "~100×" magnitudes versus the N1 [O] (R1-6).
- Footer version v0.10.0 vs VERSION 0.12.0 (R2-5).

Open [O] items:
- The absolute audible band edges (measured cochlear geometry).
- The whole-cochlea structure, which has not emerged.
- The EM1 F_max mismatch.
- Eye and nose unit emergence (missing constants).
- Building-layer order.

## Reproduction
The ZIP contains `docs/ear/` (the published HTML pages), `repro/ear/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- Seed gate: `python3 tools/verify_seed.py`, run from `repro/ear/`. Expect `SEED VERIFY: PASS`.
- Volume gate (HTML ↔ code drift): `python3 repro/ear/volume/tools/gate_volume.py`.
- Numeric source of truth: `repro/ear/volume/tools/vp_numeric_ssot.py`.
- Per-chapter research modules: `repro/ear/research/E*/`.
- EM1: `python3 repro/ear/experiments/EM1_hair_bundle_emergence/em1_run.py`. Compare with RESULT.json and PREREG.json.
- SEED = 19. No network access is needed; promoter γ is cached. `tools/fetch_promoter_gamma.py` and `tools/fetch_region_features.py` are the only steps that use the network.

## Citation and links
- Site: https://jamming-physics.org/ear/
- Concept DOI: 10.5281/zenodo.20790201
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
