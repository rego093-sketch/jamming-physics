# CHARTER — Chronobiology: the Circadian Oscillator Network, Entrainment, and Clock-Disruption Disease

**paper_id:** `circadian_vp_site`  ·  **code:** `clk`  ·  **branch:** integrative (temporal / coupled-oscillator timing layer)  ·  **version:** 0.3.0
**status:** research signed off (stress battery 8/8 green) · canonical site written + DOI wired · PHASE=writing · engine result sha256 `417823934d6e…` (seed=19, 2× identical)
**DOI:** **10.5281/zenodo.20755413** (concept; resolves to the latest version) · v0.2.0 snapshot = version DOI 10.5281/zenodo.20755414 · CC BY 4.0. Registered in `registry/cross_volume_doi.{csv,md}` and wired across the canonical site (JSON-LD identifier/sameAs, claim-strip snapshot, Highwire citation tags).

## Scope (one line)
The ~24h circadian clock is a self-sustained coupled limit-cycle oscillator network (SCN master + peripheral clocks) on the FHN substrate; it free-runs, entrains to light, and GATES nearly every homeostatic setpoint. Clock-environment misalignment (shift work, jet lag) is the disease axis.

## What this package emerges and circulates
Primary objects are LOOPS / OSCILLATORS / sense-organ instruments — node identity + order are owned by
DNA (measured γ, never fitted); nodes whose γ is not yet in the atlas are honest **to-measure** inputs.
It re-emerges NO organs owned elsewhere; it cites the seams below (SSOT) and adds its own dynamics.

### Nodes
- **scn_master_oscillator** (`(SCN_master_clock)`) — no single master gene (circuit/derived/diffuse) — suprachiasmatic ~24h master limit-cycle (light-entrained) — *dyn:* oscillator — *anchor:* circadian period ~24 h [L] TO-ANCHOR
- **core_clock_loop** (`BMAL1`) — γ **to-measure** (named master `BMAL1`; fetch via DNA pipeline, never fitted) — BMAL1/CLOCK<->PER/CRY transcription-translation feedback loop (the molecular oscillator) — *dyn:* oscillator — *anchor:* TTFL period ~24 h [L]; BMAL1 gamma TO-MEASURE
- **peripheral_clock_network** (`(peripheral_clocks)`) — no single master gene (circuit/derived/diffuse) — liver/muscle/adipose peripheral clocks (cite organ packages) — *dyn:* coupled-oscillator — *anchor:* peripheral phase lag [L]; circuit
- **light_entrainment_input** (`(retinal_entrainment)`) — no single master gene (circuit/derived/diffuse) — retinal light -> SCN phase reset (seam to sensory/neuro) — *dyn:* entrainment — *anchor:* phase-response curve [L]; seam

### Seams IN (inherited / cited)
- sensory/neuro: retinal light input -> phase reset (cited)
- ALL homeostasis + organ packages: the clock GATES their setpoints (cited, cross-cutting)
- DNA: node identity + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- circadian phase / gating signal -> thermometabolic, hemodynamic, ionic, immune, ... (this pkg is SSOT for phase/timing)

## Research program (excavated)

The circadian clock is a self-sustained ~24h LIMIT-CYCLE oscillator network on the FHN substrate. It is
not driven by light -- it FREE-RUNS and is merely ENTRAINED by light. It gates almost every homeostatic
setpoint in the other packages, so it is a cross-cutting TIMING layer. Disease is clock-environment
misalignment.

- **RC1** The molecular clock is a self-sustained oscillator: the BMAL1/CLOCK<->PER/CRY transcription-
  translation feedback loop produces a ~24h rhythm that FREE-RUNS without input (FHN limit cycle).
  *Discriminant:* a stable rhythm persists with zero external drive; period ~24h [L], mechanism [V].
- **RC2** Entrainment: a timed light pulse shifts the phase along a phase-response curve until the clock
  LOCKS to the external 24h cycle. *Discriminant:* measure the PRC and the locking range under a periodic
  light drive (`circadian_entrainment_probe`). [V]
- **RC3** Master vs network: is timekeeping ONE master oscillator (SCN) or a COUPLED NETWORK (SCN +
  peripheral liver/muscle/adipose clocks)? *Discriminant:* coupling strength vs independent phase drift;
  do peripheral clocks free-run or follow the SCN? [V]
