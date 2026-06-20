# HANDOVER — Aging & Senescence (aging_senescence_vp_site)  ·  v1.4.0-writing

Read `START_HERE.md` → `CHARTER.md` to bootstrap; this file is the live state for the next session.
State passes by files only. Return is a single zip (C0).

## Current state
- **Phase:** writing (unlocked). Research signed off; all gates green.
- **Version:** 1.4.0-writing (adds §14 Conclusion + complete LaTeX/PDF; engine/hash unchanged from v1.3.0). **DOI:** `10.5281/zenodo.20756155` (Zenodo concept DOI, **published** — resolves at https://doi.org/10.5281/zenodo.20756155; wired into HTML + PDF).
- **Determinism:** engine result sha256 `62d5e1eb93db89630c4cd288951540e36ee1c0d8d243945d8b4337188e528c81`, byte-identical across two runs (SEED=19). **Changed by v1.3.0** (new science: RA8+RA9); supersedes `d6506074…`.
- **Site:** complete — hub + **13 chapters** + _meta.json + sitemap + robots + llms.txt + CSS in `docs/`. v1.3.0 inserted §10 (archaic observation) and §11 (telomere keystone) after the cross-species chapter; pathology→§12, ledger→§13; all cross-refs fixed; stale §10/§11 folders removed.
- **Citation PDF:** `pdf/aging_senescence_vp_site.pdf` — one whitepaper built from the canonical HTML, A4, embedded DejaVu fonts. Rebuilt for v1.3.0 with the real DOI on page 1 and 13 chapters. Generator `tools/build_pdf.py`.
- **New in v1.3.0 — telomere + archaic (OBSERVATION ONLY):**
  - `repro/_engine/archaic_discriminant.py` (RA8): re-derives γ bit-for-bit from `inherited/archaic_promoters.cache.json` (sha256 `bb22cbf5…`; 25/25 sequences match the atlas). Reports per-individual γ, γ spread (every per-gene range < 0.0016), substitution counts (archaic load TP53 8 / CDKN2A 6 / FOXO3 6 / **TERT 13**), and TERT cancer-hotspot invariance. The meaning of the co-occurrences is held [O] by constitution.
  - `repro/_engine/telomere_keystone.py` (RA9): telomere repeat γ = **1.3298** (strand-symmetric, lowest of any aging sequence, length-independent); synthesis "telomere is the keystone of aging **dynamics, not γ**" — the lever is off the promoter-γ axis (reservoir length + attrition). γ-invariance [V]; reservoir law [F]; synthesis [O]; rates [L].
  - `repro/_engine/fetch_gamma_archaic.py`: documented provenance path (Ensembl GRCh37 + Max Planck EVA VCFs, GRCh37-aligned).
- **Carried forward (v1.2.0 confound audit):** `repro/_verify/xspecies_robustness_audit.py` (artifact `c771cf7e…`) + `reports/XSPECIES_ROBUSTNESS_AUDIT.md`. The §9 null is audited robust (GC, body-mass, phylogenetic, multivariate); TERT is the residual lead [O] — the lead that RA9 now follows.

## What was accomplished
- Masters measured + vendored (TP53/CDKN2A/FOXO3/TERT γ); `_to_measure` empty.
- RA1–RA6 implemented as real R19 sims; RA7 cross-species discriminant added (the user's axis).
- Cross-species finding (the headline, docs/09): **human aging genes are NOT special** (|z|<1 on every
  gene), **TP53 nearly flat** across 4–211 yr (CV 3.5%), **no discontinuous γ switch**; the longevity
  switch is **off the γ axis — TP53 copy number** (elephant ~20 copies at unchanged per-copy γ, [L]).
- Pathology derived (sarcopenia/frailty/cancer) from one law g_eff = γ(1−d).
- Canonical site built deterministically (numbers from the engine, C1); governance four-doc SSOT written;
  ledger updated; VERSION bumped.
- **(v1.1.0)** Citation-layer PDF built from the canonical HTML (`tools/build_pdf.py` → `pdf/`); invariant.
- **(v1.2.0)** Unbiased confound audit of §9: GC proxy (γ↔GC 0.96–1.00); the weak shared 4-gene lean (raw
  combined p≈0.054, a test the per-gene analysis never ran) is fully confound-attributable — body-mass p=0.16,
  phylogenetic independent contrasts p=0.55, multivariate LOOCV label-perm p=0.115, unstable to leave-one-out.
  Null re-graded **[V] robust**; TERT residual lean **[O]**; scope sharpened to the promoter-γ(=GC) axis.
  Engine science untouched.
- **(v1.3.0)** Telomere deep-dive + OBSERVATION-ONLY archaic comparison. Real archaic genomes (Altai, Vindija,
  Chagyrskaya, Denisova + Ust'-Ishim, Loschbour) reconstructed from Max Planck EVA VCFs (GRCh37-aligned) and
  measured with the identical γ pipeline; committed cache reproduces offline (25/25). RA8 finds the senescence
  gate identical in dated modern humans and TERT carrying the most archaic substitutions with invariant cancer
  hotspots; RA9 finds the telomere-repeat γ a near-exact universal constant (1.3298, lowest of all aging
  sequences) and locates the telomere as the keystone of aging **dynamics, not γ**. Two chapters added (§10/§11),
  tail renumbered (§12/§13); Zenodo concept DOI minted and wired throughout. New result hash `62d5e1eb…`.

## How to verify quickly
```
python repro/run_all.py            # RA1–RA7 all PASS, gates all_green
python repro/_verify/xspecies_robustness_audit.py   # §9 confound audit; artifact sha256 c771cf7e…
python tools/build_docs.py         # rebuilds docs/ (idempotent; numbers from engine + audit)
python tools/build_pdf.py          # rebuilds pdf/ from docs/ (invariant; byte-identical)
```

## Next session candidates (publication phase)
1. **DOI + Zenodo — DONE.** Concept DOI `10.5281/zenodo.20756155` is minted and wired into BOTH
   `tools/render_site.py` and `tools/build_pdf.py` (the `DOI_TBD` constant now holds the real DOI; it
   renders as a resolving link in the HTML and on PDF page 1). Remaining: add the
   `registry/cross_volume_doi` entry in the parent framework when convenient, and upload the v1.3.0 zip as
   a new Zenodo version under the concept DOI.
2. **GitHub repro**: push `repro/aging/<slug>/` folders so the claim-strip GitHub links resolve 1:1
   (Phase 7 gate); add a one-line README per section. Note the slugs now run to §13.
3. **PDF — built and DOI-stamped (v1.3.0).** Rebuild with `python tools/build_pdf.py` after any
   canonical-HTML change.
4. **Sibling seams**: when the immune package lands, wire the immunosenescence seam (RA5) and the oncology
   kernel's consumption of the aging risk-multiplier (this package is SSOT for that seam).
5. **Widen the archaic / cross-species panels (move [O] leads):** the telomere keystone (RA9) and the
   residual TERT lean (RA7) are the open leads. A larger species panel or more archaic individuals (and
   direct telomere-length / attrition-rate data) would test them — they would remain off-γ-axis levers
   (reservoir dynamics), not promoter-γ switches. The archaic comparison stays OBSERVATION ONLY.

## Cautions
- Do not re-derive `inherited/vp_substrate.py` (vendored). Keep SEED=19 and emit rounding (8 dp, sort_keys)
  when extending any module, or determinism breaks.
- The DOI is **minted** (`10.5281/zenodo.20756155`); it lives as the `DOI_TBD` constant in BOTH
  `tools/render_site.py` and `tools/build_pdf.py`. If it ever changes, update both and rebuild site + PDF.
- **Archaic comparison is OBSERVATION ONLY (constitution).** Report measured present-states of the
  cross-sectional set only; never phrase a shared genotype as descent, lineage, selection, or any
  process/change over time — state the measured co-occurrence and nothing beyond it. The avoid-list is
  enforced in §10/§11, the engine docstrings, and the data-file charter; keep it that way when extending.
- Do not re-fetch the archaic genomes to "improve" the cache without re-validating: `archaic_promoters.cache.json`
  is the canonical offline source (Chagyrskaya is TERT-only by design; coverage 84–93% with reference-fallback;
  γ is in the GRCh37 frame, ~0.003 off the NCBI frame — all logged in the ledger).
- The PDF is downstream of `docs/`: after any change that rebuilds the canonical HTML, re-run
  `python tools/build_pdf.py` so the citation layer stays in lock-step (it reads the HTML, never the
  engine directly). `build_pdf.py` honours the writing lock and needs the site built first.
- Keep the body English (C0); session notes Korean.
- Every new [O] needs a stated obstacle in `IRREPRODUCIBILITY_LEDGER.md`, or the gate FAILs.
