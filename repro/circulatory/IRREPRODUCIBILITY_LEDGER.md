# IRREPRODUCIBILITY LEDGER

Every `[O]` (open) quantity must be listed with its specific obstacle (VP-SPEC C3). An `[O]` without a
stated obstacle is a gate FAIL. This package reproduces all SHAPES, ORDERS, and ALGEBRA forced by the
substrate; what remains open is exclusively ABSOLUTE SCALE that requires external population/empirical
calibration. No shape, order, or synergy result is open.

| item | grade | obstacle (why not reproducible in-package) | location |
|---|---|---|---|
| absolute organ size / mass | [O] | DWELL ∝ γ^1.5 fixes RELATIVE size and developmental order [F]; the absolute magnitude needs an external growth-duration calibration (a single scale constant). Order liver→kidney and relative sizes ARE reproduced. | `inherited/vp_substrate.py` (Organ.size / dwell); engine emergence |
| absolute RCC incidence rate | [O] | The smoking dose-response SHAPE (monotone, saturating/sigmoidal) and the cited RR bands ARE reproduced [V]; converting RR to an absolute incidence per 100k needs the unexposed baseline hazard from a population life-table (external). | `repro/_oncology/carcinogen_dose_response.py::rcc_smoking_doseresponse` |
| absolute HCC incidence rate | [O] | The aflatoxin×HBV synergy ALGEBRA (additive barrier decrements ⇒ exactly multiplicative RR, ≈ meta product 72 vs 73) is reproduced parameter-free [V]; the absolute incidence still needs the population baseline hazard (external). | `repro/_oncology/carcinogen_dose_response.py::hcc_aflatoxin_hbv_synergy` |
| oncology Kramers scale D, smoking drive top h_top | [CAL] | These set the UNIT of the exposure→drive axis (pack-years, intake) only; they are calibrated once to the cited heavy-exposure RR and do NOT affect the dose-response SHAPE or the multiplicativity, which are forced by the barrier law. Honest calibration, not a free synergy knob. | `repro/_oncology/carcinogen_dose_response.py` (D_RCC, D_HCC, H_TOP_FRAC) |
| absolute resting cardiac output / vessel calibres | [O] | MAP = CO×SVR [F] and the Windkessel τ = R×C [F] are reproduced as RELATIONS and land in cited human bands; the absolute resting CO and per-vessel calibres are anthropometric inputs [L], not derived here. | `repro/_engine/vp_cir_engine.py` (windkessel, circulate) |
| absolute cardiovascular event rate (isolated systolic HTN, T8) | [O] | The hemodynamic SHAPE of arterial stiffening — PP widens, τ=RC shortens, MAP flat, an ISH point at SBP≥140/DBP<90 — is reproduced [V] and anchored to Franklin Circulation 1997;96:308; converting it to an absolute CV-event rate needs a population hazard model (external). | `repro/_verify/stress_tests.py::t8_arterial_stiffening` |
| absolute plasma sodium in diabetes insipidus (T11) | [O] | DI as ADH-gain→0 reproduces the no-recovery hyperosmolality and the intact-loop contrast [V]; mapping osmolality to an absolute plasma Na needs a renal free-water-clearance calibration (external). | `repro/_verify/stress_tests.py::t11_diabetes_insipidus` |
| absolute plasma sodium + volume-escape kinetics in SIADH (T12) | [O] | SIADH as a downward shift of the defended osmolality reproduces the held hyponatremia and the exact DI/SIADH mirror [V]; the minimal osmostat omits the volume-mediated ADH escape that caps real SIADH, so the absolute Na and the escape time-course remain open. | `repro/_verify/stress_tests.py::t12_siadh` |
| absolute CKD stage prevalence (T13) | [O] | Remaining-nephron-fraction scaling steps total GFR through the KDIGO thresholds with a flat autoregulated plateau at each level and an open-loop contrast [V]; the absolute prevalence of each G-stage needs population data (external). | `repro/_verify/stress_tests.py::t13_ckd_staging` |
| absolute drug exposure in hepatic impairment (T15) | [O] | Cirrhosis as CLint↓ reproduces the high-extraction F rise (dose-reduction direction) and the high-E/low-E selectivity [V]; the absolute exposure (AUC, plasma level) needs a severity→CLint calibration per agent (external). | `repro/_verify/stress_tests.py::t15_hepatic_impairment` |
| disease severity-axis units (C_ART stiffening range, osmostat setpoint shift, nephron fraction → KDIGO) | [CAL] | These set the UNIT of each severity axis only (compliance↔PP, ADH defended-setpoint↔serum osm, nephron fraction↔GFR stage); calibrated once to the cited clinical band, they do NOT affect the reproduced SHAPE/CONTRAST (PP-widening, DI/SIADH mirror, flat staged plateau). Honest axis calibration, not a free disease knob. | `repro/_verify/stress_tests.py` (T8/T12/T13 settings) |
| cell-fate barrier = γ²/4 from promoter stacking energy (therapeutics layer T18–T21) | [O]/[H] | The reversibility threshold (= spinodal), the ½ critical exponent, the synergy-reversal de-escalation, and the exponential barrier-restoration leverage are all FORCED [F] / VERIFIED [V] *on the R19 kernel*; but their clinical force rests on the unverified claim that a real tumour's cell-fate escape barrier equals γ²/4 read from the master-gene promoter NN-stacking ΔG37. No experiment yet links promoter stacking energy to a measured cell-fate barrier height. The therapeutic readings (differentiation-therapy responder boundary, prevention-dominance) are predictions [H], not established results, and not clinical guidance. | `repro/_oncology/barrier_therapeutics.py`; sections §20–§21 |
| simultaneous 4-way HCC co-exposure product (aflatoxin × HBV × HCV × ethanol), T23 | [H] | Single-agent RRs and the two PAIRWISE synergies (aflatoxin×HBV multiplicative; HBV×HCV between additive and multiplicative) are epidemiologically anchored [L] and reproduced [V]; a simultaneous ≥3-way multiplicative product has **no anchored cohort** in the literature. The full 4-way product (`combined_RR_multiplicative` ≈ 1647) is therefore a model extrapolation, marked machine-explicitly as **ILLUSTRATIVE [H]** (`oncology_roster.deescalation::combined_product_status`), surfaced as such in §23 — never claimed as data. Resolution per handoff §4 item 2 (v0.5.0). | `repro/_oncology/oncology_roster.py::deescalation`; `repro/_verify/stress_tests.py::t23_hcc_carcinogen_roster`; §23 |
| cross-volume gene-key references VHL (hereditary RCC) and HFE (hereditary HCC), §22/§23 | [V]/[O] | The gene-key **identities** (VHL 3p25-26; HFE 6p22.2, p.C282Y), a cited **magnitude** (HFE: HR 10.5, 95% CI 6.6–16.7, Atkins JAMA 2020), and the **seam** to circulatory's acquired R19 axes (TCE acts via the VHL/HIF pathway; iron-overload cirrhosis is a chronic drive on the liver R19 axis) are literature-anchored and wired from a single source (`inherited/cross_references.json`) — graded **[V]**. SSOT: these entities are *consumed*, not re-emerged; their cell-fate **barrier-height derivation is owned by `disease_wp`** and inherits the γ²/4-grounding `[O]/[H]` above. | `inherited/cross_references.json`; `inherited/cross_references.py`; §22 (VHL), §23 (HFE) |

