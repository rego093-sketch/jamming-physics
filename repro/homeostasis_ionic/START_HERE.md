# START HERE — homeostasis_ionic_vp_site

**Mineral / Acid-Base / Electrolyte Homeostasis** — the third homeostasis axis (calcium-phosphate · pH · Na/K
setpoints as defended attractors of multi-organ loops on the R19 jamming-lattice substrate).

**Status:** v0.8.0 · research **COMPLETE (all gates green)** · `PHASE=writing` · canonical `docs/` **built** (16 sections).
**Bootstrap:** read this → then **`CHARTER.md`** (full plan + research results + writing manifest). Handover detail
in **`HANDOVER.md`**; the remediation roadmap (why "cover everything" is multi-increment) in **`REMEDIATION_PLAN.md`**;
governance in **`VP_SPEC_v1_8.md`**; open items in **`IRREPRODUCIBILITY_LEDGER.md`**.

## What is new in v0.8.0 (THERAPEUTIC-ORGANIZING increment — the three-lever principle, cross-volume inheritance)
A genuinely new layer on top of the completed Tier roadmap: the volume now carries a **therapeutic-organizing
technology inherited from the non-opioid analgesic volume** (concept DOI **10.5281/zenodo.20733420**) and proves it
on this volume's own DNA-grounded loop. The whole construction rests on the package's existing **real DNA emergence** —
five organs emerged from MEASURED master-gene γ (RUNX2 1.2414 · CASR 1.3299 · VDR 1.4243 · GCM2 1.4642 · SIX2 1.5556,
NCBI promoters + SantaLucia 1998, never fitted) → node barrier b=γ²/4 → loop gain k. This is not a toy simulation;
the therapeutic levers are read off that measured-γ chain.
- **Three-lever principle** (`repro/_therapy/three_lever.py`, NEW): a defended setpoint dx/dt=−k(x−x*)+load+noise has
  exactly three independent handles — **L1** lowers the load (source), **L2** raises the loop gain k (gain), **L3**
  relocates the target x* (setpoint). The load-bearing **asymmetry theorem**, reproduced on the volume's own OU law:
  *only L2 tightens the stationary variance σ²/2k* (L1 lowers the mean only; L3 moves the defended value durably) [V].
  The **L2 gain ceiling per arm is the measured-γ barrier b=γ²/4** — the most powerful lever inherits its headroom
  from the emerged genome (deepest SIX2, shallowest RUNX2; monotone in γ) [V]. The 27 non-opioid analgesic targets
  map one-to-one onto L1/L2/L3 [L], because both volumes are the same R19 threshold object at two sites.
- **Existing-results crosswalk** (same module): every therapy already derived in this volume is re-read live and turns
  out to be exactly one lever — set-point resets (calcimimetic/calcilytic, durable sensor reset) = **L3**; reservoir
  refill (anabolic>anti-resorptive), dual-antibody bone window, renal-HCO₃-arm restoration = **L2** (the results that
  turn on tightening variance); otoconial stability, spinodal stone crossing, upstream-driver removal = **L1**. All validated [V].
- **Disease remediation** (`repro/_therapy/disease_remediation.py`, NEW): the nine **owned** diseases (common/polygenic/
  acquired/age-related loop disorders) each get a **primary lever SELECTED from which OU parameter they corrupted**,
  demonstrated on the OU law and turned into a cited, honestly-graded improvement. Distinctive calls include
  osteoporosis **anabolic-first** (refill the gain before holding the drain: teriparatide/abaloparatide/romosozumab →
  then bisphosphonate/denosumab), hyperparathyroidism & ADH1 as **setpoint resets** (cinacalcet down / encaleret up),
  CKD-MBD as a **multi-arm failure needing all three levers**, and calcium stones as a **fixed-threshold disease where
  L2 does not apply** (L1 keeps the drive in the soluble basin; L3 lowers the product set-point). Owned-disease
  boundaries per **VP_FRAMEWORK_MAP §6** are not crossed; rare/monogenic gene facts are cited to disease_wp, carcinogen
  cancers to the mechanistic volumes.
