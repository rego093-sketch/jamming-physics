# IRREPRODUCIBILITY LEDGER — geochronology

**Paper:** Foreign-Material Incorporation as a Cross-Chronometer Accuracy Limit
**paper_id:** `geochronology`  ·  **code:** `chr`
**DOI:** 10.5281/zenodo.20568673
**Standard:** VP-SPEC v1.8 — Constitution C3
**Generated:** 2026-06-15

---

## Purpose (C3)

Constitution clause **C3** requires a ledger enumerating every body claim graded
`[O]` (*open / not independently reproducible from the supplied artifacts*),
together with the reason each cannot be reconstructed deterministically from the
canonical HTML and the reproduction bundle.

## Epistemic-token census

The grade vocabulary for this paper (`grade_vocab_geochronology`) is `{F, I, A}`,
defined operationally in §12 (attribution-severity scale A1–A4):

| Token | Meaning | Occurrences |
|-------|---------------------------------|:----------:|
| `[F]` | directly confirmed | 26 |
| `[I]` | inferential | 13 |
| `[A]` | assumption | 8 |
| `[O]` | **open / irreproducible** | **0** |

Census method: count of `<span class="tag t{F,I,A,O}">` spans across all 14
canonical chapter documents (`docs/geochronology/**/index.html`). Reproducible
via `grep -ro 'class="tag t[FIAO]"' docs/geochronology/`.

## Ledger

**No `[O]`-graded items exist in this paper.**

Every quantitative and qualitative claim in the body carries `[F]`, `[I]`, or
`[A]`, and each is traceable to either (a) a value the reader can recompute from
the reproduction bundle under `repro/geochronology/`, or (b) an explicitly
labelled inference or assumption whose premises are stated inline. There are
therefore no entries to enumerate, and **C3 is satisfied trivially** for the
geochronology paper.

The single locked derived quantity — the diffusion / Fourier number
`N_D = Dτ/L² ≡ Fo` (§4) and its identity with Dodson's closure grouping
`AτD₀/a²` — is graded `[I]` (inferential, dimensional-analysis identity) and is
reproduced in `repro/geochronology/04-shared-physics-closure-exchange-number/`.

---

*If a future revision introduces an `[O]` claim, add a row to a table here with:
section · claim · value/quantity · reason it cannot be regenerated · pointer to
the nearest reproducible surrogate.*
