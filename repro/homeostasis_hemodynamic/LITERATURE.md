# LITERATURE — anchors, sensory cells, and the interaction map

**paper_id:** `homeostasis_hemodynamic_vp_site` · **code:** `hmd` · **version:** 0.2.0-research

This file is the existing-literature anchor registry for the hemodynamic homeostasis package, plus the
interaction map that connects the **sensory cells** to the loops. Every external result is CITED, not
re-derived; the package reproduces the loop/curve **shape or direction** ([V]) and pins each absolute
scale as **[O]** with an obstacle (see `IRREPRODUCIBILITY_LEDGER.md`). Grades: [V] reproduced
shape/direction · [L] cited identity/gain/mortality · [O] absolute scale open.

## 1. Sensory transduction layer (the fundamental layer beneath the controllers)

The CHARTER asks to go beneath the visible mechanism. The regulated variables are read by two concrete
molecular transducers, each the entry point of one loop. Modules: `repro/_sensory/`.

### 1.1 Baroreceptor — PIEZO1/PIEZO2 mechanosensor (fast loop)
- **Transducer:** PIEZO1 + PIEZO2, mechanically activated cation channels in the arterial wall
  (aortic arch / carotid sinus afferents).
- **Read:** firing rate is monotone in the stretch set by arterial pressure; transduction-limited
  (open-probability sigmoid), saturating at high pressure. Module `baroreceptor.py`: intact curve
  monotone 0→~97 Hz [arb]; PIEZO double-KO curve flat (no afferent). Afferent firing is a shared-R19
  spike train (the vendored substrate Neuron fires discrete all-or-none R19 events at suprathreshold
  drive).
- **Anchor [L]:** Zeng W-Z, Marshall KL, Min S, et al. *PIEZO channels are mechanically activated
  baroreceptors.* Science 362:464–467 (2018). Piezo1/Piezo2 sensory-neuron double-knockout abolishes
  the baroreflex and produces labile hypertension. (Identity strong; some debate on completeness,
  J Neurophysiol 122:13–15, 2019 — noted, not resolved here.)
- **Grade:** curve shape [V] · molecular identity [L] · absolute firing rate (Hz) [O].

### 1.2 Macula densa — NKCC2 NaCl chemosensor (slow loop)
- **Transducer:** apical Na-K-2Cl cotransporter NKCC2 (furosemide-sensitive) in the ~15–20 macula densa
  cells of the juxtaglomerular apparatus.
- **Read:** luminal NaCl (proportional to distal delivery / GFR) drives two monotone outputs:
  (a) **tubuloglomerular feedback (TGF)** — high NaCl → afferent arteriole constriction → GFR down
  (increasing in NaCl); (b) **renin** — INVERSELY related to NaCl (low NaCl → renin up → RAAS up).
  Module `macula_densa.py`: both transductions monotone; SGLT2i raises delivered NaCl (30→48 mM model)
  → TGF restored (0.667→0.762), damping hyperfiltration.
- **Anchor [L]:** macula densa NaCl sensing via apical NKCC2 → TGF + inverse renin control (classic
  renal physiology). SGLT2i benefit proposed via raised macula-densa NaCl delivery restoring TGF — a
  leading account of the renal/cardiovascular effect; ties the slow-loop sensor to a basin-restoring HF
  therapy.
- **Grade:** transduction shape [V] · molecular identity [L] · absolute NaCl/GFR scale [O].

### 1.3 Cited afferent seams NOT re-emerged here (SSOT)
Carotid-body chemoreceptors (O₂/CO₂/pH) and cardiopulmonary volume receptors are afferent seams owned
by the cardiorespiratory sibling package; they are **referenced**, not re-emerged here (no duplicate
sources of truth).

## 2. Loop / control anchors

- **Guyton renal–body-fluid feedback = INTEGRAL controller** ("infinite" steady-state gain): the
  kidney defends the long-run MAP setpoint; sustained hypertension REQUIRES a rightward reset of the
  pressure-natriuresis curve. Reproduced as RP3 (perfect adaptation) and RP4 (reset opposed back).
  Grade: shape [V] · anchor [L] · absolute setpoint [O].
- **Hydraulic Ohm relation** MAP = CVP + CO × SVR: RP1 reproduces resting ~93 mmHg from the two seam
  variables. Relation [V] · numeric [L] · absolute scale [O].

## 3. Major-disease therapy anchors (fundamental vs symptomatic)

The loop structure makes a sharp, falsifiable split that MATCHES the clinical evidence base in both
directions. Module: `repro/_therapy/fundamental_targets.py` (T1, T2).

### 3.1 Hypertension — reference reset (fundamental) vs operating-point push (symptomatic)
- **Renal denervation (reference reset):** FDA-approved Nov 2023 (Medtronic Symplicity Spyral; Recor
  Paradise ultrasound). Durable and TIME-INCREASING effect (e.g. GSR-DEFINE registry office SBP on the
  order of −20 mmHg at 3 yr; SPYRAL HTN-ON MED 3-yr durability) — the setpoint-reset signature, vs
  lifelong operating-point dosing. [L]
- **Diuretic / renal backbone:** durable control needs a volume/renal arm; vasodilator monotherapy
  escapes (the integral controller rejects an operating-point push back toward the reset reference).
- **Prediction (T1, direction [V]):** durability of BP reduction tracks how much a therapy resets the
  renal reference, not how much it pushes the operating point. Absolute effect sizes [O].

