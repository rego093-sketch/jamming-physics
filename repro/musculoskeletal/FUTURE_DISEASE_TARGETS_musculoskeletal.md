# FUTURE DISEASE TARGETS — Musculoskeletal (post-v0.4.1 roadmap)

**paper_id:** `musculoskeletal_vp_site` · **code:** `msk` · status: **18-target disease battery IMPLEMENTED through v0.4.0 (waves 1–3); v0.4.1 completes the §20 out-of-class/material register (scoliosis + degenerative disc disease recorded) and clears §14→§20 pointers; v0.5.0 adds the full TREATMENT axis — every owned disease now has root mechanism AND treatment, as the mirror operation on the same kernel; v0.6.0 documents it as a 4-page cluster (§21 methodology + DNA grounding, §22 bone/cartilage, §23 muscle/neuromuscular, §24 honest limits) under VP-SPEC v1.8 (answer-first, per-section SEO keywords); v0.7.0 INHERITS the non-opioid three-lever analgesic technique (concept DOI 10.5281/zenodo.20733420) and applies it to the owned painful diseases as a second 4-page cluster (§25 methodology, §26 L2 convergence, §27 L1 coupled/decoupled discriminant, §28 limits + central-gain seam), with per-disease cross-reference blocks on §12/§14/§16/§17/§19 — engine hash unchanged; this file tracks what is done vs the remaining backlog**
**Author:** Young Jae Lee (ORCID 0009-0002-7535-8245) · CC BY 4.0
**Governance:** same as the kit — VP-SPEC v1.8, No-Tuning, honest grades [F]/[V]/[L]/[O], every [O] needs
a stated obstacle, discriminant targets must PASS before any disease claim is written.

> **What changed since v0.2.0.** The disease battery proposed in the previous version of this file has been
> built, validated and written. Engine: `repro/_disease/vp_msk_disease.py` (11 targets, all PASS, deterministic
> 2×sha256 identical). Reshaped for the gate/docs by `repro/_verify/stress_tests.py::run_disease_suite()`. The
> research gate (`repro/_verify/gates.py`) now requires the disease battery green in addition to physiology +
> oncology. Pages §8–§20 are emitted into `docs/`. Two oncology sites (chondrosarcoma, Ewing) were added to
> `repro/_oncology/carcinogen_dose_response.py`. The rows below are annotated **✓ DONE** or **▢ BACKLOG**.

---

## 0. Coverage verdict (updated for v0.3.0)

**What v0.2.0 tested.** Five PHYSIOLOGY discriminants (T1–T5) + an ONCOLOGY dose-response for two tumour sites.

**What v0.3.0 adds.** A **disease battery** of cited-severity PERTURBATIONS of that passing machinery — 11 hard
targets across the four master switches and T1/T2/T3/T4/T5 — plus two more oncology sites. Every disease PASS
means the model reproduced the **direction/shape** of the documented clinical sign from a **cited** severity, never
an absolute number (No-Tuning). All deterministic.

**Implemented this cycle (✓):** T7a/b/c/d master-gene dosage dysplasias · T6 disuse/post-menopausal osteoporosis ·
T6b osteopetrosis · T8 myasthenia gravis · T8b Lambert-Eaton · T10 metabolic/mitochondrial myopathy · T9
osteoarthritis (cartilage unjamming, cited Paris/Basquin law) · T4-ext achondroplasia & chondrodysplasias ·
oncology extensions chondrosarcoma (SOX9) and Ewing (EWSR1-FLI1) · the out-of-class & material register (docs §20).

**Design principle (unchanged, and validated).** The highest-value additions were NOT new physics — they were
perturbations of already-passing machinery. That principle held: 10 of 11 hard targets needed **no new mechanism**
(only OA added one small CITED damage law), and all reproduced their clinical signatures.

---

## 1. Master-gene DOSAGE diseases — ✓ DONE (the headline γ-switch falsification)

Implemented in `vp_msk_disease.py::t7_master_gene_suite()`. Key result: a 0.5 haploinsufficiency drops the switch
drive below a **γ-independent crossing cliff at ⅔ of WT drive** (because the WT switch is driven at 1.5× its
spinodal; 0.5×1.5 = 0.75 < 1 spinodal), so the heterozygous switch cannot release from the OFF basin — occupancy
collapses from 1.00 (WT) to ≈0.10 and the crossing latency becomes undefined. Page: docs §8.

