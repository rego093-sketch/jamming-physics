# digestive — light two-reviewer review (2026-09-29)

**Scope.**
- Pages: `docs/digestive/` (hub, §1–§30, about/faq/methods).
- Code: `repro/digestive/`.

**Reviewers.**
- R1 checked claims against data.
- R2 ran the engine directly: `slow_wave_clock`, `emerge_organs`, a τs sweep and an FFT-window/ISI comparison.
- `python3 -B repro/run_all.py` did not finish within 120 s and was stopped.

## Summary
- **Reproduction.** The engine reprints the clock numbers exactly: K_TIME 2400, gastric 3.0, duodenum 11.1, jejunum 9.0 and ileum 7.5 cpm. The γ values (1.5609 / 1.45 / 1.4732 / 1.525) and the order all match.
- **Headline gradient.** The "zero intestinal tuning" duodenal prediction depends on chosen intestinal τs values and on the FFT window.
- **Order.** Developmental order is graded [V], and its "sign validation" has no code.
- **Firewall.** The magnitude firewall holds: 50 g/day is the IARC exposure anchor, and it already carries a firewall note.

## Findings
| # | Severity | Where | Finding | Evidence |
|---|---|---|---|---|
| 1 | high | §1, methods, hub | Order (intestine, pancreas, liver, stomach) is "forced by the substrate [V]" and "sign validated vs cited developmental-timing anchor". No code performs that validation: the phrase exists only as a label string (`vp_dig_engine.py` lines 197 and 212). The order also contradicts embryology, where the liver bud (about day 22–24) comes before the pancreatic buds (about day 26). | grep of `repro/digestive/` |
| 2 | high | §3 | Duodenum 11.1 cpm "with zero intestinal tuning". The intestinal τs values are chosen constants (TAU_DUO = 95, GRAD_FACTOR = 1.5). The sweep below shows how the result moves with them. | τs_duo 80 / 90 / 100 / 110 / 120 → 12.9 / 11.7 / 10.5 / 9.6 / 9.0 cpm |
| 3 | medium | §3 | Frequencies come from an FFT over a fixed window T = 8000, which puts them on a 0.3 cpm grid. That grid causes the repeated 8.7 in the "monotone" table. The duodenal value also moves with the window, and ISI estimates differ slightly. | T = 6000 → 12.0 cpm; T = 12000 → 11.0; ISI → 10.99 (jejunum 8.96, ileum 7.57) |
| 4 | medium | §2 | The gastric 3.0 cpm matches the anchor by definition, because K_TIME = 3 / f(τs = 380). The "rhythm mechanism forced [V]" label on a chosen τs is misapplied. | engine line 79 |
| 5 | medium | §4, §5 | Transport direction follows the imposed sign of the gradient (+12 segments depends on run length, coupling and flux). The setpoint return is a closed-loop property by construction. | page and code |
| 6 | medium | §7–§30 | [F]/[V] are applied throughout to R19 readings of gates, reservoirs, afferents, barriers and flares. These are interpretations with code outputs. The shared D = 0.041667 and calibrated κ set every RR. | page text |
| 7 | low | §2, §3, §5 | Observations were missing: gastric slow wave ≈ 3 cpm (EGG 2.5–3.7), ICC pacemaking, the duodenum/ileum frequencies and normal fasting glucose. | — |

## What I changed
Edits are confined to `docs/digestive`. No numbers were changed and no notes were removed.

- **Hub.** Added a reading-rule lt-note after `<h1>`. The §1 TOC grade now reads [interpretation] and the other sections read [code output]. The "grade [V]" on order now reads [interpretation]/[O].
- **All chapters.**
  - [F] → [consistency] and [V] → [code output] (§1 → [interpretation]).
  - γ cards → [code output].
  - R19 mapping cards (gate, reservoir, afferent, metaplasia, perfusion, nucleation, wall, harness …) → [interpretation].
  - "is forced/verified [label]" wording smoothed.
- **Chapter edits.**
  - §1 and methods: order → [interpretation]/[O], plus a note that the sign validation has no code, plus the embryology observation.
  - §2: K_TIME consistency note; Parkman 2003 and Sanders 2006.
  - §3: τs and FFT-window input dependence; Huizinga & Lammers 2009.
  - §4: displacement dependence plus an observation.
  - §5: fixed-point note plus the ADA fasting glucose.
  - §7: D/κ dependence, with the size/order [O] link.
- **Not changed.**
  - Legend sentences in about/faq/methods, because they define the old grades (the hub note covers them).
  - `repro/` and `registry/`.
  - Run `python3 tools/record_page_notes.py` to record the new hub note.
