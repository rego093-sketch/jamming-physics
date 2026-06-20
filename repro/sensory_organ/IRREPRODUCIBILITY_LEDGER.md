# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL. Updated for v0.4.0 (published: concept DOI assigned + PDF/TeX deposit
artifacts). Publication only renders/derives from the verified corpus, so it added **no new `[O]`**; the
open-items table below is unchanged from v0.2.0 and remains valid.

## Open items (with stated obstacle)

| item | grade | obstacle | location |
|---|---|---|---|
| transducer γ (CNGA1/CNGB1, TMC1/PCDH15/CDH23, SLC26A5, TAS1R2/TRPM5, CNGA2/ADCY3) | [O]→[V] | channel identity + NCBI/UniProt cited [L]; γ measured by the DNA pipeline (SantaLucia NN ΔG37, proximal promoter), not computed or guessed here (SSOT) | inherited/organ_gamma.json (_to_measure) |
| to-measure master-gene γ (clock / parathyroid / senescence …) | [O]→[V] | named master not yet in the DNA atlas; fetch via fetch_morpho_gamma (cross-species), measured input not fitted | inherited/organ_gamma.json (_to_measure) |
| organ-level optics / acoustics (sensory) | classical | not an R19 claim — documented + linked from classical physics (lens equation, basilar resonance, canal torsion-pendulum); arithmetic reproduces the cited anchor [V-arith] | sensory CHARTER RS1/RS3/RS4; organ_optics.py |
| absolute disease incidence / lifespan / phase | [O] | setpoint-drift SHAPES reproduce [V] (quadratic barrier collapse, Kramers rate); absolute values need the noise scale D and absolute basin depth — external calibration | _pathology/setpoint_failure.py |
| fine developmental order among early eye/ear nodes | [O]→[L] | broad signal "taste specified latest" validated [V]; fine ordering needs cited stage-timing (PAX6/RAX eye-field & EYA1/SOX2 otic placode co-occur early) | vp_sns_engine.validate_developmental_order |
| Hopf criticality μ=0 (exact operating point in vivo) | [V]-hypothesis | the cube-root exponent 1/3 is parameter-free AT μ=0 [V]; how close a real OHC sits to μ=0 is an empirical/self-tuning question, not fitted here | cochlear_amplifier.py |
| clinical efficacy of root-cause therapies | [L]/contested | substrate mapping [V]; clinical evidence is cited literature with level — AMD complement: anatomic only, NO functional acuity gain yet (partial); cataract chaperone reversal: replication FAILED (contested); ATOH1 hair cells: immature (contested for acquired SNHL) | _pathology/treatment.py; literature/ |

## Resolved in v0.2.0 (was open, now verified in-sim)

| item | resolution |
|---|---|
| "is the transducer really a switch?" | [V] — transduction.py shows bistability + discontinuous flip + hysteresis for every channel with vendored γ |
| "where does the cochlear cube-root come from?" | [V] — cochlear_amplifier.py derives exponent 1/3 from the Hopf normal form at μ=0, parameter-free |
| "do the organ instruments hit the cited numbers?" | [V-arith] — organ_optics.py reproduces axial 22.27 mm, 2.69 D/mm, presbyopia 1 D@60, Greenwood 20 Hz–21 kHz, canal velocity-band flatness 0.018 |
| determinism with the new modules | [V] — 2×sha256 identical across separate processes (6a68bc48…) |

*Note:* `literature/` (CITATIONS.md, citations.json) is documentation, not read by the engine; it does not
affect the result hash. `reports/research_complete.json` records the signed-off green state.

**Writing phase (v0.3.1):** the canonical HTML in `docs/` is generated deterministically from the verified
result (`reports/emergence_results.json`, 2×sha256 `6a68bc48…`); numbers are loaded, BUILD_DATE is fixed
(no wall-clock), so `docs/` rebuilds byte-identical (search/SEO gate 0 FAIL / 0 WARN). The v0.3.1 expansion
(12 chapters incl. the §2 no-tuning method and §12 references/provenance, deeper prose, `<h2>` subheads,
JSON-LD `keywords`, de-self-deprecated framing) added **no new `[O]`** — it only renders the verified
corpus, and grades and stated obstacles are carried through verbatim onto each page.

**Publication phase (v0.4.0):** the concept DOI `10.5281/zenodo.20755154` was wired into the generator and
the canonical HTML re-rendered byte-identical (0 `TBD` remaining); a deterministic LaTeX/PDF whitepaper was
generated from the **same** authored prose-as-data and the **same** verified numbers — so the PDF cannot
drift from the site. `dist/sensory_organ_vp_site.tex` is byte-identical on regeneration (sha256
`6e76c5dd…`), and `dist/sensory_organ_vp_site.pdf` is **byte-identical across independent compiles**
(sha256 `c6593c81…`) via SOURCE_DATE_EPOCH + `\pdfinfoomitdate` / `\pdftrailerid`. Publication introduced
**no new `[O]`**. PHASE is `published`; the gate unlocks for {writing, published} with research still
required green.
