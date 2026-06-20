# FALSIFICATION PROTOCOL — Circulatory Oncology Therapeutics Layer (§§20–21)

**paper:** `circulatory_vp_site` · **code:** `cir` · **version:** v0.6.0 · **handoff §4 item 5**

> This is a **pre-registration** of the falsifiable predictions of the oncology therapeutics layer
> (§§20–21 / T18–T21). It exists so that item 5 ("empirical tests of the falsifiable core") is
> *drop-in ready*: the predicted numbers are already FORCED and locked by the substrate
> (`repro/_verify/predictions_registry.py`, computed from `vp_substrate.barrier = γ²/4` and
> `spinodal = 2(γ/3)^1.5`), and each carries an explicit **falsification threshold** and a **candidate
> data source**. When real measurements arrive, the comparison is mechanical — no re-derivation, no
> moving of coefficients (No-Tuning).
>
> **Discipline.** These are **testable target hypotheses, not clinical guidance** (grade `[O]/[H]`, see
> `IRREPRODUCIBILITY_LEDGER.md`). No numbers here are fabricated: the predictions are the substrate's,
> and the *data columns are deliberately empty* until a cited external source fills them. A prediction
> is **PASS** only against a real anchored dataset; until then its status is **OPEN**.

Reproduce the locked predictions:
```
python repro/_verify/predictions_registry.py        # emits P1/P2/P3 forced values + falsification criteria
python repro/run_all.py                              # section [6] prints the same registry
```

---

## What is and isn't being claimed

The reversion logic itself (Waddington/Huang–Kauffman bistable cell-fate landscapes; differentiation
therapy — APL/ATRA, IDH inhibitors) is **established** systems biology and is **not** the contribution.
The framework's **falsifiable additions** are quantitative and are what this protocol tests:

1. the cell-fate escape **barrier = γ²/4** read from the *measured* master-gene promoter stacking energy;
2. the **spinodal as a sharp irreversibility threshold** (not a gradual dose-response);
3. the **½ critical-slowing exponent** near that threshold.

The weakest link — and therefore the highest-value test — is **P3**: no experiment yet links promoter
stacking energy to a measured cell-fate barrier height.

---

## P1 — Reversibility threshold = spinodal

- **Hypothesis.** A carcinogen-driven pre-malignant cell reverts on drive-removal **below** a sharp
  threshold and commits irreversibly **above** it; the threshold is the R19 spinodal
  `h_sp = 2(γ/3)^1.5` read from the master-gene promoter stacking energy.
- **Forced value (locked).** `h_sp` = **0.7468** (kidney, SIX2 γ=1.5556) · **0.7249** (liver, HHEX γ=1.525).
  Matches the §20/T18 analytic spinodal (sim 0.749/0.725).
- **Measurement.** Map differentiation-/de-driving-therapy **responders vs non-responders** onto a drive
  proxy (cumulative exposure or an equivalent severity axis).
- **Falsification threshold.** **PASS** if the responder/non-responder boundary **tracks `h_sp` sharply**.
  **FALSIFIED** if responders extend well past the spinodal, **or** if there is no sharp boundary at all
  (a smooth dose-response with no threshold).
- **Candidate data.** RCC/HCC differentiation- or de-driving-therapy responder cohorts; the cleanest
  natural experiment is **HCV-cure → HCC-risk-reversal** series (drive removed; risk falls but does not
  vanish in already-cirrhotic livers — a post-threshold signature).
- **Grade.** `[F]/[V]` on the kernel; therapeutic responder-boundary reading `[H]`. **Status: OPEN.**

## P2 — Critical-slowing exponent = ½

- **Hypothesis.** Reversion time diverges as the drive approaches the threshold with the **universal fold
  exponent ½** (`t_rev ~ (h_sp − h)^(−1/2)`); near-threshold lesions are marginally stable / relapse-prone.
- **Forced value (locked).** exponent = **0.5** (§20/T19 fits −0.506 kidney, −0.507 liver).
- **Measurement.** Reversion / relapse **latency vs distance-to-threshold** for near-boundary lesions
  under drive-removal.
- **Falsification threshold.** **PASS** if the divergence exponent is **½ within error**. **FALSIFIED**
  if the exponent differs from ½, **or** if there is no critical slowing (latency flat near threshold).
- **Candidate data.** Longitudinal relapse-latency vs lesion-grade series for near-threshold pre-malignant
  lesions.
- **Grade.** `[F]/[V]` on the kernel; relapse-proneness reading `[H]`. **Status: OPEN.**

## P3 — Cell-fate barrier = γ²/4  (the weakest link, highest value)

- **Hypothesis.** The cell-fate **escape barrier** out of the healthy basin equals **γ²/4**, where γ is the
  *measured* master-gene promoter nearest-neighbour stacking energy (−mean NN ΔG37, SantaLucia 1998).
- **Forced value (locked).** barrier = **0.6050** (kidney, SIX2) · **0.5814** (liver, HHEX).
- **Measurement.** A cell-fate escape-**barrier proxy** — transition rate → Arrhenius barrier, or basin
  depth from single-cell fate-switching statistics — across master genes with **different measured γ**.
- **Falsification threshold.** **PASS** if the proxy **scales as γ²/4** (slope 1 on a barrier-vs-γ²/4 plot)
  across genes. **FALSIFIED** if there is no correlation, or a different functional form.
- **Candidate data.** Single-cell fate-switching / reprogramming-barrier assays paired with promoter
  NN-stacking ΔG37 for the relevant master genes (SIX2, HHEX, and ideally a third with a distinct γ to give
  the scaling a lever arm).
- **Grade.** `[O]/[H]` — no experiment yet links promoter stacking energy to a measured barrier height.
  **Status: OPEN.**

---

## Acceptance / No-Tuning rule

When a dataset is obtained, record the source (PMID/DOI), run the comparison **once** against the *locked*
forced value, and report PASS/FAIL **without adjusting any coefficient** to improve the fit (No-Tuning). A
disagreement is a result, not a bug to be tuned away. Promote the prediction's grade only on a genuine PASS
against anchored data; otherwise it stays `[O]/[H]` and OPEN here and in `IRREPRODUCIBILITY_LEDGER.md`.
