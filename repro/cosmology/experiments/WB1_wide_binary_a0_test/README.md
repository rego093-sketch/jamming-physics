# WB1: a Gaia wide-binary test of a₀ = cH₀/2π (pre-registered; not run)

This is a discriminating test. Newtonian gravity predicts no velocity boost at any binary separation. The cosmology volume's law, a = g_N·ν(g_N/a₀) with a₀ = cH₀/2π, predicts a boost once g_N < a₀. For a 1.5 M☉ pair that happens at separations above about 7 kAU.

## Status
- The predictions have been computed: run `python3 wb1_predict.py`, which writes `PREDICTIONS.json`.
- The data have not been analysed. The Gaia archive, CDS, Zenodo and arXiv cannot be reached from this environment. Anyone with Gaia DR3 access can run the analysis described in `PREREG.json`.

## A gap in the theory, stated before the data
- The volume states the law using the internal field only. It says nothing about an external (Galactic) field.
- The Galactic field at the Sun is 2.06 a₀, and it can suppress the boost.
- Both variants are therefore registered in advance:
  - **H_int** (internal field only): velocity boost 1.29 at 10 kAU and 1.64 at 20 kAU.
  - **H_ext** (Galactic field included, crude bound): about 1.10–1.14 beyond 10 kAU.
- Whichever variant the data select or reject, the result is recorded. Neither variant is chosen after the data are seen.

| s (kAU) | g_N/a₀ | H_int | H_ext (bound) | Newton |
|---:|---:|---:|---:|---:|
| 5 | 3.41 | 1.090 | 1.052 | 1 |
| 10 | 0.85 | 1.288 | 1.105 | 1 |
| 20 | 0.21 | 1.644 | 1.133 | 1 |

## A finding from preparing this test
`legacy_v2_3/ch6_galaxy_rar.py` does not use the derived a₀ in its NGC 2403 fit. It uses the empirical value a₀ = 1.2×10⁻¹⁰ (line 34), so that fit does not test cH₀/2π. Separately, the volume already records that galaxy data constrain k in cH₀/k only to about 5–7.
