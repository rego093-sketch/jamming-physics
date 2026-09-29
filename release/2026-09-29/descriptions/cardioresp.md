# Cardiorespiratory VP — heart & lung as one oscillator

## Summary
This volume reads the heart and the lung as one FitzHugh–Nagumo relaxation oscillator, built on the R19 cubic switch, at two settings. It inherits the measured γ ruler and the node atlas from **dna**, the time layer from **circadian**, setpoint drift from **aging_senescence**, and the defended pressure loop from its sibling **homeostasis_hemodynamic**. It adds one module: heart + lung = one FitzHugh–Nagumo oscillator. The claims ledger records the headline as an **interpretation**. The oscillator in the code runs at γ = 1.0 for both organs, so the measured γ (NKX2-5 1.513, NKX2-1 1.509) feeds only the spinodal and size readout, and the heart–lung difference comes from the chosen recovery times τ_s = 18 / 95. The breathing rate 16.86 /min is an **anchor restatement** of the chosen lung τ_s, not a structural prediction. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its input dependence stated), a consistency check or an interpretation. [F]/[V] are no longer used for biological claims, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §1, §2, §10, hub: "γ sets each organ's oscillator" is corrected. The engine (`_fhn_rate_arb`) builds `Neuron(gamma=1.0)` for both organs, and heart vs lung is set by τ_s 18 / 95 in `ORGAN_ROWS`. A code note is added.
- §3: the breathing rate 16.86 /min and the breath-to-beat ratio 0.240 were "structural, not fitted" [V]. They are now input-dependent code outputs: τ_s 60 / 80 / 110 / 130 → 25.47 / 19.70 / 14.76 / 12.65 /min. The observed RR and HR ranges and the pulse–respiration quotient are added.
- §1, §10: the developmental order lung → heart was a [V] "pure γ readout" (γ difference 0.004). It is now interpretation / open [O]. Embryology runs the other way: the heart beats from about day 22 (CS10), and the lung bud appears at about day 28 (CS12). The order is superseded per dna §RB / §AX-A.
- §4: periodic-breathing onset at LG/LGc = 1 is relabelled consistency, because it is normalised to its own critical gain. Khoo 1982 and Younes 2001 are cited.
- §5: the RSA "lock" at 0.2784 Hz is relabelled consistency: a drive at f_resp gives a line at f_resp. The decoupled peak (0.303 Hz) also lies in the vagal band. Hirsch & Bishop 1981 is cited.
- §6: Cheyne–Stokes T ≈ 2τ (slope 1.992) is now a property of delayed negative feedback. Model periods of 17.7–41.7 s are shorter than the roughly one-minute cycles observed (Hall et al. 1996).
- §7: baroreflex sign, linearity and slope (−1.0 bpm/mmHg) restate the input gain and latency. The observed BRS range is added (La Rovere 2008).
- §8: the smoking RR of 18.3× at 100 pack-years is set by the declared `scale = barrier/3` (ceiling e³ ≈ 20) and by the pack-year mapping. RR(0) = 1 is an identity. Observed lung-cancer RRs are cited next to it.
- §11: the page showed [V] where `run_all.py` prints "[V?]" (D2, D3, D5, D6). Fever co-scaling is by construction (one κ). A fever observation is added.
- §12: the page claimed "OVERALL: PASS (11/11)". A note now records that the current run ends FAIL (9/11): R6 has 0 pinned files, R10 fails the DOI check, and R7 scans 0 pages after the move to `docs/`.

**New experiments and results**
- Simple-tissue emergence of a sinoatrial pacemaker cell from measured ionic currents was identified as the right test of the FHN reading and **not run**, because no sourced parameter set could be loaded (model repositories unreachable). Recorded as [O] on the hub. The neighbouring neuro EM2 squid-axon run is a neuro result and is not claimed here.

