# VP Chemistry & Electromagnetism — DOI Package

**Author:** Young jae Lee (ORCID 0009-0002-7535-8245), Independent researcher, Daegu, Korea
**DOI (reserved):** 10.5281/zenodo.20680541
**Version:** v1.0 (chemistry + electromagnetism, with applications) · 2026-06-14
**License:** documentation & data CC BY 4.0; code MIT (see `licenses/`)

---

## What this is

A single, self-contained, **fully reproducible** package for the Volume-Particle (VP) account of
**electromagnetism, chemistry, and their engineering applications**, all derived from one anchor —
the electron as a rotational dent in an infinitely rigid jamming lattice — using only $\pi$-geometry
and the electromagnetic inverse-square law. It is a companion to the VP Theory (physics) whitepaper
(DOI 10.5281/zenodo.17932567).

This edition consolidates the previously separate chapter files into **one whitepaper** (`whitepaper/
VP_Chemistry_EM.pdf`, 36 pp; LaTeX source `VP_Chemistry_EM.tex`) and adds two completions made
after the first release:

- **§EM.12 — dynamic field equations, Poynting's theorem, and causality** (longitudinal form),
  grounded in the AQD axiomatic field dynamics (DOI 10.5281/zenodo.17423870). New module
  `vp_em_field_dynamics.py`.
- **CO$_2$ electrocatalytic reduction**, re-grounded on the verified $d$-band CO-binding descriptor
  (copper's uniqueness for hydrocarbons). New module `vp_co2_reduction.py` + `cases_co2.csv`.

## Layout

```
whitepaper/
  VP_Chemistry_EM.pdf      consolidated whitepaper (36 pp)
  VP_Chemistry_EM.tex      single LaTeX source (compiles with xelatex)
  sources/                    markdown chapter sources + pandoc template (to regenerate the TeX/PDF)
core/                         chemistry + EM core (native layout; verify with --root .)
  code/foundation|materials|nuclear/   39 deterministic vp_*.py modules
  code/verify_chemistry.py    harness · code/gate_numeric_chem.py  numeric-drift gate
  data/cases_chemistry.csv (114) · cases_em.csv (62)
apps/                         applications (flat layout)
  vp_*.py                     9 application modules (catalysis, ammonia, water, ESS×3, materials, CO2)
  verify_applications.py      harness · vp_chem_numeric_ssot.py  numeric-drift gate
  cases_catalysis.csv (8) · cases_water.csv (12) · cases_energy_materials.csv (20) · cases_co2.csv (6)
licenses/                     MIT (code) + CC-BY-4.0 (docs/data)
SHA256SUMS.txt · RUNID.txt    integrity + deterministic run identifier
```

**Totals:** 48 deterministic standard-library Python modules (39 core + 9 applications);
222 case-ledger rows (176 core + 46 applications); one consolidated whitepaper.

## Reproduce

```sh
# chemistry + EM core  → 39/39 modules pass; ledgers 114 + 62 pass
cd core && python3 code/verify_chemistry.py --root .
python3 code/gate_numeric_chem.py                 # numeric-drift gate: PASS (zero drift)
python3 code/foundation/vp_light_emergence.py     # light emerges at c^2 = B/rho
python3 code/foundation/vp_em_field_dynamics.py   # dynamic field, Poynting, causality (EM.12)

# applications  → 9/9 modules pass; ledger 46 rows
cd ../apps && python3 verify_applications.py
python3 vp_chem_numeric_ssot.py                   # applications drift gate: PASS (17 anchors)
python3 vp_co2_reduction.py                       # CO2 reduction: copper uniqueness

# integrity
cd .. && sha256sum -c SHA256SUMS.txt
```

All modules are deterministic (standard library only); the harnesses verify execution, determinism
(re-run + hash compare), dependency, and case-ledger integrity. Every number in the whitepaper is
checked by a numeric-drift gate against both canonical recomputation and module output.

## Rebuild the whitepaper

```sh
cd whitepaper/sources
pandoc 00_front_full.md EM_CHAPTER_EN.md EM12_dynamics.md CHEMISTRY_CHAPTER_EN.md \
  CM_CHAPTER_EN.md CC_CHAPTER_EN.md CT_CHAPTER_EN.md CA_CHAPTER_EN.md CA_CO2.md \
  appendix_open.md 99_conclusion_full.md LIGHT_EMERGENCE_NOTES.md \
  -s -o ../VP_Chemistry_EM.tex --template=default.tex -H header.tex \
  -V mainfont="DejaVu Serif" -V monofont="DejaVu Sans Mono" \
  -V geometry:margin=2.3cm -V fontsize=10pt -V colorlinks=true --toc --toc-depth=2
cd .. && xelatex VP_Chemistry_EM.tex && xelatex VP_Chemistry_EM.tex
```

## Honesty note (read the Open-Items Register, Appendix O)

This package is trustworthy *because* it discards what does not work. The early "electron amplitude
(fm)" mechanism was tested and **refuted** (a Bragg band edge, not a resonance) and replaced by the
$d$-band energy descriptor; magnetic desalination and amplitude-to-electricity storage are refuted
and replaced by working alternatives. What remains **open** is admitted, not disguised — most
fundamentally the electromagnetic coupling $\alpha_{\mathrm{em}}$ (not derived; on hold), the global
$U(1)$ long-range hypothesis, and the absolute vector (magnetic/radiative) sector. Closing any of
these would be new physics, not a correction.

## Related

- VP Theory (physics, Volume I): 10.5281/zenodo.17932567 — *isSupplementTo*
- AQD axiomatic field dynamics (source of §EM.12): 10.5281/zenodo.17423870 — *references*
- VP Application notes (superseded qualitative version): 10.5281/zenodo.18043066 — *isRelatedTo*
