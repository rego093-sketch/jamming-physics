# CHARTER — Musculoskeletal Emergence: Muscle Actuation, Cartilage and Bone as Load-Bearing Jammed Matter

**paper_id:** `musculoskeletal_vp_site`  ·  **code:** `msk`  ·  **branch:** jamming (solid-mechanics / load-bearing)  ·  **version:** 0.7.0 (writing; physiology + oncology + 18-target disease battery + TREATMENT axis §21–§24 + inherited non-opioid ANALGESIC axis §25–§28 green — every owned disease now has root mechanism AND treatment, and every owned PAINFUL disease also carries its non-opioid analgesic logic, each documented as a 4-page cluster on a DNA-grounded substrate; §20 register completed)

## Scope (one line)
Skeletal muscle (the actuator neuro commands), cartilage and bone emerge as load-bearing structures on the jamming substrate; bone remodeling under mechanical load is a yield/jamming threshold (Wolff's law).

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental order*
are owned by the DNA morphogenesis gene-clock and CITED here (measured γ, never fitted). Organs whose
γ is not yet in the DNA atlas are listed as honest **to-measure** inputs (fetch via the same pipeline)
— deferred, not invented.

### Organs
- **skeletal_muscle** (`MYOD1`) — γ=1.4933 (vendored, measured [V]) — myogenic contraction: recruitment + force-frequency (the actuator neuro commands) — *dyn:* actuator — *rate anchor:* twitch->tetanus fusion freq [L] TO-ANCHOR
- **cartilage** (`SOX9`) — γ=1.4598 (vendored, measured [V]) — chondrocyte load-bearing matrix + growth plate — *dyn:* structural — *rate anchor:* growth-plate ossification timing [L]
- **limb_skeleton** (`TBX5`) — γ=1.4392 (vendored, measured [V]) — appendicular skeletal patterning (load-bearing scaffold) — *dyn:* structural — *rate anchor:* limb bud -> skeleton [V]
- **bone** (`RUNX2`) — γ=1.2414 (measured [V]; fetched this cycle from NC_000006.12, window TSS−2000..+500, MANE NM_001024630.4, via the identical DNA pipeline — never fitted) — osteoblast mineralization + load remodeling (Wolff = yield/jamming) — *dyn:* load-remodel — *rate anchor:* bone density vs load [L]

## Physical-class boundary (why these organs are one package)
Decomposition is by **physical regime / coupling topology**, not textbook organ-system labels. This
package is the **jamming (solid-mechanics / load-bearing)** class. Anything outside that class belongs to a sibling package and
is reached only through the cited seam variables — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- neuro: motor command -> muscle recruitment (cited; neuro owns the command)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- marrow cavity -> immune_hematologic_vp_site (hematopoiesis site seam)
- mechanical load / posture (systemic)

## Discriminant targets (PASS — physiology)
- T1 force-frequency: twitch summation -> fused tetanus at cited stimulation frequency [V], rate [L] — **PASS**
- T2 length-tension: active force vs sarcomere overlap reproduces the cited curve peak [V] — **PASS**
- T3 bone remodeling: sustained load raises density past a yield threshold (Wolff; jamming/yield) [F] — **PASS**
- T4 growth-plate: developmental threshold order ranked by gamma over measured organs [V] — **PASS**
- T5 fatigue: sustained drive -> reversible force decline with a cited time constant [V] — **PASS**

## Disease battery (PASS — cited-severity perturbations of the passing machinery)
Highest-value disease additions are PERTURBATIONS of an already-passing target or master switch, with a
**cited** severity (No-Tuning) and an honest grade; **PASS = reproduce the DIRECTION/SHAPE of the documented
clinical sign, never an absolute number.** Engine: `repro/_disease/vp_msk_disease.py`; reshaped for gate/docs
by `repro/_verify/stress_tests.py::run_disease_suite()`; the research gate now requires this battery green too.
- **T7a/b/c** master-gene dosage dysplasias — CCD (RUNX2), campomelic (SOX9), Holt-Oram limb (TBX5): a 0.5
  haploinsufficiency drops the switch below a **γ-independent crossing cliff at ⅔ of WT drive** → failed/partial
  crossing. Mechanism [V]; threshold shift [F]; absolute timing/morphology [O]. (**T7d** MYOD1 = secondary [V?], excluded from the hard gate.)
- **T6 / T6b** mechanostat disease — disuse/post-menopausal osteoporosis is the exact MIRROR of T3 (sub-threshold
  load lowers the dense-basin barrier; loss rate rises with unloading) [F]; osteopetrosis removes the loop's
  down-branch (density locked high) [V]. Frost setpoint [L]; absolute BMD %/month [O].
- **T8 / T8b** neuromuscular transmission — myasthenia gravis: raised NMJ threshold → low-frequency force
  decrement >10% (RNS), monotone in lesion [V]; Lambert-Eaton: presynaptic deficit → high-frequency increment
  (opposite sign) [V]. Clinical sign [L]; high-freq potentiation not modelled [O].
- **T10** metabolic / mitochondrial myopathy — perturbs T5: shorter fatigue τ (faster decline) + incomplete
  recovery (recovered fraction < 0.95) [V]; anchor [L]; absolute magnitude [O].
- **T9** osteoarthritis — cartilage unjamming: a **cited Paris/Basquin** cyclic fatigue-damage law (m=2) on the
  T2 contact number; sub-threshold protected, loss convex in load+BMI [V]; damage-law form [L]; absolute rate [O].
- **T4-ext** achondroplasia & chondrodysplasias — FGFR3-GOF as a suppressive drive on the SOX9 growth-plate
  switch → graded shortening ladder with a cliff [V]; absolute long-bone length [O].
- **Out-of-class & material register (docs §20)** — material diseases (OI, EDS/Marfan, renal osteodystrophy)
  and signatureless ones (Paget, scoliosis/DDH/clubfoot) carried as honest [O]; degenerative disc disease left
  as a one-function reuse of the §12/§17 cyclic-fatigue kernel rather than a duplicate page (NOT [O], not a
  capability gap); autoimmune (RA/AS/PsA), crystal (gout), pain (fibromyalgia), infection (septic arthritis)
  and distant-primary bone-mets ROUTED to sibling volumes via named seams — never re-emerged (SSOT).
  (Tendinopathy is now implemented in §17 [V], moved out of this register.)

- **T11 muscular dystrophy (DMD/BMD)** — dystrophin loss = mechanical fragility → a Paris/Basquin cyclic
  fatigue on the contractile contact number; the reading-frame rule (Monaco 1988) sets severity (DMD null <
  BMD partial < normal), NON-recovering (distinct from T5/T10) [V]; reading-frame ordering [L]; timeline [O].
- **T12 channelopathies (myotonia / periodic paralysis)** — perturb the FHN excitability directly: myotonia
  RAISES the depolarization-block threshold (hyperexcitable, repetitive discharge), periodic paralysis LOWERS
  it (a small depolarizing shift silences the fibre) — opposite signs like MG/LEMS, monotone in the defect [V].
- **T13 stress fracture + fracture healing** — bone has a fatigue ENDURANCE LIMIT below the T4 yield; cyclic
  sub-yield load above it fractures (S-N), sub-endurance is protected; and the fracture HEALS (load re-crosses
  the switch to the dense basin), a contrast with non-healing cartilage [V]; cycles-to-fracture [O].
- **T14 tendinopathy** — the OA cyclic-fatigue kernel on a tendon collagen contact number: sub-threshold
  protected, loss convex in overuse [V]; absolute rate [O]. (Moved from the material-[O] register.)
- **T15 sarcopenia** — gradual multi-axis ageing decline (motor-unit dropout × fibre atrophy × shorter fatigue
  τ): max force falls and fatigue onsets earlier together [V]; absolute force/rate [O].
- **T16 osteomalacia / rickets** — a MINERALIZATION CEILING: density = matrix occupancy × mineral supply, so
  deficiency caps density even under load; the decisive discriminant is that LOAD rescues osteoporosis but NOT
  osteomalacia (mineral is missing) [V]; absolute mineral density [O].
- **T17 osteolytic bone disease (myeloma / giant-cell tumour)** — osteoclast/osteoblast UNCOUPLING on the
  mechanostat: myeloma disables the formation arm (locked lytic = the MIRROR of osteopetrosis), giant-cell
  tumour's RANKL drive resorbs even dense bone [V]; absolute lesion size/incidence [O]. Modelled here (T3/T6),
  NOT via the carcinogen kernel, because the bone lesion is a remodeling-uncoupling, not a dose-response.

## Analgesic axis (PASS — inherited non-opioid three-lever technique applied to owned painful diseases)
**Adds no new physics and no new organ.** It INHERITS the three-lever non-opioid analgesic technique from the
VP non-opioid analgesic volume (**concept DOI 10.5281/zenodo.20733420**, cited and reused verbatim, exactly as the
R19/FHN primitives are vendored) and applies it to the painful diseases this package already owns. Pain is a
**threshold-crossing (Kramers) rate on the same R19 barrier ΔV = γ²/4** the diseases perturb: a noxious drive h
erodes the barrier and the nociceptor fires at rate ≈ exp(−ΔV_eff/D), ΔV_eff = max(0, γ²/4 + ΔV_L1 − κ·h). The
drive h is **READ from each disease kernel's own cited severity** (single source; never tuned to a pain score).
Engine: `repro/_disease/vp_msk_analgesia.py` (reuses `vp_msk_disease.py` verbatim, **never touches the engine** —
the determinism hash is unchanged); reshaped by `repro/_verify/stress_tests.py::run_analgesia_suite()`; the research
gate now also requires `analgesia_all_inscope_levers_direction_ok`.
- **Three levers** — **L1** raise the peripheral threshold (ΔV_L1↑→rate↓; local anaesthetics / Na_v blockers,
  topicals; structure-**DECOUPLED**) · **L2** lower the noxious drive (h↓→rate↓; NSAIDs + the musculoskeletal special
  case, **mechanical unloading**; structure-**COUPLED**) · **L3** reduce the central gain (g↓; gabapentinoids/SNRIs —
  **central gain is owned by neuro/mind, named as a SEAM and never re-emerged here, SSOT**). Opioids are a fourth
  descending/μ lever, outside the non-opioid logic and not modelled.
- **Decisive falsifiable discriminant** — L2 lowers BOTH the crossing rate AND the disease's own structural loss
  (coupled), while L1 lowers the rate but leaves the lesion FLAT (decoupled). That contrast is a real prediction the
  kernel makes and could fail — proof the axis is a grounded kernel, not a relabelling. Each lever is a monotone
  sweep (intensity 0→1); PASS = the crossing rate falls monotonically by DIRECTION (No-Tuning); the real drug/load
  is the cited **[L]** anchor for WHICH lever it pulls.
- **Ax-T9 osteoarthritis / Ax-T14 tendinopathy / Ax-T13 stress fracture / Ax-T17 osteolytic bone** — 4 scored
  painful diseases PASS with the L2-coupled / L1-decoupled cross-check holding.
- **Ax-T15 exertional / overuse muscle pain** — L1 and L2 lower the crossing rate by DIRECTION, but there is no
  discrete contact-loss lesion to run the cross-check → graded DIRECTION-only (honest partial), logged and excluded
  from the hard gate.
- **Honestly out of scope (results, not failures; obstacles in `IRREPRODUCIBILITY_LEDGER.md`):** L3 central gain
  (neuro/mind seam), the opioid lever (outside the non-opioid technique), and neuropathic / fibromyalgia / central
  sensitisation (routed to sibling volumes, as in §20).
- **Applied to existing cases:** each owned painful disease chapter (§12, §14, §16, §17, §19) carries an
  "Analgesic lever map (cross-reference)" block naming its lever classification and linking to §25–§27 (SSOT — the
  levers are emerged once in §25–§28; the disease chapters only cross-reference, never re-derive).

## Domain oncology scope (carcinogen → relative risk)
Covers this physical class's diseases; the carcinogen-exposure mechanism (how much MORE cancer with
exposure) uses the shared R19 kernel (barrier-lowering → Kramers crossing → RR(dose)) with per-site
CITED epidemiological anchors. Grades: anchor [L] / dose-response shape [V] / absolute incidence [O].
- **osteosarcoma** ← ionizing radiation (therapeutic/occupational) — radiation RR [L]; link WEAK → mostly genetic [O]
- **soft-tissue sarcoma** ← ionizing radiation; some chemicals — radiation RR [L]; chemical channel baseline-only [O]
- **chondrosarcoma** ← IDH1/2 neomorphic 2-HG (metabolic, not environmental) — SHAPE only [V]; no dose anchor [O]
- **Ewing sarcoma** ← EWSR1-FLI1 fusion (genetic, not environmental; cell-of-origin debated) — SHAPE only [V]; lineage + dose anchor [O]

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and C1/C3 in research.
  Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and
  research signed off (START_HERE §5).
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state
  passes by files only, next session resumes from the single zip (C0, §1, §5).
