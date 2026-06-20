# CIRCULATORY — DISEASE-SCOPE HANDOFF (next-session instructions)

**paper:** `circulatory_vp_site` · **code:** `cir` · **version at handoff:** v0.6.0 · **gate:** 23/23 PASS, writing unlocked

> Single-zip handoff per the framework convention. A fresh session is self-sufficient from
> `START_HERE.md → CHARTER.md`; this file records what circulatory's *disease* deliverable now covers,
> what is deliberately out of scope (with the sibling that owns it), and what remains to be done.
> Run `python repro/run_all.py` to reproduce the gate; `python tools/build_docs.py` to rebuild docs.

---

## 0. What circulatory owns (MASTER MAP §6 ownership contract)

The split axis is **etiology class, not body part**. circulatory is a *mechanical-dynamics* package, so it
owns the **acquired, common, dynamics-defined** diseases of its flow+clearance organs (kidney, liver,
vessels), explained by the **carcinogen → R19 barrier-lowering → Kramers crossing** kernel (and local
dynamics failures). Concretely, circulatory's owned diseases are its two acquired cancers:

| owned disease | organ (γ) | etiology class | status |
|---|---|---|---|
| **renal cell carcinoma (RCC)** | kidney SIX2 (1.5556) | acquired carcinogen-driven | **DONE** (root + prevention) |
| **hepatocellular carcinoma (HCC)** | liver HHEX (1.525) | acquired carcinogen-driven | **DONE** (root + prevention) |

Everything else that touches kidney/liver/vessels is owned by a **sibling** package (see §3).

---

## 1. What is DONE (v0.1.0 → v0.4.0)

**Physiology substrate (§§1–6).** Organ emergence from measured γ; hemodynamics (MAP=CO×SVR, Windkessel
τ=RC); renal filtration + autoregulation; osmoregulation; hepatic clearance F=1−E. Forced/verified.

**RCC — root + prevention (full roster).**
- Dose-response root: smoking RR(pack-years), monotone+saturating, in the Hunt-2005 band (§8, T6).
- Carcinogen roster (§22, T22): tobacco (RR 1.6) + trichloroethylene (RR 1.42, IARC Group 1) round-trip
  on the kidney R19 axis; **de-escalation** (remove a driver → divide combined risk), tobacco first.
- Honest correction: **aristolochic acid → upper-tract UROTHELIAL carcinoma (UUC) + AA-nephropathy/CKD**,
  NOT RCC; documented but not forced onto the RCC axis (different tissue, OR up to 49 exceeds the axis).
- Cross-reference: hereditary RCC (VHL) is owned by `disease_wp`; TCE acts via the same VHL pathway.

**HCC — root + prevention (full roster).**
- Synergy root: aflatoxin × HBV → exactly multiplicative RR (≈72), parameter-free (§9, T7).
- Carcinogen roster (§23, T23): aflatoxin (6.37), HBV (11.3), HCV (10.4), ethanol (2.2) round-trip;
  **two synergy datasets bracketed** by the two combination modes — aflatoxin×HBV multiplicative,
  HBV×HCV (observed 115) between additive (26.5) and multiplicative (178); **de-escalation** ranks
  prevention (HBV → HCV → aflatoxin → ethanol).

**Therapeutic-target layer for both cancers (§§20–21, T18–T21).**
- Reversibility threshold = spinodal (responder boundary for de-driving/differentiation therapy).
- Critical slowing (½ fold exponent) → near-threshold lesions are relapse-prone.
- Synergy reversal / de-escalation (remove one multiplicative driver → divide risk ~11× for HBV).
- Barrier-restoration leverage exp(−δ/D) → prevention dominates cure exponentially.

**Discipline.** 23/23 stress battery PASS; determinism 2×sha256 identical (emergence sha unchanged
across all additions); VP-SPEC v1.8 sites (answer-first, JSON-LD, claim-strip, vp-card, eq SVG alt=LaTeX);
`IRREPRODUCIBILITY_LEDGER.md` logs every [O]/[H]/[CAL].

---

## 2. Honest boundary — what is and isn't a real contribution

