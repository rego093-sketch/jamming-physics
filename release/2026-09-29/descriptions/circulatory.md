## Summary
This volume reads blood flow and clearance (vasculature, kidney and liver) as a transport-and-clearance network driven by the cardiac pump, on the R19 switch with measured promoter γ. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: `MAP = CO × SVR` pressure–flow transport with hepatic and renal clearance. The headline `MAP = CO × SVR` (MAP 95.7 mmHg) is recorded in the claims ledger as an **identity** (Ohm's law). The value is an output of the input CO and SVR and lies within the normal range. Most former [F]/[V] results in the volume are identities of the model (τ = RC, F = 1 − E, a PI loop reaching its setpoint, a round trip through the barrier law, a product of two exponentials), not tests against data. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its input dependence stated), a consistency check or an interpretation. [F]/[V] are no longer used for biological claims, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- Hub, §1, about: organ order (liver → kidney) and relative size (DWELL ∝ γ^1.5) were "forced [F]". They are now interpretation, superseded and open [O] (dna §RB; γ-order schedule null, §AX-A; order from cascade depth, §AX-I). The liver-before-kidney order matches embryology, but one agreeing pair is not evidence.
- §9: "matching the observed 73 to within 0.000%" was wrong. The 0.000% is the deviation of the combined RR from the product of the single RRs, an algebraic identity. The model gives 72.0, which is −1.4% from the cited 73. The text is corrected and no number was changed.
- §8: RR(50 pack-years) = 2.00 for renal cell carcinoma is now stated as the calibration point (`D_RCC` is chosen so that RR(50) = 2.0), not an output. Hunt 2005 is cited.
- §6, §19: the flow elasticities 0.90 / 0.10 and the CLint elasticities 0.91 / 0.11 restate the chosen extraction ratios (well-stirred model: E and 1 − E exactly). Propranolol F ≈ 25% (Routledge & Shand 1979) is cited, with "no dose derived".
- §15: the KDIGO landing is by construction (N = threshold / 125).
- §2–§5: MAP = CO × SVR "holds < 1%", τ = RC (1.54 s), GFR 125, osmolality 287 and the PI setpoint return are relabelled consistency checks / code outputs of the chosen inputs. Observations are added (MAP range, Guyton & Hall; Westerhof 2009; Carlström 2015; Verbalis 2003).
- §22, §23: "round-trips exactly [V]" is relabelled consistency (inverting the barrier law, then applying it). The VHL / HFE blocks are relabelled observation.
- §16, §17, §21: the breakthrough at 195 mmHg, the 3.1× and 1.09× folds, and the ~7× and ~148× suppressions are labelled outputs of chosen settings. §17's clinical-sounding wording was neutralised: the folds are illustrative code outputs and no dose is given.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule lt-note was added to the hub. All chapters were relabelled [F] → consistency and [V] → code output, consistency (§9, 15, 18, 19, 21–23) or interpretation (§1). γ cards became code output and mapping cards became interpretation. Manifest grade counts forced 14 / verified 24 → 0 / 0; hypothesis 8 is unchanged.
- Reading-versus-building notes were added to §1, about and the hub.
- The review finding on §9 (identity, not a 0.000% match) is recorded in the lineage for the author.

**Reproduction package changes**
- None. Code and data under `repro/circulatory/` are unchanged since the previous version.

**Site/metadata**
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The companion work-in-progress commit for the other organ volumes was included.
- Recurrence guards: integrity checks in the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume.

## Claim status (claims ledger)
Counts: identity 4 · anchor-restatement 1 · open 1 (6 rows).
- MAP = CO × SVR; MAP 95.7 mmHg — identity — within the normal range; an output of the input CO and SVR.
- §9 combined RR "matches observed 73 within 0.000%" — identity — the model gives 72.0 vs 73 (−1.4%). The 0.000% is a product-of-singles identity.
- RR(50 pack-years) = 2.00 for RCC — anchor-restatement — residual 0 (calibration point).
- Diastolic τ = RC 1.54 s; GFR 125; osmolality 287; PI setpoint return — identity — outputs of the chosen R, C and integral-controller design.
- Clearance elasticities 0.90 / 0.10 and 0.91 / 0.11; KDIGO landing; barrier round trips — identity — equal to E and 1 − E; N = threshold / 125; a law followed by its inverse.
- Organ order liver → kidney and size DWELL ∝ γ^1.5 — open — agrees with embryology for one pair, which is not evidence. Building [O].

## Open items
- Developmental order, size and timing of vasculature, kidney and liver: building is [O] (dna §RB).
- Absolute clinical magnitudes (risk, clearance-based dosing): withheld under the magnitude firewall. The volume gives direction only.
- The eight hypothesis-labelled items carried by the volume remain hypotheses.

## Reproduction
The ZIP contains `docs/circulatory/` (the published HTML pages), `repro/circulatory/` (engine, oncology kernel, inherited substrate, doc builder, reports), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/circulatory && python3 repro/run_all.py`. All 23 targets pass with drift 0, and the engine reprints MAP 95.7, τ 1.54 s, GFR 125, osmolality 287, E 0.75, the RCC RR, the aflatoxin × HBV product and the KDIGO steps.
- Gates: `repro/circulatory/repro/_verify/gates.py`. Oncology constants: `repro/circulatory/repro/_oncology/carcinogen_dose_response.py`. The §9 identity is in `repro/circulatory/tools/build_docs.py`.
- SEED = 19. Python 3 with numpy only. No network is needed (`repro/circulatory/README_REPRODUCIBILITY.md`).

## Citation and links
- Site: https://jamming-physics.org/circulatory/
- Concept DOI: 10.5281/zenodo.20754354
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
