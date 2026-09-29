# Sensory volumes — light review synthesis (2026-09-29)

Scope: four volumes (sensory_organ, eye, ear, nose). Each got two reviewers:
- R1: claims against data;
- R2: code, inheritance, and whether the reproduction runs.

Detailed reports sit next to this file.

## What holds across all four
- **Reproduction is exact.** Every script the reviewers ran printed the numbers its page states. The ear numbers come from one source with zero drift. The eye gate re-proves 253 facts with zero drift.
- **Magnitude firewall is clean.** No volume gives a dose, concentration or clinical magnitude.
- **Links and scripts pass.** `tools/check_integrity.py` reports no broken links and no new missing scripts.
- **Wave module and γ values.** nose uses no wave module, as it declares. Every inherited γ recomputes bit-for-bit.

## Shared problems (same pattern in 3–4 volumes)
1. **Developmental order graded [F] or [V] from γ.**
   - Pages still say "order = argsort(spinodal(γ))", and in eye and nose also "size ∝ dwell γ^1.5".
   - This affects the sensory_organ hub, §1 and §2; ear §1; eye hub, E1 and E11; and nose §3 plus its INHERITANCE_LEDGER.
   - AGENTS.md and the dna volume say order comes from regulatory-cascade depth, and that building (order, size, timing) is [O].
   - Two orderings also conflict with embryology: sensory_organ puts the cochlea before the eye, and nose puts LHX2 last.
2. **[V] used for self-consistency, not data.** These checks come out identical by algebra or by construction:
   - ear: the Greenwood ratio equals 1 by algebra, and its inverse round-trips are the function followed by its inverse;
   - eye: the two Snell calculations are algebraically identical;
   - eye: the 633/532 closure holds by construction;
   - nose: the CNGB1 match reuses the same promoter window and pipeline;
   - nose: the anosmia 7/7 outcome follows from how the inputs are set.

   AGENTS.md defines [V] as a test built to falsify the claim against external data.
3. **Headline numbers that are artefacts of numerical choices.**
   | Volume | Claim | Artefact |
   |---|---|---|
   | sensory_organ | Hill "3.1–3.3 ≈ 3" | It is the maximum slope on a 41-point grid. The slope diverges at the fold: 2.39 / 3.32 / 4.54 / 6.07 for 21 / 41 / 81 / 161 points. Verified independently. |
   | sensory_organ | Gain 464 | Equals the probe force F^(−2/3). |
   | sensory_organ | Disease rate ratios | Depend on the noise scale D. |
   | nose | "≈229× steeper" | Depends on the step size (229 / 48 / 24). |
   | nose | "4 patterns" | Depends on the sweep points; a dense sweep gives N + 1 = 8. |
   | eye | Red–green is the most fragile axis [F] | Flips when a cone peak moves by 1 nm; holds only 39 % of the time under ±2 nm jitter. |
4. **Cube root versus measurement.**
   - The ear's exponent 1/3 is an integrator reproducing its own analytic answer. It sits at or above the top of the measured basilar-membrane compression range.
   - The ear's "uniform compression [F]" contradicts the weaker compression measured at the apex.
   - Prior Hopf literature (Eguíluz 2000, Camalet 2000) is not cited.
   - The eye's "Weber" label is wrong: the derived response is a Stevens-type cube-root law.
   - In the eye, the measured rod Hill coefficient of about 3 belongs to CNG channel gating, not to the cubic.
5. **Volume gates broken after the move to `docs/`.**
   - In ear, eye and nose, `verify_seed.py` and `gate_volume.py` still look for `repro/<v>/docs/`, and eye and nose also look for `site.css`, `sitemap.xml` and similar files.
   - Pointed at the real pages, the ear and nose checks pass. The eye's zero-drift check also passes, but the eye gate still fails on its missing `sitemap.xml`, `robots.txt` and `llms.txt`.
6. **Declarations drift.**
   - `_decl.json` grade counts are 0 or do not match the chapters.
   - Undeclared seams: ear → sensory_organ §7 (Hopf); nose → neuro, immune and eye.
   - The ear header badge shows the dna DOI instead of the ear DOI.
   - eye pages call AIPL1, RPGR and PDE6B γ values "byte-identical to atlas", but those genes are not in the dna atlas.

## Recommended actions
- **Fix now (safe, factual; no change to any result):**
  - ear DOI badge;
  - point the volume gate paths to `docs/<v>/`;
  - relabel the eye's "Weber" as a power law;
  - soften the nose "bijection" wording;
  - add the ear Hopf citation;
  - add the undeclared seams to `_decl.json`.
- **Grade corrections that follow AGENTS.md rules:**
  - developmental-order and size claims → [O], with a banner pointing to dna §RB;
  - self-consistency checks → relabel from [V] to "identity / consistency";
  - grid-, step- or probe-dependent headlines → remove the number or show it with its dependence.
- **Needs author:** whether the eye red–green fragility claim should be kept as an [O] prediction with the jitter result attached, and how to present the cube root now that 1/3 sits at the edge of the measured 0.2–0.33 range.
