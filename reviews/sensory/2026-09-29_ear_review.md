# ear volume — light review (2026-09-29)

Scope: `docs/ear/` (hub + 7 chapters + 3 concept pages), `docs/ear/_decl.json`, `repro/ear/`.
Two reviewers: R1 (claims vs data), R2 (code and inheritance). Nothing was edited. Scripts were run with python3 and a 120 s timeout. The gate was run on a scratch copy, not in the repo.

## Summary

1. The numbers are reproducible. All 81 displayed numbers come from `vp_numeric_ssot.py` with drift 0, and the magnitude firewall holds: no dose, concentration or clinical magnitude appears anywhere. The honest-negative lists are thorough.
2. Several grades are too strong. Some identities and internal numerical checks are labelled [V], and "CF_max = 20677.07 Hz [F]" contradicts the page's own [O]. In §1, emergence order = argsort(spinodal(γ)) is graded [F], which contradicts the DNA atlas rule that order comes from cascade depth, not γ.
3. The repro gate and seed verifier both FAIL as shipped. They look for `repro/ear/docs/`, but the pages now live in `docs/ear/`. The cube-root result is inherited from `sensory_organ`, but no page or `_decl.json` declares that seam.

## R1 findings (claims vs data)

**R1-1 [should-fix] Emergence order from γ is graded [F]. This contradicts the DNA atlas.**
`docs/ear/01-place-and-traveling-wave/index.html`: "Emergence order = argsort(spinodal(γ)) with the A4 SHAPE breaking γ-ties: TMC1 0.5724 < PCDH15 0.6233 < CDH23 0.7336 < TMIE 0.7468 [F]" and "a lower discontinuous threshold means earlier switch competence."
The DNA volume says emergence order is cascade depth, "not a local barrier". AGENTS.md §1 says developmental order comes "from regulatory-cascade depth, not γ", and §8.1 says order belongs to the atlas. N2 on the same page admits that agreement with real timing is [O], but the order itself is still sold as a forced "emergence order". The neuro review (2026-09-28) raised the same issue. Fix: call it "spinodal-threshold rank" (a reading), not an emergence or developmental order, or take the order from the atlas.

**R1-2 [should-fix] "Reproduces Greenwood to 2×10⁻¹⁶ [V]" is an algebraic identity, not a verification.**
`docs/ear/01-place-and-traveling-wave/index.html`: "√S ∝ 10^(a·x) reproduces Greenwood's term to max|ratio−1| ≈ 2×10⁻¹⁶ [V]".
The code in `repro/ear/inherited/vp_sound_wave.py:101` is `ratio = (fG + 165.4*0.88) / (165.4 * 10**(a*x))`. With fG = 165.4·(10^(a·x) − 0.88), this ratio is 1 by construction, so the check cannot fail. The inverse-Greenwood round-trips (250 Hz → 0.18 …, "[V]") are also function∘inverse identities.
The real content, that a √-law on an exponential stiffness gives an exponential map, is a correct [F]. Fix: drop the [V] on the identity checks.

**R1-3 [should-fix] Cube-root exponent 0.333333 is graded [V], but it was never tested against measured compression.**
`docs/ear/02-cochlear-amplifier/index.html`: "The integrator's read-off exponent is 0.333333 and the gain exponent −0.666667 [V]".
This fit is the inherited integrator converging to its own analytic fixed point (`vp_numeric_ssot.py`: `polyfit` of `SUB.settle(0,h)`). It is not a falsification test against data.
Measured basilar-membrane compression at CF is commonly about 0.2 dB/dB (chinchilla base, Ruggero et al. 1997; human behavioural estimates are about 0.2–0.3). That puts 1/3 at or above the top of the observed range. N2 acknowledges this honestly ("study-dependent I/O slope (~0.2–0.5 dB/dB)… [O]"), but 0.5 is a generous upper bound.
The Hopf cube root is also established prior work (Eguíluz et al. 2000; Camalet et al. 2000) and is not cited. Fix: grade the exponent [F] (analytic) and add an explicit data comparison, noting that 1/3 sits at the high edge. Cite the Hopf literature.

**R1-4 [should-fix] "Compression is uniform across frequency [F]" is contradicted by observation.**
`docs/ear/02-cochlear-amplifier/index.html`: "Every place carries the same critical cubic, so the 1/3 exponent is CF-independent — compression is uniform across frequency [F]."
Apical (low-CF) cochlear regions show weaker compression and weaker, less CF-specific nonlinearity than basal regions (e.g. Robles & Ruggero 2001 review; apical recordings by Cooper, Rhode and others). The CF-independence follows from the model assumption, not from the ear. Fix: grade it as a model consequence and name the apical discrepancy as an [O] or a falsification.

