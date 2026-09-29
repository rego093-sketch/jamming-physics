# Olfactory Emergence — Smell from the R19 switch and measured DNA γ

## Summary
This volume reads the sense of smell as an R19 transduction switch (`ds/dt = g·s − s³ + h`) whose thresholds are set by promoter stiffness γ measured from public NCBI sequence. It inherits the γ ruler and the R19 switch from **dna**, hands the transduced signal off to **neuro**, cites allergic smell loss from **immune_hematologic** §11, and shares the CNGB1 γ with **eye** as a consistency check. It inherits no wave module, because smell has no wave. It adds one module: a combinatorial receptor code, a CNG transduction switch and anosmia as switch failures. The headline, "smell from R19 switch + measured DNA γ", is recorded in the claims ledger as an **interpretation**: the γ values are deterministic code outputs, but the mapping of the cubic onto olfactory transduction is not derived. The odorant→receptor key sits in the binding pocket, not in γ, and stays open [O]. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its input dependence stated), a consistency check or an interpretation. [F]/[V] theory grades are not used for biological claims, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §3 bulb map: the developmental order EBF1 → EMX2 → LHX2 was graded [F]/[V] as "forced by measured γ", with "dwell ∝ γ^1.5" as relative size. It is now a code output (a γ sort) read as interpretation. In the corpus, order comes from DNA-atlas cascade depth, and building (order, size, timing) is open [O] (dna §RB).
- §3: "one OR → one glomerulus bijection" replaced by the observed anatomy (about 2 glomeruli per OR per bulb in mouse, about 16 in human; Maresh et al. 2008). The capacity conclusion is unchanged.
- §1/§3 combinatorial code: "4 of 128 patterns" is now labelled a code output from 8 hand-picked sweep points. A dense sweep of the same code gives N+1 = 8 nested patterns.
- §2/§4 transduction switch: "≈229× steeper than a graded control" is now stated as step-dependent (±1 / 5 / 10 % steps → 229× / 48× / 24×).
- §2: CNGB1 γ = 1.4357 equal to the rod-vision value was graded [V]. It is now a consistency check: same promoter, same window, same pipeline.
- §2: the uncited "Hill ≈ 2–3 from the cubic" was replaced by the measured olfactory CNG Hill coefficient 1.4–1.8 (Frings, Lynch & Lindemann 1992), cited as an observation. The page now states that the normal-form order is not a Hill coefficient and that no mapping is derived.
- §4/§5: congenital anosmia 7/7 and allergic sensorineural 0/7 are now stated as true by construction of the inputs (h₀ = 1.15·max h*, damaged = 0.90·min h*). They are demonstrations, not tests against smell-loss data.

**New experiments and results**
- Simple-tissue emergence of the olfactory neuron chain (cAMP → CNG → Ca → Ca-activated Cl⁻) was attempted and **not run**. The inter-stage coupling scales (ciliary cAMP and Ca per unit current) were not found in sourced form, and choosing them would make the output a choice. Recorded as [O] on the hub, with the missing constants named.

**Relabelled grades / reading rule**
- The author reading rule (observation / code output with input dependence / consistency / interpretation) was applied to the hub and all chapters. Manifest grade counts forced 2 / verified 4 → 0 / 0; open 1 is unchanged.
- Declared inheritance was updated: the manifest now lists dna, neuro, immune_hematologic §11 and eye (CNGB1). A `seams.json` declares each seam and its grade.

**Reproduction package changes**
- `repro/nose/tools/build_volume.py` now writes to `repro/nose/_build/docs` (git-ignored), never into `docs/`.
- `repro/nose/tools/gate_volume.py` and the verify tooling fall back to the monorepo `docs/nose/` when `repro/nose/docs/` is absent. In the monorepo layout, the review had found the gate failing on this path.
- The research scripts E1–E5, the SSOT and the builder entered the monorepo with the volume, in the integration of +5 volumes (eye, ear, nose, wave-computer, inheritance). This includes the work-in-progress snapshot "nose: fact/code reading rule".

**Site/metadata**
- docs/ was declared the source of truth. A correction-note preservation check (`registry/page_notes.json`) fails the gate if a page loses a note.
- Highwire citation meta is regenerated from the manifest. Visible escaped comments and raw LaTeX are now guarded by the gate.
- Link audit (2026-09-28): stale GitHub repro paths and site slugs were repointed corpus-wide, leaving 0 broken links.
- Manifest, `_decl.json`, hashes and lineage were refreshed. The earlier untitled repository snapshot commits ("11111", "Final", "1111111") imported the nose pages and assets.

## Claim status (claims ledger)
Counts: interpretation 1 · anchor-restatement 2 · identity 2 · open 1 (6 rows).
- Smell from R19 switch + measured DNA γ (transduction switch) — interpretation — n/a. The "Hill 2–3 from the cubic" statement was uncited and no mapping is derived. Observed OSN responses are graded dose–responses.
- Combinatorial code: nested thermometer reaches 4 of 128 patterns — anchor-restatement — a dense sweep gives 8 = N+1 (sampling artefact).
- Transduction switch ≈229× steeper than graded control — anchor-restatement — ±1 / 5 / 10 % step → 229 / 48 / 24.
- CNGB1 γ = 1.4357 byte-identical to the rod-vision value — identity — residual 0 (same promoter, window, pipeline).
- Congenital anosmia 7/7; allergic sensorineural 0/7 (h₀ = 0.65881) — identity — outcomes set by input definitions.
- Bulb map order EBF1 → EMX2 → LHX2 by γ; one OR → one glomerulus — open — conflicts with anatomy (about 2 glomeruli per OR per bulb in mouse, about 16 in human; Lhx2 needed early). Building order [O].

## Open items
- Odorant→receptor key (binding-pocket recognition), which is not encoded in promoter γ: the central [O].
- Developmental order, size and timing of the bulb map: building is [O] per dna §RB. Order is inherited from dna cascade depth, not recomputed.
- Simple-tissue emergence of the olfactory neuron chain: [O]. The ciliary cAMP and Ca coupling scales per unit current are missing in sourced form.
- Author decisions (review): state once the γ (kcal/mol) → dimensionless g unit convention; check whether one CNGB1 promoter window covers both the rod CNGB1a and olfactory CNGB1b isoforms.
- Felt percept of smell belongs to the mind volume and is not claimed here.

## Reproduction
The ZIP contains `docs/nose/` (the published HTML pages), `repro/nose/` (code, inherited promoter data and cache, research scripts), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Full verification: `python3 repro/nose/tools/verify_seed.py`. It checks no-regression, deterministic foundation modules (2×SHA-256), offline recompute of γ and A4 against the atlas, no-omission, and HTML↔code drift 0.
- Volume gate: `python3 repro/nose/tools/gate_volume.py`.
- Per-result scripts: `repro/nose/research/E1-combinatorial-code/run.py`, `E2-transduction-switch/run.py`, `E3-bulb-map/run.py`, `E4-congenital-anosmia/run.py`, `E5-allergic-smell-loss/run.py`. Each has a `gate_E*.py`, and each runs in under 120 s.
- SEED = 19. No network is needed: γ is recomputed from the shipped promoter cache. Only the optional `repro/nose/tools/fetch_promoter_gamma.py` re-fetches sequence from NCBI.

## Citation and links
- Site: https://jamming-physics.org/nose/
- Concept DOI: 10.5281/zenodo.20790182
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