- **Additive only:** research gate sha **unchanged** (`35d31461…`, all_green, determinism 2×sha256 identical); the two
  new therapy modules import only `vp_loops` / existing modules and are surfaced in `run_all` **[15]/[16]** and docs
  **§14/§15/§16** but do **not** feed the gate. Docs advanced to **16 section pages**; the engine tree is byte-identical.
  No new [O] item — both modules reuse the existing OU law (absolute clinical magnitudes remain [O]/[H] as before).

## What is new in v0.7.0 (REMEDIATION increment — Tier-3, completes the "cover everything" program)
The v0.4.0 audit's last two open items — the molecular transport **dynamics** beneath the loop arms (G5) and
the per-species master-gene **γ** that would ground the cross-species gains (G6) — are now closed. This finishes
the Tier roadmap; both increments are **additive** (research gate sha unchanged) and the docs rebuild byte-identical.
- **G5 transport dynamics** (`repro/_engine/transport_dynamics.py`, NEW): the one new **FORCED** primitive —
  the **GHK constant-field flux** through a gated channel (reverses at Nernst, rectifies) plus Boltzmann/Hill gating.
  Its central result is a **connection**: the membrane flux slope at the setpoint **k = −dJ/dC IS the OU loop gain**
  the rest of the volume already runs on [V] — channel number sets setpoint stability, and a loss-of-function
  transporter is the loop-gain drop *at the membrane* (the molecular reading of TRPV5/6 → renal Ca wasting,
  ENaC/SCNN1A → PHA1, H⁺-ATPase/ATP6V → distal RTA [L]). GHK+gating [F]; k=−dJ/dC [V]; absolute conductances [O].
  Surfaced in `run_all` **[12]** + docs **§12**; anchors A-GHK, A-TRPV, A-ENAC, A-HATPASE added.
- **G6 per-species γ** (`repro/_engine/comparative_gamma.py`, NEW; `inherited/comparative_promoters.cache.json`):
  an **HONEST NEGATIVE**, published not hidden. The osmoregulatory master gene **ATP1A1** (Na⁺,K⁺-ATPase α-1)
  promoter γ was **measured** across six species (oyster/elephant-shark/skate/zebrafish/Xenopus/human) by the
  same NN-stacking pipeline, human-anchored and offline-reproducible [V]; the pipeline is sound (two independent
  elasmobranchs agree to γ±0.0003). But γ is **non-monotone** in the loop gain k (Spearman 0.65; the k=3.0 Xenopus
  γ exceeds the k=4.0 human) and instead tracks promoter **GC** almost perfectly (Spearman 1.0). So per-species γ
  is the wrong instrument — the within-genome γ-ladder does not transfer cross-genome — and the comparative
  absolute k stays **[O]**, now with that GC confound as its documented reason. `run_all` **[13]** + docs **§13**; anchor A-ATP1A1.
- **Additive only:** research gate sha **unchanged** (`35d31461…`, all_green); the two new modules import only
  `vp_loops` / their cache. Docs advanced to **13 section pages** (rebuild byte-identical). The only new [O] is G5's
  absolute electrophysiological calibration (single-channel conductances / densities).

