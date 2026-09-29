# reproductive_endocrine — light review (2026-09-29)

## Summary
- R2 ran `repro/run_all.py` from a scratch copy with `python3 -B`. It finished, with ALL_GREEN and determinism 2×sha256 identical (f849da7d13d2…).
- R2 then probed three functions one by one:
  - `_embryo/embryogenesis.run_E4`;
  - `_oncology/carcinogen_dose_response.breast_duration_curve`;
  - `_therapy/temporal_pattern.bat_selectivity`.
- Every printed number matches the pages:
  - organ order germline → testis → ovary → tract;
  - periods 132.4 / 656.5 / 1133.7;
  - breast RR 5.2942;
  - BAT 13.6×;
  - stage ρ 0.5507 (p 0.02).
- Magnitude firewall: clean. The therapy pages give direction only, and the clinical schedule is [O]. The RRs are modelled and carry no dose.
- The hub headlines each ended in [V] or [F], and every chapter badge read "[V] sim-verified".

## Findings
1. **Organ order "germline → testis → ovary → tract" graded [V].** Severity: high.
   - Where: the hub and `02-organ-emergence-measured-gamma/`.
   - Testis and ovary never develop in the same individual, so their relative rank has no observable counterpart.
   - WT1, ranked last, is required for the gonad to form at all (Kreidberg et al. 1993).
2. **Embryo body-plan order graded [V] ("the order the framework predicts").** Severity: high.
   - Where: `12-embryogenesis-.../` and the hub.
   - ρ = 0.55 on 14 genes with 3 stage ranks.
   - Gene by gene the order conflicts with observation. POU5F1 (OCT4) ranks 10th of 17, and TBXT (Brachyury; gastrulation, Wilkinson et al. 1990) ranks 16th, tied in γ with NKX2-5.
   - The dna volume's own test of the γ-order schedule returned a null (dna §AX-A).
3. **The spermatogenic/menstrual "one oscillator at two speeds" ratio is an input.** Severity: medium.
   - `spermatogenesis.py` sets τ_s from the observed 16 : 28 d ratio (600 × 16/28 → 340).
   - The period ratio 656.5 / 1133.7 ≈ 0.58 restates that input: consistency.
   - The code comment says "→350", but the code computes 340; the page correctly says 340.
4. **Breast RR plateau 5.29 is set by the noise scale.** Severity: high.
   - At the drive cap the barrier is 0, so RR = e^{(γ²/4)/D} = e^{0.25/0.15} ≈ 5.29. It is independent of exposure years.
   - The docstring says the WHI RR ≈ 1.26 anchor "lands in the 5–10 year range". The code gives RR 2.07 at 5 years and 3.63 at 10.
   - WHI 2002 reported HR 1.26 at a mean follow-up of 5.2 years, so the stated anchor is not reproduced.
5. **BAT "13.6×" depends on the inputs.** Severity: medium.
   - It is about 27× at cycle period 4, 13.6× at 8 and 6.7× at 16. It is nearly flat in κ (13.2–13.8× for κ = 2–4).
   - Only the direction is robust.
6. **The measured γ is mostly not in the dynamics.** Severity: low; noted, not changed.
   - The HPG, menstrual and spermatogenic oscillators and the cancer kernel run at γ = 1.0 ("0.3849 at γ = 1").
   - The organ γ enter only the ranking.

## What I changed (docs/reproductive_endocrine only)
- **Hub.**
  - Added the reading-rule note after `<h1>`.
  - The five headline paragraphs (organ order, two-speed oscillator, breast RR, BAT, embryo) now carry their label, input dependence and observation, with [O] per dna §RB and the §AX-A null.
  - The legend now reads "Labels (reading rule 2026-09-29): …".
- **Chapter pages.**
  - §2: label and observation paragraph; the answer paragraph is relabelled.
  - §6: consistency note on the period ratio.
  - §8: input dependence of 5.29 and the WHI mismatch.
  - §9: dependence of 13.6× on period and κ.
  - §12: label, observation and the §AX-A null.
- **All pages, relabelled outside the existing lt-note asides:**
  - [V] → code output;
  - [F] → consistency;
  - retrodiction badges → "code output · retrodiction (interpretation)";
  - "sim-verified" → "simulated".
- No number or lt-note was removed.
