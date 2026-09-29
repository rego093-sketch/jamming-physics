## Summary
Neural Emergence builds the chain from membrane to behaviour. It inherits from `physics` (substrate and EM), `chemistry` (EM on the same substrate) and `dna` (γ ruler and atlas). The one module it adds is the neuron read as the R19 switch plus a slow recovery variable (FitzHugh–Nagumo), from which rhythms, working memory, memory and motor control follow. The headline is now "working memory = f_γ/f_θ ≈ 6–7 [L] (literature bands, tACS-consistent)". The previous wording was "θ/γ ≈ 7±2 (tACS-causal)". In the claims ledger the headline is an **anchor restatement**: the value depends on the chosen band edges or the chosen τ pair, with a sensitivity range of 4.3–11.6, and "derived" and "causal" are withdrawn. The new EM2 result is an **independent prediction**, pre-registered at ±15%. A squid axon built from the measured Hodgkin–Huxley 1952 membrane elements gives a conduction velocity of 18.96 m/s against 21.2 m/s measured (residual −10.6%). That reproduces HH's own classic result; it is standard biophysics, not a VP-specific test. The biology reading rule applies. Measured γ is used only as reading, meaning switch thresholds. Building-layer claims (organ order and size) are [O] per `dna` §RB. Every number is an observation, a code output with its inputs stated, a consistency check, or an interpretation.

## What changed in this version (2026-09-29)
**Corrections**
- Working-memory headline regraded to [L]. It rests on the literature identity (Lisman) and literature band edges. The band-convention sensitivity (4.3–11.6) and the three in-corpus values (6.25 / 6.9 / 6.1) are stated. "Derived" and "causal" are deleted. The tACS studies are cited as literature support (Vosskuhl 2015; Reinhart & Nguyen 2019); neither measured the ratio itself.
- Building-layer claims were regraded to [O] or principle demonstration per `dna` §RB. This covers promoter-γ organ order and dwell-set size in §12, §17, §20, §23 and the hub. The review found PRDM12 placed last contradicts regulatory order, and the Briscoe 2000 order was taken from repressor pairs (circular).
- The promoter threshold is separated from the membrane firing threshold (§21, §23). The L1/L2/L3 classification is [L].
- §11: the eye γ of 1.21 is stated as disagreeing with the DNA atlas value (1.511), and the atlas takes precedence. Reflex gain 9.4 is labelled illustrative, since the physiological range is ~1–3.
- §15 and §18: "transverse [F]" is withdrawn to [H]. Light's E and B are read as transverse swing and lattice rotational response, aligned with physics §LT Link 6a. The "0.06%" light figure is marked as a 1-D check.
- §19: α_em stays [O]; 0.5424 exceeding the bound and its source are stated. §18: the winding value depends on v. §16: the frog data vs GHJ circularity is stated.
- The γ notations are disambiguated: f_γ (gamma band), γ_DNA (DNA stiffness) and the engine g. The rule was added to `TERMINOLOGY_canonical.md`.
- R = 0.39 is attributed to `mind`.
- The organ-emergence chapters carry the reading-vs-building note. The γ-order schedule is superseded (measured null, dna §AX-A), order comes from cascade depth (dna §AX-I), and building is [O].

**New experiments and results**
- EM2, a squid giant axon built from measured HH 1952 membrane elements (pre-registered). The spike, threshold, all-or-none behaviour and refractoriness emerge (spike 95.8 mV). Conduction velocity is 18.96 m/s against 21.2 m/s measured (−10.6%, inside the pre-registered 15% band; HH's own 1952 hand calculation gave 18.8). P1–P4 all PASS. Run 1 (weak launch stimulus) is kept on record with an amendment.
- Unit-level emergence of the cardiorespiratory SA node and the circadian clock was left [O], for stated reasons: no sourced constants here, and the clock constants are period-fitted.

**Relabelled grades / reading rule**
- WM → [L]; building-layer claims → [O]; model-property gates in §14 and §22 go [V] → [F] (self-simulations true by construction; the three levers in §22 trace the same curve in the model); transverse [F] → [H].
- The numbers in §2–§8 (19×, 0.65 bits, 17×, 9.4× reflex gain, 3.9×, 123.1) are declared data-pending in the methods: there is no reproduction code, because the neuro_extension module is missing.

**Reproduction package changes**
- `repro/neuro/experiments/EM2_hh_axon_emergence/` was added (PREREG.json, PREREG_AMENDMENT.json, em2_run.py, RESULT.json, RESULT_run1_weak_stimulus.json, README).
- 28 repro links were repointed to real paths.
- The reproduction scope and the weak drift gate are disclosed in the methods.

**Site/metadata**
- The manifest, AGENTS headline and homepage headline were updated.
- The corpus DAG gained the neuro → mind edge.
- §1 gained its prev link, and the hub now links methods and FAQ.
- §23: a stray `<-` was escaped. The α2δ-1 and K_V7 typos were fixed.
- The corpus link audit repaired stale links.
- Highwire citation meta was added to the hub.
- Corpus integrity checks were added to the gate.
- Earlier site-assembly snapshot commits ("VP Theory site", "Final", "1111111", June 2026) include the `_decl.json` worked example (gate REQUIRED PASS 8/8) and concept retagging (Kramers cards). No claim changed.

## Claim status (claims ledger)
Counts: anchor-restatement 1 · independent-prediction 1 · interpretation 1 · identity 1 · open 2.
- Working memory = f_γ/f_θ ≈ 6–7 — anchor-restatement — 6.25 / 6.9 / 6.1; band choice spans 4.3–11.6, and a broad gamma band gives 9.68.
- EM2: HH squid-axon conduction velocity emerges from measured membrane elements — independent-prediction — 18.96 vs 21.2 m/s (−10.6%, PASS). Not VP-specific, because the HH kinetics were fitted to squid voltage-clamp data.
- Neuron = R19 + slow recovery (FHN reduction) — interpretation — n/a (an interpretation of an emergent fact, not its source).
- Promoter γ orders organs / DWELL sets size (§12, §17, §20, §23) — open — reclassified [O] (dna §RB).
- Model gates §10, §13, §14, §18, §22 — identity — true by construction; relabelled [F].
- §2–§8 numbers — open — data-pending; 9.4 lies above the physiological range and is labelled illustrative.

## Open items
- Per-subject theta and gamma peaks against working-memory span (data-pending).
- The neuro_extension module that would reproduce §2–§8.
- A running CPG network rhythm.
- Moving the nine pain-lineage genes into the DNA atlas.
- Adding dna and chemistry edges to seams.
- Fixing the layout and CSS paths of `verify_all.py`.
- §19 α_em [O].
- Building-layer order and size [O] (dna §RB).
- SA-node and circadian unit emergence [O]; sourced, unfitted constants are needed.

## Reproduction
The ZIP contains `docs/neuro/` (the published HTML pages), `repro/neuro/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- Whole package: `python3 verify_all.py`, run from `repro/neuro/`.
- v1.11 gate: `python3 tools/gate_neuro_v1_11.py`.
- EM2: `python3 repro/neuro/experiments/EM2_hh_axon_emergence/em2_run.py`; compare with RESULT.json and PREREG.json.
- SEED = 19 where a seed is used. No network access is needed.

## Citation and links
- Site: https://jamming-physics.org/neuro/
- Concept DOI: 10.5281/zenodo.17979015
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
