# aging_senescence — light review (2026-09-29)

## Summary
R2 ran these from `repro/aging_senescence/repro/` with `python3 -B`:
- `run_all.py`: the battery completed, but the gates step hit the 120 s limit;
- RA1–RA6 in `_engine/aging_dynamics.py`;
- `xspecies_discriminant.discriminant()`.

The printed numbers match the pages:
- RA1: flip 0.790364;
- RA2: 0.391;
- RA3: 89 / 78 steps;
- RA5: 52.32×;
- RA6: 0.8889;
- TP53: CV 3.52 %, human z 0.088, perm p 0.114.

The magnitude firewall is clean.

## Findings
1. **Headline numbers are set by model inputs** (reruns in this review). Severity: high.
   - **52.3×** comes from the Armitage–Doll stage count, `stages = 6`. With 5 / 6 / 7 stages it is 25.0 / 52.3 / 107.9×. RA5 contains no barrier or Kramers term, although §7 says "shrinking barrier raises the Kramers hazard".
   - **135× (§12)** equals exp(Δb/T) with T = 0.1. With T = 0.05 / 0.1 / 0.2 it is about 18,000 / 135 / 12×.
   - **0.889 (§8)** is PCA-1 of synthetic curves of one functional form. It is 0.986 / 0.889 / 0.682 at noise 0.05 / 0.15 / 0.30.
   - **0.391 (§4)** is 0.224 / 0.391 / 0.625 at base hazard 0.006 / 0.012 / 0.024.
2. **[V] on results that hold by construction.** Severity: medium.
   - §5: the depletion steps equal γ^1.5 / 0.02.
   - §6: the hallmark table is hand-entered, so "no orphans" is guaranteed.
   - §11: the telomere-repeat γ follows from the table (7.98 / 6), and strand symmetry is a property of the table.
3. **Span misstatement.** Severity: medium.
   - The hub, §9 and §14 say "4–211 yr" and "fifty-fold".
   - The bowhead has no γ, so the data span is 3.8–122.5 yr, about 32-fold.
4. **Order from γ.** Severity: medium.
   - §2 gives an "emergence order by ascending γ", and §14 says "γ fixes what and in what order".
   - This conflicts with AGENTS.md and dna §RB.
5. **Interpretation stated as fact.** Severity: medium.
   - §9 calls TP53 copy number the "longevity switch". The cited observation (Abegglen 2015; Sulak 2016) concerns cancer resistance.
   - §4 calls senescence irreversible, but it can be reversed in some cells by inactivating p53 or p16 (Beauséjour 2003).
6. **Hallmarks coverage.** Severity: low.
   - The map uses a 10-item list. The 2023 update lists 12, and disabled macroautophagy and dysbiosis are unmapped.
7. **§10 present-day TP53 γ differs from the §2 atlas value** (1.4333 vs 1.4298), and the page gives no reason. Severity: low.
8. **Cross-species detail.** Severity: info.
   - TERT has `clean_threshold_switch = true` in the code. This is consistent with the page's "three of four overlap".
   - The human z-scores include the human value.

## What I changed (docs/aging_senescence only)
- **Hub:** added a Reading-rule note after the `<h1>`. It covers the labels, the input-dependent headlines and the 3.8–122.5 yr span.
- **§1–§14:** each chapter gets one lt-note with its input dependence, consistency status, order rule or clarification, plus cited observations:
  - López-Otín 2013 and 2023;
  - Dimri 1995; Krishnamurthy 2004; Beauséjour 2003;
  - Hayflick 1965; Harley 1990;
  - Armitage & Doll 1954; Oh 2023; Fried 2001.
- No numbers changed and nothing deleted.
