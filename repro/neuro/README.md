# Neural Emergence Chain — integrated VP-SPEC package (chapters 00–23, v1.11.0)

One self-contained package for the neuro whitepaper "From Ion Channels to Behaviour: A
Falsifiable Neural Emergence Chain", reassembled from the fragmented per-chapter handoffs
into a single whole with duplication removed. Governed by `VP_SPEC_v1_8.md` (C1–C4), bundled at
the package root.

**v1.11.0** inherits the analgesic technique (`analgesic_threshold_logic` v2.0, DOI 10.5281/zenodo.20733420) into its home volume: §21 the 27-target three-lever firing-threshold map re-derived on this volume's own byte-identical engine (drift 0), §22 neuropathic pain as a firing-threshold shift + the three improvement levers, §23 the channelopathy anchor + the explicit DNA-emergence grounding (form ← γ). See `CHANGELOG_v1_11.md`. Run `python3 tools/gate_neuro_v1_11.py` for the v1.11 gate (11/11); `python3 verify_all.py` for the whole package (6/6).

## Verify everything with one command (from this directory)

```
python3 verify_all.py
```

Expected: `OVERALL: PASS (5/5 checks)` —
1. `repro/neuro/run_all.py` — 18 modules deterministic, frozen hashes match, HTML↔code drift 0 (incl. §18 + §19 EM capstones + §20 sensory-atlas capstone)
2. slug `16-muscle-force-length` — gate + determinism + fidelity 27/27 + [O] declared
3. slug `17-spinal-cord-locomotor-cpg` — gate + determinism + fidelity + ledger (21 items, 0 ungraded)
4. `tools/gate_neuro_16.py` — chapter-16 C1 gate, 16/16 (displayed numbers = regenerated, drift 0)
5. `tools/gate_neuro_17.py` — chapter-17 C1 gate, 39/39

## Layout (repo-relative)

```
docs/neuro/{00..20}/index.html      canonical chapters + docs/neuro/_meta.json (21 chapters; §18+§19 EM capstones, §20 = sensory-atlas capstone)
content/neuro-{15,16,17}-*.json     content data for the chapters built in-session (§1: code builds HTML)
tools/build_chapter_neuro.py        the deterministic content→HTML builder (single copy)
tools/gate_neuro_{16,17}.py         per-chapter C1 gates
tools/package_neuro_v18.py          package gater (00–15)
repro/neuro/{00..20}/               per-chapter reproduction (engines under _engine/, NCBI FASTAs under */inputs/)
repro/neuro/run_all.py + expected_sha256.json    reproduction harness + frozen hashes
reports/                            gate results + reproduction_manifest.json
manifest/                           file manifest
```

## Reproduction status — two yardsticks (honest)

**(A) Internal reproduction — complete.** Every displayed number is regenerated
deterministically (2×sha256), HTML↔code drift 0, across all 21 chapters. `verify_all.py` is 5/5.

**(B) External validation against measured biology — anchored at both ends, modelled in the middle.**

