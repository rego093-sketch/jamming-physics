# CHARTER — Integumentary Emergence: the Epidermal Barrier, Wound-Healing Unjamming, and the UV-Carcinogenesis Showcase

**paper_id:** `integumentary_vp_site`  ·  **code:** `skn`  ·  **branch:** jamming (barrier/interface + external insult)  ·  **version:** 1.0.0

## Scope (one line)
Epidermis, keratinocyte barrier, melanocyte photoprotection and appendages emerge as the body boundary; wound healing is a jamming->unjamming->re-jamming transition, and UV dose-response is the cleanest R19 carcinogenesis case.

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental order*
are owned by the DNA morphogenesis gene-clock and CITED here (measured γ, never fitted). Organs whose
γ is not yet in the DNA atlas are listed as honest **to-measure** inputs (fetch via the same pipeline)
— deferred, not invented.

### Organs
- **epidermis** (`TP63`) — γ=1.3643 (vendored, measured [V]) — stratified barrier: basal->cornified transit — *dyn:* barrier — *rate anchor:* epidermal turnover ~28-40 d [L] TO-ANCHOR
- **keratinocyte** (`KRT14`) — γ=1.4894 (vendored, measured [V]) — keratin barrier mechanics / structural integrity — *dyn:* barrier — *rate anchor:* barrier permeability (TEWL) [L]
  - **cell-adhesion binding jam (v0.7.0):** junctional adhesion as a **hysteretic two-state binding jam** on this *same* measured KRT14 γ (no new organ, no new fitted constant; desmosomes/hemidesmosomes anchor the keratin network, so adhesion is intrinsic to this organ — the hair-cycle pattern, not the sebaceous new-organ pattern) — discontinuous detachment at a lower spinodal, re-adhesion only at a higher one (loop width ≈ 2.01) [V]; adherent above the upper spinodal at net adhesion +1.4; reserve/titres [F]; absolute counts/titre/depth/BSA [O]. Two coupled compartments on the *same* γ and spinodal — cell-cell (DSG3) and cell-matrix (BP180) — with a *derived* Nikolsky sign. Additive layer `repro/_adhesion/` with its own gate.
- **melanocyte** (`MITF`) — γ=1.3945 (vendored, measured [V]) — melanin synthesis + UV photoprotection — *dyn:* defense — *rate anchor:* melanin UV-dose protection [L]
- **skin_appendage** (`EDAR`) — γ=1.3696 (vendored, measured [V]) — hair follicle / sweat gland (thermoregulation interface) — *dyn:* appendage — *rate anchor:* appendage identity [V]
  - **hair-follicle cycle (v0.5.0):** an emergent **relaxation oscillator** on this *same* measured EDAR γ (no new organ, no new fitted constant) — anagen-dominant, plateau-then-collapse waveform [V]; absolute fraction/period [O]. Additive layer `repro/_cycle/` with its own gate.
  - **neurovascular reactivity (v0.8.0 · T9):** cutaneous **vasomotor tone** as a **hysteretic two-lock reactivity jam** on this *same* measured EDAR γ (no new organ, no new fitted constant). The thermoregulation-interface organ carries two autonomic effector arms — the **sudomotor** arm (sweat, T5) and the **vasomotor** arm (skin blood flow); rosacea dysregulates the vasomotor arm, the *vascular mirror of hyperhidrosis* on the sudomotor arm, so it is intrinsic to this organ. The vessel **locks dilated** at the upper spinodal and **locks constricted** at the lower one (loop width ≈ 2.01) and is **responsive** in the reversible middle [V]; reversibility is a uniform consequence of *whether a drive crosses its lock*. Tone/reactivity/constrictor drives [F]; clinical mappings [L]; absolute erythema/vessel/temperature magnitudes [O]. **SSOT seam:** dermal-perfusion *magnitude* stays an inherited circulatory citation (only the reactivity dynamics is added). Additive layer `repro/_vasomotor/` with its own gate. *(dilated=jammed ON, constricted=OFF.)*
- **sebaceous_gland** (`PRDM1`) — γ=1.3432 (vendored, measured [V]; Blimp1, sebaceous-lineage master) — pilosebaceous duct occlusion — *dyn:* jamming — *rate anchor:* follicular-occlusion clinical anchor [L]
  - **sebaceous-duct jam (v0.6.0):** the duct as a **hysteretic two-state occlusion jam** on the *same* R19 switch (new measured organ) — discontinuous closure at an upper spinodal, reopening only at a lower one (loop width ≈ 2.01) [V]; occlusion set-points [F]; absolute lesion counts [O]. PRDM1 is the atlas's lowest γ → earliest spinodal (emergence-order prediction graded by sign [V]). Additive layer `repro/_seb/` with its own gate.