| ID | disease | master (organ) | status | grade as built |
|---|---|---|---|---|
| **T7a** | Cleidocranial dysplasia (CCD) | **RUNX2** (bone) | ✓ DONE (primary) | mechanism [V]; threshold shift [F]; absolute timing/morphology [O] |
| **T7b** | Campomelic dysplasia | **SOX9** (cartilage) | ✓ DONE (primary) | mechanism [V]; threshold shift [F]; absolute morphology [O] |
| **T7c** | Holt-Oram (limb component) | **TBX5** (limb_skeleton) | ✓ DONE (primary; cardiac part routed out) | mechanism [V]; threshold shift [F]; absolute pattern [O] |
| **T7d** | MYOD1-related myogenic myopathy | **MYOD1** (skeletal_muscle) | ✓ DONE (**secondary**, excluded from hard gate) | mechanism [V?]; mostly [O] |

T7a–c are the primary 3-of-4 master-gene falsification suite (hard gate). T7d passes the same cliff but is held
SECONDARY because human MYOD1 loss-of-function disease is rare/recent.

---

## 2. Mechanostat / bone-density diseases — ✓ DONE (extend T3)

Implemented in `t6_disuse_osteoporosis()` and `t6b_osteopetrosis()`. Page: docs §9.

| ID | disease | status | grade as built |
|---|---|---|---|
| **T6** | Disuse & post-menopausal osteoporosis | ✓ DONE — the exact mirror of T3: sub-threshold load lowers the dense-basin escape barrier; rel. loss rate rises 1.00→2.59× from maintenance to complete unloading | mirror of T3 [F]; Frost setpoint [L]; absolute BMD %/month [O] |
| **T6b** | Osteopetrosis | ✓ DONE — disable resorption (remove the loop's DOWN-branch) → density locked high on unloading (normal returns to 0.0, petro stays 1.0) | mechanism [V]; brittleness/material [O] |
| — | Paget's disease | ▢ BACKLOG — disorganised runaway cross-basin cycling; no clean single-switch signature. Recorded as honest [O] in docs §20 (register), not emerged. | [O] |
| — | Renal osteodystrophy / osteomalacia | ▢ BACKLOG — mineralization-supply defect, outside switch-threshold scope. Recorded as [O] in docs §20. | [O] |

---

## 3. Activation & fatigue diseases — ✓ DONE (perturb T1 / T5)

Implemented in `_nmj_train()` (T8/T8b) and `_fatigue_metabolic()` (T10). Pages: docs §10, §11.

| ID | disease | status | grade as built |
|---|---|---|---|
| **T8** | Myasthenia gravis (MG) | ✓ DONE — raised NMJ threshold → 18.4% force decrement at 3 Hz (> 10% RNS line), monotone in lesion severity | T1 perturbation [V]; clinical threshold [L]; high-freq potentiation not modelled [O] |
| **T8b** | Lambert-Eaton (LEMS) | ✓ DONE — presynaptic deficit + facilitation → +46.7% increment at 50 Hz (opposite sign to MG), 0% low-freq decrement | T1 perturbation [V]; clinical sign [L] |
| **T10** | Metabolic / mitochondrial myopathy | ✓ DONE — T5 with shorter τ (60→25 s) + non-recovering residual → recovered fraction 0.835 < 0.95 | T5 perturbation [V]; anchor [L]; magnitude [O] |
| — | Sarcopenia | ▢ BACKLOG — fewer motor units + fibre atrophy; absolute max force is not fixed by the substrate ([O]-ish). Candidate as a graded multi-axis decline (motor-unit count × T5 τ × T2 contact number). | [O] |

---

## 4. Cartilage / joint load-bearing failure — ✓ DONE (jamming-rich, one cited law)

Implemented in `_oa_contact_loss()` (T9) and `t4ext_achondroplasia()` (T4-ext). Pages: docs §12, §13.

| ID | disease | status | grade as built |
|---|---|---|---|
| **T9** | Osteoarthritis (OA) | ✓ DONE — cyclic-fatigue unjamming of the T2 cartilage contact number via a CITED Paris/Basquin damage law (m=2): sub-threshold protected, matrix loss convex in load+BMI (0.036 → 0.256 → 0.676) | shape [V]; damage-law form [L]; absolute progression rate A [O] |
| **T4-ext** | Achondroplasia & chondrodysplasias | ✓ DONE — FGFR3-GOF = suppressive drive on the SOX9 growth-plate switch → graded shortening ladder with a cliff (WT 1.00 → achondroplasia 0.09 → thanatophoric 0.04) | mechanism [V]; absolute long-bone length [O] |

---

## 5. Connective-tissue / MATERIAL diseases — ▢ BACKLOG (honest [O], registered in docs §20)

Still in the kit's already-open absolute-material region; carried as honest [O] with obstacles in
`IRREPRODUCIBILITY_LEDGER.md` and listed in docs §20, **not** forced into a claim.

- **Osteogenesis imperfecta (COL1A1/2)** — ▢ qualitative "lower yield threshold" [V?]; quantitative brittleness [O].
- **Ehlers-Danlos / Marfan (collagen, fibrillin)** — ▢ connective-tissue laxity; material compliance [O].
- **Tendinopathy** — ✓ RESOLVED in §17 (T14): the OA Paris/Basquin cyclic-fatigue kernel on a tendon collagen
  contact number gives a verified SHAPE [V]; only the absolute rate is [O]. Moved out of this material-[O] list.
- **Scoliosis / developmental dysplasia of the hip / clubfoot** — ▢ 3-D structural/developmental deformities; no
  clean single-switch signature → honest [O], registered §20 (same category as Paget).
- **Degenerative disc disease** — ✓ available as a one-function reuse of the §12/§17 Paris/Basquin kernel on a
  disc contact number; SHAPE [V]-capable, rate [O]. Deliberately NOT given a duplicate page (SSOT); recorded §20
  as an explicit de-duplication, not an [O] gap.

---

## 6. Oncology extensions — ✓ PARTIALLY DONE

Implemented in `carcinogen_dose_response.py::SITES` (now four sites). Page: docs §7 extended.

| site | status | grade as built |
|---|---|---|
| **Chondrosarcoma** (SOX9 lineage; IDH1/2) | ✓ DONE — mapped to the SOX9 chondrocyte switch; aetiology is metabolic (2-HG), so the dose axis is the NORMALISED drive and there is no exposure anchor | SHAPE [V]; no environmental dose anchor + absolute incidence [O] |
| **Ewing sarcoma** (EWSR1-FLI1 fusion) | ✓ DONE — fusion-driven; cell-of-origin debated, so RUNX2 is a bone-mesenchyme context stand-in only | SHAPE [V]; lineage assignment + dose anchor + incidence [O] |
| **Multiple myeloma bone disease** | ▢ BACKLOG — osteoclast/osteoblast uncoupling; couples to the T3/T6 remodelling axis (not the carcinogen kernel). Better modelled as a perturbation of the T6 mechanostat than as a dose-response. | — |
| **Giant-cell tumour of bone** (RANKL-driven) | ▢ BACKLOG — osteoclast-recruitment axis; same T3/T6 coupling note. | — |

---

## 7. Explicitly OUT of the physical class — ✓ DONE as routing (docs §20), do NOT re-emerge (SSOT)

These are routed to sibling volumes via a named seam and listed (not emerged) in the out-of-class register, docs
§20. This is the SSOT-correct treatment and is considered **complete** as routing.

| disease | true owner | seam cited | status |
|---|---|---|---|
| RA, ankylosing spondylitis, psoriatic arthritis (autoimmune) | immune/inflammatory | immune-attack-on-joint | ✓ routed (docs §20) |
| Gout / pseudogout (crystal/metabolic) | metabolic sibling | crystal-deposition | ✓ routed (docs §20) |
| Fibromyalgia, chronic MSK pain | neuro / mind | nociception | ✓ routed (docs §20) |
| Bone metastases (breast/prostate/lung) | primary-tumour sibling + bone | metastasis-to-bone | ✓ routed (docs §20; bone microenvironment is in-class, primary is not) |
| Septic arthritis / osteomyelitis (infection) | infectious sibling | pathogen-load | ✓ routed (docs §20) |

---

## 8. Implementation notes — DONE (kept for provenance / future sessions)

All five wiring steps from the previous version were executed:

1. **Wired as perturbations** in `repro/_disease/vp_msk_disease.py` (a separate `_disease/` package, not edits to
   `_engine/`), exactly as specified: T7 = master-drive scaling past the spinodal cliff; T6 = T3 settle below
   threshold + barrier-lowering loss rate; T8 = depression+facilitation NMJ re-running the T1 force train; T10 =
   shorter T5 τ + incomplete-recovery residual; T9 = cited Paris/Basquin damage law on the T2 contact number.
2. **Suites added** via `stress_tests.py::run_disease_suite()` (standard target/disease/perturbs/status/value/
   grade/cited_severity/obstacle_if_open/detail schema; reshapes the disease engine for gate + docs).
3. **No-Tuning, hard** — severities are CITED (haploinsufficiency = 0.5; Frost MES; RNS > 10%; Paris/Basquin m=2).
4. **Honest negatives** — all absolute quantities (incidence, BMD %/month, long-bone length, material strength,
   developmental timing) are graded [O] with obstacles in `IRREPRODUCIBILITY_LEDGER.md`.
5. **Writing gated** — `gates.research_gate()` now also requires `disease_all_targets_pass`; the gate was re-signed,
   `PHASE=writing`, and `tools/build_docs.py` emitted one page per disease cluster (docs §8–§20).

---

## 9. Remaining backlog (after waves 1–3, v0.4.0)

Waves 2 and 3 cleared the major clinical gaps. **Done since v0.3.0:** T11 muscular dystrophy (DMD/BMD,
reading-frame severity), T12 channelopathies (myotonia + periodic paralysis), T13 stress fracture + fracture
healing, T14 tendinopathy, T15 sarcopenia, T16 osteomalacia/rickets (mineralization ceiling), T17 osteolytic
bone disease (myeloma + giant-cell tumour, osteoclast/osteoblast uncoupling). Engine: `repro/_disease/
vp_msk_disease.py` (18 targets, all PASS, deterministic 2×sha256 identical); pages docs §8–§19; register §20.

**Honest coverage verdict.** The major musculoskeletal disease space is now broadly covered:
- **Muscle** — essentially complete: NMJ (MG/LEMS), metabolic/mitochondrial myopathy, muscular dystrophy,
  channelopathies, sarcopenia, tendinopathy.
- **Bone density / remodeling** — complete for the major diseases: osteoporosis, osteopetrosis, osteomalacia/
  rickets, osteolytic (myeloma/GCT), stress fracture + healing, and the dysplasias (CCD, achondroplasia).
- **Cartilage / joint** — osteoarthritis; the inflammatory/crystal arthritides are correctly OUT of class (§7/§20).
- **Oncology** — four sarcoma sites (osteo-, soft-tissue, chondro-, Ewing).

**What genuinely remains (lower-value or honest [O]):**
1. **Osteogenesis imperfecta / Ehlers-Danlos / Marfan** — material-constant diseases (brittleness, laxity); stay
   [O] unless a cited matrix-yield law is adopted. (Registered §20.)
2. **Paget's disease** — disorganised runaway cross-basin cycling; no clean single-switch signature → [O]. (§20.)
3. **Degenerative disc disease** — available NOW via the existing OA/tendinopathy Paris/Basquin kernel applied to
   an intervertebral-disc contact number (a near-duplicate of T9/T14); deliberately not added as a separate page
   to avoid a third identical-kernel tissue (SSOT), but it is a one-function reuse if wanted. Touches the
   posture/load seam. **Now recorded in §20** as a deliberate de-duplication — explicitly NOT [O], not a capability gap.
4. **Scoliosis, developmental dysplasia of the hip, clubfoot** — 3-D structural/developmental deformities with no
   clean single-switch signature → honest [O]. **Now recorded in §20** (same category as Paget) and in the ledger.
5. **Congenital/rare myopathies, rhabdomyolysis** — rare or acute-threshold cases; low marginal value.
6. **Inflammatory myopathies (poly-/dermatomyositis), septic arthritis, gout, RA/AS/PsA, bone metastases,
   fibromyalgia** — CAUSE is in another physical class; correctly ROUTED to sibling volumes (§20), not re-emerged.

**One-line summary:** through v0.4.1 the kit covers the major musculoskeletal disease space across muscle, bone
and cartilage as cited-severity perturbations of passing machinery; the residue is material-constant [O]
(OI/EDS/Marfan), signatureless [O] (Paget, scoliosis), a one-function reuse (disc degeneration), or correctly
out-of-class — no new physics is required for any of it, and all of it is now recorded in the §20 register or routed.
**v0.5.0 adds the treatment axis (§21):** treatment = the MIRROR of disease on the same kernel (raise the barrier /
restore the drive across the spinodal / re-enable the disabled branch / refill the capped supply). 13 reversible
mirror treatments restore the healthy attractor by DIRECTION (No-Tuning), each citing the real drug or load for
WHICH knob it targets; the honest negatives — developmental dosage cliffs (T7), cartilage regeneration (OA),
established-tumour cytotoxic therapy (oncology; prevention is [V]), and general metabolic myopathy (T10) — are
graded [O] with a stated obstacle. The treatment battery is a separate module that reuses the disease kernels, so
the engine determinism hash is unchanged (7cf99d3baa26).