| chapter | reproduced | root-cause input | validated against | status |
|---|---|---|---|---|
| §12 sensory-organ-4d | organ emergence (STATE/ORDER/SIZE) | measured γ (LCT NCBI-verified pattern) | the 4D slugs' expected | **strong** (molecular anchor) |
| §16 muscle-force-length | force–length law | filament dimensions (measured EM structure) | Gordon–Huxley–Julian 1966 | **strong** — derived, \|Δ\|≤0.02 µm |
| §17 spinal-cord-cpg | ventral D-V order + CPG wiring | 19 master-gene promoters, NCBI GRCh38 2501 bp | measured D-V order p3/pMN/p2/p1/p0 + class wiring | **strong** — γ 0-drift; order from Shh spinodal |
| §04 code-working-memory | capacity = γ/θ | nested-oscillation structure | Miller 7±2 (ratio); tACS (causal [V]) | **partial** — ratio matches; absolute Hz [O] |
| §03 rhythm-bands | band structure | E/I model (tau_inh) | measured bands | structure [F]; absolute Hz [O] |
| §13/§15 em-emission/link | near/far field + multiplex | lattice model (c²=B/ρ) | electrophysiology + MEG (that the signal IS EM) | self-consistent **model**; identity observed |
| §14 motor-quantification | size principle: recruitment order + force-recruitment shape + **force-frequency twitch-fusion saturation** | rheobase = dVth/R_input (Ohm's law) on two cited cat-motoneuron datasets (Fleshman 1981; Gustafsson & Pinter 1984); Fuglevand-Winter-Patla 1993 analytical twitch (twitch-fusion) | measured orderly recruitment (Henneman 1965); measured sigmoidal tension-frequency (Rack & Westbury 1969) | **order: strong; magnitude: within-range; shape: derived** — order derived & matches measured recruitment; derived rheobases contained in Fleshman's measured 0.8–17.1 nA; force-frequency saturation **derived** as twitch fusion (dimensionless ν=f·T, monotone+saturating, reproduces R&W); measured span-excess (×3.353), newton scale, absolute fusion rate + mean-force plateau [O] |
| §18 em-brain-circulation (capstone) | near-field circulation loop: geometry + ionic ring + emission + multiplex | engine FHN oscillators + §13/§15 lattice emission, **wired together** (no new physics) | self-consistency: near-field dominance (r/(λ/2π)≈10⁻⁸), ionic timing (v≈3.20 m/s), lockstep winding (0.98225), multiplex (×-talk ≈5×10⁻¹⁶) | **model — physics [V]; function OPEN** (built & simulation-verified; whether the brain *uses* the near-field deferred to Mind) |
| §19 em-ephaptic-threshold (capstone) | endogenous near-field measured against the ephaptic threshold: ΔVm derivation + containment + at-threshold ratio | §18 near-field (**imported**) + cited measured cortical E-field (Fröhlich & McCormick 2010, \|avg\| 2.29 mV/mm) × measured sensitivity (Bikson 2004, 0.12 mV per mV/mm) | independently-measured induced ΔVm < 0.5 mV (Anastassiou 2011); entrainment threshold within the endogenous range (Fröhlich & McCormick 2010) | **model — physics [V]; function OPEN** (derived ΔVm 0.2748 mV **contained** in measured <0.5 mV, margin 0.2252; field **at** threshold ρ≈1, not weak — §18's "weak" was true only of scalp EEG; far-field radiative carrier stays retired; functional use deferred to Mind, decisive test named) |
| §20 complete-sensory-atlas (capstone) | the 4 remaining modalities (touch · pain · proprioception · vestibular) emerge from measured γ + transduce; somatosensory triad threshold contrast; proprioceptive loop closure; vestibular directionality | 14 sensory master-gene promoters, NCBI GRCh38 (cached); measured TRPV1 heat threshold 43 °C (Caterina 1997) | corr(γ,GC)=0.997 (γ is a real read-out); pain HIGH vs touch/warmth LOW threshold ORDER anchored to TRPV1 43 °C; reflex disturbance rejection ×10.4 | **strong (order) — model (magnitude)** — all 9 modalities emerge from measured γ; developmental ORDER + relative SIZE + threshold ORDER derived [F]; absolute size/time/firing magnitudes + mechanical noxious threshold + vestibular resting rate/gain [O] (ledger) |

**Motor side now has measured-validated anchors:** §16 (muscle mechanics vs GHJ), §17
(spinal locomotor architecture from NCBI γ + morphogen spinodal vs measured developmental order),
and §14 (the size-principle recruitment order derived from Ohm's law and bound to two cited
cat-motoneuron datasets, with the derived rheobases contained in the measured range and the
measured span-excess honestly reported).
The chain's two ends — molecular emergence and mechanical/architectural output — are measurement-bound;
the middle (rhythms, coupling, EM signalling) is internally reproduced and structurally consistent
with measurement, with absolute scales honestly `[O]`.

## Resolved across the v1.9 line — v1.9.0 → v1.9.3 (these were the v1.8 known issues)

- **§16 bare-zone fit — REMOVED.** v1.8 picked the bare-zone value 0.15 within its measured
  range [0.15, 0.20] so the plateau top landed exactly on GHJ's 2.20 (a fit). v1.9 reports the
  plateau top as the DERIVED RANGE 2.20–2.25 and validates GHJ's 2.20 by **containment** (it sits
  at the lower edge), not by an exact-endpoint \|Δ\|=0 hit. The three single-valued landmarks
  (zero, plateau floor, steepen) are still validated by \|Δ\| (max 0.02 µm).
- **§17 spinodal order — DE-CIRCULARIZED.** The ventral→dorsal order is now DERIVED from the
  measured cross-repression adjacency names + the Shh-threshold ranking (both read from data),
  not a hard-coded list; the output is bit-identical and the Briscoe-2000 match is now a real check.
- **§14 size principle — BOUND to cited measured biology.** Recruitment order is derived from
  Ohm's law (rheobase = dVth/R_input) and, in v1.9.1, locked to two cited cat-motoneuron datasets:
  Fleshman et al. 1981 (input resistance 0.8–5.1 MΩ, rheobase 0.8–17.1 nA) and Gustafsson & Pinter
  1984 (rheobase∝conductance, with the rheobase range exceeding the conductance range ~2×). A single
  derived 7.471 mV threshold (geometric-mean cell, not tuned) puts the pure-Ohm rheobases at
  1.465–9.339 nA, contained in Fleshman's measured range; the measured rheobase span exceeds the
  conductance-only prediction by ×3.353 (the G&P threshold-drift signature, honestly labelled [O]).
  The circular twitch→tetanus self-assertion is removed (that ratio is a locked measured input, not
  a derived match). Threshold-vs-rheobase drift and the absolute newton scale stay [O].
  **In v1.9.2 the force-frequency saturation is closed by derivation, not assertion:** summing the
  cited Fuglevand–Winter–Patla 1993 analytical twitch (h(τ)=τ·e^(1−τ), peak 1 at τ=1, no free
  parameter) at firing rate f gives a fusion index that rises monotonically and saturates, universal
  in the dimensionless rate ν=f·T — reproducing the sigmoidal tension-frequency shape Rack & Westbury
  1969 measured, with no tuned constant. The two firing-rate codes (rate vs recruitment) are unified
  onto the single measured 5-unit rheobase pool. The absolute fusion rate (f=ν/T, T muscle-dependent)
  and the mean-force plateau — which needs nonlinear Ca²⁺ summation, not modelled here — stay [O].
- **§03 absolute-Hz — SHARPENED.** The dimensionless γ/θ ≈ 7±2 (Miller; tACS-causal) is made
  explicit as the one validated quantity; the absolute theta/gamma frequencies in Hz are [O].
- **§18/§19 EM capstones — ADDED; EM advanced, not dismissed.** v1.9.1 added **§18**, which *wires the
  package's own modules together* (engine FHN oscillators + §13/§15 lattice emission + the light anchor)
  into a closed near-field circulation loop — building the *physics* `[V]` while keeping *function*
  OPEN. v1.9.3 added **§19**, which **quantifies** that local near-field against the **measured**
  ephaptic threshold: scaling the cited cortical field (Fröhlich & McCormick 2010, \|avg\| 2.29 mV/mm)
  by the cited sensitivity (Bikson 2004, 0.12 mV per mV/mm) gives a derived ΔVm = 0.2748 mV
  **contained** in the independently-measured <0.5 mV (Anastassiou 2011), and the field sits **at** the
  threshold (ρ≈1) — so §18's "weak" was true only of the volume-conducted *scalp* EEG, not the *local*
  near-field. The far-field *radiative* carrier stays retired (a different object, kept orthogonal);
  whether cognition *uses* the near-field stays OPEN, with a named decisive test (intracranial field
  cancel-vs-augment), deferred to Mind. No tuned constant.
- **Builder path bug — FIXED.** `tools/build_chapter_neuro.py` now writes to the package-root
  `docs/` (matching its docstring), so "rebuild HTML then re-gate" is reproducible.

See `CHANGELOG_v1_9.md` and the next-session handover (`WORK_HANDOVER_next_session.md`) for details
and the remaining open items.
