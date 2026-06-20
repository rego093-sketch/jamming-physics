# CHARTER — Special-Sense Organ Dynamics: Ocular Optics, Cochlear Frequency Analysis, and Vestibular Balance

**paper_id:** `sensory_organ_vp_site`  ·  **code:** `sns`  ·  **branch:** physical (sense-organ instrument physics + R19 transduction)  ·  **version:** 0.4.0-published
**DOI:** 10.5281/zenodo.20755154 (concept; resolves to the latest version). Living version: https://jamming-physics.org/sensory-organs/ .

## Scope (one line)
The special-sense ORGANS as physical instruments: ocular optics/accommodation, the cochlear basilar-membrane frequency map, vestibular inertial sensing, and taste/olfaction chemodetection. Organ optics/acoustics are CLASSICAL physics (documented, linked); the R19 substrate handles the cellular transduction switch. neuro owns transduction->spike. Cataract, glaucoma, AMD, presbycusis are the disease axis.

## What this package emerges and circulates
Primary objects are LOOPS / OSCILLATORS / sense-organ instruments — node identity + order are owned by
DNA (measured γ, never fitted); nodes whose γ is not yet in the atlas are honest **to-measure** inputs.
It re-emerges NO organs owned elsewhere; it cites the seams below (SSOT) and adds its own dynamics.

### Nodes
- **eye_retina_optics** (`PAX6`) — γ=1.511 (vendored, measured [V]) — retinal photoreceptor mosaic + the ocular dioptric system (optics classical; switch R19) — *dyn:* sensor — *anchor:* refraction / accommodation [L]; PAX6 measured
- **eye_photoreceptor** (`RAX`) — γ=1.4541 (vendored, measured [V]) — photoreceptor phototransduction switch (R19 cellular) — *dyn:* sensor-switch — *anchor:* phototransduction threshold [L]
- **cochlea_frequency_map** (`EYA1`) — γ=1.3638 (vendored, measured [V]) — basilar-membrane tonotopic frequency analysis (mechanics classical; switch R19) — *dyn:* sensor — *anchor:* tonotopic place-frequency map [L]; EYA1 measured
- **inner_ear_haircell** (`SOX2`) — γ=1.4573 (vendored, measured [V]) — cochlear/vestibular hair-cell mechanotransduction (R19 switch) — *dyn:* sensor-switch — *anchor:* mechanotransduction threshold [L]
- **vestibular_balance** (`(vestibular_system)`) — no single master gene (circuit/derived/diffuse) — semicircular-canal + otolith inertial sensing (balance) — *dyn:* sensor — *anchor:* vestibulo-ocular reflex gain [L]; circuit
- **taste_chemodetection** (`TAS1R3`) — γ=1.5555 (vendored, measured [V]) — taste receptor chemodetection (sweet/umami; bitter via TAS2R) — *dyn:* sensor — *anchor:* taste detection threshold [L]; TAS1R3 measured

### Seams IN (inherited / cited)
- neuro: transduction->spike->brain is neuro's; this pkg hands off the transduced signal (cited)
- circulatory: ocular / cochlear perfusion (cited)
- circadian: retinal light also feeds the master clock (seam to circadian)
- DNA: identity + order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- transduced sensory signal -> neuro (this pkg is SSOT for the organ-physics stage)
- retinal light -> circadian_vp_site (entrainment input)

## Research program (excavated)

The special-sense ORGANS as physical instruments. CRITICAL honest boundary: the organ-level OPTICS and
ACOUSTICS are partly CLASSICAL physics (the lensmaker / dioptric equations, basilar-membrane resonance,
semicircular-canal fluid dynamics) -- this package DOCUMENTS and LINKS those, it does NOT re-derive them
from R19. The R19/FHN substrate handles the CELLULAR transduction switch (photoreceptor, hair cell,
chemoreceptor). neuro owns transduction->spike->brain; this package owns the organ-physics stage BEFORE
the spike. The seam to neuro is where the transduced signal is handed off.

