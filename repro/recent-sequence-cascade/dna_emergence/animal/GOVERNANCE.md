# GOVERNANCE — the VP Recent-Sequence DNA-Emergence constitution

This document fixes the rules this volume is built under, so any reader can audit it against a stable standard rather than against taste. It is the DNA-face statement of the VP-SPEC discipline, inherited from the foundation, the Atlantic-opening volume, the Recent-Sequence Cascade (its sibling), and the **VP DNA interpretation method** whose instrument it uses.

---

## Article 1 — The question, and the occurrence cap

**1.1** This volume asks only what the **inherited material instrument** measures when applied to real NCBI genomes of "a past animal and a present animal" (mammoth/elephant; Neanderthal/modern human), and whether the **molecular clock** (the average theory's deep-time axis) is the same channel as the **material** or a different one.

**1.2 — Occurrence cap.** Any statement that a particular **history** between the two animals **occurred** — a flood between them, *or* a deep-time gradual descent between them — is capped at grade **[O] (open)**. No chain of reasoning here may raise *either* past-history claim above [O]. Only *present-tense measurement* and *mechanism* may be graded higher.

**1.3** Which history occurred is a separate, pre-registered question, decided by independent evidence, not by the material reading here. The reading establishes *present material kind* and *channel structure*, not chronology.

---

## Article 2 — The bidirectional chronology firewall

**2.1** Absolute chronology and any descent-history premise are **forbidden as load-bearing in both directions.** This volume neither asserts "recent / a flood" nor "deep time / gradual descent." Both are held as **open ([O])**.

**2.2 — Symmetry with the decoupling result.** The central empirical result (Article 5 data tier; Whitepaper §3) is that the molecular clock is **decoupled** from the material (r ≈ 0). This **cuts both ways**: it forbids promoting the clock into a material/age claim, *and* it forbids using the same decoupling to assert that a flood replaced descent. The decoupling demotes the *clock* as a history instrument; it does **not** elevate any alternative history. The firewall is therefore not rhetorical — it is forced by the data structure itself.

**2.3** The inherited DNA method is **explicitly silent on evolution and out-of-scope for phylogeny** by construction; it reads present-tense material only. This volume adopts that silence without modification and does not convert any material reading into a descent or age statement.

---

## Article 3 — Data grading (what may be load-bearing)

Genomic inputs are tiered by directness; only the top tiers may bear weight.

| Tier | Meaning | Load-bearing? |
|---|---|---|
| **G0** | a real, fetchable NCBI accession (a deposited sequence) | **yes (ACTIVE)** |
| **G1** | a deterministic, no-tuning read of G0 (γ from the LOCK table; a CDS extraction; a global alignment substitution count) | **yes (ACTIVE)** |
| **G2** | a model-light contrast of G1 quantities (per-gene gap/spread; cross-channel correlation) | yes (ACTIVE), flagged |
| **G3** | a literature cross-reference used only to *confirm* a G1 read (e.g. Campbell 2010 AA set) | corroboration only |
| **G4** | a model-dependent reconstruction (a tree, a calibrated clock, an inferred ancestral state, a divergence date) | **record only** |
| **G5** | an absolute date / molecular-clock age | **record only** |

A claim may be promoted to [F]/[V] only on G0–G2; **G4–G5 inputs are carried as record and never decide a grade.** The molecular-clock *count* used in §3 is a G1 read (a raw substitution tally over an alignment); the *interpretation of that count as an age* is G5 and is never load-bearing — that asymmetry is the whole point of the decoupling test.

---

## Article 4 — No-tuning, single substrate, inherited-instrument integrity

**4.1 — No-tuning.** No parameter is fitted to make a result come out. The material engine's only constants are the SantaLucia (1998) nearest-neighbour LOCK table, inherited unchanged; γ, the R19 spinodal and barrier are derived from it with no free parameter. SEED = 19 convention; every computation is deterministic and scripted.

**4.2 — Single substrate.** One engine — the **R19 jammed ⇄ unjammed bistable switch** — underlies every read: γ sets the switch threshold, the STATE face is the switch in two settings (MC1R caught in both), and the material conservation is the switch's substrate read across taxa. No new mechanism is introduced per phenomenon.

**4.3 — Inherited-instrument integrity.** The DNA reading is **not re-derived or re-tuned here**; it is vendored faithfully from the inherited method (DOI 10.5281/zenodo.20471407) and reproduces that method's behaviour and its archaic/modern precedent (< 0.0016 per-gene promoter conservation). Modifying the instrument would define a new method, not tune this one.

**4.4 — Build-then-grade, anti-contamination.** Each emergence is built first, then graded; honest qualifications are recorded at the end of each step, not used to retreat before the read is done. Where a read is an instrument artefact (the window-length effect), it is **stated in the open** and its scope (within-kind only) is bounded — without letting it contaminate the between-kind/cross-channel results it does not touch.

---

## Article 5 — Verdict scheme

| Grade | Meaning |
|---|---|
| **[F]** | forced / derived — follows from the LOCK table + the engine |
| **[V]** | verified — measured directly on a real accession, or reproduced by the SEED-fixed engine |
| **[L]** | leaning — a well-anchored inference / forward prediction, not yet forced |
| **[O]** | open — undecided; includes **all past-history claims in both directions** (Art. 1.2, 2.1) |

Precedence **[F] > [V] > [L] > [O]**. FAIL/INCONCLUSIVE are contagious: nothing downstream may cite a failed result as support, and nothing may launder an [O] occurrence claim into a higher grade.

---

## Article 6 — Reproducibility obligation

**6.1** Every load-bearing read is a runnable, SEED-fixed, no-tuning script over a **frozen real NCBI record**; every load-bearing observation is a fetchable accession. The mapping is given in `REPRODUCIBILITY_MAP.md`; the accessions in `repro/data/accessions.json`; the live re-fetch in `repro/fetch_ncbi.py`.

**6.2** The whole spine reproduces from `repro/run_all.py` with **no network** (it runs from the frozen GenBank records) and **no fitted parameter** (search the scripts: only the SantaLucia LOCK and SEED = 19 appear).

**6.3 — 반증 = 발견.** An honest negative is a finding. The two honest results here — that the *pooled* γ is **not** bimodal (only the per-gene partition is clean), and that within-kind γ-range is inflated by a **window-length artefact** — are recorded openly and their scope is bounded, not silently removed. They sharpen the instrument; they are part of the contribution, not hidden from it.

---

*These rules are fixed for this volume. A reader who disagrees with a grade can locate the exact article it rests on and the exact script + NCBI accession that backs it. The material reading speaks in the present tense and stays there; the history — flood or deep time — is held open by construction, in both directions.*