### 3.2 Heart failure — load reduction + cycle break (fundamental) vs effector flog (harmful)
- **Effector flog — positive inotrope:** PROMISE (Packer M, et al. NEJM 325:1468–1475, 1991): oral
  milrinone +28% all-cause mortality despite better hemodynamics. Neurohormonal-cost hypothesis. [L]
- **Load reduction + neurohormonal blockade — the four pillars, each with independent mortality
  benefit:** ARNI sacubitril/valsartan −16% all-cause death vs enalapril (PARADIGM-HF, HR 0.80,
  P<0.001); beta-blockers (CIBIS-II / MERIT-HF / COPERNICUS); MRA (RALES / EMPHASIS-HF); SGLT2i
  (DAPA-HF / EMPEROR-Reduced, NNT ≈ 19–21; DELIVER for HFpEF). All reduce load / break the vicious
  cycle — none flog the pump. [L]
- **Prediction (T2, direction [V]):** mortality benefit tracks the barrier margin
  M = spinodal(κ) − |load_eff|; load reduction + cycle interruption GROWS M (basin restored), effector
  flogging SHRINKS M (accelerated collapse). The SGLT2i arm acts via the macula-densa sensor (§1.2).
  Absolute effect sizes [O].

## 4. Interaction map (sensory → afferent → integrator/controller → effector → MAP → feedback)

Directed edges; sign: `0` read-only sense, `+` raises, `−` lowers. Built in
`repro/_engine/vp_hmd_engine.py::build_interaction_map()` (7 nodes, 11 edges).

| src | → dst | sign | grade | mechanism |
|---|---|---|---|---|
| MAP | baroreceptor | 0 | [L] | arterial wall stretch ~ pressure; PIEZO1/2 transduction (Zeng 2018) |
| MAP | macula_densa | 0 | [L] | distal NaCl delivery ~ GFR ~ pressure; NKCC2 chemosensing (slow) |
| baroreceptor | baroreflex | + | [L] | afferent firing → NTS → autonomic outflow set |
| baroreflex | vascular_resistance | − | [V] | fast negative feedback: pressure↑ → sympathetic withdrawal → SVR↓ (RP2) |
| baroreflex | MAP | − | [V] | net fast buffering of a pressure step, residual ≈ step/(1+G) (RP2) |
| macula_densa | raas_endocrine | − | [L] | high luminal NaCl → renin DOWN (inverse); low NaCl → renin UP |
| macula_densa | kidney_volume_integrator | + | [V] | TGF: high NaCl → afferent constriction → GFR down |
| raas_endocrine | vascular_resistance | + | [L] | AngII vasoconstriction raises SVR |
| raas_endocrine | kidney_volume_integrator | + | [L] | aldosterone/AngII raise Na/volume retention → raises the defended reference |
| kidney_volume_integrator | MAP | + | [V] | integral (pressure-natriuresis) control sets the slow defended MAP reference (RP3) |
| vascular_resistance | MAP | + | [V] | Ohm hydraulic: MAP = CVP + CO × SVR (RP1) |

**Fast loop (seconds):** MAP → baroreceptor(PIEZO) → baroreflex −(−)→ SVR/HR → MAP (RP2).
**Slow loop (hours–days):** MAP → macula_densa(NKCC2) → renin(−)/TGF(+) → RAAS/kidney integrator →
volume → MAP (RP3). **Disease axes:** essential hypertension = rightward reset of the kidney integral
reference (RP4); chronic heart failure = collapse of the cardiac high-output basin (RP5).

## 5. Reference list (verify-as-cited; [L])

1. Zeng W-Z, Marshall KL, Min S, et al. PIEZO channels are mechanically activated baroreceptors.
   Science 362:464–467 (2018).
2. Nonomura K, et al. / commentary on baroreceptor PIEZO completeness. J Neurophysiol 122:13–15 (2019).
3. Guyton AC. Renal function curve / integral control of arterial pressure (renal–body-fluid feedback);
   classic pressure-natriuresis and "infinite gain" formulation.
4. Macula densa NKCC2 NaCl sensing → tubuloglomerular feedback + inverse renin control (renal
   physiology; furosemide-sensitive apical transporter).
5. Packer M, Carver JR, Rodeheffer RJ, et al. Effect of oral milrinone on mortality in severe chronic
   heart failure (PROMISE). NEJM 325:1468–1475 (1991).
6. McMurray JJV, Packer M, Desai AS, et al. Angiotensin–neprilysin inhibition vs enalapril in heart
   failure (PARADIGM-HF). NEJM 371:993–1004 (2014).
7. CIBIS-II; MERIT-HF; COPERNICUS — beta-blockade mortality benefit in HFrEF.
8. RALES (Pitt B, et al. NEJM 1999); EMPHASIS-HF (Zannad F, et al. NEJM 2011) — MRA mortality benefit.
9. McMurray JJV, et al. DAPA-HF (NEJM 2019); Packer M, et al. EMPEROR-Reduced (NEJM 2020); Solomon SD,
   et al. DELIVER (NEJM 2022) — SGLT2i in HF.
10. Renal denervation pivotal program (SPYRAL HTN-ON/OFF MED; RADIANCE; GSR-DEFINE registry); FDA
    approvals of Symplicity Spyral and Paradise systems (Nov 2023).

> Citations are recorded for the writing phase (VP-SPEC C4). Exact effect sizes are anchors [L]; the
> package itself asserts only reproduced shapes/directions [V] and leaves absolute scales [O].
