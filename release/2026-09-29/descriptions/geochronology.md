# Cross-Chronometer Limit

## Summary
Cross-Chronometer Limit (Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit) is a methods volume of the VP corpus. It is listed as inheriting from the physics and geodynamics volumes and adds one module: an incorporation / dating-accuracy limit shared by radiocarbon and zircon U-Pb. The headline — incorporating older foreign material biases a sample's age old — is classed as identity in the claims ledger: it is mass balance and textbook geochronology, not a VP-physics claim. Its one genuine held-out test, a leave-one-out reservoir-offset correction, reduces radiocarbon error out of sample (independent prediction; residual RMSE 141 yr and 453 yr, n = 3 pairs per site, standard method). The zircon demonstrations recompute published results with standard methods.

## What changed in this version (2026-09-29)
**Corrections**
- None to the volume's claims or text; no correction notes were added in this version.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- None.

**Reproduction package changes**
- Repro links on all 14 chapter pages and the hub repointed from stale paths to the existing repro/geochronology/repro/geochronology/<chapter>/ folders.

**Site/metadata**
- Declarations: a _decl.json was added for the volume, and the R19 switch kernel is no longer claimed by it (primitives aligned with the manifest); an inherits strip was added to the hub.
- Highwire citation meta regenerated from the manifest (citation title now "Cross-Chronometer Limit"; DOI, abstract URL, language); page head metadata consolidated; the old hand-built "Cross-package connections" block removed from the hub.
- Corpus link audit repaired stale GitHub repro and site URLs; manifest row and content/repro hashes recorded in the lineage; corpus integrity checks added to the gate.

## Claim status (claims ledger)
5 rows: identity 2 · independent-prediction 1 · anchor-restatement 1 · interpretation 1.
- Incorporating older foreign material biases a sample's age old (headline) — identity — direction by mass balance; documented cases (Riggs 1984; Keith & Anderson 1963; Heaton et al. 2020).
- Closure/exchange number N_D = Dτ/L² equals the Fourier number and Dodson's grouping — identity — dimensional-analysis identity (graded [I] in the volume).
- Leave-one-out reservoir-offset correction reduces radiocarbon error out of sample — independent-prediction — RMSE 418 → 141 yr (Elk Hills), 739 → 453 yr (Lake Chichancanab); n = 3 pairs per site; standard practice, nothing VP-derived.
- Lava Creek: classifying zircon by crystal position recovers the eruption age — anchor-restatement — faces weighted mean ≈ 626.5 ka, ≈ 0 vs the published rim age (same data, by construction), about −4.5 ka vs the ≈ 631 ka eruption.
- 204Pb common-Pb correction and youngest detrital grains for maximum depositional age — interpretation — depends on an assumed Stacey–Kramers-type common-Pb composition; demonstrates a standard method.

## Open items
- The Lava Creek input file dss1.xls is not shipped and must be downloaded.
- The general-case U-Pb demonstration clones IsoplotR and needs network access.
- Remaining limits of the method are stated in §11 (working range, honest limits) and §12 (grading, attribution, severity, test strength); see repro/geochronology/IRREPRODUCIBILITY_LEDGER.md.

## Reproduction
The ZIP contains docs/geochronology/ (the published HTML pages), repro/geochronology/ (code and data), LEDGER.json (this volume's claims-ledger rows), CORPUS_GUIDE.md and MANIFEST.sha256 (SHA-256 of every file).
Main checks (Python 3):
- Radiocarbon demonstration data: repro/geochronology/repro/geochronology/06-demonstration-i-radiocarbon-homogeneous-case/data/*.csv (leave-one-out recomputation; no network).
- `python3 repro/geochronology/repro/geochronology/07-demonstration-ii-zircon-u-pb/01_lava_creek_canonical.py` (needs the published dss1.xls, downloaded separately).
- `python3 repro/geochronology/repro/geochronology/08-demonstration-iii-zircon-u-pb/02_isoplotr_common_pb_detrital.py` (clones IsoplotR; needs network).
- Documented cases: repro/geochronology/repro/geochronology/09-documented-cases-mechanism-real-chronologies/cases_catalogue.csv.
Deterministic scripts use SEED = 19 where randomness is involved.

## Citation and links
- Site: https://jamming-physics.org/geochronology/
- Concept DOI: 10.5281/zenodo.20568673
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