- **RC4** Setpoint gating: the clock imposes a daily rhythm on thermometabolic / hemodynamic / ionic
  setpoints (core temperature, blood pressure, cortisol). *Discriminant:* the defended setpoints oscillate
  with circadian phase (cross-cutting seam). [V]
- **RC5** Misalignment: when the internal clock and external time decouple (shift work, jet lag), the
  failure emerges. *Discriminant:* phase-decoupling produces the disease state in RC4's gated setpoints. [V]
- **RC6** Circadian–mood seam (EXECUTED): misalignment flattens the gated HPA cortisol rhythm, and that
  sustained, demand-misaligned signal supplies the CIRCADIAN depression contributor the mind volume explicitly
  locked (mind's withdrawal bias b<0). *Discriminant:* the HPA flattening index grows monotonically with the
  phase gap (0→2.11085). SIGN only — magnitude [O], felt quality stays in mind (consciousness_claim=0). [V sign]
- **TX1** Chronotherapy (EXECUTED): re-aligning the clock with a PRC-correct zeitgeber; the wrong phase worsens
  it. *Discriminant:* a correct-phase pulse corrects the delay (2.56→0 h), the same pulse at the wrong phase
  grows it (5.44→11.2 h). Direction [V]; efficacy=0; not medical advice.
- **Status:** all eight discriminants (RC1–RC6 + TX1) PASS; the molecular clock carries a MEASURED BMAL1 well
  γ=1.33348 (gene 406, NC_000011.10), never fitted; aggregate result sha256 `417823934d6e…` (seed=19).
- Grades (C3): oscillator mechanism / PRC shape [V]; period 24h + cited phases [L]; absolute phase [O].

## Major diseases (non-rare) — covered here; rare/monogenic → disease_wp
Disease is modeled as a failure of a defended setpoint / clock / sense organ on the SAME R19 substrate.
The MAJOR (common, polygenic, acquired, age-related) diseases of this system are covered here; RARE and
monogenic forms are owned by disease_wp and only cross-referenced (entered here as a cited parameter).
Grades: anchor [L] / shape [V] / absolute incidence-rate [O] (state obstacle).
- **circadian rhythm sleep-wake disorders** ← delayed/advanced sleep phase, non-24h, shift-work disorder, jet lag = clock<->environment misalignment
  - anchor/grade: misalignment vs cited chronotype data [L]; phase-decoupling [V]; sleep/affect cross-ref to mind/neuro
- **shift-work metabolic & cardiovascular risk** ← chronic clock disruption dysregulates the gated metabolic + pressure setpoints (seam)
  - anchor/grade: RR vs shift-work exposure [L]; cross-loop disruption [V]; absolute [O]
- **shift-work cancer risk** ← IARC class 2A: circadian disruption raises the crossing rate (clock-gated + immune)
  - anchor/grade: RR vs night-shift years (IARC anchor) [L]; clock-gated crossing [V]; ties to the oncology kernel
- **circadian-misalignment depression** (seam, EXECUTED) ← misalignment flattens the gated HPA rhythm → mind's
  withdrawal bias → (mind) hypo-coordination → chronification; supplies the contributor mind locked
  - anchor/grade: flattening sign [V]; magnitude [O] (owned by mind); SIGN-only firewall, consciousness_claim=0
- **circadian disruption in autism** (cross-ref, EXECUTED) ← the same timing seam aggravates mind's
  coupling-organisation reading of autism (common circadian/sleep disruption)
  - anchor/grade: SIGN only [V]; coupling pathology owned by mind; cross-ref to mind §18/§19

### Management (EXECUTED) — chronotherapy, efficacy=0
PRC-based re-alignment is the treatment axis: timed light (morning advances / evening delays), timed melatonin
(PRC ~antiphase to light), wake therapy (transient homeostatic lift, no clock re-alignment), behavioural
entrainment (wider Arnold tongue). The wrong phase is iatrogenic, not inert. No new constant (the PRC in
reverse); direction [V]; clinical windows [L]; **efficacy=0; not medical advice** (mood response owned by mind).

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase + C1/C3 in research. C0 overrides on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and research signed off.
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **DOI:** **10.5281/zenodo.20755413** (concept) wired across the site; v0.2.0 snapshot DOI 10.5281/zenodo.20755414. Cross-volume registry entry recorded in `registry/cross_volume_doi.{csv,md}` (writing-phase task, done at v0.3.0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state passes by files only.