**R1-5 [should-fix] The audible band is "derived", yet its edges are the Greenwood calibration, and CF_max is graded both [F] and [O].**
`docs/ear/06-audible-band/index.html`: "the base's finite stiffness fixes a finite ceiling CF_max = 20677.07 Hz [F]". The same page's N1 and N3 say "The absolute band edges CF_min / CF_max (Hz) are [O]". The hub says "Why we hear ~20 Hz–20 kHz is derived".
19.848 Hz and 20677.07 Hz are simply CF(0) and CF(1) for Greenwood's A = 165.4, a = 2.1, k = 0.88. Those constants were chosen to span the human audible range, so the edges are inputs [L]. The "6.976049 oct" bare term is just a·log₂10.
Also, "a ratio ~10⁶ is the basilar membrane's graded geometry [L]" is not anchored to a stiffness measurement. It is back-computed from Greenwood (1.0853×10⁶ = (CF ratio)²). Direct BM point-stiffness gradients are, to this reviewer's knowledge, far smaller (roughly 1–2 orders of magnitude), which is the classic reason pure local-resonance models need mass and fluid loading. Fix: remove the [F] on CF_max, change "derived" to "read off the calibrated map", and either cite a measured stiffness ratio or grade the 10⁶ as [O] with that discrepancy stated.

**R1-6 [should-fix] "~120 dB" is an ungraded magnitude, while N1 says dynamic range in dB is [O].**
`docs/ear/02-cochlear-amplifier/index.html`: "the gain falls as F^(−0.666667) — the ~120 dB compression" and "faint drives amplified ~100× more than loud, the dynamic-range compression that lets the ear span ~120 dB". N1 on the same page says "dynamic-range-in-dB … are [O]". Fix: mark 120 dB as a cited literature value [L], and state over how many decades "~100×" applies.

**R1-7 [nit] Other grade and wording overreach.**
- §3 (`03-congenital-deafness-failure-modes`): the overlap of 0.1474 "prov[es] it reads structure only". Overlap shows γ does not separate the classes. It does not prove what γ reads.
- §4 (`04-readout-synapse-otoferlin`): s = +1.3864 and release 0.5810 → 0.0000 are graded [V]. They are model outputs in arbitrary units, not a data test. The OAE⁺/ABR⁻ fingerprint and "cooperativity m is cited [L]" are handled correctly.
- §5: the group delay "10.0 / 40.0 / 160.0 [V]" displays the law 2Q (`vp_numeric_ssot.py` computes `2.0*Q`) rather than the numeric τ_max that E6 does compute (10.025 / 40.006 / 160.001). Display the numeric value next to the law.

**R1-8 [no action] The magnitude firewall is intact.**
No dose, concentration or molecule magnitude appears in §3, §4 or §7. Lever statements are direction-only ("restore Ca²⁺-sensor coupling, with no molecule, dose…"). The "~3–6 kHz" notch is a cited clinical frequency and is itself marked [O]. The basal-first presbycusis direction and the OTOF auditory-neuropathy fingerprint agree with established observation.

## R2 findings (code and inheritance)

Scripts run (`repro/ear/`):

| Script | Result | Matches pages? |
|---|---|---|
| `volume/tools/vp_numeric_ssot.py` | exit 0, 60 facts, sha `ee6e681f…` | yes. It is the page source, and the gate's `display_drift_zero` passes (81 spans, drift 0) |
| `volume/tools/gate_volume.py` | **crash**: `FileNotFoundError …/repro/ear/docs/index.html` | could not run in place (R2-1) |
| `tools/verify_seed.py` | **SEED VERIFY: FAIL**. Only block [4] fails: 16 "MISSING: docs/…". Hashes, DNA recompute (19 genes, 0 mismatches) and E-numbering pass | — |
| `inherited/vp_sound_wave.py` | exit 0. Greenwood 19.8 / 1710.3 / 20677.1 Hz, exponent 0.3333 | yes (19.848, 20677.07) |
| `research/E6-traveling-wave-envelope/run.py` | τ_max 10.025 / 40.006 / 160.001 vs 2Q | the page shows the law value (R1-7) |
| `tools/check_integrity.py` (repo root) | links PASS (0 broken), scripts PASS (13 known gaps, 0 new), aggregates PASS | — |

**R2-1 [should-fix] The shipped gate and verifier point at a directory that no longer exists.**
`repro/ear/volume/tools/gate_volume.py:26` has `DOCS = os.path.join(PKG, "docs")`, and `repro/ear/tools/verify_seed.py` expects `repro/ear/docs/*`. The pages were moved to `docs/ear/`.
On a scratch copy with `docs/ear` placed back as `ear/docs`, the gate gives:
- passes: ssot 2× determinism, drift 0 (81 numbers), and chapter, hub and concept structure;
- fails: `build_on_disk_byte_match`, because the hub `index.html` has a byte-diff (the deployed hub carries corpus-injected "Inherits" chips);
- fails: `sitemap.xml` / `robots.txt` / `llms.txt` missing, because they are now corpus-level;
- fails: 2 links, `/modules/#kernel` and `/modules/#dna_interpretation`, which resolve at site level (the repo `check_integrity.py` passes them).

So the README's "gate-clean / drift 0" claim is true for numbers but cannot be reproduced from the repo as shipped. Fix: add a `--docs` argument (default `../../docs/ear`) and drop the per-volume sitemap, robots and llms expectations.