- **Established, not new:** the well-stirred/Windkessel/Starling physiology; bistable cell-fate
  landscapes (Waddington/Huang–Kauffman) and the reversion logic of differentiation therapy; the
  standard curative/systemic care of RCC and HCC (NOT derived here).
- **The framework's falsifiable additions (the burden of proof):** (i) the cell-fate escape barrier =
  γ²/4 read from the **measured** master-gene promoter stacking energy; (ii) the spinodal as a **sharp**
  irreversibility threshold with a ½ critical exponent; (iii) additive barrier decrements ⇒
  multiplicative synergy and its inverse (multiplicative de-escalation), which **retrodicts** the HBV/HCV
  bracketing and the HBV-control benefit in aflatoxin regions.
- **Weakest link ([O]/[H]):** no experiment yet links promoter stacking energy to a measured cell-fate
  barrier height. All therapeutic readings are **testable predictions / target hypotheses, not clinical
  guidance**.

---

## 3. OUT of circulatory's scope (owned by a sibling — do NOT re-emerge here)

| disease(s) | rightful owner | why |
|---|---|---|
| essential hypertension, shock, chronic heart failure | **homeostasis_hemodynamic** | regulated-setpoint (loop) dysregulation, not a clearance-organ dynamics failure |
| diabetes insipidus, SIADH, electrolyte / acid–base, nephrolithiasis | **homeostasis_ionic** | defended-setpoint loop dysregulation (ADH/mineral), not owned by a single organ |
| hereditary RCC (VHL), hereditary HCC predisposition (e.g. HFE haemochromatosis) | **disease_wp** | monogenic, gene-key entities (cross-reference both ways) |
| aristolochic-acid UUC (urothelial), AA-nephropathy | borderline (urothelium) | distinct tissue/master-gene; documented as cross-reference, not RCC |

> NOTE on §§10–19 (T8–T17). The current build contains hemodynamic/renal/hepatic single-knob disorder
> sections (arterial stiffening, hypertension, shock, DI/SIADH, CKD staging, autoregulation breakthrough,
> hepatic-impairment PK, shunt, DDI). Under the §6 contract these are **boundary demonstrations** of
> circulatory's *relations*, but the **diseases** belong to the homeostasis siblings above.
> **RESOLVED in v0.4.1 (option (a)):** each of §§10–19 now carries a one-line ownership banner
> (`<aside class="ownership-banner">`) naming the sibling owner and reframing the section as a perturbation
> of a circulatory relation, not a circulatory-owned disease. §§20–23 (RCC/HCC, circulatory-owned) and
> §§1–9 (physiology substrate) deliberately carry no banner. The banner text is also mirrored as a
> plain-text `owner_note` per chapter in `_meta.json` for machine/RAG consumption. A future pass may still
> elect option (b) — migrating the full disease framing into the owning homeostasis packages and keeping
> only the relation demonstrations here.

---

## 4. REMAINING work (next sessions) — priority order

1. ~~**Scope-tidy §§10–19** per §3 NOTE~~ — **DONE in v0.4.1.** Each of §§10–19 now carries an ownership
   banner (sibling owner + "shown here as a perturbation of the circulatory relation"); §§20–23 and §§1–9
   carry none; `owner_note` mirrored in `_meta.json`. The only scope ambiguity is removed. *(Next session:
   start at item 2.)*
2. ~~**Live-wire the cross-references**~~ — **DONE in v0.5.0.** The VHL→hereditary-RCC and HFE→hereditary-HCC
   gene-key references are now wired from a single source (`inherited/cross_references.json`, loaded by
   `inherited/cross_references.py`) into the research battery (`stress_tests.py` T22/T23, as structured
   `hereditary_*_cross_reference` records, not prose), the canonical pages (§22 VHL aside; §23 HFE aside,
   cited to Atkins JAMA 2020, HR 10.5), and `_meta.json` (per-chapter `cross_references`). SSOT preserved —
   the entities are *consumed*, not re-emerged; their barrier-height derivation stays owned by `disease_wp`.
   The **4-way HCC co-exposure product** is **marked ILLUSTRATIVE [H]** machine-explicitly
   (`oncology_roster.deescalation` now emits `combined_product_status`; surfaced in §23 and the ledger):
   no anchored ≥3-way simultaneous cohort exists, so the full product is a model extrapolation, not data —
   single agents and pairwise synergies remain the anchored results. *(Next session: start at item 5.)*