## Reproduced in-package (NOT open) — for contrast

- Organ identity + developmental order from measured master-gene γ (SIX2 kidney 1.5556, HHEX liver 1.525): **[V]**, cited from DNA morphogenesis clock; consumed read-only.
- MAP − CVP = CO × SVR across a wide CO×SVR grid (Ohm pressure–flow): **[F]**.
- Windkessel diastolic decay τ = R × C across an R×C grid; resting aortic τ ≈ 1.5 s: **[F]/[L]**.
- Glomerular autoregulation plateau via tubuloglomerular feedback (flat GFR over 80–180 mmHg; open-loop is not flat): **[V]**.
- Osmoregulation ADH/thirst loop returns plasma osmolality to ≈287 mOsm/kg under load (no-loop does not): **[V]**.
- Well-stirred hepatic extraction E: 0→1 with intrinsic clearance, F = 1 − E; flow-limited (high-E, clearance flow-elasticity ≈ 0.90) vs capacity-limited (low-E, ≈ 0.10); propranolol E ≈ 0.75, F ≈ 0.25: **[F]/[L]**.
- Carcinogen barrier law barrier_eff(g,0) = g²/4 exactly, → 0 at the spinodal: **[F]**.
- Aflatoxin × HBV additive barrier decrements ⇒ exactly multiplicative RR (≈72 vs cited 73), parameter-free; predicted sub→supra crossover as combined drive nears the spinodal: **[V]**.

