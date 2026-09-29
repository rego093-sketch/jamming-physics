# circulatory — light two-reviewer review (2026-09-29)

Scope: `docs/circulatory/` (hub, §1–§23, about) and `repro/circulatory/`. R1 checked claims against data. R2 ran `python3 -B repro/run_all.py` in `repro/circulatory/` and read the oncology constants.

## Summary

**Reproduction.** All 23 targets pass with drift 0 (digest `d8610156dcdd…`). The engine prints the page numbers: MAP 95.7, τ 1.54 s, GFR 125, osmolality 287, E 0.75, the RCC RR, the aflatoxin × HBV product and the KDIGO steps.

**Main problem.** Most [F] and [V] labels mark identities of the model, not tests against data:

- Ohm's law;
- τ = RC;
- F = 1 − E;
- a PI loop reaching its setpoint;
- a round trip through the barrier law;
- the product of two exponentials.

Headline numbers also depend on calibrated or chosen constants.

**Magnitude firewall.** The firewall held, but §17 is worded clinically ("demanding dose reduction", "must be dosed very carefully").

## Findings

| # | Severity | Where | Finding | Evidence |
|---|---|---|---|---|
| 1 | high | hub, §1 | Order (liver → kidney) and relative size (DWELL ∝ γ^1.5) are called "forced [F]". The hub says the switch fixes "which organ appears, in what order, and at what relative size". | Superseded per dna §RB and §AX-A. The liver-before-kidney order happens to match embryology, but one agreeing pair is not evidence. |
| 2 | high | §9 | "Matching the observed 73 to within 0.000%" is wrong. The 0.000% is the deviation of the combined RR from the product of the singles, an algebraic identity. The model gives 72.0, which is about −1.4% from the cited 73. | `tools/build_docs.py` line 420 uses `multiplicativity_dev_pct`; `RR_COMB_META = 73.0` |
| 3 | high | §8 | RR(50 PY) = 2.00 is the calibration point, not an output. | `D_RCC = 0.76645 # Kramers scale s.t. RR(50 pack-years) = 2.0` in `repro/_oncology/carcinogen_dose_response.py` |
| 4 | medium | §6, §19 | The flow-elasticities 0.90 and 0.10 and the CLint-elasticities 0.91 and 0.11 restate the chosen extraction ratios. In the well-stirred model d ln CL/d ln Q = E and d ln CL/d ln CLint = 1 − E exactly. | algebra |
| 5 | medium | §15 | The KDIGO landing holds by construction: N = threshold/125 (for example, 0.72 × 125 = 90). | page table |
| 6 | medium | §2, §3, §4, §5 | Several results were graded [F]/[V] but hold by construction or come straight from inputs: MAP = CO × SVR "holds <1%", fitted τ = RC, and the plateau or setpoint reached by an integral controller. MAP 95.7 and τ 1.54 are outputs of the input CO, SVR, R and C. | engine design |
| 7 | medium | §22, §23 | "Round-trips exactly [V]" means inverting the barrier law and then applying it, which returns the input. | page text |
| 8 | low | §16, §17, §21 | Several values are outputs of chosen settings: breakthrough at 195 mmHg (chosen resistance ceiling), the 3.1× and 1.09× folds (chosen CLint reduction), and the ~7× and ~148× suppression (chosen D = 0.10). | page and code |
| 9 | low | §2–§6 | Observations were missing next to the model claims: the normal MAP range, human diastolic τ, the autoregulation range, the osmolality range and propranolol F ≈ 25%. | — |

## What I changed (docs/circulatory only; no numbers changed, no notes removed)

- **Hub:**
  - reading-rule lt-note after `<h1>`;
  - TOC grades relabelled per section;
  - order/size sentence marked [interpretation]/[O];
  - legend put in entity form.
- **All chapters:** [F] → [consistency]. [V] → [code output], [consistency] (§9, 15, 18, 19, 21–23) or [interpretation] (§1). γ cards → [code output]. Mapping cards → [interpretation].
- **§1:** order and size marked [interpretation]/[O], with the embryology observation and the §AX-A caveat.
- **§2:** consistency note, MAP range (Guyton & Hall).
- **§3:** consistency note, Westerhof 2009.
- **§4:** consistency note, Carlström 2015.
- **§5:** consistency note, Verbalis 2003.
- **§6:** elasticity = E, propranolol F (Routledge & Shand 1979), "no dose derived".
- **§8:** calibration-point note, Hunt 2005.
- **§9:** corrected the meaning of 0.000% (72.0 vs 73 is −1.4%), without changing any number.
- **§15:** construction note, KDIGO 2012.
- **§16:** ceiling dependence.
- **§17:** consistency wording, plus a note that the folds are illustrative code outputs and the page gives no dose.
- **§19:** 1 − E identity.
- **§20:** consistency wording.
- **§22, §23:** VHL/HFE blocks → [observation]; roster → [interpretation] plus a round-trip [consistency].

Not changed: `about/` legend, `repro/`, `registry/`. Run `python3 tools/record_page_notes.py` to record the new hub note.
