# VP — The Eye Volume: the high→low down-conversion ladder (E0→E8) + mechanism extensions (E9–E12)

## Summary
The Eye volume reads vision as a high→low down-conversion ladder (E0→E8) with mechanism extensions (E9–E12). It inherits the wave substrate from `physics` (c² = B/ρ), node identity and the γ reader from `dna`, and the graded-to-spike layer from `neuro`. The one added module is the ladder itself. It includes a single-photon R19 switch, a refraction reading n = √(B/ρ ratio), and cube-root gain control. The headline "single-photon R19 flip; n = √(B/ρ ratio)" is unchanged in wording, but both parts are now graded down.
- The single-photon flip is an **interpretation**. It is a property of the model switch, and it conflicts with the measured graded, reversible rod single-photon responses (~1 pA, n ≈ 1; Baylor, Lamb & Yau 1979; Rieke & Baylor 1998). The measured Hill ≈ 3 belongs to CNG-channel cGMP gating. The photon→drive link is [O].
- The refractive index is an **anchor restatement**: n = 4/3 is the cited input, with no independent B or ρ.

The biology reading rule applies. The volume accepts existing observations and uses them. Every statement is an observation (cited) or a code output (input dependence stated), and mappings of VP/DNA onto the eye are interpretation. [V] on these pages means "reproduced by code", not tested against external data. Emergence order and size by γ are building and stay [O] per `dna` §RB.

## What changed in this version (2026-09-29)
**Corrections**
- E2: the single-photon flip is relabelled as interpretation. The measured rod responses (graded, reversible, dim flashes summing roughly linearly) are placed next to the model. The measured Hill ≈ 3 is assigned to CNG cGMP gating, not to the cubic order. The model's all-or-none flip is stated as not verified by these observations.
- E9: "M–L margin smallest ⇒ red-green is the most fragile axis" is restated as a code output with its sensitivity. The ordering flips with a 1 nm peak shift, and under ±2 nm jitter (seed 19, n = 2000) M–L is the smallest margin only 39% of the time. Reading it as the cause of red-green fragility is interpretation.
- E10: "Weber-like" is corrected. With a fixed criterion the model gives ΔI ∝ I^(2/3), which is not Weber. The contrast gain of 1/3 is compared with the observed Stevens brightness power-law exponent (~1/3). Weber–Fechner is stated as the separately observed photopic law.
- E0/E1: "colour = the angle χ" is labelled interpretation. The inherited colour module gives violet and red the same angle. Trichromacy is the observation.
- E0/E3: the 633/532 closure ratio (1.189831), m·sinχ·D/λ = 1, and the Snell two-path agreement are labelled identities that hold by construction (consistency, not evidence). The chromatic split of 0.0 mm is labelled a single-index model output: the real eye shows longitudinal chromatic aberration, which is [O] here.
- E1/E11 and the hub: the cone/rod order by spinodal(γ) and size by dwell are labelled code output and interpretation; developmental order is building [O].
- Atlas wording: the rod, cone and disease-gene γ values (AIPL1, RPGR, PDE6B, OPN1*, GNAT1) are stated as measured by this volume with the inherited DNA reader, not taken from the dna atlas. PAX6 γ equals the atlas value.
- Transcript hashes are relabelled as hashes of the printed output (stdout), not of the source file.

**New experiments and results**
- None run. Unit-level emergence of a rod single-photon response from the observed cascade (rhodopsin → transducin → PDE → cGMP → CNG, with Ca feedback) is named as the next unit and left [O]. It needs one sourced set of cascade rates, which could not be verified here. The compare target is Baylor, Lamb & Yau 1979.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. Pages E0–E12 were relabelled to observation, code output, consistency and interpretation, and the manifest forced/verified counts are 0.

**Reproduction package changes**
- None to the computations. The transcript hash labels changed in the rendered pages.

**Site/metadata**
- The volume was integrated into the corpus site and repository (docs + repro, 2026-09-29).
- Registry: `_decl.json` was regenerated from the manifest, and hashes and lineage were refreshed; the gate is CLEAN.
- The neuro §11 eye γ now defers to the atlas.
- Highwire citation meta was added to the hub.
- Earlier site-assembly snapshot commits ("11111", "1111111", June 2026) included the light_emergence module wiring (eye E0/E5 canonical; 633/532 closure). No claim changed.

## Claim status (claims ledger)
Counts: interpretation 2 · anchor-restatement 1 · identity 1 · open 2.
- (a) Single-photon R19 flip; Hill ~3 from the cubic — interpretation — conflicts with the observed graded rod response (n ~ 1); the 231× steepness depends on the sweep step; the photon→h link is [O].
- (b) n = √(B/ρ ratio); reduced eye 60.06 D / 22.2 mm — anchor-restatement — matches, because n = 4/3 is the input.
- Red-green is the structurally most fragile axis (M–L margin 0.0421°) — open — the ordering flips with a 1 nm shift and holds 39% of the time under ±2 nm jitter.
- 633/532 closure 1.189831; m·sinχ·D/λ = 1 — identity — by construction.
- Light/dark adaptation contrast gain → 1/3 — interpretation — consistent with the Stevens exponent; not Weber.
- Cone/rod emergence order by spinodal(γ); size ~ dwell γ^1.5 — open — building layer [O].

## Open items
Author decisions from the review:
- Downgrade E9 from [F] to [O], or reformulate it. This was flagged as the blocker; the page now states the jitter sensitivity.
- Decide whether colour-as-angle survives violet χ = red χ, and at minimum grade E1 trichromacy-as-angle as [O] or hypothesis.
- Redefine volume-wide [V] per AGENTS.md, and regrade the tautologies and model-internal checks.
- E2: remove "single-photon sensitivity as pure structure", or keep it with the stated conflict (currently kept, with the conflict stated).
- Upstream the eye-local gene γ values into the DNA atlas, or keep them labelled eye-local.
- Drop "chromatic split 0.0 mm" as a key result.
- Tooling: make `DOCS` in `repro/eye/tools/_volume_lib.py` resolve to the repo `docs/eye`, or document the layout; drop or generate the promised sitemap, robots and llms files.

Open [O] items:
- The absolute photon → drive → firing scale.
- The literal physiological rod Hill value.
- Longitudinal chromatic aberration.
- Rod single-photon unit emergence (needs sourced cascade rates).
- Building-layer order and size.

## Reproduction
The ZIP contains `docs/eye/` (the published HTML pages), `repro/eye/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- One-command gate: `python3 tools/verify_seed.py`, run from `repro/eye/`. Expect `SEED VERIFY: PASS`. It checks no-regression of the inherited artifacts, deterministic reproduction of the foundation, and the gene γ values.
- Per-chapter modules: `repro/eye/research/E*/run.py` (E1–E12). For example, `repro/eye/research/E2-single-photon-switch/run.py`, `E9-red-green-dichromacy/run.py` and `E10-light-dark-adaptation/run.py`.
- `repro/eye/tools/gate_volume.py` re-runs the modules and checks that the HTML and code agree (drift 0).
- Do not rebuild into `docs/`. The published pages carry later reading-rule edits.
- SEED = 19. No network access is needed; promoter γ is cached. `tools/fetch_promoter_gamma.py` is the only step that uses the network.

## Citation and links
- Site: https://jamming-physics.org/eye/
- Concept DOI: 10.5281/zenodo.20790134
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