- **RS1** Ocular optics (CLASSICAL): accommodation focuses the dioptric system onto the retina; refractive
  error is a focal-length/axial-length mismatch. *Handling:* documented from classical optics + cited,
  linked not re-derived. [cited]
- **RS2** Phototransduction (R19): the photoreceptor is an R19 switch -- light past threshold flips the
  cell. *Discriminant:* the transduction threshold and the switch dynamics. [V], threshold [L].
- **RS3** Cochlear frequency analysis: the basilar membrane maps frequency to PLACE (tonotopy; a resonant
  filter bank -- mechanics CLASSICAL) and the hair cell mechanotransduces (R19 switch). *Discriminant:* the
  place-frequency map [cited] + the hair-cell switch [V].
- **RS4** Vestibular balance: semicircular canals sense angular acceleration, otoliths sense linear; the
  vestibulo-ocular reflex stabilizes gaze. *Discriminant:* the VOR gain; canal fluid dynamics classical. [V].
- **RS5** Chemodetection: taste / olfaction receptor activation as a threshold crossing (R19). *Discriminant:*
  detection threshold and concentration-response. [V], threshold [L].
- Grades (C3): cellular transduction switch [V]; cited thresholds/maps [L]; organ optics/acoustics are
  CLASSICAL (cited, not an R19 claim) -- this honesty is part of the scope.

## Deepened research (v0.2.0 — excavation BELOW the organ, to the molecule)

The v0.1 charter stopped at "the transducer is an R19 switch." v0.2 connects that claim down to the actual
ion channels (NCBI/UniProt cited) and out to root-cause therapy, with everything reproduced by
`repro/run_all.py`. Four new verification modules + a treatment dossier + a literature registry.

- **Molecular transducer layer** (`repro/_engine/transduction.py` → run section [3]). The UNIFYING result:
  *every* special-sense transducer is the same object — a cooperative/bistable ION CHANNEL = an R19
  double-well. Verified [V] bistable + discontinuous flip for photoreceptor (CNG: CNGA1/CNGB1), hair cell
  (MET: TMC1 + tip-link PCDH15/CDH23), taste (TAS1R2/TAS1R3 → TRPM5). Olfaction (CNGA2/ADCY3) shares the
  SAME CNG superfamily as the rod — a literal common transducer; its γ is deferred to the DNA pipeline.
  Channel identity + accession are cited [L]; γ is NOT computed here (SSOT → DNA `_to_measure`).
- **Cochlear Hopf amplifier** (`repro/_engine/cochlear_amplifier.py` → run section [4]). The cochlea's active
  amplifier is an oscillator poised AT a bifurcation. Normal form dz/dt=(μ+iω₀)z−β|z|²z+Fe^{iω₀t}; at the
  critical point μ=0 the response is R=(F/β)^{1/3} → **cube-root compression, exponent 1/3, parameter-free**
  [V] (matches the cited ~0.3–0.5 BM compression [L]). Active force = prestin (SLC26A5). μ=0 is the
  *hypothesis*, not a tuned knob; β is a unit. This is why some organs sit near criticality: maximal gain.
- **Setpoint-drift LAW** (`repro/_pathology/setpoint_failure.py` → run section [7]). Disease derived from the
  substrate: a loop-gain drop d gives g_eff=g(1−d) and barrier B(d)=(g²/4)(1−d)² — a QUADRATIC basin
  collapse — with Kramers escape rate ~exp(−B/D). Presbycusis is the amplifier's μ pushed back off
  criticality (the F^{1/3} gain collapses). Shapes [V]; per-disease anchors [L]; absolute rate [O].
