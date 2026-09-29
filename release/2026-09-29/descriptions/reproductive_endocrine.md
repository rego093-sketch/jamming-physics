## Summary
This volume reads the reproductive and gonadal-endocrine organs (germline, testis, ovary, tract) and their rhythms (the HPG axis, the menstrual cycle, spermatogenesis) on the R19 switch and a FitzHugh–Nagumo oscillator. The switch thresholds are read from measured master-gene promoter γ. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: four reproductive organs read from measured γ. The headline was corrected in this version. The former "four organs emerge in measured-γ order" is now "four reproductive organs read from measured master-gene γ (thresholds; building order is open [O])". The claims ledger records it as an **interpretation**: the ranking conflicts with observation (WT1, required for gonad formation, is ranked last), and the relative rank of testis and ovary has no observable counterpart. The embryo body-plan order computed from γ without tuning is recorded as an **independent prediction** with a weak, coarse correlation (Spearman ρ 0.55 on 14 genes and 3 stages). It is contradicted gene by gene, and the dna γ-order test returned a null. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its dependence on inputs, grid or step stated), a consistency check or an interpretation. The former [F]/[V] grades are relabelled in place, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- Headline (manifest, hub): "four organs emerge in measured-γ order" → "four reproductive organs read from measured master-gene γ (thresholds; building order is open [O])".
- §2 organ order germline → testis → ovary → tract, graded [V]: now code output (the ranking) plus interpretation, with building [O] per dna §RB. WT1, ranked last, is required for the gonad to form at all (Kreidberg et al. 1993). Testis and ovary never develop in the same individual, so their relative rank has no observable counterpart.
- §12 embryo body-plan order, "the order the framework predicts" [V]: ρ = 0.55 on 14 genes with 3 stage ranks. It conflicts gene by gene: POU5F1 ranks 10th of 17, and TBXT (gastrulation; Wilkinson et al. 1990) ranks 16th. The dna §AX-A γ-order test returned a null. The chapter is relabelled with the observation and the null.
- §6 spermatogenic vs menstrual "one oscillator at two speeds": τ_s is set from the observed 16 : 28 d ratio (600 × 16/28 → 340), so the period ratio 656.5 / 1133.7 ≈ 0.58 restates that input. It is relabelled consistency.
- §8 breast-cancer RR plateau 5.29 (model): at the drive cap the barrier is 0, so RR = e^{(γ²/4)/D} = e^{0.25/0.15}, set by the noise scale D and independent of exposure years. The docstring's claim that the WHI anchor "lands in the 5–10 year range" is not reproduced by the code (model 2.07 at 5 y, 3.63 at 10 y; WHI 2002 cited as the observation). The input dependence and the mismatch are stated on the page.
- §9 BAT "13.6×" temporal-pattern selectivity (model) depends on the cycle period (~27× / 13.6× / 6.7× at period 4 / 8 / 16) and is nearly flat in κ. Only the direction is claimed, and therapy is recorded as direction / class only.
- The hub's five headline paragraphs (organ order, two-speed oscillator, breast RR, BAT, embryo) now each carry their label, input dependence and observation.

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. The legend now reads "Labels (reading rule 2026-09-29): …". On all pages outside the existing lt-note asides: [V] → code output, [F] → consistency, retrodiction badges → "code output · retrodiction (interpretation)", "sim-verified" → "simulated". Manifest grade counts forced 4 / verified 29 → 0 / 0; open 3 is unchanged.
- Reading-versus-building notes were added to §2 and the hub. The concepts `dev_order` and `emergence_engine` were corrected corpus-wide in the same change.
- Noted, not changed: the HPG, menstrual and spermatogenic oscillators and the cancer kernel run at γ = 1.0. The measured organ γ enter only the ranking.

**Reproduction package changes**
- No code or data change under `repro/reproductive_endocrine/`. The whitepaper `repro/reproductive_endocrine/paper/reproductive_endocrine_vp.pdf` and its `.tex` were added in the June snapshot ("Final"). They predate the corrections above.

**Site/metadata**
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The work-in-progress snapshot commits for the organ volumes were included.
- Recurrence guards: integrity checks in the gate, the manifest generator fixed, and `_decl` inheritance aligned.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links (including the `reproductive-endocrine` slug) repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume and added its `_decl.json`.

## Claim status (claims ledger)
Counts: interpretation 3 · independent-prediction 1 · anchor-restatement 2 (6 rows).
- Four organs read from measured γ; organ order germline → testis → ovary → tract — interpretation — conflicts with observation (WT1 ranked last); testis vs ovary rank has no observable counterpart.
- Embryo body-plan order from γ (Spearman ρ 0.5507, p 0.02; 14 genes / 3 stages) — independent prediction — weak ρ on coarse ranks, gene-level conflicts (POU5F1 10th / 17, TBXT 16th); the dna §AX-A test returned a null.
- Spermatogenic vs menstrual = one oscillator at two speeds (periods 656.5 / 1133.7 ≈ 0.58) — anchor-restatement — τ_s is set from the observed 16 : 28 d ratio.
- Breast-cancer RR plateau under hormone exposure (5.2942, model) — anchor-restatement — the plateau is set by D; the stated WHI anchor is not reproduced (2.07 at 5 y, 3.63 at 10 y).
- BAT selectivity of the temporal pattern (13.6×, model) — interpretation — ~27 / 13.6 / 6.7× at period 4 / 8 / 16; only the direction is robust.
- HPG / menstrual / spermatogenic dynamics "use measured γ" — interpretation — the dynamics run at γ = 1.0; the measured γ enter only the ranking.

## Open items
- Developmental (building) order, size and timing of the reproductive organs and the embryo body plan: [O] (dna §RB; γ-order schedule null, dna §AX-A).
- The clinical schedule for the temporal-pattern therapy direction: [O]. Every clinical magnitude is withheld under the magnitude firewall.
- Author decision (review): whether the measured organ γ should enter the oscillator and cancer dynamics, which currently run at γ = 1.0; resolving the breast-RR anchor mismatch in the oncology kernel docstring.

## Reproduction
The ZIP contains `docs/reproductive_endocrine/` (the published HTML pages), `repro/reproductive_endocrine/` (engines, embryo / oncology / therapy / dynamics modules, inherited substrate, reports, whitepaper), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/reproductive_endocrine && python3 repro/run_all.py`. It finishes ALL_GREEN, and determinism is 2×SHA-256 identical.
- Focused modules:
  - `repro/reproductive_endocrine/repro/_embryo/embryogenesis.py` (`run_E4`, embryo order);
  - `repro/reproductive_endocrine/repro/_oncology/carcinogen_dose_response.py` (`breast_duration_curve`);
  - `repro/reproductive_endocrine/repro/_therapy/temporal_pattern.py` (`bat_selectivity`);
  - `repro/reproductive_endocrine/repro/_dynamics/spermatogenesis.py`.
- Gates: `repro/reproductive_endocrine/repro/_verify/gates.py`.
- SEED = 19. No network is needed for the checks. The optional `fetch_*_gamma.py` scripts under `_embryo/`, `_germline/` and `_sexratio/` re-fetch promoter sequence from NCBI.

## Citation and links
- Site: https://jamming-physics.org/reproductive_endocrine/
- Concept DOI: 10.5281/zenodo.20754657
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
