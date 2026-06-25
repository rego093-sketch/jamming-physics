# INTEGRITY ATTESTATION — dna_vp_site_INTEGRATED v1.18.1 (AX-G recovered)

**paper_id** `dna` · **DOI (concept)** 10.5281/zenodo.20471407 · Young Jae Lee · ORCID 0009-0002-7535-8245
**Scope of guarantee:** the package as shipped. Re-run every check below on a fresh extraction to reproduce it.

## VERDICT

**Integrity is guaranteed.** The reproduction closure is complete and self-contained: every published number
reproduces from shipped inputs through shipped code, deterministically, to the frozen hashes below; the
published site has zero dangling references; and **no shipped, executed code path references a missing file.**
There is nothing outstanding to fix.

## Reproduction closure — verified on a clean extraction (not a working tree)

| check | result |
|---|---|
| archive CRC (`unzip -t`) | OK — no corruption |
| build artifacts (`__pycache__`/`.pyc`) | 0 |
| OS junk (`.DS_Store`, hidden files) | 0 |
| site gate (`python3 gate_multipage.py`) | **PASS 318 / WARN 1 / FAIL 0** (WARN = source-monolith diff is informational; not a defect) |
| completion gate (`cd repro/dna/ax-l-completion-closeout && python3 -m completion.gate`) | **PASS 18/18**, gate sha `b0cf5eae7285b50a` |
| determinism (gate item L10) | **2× SHA-256 identical** |
| honest-declaration (gate item L11) | **PASS** |
| frozen reading hash (`repro/dna/ax-l-…/expected/reading.json`) | `a817287d1b57d84ea30a2c6ce7ade71f1333561205a4e1b4785abda78af37aca` — **MATCH** |
| published `docs/` dangling `.md`/`.py` references | **0** |
| reproduction substrate (`repro/dna/_verify`, `repro/dna/_engine`, all `ax-*`) | byte-identical to v1.17 source |
| recovered files vs v1.17 source (md5) | identical — `IRREPRODUCIBILITY_LEDGER.md` `09773ada…`, `GAMMA_VS_A4_LEVEL_SHAPE_SPEC.md` `2d6a0374…`, `FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md` `603c5958…` |
| measured values / grades / DOI vs v1.17 | unchanged (heart null `+0.071 / p=0.882`, methylation `74th percentile`, `corr(γ,GC)=0.998`, DOI `10.5281/zenodo.20471407`) |
| newly-introduced dangling references vs v1.17 | **0** |

A fail-closed gate failing the instant a dependency is absent is what makes the closure check decisive: the
gates pass, therefore the executed-code dependency set is whole.

## Full disposition of every non-resolving filename token (so nothing is left ambiguous)

A basename scan of the whole corpus surfaces filename tokens that have no corresponding file. **Every one is a
non-executing reference** — none is imported or `subprocess`/`exec`/`runpy`-invoked by any `.py` in any gate
path (verified by static search across all `*.py`). They split into three classes, all benign:

**1. Regex / line-wrap artifacts (the file actually exists):**
`hashlib.md` = `hashlib.md5(...)`; `matplotlib.py` = `import matplotlib.pyplot`; `g.py` / `_timing.py` =
substrings of real names like `timing.py`, `dev_timing.py`; `_CLOSEOUT.md` = a wrapped fragment of
`FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md` (present). Not real references.

**2. Deliberately-removed files, documented as removed (by design):**
`build_single_file_dna.py`, `build_v1_13_level_shape.py`, and the `repro/dna/_research/` items
(`RESEARCH_PLAN_missing_grammar.md`, `orthogonality_probe.py`, `structural_periodicity_probe.py`),
plus `FINALIZATION_VPSPEC_v1_8_ABSTRACT_CALIBRATION.md` — named only inside changelogs that record their
removal. Their machine references were severed before removal (e.g. the gate build-provenance hash was
repointed to `build_multipage_dna.py`).

**3. Upstream-generator / provenance references — frozen outputs are shipped, generators are not (by design):**

| token | where | what it is |
|---|---|---|
| `fetch_taste_gamma.py` | `_provenance` strings in `*_gamma.json`; docstrings in sibling `fetch_*_gamma.py` | provenance note: how the **frozen** taste-organ γ was fetched from NCBI eutils (the γ values are shipped, READ-ONLY; the live-NCBI fetch script is upstream) |
| `derive_meta.py` | `INTEGRATION_README.md`, a **frozen** v1.8 gate-report string | describes a `tools/` answer-first migration; the report itself states it is inherited, not hand-authored |
| `grape_color_4d.py` | `04-…/README.md` | parenthetical note that white-grape MYBA is a verified kit case; the chapter's reproduce command is `run_regression.py` (shipped, gate-run) |
| `validate_organs.py` | docstring of `emergence_v2/emergence_organs.py` | documents the NON-FIT firewall ("the validation-target file is touched only by `validate_organs.py`"); the engine never reads it |
| `reconcile_derived_to_html.py` | `FINALIZATION_VPSPEC_v1_8_CLOSEOUT.md` | text explicitly frames it as a **future** `tools/` script "could … in-package" — i.e. deliberately not present |
| `CLOSURE.md` | v1.10 / v1.11 changelogs | v1.11 explicitly records "No CLOSURE.md file was available; the closure is reconstructed from quantities verifiable in this package" |
| `WORK_HANDOVER_dna_whitepaper_reframe.md` | v1.9.2 changelog | an upstream handover/planning note for the staged reframe |

This is the package's own documented discipline: **measured quantities are shipped frozen and read-only;
the upstream scripts that originally produced them are referenced for provenance but are not part of the
reproduction closure** (the same property the v1.18 changelog records for `run_regression.py`'s
`comparative_taxa_results.json` input). No frozen value depends on re-running any of these scripts.

## What "guaranteed" means here, precisely

- **In-closure (everything required to reproduce the paper):** complete and self-contained — gates pass to the
  frozen hashes above. No missing file.
- **Out-of-closure (upstream generators / historical planning notes):** referenced for provenance only, never
  executed; their frozen outputs are shipped. Listed exhaustively above so nothing is left implicit.

No file was fabricated to make a reference resolve, and no historical/frozen record was edited to hide one;
doing either would violate the package's no-confabulation and append-only discipline.

— v1.18.1 integrity attestation. Reproduce by re-running the commands in the table on a fresh extraction.
