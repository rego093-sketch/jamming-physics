# Eye volume: light review (2026-09-29)

Scope: `docs/eye/` (hub + E0–E12), `repro/eye/`, `docs/eye/_decl.json`. Two reviewers: R1 checks claims against data, R2 checks code and inheritance. No page or code was edited.

## Summary

1. **Code matches the pages.** All 5 chapter scripts I ran reproduce their page transcripts byte for byte. The gate re-proves 253 facts with 0 drift, and the magnitude firewall is clean. The problems are grading and physics, not reproduction.
2. **The main physics problem is the colour-as-angle channel.** χ(λ) behaves like a pseudo-random sawtooth: 1 pm of wavelength moves χ by about 0.04°, which is as large as the cone margins. So E9's [F] result "red-green is the most fragile axis" depends on the chosen integer-nm peaks. Several [F]/[V] labels are also given to tautologies or to the model's own outputs rather than to tests against data.
3. **The rebuild commands printed on the hub do not pass as documented.** Both `verify_seed.py` and `gate_volume.py` FAIL, because of a path layout mismatch and 3 missing promised files. Two grades also conflict with AGENTS.md: γ-ordered "emergence order" and γ-set "size" appear as [F], but AGENTS.md makes both BUILD [O].

## R1: claims vs data

| # | Claim (page, quoted) | Finding | Severity |
|---|---|---|---|
| R1-1 | `docs/eye/e9-red-green-dichromacy/index.html`: "the green-red (M–L) margin is the smallest of the three — so red-green is the structurally most fragile axis. This is forced by the measured peaks and the frozen law" [F] | I recomputed χ = asin(λ/(⌈λ/D⌉D)) with the page's D. **S/M/L = 420/530/561 nm** gives M–L = 0.0563° > S–M = 0.0509°, so the ordering flips. 419/531/558 gives M–L = 0.0052°. **424/530** gives S and M the *same* angle (margin 0), i.e. "dichromacy" for normal cones. Under ±2 nm jitter (seed 19, n = 2000), M–L is smallest only 39% of the time. Moving λ by 0.001 nm (560 → 560.001 nm) shifts χ by 0.043°. The page's caveat ("hypersensitive and distributional") admits this, but the headline is still graded [F]. It should be [O] or dropped. | **blocker** (for the E9 headline and its grade) |
| R1-2 | `docs/eye/e0-carrier/index.html` transcript: "violet χ=89.8428° … red χ=89.8428°", printed alongside "colour = the light-propagation angle χ(λ)" | The inherited colour module itself gives violet and red the *same* angle. Page 0 already shows that "colour is geometry" cannot tell the two ends of the spectrum apart. E1's "trichromacy as three angle-bands" [F] is trivial, because almost any three distinct λ give three distinct χ. | should-fix |
| R1-3 | `docs/eye/e2-single-photon-switch/index.html`: "One quantum of drive across h* flips the whole switch; anything less does nothing — single-photon sensitivity, as pure structure" and "this is where 'Hill≈3' comes from: the cubic, NOT a fit" [F] | The model has no photon→h link: the page itself grades that link [O]. So "single-photon" is a label, not a result. Established rod data (Baylor, Lamb & Yau 1979; Rieke & Baylor 1998) show a graded, reversible single-photon current of about 1 pA. Dim-flash responses sum roughly linearly, and the rod intensity-response curve has n ≈ 1, not 3. The Hill ≈ 2–3 that is measured belongs to cGMP gating of the CNG channel, which is a different quantity from the order of the normal form. "Steepness ratio ≈ 231×" depends on the sweep step (the page itself says "formally → ∞"). | should-fix |
| R1-4 | `docs/eye/e10-light-dark-adaptation/index.html`: "the CONTRAST gain → 1/n = 1/3 exactly (a Weber-like law)… Equal fractional steps feel equal" | The derived result s ∝ h^(1/3) is a Stevens power law, not Weber–Fechner. With a fixed response criterion it gives ΔI ∝ I^(2/3), whereas Weber gives ΔI ∝ I. "Equal fractional steps feel equal" is the Fechner (log) reading, which this law does not produce. The cited [L] brightness exponent ~1/3 does match. The label should say "power law, exponent 1/3", not Weber. | should-fix |
| R1-5 | `docs/eye/e3-image-formation/index.html`: "n = c_vac/c_med = √((B/ρ) ratio) … The wavefront/speed derivation and the index form agree to 0" [F][V] | n = 4/3 is the cited Emsley input, which is honest [L], and 60.06 D / 22.2 mm match textbook reduced-eye values. However, "n = √(B/ρ ratio)" is a relabelling with no independent B, ρ measurement. The "agree to 0" test compares two algebraically identical code paths, so it is a tautology, not a [V]. "First-order chromatic split = 0.0e+00 mm" is listed as a key result, but the real eye has about 2 D of longitudinal chromatic aberration across the visible band. The [O] is stated, but the 0 should not appear as a result. | nit |
| R1-6 | `docs/eye/e0-carrier/index.html`: "633/532 closure ratio 1.189831 = 633/532 (forced, not fitted)"; "Two-channel closure m·sinχ·D/λ = 1.000000000000000" [F][V] | Both hold by construction: (λ₁/D)/(λ₂/D) = λ₁/λ₂, and sinχ is *defined* as λ/(mD). They are identities, not evidence. | nit |
| R1-7 | `docs/eye/index.html` Grades box: "[V] verified — deterministic recomputation (2×sha256) of every displayed number, byte-identical across runs, HTML↔code drift 0" | AGENTS.md §5 defines [V] as "passed a test *built to falsify it* against external data". Here the volume-wide [V] means reproducibility, and no [V] item in E2/E3/E5/E7/E10 compares against external measurements. The grades are therefore inflated relative to the corpus rule. | should-fix |
| R1-8 | Magnitude firewall (E4, E9, E11, E12) | No dose, concentration, dioptre prescription, axial length or "%" was found in the condition chapters (grep, and gate reports "no magnitude token"). Corrections are stated as directions only (e.g. E11 "myopia ⇒ reduce power"). | no action |