### Disease extensions T8–T17 (single-knob perturbations of the relations above)

- **T8** arterial stiffening (C↓): PP widens, τ=RC shortens, MAP flat, ISH point SBP≥140/DBP<90 (Franklin 1997): **[V]**.
- **T9** essential hypertension (SVR↑): MAP rises with MAP=CO×SVR exact (<1%); same MAP from a CO rise (flow vs resistance contrast): **[F]**.
- **T10** shock subtypes: hypovolemic (CO↓) and distributive (SVR↓) both reach MAP<65 from distinct knobs at equal MAP (Surviving Sepsis): **[F]**.
- **T11** diabetes insipidus (ADH gain→0): water deficit uncorrected, sustained hyperosmolality vs intact-loop recovery: **[V]**.
- **T12** SIADH (defended osmolality shifted down): osmolality held below setpoint, exact mirror of DI: **[V]**.
- **T13** CKD (remaining-nephron fraction): total GFR steps through KDIGO 90/60/45/30/15 with a flat plateau at each level; open loop does not: **[V]**.
- **T14** autoregulation breakthrough: GFR/P_GC flat over 80–180 mmHg then rise past the ceiling (~195 mmHg), from the TGF actuator saturating: **[V]**.
- **T15** hepatic impairment (CLint↓): high-extraction F rises ~3× (dose-reduction rule F=1−E) while a low-extraction drug is spared: **[V]**.
- **T16** portosystemic shunt: F = 1−(1−s)E with dF/ds = E exactly, so high-extraction (flow-limited) drugs are most affected: **[F]**.
- **T17** enzyme induction/inhibition: clearance CLint-elasticity ≈1 (low-E, capacity-limited, DDI-sensitive) vs ≈0 (high-E, flow-limited); inhibition raises F, induction lowers it: **[V]**.

### Oncology therapeutic-target layer T18–T21 (consequences of the carcinogenesis kernel for REVERSING the transition)

- **T18** reversibility threshold = spinodal: a driven pre-malignant cell reverts on drive-removal below h_sp = 2(γ/3)^1.5 and commits irreversibly above it; simulated threshold equals the analytic spinodal (RCC 0.749 vs 0.747, HCC 0.725 vs 0.725): **[F]/[V]**, therapeutic responder-boundary reading **[H]**.
- **T19** critical slowing: reversion time diverges with the universal fold exponent ½ (fitted −0.506 RCC, −0.507 HCC) as drive approaches the threshold; near-threshold lesions are marginally stable / relapse-prone: **[F]/[V]**.
- **T20** synergy reversal (de-escalation): removing one of two multiplicative carcinogens divides combined risk by its RR (HBV: 72→6.37, 11.3×) versus the ~1.17× additive expectation; retrodicts the large benefit of HBV control in aflatoxin regions: **[V] vs [L]**.
- **T21** barrier-restoration leverage: raising the escape barrier by δ suppresses malignant crossing by exp(−δ/D) (log-suppression linear in δ, slope −1/D exactly); prevention dominates cure exponentially: **[F]/[V]**.

> Honest boundary (T18–T21): the reversion logic itself (Waddington landscapes; differentiation therapy — APL/ATRA, IDH inhibitors) is established systems biology. The package's falsifiable additions are quantitative — barrier = γ²/4 from measured promoter stacking energy, and the spinodal as a sharp irreversibility threshold with a ½ exponent. The barrier grounding is the weakest link ([O]/[H], see table); these are testable target hypotheses, not clinical recommendations.

> Determinism: every result emits a stable sha256; the gate requires two independent computations to be
> byte-identical (`research_complete.json`), stdlib + numpy only, BLAS thread-pinned.
