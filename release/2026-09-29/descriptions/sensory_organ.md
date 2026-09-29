# Special-Sense Organs

## Summary
Special-Sense Organs covers the special-sense organs (eye, ear, vestibular organ, taste and smell) as organ dynamics on inherited nodes. It inherits node identity and γ from the `dna` atlas and the excitable-membrane layer from `neuro`. Its one added module is organ dynamics: the Hopf cube-root amplifier plus the instrument physics of each organ. The headline, the cochlear Hopf response R = (F/β)^⅓ with exponent 0.333, is unchanged in wording. In the claims ledger it is an **identity**. The exponent is forced analytically by the cubic normal form (known from Eguíluz 2000 and Camalet 2000), and the integrator reproduces its own analytic value. Against observation, 1/3 sits at the top edge of the measured basilar-membrane compression range of ~0.2–0.33. The biology reading rule applies throughout. The volume accepts established observations and uses them, and does not decide theory. Each statement is labelled as an observation (cited), a code output (input dependence stated; "consistency (code)" when it checks the model against itself), or an interpretation; every DNA or VP mapping is an interpretation. Developmental order and size by γ are superseded, and building is [O] per `dna` §RB.

## What changed in this version (2026-09-29)
**Corrections**
- The transducer "maximum slope 3.1–3.3 ≈ Hill 3" is annotated as a grid-dependent code output, not a Hill coefficient (§3, §4, §9). A 21/41/81/161-point grid gives 2.39/3.32/4.54/6.07.
- The small-signal gain of ~464 at µ = 0 is annotated as set by the chosen probe force (F^(−2/3) at F = 1e−4). It is not a measured gain; the gains 1, 10 and 99 are 1/|µ| (§7).
- The disease relative crossing rates (1.00× … 52.46×) are annotated as depending on the chosen noise scale D (D_ref = B0/4). Only the barrier fraction (1 − d)² is D-free. Shapes are consistency (code), and absolute incidence is [O] (§10).
- Channel bistability for CNG, MET, TRPM5 and olfactory CNG is stated to hold by construction for any positive stiffness. It is a model property, not a verification.
- Developmental order and size by γ are superseded, per the reading-vs-building notes on §1, §2 and the hub. The γ-order schedule returned a measured null (dna §AX-A), order comes from regulatory-cascade depth (dna §AX-I), and building is [O] (dna §RB). The [V] on those pages covers in-model ranking only.
- Classical anchors are labelled as cited and not derived from the substrate: reduced eye, D/mm, the Hofstetter maximum-amplitude formula (name corrected), Greenwood, canal and VOR.
- Magnitude-firewall notes were added to §11 and §12. Clinical interventions and efficacy figures there are literature citations [L] for the direction of each lever, not framework outputs. No dose, concentration, exposure or schedule is given or implied.

**New experiments and results**
- None in this volume. Related: the downstream `ear` volume's EM1 hair-bundle emergence found a compression exponent of 0.22–0.32 from observed elements.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub, and 12 chapters were relabelled with observation, code output, consistency (code) and interpretation. No [F]/[V] theory grades remain in biology. The manifest verified count went from 21 to 0.

**Reproduction package changes**
- None to code. The review confirmed determinism, gates, stress tests and integrity, and found that the vendored γ equals the DNA source.

**Site/metadata**
- `seams.json` gained neuro and substrate edges. `_decl.json` was regenerated from the manifest, and hashes and lineage were refreshed; the gate is CLEAN.
- The corpus link audit repaired stale links (old "sensory-organs" slugs).
- Highwire citation meta was added to the hub.
- Corpus integrity checks and a wider magnitude-firewall pattern were added to the gate.
- Earlier site-assembly snapshot commits ("VP Theory site", "Final", "1111111", June 2026) carried no claim changes.

## Claim status (claims ledger)
Counts: identity 2 · anchor-restatement 3 · open 1.
- Cochlear Hopf R = (F/β)^(1/3), exponent 0.333 — identity — 1/3 at the top edge of the observed BM compression of ~0.2–0.33 (Ruggero 1997).
- Small-signal gain ~464 at criticality — anchor-restatement — equals F_probe^(−2/3), so it restates the chosen probe amplitude.
- Transducer maximum slope 3.1–3.3 matches Hill ~3 — anchor-restatement — a grid artefact (2.39–6.07 across grids); not a Hill coefficient.
- Developmental order argsort(γ), "taste latest confirmed" — open — contradicted by embryology (the PAX6 eye field precedes the otic placode) beyond the "taste latest" bit; superseded by dna §AX-A / §RB.
- Disease relative crossing rates 1.00× … 52.46× — anchor-restatement — depend on the chosen D.
- Classical anchors (reduced eye 22.27 mm, 2.69 D/mm, Greenwood 19.8 Hz–20.7 kHz) — identity — correct arithmetic of the cited classical formulas; not VP output.

## Open items
Author decisions from the review:
- Retract the "slope ≈ Hill 3" comparison, or replace it with a Hill coefficient computed from a declared model. It is currently annotated, not retracted.
- Decide whether "every channel verified bistable" should read "the R19 normal form at the master-gene γ is bistable (by construction); channel γ to be measured".
- Retire or regrade `order_grade` and `broad_validated` in `vp_sns_engine.py` after the dna §AX-A null, and reconsider TAS1R3 as the taste master gene.
- Regrade the cube-root exponent to [F]/identity and update the `_decl.json` counts.
- Clarify the SOX2 promoter vs locus γ window across dna and sensory_organ.

Open [O] items:
- Absolute disease incidence and timing need an external noise scale D and absolute basin depth.
- Building-layer order and size (dna §RB).
- Absolute channel thresholds are calibrations.

## Reproduction
The ZIP contains `docs/sensory_organ/` (the published HTML pages), `repro/sensory_organ/` (code and data), `LEDGER.json` and `MANIFEST.sha256`.
- Full research entry: `python3 repro/run_all.py`, run from `repro/sensory_organ/`. It covers emergence, probes, stress and pathology, and the gate.
- Gates: `repro/sensory_organ/repro/_verify/gates.py` and `stress_tests.py`.
- Engines: `repro/sensory_organ/repro/_engine/`, which holds `cochlear_amplifier.py`, `transduction.py`, `organ_optics.py` and `vp_sns_engine.py`.
- Pathology law: `repro/sensory_organ/repro/_pathology/`.
- Do not run `tools/build_docs.py` into `docs/`. The published pages carry later correction notes.
- SEED = 19. No network access is needed; promoter γ is vendored from dna.

## Citation and links
- Site: https://jamming-physics.org/sensory_organ/
- Concept DOI: 10.5281/zenodo.20755154
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
