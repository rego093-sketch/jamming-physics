# MASTER MANUAL — Chronobiology (circadian_vp_site) · v0.3.0

The single operating manual for this package. Self-contained: substrate (FHN/R19), VP-SPEC v1.8, and node
identities ship inside the zip. Read order for a fresh session: **START_HERE → CHARTER → this manual.**

**DOI:** concept **10.5281/zenodo.20755413** (resolves to the latest version) · v0.2.0 snapshot
10.5281/zenodo.20755414 · CC BY 4.0. Wired across the canonical site and recorded in
`registry/cross_volume_doi.{csv,md}`.

## 1. What this package is
The ~24h circadian clock as a **self-sustained coupled limit-cycle oscillator network** (SCN master +
peripheral clocks) on the shared FHN/R19 substrate. It free-runs, is entrained by light (biphasic PRC,
Arnold tongue), synchronises as a master-led network, and **gates** defended setpoints (worked case: the HPA
cortisol axis). Disease is **clock–environment misalignment**. The package is SSOT for circadian phase/timing
and exports a gating signal to sibling homeostasis packages and a SIGN to the mind volume's affect layer.

## 2. Layout
```
START_HERE.md            bootstrap (KR instructions)
CHARTER.md               scope, nodes, seams, research program, governance
MASTER_MANUAL.md         this file
CHANGELOG.md             version history (SSOT)
COMPLETION_LEDGER.md     gate-by-gate completion record
HANDOVER_v0_3_0_to_v0_4_0.md  next-session entry point
IRREPRODUCIBILITY_LEDGER.md   every [O] with its stated obstacle
VERSION                  0.3.0
VP_SPEC_v1_8.md          full spec governing the writing phase
PHASE                    research|writing  (currently: writing)
registry/cross_volume_doi.{csv,md}  this volume's concept/version DOI + cited mind seam
inherited/               vendored measured γ + cited mind seam (JSON)
repro/
  _engine/vp_clk_engine.py     the oscillator engine (8 discriminants)
  _engine/vp_substrate.py      FHN/R19 cell — VENDORED, byte-identical
  _verify/gates.py             research/writing gate logic
  _verify/stress_tests.py      8-suite stress battery (RC1–RC6 + TX1)
  _pathology/setpoint_failure.py  5 disease failures + chronotherapy management
  run_all.py                   end-to-end: emerge → oscillate → battery → pathology → gates
manifest/circadian_vp_site.csv  chapter manifest (9 rows: §0 grounding + §1–§8)
reports/research_complete.json  gate artifact (all_green)
tools/build_docs.py      canonical SEO HTML generator (refuses while writing locked; DOI/JSON-LD/citation wired)
docs/circadian/          hub + §0 grounding + 8 canonical chapters + _meta.json (VP-SPEC §9 card)
docs/assets/css/site.css vendored stylesheet
docs/{robots.txt,sitemap.xml,llms.txt,llms-full.txt}
```

> **§0 grounding chapter** (`docs/circadian/00-grounding-measured-dna-emergence/`) is the "this is not a toy"
> page: answer-first, it foregrounds the measured BMAL1/ARNTL γ provenance, the deterministic reproducibility
> hash, the 8 falsifiable discriminants, and the [V]/[L]/[O] honesty triad. Read it first.

## 3. How to run
```
python repro/run_all.py          # research pipeline; prints gate status + writing lock
python tools/build_docs.py       # writing phase: emits docs/ (only when PHASE=writing)
```
`run_all.py` emerges the nodes from measured γ (to-measure masters held honestly), checks the oscillator,
runs the stress battery and pathology, evaluates the gates, and prints whether writing is unlocked.
`build_docs.py` refuses unless research is signed off (`reports/research_complete.json` all_green) **and**
`PHASE=writing`.

## 4. The eight discriminants (all PASS, seed=19)
| id | claim | headline number | grade |
|---|---|---|---|
| RC1 | molecular clock free-runs (limit cycle) + block control | 76 cycles, cv=0.003691; block→1 | [V] mech / [L] period |
| RC2a | biphasic light PRC (advance/delay/dead zone) | adv 0.185022 / delay −0.129012 cyc | [V] |
| RC2b | Arnold tongue (locking range widens with strength) | 5→11→15→15→15 detunings | [V] |
| RC3 | coupled-network synchronisation + master-led | coherence 0.596→0.99993; drift 0.003823→0.002956 | [V] |
| RC4 | HPA setpoint gating (clock creates the rhythm) | gated 0.976237 vs ablated 0.0 | [V] mech / [L] kinetics |
| RC5 | misalignment dysregulates the gated setpoint | signed amp 1.227923→−1.364039; reentrain 0→12 cyc | [V] sign |
| RC6 | circadian–mood seam (mind's locked contributor) | flattening index 0→2.11085 | [V] sign / [O] mag |
| TX1 | chronotherapy: right phase corrects, wrong worsens | corrected 2.56→0 h; worsened 5.44→11.2 h | [V] dir / eff=0 |

Aggregate result sha256: `417823934d6e3c0ad3ced5890a6da2da4da7ce7da57a693ded769b7f5dce612c`.

## 5. The measured input
BMAL1 (ARNTL) well **γ = 1.33348** — Gene ID 406, NC_000011.10, sequence sha256 `7293be92…`, fetched via the
DNA nearest-neighbour pipeline (SantaLucia 1998) through NCBI eutils and vendored to
`inherited/clock_promoters.cache.json` + `inherited/organ_gamma.json`. It is a **measured input, graded [V],
never fitted**. SCN and peripheral nodes are diffuse circuits (no single master gene).

## 6. The mind seam (firewall)
The mind volume modelled depression on an HPA withdrawal handle and **explicitly locked the circadian
contributor**. This package supplies it: misalignment flattens the gated HPA cortisol rhythm (RC6), and that
sustained, demand-misaligned signal **is** mind's withdrawal bias b<0 (→ lower coupling k=κ/(1+|b|) →
hypo-coordination → chronification under mind's plasticity layer). **Only the SIGN crosses.** The magnitude is
[O] (owned by mind); the felt quality of mood stays behind mind's Axis-A firewall (consciousness_claim=0, hard
problem open); efficacy=0; not medical advice. Cited mind concept DOI 10.5281/zenodo.20694404; mind anchor
R=0.38961455156044245 (engine tree 0fbf4988…) is cited, not recomputed.

## 7. Grades (VP-SPEC C3)
- **[V]** oscillator mechanism, PRC shape, synchronisation transition, every sign result (deterministic).
- **[L]** the ~24h period, cited HPA kinetics, cited clinical timing windows, cited relative-risk anchors.
- **[O]** absolute phase, inter-tissue lags, absolute incidence/RR magnitude, the depression-handle magnitude,
  the per-pulse chronotherapy gain — each listed with its obstacle in `IRREPRODUCIBILITY_LEDGER.md`.

## 8. Non-negotiable discipline
1. `vp_substrate.py` stays byte-identical (coupling/entrainment/gating are new dynamics on top).
2. No tuning: every constant is a measured input or a derived value, never chosen to hit a target.
3. Determinism: seed=19, 2× sha256 identical, before every release.
4. Firewall: timing in, felt quality out; efficacy=0; not medical advice; rare/monogenic → disease_wp.
5. Every [O] carries a stated obstacle, or the gate FAILs.
