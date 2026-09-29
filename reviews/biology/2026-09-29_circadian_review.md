# circadian — light review (2026-09-29)

## Summary
R2 ran the RC1–RC6 and TX1 probes one by one from `repro/circadian/repro/_engine/vp_clk_engine.py` with `python3 -B`. `run_all.py` did not finish within 120 s.

Every printed number matches the pages:
- free run: 76 beats, cv 0.003691;
- PRC: +0.185022 / −0.129012; Arnold tongue: [5, 11, 15, 15, 15];
- network: coherence 0.596406 → 0.999925, drift 0.003823 → 0.002956;
- gating: amplitude 0.976237 vs 0.0;
- misalignment: 1.227923 → −1.364039; flattening index: 0 → 2.11085;
- chronotherapy: 2.56 / 1.12 / 0 h and 5.44 → 11.2 h.

The BMAL1 γ = 1.33348 recomputes bit-for-bit from the cached ARNTL promoter (2501 bp, GC 0.443).

The magnitude firewall is clean: there is no melatonin dose, no lux value and no clinical timing window.

## Findings
1. **The measured γ does not enter the dynamics.** Severity: high.
   - Every `Neuron(...)` in the engine uses γ = 1.0, and `coupled_network` uses `np.ones(N)`.
   - The claim "seeded by a measured clock-gene γ" is true only of the node table.
   - The hub, §0 and §1 call γ "a measured input graded [V]".
   - Files: `repro/circadian/repro/_engine/vp_clk_engine.py`, lines 116–295.
2. **§6: "PRC-bounded ~1 h/day" is an input, not derived.** Severity: high.
   - The code sets `max_shift_per_cycle = 1.0`, and the cycles equal the gap divided by 1.
   - The rate is an observation (Aschoff 1975; Waterhouse 2007), but it was not cited.
3. **§8 chronotherapy is arithmetic on entered values.** Severity: medium.
   - The corrected delay is 4 − 24·0.6·strength.
   - The light/melatonin antiphase comes from two hard-coded phases (6 h and 18 h). The page says "reproduced here".
   - The melatonin PRC was not cited.
4. **[V] on results that hold by construction.** Severity: medium.
   - §5: an ablated constant drive gives an amplitude of 0.
   - §6 and §7: the alignment and flattening indices are cosine projections.
   - §7: the code sets `sign_consistent_with_mind = True` directly.
5. **§3: the Arnold-tongue counts saturate at the sweep size.** The last three values are 15 of 15 detunings. Severity: low.
6. **Missing observations.** Severity: low.
   - human period of about 24.2 h (Czeisler 1999);
   - human light PRC (Khalsa 2003);
   - peripheral self-sustained clocks (Yoo 2004);
   - IARC Monograph 124.

## What I changed (docs/circadian only)
- **Hub:** added a Reading-rule note after the `<h1>`. The existing 2026-09-29 emergence [O] note is kept. "a measured input graded [V]" is relabelled "DNA reading".
- **§0 and §1:** the same relabel. §0 also gets a note that the oscillators run at γ = 1.0.
- **§2–§8:** each chapter gets one lt-note with its input dependence or consistency status, plus cited observations.
- No numbers changed and no content deleted.
