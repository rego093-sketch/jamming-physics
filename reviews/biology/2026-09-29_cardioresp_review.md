# cardioresp — light two-reviewer review (2026-09-29)

Scope: `docs/cardioresp/` (hub + §1–§12), `repro/cardioresp/`.
- R1 checked claims against data.
- R2 ran `python3 -B repro/run_all.py` in `repro/cardioresp/` and swept the recovery-time constant through the engine.

## Summary

- **Reproduction is exact.** Every number on the pages is reprinted by the engine with drift 0 (sha `25900a90079a…`): 16.86 /min, the RSA peak 0.2784 Hz, the Cheyne–Stokes slope 1.992, the RR table 1.00→18.32 and the counts 115/28 beats.
- **The main problem is what the numbers rest on.** The oscillator ignores γ. The heart and lung "difference" is a pair of chosen constants. Several [V] labels mark checks that hold by construction.
- **Magnitude firewall is clean.** Pack-years is an epidemiological exposure, not a dose.

## Findings

| # | Severity | Where | Finding | Evidence |
|---|---|---|---|---|
| 1 | high | §1, §2, §10, hub | "γ sets each organ's oscillator" is not what the code does. | `repro/cardioresp/repro/_engine/vp_car_engine.py` `_fhn_rate_arb` builds `Neuron(gamma=1.0, …)` for both organs. The measured γ values (1.513 / 1.509) only feed the spinodal and size readout. Heart vs lung comes from `tau_s` 18 / 95, which are hard-coded in `ORGAN_ROWS`. |
| 2 | high | §3 | The breathing rate 16.86 /min and the ratio 0.240 are called "structural, not fitted" [V]. They follow from the chosen τs = 95. | Review sweep (same κ anchor): τs 60 / 80 / 110 / 130 → 25.47 / 19.70 / 14.76 / 12.65 /min. |
| 3 | high | §1, §10 | Developmental order lung → heart is graded [V] "pure γ readout". | The γ difference is 0.004. Embryology runs the other way: the heart beats from about day 22 (CS10), and the lung bud appears at about day 28 (CS12). Superseded per dna §RB / §AX-A. |
| 4 | medium | §4 | Onset at LG/LGc = 1 [V] holds by construction, because it is normalised to its own critical gain. The ≈32 s period depends on the example delay. | page text + engine |
| 5 | medium | §5 | RSA "lock" [V] is by construction: a drive modulated at f_resp gives a line at f_resp. | The decoupled peak of 0.303 Hz also lies inside the 0.15–0.40 band. |
| 6 | medium | §6 | "Forced number" T ≈ 2τ is a property of delayed negative feedback (consistency), not a biological law. | Single-delay ratios are 2.09–2.22. Model periods of 17.7–41.7 s are shorter than the roughly one-minute cycles observed in heart failure (Hall et al. 1996). |
| 7 | medium | §7 | "Verified content" (sign, linearity, regulation) is guaranteed by the input gain and latency. | Table slope −1.0 = input |
| 8 | medium | §8 | 18.3× at 100 PY is set by declared `scale = barrier/3` (RR ceiling e³ ≈ 20) and the PY→spinodal mapping. RR(0)=1 and slope √γ are identities. | `repro/_oncology/carcinogen_dose_response.py` lines 193–194 |
| 9 | low | §11 | The page shows [V], but `run_all.py` prints "[V?]" for D2, D3, D5 and D6. Fever co-scaling is by construction (one κ). | run_all output |
| 10 | low | §12 | The page states "OVERALL: PASS (11/11)". The current run ends `OVERALL: FAIL (9/11)`. | R6 has 0 pinned files, R10 fails the DOI check, and R7 scans 0 pages after the move to `docs/`. |
| 11 | low | §2–§7 | Observations were missing next to the model claims: measured HR/RR ranges, the pulse–respiration quotient, CSR cycle length, BRS range and RSA physiology. | — |

## What I changed (docs/cardioresp only; no numbers changed, no notes removed)

- **Hub**
  - Added a reading-rule lt-note after the `<h1>`.
  - Relabelled the TOC grades by section.
  - Put the legend in entity form, with the note that [F]/[V] are no longer used here.
  - Added the size/order [O] link to dna §RB.
- **All chapters**
  - Mapped [F] → [consistency].
  - Mapped [V] → [code output], [consistency] or [interpretation], chosen per page. γ cards became [code output] (a measured input from the dna reading), and FHN cards became [interpretation].
- **Chapter additions**
  - §1 and §10: order marked [interpretation]/[O] with the embryology observation, plus a code note that the oscillator uses γ = 1.0.
  - §2: code note, plus SA-node and preBötC observations.
  - §3: τs sweep (input dependence), plus HR/RR ranges and the pulse–respiration quotient.
  - §4: Khoo 1982 and Younes 2001.
  - §5: decoupled-peak note and Hirsch & Bishop 1981.
  - §6: consistency wording and Hall 1996.
  - §7: consistency wording and the BRS range (La Rovere 2008).
  - §8: declared-scale dependence and lung-cancer RR observations.
  - §9: reading-rule paragraph under the legend.
  - §11: fever observation and the [V?] note.
  - §12: note on the current 9/11 run.

Not changed: `repro/`, `registry/`. `registry/page_notes.json` still needs `python3 tools/record_page_notes.py` to record the new hub note.