## Physical-class boundary (why these organs are one package)
Decomposition is by **physical regime / coupling topology**, not textbook organ-system labels. This
package is the **jamming (barrier/interface + external insult)** class. Anything outside that class belongs to a sibling package and
is reached only through the cited seam variables — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- circulatory: dermal perfusion (cited)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- barrier integrity + thermoregulation interface (systemic boundary)

### Seam manifest (v0.9.0 · additive)
The interfaces above are consolidated into one labelled, machine-readable record by the additive layer `repro/_seam/` — three honestly distinct classes: **INHERITED-IN** (the three cited inputs above, vendored never re-derived), **INTERNAL-LIVE** (the pigment-loss→oncology coupling, HANDOFF §5.3 — a melanocyte-target T3 lesion that removes the melanin screen raises the shared oncology-kernel hazard; numbers **re-exported verbatim** from the verified pathology layer, so the seam output provably *is* the internal link surfaced, not a parallel implementation), and **DECLARED-OUT** (the sibling-package contracts, flagged *declared, not yet live wiring* — the §5.3/§5.4 integration harness does not exist). No new mechanism, no new constant. Gate: `repro/_seam/seam_verify.py` → `seam_gate()` (re-export fidelity, coupling sign + causal lever, provenance + contract validity, non-disturbance); runner `repro/run_seam.py`.

## Discriminant targets (must pass before writing)
- T1 barrier permeability: transepidermal water loss crosses a diffusion threshold as the barrier thins [V], abs [O]
- T2 wound healing: injury -> unjamming -> collective migration -> re-jamming closure (jamming/unjamming) [V]
- T3 melanin UV response: UV dose raises melanin to a protective plateau (negative feedback) [V]
- T4 epidermal turnover: basal->cornified transit time matches the cited window [V], rate [L]
- T5 thermoregulation: appendage (sweat) response to a thermal load (interface flux) [V]

**Additive target (own gate, post-core — does not gate the core writing lock):**
- T6 hair-follicle cycle (v0.5.0): the EDAR appendage as a relaxation oscillator — oscillates, anagen-dominant, relaxation waveform, and the delayed-vs-immediate shedding dichotomy [V]; absolute anagen fraction + years-long period [O]. Gate: `repro/_cycle/cycle_verify.py` → `cycle_gate()`; runner `repro/run_cycle.py`.
- T7 sebaceous-duct occlusion (v0.6.0): the pilosebaceous duct (new measured PRDM1 organ) as a hysteretic occlusion jam — discontinuous closure at an upper spinodal, hysteretic reopening at a lower one, healthy-patent, and the reversible-vs-irreversible depth discriminant [V]; occlusion set-points [F]; absolute counts [O]; γ reproduces offline. Gate: `repro/_seb/seb_verify.py` → `seb_gate()`; runner `repro/run_seb.py`.
- T8 cell adhesion (v0.7.0): junctional adhesion on the *existing measured* KRT14 γ (no new organ, none fitted) as a hysteretic two-state binding jam — discontinuous detachment at a lower spinodal, hysteretic re-adhesion at a higher one, healthy-adherent, two compartments (cell-cell DSG3 / cell-matrix BP180) on the *same* γ and spinodal, a *derived* Nikolsky sign, and the three-axis opposite-property discriminant (plane / Nikolsky / tension) at the *same* antibody magnitude [V]; reserve/titres [F]; clinical mappings [L]; absolute counts/titre/depth/BSA [O]. Gate: `repro/_adhesion/adhesion_verify.py` → `adhesion_gate()`; runner `repro/run_adhesion.py`.
- T9 neurovascular reactivity (v0.8.0): cutaneous vasomotor tone on the *existing measured* EDAR γ (no new organ, none fitted — the thermoregulation-interface organ's vasomotor arm, the vascular mirror of the sudomotor T5 arm) as a hysteretic two-lock reactivity jam — discontinuous dilation lock at the upper spinodal, discontinuous constriction lock at the lower one, responsive in the reversible middle, reversibility a uniform consequence of *whether a drive crosses its lock*, and the three-axis opposite-property discriminant (vasodilation↔vasoconstriction / fixed↔reversible / vascular↔inflammatory) [V]; tone/reactivity/constrictor drives [F]; clinical mappings [L]; absolute erythema/vessel/temperature/BSA [O]. **Seam:** dermal-perfusion magnitude inherited from circulatory, not re-emerged. Gate: `repro/_vasomotor/vasomotor_verify.py` → `vasomotor_gate()`; runner `repro/run_vasomotor.py`.

## Domain diseases + oncology scope (carcinogen → incidence)
Covers this physical class's diseases; the carcinogen-exposure mechanism (how much MORE cancer with
exposure) uses the shared R19 kernel (barrier-lowering → Kramers crossing → RR(dose)) with per-site
CITED epidemiological anchors. Grades: anchor [L] / dose-response shape [V] / absolute incidence [O].
- **melanoma** ← UV radiation (cumulative + intermittent sunburn)
  - anchor/grade: cumulative-UV / sunburn RR for melanoma [L]; barrier-crossing dose-response [V]