## What was new in v0.6.0 (REMEDIATION increment — Tier-2 disease coverage)
The v0.4.0 audit also asked whether every ion-imbalance disease was covered. The pathology chapter closed
seven representative diseases and let rare/specific forms enter as a cited parameter; three further **major**
diseases were named but not yet modelled. v0.6.0 closes them — **reusing the existing six failure modes, no
new primitive** — and filed the rest (molecular transport dynamics; per-species γ) as Tier-3, now done above.
- **Tier-2 module** (`repro/_pathology/tier2_ion_diseases.py`, NEW): **G2 magnesium** (hypo-/hypermagnesemia)
  = the loop-gain-drop / buffer-arm-failure mode read on a third defended ion via the volume's own
  `ou_setpoint` (err=load/k); a failed arm (low k) under an Mg-loss drive → hypomagnesemia (TRPM6/Gitelman),
  under an Mg-intake drive → hypermagnesemia; both monotone in 1/k, ratio == gain ratio (4.0×), variance
  blow-up. **G3 CKD-MBD** = a multi-arm renal-integrator gain drop: stepping the renal gain down drives the
  cited KDIGO cascade — PO4 up, 1,25-vitD down, Ca down, PTH up (secondary HPT) all monotone, the Ca×PO4
  product near-normal early and climbing to the precipitation ceiling in advanced CKD. **G4 humoral
  hypercalcemia of malignancy** = a set-point drift UP: an exogenous unsuppressible PTHrP drive relocates the
  defended Ca up (the inverse of the T1 reset) with endogenous PTH appropriately suppressed (the fingerprint).
  Directions [V]; cited setpoints/variants/guidelines [L] (Mg ~0.85 mM; Schlingmann 2002 TRPM6; Gitelman;
  KDIGO 2017; Stewart 2005 PTHrP); absolute magnitudes/timing [O]. Surfaced in `run_all` [11] + docs **§11**;
  anchors A-MG, A-CKD, A-PTHRP added.
- **Additive only:** research gate sha **unchanged** (`35d31461…`, all_green) — γ-emergence + stress battery
  do not import the new module; docs were at **11 section pages** (rebuild byte-identical).

## What is new in v0.5.0 (REMEDIATION increment — cross-species axis added)
A v0.4.0 audit asked: which animals use ions precisely, which conform, and is every ion disease covered? The
package modeled ONE species (human). v0.5.0 closes the **largest** gap — the cross-species axis — and files a
tiered plan (`REMEDIATION_PLAN.md`) for the rest.
- **Comparative ionoregulation** (`repro/_engine/comparative_ionoregulation.py`, NEW): which animals **defend**
  ions (regulators) vs **conform** to the environment, on the SAME R19 substrate, via the volume's OWN OU law
  (step error = load/k). One knob — loop gain k. osmoconformer (k 1.0, tracks env 100%) < urea-retaining
  elasmobranch (2.0) < teleost/amphibian regulator (3.0) < terrestrial mammal (4.0, tracks 25% = tightest).
  Conformer dragged to 1.00 under a salinity load vs regulator 0.25 (ratio 4.0× == gain ratio); excursion
  monotone in k. Strategy assignment cited [L]; separation [V]; absolute k & salinity tolerance [O]; per-species
  master-gene γ not yet measured [O]/[H]. Surfaced in `run_all` [10] + docs **§10**.
- **Additive only:** research gate sha **unchanged** (`35d31461…`, all_green); docs concat sha advanced to
  `d6a67a25…` (10 section pages now; rebuild byte-identical).
- **Honest scope:** "cover everything" is a multi-increment program. v0.5.0 = Tier-1 (cross-species). Tier-2
  (Mg / CKD-MBD / humoral hypercalcemia of malignancy, reusing existing failure modes) and Tier-3 (transporter
  gating dynamics; per-species γ measurement) are the next tasks — see `REMEDIATION_PLAN.md`.

## What is new in v0.4.0 (frontier program complete — all four hypotheses quantified)
- **H-RESET & H-ARM quantified** (`repro/_therapy/frontier_quant.py`): the last two bare-[H] frontier
  hypotheses now have a reproduced mechanism. **H-RESET** — a sensor is a comparator whose defended attractor
  equals its set-point for every Hill steepness (structural identity), so an allosteric reset relocates the
  defended value durably (residual ~0) while symptom control relapses to the mis-set attractor on withdrawal
  (residual 0.15), and the direction holds for the whole ionic-sensor family CaSR/ENaC/ASIC/OTOP1 (encaleret
  Phase-3 CALIBRATE / cinacalcet [L]). **H-ARM** — reusing the volume's own OU law (err=load/k, Var=σ²/2k),
  restoring the failed arm (raising k) tightens variance and rejects a fresh acid load by ≈k_high/k_low (4.0×:
  excursion 2.00→0.50), whereas lifelong buffering (distal-RTA → ADV7103/Sibnayal [L]) cancels only the mean.
  Direction [V]; absolute magnitudes [O]; clinical efficacy [H].