3. ~~**UUC as its own entity**~~ — **RESOLVED (deferred) in v0.5.0.** Decision: upper-tract urothelial
   carcinoma is **not** taken on as a circulatory-owned entity. Its master-gene γ (urothelium) is unmeasured
   in the DNA pipeline and its potency (OR up to 49) exceeds the smoking-calibrated kidney axis, so AA/UUC
   stays the documented cross-reference it is in §22, not a forced point on the RCC axis. Revisit only when
   the urothelial γ is measured.
4. ~~**CKD ownership decision**~~ — **DECIDED in v0.5.0.** Chronic kidney disease is **not** circulatory-owned.
   It is the downstream final-common-pathway readout of sibling etiologies — diabetic/hypertensive nephropathy
   (owned by the **homeostasis** siblings) and intrinsic age-related nephron loss (owned by **aging_senescence**).
   Circulatory retains §15 **only** as a demonstration of its renal autoregulation relation
   (total GFR = surviving-nephron fraction × the autoregulated per-nephron value). The §15 banner and
   `_meta.json` `owner_note` now state the decision (replacing the prior "pending" text).
5. **Empirical tests of the falsifiable core** — **PREP DONE in v0.6.0 (drop-in ready); measurement remains.**
   The three falsifiable predictions are now pre-registered and locked: `repro/_verify/predictions_registry.py`
   emits P1 (reversibility threshold = spinodal: h_sp 0.747 kidney / 0.725 liver), P2 (½ critical-slowing
   exponent), and P3 (cell-fate barrier = γ²/4: 0.605 / 0.581) — all FORCED from the vendored substrate, so
   byte-consistent with §§20–21/T18–T21 — each with an explicit falsification threshold and a candidate data
   source. `FALSIFICATION_PROTOCOL.md` is the pre-registration (hypothesis / measurement / falsification per
   prediction) with a No-Tuning acceptance rule; `run_all.py` section [6] surfaces the registry. **Remaining
   = the external measurement** (responder cohorts for P1/P2; a barrier-proxy-vs-γ assay for P3 — the weakest
   link). Status stays `[O]/[H]`/OPEN until a real anchored dataset passes; no fabrication.
6. **Publication registry** — **PREP DONE in v0.6.0 (one-line swap on DOI mint); registration remains.**
   Publication identifiers are now single-sourced in `manifest/publication.json` (`status:"pending"`,
   `doi/concept_doi/zenodo_record:null`, plus a `cross_volume_registry` pointer listing what this volume
   consumes from `disease_wp` and the seams it exports). `tools/build_docs.py` reads the DOI from there (null
   → "DOI: pending", byte-identical to before); `_meta.json` now carries `concept_doi`, `cross_volume_doi`,
   `publication_status`. **Remaining = mint the Zenodo record** and follow `publication.json` `swap_procedure`
   (set the fields, rebuild; `grep -r 'DOI: pending' docs/` returns nothing).

---

## 5. Reproduce / extend

```
python repro/run_all.py        # emergence + 23/23 stress battery + gate (must be all_green)
python tools/build_docs.py     # rebuild docs/ (refuses unless gate green and PHASE=writing)
```
Key files: engine `repro/_engine/vp_cir_engine.py`; oncology kernel
`repro/_oncology/carcinogen_dose_response.py`; therapeutics `repro/_oncology/barrier_therapeutics.py`;
roster `repro/_oncology/oncology_roster.py`; discriminants `repro/_verify/stress_tests.py`; site
generator `tools/build_docs.py`; open items `IRREPRODUCIBILITY_LEDGER.md`.

Discipline (non-negotiable): no new mechanism for a disease — only a named setting / cited drive on an
existing relation; contrast not curve-fit; honest grades; determinism 2×sha256; single-zip returns.
