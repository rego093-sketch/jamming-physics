# Digestive/Metabolic — contents

## Summary
This volume reads digestive transport and metabolism (stomach, intestine, pancreas and liver) with one slow-wave clock. The clock is a FitzHugh–Nagumo oscillator on the R19 switch, with thresholds read from measured promoter γ. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: one clock running from gastric ~3 cpm to duodenal 11.1 cpm. The claims ledger records the headline as an **anchor restatement**. The gastric 3.0 cpm holds by definition (the time scale is set to hit it). The duodenal 11.1 cpm is close to the observed ~11–12 cpm, but it depends on the chosen intestinal recovery time and the FFT window (τ_duo 80–120 → 12.9–9.0 cpm), so it is not a "zero intestinal tuning" prediction. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its input dependence stated), a consistency check or an interpretation. [F]/[V] are no longer used for biological claims, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §1, methods, hub: the developmental order intestine → pancreas → liver → stomach was "forced by the substrate [V]" and "sign validated vs cited developmental-timing anchor". No code performs that validation: the phrase exists only as a label string in `vp_dig_engine.py`. The order also contradicts embryology, where the liver bud (about day 22–24) precedes the pancreatic buds (about day 26). It is now interpretation / open [O] (dna §RB, §AX-A, §AX-I).
- §3: duodenum 11.1 cpm "with zero intestinal tuning" is now stated as input-dependent. TAU_DUO = 95 and GRAD_FACTOR = 1.5 are chosen, and τ_duo 80 / 90 / 100 / 110 / 120 → 12.9 / 11.7 / 10.5 / 9.6 / 9.0 cpm. Huizinga & Lammers 2009 is cited.
- §3: the frequencies sit on a 0.3 cpm FFT grid (window T = 8000), which caused the repeated 8.7 in the "monotone" table. The duodenal value moves with the window (T = 6000 → 12.0; T = 12000 → 11.0; ISI → 10.99).
- §2: gastric 3.0 cpm matches its anchor by definition (K_TIME = 3 / f(τ_s = 380)). It is relabelled consistency, and EGG 2.5–3.7 cpm (Parkman 2003) and Sanders 2006 are cited.
- §4, §5: aboral transport follows the imposed sign of the gradient (+12 segments depends on run length, coupling and flux). The glucose setpoint return is a closed-loop fixed point by construction. ADA fasting glucose is cited.
- §7–§30: R19 readings of gates, reservoirs, afferents, barriers and flares are relabelled interpretation with code outputs. The shared D = 0.041667 and the calibrated κ set every relative risk.
- §8 colorectal / processed meat: a magnitude-firewall note was added. The single slope κ is calibrated to the cited IARC exposure anchor [L]; this is disclosed as a calibration, not a derivation. Other points on the curve are extrapolations of that calibration, not clinical or individual risk estimates. Absolute incidence stays [O], and the page gives no dietary advice.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule lt-note was added to the hub. All chapters were relabelled [F] → consistency and [V] → code output (§1 → interpretation). γ cards became code output and R19 mapping cards became interpretation. Manifest grade counts forced 2 / verified 61 → 0 / 0.
- Reading-versus-building notes were added to §1, about, methods and the hub.
- The review findings (11.1 cpm depends on chosen τ_s; the order check is absent in code) are recorded in the lineage for the author.

**Reproduction package changes**
- None. Code and data under `repro/digestive/` are unchanged since the previous version.

**Site/metadata**
- A magnitude-firewall audit ran corpus-wide: the clinical volumes are clean, borderline pages (including digestive §8) are annotated, and the gate pattern was widened.
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The companion work-in-progress commit for the other organ volumes was included.
- Recurrence guards: integrity checks in the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume.

## Claim status (claims ledger)
Counts: anchor-restatement 3 · identity 1 · open 1 (5 rows).
- One clock gastric ~3 → duodenum 11.1 cpm (jejunum 9.0, ileum 7.5) — anchor-restatement — close to the observed ~11–12 cpm, but τ_duo 80–120 → 12.9–9.0; T = 6000 → 12.0; ISI 10.99.
- Gastric slow wave 3.0 cpm — anchor-restatement — residual 0 by definition (EGG 2.5–3.7 cpm).
- Developmental order intestine, pancreas, liver, stomach "[V], sign-validated" — open — contradicted by embryology (liver bud before pancreatic buds). No validation code exists.
- Aboral transport direction; glucose setpoint return — identity — imposed gradient sign; closed-loop fixed point by construction.
- Disease RRs via R19 gates (§7–§30) — anchor-restatement — the calibrated κ and shared D = 0.041667 set every RR; the R19 readings are interpretations.

## Open items
- Developmental order, size and timing of the digestive organs: building is [O] (dna §RB).
- Absolute incidence and every clinical magnitude, including the felt pain in the functional-pain pointers: [O] under the magnitude firewall.
- Author decision (review): whether to derive or observe the intestinal τ_s values instead of choosing them, and whether to report frequencies by ISI instead of on a fixed FFT grid.

## Reproduction
The ZIP contains `docs/digestive/` (the published HTML pages), `repro/digestive/` (engine, inherited substrate, reports), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/digestive && python3 repro/run_all.py`. A full run takes longer than two minutes; in the review it did not finish within 120 s.
- Engine alone: `repro/digestive/repro/_engine/vp_dig_engine.py` (`slow_wave_clock`, `emerge_organs`). This reprints K_TIME 2400, gastric 3.0, duodenum 11.1, jejunum 9.0 and ileum 7.5 cpm and the γ values.
- Gates: `repro/digestive/repro/_verify/gates.py`.
- SEED = 19 (`repro/digestive/inherited/vp_substrate.py`). No network is needed.

## Citation and links
- Site: https://jamming-physics.org/digestive/
- Concept DOI: 10.5281/zenodo.20755319
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