- **Root-cause treatment program** (`repro/_pathology/treatment.py` → run section [8]). The principle:
  *root-cause therapy = the inverse substrate operation*. Five inverse ops — (1) restore loop gain,
  (2) raise the attractor barrier, (3) re-engage the error signal, (4) repair the instrument, (5) lower a
  run-away loop gain — instantiated for 7 diseases with the symptomatic-vs-root contrast and evidence level.
  Contested/partial items are flagged honestly: AMD complement inhibitors slow atrophy but show **no
  functional acuity gain yet**; cataract chaperone reversal **failed replication** (Daszynski 2019);
  ATOH1-regenerated hair cells remain **immature**. The substrate mapping is [V]; clinical evidence is [L].
- **Literature & accession registry** (`literature/CITATIONS.md` + `literature/citations.json`). Every anchor
  with its grade: Greenwood 1990 (place-map), the gating-spring series (Howard/Corey/Markin/Martin–Hudspeth),
  the Hopf-cochlea series (Camalet/Eguíluz/Hudspeth–Jülicher–Martin), Fesenko 1985 (cGMP rod conductance),
  Van Egmond/Groen/Jongkees 1949 (canal mechanics), Hofstetter (accommodation), plus all 15 gene accessions.

## Major diseases (non-rare) — covered here; rare/monogenic → disease_wp
Disease is modeled as a failure of a defended setpoint / clock / sense organ on the SAME R19 substrate.
The MAJOR (common, polygenic, acquired, age-related) diseases of this system are covered here; RARE and
monogenic forms are owned by disease_wp and only cross-referenced (entered here as a cited parameter).
Grades: anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle).
- **cataract** ← lens opacification (age / UV / oxidative) -> optical scattering
  - anchor/grade: opacity vs cited age/UV [L]; UV cross-ref integumentary; rare congenital -> disease_wp
- **glaucoma** ← intraocular-pressure setpoint failure -> retinal ganglion-cell loss
  - anchor/grade: IOP setpoint + RGC loss [V]; cited [L]
- **age-related macular degeneration** ← photoreceptor / RPE degeneration (age)
  - anchor/grade: degeneration vs cited age [L]; cross-ref aging
- **refractive error (myopia)** ← axial-length / focal mismatch (classical optics)
  - anchor/grade: prevalence vs cited [L]; optics classical
- **presbycusis / noise-induced hearing loss** ← hair-cell loss (age / acoustic over-drive)
  - anchor/grade: threshold shift vs cited age/noise dose [L]; hair-cell over-drive [V]
- **diabetic retinopathy** ← microvascular damage from chronic hyperglycemia (seam to thermometabolic/diabetes)
  - anchor/grade: cross-ref thermometabolic; microvascular [V]
- **BPPV / vertigo** ← otolith displacement -> false motion signal
  - anchor/grade: mechanical displacement [V]; cited [L]

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and research signed off.
  **STATUS (v0.4.0):** research signed off (all_green=true, 2×sha256 `6a68bc48…`, RS1–RS5 PASS), writing
  COMPLETE + EXPANDED (12 chapters, body 4,375 words, search/SEO gate 0 FAIL / 0 WARN, byte-identical on
  rebuild), **and PUBLISHED** — concept DOI `10.5281/zenodo.20755154` wired into the generator and the
  canonical HTML re-rendered (0 `TBD` remaining), plus a deterministic LaTeX/PDF whitepaper
  (`dist/sensory_organ_vp_site.{tex,pdf}`, 18 pages, byte-identical compile sha256 `c6593c81…`) generated
  from the same corpus. The publication phase rendered/derived only the verified corpus and introduced
  **no new `[O]`**. PHASE=`published`. Next session is **monorepo integration** (push `repro/` to
  `repro/sensory-organs/`, register as the 10th volume in `cross_volume_doi`).
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **DOI:** 10.5281/zenodo.20755154 (concept). Assigned at publication (v0.4.0); wired into the generator
  (claim-strip, JSON-LD `identifier`/`sameAs`, footer, landing, `llms.txt`, `_meta.json`) and emitted on
  the PDF title page as the *Living version* line. Registration as the 10th volume in the upstream
  `cross_volume_doi` registry is done monorepo-side on integration.
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