- **All four frontier hypotheses now quantified** — H-RESET, H-DUAL, H-OTOC (v0.3.0) and H-ARM together close
  the frontier-quantification program begun in v0.3.0. Surfaced in `run_all` [9] and docs §09.
- **Additive only:** research gate sha **unchanged** (`35d31461…`, all_green) — γ-emergence + stress battery
  untouched; the new functions are pure additions surfaced in `run_all`/docs.

### Carried from v0.3.0 (TmP/GFR closure + first two frontier quantifications)
- **RI5 TmP/GFR COMPUTED** (`repro/_engine/renal_phosphate.py`): exact Walton-Bijvoet — normal 1.114 mmol/L
  (in reference 0.80–1.35 [L]); FGF23/PTH lower it (XLH 0.450 < normal < hypoPTH 2.342 [V]/[L]). γ sets
  STABILITY, not the VALUE ([CAL]/[F], not γ-derivable) — a precise by-design residual, not a blanket [O].
- **H-DUAL & H-OTOC** (`repro/_therapy/frontier_quant.py`): H-DUAL window dual 12.79 > single 1.08 >
  untreated 0.00 (Florio 2016 [L]); H-OTOC calcite Ω → acidosis 0.695 / low-Ca 0.755 (both <1; Frontiers 2025 [L]).

## Measured master γ (NCBI promoters, SantaLucia 1998 NN-stacking; never fitted; bit-validated vs vendored SIX2)
| node | master | γ | dyn class |
|---|---|---|---|
| bone_mineral_reservoir | RUNX2 | 1.2414 | reservoir |
| calcium_sensing_receptor | CASR | 1.3299 | setpoint-comparator |
| vitamin_d_axis | VDR | 1.4243 | slow-loop |
| parathyroid_pth | GCM2 | 1.4642 | setpoint-loop |
| kidney_mineral_acidbase | SIX2 | 1.5556 | setpoint-loop |

Developmental order (γ asc): **bone < CaSR < vitD < PTH < kidney**.

## Stress battery (RI1–RI5) — all PASS
RI1 calcium → setpoint 1.0003 · RI2 acid-base → pH 7.401 (Winters slope 1.10) · RI3 bone reservoir 1.00→0.43
(serum Ca held) · RI4 Na 140 / K 4.2 · RI5 phosphate Ca×PO4 max 1.399 < 1.6. Substrate law: barrier b=γ²/4 sets
loop stiffness k (γ sets setpoint **stability**; the value stays cited).

## Reproduce
```
python repro/run_all.py        # emerge + laws + RI1–RI5 + sensory + literature + pathology + therapy + [8]TmP/GFR + [9]frontier + [10]comparative + [11]Tier-2 diseases + [12]transport dynamics + [13]comparative γ + [14]gates (all_green=True)
python tools/build_docs.py     # rebuild canonical docs/ (PHASE=writing; 13 sections; byte-identical)
```
Deterministic (VP-SPEC C1): BLAS single-thread, fixed seed, round-before-hash, sorted JSON. Research sha
`35d31461…` (2× identical, **unchanged in v0.7.0 — additive**; γ-emergence + stress battery do not import the Tier-2/Tier-3 modules); `docs/` rebuild byte-identical (13 section pages; the HTML concat sha embeds the build date).

## Invariants (do not break)
γ is measured (no fitting) · determinism (seed/round/2×sha) · honest grade + stated [O]/[H] · English body ·
single zip (original + additions). DOI: **TBD** (assigned on publication → fills `build_docs.py` `DOI=` + cross_volume registry).