**R2-2 [should-fix] The seam to sensory_organ is undeclared.**
The cube-root amplifier is labelled in code as inherited: `inherited/vp_sound_wave.py:40` says "cube-root (1/3) compression at the Hopf bifurcation: [V] parameter-free (sensory_organ §7)". However, `docs/ear/_decl.json` lists only `physics:wave+cubic` and `dna`, and no ear page mentions `sensory_organ` or "Hopf" (grep count 0). AGENTS.md §3.2 rule 5 and §8.4 prohibit silent seam crossing. Fix: declare `sensory_organ` (Hopf cube root) as an inherited source, or state that ear re-derives it from the R19 cubic and remove the sensory_organ tag.

**R2-3 [nit] The `_decl.json` inheritance label conflicts with AGENTS.md on where R19 lives.**
`_decl.json` says `"physics:wave+cubic"`, but AGENTS.md states that R19 is "not in physics; first stated in dna". The hub chips read "Inherits: R19 switch · DNA interpretation". Suggest `physics:wave` plus `dna:R19`.

**R2-4 [no action / note] There is no re-derivation of DNA-atlas nodes in γ.**
The 19 ear genes (TMC1, TMC2, OTOF, …) are not in the DNA atlas pages. Ear measures them with the inherited `dna_interpreter.gamma`, and they recompute offline bit-for-bit (verify_seed [3] PASS, corr(γ,GC) = 0.996). That is an allowed use of the inherited reader. The only atlas-contract problem is ORDER (R1-1).

**R2-5 [nit] The version and DOI labels are inconsistent.**
- Versions: `repro/ear/VERSION` = 0.12.0, the README headline says v0.11.0, and every page footer says "v0.10.0".
- DOI: the header badge on every page is `doi:10.5281/zenodo.20471407`, which is the DNA volume's DOI. The volume's own concept DOI, 10.5281/zenodo.20790201, appears only in the footer. Readers will take the badge as this volume's DOI.
- Grades: `_decl.json` grades have no key for [L], but the pages use [L] about 6 times.

## Action table

| # | Finding | Severity | File / evidence | Bucket |
|---|---|---|---|---|
| R2-1 | Gate and verifier look for `repro/ear/docs` and crash or FAIL | should-fix | `repro/ear/volume/tools/gate_volume.py:26`, `repro/ear/tools/verify_seed.py` | Fix now (small, safe) |
| R2-5 | Footer version v0.10.0 vs VERSION 0.12.0; header DOI badge is the DNA DOI | nit | `repro/ear/VERSION`, all `docs/ear/*/index.html` (rebuild via builder) | Fix now (small, safe) |
| R2-3 | `physics:wave+cubic` vs AGENTS "R19 first in dna"; no [L] key in decl | nit | `docs/ear/_decl.json` | Fix now (small, safe) |
| R1-2 | Identity checks (Greenwood ratio, inverse round-trips) graded [V] | should-fix | `docs/ear/01-…/index.html`; `repro/ear/inherited/vp_sound_wave.py:101` | Fix now (grade label only, via `chapters.py`) |
| R1-7 | "proves structure only"; model outputs graded [V]; §5 shows law not numeric τ | nit | `docs/ear/03-…`, `04-…`, `05-…` | Fix now (small, safe) |
| R1-1 | argsort(spinodal(γ)) sold as [F] emergence order, against DNA cascade-depth rule | should-fix | `docs/ear/01-…/index.html` | Needs author |
| R1-3 | Exponent 1/3 [V] without a data test; measured ≈0.2 dB/dB; Hopf literature not cited | should-fix | `docs/ear/02-cochlear-amplifier/index.html` | Needs author |
| R1-4 | "Compression uniform across frequency [F]" vs weaker apical compression | should-fix | `docs/ear/02-cochlear-amplifier/index.html` | Needs author |
| R1-5 | CF_max both [F] and [O]; band "derived" from calibration; 10⁶ stiffness ratio not measured | should-fix | `docs/ear/06-audible-band/index.html`, hub | Needs author |
| R1-6 | "~120 dB" / "~100×" ungraded magnitudes vs N1 [O] | should-fix | `docs/ear/02-cochlear-amplifier/index.html` | Needs author |
| R2-2 | Hopf cube root inherited from sensory_organ, seam undeclared | should-fix | `repro/ear/inherited/vp_sound_wave.py:40`; `docs/ear/_decl.json` | Needs author |
| R1-8 | Magnitude firewall intact | — | §3, §4, §7 | No action |
| R2-4 | Ear genes measured with inherited reader; no atlas γ re-derived | — | `repro/ear/tools/verify_seed.py` [3] PASS | No action |
| — | Repo links / scripts / aggregates | — | `tools/check_integrity.py` all PASS | No action |

No blockers found. Nothing presents a fitted number as derived in a way that changes a headline. The main issues are grade inflation, one inheritance-contract conflict (R1-1), one undeclared seam (R2-2) and a broken local gate path (R2-1).