Also checked, no issue found: E5's ν = c/λ and E = hν values (4.736e14 Hz, 1.959 eV for 632.99 nm) are correct. E6 honestly grades the chromophore window [L] and its origin [O]. E7's single-pole low-pass numbers are correct for the stated recurrence.

## R2: code and inheritance

Scripts run (python3, each finished well under 120 s, exit 0): `repro/eye/research/{E2-single-photon-switch,E3-image-formation,E5-frequency-ladder,E9-red-green-dichromacy,E10-light-dark-adaptation}/run.py`.

| # | Finding | Evidence | Severity |
|---|---|---|---|
| R2-1 | **Numbers match.** Each page's `<pre class="transcript">` equals the live stdout exactly (5/5). Spot values: E2 h* 0.68733, jump +2.2905, 231×. E3 48.5904°, 60.06 D, 22.200 mm. E9 89.7497/89.8006/89.8428, M–L 0.0421. E10 3.014737, 1296.0×, 0.333182. E5 11.3%, 4.736e+14. On a scratch copy with docs laid out as the tool expects, `gate_volume.py` reported 13/13 chapters, 16 runs ×2 byte-identical, 253 facts re-proven, drift 0. | re-run outputs vs page transcripts | no action |
| R2-2 | **The documented rebuild fails in the monorepo.** `repro/eye/tools/_volume_lib.py:28` sets `DOCS = os.path.join(ROOT,"docs","eye")` relative to `repro/eye`. Run from `repro/eye` as the hub says, `verify_seed.py` prints "SEED VERIFY: FAIL" (all docs MISSING) and `gate_volume.py` crashes with `FileNotFoundError …/repro/eye/docs/eye/facts/e0-carrier.json`. The hub says both print PASS. | hub "Reproducibility" block; tool output | should-fix |
| R2-3 | **Promised files are absent even with the correct layout.** Both tools still FAIL on G7 no-omission: `docs/eye/sitemap.xml`, `robots.txt`, `llms.txt` (listed in `_volume_lib.py:240`). They are probably superseded by the site-level aggregates, so the list should be updated. | gate output | should-fix (small) |
| R2-4 | **Hash label is ambiguous.** The pages show "research/E2-single-photon-switch/run.py sha256 5cfa2d60…". That value is the sha256 of the script's *stdout*, not of `run.py`, and the source hash differs. It reads as a source pin. | sha256 of stdout = 5cfa2d60…; sha256 of run.py ≠ | nit |
| R2-5 | **Inheritance is declared.** `_decl.json` lists `physics:wave, dna, neuro`. `repro/eye/INHERITANCE_LEDGER.md` pins every inherited file, and all 11 sha256 prefixes match the files on disk. The `organ_gamma.json` `_seam_note`/`_reconcile_obligation` states that the DNA atlas is authoritative. PAX6 γ = 1.511044 is byte-equal to `repro/dna`. | ledger vs `sha256sum` | no action |
| R2-6 | **Some atlas nodes are measured locally.** The ledger v0.6.0 says AIPL1, RPGR and PDE6B were fetched by `tools/fetch_promoter_gamma.py` and "removed from the atlas `_to_measure` queue". OPN1LW, GNAT1 and AIPL1 do not appear anywhere under `repro/dna`. The eye volume is therefore the de-facto source for these node γ values, while pages say "byte-identical to atlas" (e.g. E2 [L]). The declared seam softens this, but the values should be upstreamed to the DNA atlas or the wording should say "eye-local measurement, pending atlas". | `repro/eye/INHERITANCE_LEDGER.md` §re-freeze; grep of repro/dna | should-fix |
| R2-7 | **Grades conflict with AGENTS.md reading vs building.** The hub grades "the emergence order argsort(spinodal(γ))" as [F]. E1 says the "cone/rod lineage emerges … ordered by spinodal(γ)". E11 says "organ size = dwell ∝ γ^1.5 … the growth axis has a forced direction". AGENTS.md §1 says developmental order comes "from regulatory-cascade depth, not γ", and size/order/timing are BUILD [O]. (E2 does honestly mark cascade order vs biochemistry as [O].) | `docs/eye/index.html` Grades; `e1-…`, `e11-accommodation-refraction/index.html` | should-fix |
| R2-8 | **Declaration is weak.** `_decl.json` has `grades` all 0 (forced/verified/open = 0) although the pages carry many graded claims. It also declares 4 `adds`, while the contract is "exactly one new module". | `docs/eye/_decl.json` | nit |
| R2-9 | **Integrity is clean.** `python3 tools/check_integrity.py`: links PASS (0 broken), scripts PASS (0 new gaps), aggregates PASS. | tool output | no action |