- **squamous / basal cell carcinoma** ← UV radiation (cumulative)
  - anchor/grade: SCC near-linear with cumulative UV [L]; the clean R19 dose-response showcase [V]

**Hair-cycle diseases (v0.5.0, on the T6 oscillator — each a signed perturbation, no new constant):**
- **androgenetic alopecia** (anti-growth drive → anagen shortening / miniaturisation; minoxidil reverses) · anchor [L], direction/shape [V], absolute count [O]
- **alopecia areata** (sustained premature-catagen drive → anagen arrest; regrowth on removal, hysteresis) · anchor [L], shape [V], extent [O]
- **telogen effluvium** (transient stressor → synchronised telogen entry → shed one telogen later, self-limited) · anchor [L], delayed-shed shape [V], absolute latency [O]
- **anagen effluvium** (cytotoxic anagen-matrix insult → immediate shed, bypasses telogen; reversible) · anchor [L], immediate-shed shape [V], fraction [O]

**Sebaceous-duct diseases (v0.6.0, on the T7 occlusion jam — each a signed perturbation, no new constant):**
- **acne vulgaris** (standing high net occlusion → past the upper spinodal → inflammatory comedo; combined comedolytic + sebostatic + antimicrobial / isotretinoin reopens; de-inflame alone leaves a comedonal-but-jammed residue) · anchor [L], occlusion-jam direction + inflammatory branch + reopening shape [V], absolute lesion counts [O]
- **hidradenitis suppurativa** (the same jam in deeper apocrine follicles → plug rupture → scarring sinus-tract sub-state; biologics de-inflame but drive reduction does not reopen the ruptured tract — deroofing/excision resets it) · anchor [L], deeper-jam + rupture branch + drive-down irreversibility shape [V], Hurley extent [O]

**Cell-adhesion diseases (v0.7.0, on the T8 binding jam — each a signed de-adhesion, same antibody magnitude, no new constant):**
- **pemphigus vulgaris** (anti-DSG3 → the *cell-cell* compartment detaches → intraepidermal/suprabasal split, cell-matrix bond intact ("tombstone"); failing bond is lateral → shear propagates → **Nikolsky positive**, flaccid roof; partial titre reduction does not re-adhere, clearance (rituximab/immunosuppression) does) · anchor [L]; de-adhesion direction + intraepidermal plane + derived positive Nikolsky + hysteretic re-adhesion shape [V]; absolute counts/titre [O]
- **bullous pemphigoid** (anti-BP180 of the *same* magnitude → the *cell-matrix* compartment detaches → subepidermal split, cell-cell bonds intact (epidermis lifts whole); failing bond is basal not lateral → shear does not propagate → **Nikolsky negative**, tense roof; corticosteroid/immunosuppression re-adheres) · anchor [L]; de-adhesion direction + subepidermal plane + derived negative Nikolsky + hysteretic re-adhesion shape [V]; absolute counts/titre [O]
- *Boundary:* congenital **epidermolysis bullosa** (defective adhesion *gene* KRT14/COL17A1/LAMB3) is gene-keyed → the gene-lesion disease registry, not this dynamical layer.

**Vasomotor diseases (v0.8.0, on the T9 reactivity jam — each a signed vasomotor drive, opposite sign poles, no new constant):**
- **rosacea** (a standing vasodilator reactivity drive / lowered flush threshold carries the net dilator drive past the *upper* spinodal → the vessel locks dilated into persistent erythema and fixed telangiectasia; an early transient flush is a sub-lock excursion that still returns; the LL-37/Demodex inflammatory amplifier on the same dilated background gives the papulopustular subtype; anti-inflammatories clear the papules, brimonidine blanches transiently but does not reset the fixed vessels (hysteresis), laser/IPL resets the telangiectasia) · anchor [L]; vasodilation direction + discontinuous dilation lock + reversible sub-lock flush + papulopustular amplifier + hysteretic non-reset shape [V]; absolute erythema/vessel/BSA [O]
- **Raynaud phenomenon** (a cold/stress vasoconstrictor drive carries the net dilator drive negative into the constricted/ischemic basin → a reversible digital vasospastic attack; primary Raynaud crosses no lock and reverses on rewarming, a vasodilator / calcium-channel blocker aborts it) · anchor [L]; vasoconstriction direction (opposite pole) + reversible attack + vasodilator reversal shape [V]; absolute digital temperature/frequency [O]
- *Boundary:* the **fixed** digital ischemia / ulcer of **secondary Raynaud** (connective-tissue disease) is a downstream structural change → an immune/rheumatology sibling-package seam; the dermal-perfusion magnitude is an inherited circulatory seam — neither is re-emerged in this dynamical layer.

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and C1/C3 in research.
  Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and
  research signed off (START_HERE §5).
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state
  passes by files only, next session resumes from the single zip (C0, §1, §5).