**Relabelled grades / reading rule**
- A reading-rule lt-note was added to the hub. All chapters were relabelled [F] → consistency and [V] → code output / consistency / interpretation per page. γ cards became code output (a measured input from the dna reading) and FHN cards became interpretation. Manifest grade counts forced 2 / verified 18 → 0 / 0.
- A reading-versus-building note was added to §1 and the hub. The γ thresholds (can-fire, spinodal ∝ γ^1.5, barrier γ²/4) remain valid as reading. Order and size from γ are superseded (dna §AX-A measured null; order from cascade depth, §AX-I; building [O], §RB).
- The review findings (γ = 1.0 in the oscillator; lung τ_s sets breathing rate) are recorded in the lineage for the author.

**Reproduction package changes**
- None to the code or data under `repro/cardioresp/` since the previous version. The previous deposit's whitepaper (`repro/cardioresp/zenodo/cardioresp_vp_site_v0_5_0.pdf` / `.tex`) and `ZENODO_METADATA.md` are carried in the package, but their abstract predates these corrections. In particular, its "no constant is chosen to hit a target" and "OVERALL: PASS (11/11)" no longer hold as written.

**Site/metadata**
- The corpus-wide biology reading-rule registry integration regenerated `_decl.json`, page notes, hashes, lineage, the homepage and the sitemap. Light reviews of circadian, aging_senescence and inheritance were committed alongside (sibling volumes).
- Recurrence guards: `tools/check_integrity.py` wired into the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume and its whitepaper.

## Claim status (claims ledger)
Counts: interpretation 1 · anchor-restatement 2 · identity 1 · open 1 (5 rows).
- Heart + lung = one FitzHugh–Nagumo oscillator set by measured γ — interpretation — n/a. The oscillator uses γ = 1.0, and τ_s 18 / 95 sets heart vs lung.
- Breathing rate 16.86 /min, heart:lung ratio 0.240 — anchor-restatement — in the normal 12–20 /min range, but τ_s 60 / 80 / 110 / 130 → 25.47 / 19.70 / 14.76 / 12.65.
- Developmental order lung → heart from γ — open — contradicted by embryology (heart ~day 22, lung bud ~day 28).
- Loop-gain onset at LG = 1; RSA lock at 0.2784 Hz; Cheyne–Stokes T ≈ 2τ (slope 1.992) — identity — model periods of 17.7–41.7 s are shorter than the observed ~1 min cycles.
- Smoking RR 18.3× at 100 pack-years — anchor-restatement — set by the declared scale (ceiling e³ ≈ 20) and the pack-year mapping.

## Open items
- Developmental order, size and timing of heart and lung: building is [O] (dna §RB).
- Simple-tissue emergence of a sinoatrial pacemaker cell from sourced ionic-current constants: [O]. The FHN reading stays an interpretation until it is run.
- Absolute cancer relative-risk magnitude: [O] (magnitude firewall).
- Author decisions (review): whether the measured γ should enter the oscillator dynamics; repairing the harness checks R6, R7 and R10 that fail after the move to `docs/` (current run 9/11).

## Reproduction
The ZIP contains `docs/cardioresp/` (the published HTML pages), `repro/cardioresp/` (engine, inherited substrate, reports, previous whitepaper), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/cardioresp && python3 repro/run_all.py`. The run reprints every page number with drift 0 (16.86 /min, 0.2784 Hz, slope 1.992, RR table 1.00 → 18.32). The overall verdict currently reads FAIL (9/11), because checks R6, R7 and R10 fail on the monorepo layout, not on numbers. A full run takes more than two minutes.
- Gates: `repro/cardioresp/repro/_verify/gates.py`.
- Engine: `repro/cardioresp/repro/_engine/vp_car_engine.py`. Oncology kernel: `repro/cardioresp/repro/_oncology/carcinogen_dose_response.py`.
- SEED = 19 (`repro/cardioresp/inherited/vp_substrate.py`). No network is needed.

## Citation and links
- Site: https://jamming-physics.org/cardioresp/
- Concept DOI: 10.5281/zenodo.20755371
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