## Action table

| Bucket | Item | File | Severity |
|---|---|---|---|
| **Fix now (small, safe)** | Relabel transcript hash as "stdout sha256" | `repro/eye/tools/build_volume.py` → regenerated pages | nit (R2-4) |
| Fix now | Drop `sitemap.xml/robots.txt/llms.txt` from the promised list, or generate them | `repro/eye/tools/_volume_lib.py:240` | should-fix (R2-3) |
| Fix now | Make `DOCS` resolve to the repo `docs/eye` (or document the layout) so the hub's PASS claims hold | `repro/eye/tools/_volume_lib.py:28`, hub Reproducibility | should-fix (R2-2) |
| Fix now | Rename "Weber-like" to "power law, exponent 1/3 (Stevens-like)"; drop "equal fractional steps feel equal" | `docs/eye/e10-light-dark-adaptation/` via build | should-fix (R1-4) |
| Fix now | Fill `_decl.json` grade counts | `docs/eye/_decl.json` (regenerate) | nit (R2-8) |
| **Needs author** | Downgrade E9 "M–L smallest ⇒ red-green most fragile" from [F] to [O] (fails under ±1 nm) or reformulate | `docs/eye/e9-red-green-dichromacy/`, `repro/eye/research/E9-*` | **blocker** (R1-1) |
| Needs author | Decide whether colour-as-angle survives violet χ = red χ; at minimum grade E1 trichromacy-as-angle as [O]/hypothesis | `e0-carrier`, `e1-angle-to-cone` | should-fix (R1-2) |
| Needs author | Redefine volume-wide [V] per AGENTS.md; re-grade tautologies (Snell two paths, 633/532 closure, m·sinχ·D/λ) and model-internal checks | `docs/eye/index.html`, E0, E2, E3, E5, E7, E10 | should-fix (R1-5, R1-6, R1-7) |
| Needs author | E2: remove "single-photon sensitivity as pure structure" and "Hill≈3 comes from the cubic" [F], or state the conflict with measured graded, reversible rod responses (n ≈ 1) | `docs/eye/e2-single-photon-switch/` | should-fix (R1-3) |
| Needs author | Emergence order / size by γ graded [F] vs AGENTS.md BUILD [O] | hub, E1, E11 | should-fix (R2-7) |
| Needs author | Upstream AIPL1/RPGR/PDE6B/OPN1*/GNAT1 γ into the DNA atlas, or label them eye-local | `repro/eye/inherited/organ_gamma.json`, ledger | should-fix (R2-6) |
| Needs author | Don't list "chromatic split 0.0 mm" as a key result | `e3-image-formation` | nit (R1-5) |
| **No action** | Transcripts = live stdout; gate drift 0 | R2-1 | — |
| No action | Magnitude firewall clean in E4/E9/E11/E12 | R1-8 | — |
| No action | Inherited file hashes match ledger; PAX6 γ equals DNA atlas | R2-5 | — |
| No action | Links/scripts/aggregates integrity PASS | R2-9 | — |
