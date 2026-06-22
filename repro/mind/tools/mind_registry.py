#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
mind_registry.py — single source of truth for the Felt-Cognition search-readiness layer (VP-SPEC v1.8).

Holds, in ONE place (C1 SSOT):
  LOCKS   the emerged quantities chapters cite -> each becomes a self-contained vp-card
          (value + one-line meaning + grade + link to the canonical chapter). 6-R.2.
  ANSWERS the answer-first direct answer for each chapter (40-60 words). 6-R.3.
  CITES   which locks each chapter cites (gets a card).

Every numeric value in LOCKS is cross-checked against the frozen engine results
(repro/mind/_engine/results/mind_emergence_results.json) at validate() time, so the cards can
never drift from the simulation (C1, drift 0). Values are restated, not re-derived (6-R.2).
"""
import os, json

_HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.abspath(os.path.join(_HERE, os.pardir))
RESULTS = os.path.join(PKG, "repro", "mind", "_engine", "results", "mind_emergence_results.json")
DOI = "10.5281/zenodo.20694404"
ORCID = "0009-0002-7535-8245"

# RELEASE_DATE — single source of truth for sitemap <lastmod> (ISO-8601, UTC date).
# DETERMINISM CONTRACT (VP-SPEC C1, §8 idempotency): the search-layer build is a pure
# function of source content; it must NOT read the wall clock. sitemap.xml therefore stamps
# every <lastmod> from this constant, not datetime.date.today(). Re-running the build on any
# day yields a byte-identical docs/ tree. Bump this string by hand only when a release ships
# new content; that edit is the intentional, version-controlled act that updates <lastmod>.
RELEASE_DATE = "2026-06-18"

# ---------------------------------------------------------------------------
# LOCKS — emerged quantities (value strings are display; check_key/check ties to results)
# ---------------------------------------------------------------------------
LOCKS = {
    "front_speed_c": {
        "label": "front speed = c", "value": "1.01 c", "grade": "[V]",
        "meaning": "the radiated brainwave front travels at the wave speed c — a genuine EM emission, "
                   "the signal an EEG/MEG records.",
        "canonical": "04-em-brainwave",
        "check": ("M1_em_brainwave/front_speed", 1.0146046496),
    },
    "theta_gamma": {
        "label": "θ/γ ≈ 6.1", "value": "≈ 6.1 (within 7 ± 2)", "grade": "[V]",
        "meaning": "gamma cycles nested in one theta cycle — the working-memory slot count, inside "
                   "Miller's 7 ± 2. The ordering θ < γ is forced; absolute hertz are open.",
        "canonical": "04-em-brainwave",
        "check": ("M1_em_brainwave/theta_over_gamma_capacity", 6.125),
    },
    "field_coherence": {
        "label": "coherence ≈ 0.998", "value": "≈ 0.998", "grade": "[V]",
        "meaning": "classical-field coherence end-to-end across a brain transect (worst-case phase "
                   "shift ~10⁻³ rad, amplitude drop ~0.1%); swept across the 1–100 Hz EEG band.",
        "canonical": "04-em-brainwave",
        "check": ("M8_field_coherence/classical_coherence_across_brain", 0.9983704227),
    },
    "brain_wavelengths": {
        "label": "brain ≈ 10⁻⁴ λ", "value": "~10⁻⁴ wavelength", "grade": "[V]",
        "meaning": "the brain spans a single quasi-static point of the low-frequency field; the skin "
                   "depth is >600× its width, so the field is essentially undamped across it.",
        "canonical": "04-em-brainwave",
        "check": ("M8_field_coherence/brain_in_wavelengths", 0.0002600486),
    },
    "commit_order": {
        "label": "organ commit order", "value": "hypothalamus < cerebellum < cerebrum < hippocampus",
        "grade": "[V dir]",
        "meaning": "each master gene sets a measured bistable gamma; an ascending fold-threshold "
                   "fixes the commit order. Substrate emerged under drive; absolute size open.",
        "canonical": "03-organ-emergence",
        "check": None,
    },
    "pattern_completion": {
        "label": "completion from a 10% cue", "value": "attractor overlap → 1.0", "grade": "[V]",
        "meaning": "a Hebbian-deepened engram well completes the full stored pattern from a 10% partial "
                   "cue — memory as a physical attractor. Absolute capacity open.",
        "canonical": "05-memory-physics",
        "check": ("M2_hippocampal_memory/attractor_overlap", 1.0),
    },
    "phase_protect": {
        "label": "theta-phase protection", "value": "interference → 0 (phase-separated)", "grade": "[V]",
        "meaning": "writing and retrieving on opposite theta phases measurably protects old memory "
                   "from interference — the brainwave clock memory rides.",
        "canonical": "05-memory-physics",
        "check": ("M2_hippocampal_memory/interference_separated", 0.0),
    },
    "mediator_discipline": {
        "label": "physical-mediator rule", "value": "every eddy names a carrier", "grade": "[F disc]",
        "meaning": "every claim names a physical mediator — ion spikes / synaptic currents gated by "
                   "classified low-frequency phase (communication-through-coherence) — never an unnamed field.",
        "canonical": "02-not-a-field",
        "check": None,
    },
    "pci_negative": {
        "label": "PCI = honest negative", "value": "HONEST NEGATIVE", "grade": "[O]",
        "meaning": "the consciousness access marker (perturbational complexity, PCI) did not robustly "
                   "reproduce; it is reported as a negative, not quietly dropped.",
        "canonical": "12-open-problem",
        "check": ("M7_embodied_open/pci_access_marker", "HONEST_NEGATIVE"),
    },
    "hard_problem": {
        "label": "hard problem = OPEN", "value": "OPEN", "grade": "[O]",
        "meaning": "the subjective character of a thought/feeling (the quale) is not solved; the model "
                   "specifies function, not experience. No link in the paper is causal.",
        "canonical": "12-open-problem",
        "check": ("M7_embodied_open/hard_problem", "OPEN"),
    },
    "coord_kappa": {
        "label": "ephaptic coupling κ = 0.55", "value": "κ = 0.5496 (measured)", "grade": "[F]",
        "meaning": "the inter-organ coupling strength is not chosen — it is the measured ephaptic "
                   "depolarisation ΔVm = 0.2748 mV as a fraction of the measured 0.5 mV entrainment "
                   "threshold (neuro §19). The field sits AT threshold, so the fraction is order-one.",
        "canonical": "13-em-coordination",
        "check": ("M9_em_coordination/kappa_ephaptic_measured", 0.5496),
    },
    "coord_regime": {
        "label": "partial / metastable lock", "value": "R ≈ 0.39 (between 0.25 and 1.0)", "grade": "[V]",
        "meaning": "at the measured coupling the twelve central organs neither drift free (R ≈ 0.25) nor "
                   "fully lock (R = 1, a seizure); they sit in a partial, fluctuating synchrony — the regime "
                   "that supports flexible coordination rather than rigid global lock. Grounding the geometry "
                   "on real MNI anatomy (v1.19, ring → measured [L]) lifts the operating point from R ≈ 0.33 "
                   "to R ≈ 0.39 — higher, but still far below the R ≥ 0.9 synchronization threshold: real "
                   "anatomy strengthens coordination without ever seizing.",
        "canonical": "13-em-coordination",
        "check": ("M9_em_coordination/R_measured", 0.3896145516),
    },
    "coord_field_contribution": {
        "label": "field's causal contribution", "value": "+0.135 order (measured MNI [L] geometry)", "grade": "[V]",
        "meaning": "the named cancel-vs-augment test, run in silico on the v1.19 MEASURED MNI [L] "
                   "inter-organ geometry: cancelling the local field drops global order by ≈ 0.135 "
                   "and augmenting it raises order to ≈ 0.42 — so the near-field causally contributes "
                   "coordination on real anatomy. Grounding the geometry (ring → measured) RAISES this "
                   "contribution (~0.073 on the old [O] ring → ~0.135 measured) but the regime stays "
                   "partial_metastable; this is the prediction the in-vivo test must check.",
        "canonical": "13-em-coordination",
        "check": ("M9_em_coordination/field_contribution", 0.1346804816),
    },
    "coord_efficacy_open": {
        "label": "functional use = OPEN", "value": "medium_efficacy_tested = 0", "grade": "[O]",
        "meaning": "M9 shows the measured field CAN coordinate (mechanism, [V]); whether cognition "
                   "biologically USES it is untested. The obstacle: the behaviour-labelled in-vivo "
                   "field-cancel-vs-augment recording named in neuro §9/§19 has not been performed.",
        "canonical": "13-em-coordination",
        "check": ("M9_em_coordination/medium_efficacy_tested", 0.0),
    },
    "sens_coupling_kappa": {
        "label": "sensory coupling κ = 0.55", "value": "κ = 0.5496 (same measured value)", "grade": "[F]",
        "meaning": "the sensory↔central coupling is NOT a new constant — it is the same measured ephaptic "
                   "fraction the central organs use (ΔVm 0.2748 mV / 0.5 mV threshold, neuro §19). Eight "
                   "afferent streams couple reciprocally to their anatomical relays at exactly this strength.",
        "canonical": "14-sensory-coupling",
        "check": ("M10_sensory_coupling/kappa_ephaptic_measured", 0.5496),
    },
    "sens_crossmodal_field": {
        "label": "cross-modal binding via the field", "value": "+0.039 PLV (cancel → measured)", "grade": "[V]",
        "meaning": "cross-relay senses (sitting on different central organs) phase-organise ONLY through the "
                   "shared ephaptic field: cancelling it drops cross-modal PLV to 0.018, the measured field "
                   "gives 0.057, augmenting gives 0.108. Co-relay senses (same organ) stay locked ≈ 0.32 "
                   "regardless — so the binding is field-mediated, not an artifact of the inputs.",
        "canonical": "14-sensory-coupling",
        "check": ("M10_sensory_coupling/crossmodal_field_contribution", 0.0386219394),
    },
    "sens_regime_bounded": {
        "label": "sensory drive loads, never seizes", "value": "R ≈ 0.323 (bounded, lifted)", "grade": "[V]",
        "meaning": "adding eight afferent streams leaves the central substrate's anchor R unchanged "
                   "(0.328 = frozen M9) and drives it to R ≈ 0.323 — still above the uncoupled baseline, "
                   "still far below lock. Input loads onto the central field without seizing or silencing "
                   "it, and stays in this regime under ±20% band perturbation.",
        "canonical": "14-sensory-coupling",
        "check": ("M10_sensory_coupling/central_R_with_sensory", 0.3231730263),
    },
    "sens_efficacy_open": {
        "label": "functional use = OPEN", "value": "medium_efficacy_tested = 0", "grade": "[O]",
        "meaning": "M10 shows the measured field CAN bind sensory input to the central organs (mechanism, "
                   "[V]); whether cognition biologically USES this sensory↔central coupling is untested. The "
                   "same behaviour-labelled in-vivo field-cancel-vs-augment recording owed for M9 "
                   "(neuro §9/§19) is owed here too.",
        "canonical": "14-sensory-coupling",
        "check": ("M10_sensory_coupling/medium_efficacy_tested", 0.0),
    },
    "lm_angle_rectification": {
        "label": "angle rectification α = 2/π", "value": "α = 0.6366 (single), δ = 1/π² (double)", "grade": "[F]",
        "meaning": "the cited bridge constant (DOI 10.5281/zenodo.17932566): a SIGNED phase overlap "
                   "(X0·cosθ, which cancels on average) becomes a sign-surviving scalar only through "
                   "geometric rectification — single ⟨|cos|⟩ = 2/π, double ⟨[cos]+[cos]+⟩ = 1/π², with "
                   "2π = α/δ recovered exactly. That sign-surviving scalar is the information bit. No new "
                   "constant: α and δ are pure quadrature averages.",
        "canonical": "15-light-to-memory",
        "check": ("M11_light_memory_binding/alpha_rect", 0.6366197724),
    },
    "lm_information_contrast": {
        "label": "binding carries information", "value": "contrast = 0.149 (bound ¼ vs unbound floor δ)", "grade": "[V]",
        "meaning": "phase-locked (bound) brainwave⊕sensory overlap rectifies to a coincidence of ¼ = 0.25; "
                   "antiphase cancels to 0; unrelated (unbound) inputs sit at the floor (1/π)² = δ = 0.1013. "
                   "The information contrast bound − unbound = 0.1487 > 0 is what a memory cell can read out: "
                   "a bound pair delivers a measurably larger rectified drive than chance coincidence.",
        "canonical": "15-light-to-memory",
        "check": ("M11_light_memory_binding/information_contrast", 0.1486788164),
    },
    "lm_memory_write": {
        "label": "bound light writes memory, unbound does not", "value": "drive 0.824 > fold 0.385 → write+persist", "grade": "[V]",
        "meaning": "the rectified bound drive (0.8244) clears the engram cell's R19 bistable fold threshold "
                   "(0.3849), so the well deepens and the pattern persists after the input is removed — a "
                   "written memory. Weak or antiphase (unbound) drive stays below fold and the cell holds "
                   "(no write). Writing and retrieving on opposite theta phases keeps two memories separable "
                   "(interference 0.0 separated vs 0.217 mixed): the brainwave is the write clock.",
        "canonical": "15-light-to-memory",
        "check": ("M11_light_memory_binding/bound_input_writes_and_persists", 1.0),
    },
    "lm_reader_feels_field": {
        "label": "a downstream neuron feels the field", "value": "cancel 0.118 < measured 0.605 < augment 0.642", "grade": "[V]",
        "meaning": "a reader neuron placed in the rolled multi-information field entrains to it: with the field "
                   "cancelled its phase-lock is 0.118, at the measured ephaptic strength 0.605, augmented 0.642 "
                   "— a strictly monotone cancel < measured < augment ordering. The neuron responds to the "
                   "field itself, not to a copied input wire (field-mediated, non-circular). Multiple infos "
                   "rolled into gamma slots within one theta frame are each recovered at fidelity 1.000.",
        "canonical": "15-light-to-memory",
        "check": ("M11_light_memory_binding/reader_feels_field", 1.0),
    },
    "lm_efficacy_open": {
        "label": "biological use = OPEN", "value": "medium_efficacy_tested = 0", "grade": "[O]",
        "meaning": "M11 establishes a complete IN-SILICO mechanism — emergent light → brainwave⊕sensory "
                   "superposition → angle rectification → information bit → engram write → multi-info roll → "
                   "downstream read — reproducibly, bit-for-bit. It does NOT establish that biological "
                   "cognition uses light-rectified binding to write memory; that link is untested and strongly "
                   "inferred from the cited physics, not measured. No experience claim is made.",
        "canonical": "15-light-to-memory",
        "check": ("M11_light_memory_binding/medium_efficacy_tested", 0.0),
    },
    "thought_definition": {
        "label": "thought = a faculty union (defined term)",
        "value": "F1-F10 closed; F11-F14 owed", "grade": "[F disc]",
        "meaning": "'thought' names the union of fourteen mental faculties, not an abstract umbrella; the "
                   "ten core faculties (perception, selection, the serial stream, memory, learning, the "
                   "affect mechanism, arousal/sleep, dreaming, large-scale binding, pathology) are built, "
                   "frozen and bit-reproducible on an emerged substrate, while the four higher faculties "
                   "(language, volition, social cognition, metacognition) are honestly owed with their "
                   "external inputs named. Closure is on the mechanism axis only; the felt axis is "
                   "orthogonal and out of scope.",
        "canonical": "16-what-is-a-thought",
        "check": None,
    },
    # --- Part II: disorders of the mind (autism / theta-cap / ADHD) ----------
    # These cite the add-only D9 (autism cohort) and VC (theta-cap virtual clinical) decision-checks
    # in repro/mind/_verify/ (run_all_d9.py, run_all_vc.py), which import the engine READ-ONLY and
    # reproduce bit-for-bit (SEED=19). They are framing locks (check:None): the numbers live in the
    # _verify modules' own committed sha256 gates, not in the engine emergence results.
    "autism_three_axis": {
        "label": "autism = three separable faults (T / O / W)",
        "value": "threshold, output/gain, wiring — fingerprinted by (ΔPAC, ignition)", "grade": "[V mech]",
        "meaning": "on the emerged cerebrum autism is read as three separable faults: a threshold/E-I fault "
                   "(T, raised ignition fold), an output/gain fault (O, low per-node drive), and a long-range "
                   "wiring fault (W, intact fold and drive but a local-over/long-range-under geometry). The pair "
                   "(ΔPAC, ignition) uniquely fingerprints each — T: PAC down, fold raised; O: PAC down, fold "
                   "normal; W: PAC unchanged — and reproduces under SEED=19. Which fault any individual's autism "
                   "is, is held open. efficacy=0; not a diagnosis.",
        "canonical": "18-autism-three-axis",
        "check": None,
    },
    "autism_chemical_reach": {
        "label": "a gain chemical: full on T, partial on O, mask-only on W",
        "value": "T fully reversed; O partial; W masked by over-sync, not corrected", "grade": "[V mech]",
        "meaning": "a scalar threshold-lowering (gain) operator — the mechanism by which the catecholaminergic "
                   "stimulant class raises excitability — fully reverses the threshold fault (R back to health), "
                   "partly helps the output fault, and cannot correct the wiring fault: brute gain leaves the "
                   "locality imbalance exactly invariant and reaches health only by over-synchronising the whole "
                   "network (a mask). Selective multi-lever schemes buy a safety margin, not new efficacy. "
                   "efficacy=0; not a claim any drug treats autism.",
        "canonical": "19-autism-chemical-limits",
        "check": None,
    },
    "theta_cap_pacemaker": {
        "label": "θ-cap = external pacemaker, not a benign lane (keystone)",
        "value": "only a forced carrier routes; every passive lane is inert", "grade": "[V mech]",
        "meaning": "on the wiring-faulted cohort only a coherence-forcing external clock lifts synchrony toward "
                   "health, and only inside a narrow window (inj ≈ 0.08–0.10, over-sync past 0.15); every passive "
                   "additive coupling — broadcast relay of the network's own mean phase, far-pair relay, pure "
                   "superposition — is inert. No passive lane routes on a broken substrate, so the benign "
                   "additive-lane reframing is REFUTED. The cap forces coordination as a pacemaker; it does not "
                   "repair the wiring.",
        "canonical": "20-theta-cap-pacemaker",
        "check": None,
    },
    "theta_cap_removable": {
        "label": "θ-cap is cleanly removable (no dependence, no rebound)",
        "value": "far-coh restored on; deficit resumes off; no acquired dependence", "grade": "[V mech]",
        "meaning": "with the cap on, far-pair coherence is restored (0.213 ≥ health 0.170) at the healthy "
                   "metastable synchrony without over-sync; across OFF/ON/OFF/ON/OFF epochs every off-epoch returns "
                   "to the deficit (drift ~0.004) with no rebound undershoot and no acquired dependence. The "
                   "oscillator substrate carries no plasticity variable, so removing the drive resumes the deficit "
                   "instantly — the cap paces rather than repairs.",
        "canonical": "20-theta-cap-pacemaker",
        "check": None,
    },
    "theta_cap_molecular_safe": {
        "label": "molecularly safe below the spinodal fold",
        "value": "0 irreversible flips at any cycle count; cost ∝ amplitude²", "grade": "[V mech]",
        "meaning": "tested at the R19 switch with the fatigue law derived (λ = 2g; no new constant), the θ carrier "
                   "sits deep in the quasi-static regime (Ω = ω/λ = 0.018). Below the spinodal fold the switch is a "
                   "memoryless relaxor with zero irreversible basin flips at any cycle count (the first flip needs "
                   "amplitude 0.70, past the fold); the only cost is a reversible per-cycle thermal load scaling as "
                   "amplitude². The binding constraint is circuit over-synchronisation, not molecular wear.",
        "canonical": "20-theta-cap-pacemaker",
        "check": None,
    },
    "theta_cap_operating_principle": {
        "label": "operating mode = minimum-effective, deficit-matched, continuous",
        "value": "weaker inert · stronger over-syncs · intermittent reverts · nothing banked", "grade": "[F disc]",
        "meaning": "if a θ-cap is to supply the wiring-axis function at all, the dynamics force one mode: the "
                   "minimum amplitude that produces a real routing change, matched to the individual wiring deficit, "
                   "applied continuously. Below the window it is inert, above it over-syncs, intermittent dosing "
                   "reverts to the deficit, and no benefit is banked (no plasticity). The cap is a wearable drug "
                   "with no half-life past removal. efficacy=0; not a dosing protocol.",
        "canonical": "21-theta-cap-operating-principle",
        "check": None,
    },
    "theta_cap_feasibility": {
        "label": "physical feasibility = OPEN (components exist, assembly does not)",
        "value": "theta-tACS + closed-loop + multi-electrode all real; the combination is not", "grade": "[O]",
        "meaning": "every component the operating principle demands exists in research form — θ-band tACS, "
                   "closed-loop phase-locked EEG-tACS, multi-electrode phase-shifted montages built to alter "
                   "long-range connectivity (in-phase coordinates, anti-phase disorganises), individualised "
                   "MRI-optimised targeting, and wearable home delivery — but the specific assembly "
                   "(individualised + phase-structured + amplitude-windowed + network-targeted + continuous) does "
                   "not, there is no in-vivo readout of the wiring deficit to set the matched amplitude, the narrow "
                   "window risks over-sync, and the plasticity sign is phase-dependent. Feasibility of the "
                   "apparatus is not evidence of benefit; efficacy=0.",
        "canonical": "21-theta-cap-operating-principle",
        "check": None,
    },
    "adhd_axis_specific": {
        "label": "ADHD = gain/arousal with intact wiring (separates from autism)",
        "value": "stimulant restores ADHD; cap is for autism's wiring; they compose on AuDHD", "grade": "[V mech]",
        "meaning": "an explicit gene-grounded ADHD substrate (six output/gain genes, two arousal/threshold genes, "
                   "wiring = none; axis-ambiguous/syndromic genes pre-registered excluded) restores to health under "
                   "the stimulant in both synchrony and θ–γ coupling, where the same stimulant only partly reaches "
                   "autism; the cap's long-range benefit is 3.3× larger where wiring is broken. On an explicit "
                   "AuDHD substrate the stimulant fixes the gain axis and the cap the wiring axis, without "
                   "interference. The engine has no separately-validated ADHD model — this is a gene-grounded "
                   "interpretation, model validity OPEN.",
        "canonical": "22-adhd-vs-autism",
        "check": None,
    },
    "virtual_trial": {
        "label": "population: gain responders, wiring non-responders, dose-cap residual",
        "value": "stim-responders gain-dominated; residual = dose-cap/stiffness limit, not a wiring tail",
        "grade": "[V mech]",
        "meaning": "across a synthetic population (N = 80, 76 affected) stimulant responders are gain-dominated "
                   "(responder fraction falls monotonically with wiring share, r = −0.60), non-responders are "
                   "wiring-dominated and partly cap-rescuable, and a bundled sub-claim is refuted and promoted to a "
                   "finding: the cap-unrescued residual is not a pure severe-wiring tail but a dose-cap / stiffness "
                   "limit, with a fixed amplitude over-syncing the milder cases (so amplitude must be matched to "
                   "the deficit). Every fraction is an in-silico coupling state, not a clinical response rate. "
                   "efficacy=0.",
        "canonical": "23-virtual-trial",
        "check": None,
    },
    # --- Part II atlas extension: schizophrenia (T1a) + epilepsy (T2a) ---
    "schizophrenia_mirror": {
        "label": "schizophrenia = the over-ignition mirror of autism-T on the same R19 axis",
        "value": "excitatory bias lowers the fold → aberrant ignition; antipsychotic restores it and worsens autism-T",
        "grade": "[V mech]",
        "meaning": "on the one shared ignitability axis (the M3 R19 fold = spinodal(g) = 2(g/3)^1.5 = 0.3849, "
                   "measured-grounded), schizophrenia is the opposite pole from autism-T: a disinhibitory/excitatory "
                   "E/I bias LOWERS the fold (ignition threshold 0.245 vs health 0.395) so weak, in-health-sub-fold "
                   "assemblies (candidates 2,3) now ignite — aberrant salience with no loss of the relevant ones — "
                   "where autism-T's inhibitory bias RAISES the fold and loses relevant ignitions. The pair "
                   "(ignition-direction, aberrant-vs-lost) separates HEALTH / AUTISM-T / SCHIZOPHRENIA uniquely. A "
                   "uniform gain-reducing / threshold-raising antipsychotic-class push restores the healthy selective "
                   "set (4,5) and worsens autism-T; the gain-raising stimulant that helped autism-T worsens "
                   "schizophrenia — one handle, opposite signs at the two poles. The therapeutic sign aligns with "
                   "sleep-need (arousal down), the mirror of autism. Which pole a given psychosis is, is OWED [O]. "
                   "efficacy=0; not medical advice.",
        "canonical": "24-schizophrenia-mirror",
        "check": None,
    },
    "schizophrenia_symptom_domains": {
        "label": "positive / negative / cognitive symptoms sit on the threshold / output / wiring axes",
        "value": "one gain-reducing operator reverses positive only; negative and cognitive are not reached → axis-structured",
        "grade": "[V mech]",
        "meaning": "the three symptom domains map onto the three T/O/W axes. POSITIVE = the threshold over-ignition "
                   "pole (excitatory bias lowers the fold → aberrant ignition of irrelevant assemblies); the "
                   "gain-reducing antipsychotic raises the fold back and removes them (REACHED). NEGATIVE = an "
                   "output/gain DEFICIT (R = 0.354 < health 0.390); the antipsychotic is itself a gain reduction, so "
                   "it pushes output even lower (to 0.309 — wrong direction, NOT reached). COGNITIVE = a long-range "
                   "WIRING fault (locality 0.842 > health 0.794; the dysconnection hypothesis); a scalar gain "
                   "operator leaves the locality imbalance EXACTLY invariant (NOT reached). One gain-reducing operator "
                   "reverses POSITIVE only → the differential antipsychotic response is AXIS-structured, not "
                   "dose-structured: the mechanistic account of why D2 blockade relieves positive but not "
                   "negative/cognitive symptoms. It retires more D2 blockade as a route to negative/cognitive benefit "
                   "(an in-silico mechanistic null). Which domain dominates a given illness is OWED. efficacy=0.",
        "canonical": "24-schizophrenia-mirror",
        "check": None,
    },
    "epilepsy_oversync": {
        "label": "epilepsy = the over-synchronisation pole; the ictal state = collapse of the selective gate",
        "value": "excitatory bias drives R to the over-sync ceiling and all assemblies ignite; an anticonvulsant reverses it and raises the threshold",
        "grade": "[V mech]",
        "meaning": "epilepsy is the over-synchronisation pole of the engine's synchrony axis (the global Kuramoto "
                   "order parameter R on the measured ephaptic kernel, plus the M3 R19 ignition gate). An "
                   "excitatory/disinhibitory E/I bias raises R monotonically toward the over-sync ceiling "
                   "(0.422 > health 0.390); past a critical bias (+0.3) the selective single-winner gate collapses "
                   "and EVERY candidate assembly ignites — the ictal state, a loss of GATING (Axis-A firewall: a "
                   "mechanism boundary, not a claim about ictal experience; consciousness_claim=0). On one axis: "
                   "autism-T (under-ignited) < health (selective) < schizophrenia (aberrant, some irrelevant) < "
                   "epilepsy (all ignited). An inhibitory / threshold-raising anticonvulsant-class push moves R back "
                   "down and restores the gate — it raises the seizure threshold by moving the operating point away "
                   "from the over-sync ceiling (the same ceiling the θ-cap must stay below, §20). The static "
                   "susceptibility is characterised; the ictal time-course is OWED to a state-switching layer (E2). "
                   "efficacy=0; not medical advice.",
        "canonical": "25-epilepsy-oversync",
        "check": None,
    },
    "plasticity_consolidation": {
        "label": "plasticity = the consolidation layer; the reversible→chronified switch the static atlas never had",
        "value": "a phase-correlation Hebbian update of the ephaptic W makes consolidation representable, resolves the open dosing question (spaced > massed), and turns a reversible excursion into a chronified one",
        "grade": "[V mech]",
        "meaning": "the frozen engine has NO plasticity variable — which is why the θ-cap (§20-21) could only PACE, "
                   "not repair, and why its plasticity sign was OPEN [O]. This layer adds a slow phase-correlation "
                   "Hebbian update to the ephaptic kernel, W_ij ← max(0, W_ij(1+η·C_ij)) with C_ij = "
                   "<cos(θ_j−θ_i)>, row-renormalised. The rule FORM is forced [F] (standard phase-STDP, no free "
                   "constant, row-stochastic so the ~1/r³ ephaptic locality is preserved); the RATE η is [O] and "
                   "every sign holds over an η sweep (anti-tuning), and the coupling-vs-bias map is the SAME "
                   "k=κ/(1−|b|)[excit]/κ/(1+|b|)[inhib] cap 2κ as the SZ/epilepsy modules — no new tuned constant. "
                   "Four results: (E0.1) driving the healthy point under plasticity then removing the drive leaves "
                   "R at or above baseline (0.390→0.391) — consolidation / after-effects, over an η sweep; (E0.2) "
                   "the same total cap dose delivered SPACED (periodic) leaves a LARGER retained structural trace "
                   "‖ΔW‖ than MASSED (continuous) (0.225 vs 0.115) — a spacing effect from pure phase-plasticity, "
                   "so with plasticity the cap REPAIRS and pacing beats holding (resolving the §20-21 [O]); (E0.3) "
                   "without plasticity (η=0) a faulted excursion fully REVERTS when the bias is removed (the §20 "
                   "'paces not repairs / no rebound' result, now shown to be a consequence of the plasticity-free "
                   "substrate), while with plasticity (η>0) it leaves a retained trace (0.394>0.390) — plasticity "
                   "is the reversible→chronified switch (Axis-A firewall: a mechanism boundary, not a claim about "
                   "the felt quality of chronic illness; consciousness_claim=0); (E0.4) η=0 reproduces the frozen "
                   "M9 anchor R=0.38961455156044245 bit-for-bit and leaves W identical — a pure add-on (engine "
                   "e61083ae…, tree 0fbf4988…, byte-unchanged). E0 is the LAYER, not a disorder; depression (T1b), "
                   "bipolar (T2b) and addiction (T3a) import its substrate and are owed to later modules. "
                   "efficacy=0; not medical advice; hard problem OPEN.",
        "canonical": "26-plasticity-consolidation",
        "check": None,
    },
    "depression_chronification": {
        "label": "depression = the chronification of a low-coordination operating point; TRD = the trace's depth",
        "value": "a sustained HPA-driven withdrawal lowers coordination below health (acute, reversible); under the plasticity layer it writes a retained structural trace (chronification); delayed onset = a consolidation timescale; treatment resistance = trace depth",
        "grade": "[V mech]",
        "meaning": "depression is the first TEMPORAL disorder, built ON TOP of E0: it IMPORTS PlasticConnectome and "
                   "drives it (no rule re-derivation). The handle is the engine's HPA/stress axis (M18 cortisol cascade "
                   "+ M17 valence, where cortisol sits on the withdrawal pole), mapped to a sustained withdrawal bias "
                   "b<0 through the SAME coupling map k=κ/(1+|b|) the SZ/epilepsy/E0 modules use — no new constant; only "
                   "the stress→withdrawal SIGN is asserted (consistent with the M17 valence geometry), the magnitude is "
                   "[O], and every sign holds over a rate/stress sweep. Four results: (D1) a sustained withdrawal lowers "
                   "the global order parameter below health (R 0.390→0.331 at severe withdrawal) — the acute, reactive "
                   "depressed operating point, fully reversible on the static substrate; (D2) WITHOUT plasticity (η=0) "
                   "the excursion reverts exactly when the stressor lifts (reactive low mood), WITH plasticity (η>0) it "
                   "leaves a retained structural trace that does not revert and deepens with exposure (‖ΔW‖ 0.075→0.151→"
                   "0.227→0.338) — the reversible→chronified switch on the HPA handle (HONEST: the robust signal is the "
                   "structural trace ‖ΔW‖; post-removal R is NOT asserted below baseline); (D3) a coordination-restoring "
                   "push moves the chronified structure only slowly — the restoring movement accumulates over epochs and "
                   "is small after one (0.018 vs 0.138 at eight) with a therapeutic R direction — antidepressant DELAYED "
                   "ONSET as a consolidation timescale, not a pharmacokinetic delay; (D4) at a fixed restoring budget the "
                   "FRACTION of the depressive trace neutralised decreases as the trace deepens — treatment resistance is "
                   "the DEPTH of the chronified trace. η=0/stress=0 reproduces the frozen M9 anchor R=0.38961455156044245 "
                   "bit-for-bit (engine e61083ae…, tree 0fbf4988…, byte-unchanged). Axis-A firewall: a retained trace is "
                   "a mechanism boundary, not a claim about the felt quality of depression (consciousness_claim=0). "
                   "Bipolar (E2+E0, T2b) and addiction (T3a) import this substrate and are owed. efficacy=0; not medical "
                   "advice; hard problem OPEN.",
        "canonical": "27-depression-chronification",
        "check": None,
    },
    "state_switching": {
        "label": "the state-switching layer = the R19 bistable cell read OVER TIME; closes the §25 ictal time-course",
        "value": "hysteresis (loop width 2·spinodal≈0.77), a transition latency that diverges at the fold (critical slowing → the owed §25 ictal time-course), and the barrier as the switching threshold",
        "grade": "[V mech]",
        "meaning": "the plasticity layer (§26) gave the atlas a SLOW structural variable; this layer gives the FAST "
                   "one — a state that switches and stays switched. No new machinery: the R19 cell s\u0307 = g·s − s³ + h "
                   "(the supercritical pitchfork the whole framework rests on) is bistable for g>0; every earlier chapter "
                   "read it at a single instant, this one reads it OVER TIME. g=1.0 universal R19 scale, fold = the "
                   "engine's own spinodal(g), no free constant; all grids are swept stimulus probes (anti-tuning). Four "
                   "results: (E2.1) sweeping the field up then down, the up/down transitions sit on OPPOSITE sides of "
                   "zero (h_up=+0.39, h_dn=−0.39 on the grid), enclosing a hysteresis loop of width 2·spinodal≈0.77 "
                   "predicted as twice the fold — a state, once switched, resists switching back; (E2.2) the transition "
                   "latency DIVERGES as the drive approaches the fold (critical slowing) and falls monotonically as it "
                   "overshoots (73.4→1.36) — small overshoot gives a slow run-up, large overshoot an abrupt jump — which "
                   "CLOSES the ictal time-course the epilepsy chapter (§25) explicitly OWED to E2; (E2.3) spinodal(g) "
                   "rises monotonically with the well depth (0.18 at g=0.6 → 0.64 at g=1.4), so the SAME handle that "
                   "sets the barrier sets the SWITCHING THRESHOLD — shallow wells flip under a fixed drive, deep wells "
                   "hold; (E2.4) const-drive integration reproduces the engine's settle BIT-FOR-BIT with the fold read "
                   "from the engine, so the layer adds without altering (engine e61083ae…, tree 0fbf4988…, byte-"
                   "unchanged). Axis-A firewall: a bistable transition is a mechanism boundary, not a claim about the "
                   "felt quality of a mood state (consciousness_claim=0). E2 is the LAYER, not a disorder; bipolar (T2b), "
                   "the ictal onset, and the cycle disorders import it. efficacy=0; not medical advice; hard problem OPEN.",
        "canonical": "28-state-switching",
        "check": None,
    },
    "bipolar_state_switching": {
        "label": "bipolar = two operating poles on ONE valence axis; episodes are bistable switches, kindling is the retained trace",
        "value": "mania sits above health and depression below (one axis, two excursions); an episode is a bistable transition (E2 hysteresis+latency); kindling is the E0 trace accumulating across episodes (each switch easier); the mood-stabiliser sign is barrier-raising",
        "grade": "[V mech]",
        "meaning": "bipolar is the second TEMPORAL disorder and the first to USE the state-switching layer: it IMPORTS "
                   "both PlasticConnectome (E0, the slow trace) and BistableSwitch (E2, the fast switch) and re-derives "
                   "neither. The axis is the engine's own M17 valence geometry (dopaminergic approach pole, M18 cortisol "
                   "cascade on the withdrawal pole), mapped to a sustained bias through the SAME coupling map "
                   "k=κ/(1−|b|)[approach]/κ/(1+|b|)[withdrawal] cap 2κ the SZ/epilepsy/E0 modules use — no new constant; "
                   "every sign holds over a severity sweep. Five results: (B1) an approach bias raises the global order "
                   "parameter ABOVE health (R=0.422>0.390), a withdrawal bias lowers it BELOW (0.367<0.390), euthymia is "
                   "the anchor between, ordering depressive<euthymic<manic monotone — NOT two diseases but two excursions "
                   "on one axis; (B2) an episode is a bistable transition inheriting E2's hysteresis (loop 2·spinodal≈0.77) "
                   "and its latency falling with overshoot (31.6→1.9), so an episode is entered at one fold and only left "
                   "at the other (it persists past its trigger) and a slow approach gives a prodromal run-up; (B3) "
                   "kindling = the E0 trace accumulating across alternating manic/depressive episodes (‖ΔW‖ deepening "
                   "0.06→0.11→0.17→0.22→0.27→0.33 over episode count, across an η sweep), and a deeper trace LOWERS the "
                   "barrier so each subsequent switch needs less drive — history makes the next episode easier; (B4) the "
                   "mood-stabiliser sign is whatever RAISES the barrier — raising the well depth raises the flip threshold "
                   "(0.38→0.44→0.51→0.64) so both manic and depressive switches become harder to enter (the direct "
                   "counterpart of kindling); (B5) η=0/no-bias reproduces the frozen M9 anchor R=0.38961455156044245 "
                   "bit-for-bit, W identical, static==settle (engine e61083ae…, tree 0fbf4988…, byte-unchanged). Bipolar "
                   "is what E2 and E0 do TOGETHER on the valence axis, no third mechanism invented. Axis-A firewall: a "
                   "bistable transition and a retained trace are mechanism boundaries, not a claim about the felt quality "
                   "of a mood state (consciousness_claim=0). Heterogeneity (bipolar I/II, cyclothymia, mixed states, rapid "
                   "cycling, psychosis) is LOCKED. Addiction (T3a, sensitisation) is owed. efficacy=0; not medical advice; "
                   "hard problem OPEN.",
        "canonical": "29-bipolar-state-switching",
        "check": None,
    },
    "bipolar_threshold_levers": {
        "label": "the §29 mood-stabiliser barrier-raise decomposed into a DNA-grounded three-lever target map",
        "value": "the abstract barrier-raising operator of B4 is resolved into three concrete levers (L1 reduce inward excitatory current, L2 increase outward K+ current, L3 remove the upstream circadian/HPA drive) over 16 bipolar excitability genes placed by their own promoter switch stiffness; targets are ranked, never drugs or doses",
        "grade": "[V map · O links]",
        "meaning": "the bipolar chapter's B4 proved the mood-stabiliser SIGN is barrier-raising but treated the "
                   "stabiliser as ONE undifferentiated operator -- it never said WHICH genes or channels realise "
                   "the barrier-raise. This module inherits the threshold-shift intervention logic from the "
                   "analgesic reproducibility package (Zenodo 10.5281/zenodo.20733420) and uses it to DECOMPOSE "
                   "that single operator into a three-lever target map on the SAME R19 substrate, with NO new "
                   "mechanism and NO new tuned constant. A symptom is a firing-threshold crossing and an "
                   "intervention is a controlled UPWARD shift of that threshold, reachable three ways: (L1) reduce "
                   "the inward, excitatory current -- the voltage-gated Ca2+/Na+/NMDA set CACNA1C, CACNA1D, "
                   "CACNA1I, SCN2A, GRIN2A, with CACNB2 and ANK3 L1-adjacent; (L2) increase the outward, "
                   "repolarising K+ current -- the KCNQ2/KCNQ3 M-current pair and KCNB1; (L3) remove the "
                   "up-stream sensitising drive -- the circadian/HPA set ARNTL(BMAL1), CLOCK, PER2, NR3C1, CRHR1 "
                   "and GSK3B (lithium's best-characterised molecular target). Each gene's gamma = -mean(nearest-"
                   "neighbour stacking dG, SantaLucia 1998) is read from its OWN promoter window (TSS-2000..+500, "
                   "Homo sapiens) and turned into that promoter's switch stiffness |h_sp| = spinodal(gamma) and "
                   "barrier = gamma^2/4 using the frozen engine READ-ONLY -- the identical pipeline the analgesic "
                   "package ran for the Na_V channels, and the identical R19 primitive the bipolar chapter uses. "
                   "Three fail-closed disciplines ride along: an L3-honesty gate keeps every L3 mechanism link "
                   "graded [O] cited biology (never derived); a forbidden-claim scanner rejects any dose, efficacy, "
                   "safety or synthesis statement (with a planted self-test that must fire); and a burden-weighted "
                   "prioritisation ranks TARGETS (CACNA1C and ANK3 top the genetic-burden tier, GSK3B and the "
                   "circadian set follow) with the gamma read carried alongside as structural context but NEVER "
                   "folded into the score. FIREWALL (non-negotiable): the promoter |h_sp| is the gene's own "
                   "switch stiffness, NEVER equated with the sec.29 network mood-switch barrier g, nor with a "
                   "channel's activation voltage, a drug's potency, a dose, an in-vivo selectivity, or a clinical "
                   "effect. Registered in run_all_atlas.py as the 8th atlas citizen (BIP-T2b-L), reproducing "
                   "bit-for-bit with engine byte-unchanged. medium_efficacy_tested=0; ranks targets not drugs; "
                   "not medical advice; hard problem OPEN.",
        "canonical": "30-bipolar-threshold-levers",
        "check": None,
    },
    "epilepsy_threshold_levers": {
        "label": "the §25 over-synchronisation threshold-raise decomposed into a DNA-grounded three-lever target map",
        "value": "the abstract over-sync-threshold-raising push of §25 is resolved into three concrete levers (L1 reduce inward Na/Ca/NMDA current, L2 increase outward K+ current -- the dominant lever, the retigabine M-current axis, L3 remove the upstream mTOR drive) over 16 epilepsy excitability genes placed by their own promoter switch stiffness; targets are ranked, never drugs or doses",
        "grade": "[V map · O links]",
        "meaning": "the epilepsy chapter (§25) proved seizures are the network crossing an over-synchronisation "
                   "threshold on the global order parameter R and that the corrective SIGN is threshold-raising, "
                   "but it treated that push as ONE undifferentiated operator -- it never said WHICH genes or "
                   "channels realise the raise. This module applies the SAME threshold-shift intervention logic "
                   "the bipolar levers chapter used (inherited from the analgesic reproducibility package, Zenodo "
                   "10.5281/zenodo.20733420) to DECOMPOSE that single operator into a three-lever target map on "
                   "the SAME R19 substrate, with NO new mechanism and NO new tuned constant. A symptom is a "
                   "firing-threshold crossing and an intervention is a controlled UPWARD shift of that threshold, "
                   "reachable three ways: (L1) reduce the inward, excitatory current -- the voltage-gated "
                   "Na+/Ca2+/NMDA set SCN1A, SCN2A, SCN8A, CACNA1A, CACNA1H, GRIN2A; (L2, DOMINANT) increase the "
                   "outward, repolarising K+ current -- the KCNQ2/KCNQ3 M-current pair (the retigabine target), "
                   "KCNB1, KCNA1 and KCNT1, with the inhibitory GABA-A pair GABRG2/GABRA1 L2-adjacent; (L3) "
                   "remove the up-stream mTOR drive -- the repressors DEPDC5, TSC1, TSC2 (the everolimus "
                   "direction). Each gene's gamma = -mean(nearest-neighbour stacking dG, SantaLucia 1998) is read "
                   "from its OWN promoter window (TSS-2000..+500, Homo sapiens) and turned into that promoter's "
                   "switch stiffness |h_sp| = spinodal(gamma) and barrier = gamma^2/4 using the frozen engine "
                   "READ-ONLY -- the identical pipeline the analgesic and bipolar packages ran, and five reads "
                   "(KCNQ2, KCNQ3, KCNB1, SCN2A, GRIN2A) are carried over VERBATIM from the bipolar promoter "
                   "cache (gamma is strand-symmetric). Two honest caveats are recorded, not hidden: KCNT1 is "
                   "sign-INVERTED (its gain-of-function is the pathology) and the L1 Na-block direction is "
                   "CONTRAINDICATED in Dravet/SCN1A loss-of-function -- exactly why gamma is graded [V] for "
                   "promoter STRUCTURE only, trait-blind, with clinical direction [O]. Three fail-closed "
                   "disciplines ride along: an L3-honesty gate keeps every mTOR link graded [O] cited biology "
                   "(never derived); a forbidden-claim scanner rejects any dose, efficacy, safety or synthesis "
                   "statement incl. seizure-freedom language (with a planted self-test that must fire); and a "
                   "burden-weighted prioritisation ranks TARGETS (SCN1A tops the genetic-burden tier but is "
                   "flagged not-actionable by the generic sign, KCNQ2 and the TSC/GATOR1 mTOR set follow) with "
                   "the gamma read carried alongside as structural context but NEVER folded into the score -- the "
                   "stiffest promoter CACNA1H sits LOW on priority while the top-priority SCN1A reads near the "
                   "softest, the decoupling that makes the firewall visible. FIREWALL (non-negotiable): the "
                   "promoter |h_sp| is the gene's own switch stiffness, NEVER equated with the sec.25 network "
                   "over-sync threshold on R, nor with a channel's activation voltage, a drug's potency, a dose, "
                   "an in-vivo selectivity, or a clinical effect. Registered in run_all_atlas.py as the 9th atlas "
                   "citizen (EPI-T2a-L), reproducing bit-for-bit with engine byte-unchanged. "
                   "medium_efficacy_tested=0; ranks targets not drugs; not medical advice; hard problem OPEN.",
        "canonical": "31-epilepsy-threshold-levers",
        "check": None,
    },
    "depression_threshold_levers": {
        "label": "the §27 low-coordination operating-point restoration decomposed into a DNA-grounded three-lever target map (L3-dominant)",
        "value": "the abstract operating-point-restoring push of §27 is resolved into three concrete levers (L1 modulate inward glutamatergic/Ca current, L2 increase outward K+/GABA-A current, L3 -- the DOMINANT lever -- remove the upstream HPA drive and restore the deficient monoamine and neurotrophic drives) over 18 depression genes placed by their own promoter switch stiffness; the first L3-dominant case and the corrective sign is flipped (restore deficient, not reduce excess); targets are ranked, never drugs or doses",
        "grade": "[V map · O links]",
        "meaning": "the depression chapter (§27) proved major depression is the chronification of a LOW-coordination "
                   "operating point on the global order parameter R -- a sustained HPA-driven withdrawal holds R "
                   "below health and plasticity consolidates the excursion -- and that the corrective SIGN is to "
                   "RESTORE the deficient drive (or remove the chronic-stress drive), but it treated that push as "
                   "ONE undifferentiated operator -- it never said WHICH drives realise the restoration. This "
                   "module applies the SAME threshold-shift intervention logic the bipolar and epilepsy levers "
                   "chapters used (inherited from the analgesic reproducibility package, Zenodo "
                   "10.5281/zenodo.20733420) to DECOMPOSE that single operator into a three-lever target map on "
                   "the SAME R19 substrate, with NO new mechanism and NO new tuned constant. Depression is the "
                   "FIRST L3-DOMINANT case: of 18 genes, 12 sit on L3 -- (a) HPA REMOVE: NR3C1 (restore "
                   "glucocorticoid-receptor negative feedback), CRHR1, FKBP5; (b) monoamine RESTORE: SLC6A4 "
                   "(SSRI site), SLC6A2 (SNRI site), MAOA (MAOI site), TPH2, HTR1A, HTR2A, COMT; (c) neurotrophic "
                   "RESTORE: BDNF, NTRK2 (the convergence point where the rapid-acting and monoamine routes meet) "
                   "-- while only L1 (the inward glutamatergic/Ca set GRIN2A, GRIN2B, CACNA1C) and L2 (the outward "
                   "K+/GABA-A set KCNQ2, KCNQ3, GABRA1) carry three genes each. This is the disorder-level SIGN "
                   "FLIP, stated not hidden: epilepsy/bipolar mania sit ABOVE health (reduce the excess) but "
                   "depression sits BELOW health (restore the deficient) -- the three abstract levers carry over, "
                   "the direction is mirrored. Each gene's gamma = -mean(nearest-neighbour stacking dG, SantaLucia "
                   "1998) is read from its OWN promoter window (TSS-2000..+500, Homo sapiens) and turned into that "
                   "promoter's switch stiffness |h_sp| = spinodal(gamma) and barrier = gamma^2/4 using the frozen "
                   "engine READ-ONLY -- the identical pipeline the analgesic, bipolar and epilepsy packages ran, "
                   "and seven reads (NR3C1, CRHR1, GRIN2A, CACNA1C, KCNQ2, KCNQ3 from the bipolar cache, GABRA1 "
                   "from the epilepsy cache) are carried over VERBATIM (gamma is strand-symmetric). Two honest "
                   "caveats are recorded, not hidden: the L1 glutamatergic direction is an NMDA ANTAGONIST (the "
                   "ketamine/esketamine route) acting via DOWNSTREAM BDNF/TrkB signalling, NOT an excitation "
                   "reduction, so its naive L1 sign is flagged sign-subtle; and the HTR2A direction is "
                   "NON-MONOTONE (an agonist psychedelic route and an antagonist route both appear) -- exactly why "
                   "gamma is graded [V] for promoter STRUCTURE only, trait-blind, with clinical direction [O]. "
                   "Three fail-closed disciplines ride along: an L3-honesty gate keeps every upstream-drive link "
                   "graded [O] cited biology (never derived) AND asserts L3 is dominant; a forbidden-claim scanner "
                   "rejects any dose, efficacy, safety or synthesis statement incl. mood-lift and remission "
                   "language (with a planted self-test that must fire); and a burden-weighted prioritisation ranks "
                   "TARGETS (BDNF tops the genetic and unmet-need tiers, followed by FKBP5, GRIN2B and NR3C1; the "
                   "unmet-need weight lifts upstream HPA/neurotrophic targets above the well-served monoamine "
                   "transporters; KCNQ2, KCNQ3 and CACNA1C are flagged not-actionable by the generic sign) with "
                   "the gamma read carried alongside as structural context but NEVER folded into the score -- the "
                   "stiffest promoter KCNQ2 (a minor exploratory L2 lever) sits LOW on priority while the "
                   "top-priority BDNF reads mid-range, the decoupling that makes the firewall visible. FIREWALL "
                   "(non-negotiable): the promoter |h_sp| is the gene's own switch stiffness, NEVER equated with "
                   "the sec.27 network operating-point on R, nor with a receptor occupancy, a synaptic monoamine "
                   "level, a drug's potency, a dose, an in-vivo selectivity, or a clinical effect. Registered in "
                   "run_all_atlas.py as the 10th atlas citizen (DEP-T1b-L), reproducing bit-for-bit with engine "
                   "byte-unchanged. medium_efficacy_tested=0; ranks targets not drugs; not medical advice; hard "
                   "problem OPEN.",
        "canonical": "32-depression-threshold-levers",
        "check": None,
    },
    "schizophrenia_threshold_levers": {
        "label": "the §24 over-ignition operating-point correction decomposed into a DNA-grounded three-lever target map (L1+L3 co-dominant, positive-domain only)",
        "value": "the abstract over-ignition-correcting push of §24 is resolved into three concrete levers (L1 modulate inward glutamatergic/NMDA current, L3 remove the up-stream dopamine drive -- L1 and L3 CO-DOMINANT -- L2 increase outward GABA-A current as the minor lever) over 14 schizophrenia genes placed by their own promoter switch stiffness; the first L1+L3 co-dominant case AND the first domain-restricted case (the map reaches the positive domain only -- the negative and cognitive domains are not reached); targets are ranked, never drugs or doses",
        "grade": "[V map · O links]",
        "meaning": "the schizophrenia chapter (§24) proved the positive symptoms are an OVER-IGNITION / aberrant-salience "
                   "operating point on the global order parameter R -- the ignition fold sits too low so weak internally "
                   "generated assemblies ignite as hallucinations/delusions -- and that the corrective SIGN is to REDUCE "
                   "the excess drive (or raise the fold), the SAME direction as epilepsy/bipolar mania; §24 also proved "
                   "schizophrenia is NOT one axis but three distinct domains (positive/negative/cognitive). This module "
                   "applies the SAME threshold-shift intervention logic the bipolar, epilepsy and depression levers "
                   "chapters used (inherited from the analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) "
                   "to DECOMPOSE that single operator into a three-lever target map on the SAME R19 substrate, with NO "
                   "new mechanism and NO new tuned constant. Schizophrenia is the FIRST L1+L3 CO-DOMINANT case: of 14 "
                   "genes, 6 sit on L1 (the glutamate/NMDA inward axis GRIN1, GRIN2A, GRIN2B, GRIA3, CACNA1C, CACNB2) "
                   "and 6 on L3 (the dopamine up-stream axis in three sub-axes: receptors DRD2, DRD4; synthesis/transport "
                   "TH, SLC6A3; serotonergic/catabolic HTR2A, COMT), while only L2 (the GABA-A pair GABRA1, GABRB3) is "
                   "minor -- the two leading pathophysiologies (glutamate hypofunction + dopamine) loaded on the map at "
                   "once. The NEW structural finding is the DOMAIN RESTRICTION: the gain-reducing scalar lever reverses "
                   "the POSITIVE domain ONLY; the NEGATIVE (output/gain deficit) and COGNITIVE (long-range wiring/"
                   "dysconnection) domains are NOT reached -- a threshold shift cannot lift a deficit by lowering a fold "
                   "nor re-route geometry (the §19 result), so the map records a domain-restriction witness (positive "
                   "reached, negative/cognitive not), axis-structured not dose-structured. Each gene's gamma = "
                   "-mean(nearest-neighbour stacking dG, SantaLucia 1998) is read from its OWN promoter window "
                   "(TSS-2000..+500, Homo sapiens) and turned into that promoter's switch stiffness |h_sp| = "
                   "spinodal(gamma) and barrier = gamma^2/4 using the frozen engine READ-ONLY -- the identical pipeline "
                   "the analgesic, bipolar, epilepsy and depression packages ran, and seven reads (GRIN2A, CACNA1C, "
                   "CACNB2 from the bipolar cache, GRIN2B, COMT, HTR2A, GABRA1 from the depression cache) are carried "
                   "over VERBATIM (gamma is strand-symmetric). Two honest caveats are recorded, not hidden: the L1 "
                   "NMDA-HYPOFUNCTION direction is sign-subtle (the leading model is parvalbumin-interneuron NMDA "
                   "hypofunction that DISINHIBITS downstream circuits, so a glycine-site AGONIST direction appears "
                   "alongside the naive reduce-excitation sign -- the SZ analogue of depression's ketamine caveat); and "
                   "the HTR2A direction is NON-MONOTONE -- exactly why gamma is graded [V] for promoter STRUCTURE only, "
                   "trait-blind, with clinical direction [O]. Three fail-closed disciplines ride along: an L3-honesty "
                   "gate keeps every dopamine-axis link graded [O] cited biology (never derived) AND asserts L1+L3 "
                   "co-dominance AND the positive-domain restriction; a forbidden-claim scanner rejects any dose, "
                   "efficacy, safety or synthesis statement incl. treats-psychosis, remission and relapse-prevention "
                   "language (with a planted self-test that must fire); and a burden-weighted prioritisation ranks "
                   "TARGETS (GRIN2A tops the genetic and unmet-need tiers, and the unmet-need weight lifts the "
                   "glutamatergic L1 axis ABOVE the established D2 route because D2 is already the established axis; "
                   "CACNA1C, CACNB2, DRD4, GABRB3 and SLC6A3 are flagged not-actionable by the generic sign -- SLC6A3 "
                   "because DAT blockade RAISES dopamine, the wrong direction) with the gamma read carried alongside as "
                   "structural context but NEVER folded into the score -- the stiffest promoter SLC6A3 sits LOW on "
                   "priority and non-actionable while the top-priority GRIN2A reads mid-range, the decoupling that makes "
                   "the firewall visible. FIREWALL (non-negotiable): the promoter |h_sp| is the gene's own switch "
                   "stiffness, NEVER equated with the sec.24 network over-ignition threshold on R, nor with a receptor "
                   "occupancy, a synaptic dopamine level, a drug's potency, a dose, an in-vivo selectivity, or a "
                   "clinical effect. Registered in run_all_atlas.py as the 11th atlas citizen (SZ-T1a-L), reproducing "
                   "bit-for-bit with engine byte-unchanged. medium_efficacy_tested=0; ranks targets not drugs; not "
                   "medical advice; hard problem OPEN.",
        "canonical": "33-schizophrenia-threshold-levers",
        "check": None,
    },
    "autism_threshold_levers": {
        "label": "the §18-19 E/I over-excitation operating-point correction decomposed into a DNA-grounded three-lever target map (L1-dominant, L3-sparse, T-axis only; the out-of-reach O/W axes named and §19-proven)",
        "value": "the abstract over-excitation-correcting push of §18-19 is resolved into three concrete levers (L1 reduce inward glutamatergic/Na/Ca current -- DOMINANT, 5 targets; L2 increase outward K+ / restore GABA-A current, 4 targets; L3 remove the up-stream serotonergic drive -- SPARSE, 1 cautious [O] node) over 10 autism E/I genes placed by their own promoter switch stiffness, unifying the pre-existing autism_multilever_threshold.py under the formal L1/L2/L3 frame; the map reaches the excitability/threshold (T) axis ONLY -- the output-deficit (O) and long-range-wiring (W) axes are NAMED with six real genes but explicitly NOT reachable, and W-unreachability is PROVEN (not asserted) by §19; targets are ranked, never drugs or doses",
        "grade": "[V map · O links]",
        "meaning": "the autism chapters (§18-19) proved autism is NOT one axis but three distinct fault axes -- "
                   "T (excitability / E-I threshold, an over-excitation operating point whose ignition fold sits "
                   "too low), O (synaptic gain / output deficit), and W (long-range wiring / connectivity) -- and "
                   "that of these only the T axis is reachable by a scalar chemical lever, whose corrective SIGN "
                   "is to REDUCE the excess drive / restore inhibition (raise the fold), the SAME direction as "
                   "epilepsy/schizophrenia-positive. This module applies the SAME threshold-shift intervention "
                   "logic the bipolar, epilepsy, depression and schizophrenia levers chapters used (inherited from "
                   "the analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) to UNIFY the pre-existing "
                   "autism_multilever_threshold.py (which carried the idea under informal A1/A2/A3 levers) into a "
                   "DNA-grounded three-lever target map on the SAME R19 substrate, with NO new mechanism and NO new "
                   "tuned constant. Autism is L1-DOMINANT with a nearly-empty L3 -- the 5th distribution pattern "
                   "across the threshold-levers series (epilepsy L1+L2, depression L3, schizophrenia L1+L3 "
                   "co-dominant, bipolar channel-led): of 10 lever genes, 5 sit on L1 (the excitatory-reduce axis "
                   "GRIN2A, GRIN2B, GRIA1, SCN2A, CACNA1C), 4 on L2 (the inhibitory-restore axis KCNQ3, GABRB3, "
                   "GABRA5, GABRA2), and just 1 on L3 (SLC6A4, a cautious non-monotone serotonergic node, graded "
                   "[O]) -- the L3-sparsity is itself the finding that autism's actionable biology sits locally on "
                   "the E/I set, with no clean up-stream drug drive. The TWO structural strengthenings beyond the "
                   "schizophrenia domain-restriction template are: (1) the OUT-OF-REACH axes are NAMED with six real "
                   "genes -- O (output/gain deficit) = SHANK3, SYNGAP1, NRXN1; W (long-range wiring/dysconnection) = "
                   "CNTNAP2, RELN; plus the syndromic master MECP2 -- carried alongside the map but explicitly NOT "
                   "levers (a gain-reducing scalar push would drive an output deficit LOWER, and cannot re-route "
                   "geometry); and (2) the W-axis unreachability is PROVEN, not merely asserted -- §19 "
                   "(autism_candidate_limits) showed a scalar threshold lever can only MASK the wiring fault via "
                   "over-synchronisation (the seizure analogue: P5_threshold_lowering_is_mask_not_correction), never "
                   "CORRECT it (P4_chemical_cannot_fix_W). Each gene's gamma = -mean(nearest-neighbour stacking dG, "
                   "SantaLucia 1998) is read from its OWN promoter window (TSS-2000..+500, Homo sapiens) and turned "
                   "into that promoter's switch stiffness |h_sp| = spinodal(gamma) and barrier = gamma^2/4 using the "
                   "frozen engine READ-ONLY -- the identical pipeline the analgesic, bipolar, epilepsy, depression "
                   "and schizophrenia packages ran, and seven reads (GRIN2A, GRIN2B, CACNA1C, GABRB3 from the "
                   "schizophrenia cache, SCN2A, KCNQ3 from the bipolar cache, SLC6A4 from the depression cache) are "
                   "carried over VERBATIM (gamma is strand-symmetric, bit-identical). Two honest caveats are "
                   "recorded, not hidden: SCN2A and GRIN2B are GoF/LoF SIGN-SUBTLE (a gain-of-function pushes the "
                   "early-infantile DEE/seizure pole while a loss-of-function pushes the milder ASD/ID pole -- "
                   "opposite directions), and the T-lever pushed TOO HARD is itself the seizure edge (the real "
                   "ASD+epilepsy comorbidity) -- exactly why gamma is graded [V] for promoter STRUCTURE only, "
                   "trait-blind, with clinical direction [O]. Three fail-closed disciplines ride along: an "
                   "L3-honesty gate keeps the serotonergic link graded [O] cited biology (never derived) AND asserts "
                   "L1 UNIQUE dominance, L3 SPARSITY, the T-axis domain restriction, and the NAMED + §19-proven O/W "
                   "out-of-reach axes; a forbidden-claim scanner rejects any dose, efficacy, safety or synthesis "
                   "statement PLUS -- uniquely for this YMYL topic -- an autism QUACKERY class (chelation, MMS / "
                   "miracle-mineral / chlorine-dioxide bleach protocols) and a NORMALISE-framing class that protects "
                   "neurodiversity respect (autism is a neurodevelopmental DIFFERENCE, not only a deficit; the map "
                   "never emits cure/normalise/fix-autism language), each with a planted self-test that must fire; "
                   "and a burden-weighted prioritisation ranks TARGETS with the gamma read carried alongside as "
                   "structural context but NEVER folded into the score. The AUTISM unmet-need signature is that "
                   "there is NO approved CORE-feature pharmacology (only the irritability adjunct is licensed), so -- "
                   "unlike schizophrenia where the established D2 route lowers DRD2's unmet need -- U stays uniformly "
                   "HIGH, and the L2 INHIBITORY-RESTORE route surfaces as the cleanest ACTIONABLE direction precisely "
                   "because the high-scoring L1 excitatory genes are GoF/LoF sign-subtle (SCN2A/GRIN2B) or "
                   "cross-disorder set-points (CACNA1C); the stiffest promoter SLC6A4 sits LOWEST on priority and "
                   "non-actionable while the top-priority GABRB3 reads mid-range, the decoupling that makes the "
                   "firewall visible. FIREWALL (non-negotiable): the promoter |h_sp| is the gene's own switch "
                   "stiffness, NEVER equated with the §18 network over-excitation fold (the E/I ignition threshold "
                   "on R), nor with a receptor occupancy, a synaptic level, a drug's potency, a dose, an in-vivo "
                   "selectivity, or a clinical effect. Registered in run_all_atlas.py as the 12th atlas citizen "
                   "(ASD-T-L), reproducing bit-for-bit with engine byte-unchanged. medium_efficacy_tested=0; ranks "
                   "targets not drugs; not medical advice; autism is a difference not only a deficit; hard problem "
                   "OPEN.",
        "canonical": "34-autism-threshold-levers",
        "check": None,
    },
    "adhd_threshold_levers": {
        "label": "the §22 ADHD gain/arousal substrate mapped onto the threshold-shift frame -- L3-ONLY (5 drive-tone levers; L1/L2 BOTH empty), the dominant gain-amplitude axis NAMED but out of reach, wiring ABSENT; the FIRST PARTIAL [L] fit in the series",
        "value": "the §22 adhd_axis_specific substrate (gain/arousal, intact wiring) is mapped onto the inherited L1/L2/L3 threshold frame by REACHABILITY and loads ENTIRELY on L3 (the up-stream catecholamine/monoaminergic drive): 5 drive-tone levers (SLC6A3/DAT, SLC6A2/NET, SLC6A4/SERT, ADRA2A/alpha-2A, DRD4/D4) with L1 and L2 BOTH EMPTY -- the 6th distribution pattern and the purest L3 case; the DOMINANT axis GA (gain-amplitude: catecholamine SYNTHESIS TH/DBH, RELEASE SNAP25, catabolic clearance COMT boundary) is NAMED with 4 real genes (gamma carried alongside) but explicitly NOT reachable by a drive-tone lever; W (wiring) is ABSENT (intact wiring, zero genes -- the discriminant from autism); the fit is PARTIAL [L], the FIRST and only non-clean fit across six disorders; targets ranked, never drugs or doses; no stimulant-misuse or cognitive-enhancement licence",
        "grade": "[L partial · O links]",
        "meaning": "the ADHD-vs-autism chapter (§22) proved ADHD is NOT a milder autism but a different fault: a "
                   "disorder of GAIN and AROUSAL with INTACT WIRING -- an explicit gene substrate of six output/gain "
                   "genes, two arousal/threshold genes, ZERO wiring genes (axis-ambiguous/syndromic genes FOXP2 and "
                   "ADGRL3 pre-registered OUT to keep the 'intact wiring' discriminant airtight). This module applies "
                   "the SAME threshold-shift intervention logic the bipolar, epilepsy, depression, schizophrenia and "
                   "autism levers chapters used (inherited from the analgesic reproducibility package, Zenodo "
                   "10.5281/zenodo.20733420) to that substrate on the SAME R19 engine, READ-ONLY, with NO new "
                   "mechanism and NO new tuned constant -- and it produces the FIRST PARTIAL [L] fit in the series. "
                   "Mapped by REACHABILITY, ADHD is L3-ONLY: of 5 lever genes ALL 5 sit on L3 (the up-stream "
                   "catecholamine/monoaminergic drive -- SLC6A3/DAT and DRD4/D4, §22-O gain genes reachable HERE as "
                   "drive-TONE; SLC6A4/SERT and ADRA2A/alpha-2A, §22-T arousal tone; SLC6A2/NET, the atomoxetine arm "
                   "extending the substrate), and L1 and L2 are BOTH EMPTY -- the 6th distribution pattern across the "
                   "series (bipolar L1, epilepsy L1+L2, depression L3-dominant, schizophrenia L1+L3 co-dominant, "
                   "autism L1-dominant) and the PUREST L3 case. The L1/L2 EMPTINESS is itself a finding: ADHD is NOT a "
                   "channelopathy -- it has no ionic fold lever, only the [O] cited-biology drive surface (where the "
                   "stimulant/atomoxetine/guanfacine arms live, as DIRECTIONS). The fit is PARTIAL [L] for a two-sided "
                   "reason. (1) The DOMINANT ADHD axis is OUT OF REACH: ADHD is a GAIN/AROUSAL disorder, not a "
                   "firing-FOLD disorder, and the threshold frame operates on the fold via an up-stream DRIVE lever, "
                   "so it reaches ADHD only through the SECONDARY drive-tone surface and NOT through the GA "
                   "gain-amplitude machinery (synthesis/release), which is the dominant fault -- the GA axis is NAMED "
                   "with four real genes (TH rate-limiting catecholamine synthesis, DBH DA->NA synthesis, SNAP25 SNARE "
                   "release output, COMT prefrontal catabolic clearance boundary), each carried with its own promoter "
                   "gamma read ALONGSIDE but graded [F] NOT REACHED -- the autism O-axis named-out-of-reach discipline "
                   "(§34), here applied to the DOMINANT axis. (2) A second sense of partial: the frame has NO "
                   "structural [F] grounding on ADHD at all -- the [F] ionic levers L1/L2 are empty, leaving only the "
                   "[O] drive surface. And W is ABSENT (intact wiring, zero genes) -- the discriminant from autism, "
                   "which carried a W axis §19-PROVEN unreachable. This is the precise INVERSE of autism: autism "
                   "REACHED its dominant axis (excitability) and missed O+W; ADHD reaches only the SECONDARY axis "
                   "(drive-tone) and misses the DOMINANT axis (gain), with no W axis at all. Each gene's gamma = "
                   "-mean(nearest-neighbour stacking dG, SantaLucia 1998) is read from its OWN promoter window "
                   "(TSS-2000..+500, Homo sapiens) and turned into that promoter's switch stiffness |h_sp| = "
                   "spinodal(gamma) and barrier = gamma^2/4 using the frozen engine READ-ONLY -- the identical "
                   "pipeline the analgesic, bipolar, epilepsy, depression, schizophrenia and autism packages ran, and "
                   "six reads (SLC6A3, DRD4, SLC6A4, TH, COMT from the depression/schizophrenia caches) are carried "
                   "over VERBATIM (gamma is strand-symmetric, bit-identical), with ADRA2A, DBH, SNAP25 live GRCh38 "
                   "strand-aware reads. The DNA reads carry an INVERSION that names itself: the STIFFEST promoter in "
                   "the set, the dopamine transporter SLC6A3 (gamma~1.598, |h_sp|~0.778), is a REACHABLE drive-tone "
                   "lever, while the SOFTEST, the SNARE release gene SNAP25 (gamma~1.438, |h_sp|~0.664), is an "
                   "OUT-OF-REACH gain gene -- the exact opposite of autism, where the stiffest reads were the "
                   "out-of-reach genes. Three fail-closed disciplines ride along: an L3-honesty gate keeps all five "
                   "drive-tone links graded [O] cited biology (never derived) AND asserts L3 UNIQUE dominance, L1==L2"
                   "==0 emptiness, the GA-axis named-out-of-reach, the W-axis ABSENCE, and the PARTIAL [L] grade; a "
                   "forbidden-claim scanner -- the STRICTEST in the series -- rejects any dose/efficacy/safety/"
                   "synthesis statement PLUS two stimulant-topic classes: a STIMULANT-MISUSE class (get-high/snort/"
                   "euphoria/recreational/party-drug) and a COGNITIVE-ENHANCEMENT class (smart-drug/study-drug/"
                   "nootropic/boost-focus/limitless), both NEGATION-GUARDED with planted self-tests that must fire; "
                   "and a burden-weighted prioritisation ranks all 9 TARGETS with the gamma read carried alongside but "
                   "NEVER folded into the score. The ADHD unmet-need signature is the INVERSE of autism's: ADHD HAS "
                   "established core routes (DAT/stimulant, NET/atomoxetine, alpha-2A/guanfacine), so the reachable "
                   "drive-tone transporters carry LOW unmet need (the LOWEST floor in the series), while the "
                   "out-of-reach gain genes carry the unmet-need CEILING but are flagged not-actionable -- so the "
                   "highest-burden targets (TH #1, DRD4 #2, DBH #3, SNAP25 #4) are all NON-actionable and the leading "
                   "ACTIONABLE target SLC6A3/DAT sits only at #5 (lowered by its established-route low unmet). "
                   "DECOUPLING (the firewall made visible, INVERSE of autism's): the stiffest promoter SLC6A3 sits at "
                   "priority #5 not the top, while the top-priority TH has only the third-stiffest read. FIREWALL "
                   "(non-negotiable): the promoter |h_sp| is the gene's own switch stiffness, NEVER equated with a "
                   "transporter occupancy, a synaptic catecholamine level, a stimulant's potency, a dose, an in-vivo "
                   "selectivity, or any clinical effect. Registered in run_all_atlas.py as the 13th atlas citizen "
                   "(ADHD-T-L), reproducing bit-for-bit with engine byte-unchanged. medium_efficacy_tested=0; ranks "
                   "targets not drugs; not medical advice; no stimulant-misuse or cognitive-enhancement licence; ADHD "
                   "is a difference in regulation not a deficit of worth; hard problem OPEN.",
        "canonical": "35-adhd-threshold-levers",
        "check": None,
    },
    "addiction_threshold_levers": {
        "label": "the §28 state-switching / §26 E0 plasticity incentive-sensitisation substrate mapped onto the threshold-shift frame -- L3-DOMINANT with L1 AND L2 BOTH PRESENT (5 reward-drive + 2 glutamate-plasticity + 2 inhibitory-restore levers), the dominant consolidated-sensitisation-gain axis NAMED but out of reach; the SECOND PARTIAL [L] fit, the convergence with the E0 dynamics layer",
        "value": "the §28/§26 incentive-sensitisation substrate (repeated exposure trains the reward circuit into a consolidated low-threshold attractor whose reward GAIN persists after withdrawal) is mapped onto the inherited L1/L2/L3 threshold frame by REACHABILITY and loads MOST on L3 (the up-stream reward drive) while ALSO engaging the ionic levers: 5 reward-drive levers (OPRM1/mu-opioid, OPRK1/kappa-opioid, DRD2/D2, SLC6A3/DAT, CHRNA5/nAChR), 2 glutamate-plasticity-substrate levers (GRIN2A/GRIN2B), 2 inhibitory-restore levers (GABRA2/GABRG3) -- the 7th distribution pattern and the TEXTURAL INVERSE of ADHD's L3-only emptiness; the DOMINANT axis SG (consolidated sensitisation gain: deltaFosB FOSB, BDNF remodelling, the CREB1 tolerance/dependence programme, ARC consolidation) is NAMED with 4 real genes (gamma carried alongside) but explicitly NOT reachable by a threshold/drive lever, because SG is a GAIN not a fold (the ADHD lesson) AND moreover CONSOLIDATED/LEARNED -- a plasticity (E0-layer) variable; the fit is PARTIAL [L], the SECOND non-clean fit, and the SG axis is precisely the E0 plasticity layer where threshold-leverisation meets the dynamics route; targets ranked, never drugs or doses; no drug-seeking or cure-miracle licence; addiction is a treatable medical condition, not a moral failing",
        "grade": "[L partial · O links]",
        "meaning": "addiction is modelled (§28 state-switching / §26 E0 plasticity) as INCENTIVE SENSITISATION: "
                   "repeated exposure TRAINS the reward circuit (a plasticity process, the E0 layer) into a "
                   "consolidated low-threshold attractor whose reward GAIN has grown and PERSISTS after withdrawal "
                   "(the relapse and cue-reactivity driver). This module applies the SAME threshold-shift "
                   "intervention logic the bipolar, epilepsy, depression, schizophrenia, autism and ADHD levers "
                   "chapters used (inherited from the analgesic reproducibility package, Zenodo "
                   "10.5281/zenodo.20733420) to that substrate on the SAME R19 engine, READ-ONLY, with NO new "
                   "mechanism and NO new tuned constant -- and it produces the SECOND PARTIAL [L] fit in the "
                   "series, for a DEEPER reason than ADHD. Mapped by REACHABILITY, addiction is L3-DOMINANT but "
                   "NOT L3-only: of 9 lever genes, 5 sit on L3 (the up-stream reward drive -- OPRM1 mu-opioid/"
                   "naltrexone, OPRK1 kappa-opioid/anti-reward, DRD2 D2/Taq1A, SLC6A3 DAT/bupropion, CHRNA5 nAChR/"
                   "varenicline), 2 on L1 (the glutamatergic plasticity substrate -- GRIN2A/GRIN2B, the acamprosate/"
                   "NAC direction) and 2 on L2 (the inhibitory-restore arm -- GABRA2/GABRG3, the topiramate "
                   "direction) -- the 7th distribution pattern across the series (bipolar L1, epilepsy L1+L2, "
                   "depression L3-dominant, schizophrenia L1+L3 co-dominant, autism L1-dominant, ADHD L3-only) and "
                   "the TEXTURAL INVERSE of ADHD's emptiness: where ADHD was 'not a channelopathy' (L1/L2 EMPTY), "
                   "addiction ENGAGES the ionic levers too -- a richer reachable surface. The fit is PARTIAL [L] "
                   "because the DOMINANT addiction fault is OUT OF REACH: the SG (consolidated sensitisation-gain) "
                   "axis -- the learned plastic trace that drives chronicity and relapse -- is NAMED with four real "
                   "genes (deltaFosB FOSB the master sensitisation switch, BDNF activity-dependent remodelling, "
                   "CREB1 the tolerance/dependence programme, ARC synaptic consolidation), each carried with its "
                   "own promoter gamma read ALONGSIDE but graded [F] NOT REACHED. This extends the ADHD "
                   "named-out-of-reach gain-axis discipline (§35) but DEEPENS it: ADHD's gain was out of reach "
                   "because a fold lever does not set a gain; addiction's gain is out of reach for that reason AND "
                   "because it is CONSOLIDATED/LEARNED -- a plasticity (E0-layer, §26) variable, so even a drive "
                   "lever that DAMPENS the instantaneous reward response cannot ERASE the durable trace. That is "
                   "the precise point where threshold-leverisation (the B-i route) structurally MEETS the E0 "
                   "dynamics route (B-ii): addiction is the CONVERGENCE, and B-i names the learned trace "
                   "out-of-reach honestly rather than overclaiming. Each gene's gamma = -mean(nearest-neighbour "
                   "stacking dG, SantaLucia 1998) is read from its OWN promoter window (TSS-2000..+500, Homo "
                   "sapiens) and turned into that promoter's switch stiffness |h_sp| = spinodal(gamma) and barrier "
                   "= gamma^2/4 using the frozen engine READ-ONLY -- the identical pipeline the analgesic, bipolar, "
                   "epilepsy, depression, schizophrenia, autism and ADHD packages ran, and six reads (DRD2 from "
                   "schizophrenia; BDNF from depression; GRIN2A, GRIN2B, GABRA2 from autism; SLC6A3 from ADHD) are "
                   "carried over VERBATIM (gamma is strand-symmetric, bit-identical), with OPRM1, OPRK1, CHRNA5, "
                   "GABRG3, FOSB, CREB1, ARC live GRCh38 strand-aware reads. Three fail-closed disciplines ride "
                   "along: an L3-honesty gate keeps all five reward-drive links graded [O] cited biology (never "
                   "derived) AND asserts L3 UNIQUE dominance, L1 AND L2 BOTH PRESENT (the ADHD inverse), the "
                   "INSTANT-axis domain restriction, the SG-axis named-out-of-reach, and the PARTIAL [L] grade; a "
                   "forbidden-claim scanner rejects any dose/efficacy/safety/synthesis statement PLUS two "
                   "addiction-topic classes: a DRUG-SEEKING class (where-to-buy/how-to-obtain/inject/snort/get-high/"
                   "euphoria/dealer) and a CURE-MIRACLE class (miracle-cure/guaranteed-sober/detox-miracle/"
                   "addiction-gone/permanently-cured), both NEGATION-GUARDED with planted self-tests that must "
                   "fire; and a burden-weighted prioritisation ranks all 13 TARGETS with the gamma read carried "
                   "alongside but NEVER folded into the score. The addiction unmet-need signature is a MIDDLE case "
                   "between ADHD and autism: addiction HAS established core routes (mu-opioid/naltrexone, nicotinic/"
                   "varenicline, DAT/bupropion, glutamate/acamprosate, GABA/topiramate) but every one is only "
                   "PARTIALLY effective with HIGH RELAPSE, so the reachable levers carry only MODERATE unmet need "
                   "(U-floor=3, ABOVE ADHD's clean-route floor of 2), while the out-of-reach SG gain genes carry "
                   "the unmet-need CEILING but are flagged not-actionable -- so the highest-need target FOSB/"
                   "deltaFosB (#1) is NON-actionable and the leading ACTIONABLE target OPRM1 sits at #2 (lowered by "
                   "its established-route partial unmet). DECOUPLING (the firewall made visible): the stiffest "
                   "promoter SLC6A3 sits at priority #9 not the top, while the top-priority FOSB has only the "
                   "seventh-stiffest read. FIREWALL (non-negotiable): the promoter |h_sp| is the gene's own switch "
                   "stiffness, NEVER equated with the consolidated sensitisation gain, a receptor occupancy, a "
                   "synaptic dopamine/opioid level, a drug's potency, a dose, an in-vivo selectivity, or any "
                   "clinical effect. Registered in run_all_atlas.py as the 14th atlas citizen (ADD-T-L), "
                   "reproducing bit-for-bit with engine byte-unchanged. efficacy_tested=0; ranks targets not "
                   "drugs; not medical advice; no route to obtain or use any substance; no claim that addiction is "
                   "cured; addiction is a treatable medical condition, not a moral failing; hard problem OPEN.",
        "canonical": "36-addiction-threshold-levers",
        "check": None,
    },
    "addiction_sensitization_dynamics": {
        "label": "the integrated sensitisation gain of addiction (the deltaFosB trace) modelled DIRECTLY on the E0 plasticity layer -- the OTHER HALF of the §36 convergence: §36 (B-i) NAMED the gain out of reach for the instant levers, this module (B-ii) MODELS it and supplies the variable that MOVES it; reward sign grounded READ-ONLY in M5 dopamine RPE; five sign-only results, all CONFIRMED over an eta sweep",
        "value": "the dominant addiction fault §36 (ADD-T-L, B-i) named OUT OF REACH for the instant L1/L2/L3 threshold levers -- the integrated sensitisation gain (the deltaFosB trace that makes addiction chronic and relapsing) -- is modelled DIRECTLY here by IMPORTING the E0 PlasticConnectome (§26) and driving it with a REWARD bias whose SIGN is grounded READ-ONLY in the engine: M5 (dopamine reward-prediction error) potentiates the rewarded eddy's laid-down probability above an unrewarded control, M4 (selection) commits a winner -- reward POTENTIATES, so a reward-exposure epoch maps to a positive reward-drive bias and the E0 phase-correlation Hebbian update accumulates it into a retained ||W-W0|| (the integrated gain as a structural quantity). Five pre-registered SIGN-only results, all CONFIRMED over an eta sweep: A1 incentive sensitisation (repeated exposure monotonically builds the trace), A2 cue-reactivity (the sensitised connectome responds MORE to the same reward cue than a naive one -- the relapse substrate; only the response-exceeds-naive sign asserted, the marginal cue gain NOT claimed monotone), A3 extinction-persistence (removing the reward does NOT return the trace to zero under plasticity, eta>0 trace > 0, while eta=0 trace == 0 exactly -- extinction removes the DRIVE, the reachable instant axis, but not the LEARNED TRACE, the out-of-reach axis: the convergence seam), A4 the plasticity-variable guard (with eta=0 the reward excursion reverts EXACTLY and W stays identical to the kernel -- the gain vanishes without plasticity, which is precisely why B-i's instant levers cannot reach it; eta=0 reproduces the frozen M9 anchor bit-for-bit), A5 the dynamics handle (SPACED/intermittent reward exposure consolidates a LARGER trace than MASSED/continuous at equal total exposure -- intermittent reinforcement sensitises more, the structural HANDLE on the trace the instant frame could not reach). The two halves of the convergence meet in one disorder: B-i names the gain unreachable for instant levers, B-ii exhibits it AND gives a structural handle on it; reuses the E0 layer, no new tuned constant, engine byte-unchanged; addiction is a chronic relapsing medical condition, not a moral failing; efficacy=0; not medical advice; no cure; no licence to use any substance; Axis-A firewall; hard problem OPEN",
        "grade": "[V mech]",
        "meaning": "addiction's dominant defect -- the INTEGRATED SENSITISATION GAIN (the deltaFosB "
                   "structural trace that makes the disorder chronic and relapsing) -- was NAMED out of "
                   "reach for the instant threshold levers in §36 (ADD-T-L, B-i), for two reasons: it is a "
                   "GAIN not a fold (the ADHD lesson -- an instant lever has no handle on amplitude) AND a "
                   "LEARNED/CONSOLIDATED plasticity variable (a memory the circuit hardened over time) that "
                   "no instant lever can move. That naming was the honest HALF of a convergence; this "
                   "module is the OTHER half -- it MODELS the trace directly via the §26 E0 plasticity "
                   "dynamics, supplying the variable that actually MOVES the trace B-i could only name. It "
                   "IMPORTS the E0 PlasticConnectome (it does NOT re-derive the phase-correlation Hebbian "
                   "rule or the coupling-vs-bias map -- handover reuse discipline) and drives it with a "
                   "REWARD bias whose SIGN is grounded READ-ONLY in the already-emerged engine: M5 emerge_"
                   "learned_field (dopamine reward-prediction error) raises a rewarded eddy's laid-down "
                   "probability well above an unrewarded control (p_target_learned >> p_target_control -- "
                   "reward POTENTIATES), and M4 emerge_selection commits a basal-ganglia winner. A reward-"
                   "exposure epoch therefore maps to a positive (excitatory) reward-drive bias b>0 (the "
                   "SAME map k=kappa/(1-|b|), capped 2*kappa; NO new constant), and the E0 Hebbian update "
                   "accumulates repeated exposure into a retained ||W-W0|| -- the integrated sensitisation "
                   "gain as a STRUCTURAL quantity. Five pre-registered SIGN-only predictions are all "
                   "CONFIRMED and all hold over an eta sweep (anti-tuning): A1 INCENTIVE SENSITISATION -- "
                   "repeated reward exposure monotonically strengthens the retained trace (the gain "
                   "accumulating, the thing a one-shot reward does not do); A2 CUE-REACTIVITY -- a "
                   "connectome sensitised by reward exposure responds MORE to the SAME reward cue than a "
                   "naive one (R_sens(cue) > R_naive(cue), resting R already >= naive: the learned trace "
                   "sits the circuit in a higher-coordination basin, so the same cue evokes a larger "
                   "coordinated response -- the cue-induced craving/relapse substrate; only the response-"
                   "exceeds-naive SIGN is asserted, the marginal cue gain is NOT claimed monotone); A3 "
                   "EXTINCTION DOES NOT ERASE -- removing the reward (baseline OFF epochs, plasticity "
                   "running) does NOT return the trace to zero (eta>0 trace stays above zero, here it even "
                   "continues to consolidate) whereas eta=0 leaves the trace EXACTLY zero, so extinction "
                   "removes the DRIVE (the B-i reachable instant axis) but not the LEARNED TRACE (the B-i "
                   "out-of-reach axis): the convergence seam, exhibited dynamically; A4 the PLASTICITY-"
                   "VARIABLE GUARD -- with eta=0 the reward excursion reverts EXACTLY when the reward bias "
                   "is removed and W stays identical to the kernel, so the integrated gain DISAPPEARS "
                   "without plasticity, proving the sensitisation axis is a LEARNED/CONSOLIDATED variable, "
                   "which is precisely why B-i's instant levers (drive or ion) cannot reach it (eta=0 "
                   "reproduces the frozen M9 anchor bit-for-bit, pure add-on); and A5 the DYNAMICS HANDLE "
                   "-- SPACED (intermittent) reward exposure consolidates a LARGER retained trace than "
                   "MASSED (continuous) at EQUAL total time-at-reward (intermittent reinforcement "
                   "sensitises MORE, the E0.2 spacing effect applied to the reward bias) -- the structural "
                   "HANDLE on the trace the instant frame could not reach. The two halves of the "
                   "convergence thus MEET in one disorder: the threshold frame (B-i) names the gain "
                   "unreachable for instant levers, the plasticity-dynamics frame (B-ii) both EXHIBITS the "
                   "gain (A1-A3) and gives a structural handle on it (A5). FIREWALL: the retained ||W-W0|| "
                   "is the integrated sensitisation gain as a STRUCTURAL quantity, NEVER a claim about the "
                   "FELT quality of craving, reward or relapse (Axis-A; consciousness_claim=0; hard problem "
                   "OPEN); real addiction plasticity is HETEROGENEOUS (deltaFosB/CREB/BDNF transcriptional "
                   "cascades, AMPA trafficking, dendritic spine remodelling, glutamatergic homeostatic "
                   "adaptation, epigenetic marks -- LOCKED), only the SIGN of a phase-correlation Hebbian "
                   "trace is asserted; the reward SIGN is grounded in M5 RPE and every MAGNITUDE (including "
                   "the rate eta and the identity of the real plasticity rule) is [O]; addiction is a "
                   "CHRONIC, RELAPSING MEDICAL condition, not a moral failing and not a failure of will, "
                   "and NOTHING here is a cure, a treatment, a recommendation, or a licence to acquire or "
                   "use any substance. Registered in run_all_atlas.py as the 15th atlas citizen (ADD-T3a), "
                   "reproducing bit-for-bit with the engine byte-unchanged; reuses the E0 PlasticConnectome "
                   "(imported, not re-derived). efficacy_tested=0; not medical advice; no cure; no licence "
                   "to use; hard problem OPEN.",
        "canonical": "37-addiction-sensitization-dynamics",
        "check": None,
    },
    "alzheimers_threshold_levers": {
        "label": "the cholinergic / glutamatergic-excitotoxicity / inhibitory-network substrate of Alzheimer's mapped onto the threshold-shift frame -- L3-DOMINANT with L1 AND L2 BOTH PRESENT and a SPLIT corrective sign (4 cholinergic-drive + 2 glutamate-excitotoxicity + 3 inhibitory-restore levers), the dominant neurodegenerative-progression axis NAMED but out of reach; the THIRD and DEEPEST PARTIAL [L] fit, the reachable surface purely symptomatic and the out-of-reach axis an E0 DECAY (the inverse of addiction's E0 gain)",
        "value": "the cholinergic-deficit / glutamatergic-excitotoxicity / network-hyperexcitability substrate of Alzheimer's is mapped onto the inherited L1/L2/L3 threshold frame by REACHABILITY and loads MOST on L3 (the up-stream cholinergic drive) while ALSO engaging the ionic levers, with a SPLIT corrective sign: 4 cholinergic-drive levers RESTORED (ACHE/BCHE cholinesterases, CHRNA7 nicotinic, CHRM1 muscarinic -- the donepezil/rivastigmine/galantamine direction, deficient tone UP), 2 glutamate-excitotoxicity levers REDUCED (GRIN2B/GRIN2A NMDA -- the memantine direction, excess drive DOWN), 3 inhibitory-restore levers RESTORED (GABRA1/GABRA5/GABRB3 -- inhibitory tone UP against AD network hyperexcitability) -- the 8th distribution pattern, gross shape shared with addiction's L3-dominant-plus-L1/L2 but distinguished by SPLIT SIGN and a PURELY SYMPTOMATIC reachable surface; the DOMINANT axis PROG (neurodegenerative progression: APP/PSEN1/PSEN2 amyloid/gamma-secretase, MAPT tau, APOE clearance, TREM2 microglial) is NAMED with 6 real genes (gamma carried alongside) but explicitly NOT reachable by a threshold/drive lever, because PROG is a gain/loss not a fold (the ADHD lesson) AND a progression over time -- a plasticity-layer variable (the addiction lesson) -- AND moreover a DEGENERATION, a cumulative irreversible LOSS, an E0 DECAY that is the structural INVERSE of addiction's E0 gain; the fit is PARTIAL [L], the THIRD and DEEPEST non-clean fit; targets ranked, never drugs or doses; cholinesterase inhibitors and memantine are SYMPTOMATIC ONLY and do not slow progression; no cure/reversal/prevention licence and no dignity violation -- a person living with dementia remains a person",
        "grade": "[L partial · O links]",
        "meaning": "Alzheimer's is modelled on the cholinergic-deficit (Davies 1976), glutamatergic-"
                   "excitotoxicity (the memantine rationale) and network-hyperexcitability (Palop 2007) "
                   "substrate, mapped onto the SAME threshold-shift intervention frame the bipolar, "
                   "epilepsy, depression, schizophrenia, autism, ADHD and addiction levers chapters used "
                   "(inherited from the analgesic reproducibility package, Zenodo 10.5281/zenodo.20733420) "
                   "on the SAME R19 engine, READ-ONLY, with NO new mechanism and NO new tuned constant -- "
                   "and it produces the THIRD and DEEPEST PARTIAL [L] fit in the series. Mapped by "
                   "REACHABILITY, Alzheimer's is L3-DOMINANT but NOT L3-only and carries a SPLIT corrective "
                   "sign: of 9 lever genes, 4 sit on L3 (the up-stream cholinergic drive, RESTORED toward "
                   "deficient tone -- ACHE/BCHE cholinesterases the donepezil/rivastigmine/galantamine "
                   "target, CHRNA7 alpha-7 nicotinic, CHRM1 M1 muscarinic), 2 on L1 (glutamatergic "
                   "excitotoxicity, REDUCED -- GRIN2B/GRIN2A NMDA, the memantine direction) and 3 on L2 "
                   "(inhibitory restore, RESTORED against AD network hyperexcitability -- GABRA1/GABRA5/"
                   "GABRB3) -- the 8th distribution pattern across the series and gross-shape kin to "
                   "addiction's L3-dominant-plus-L1/L2, but the FIRST reachable surface that is BOTH purely "
                   "SYMPTOMATIC and SPLIT-SIGN (drive up, excitotoxicity down, inhibition up). The fit is "
                   "PARTIAL [L] because the DOMINANT Alzheimer's fault is OUT OF REACH: the PROG "
                   "(neurodegenerative-progression) axis -- the cumulative degeneration that drives the "
                   "disease -- is NAMED with six real genes (APP the amyloid source and an autosomal-"
                   "dominant early-onset gene, PSEN1/PSEN2 the gamma-secretase subunits, MAPT tau, APOE the "
                   "strongest common risk allele, TREM2 microglial), each carried with its OWN promoter "
                   "gamma read ALONGSIDE but graded [F] NOT REACHED. This DEEPENS both prior partial fits: "
                   "ADHD's gain was out of reach because a fold lever does not set a gain (§35); addiction's "
                   "gain was out of reach for that reason AND because it is consolidated/LEARNED, a "
                   "plasticity variable (§36); Alzheimer's progression is out of reach for BOTH reasons AND "
                   "because it is a DEGENERATION -- a cumulative, irreversible LOSS, an E0 DECAY that is the "
                   "structural INVERSE of addiction's E0 GAIN, so even a drive lever that RESTORES "
                   "instantaneous cholinergic tone cannot HALT the cumulative loss. That is why the "
                   "reachable surface is purely SYMPTOMATIC and the fit is the DEEPEST in the series. Each "
                   "gene's gamma = -mean(nearest-neighbour stacking dG, SantaLucia 1998) is read from its "
                   "OWN promoter window (TSS-2000..+500, Homo sapiens) and turned into that promoter's "
                   "switch stiffness |h_sp| = spinodal(gamma) and barrier = gamma^2/4 using the frozen "
                   "engine READ-ONLY -- the identical pipeline the analgesic, bipolar, epilepsy, depression, "
                   "schizophrenia, autism, ADHD and addiction packages ran, and five reads (GRIN2A, GRIN2B, "
                   "GABRA5, GABRB3 from autism; GABRA1 from epilepsy) are carried over VERBATIM (gamma is "
                   "strand-symmetric, bit-identical), with ACHE, BCHE, CHRNA7, CHRM1, APP, PSEN1, PSEN2, "
                   "MAPT, APOE, TREM2 live GRCh38 strand-aware reads. Two fail-closed disciplines ride "
                   "along: an L3-honesty gate keeps all four cholinergic-drive links graded [O] cited "
                   "biology (never derived) AND asserts L3 UNIQUE dominance, L1 AND L2 BOTH PRESENT, the "
                   "SYMPTOMATIC split-sign domain restriction, the PROG-axis named-out-of-reach, and the "
                   "PARTIAL [L] grade; a forbidden-claim scanner rejects any dose/efficacy/safety/synthesis "
                   "statement PLUS two Alzheimer's-topic classes: a CURE_REVERSAL class (reverse/cure/"
                   "prevent AD, stop/halt the progression, restore lost memory, regrow neurons, miracle "
                   "cure) and a DIGNITY class (empty shell/no longer a person/vegetable/already gone/not "
                   "worth treating), both NEGATION-GUARDED with planted self-tests that must fire; and a "
                   "burden-weighted prioritisation ranks all 15 TARGETS with the gamma read carried "
                   "alongside but NEVER folded into the score. The Alzheimer's unmet-need signature is the "
                   "DEEPEST partial fit: the reachable surface is purely symptomatic, the cholinergic levers "
                   "carry only MODERATE unmet need where an established but SYMPTOMATIC/temporary route "
                   "exists (U-floor=3, ABOVE ADHD's clean-route floor of 2), while the out-of-reach PROG "
                   "progression genes carry the unmet-need CEILING -- disease-MODIFICATION, the single "
                   "greatest unmet need, only modestly touched even by the anti-amyloid antibodies "
                   "lecanemab/donanemab -- but are flagged not-actionable, so the highest-need targets APP "
                   "(#1) and APOE (#2) are NON-actionable and the leading ACTIONABLE target ACHE sits at #3 "
                   "(lowered by its established symptomatic-route unmet). DECOUPLING (the firewall made "
                   "visible): the stiffest promoter CHRM1 sits at priority #6 not the top, while the "
                   "top-priority APP has only the seventh-stiffest read. FIREWALL (non-negotiable): the "
                   "promoter |h_sp| is the gene's own switch stiffness, NEVER equated with a "
                   "neurodegeneration rate, an amyloid burden, a tau load, a receptor occupancy, a drug's "
                   "potency, a dose, or any clinical effect; cholinesterase inhibitors and memantine are "
                   "SYMPTOMATIC ONLY and do NOT slow progression; the anti-amyloid antibodies (lecanemab/"
                   "donanemab) target the out-of-reach PROG axis and are progression-modifiers, not "
                   "threshold levers. Registered in run_all_atlas.py as the 16th atlas citizen (AD-T3b-L), "
                   "reproducing bit-for-bit with engine byte-unchanged. efficacy_tested=0; ranks targets "
                   "not drugs; not medical advice; no claim that Alzheimer's is cured, reversed, halted or "
                   "prevented; a person living with dementia remains a person; hard problem OPEN.",
        "canonical": "38-alzheimers-threshold-levers",
        "check": None,
    },
    "ocd_threshold_levers": {
        "label": "the cortico-striato-thalamo-cortical (CSTC) loop substrate of OCD mapped onto the threshold-shift frame -- L3-DOMINANT with L1 STRONG and L2 SPARSE and a MIXED corrective sign (4 serotonergic/dopaminergic-drive + 3 glutamatergic-excitatory + 1 sparse inhibitory-restore lever), the dominant pathological loop-LOCK axis NAMED but out of reach; the FOURTH PARTIAL [L] fit and a NEW MODE, the out-of-reach axis a pathological STABILISATION (an E0 STABILISATION, the third distinct E0 mode after addiction's GAIN and Alzheimer's DECAY, completing the trio)",
        "value": "the serotonergic / glutamatergic / circuit substrate of OCD is mapped onto the inherited L1/L2/L3 threshold frame by REACHABILITY and loads MOST on L3 (the up-stream serotonergic/dopaminergic drive) while ALSO strongly engaging the glutamate lever and sparsely the inhibitory lever, with a MIXED corrective sign: 4 serotonergic/dopaminergic-drive levers (SLC6A4/HTR2A/HTR1B RESTORE the serotonergic tone -- the SSRI/clomipramine first-line, tone UP; DRD2 REDUCE the dopaminergic drive -- antipsychotic augmentation, drive DOWN), 3 glutamatergic-excitatory levers REDUCED (SLC1A1/EAAT3 the most replicated OCD gene, GRIN2B, GRIK2 -- the glutamate-modulator direction, hyperactive loop drive DOWN), 1 SPARSE inhibitory-restore lever (GABRA1 -- a single weak node, inhibitory tone UP; OCD's GABAergic arm is thin, itself a finding) -- the 9th distribution pattern, gross shape kin to addiction's/Alzheimer's L3-dominant-plus-L1/L2 but distinguished by a SPARSE L2 and by an out-of-reach axis that is a pathological STABILISATION; unlike Alzheimer's purely-symptomatic surface, the OCD levers are the actual mainstay/investigational routes and genuinely (PARTIALLY) help. The DOMINANT axis LOCK (pathological stabilisation / stuck-attractor lock-in: the corticostriatal circuit-fixation machinery DLGAP3/SAPAP3 the canonical OCD-model scaffold, SLITRK5, PTPRD, BTBD3) is NAMED with 4 real genes (gamma carried alongside) but explicitly NOT reachable by a threshold/drive lever, because LOCK is a gain/loss not a fold (the ADHD lesson) AND a consolidated/learned plasticity (E0-layer) variable (the addiction lesson) AND moreover a pathological STABILISATION -- an over-deep basin / hysteresis (an E2 phenomenon), an E0 STABILISATION that is the THIRD distinct E0 mode, distinct from addiction's E0 GAIN and Alzheimer's E0 DECAY (completing the trio addiction GAIN -> Alzheimer's DECAY -> OCD STABILISATION); the fit is PARTIAL [L], the FOURTH non-clean fit; targets ranked, never drugs or doses; the reachable levers nudge the operating point but do NOT unstick the loop (deep-brain stimulation of the CSTC loop and exposure-response-prevention are the dynamics handles the levers are not); no cure/miracle licence and no moral-framing/stigma violation -- OCD is a treatable medical condition and intrusive thoughts are a symptom, not a moral failing",
        "grade": "[L partial · O links]",
        "meaning": "OCD is modelled on the cortico-striato-thalamo-cortical (CSTC) loop substrate -- the "
                   "worry-compulsion loop that settles into a self-sustaining, over-consolidated, "
                   "pathologically STABILISED attractor, reinforced by the transient anxiety-relief each "
                   "compulsion delivers -- mapped onto the SAME threshold-shift intervention frame the "
                   "bipolar, epilepsy, depression, schizophrenia, autism, ADHD, addiction and Alzheimer's "
                   "levers chapters used (inherited from the analgesic reproducibility package, Zenodo "
                   "10.5281/zenodo.20733420) on the SAME R19 engine, READ-ONLY, with NO new mechanism and "
                   "NO new tuned constant -- and it produces the FOURTH PARTIAL [L] fit in the series, and "
                   "a NEW MODE. Mapped by REACHABILITY, OCD is L3-DOMINANT but NOT L3-only and carries a "
                   "MIXED corrective sign: of 8 lever genes, 4 sit on L3 (the up-stream "
                   "serotonergic/dopaminergic drive -- SLC6A4/HTR2A/HTR1B RESTORED toward deficient "
                   "serotonergic tone, the SSRI/clomipramine first-line; DRD2 REDUCED, the antipsychotic-"
                   "augmentation direction), 3 on L1 (glutamatergic excitatory, REDUCED -- SLC1A1/EAAT3 the "
                   "MOST replicated OCD candidate gene, GRIN2B, GRIK2, the glutamate-modulator direction) "
                   "and 1 on L2 (inhibitory restore, RESTORED -- GABRA1, a single SPARSE weak node) -- the "
                   "9th distribution pattern across the series, with two distinctive features: the L2 arm is "
                   "SPARSE (a single weak node, where addiction had two and Alzheimer's three -- OCD's "
                   "GABAergic arm is thin), and the reachable surface, unlike Alzheimer's purely-"
                   "symptomatic one, is where the actual mainstay/investigational treatments act and "
                   "genuinely (PARTIALLY) help. The fit is PARTIAL [L] because the DOMINANT OCD fault is OUT "
                   "OF REACH: the LOCK (pathological-stabilisation / stuck-attractor) axis -- the over-"
                   "consolidated, self-sustaining compulsive loop -- is NAMED with four real circuit-"
                   "fixation genes (DLGAP3/SAPAP3 the corticostriatal scaffold whose knockout produces "
                   "compulsive overgrooming, the canonical OCD model; SLITRK5 a synaptic-adhesion molecule "
                   "with the same knockout phenotype; PTPRD a presynaptic adhesion phosphatase from OCD "
                   "GWAS; BTBD3 a circuit-patterning gene from OCD GWAS), each carried with its OWN promoter "
                   "gamma read ALONGSIDE but graded [F] NOT REACHED. This COMPLETES the E0 trio: ADHD's gain "
                   "was out of reach because a fold lever does not set a gain (the 35); addiction's gain was "
                   "out of reach for that reason AND because it is consolidated/LEARNED, an E0 GAIN (the "
                   "36); Alzheimer's progression was out of reach for both reasons AND because it is a "
                   "DEGENERATION, an E0 DECAY (the 38); OCD's lock is out of reach for the ADHD and "
                   "addiction reasons AND because it is a pathological STABILISATION -- an over-deep basin / "
                   "hysteresis (an E2 phenomenon), an E0 STABILISATION that is the THIRD distinct E0 mode, "
                   "neither addiction's GAIN nor Alzheimer's DECAY (addiction BUILDS a trace, Alzheimer's "
                   "LOSES a substrate, OCD FREEZES an attractor). So even a drive lever that nudges the "
                   "instantaneous serotonergic/dopaminergic/glutamatergic tone cannot UNSTICK the loop, "
                   "which is exactly why OCD's response to the mainstay treatments is partial and slow, and "
                   "why a DYNAMICS intervention (deep-brain stimulation of the CSTC loop, the exposure-"
                   "response-prevention that re-plasticises the loop through extinction) reaches refractory "
                   "cases the levers cannot -- OCD is the convergence point with the E2/E0 dynamics layer (a "
                   "future B-ii). Each gene's gamma = -mean(nearest-neighbour stacking dG, SantaLucia 1998) "
                   "is read from its OWN promoter window (TSS-2000..+500, Homo sapiens) and turned into that "
                   "promoter's switch stiffness |h_sp| = spinodal(gamma) and barrier = gamma^2/4 using the "
                   "frozen engine READ-ONLY -- the identical pipeline the analgesic, bipolar, epilepsy, "
                   "depression, schizophrenia, autism, ADHD, addiction and Alzheimer's packages ran, and "
                   "five reads (SLC6A4, HTR2A from depression; DRD2 from addiction; GRIN2B from autism; "
                   "GABRA1 from epilepsy) are carried over VERBATIM (gamma is strand-symmetric, bit-"
                   "identical), with HTR1B, SLC1A1, GRIK2, DLGAP3, SLITRK5, PTPRD, BTBD3 live GRCh38 strand-"
                   "aware reads. Two fail-closed disciplines ride along: an L3-honesty gate keeps all four "
                   "serotonergic/dopaminergic-drive links graded [O] cited biology (never derived) AND "
                   "asserts L3 UNIQUE dominance, L1 PRESENT, L2 SPARSE, the INSTANT-axis domain restriction "
                   "with a MIXED sign, the LOCK-axis named-out-of-reach, and the PARTIAL [L] grade; a "
                   "forbidden-claim scanner rejects any dose/efficacy/safety/synthesis statement PLUS two "
                   "OCD-topic classes: a CURE_MIRACLE class (cure/permanently-stop-the-intrusive-thoughts/"
                   "eliminate-the-compulsions/miracle-cure/one-weird-trick) and a MORAL_FRAMING/STIGMA class "
                   "(just-stop-worrying/lack-of-willpower/character-flaw/moral-failing/attention-seeking/"
                   "not-a-real-illness), both NEGATION-GUARDED with planted self-tests that must fire; and a "
                   "burden-weighted prioritisation ranks all 12 TARGETS with the gamma read carried "
                   "alongside but NEVER folded into the score. The OCD unmet-need signature: the deepest-"
                   "unmet tier (U=5) is held ENTIRELY by the out-of-reach loop-lock genes (DLGAP3/SLITRK5/"
                   "PTPRD/BTBD3 -- the refractory loop-lock has NO molecular therapy, DBS only), while the "
                   "leading ACTIONABLE target SLC1A1 (the most replicated OCD gene, the glutamate-modulator "
                   "direction) is reachable and the single highest-leverage handle yet only PARTIALLY helps; "
                   "U-floor=3 (the established but partial serotonergic route, ABOVE ADHD's clean-route "
                   "floor of 2). DECOUPLING (the firewall made visible): the stiffest promoter DLGAP3 (an "
                   "out-of-reach loop-lock gene) sits at priority #3 not the top, the softest GABRA1 is a "
                   "reachable lever, and the four out-of-reach genes span the WHOLE stiffness range -- so "
                   "stiffness predicts neither axis nor reach nor priority. FIREWALL (non-negotiable): the "
                   "promoter |h_sp| is the gene's own switch stiffness, NEVER equated with a basin depth, a "
                   "hysteresis width, the strength of the compulsive lock, a receptor occupancy, a synaptic "
                   "serotonin/dopamine/glutamate level, a drug's potency, a dose, an in-vivo selectivity, or "
                   "any clinical effect. Registered in run_all_atlas.py as the 18th atlas citizen "
                   "(OCD-T3c-L), reproducing bit-for-bit with engine byte-unchanged. efficacy_tested=0; "
                   "ranks targets not drugs; not medical advice; the reachable levers nudge the operating "
                   "point but do not unstick the loop; no claim that OCD is cured or that intrusive thoughts "
                   "are permanently stopped; OCD is a treatable medical condition and intrusive thoughts are "
                   "a symptom, not a moral failing; hard problem OPEN.",
        "canonical": "40-ocd-threshold-levers",
        "check": None,
    },
    "alzheimers_progression_dynamics": {
        "label": "the dominant neurodegenerative-progression axis of Alzheimer's (the cumulative, irreversible LOSS) modelled DIRECTLY on the E0 plasticity layer as the structural INVERSE of addiction's gain -- the OTHER HALF of the §38 convergence: §38 (B-i) NAMED the decay out of reach for the instant symptomatic levers, this module (B-ii) MODELS it and shows the only handle lives on the progression axis; the loss SIGN is the structural inverse of E0 GAIN (the engine has NO degeneration signal -- the honest disanalogy with §37); five sign-only results, all CONFIRMED over a decay-rate sweep",
        "value": "the dominant Alzheimer's fault §38 (AD-T3b-L, B-i) named OUT OF REACH for the instant symptomatic L1/L2/L3 levers -- the PROG neurodegenerative-progression axis (the cumulative, irreversible loss of synapses and neurons that makes the disease the disease) -- is modelled DIRECTLY here by REUSING the §26 E0 PlasticConnectome (the kernel W0, the coupling map, the order-parameter machinery -- imported, not re-derived) and applying to that frozen kernel the structural INVERSE of E0's Hebbian consolidation: a slow progressive CONNECTIVITY ATTRITION (synapse/neuron loss, mass DOWN where §37 drove mass UP). Unlike §37 -- whose reward SIGN came from an engine signal (M5 dopamine reward-prediction error) -- the engine has NO degeneration signal (no amyloid/tau/synapse-loss variable; it is a healthy emergent atlas), so this module does NOT claim to ground the loss sign in an engine pathology signal: it grounds the BASELINE being lost (the frozen M9 anchor W0, the engine's own emergent coordination) and the GUARD read-only, and the loss DIRECTION is grounded as the structural INVERSE of E0 GAIN (neurodegeneration is, by definition, progressive loss of connectivity). Five pre-registered SIGN-only results, all CONFIRMED over a decay-rate sweep, each the inverse of a §37 result: D1 progressive degeneration (progression monotonically accumulates connectivity loss, deeper -> less surviving mass and lower coordination R -- the inverse of incentive sensitisation), D2 loss of responsiveness (a degenerated connectome responds LESS to the same coordinating cue than a healthy one, R_degen(cue) < R_healthy(cue), resting R <= the healthy anchor -- progressive functional decline, the inverse of cue-reactivity), D3 levers-do-not-rebuild (the symptomatic cue -- the B-i reachable instant axis -- leaves the cumulative structural loss EXACTLY unchanged, a read-time coupling adds no mass, and at deep loss even the MAXIMUM cue cannot return the circuit to the healthy resting anchor -- relief WITHOUT disease modification, the convergence seam, the inverse of extinction-persistence; exactly why cholinesterase inhibitors and memantine are symptomatic only and do not slow progression), D4 the structural-variable guard (with decay rate = 0 the connectome stays identical to the kernel, the order parameter returns to the frozen M9 anchor bit-for-bit, and the loss is exactly zero -- degeneration is a structural-loss variable the instant levers cannot reach, pure add-on; mirror of the addiction plasticity-variable guard), D5 the dynamics handle (a LOWER decay rate preserves STRICTLY MORE structure at equal progression time while the symptomatic cue has NO handle on the structural trajectory -- the handle lives ONLY on the progression axis, the disease-modification direction where the anti-amyloid antibodies act; the inverse of the spacing handle). The two halves of the AD convergence meet in one disorder, the exact INVERSE of the addiction convergence: addiction CONSOLIDATES a trace the levers cannot erase (E0 GAIN), Alzheimer's LOSES a substrate the levers cannot rebuild (E0 DECAY) -- the same E0 layer from opposite directions. Reuses the E0 layer, no new tuned constant, engine byte-unchanged; the connectivity loss is the progression as a STRUCTURAL quantity, never the felt quality of memory/loss/selfhood in dementia (Axis-A; consciousness_claim=0; hard problem OPEN); a person living with dementia REMAINS a person; efficacy=0; not medical advice; no cure, reversal, prevention, or halt of progression",
        "grade": "[V mech]",
        "meaning": "Alzheimer's dominant defect -- the PROG NEURODEGENERATIVE-PROGRESSION axis (the "
                   "cumulative, irreversible loss of synapses and neurons that makes the disease the "
                   "disease) -- was NAMED out of reach for the instant symptomatic threshold levers in "
                   "§38 (AD-T3b-L, B-i), for the DEEPEST reason in the series: it is a GAIN/LOSS not a "
                   "fold (the ADHD lesson -- an instant lever has no handle on amplitude), AND a "
                   "PROGRESSION over time (a plasticity/E0-layer variable, not an instant operating "
                   "point -- the addiction lesson), AND moreover a DEGENERATION -- a cumulative "
                   "IRREVERSIBLE LOSS = E0 DECAY, the structural INVERSE of addiction's E0 GAIN. That "
                   "naming was the honest HALF of a convergence; this module is the OTHER half -- it "
                   "MODELS the decay directly via the §26 E0 plasticity dynamics, supplying the "
                   "variable that actually MOVES the trajectory (the decay rate, the disease-"
                   "modification axis) and showing the symptomatic levers have no handle on it. It "
                   "REUSES the E0 PlasticConnectome (it does NOT re-derive the kernel, the coupling-vs-"
                   "bias map, or the order-parameter machinery -- handover reuse discipline) and "
                   "applies to that frozen kernel the structural INVERSE of E0's Hebbian consolidation: "
                   "a slow progressive CONNECTIVITY ATTRITION (synapse/neuron loss, the defining "
                   "structural feature of neurodegeneration, mass DOWN where §37 drove mass UP). The "
                   "GROUNDING is honestly disanalogous to §37: the addiction reward SIGN was read out "
                   "of an ENGINE signal (M5 RPE potentiation), but the engine has NO degeneration "
                   "signal -- it is a healthy emergent atlas with no amyloid/tau/synapse-loss variable "
                   "(the very reason E0 had to ADD plasticity, and why §38 named this axis out of "
                   "reach) -- so this module does NOT claim to ground the loss sign in an engine "
                   "pathology signal; it grounds the BASELINE being lost (the frozen M9 anchor W0, the "
                   "engine's own emergent coordination) and the GUARD read-only, and the loss DIRECTION "
                   "is grounded DEFINITIONALLY and as the structural INVERSE of E0 GAIN (neuro"
                   "degeneration is, by the meaning of the word, progressive LOSS of connectivity). "
                   "Five pre-registered SIGN-only predictions are all CONFIRMED and all hold over a "
                   "decay-rate sweep (anti-tuning), each the inverse of a §37 result: D1 PROGRESSIVE "
                   "DEGENERATION -- progression monotonically accumulates structural loss (the "
                   "connectivity lost from the kernel rises with epochs, 0->2.23->4.04->5.52->7.23->"
                   "8.50 over 0-24) and coordination falls with it (deeper -> less surviving mass AND "
                   "lower R), the inverse of incentive sensitisation; D2 LOSS OF RESPONSIVENESS -- a "
                   "degenerated connectome responds LESS to the SAME coordinating cue than a healthy "
                   "one (R_degen(cue) < R_healthy(cue), resting R <= the healthy anchor: the lost "
                   "structure sits the circuit in a LOWER-coordination basin, so the same cue evokes a "
                   "SMALLER response -- progressive functional decline, the inverse of cue-reactivity; "
                   "only the response-falls-below-healthy SIGN is asserted, magnitudes [O]); D3 LEVERS-"
                   "DO-NOT-REBUILD -- the symptomatic cue (the B-i reachable instant axis) lifts the "
                   "instant operating point but leaves the cumulative structural loss EXACTLY unchanged "
                   "(a read-time coupling adds no mass), and at deep degeneration even the MAXIMUM cue "
                   "cannot return the circuit to the healthy resting anchor (a ceiling set by surviving "
                   "structure: max-cue R ~0.342 < anchor 0.38961) -- relief WITHOUT disease "
                   "modification, the convergence seam exhibited dynamically and exactly why "
                   "cholinesterase inhibitors and memantine are symptomatic only; the inverse of "
                   "extinction-persistence (there the drive came off but the trace stayed, here the "
                   "lever lifts the symptom but the loss stays); D4 the STRUCTURAL-VARIABLE GUARD -- "
                   "with the decay rate = 0 the connectome stays identical to the kernel, the order "
                   "parameter returns to the frozen M9 anchor BIT-FOR-BIT, and the loss is EXACTLY "
                   "zero, so the degeneration DISAPPEARS without the decay process, proving the PROG "
                   "axis is a cumulative STRUCTURAL-LOSS variable which is precisely why the instant "
                   "levers cannot reach it (pure add-on; mirror of the addiction plasticity-variable "
                   "guard); and D5 the DYNAMICS HANDLE -- a LOWER decay rate preserves STRICTLY MORE "
                   "structure (less cumulative loss, more surviving mass) at equal progression time, "
                   "while the symptomatic cue has NO handle on the structural trajectory at all (it "
                   "leaves the loss invariant, D3) -- the handle lives ONLY on the PROGRESSION axis, "
                   "the disease-modification direction (the structural separation between the "
                   "SYMPTOMATIC agents, which drive the operating point and have no handle on the loss, "
                   "and the PROGRESSION-MODIFIERS -- the anti-amyloid antibodies lecanemab/donanemab -- "
                   "which act on the progression axis and only modestly slow decline); the inverse of "
                   "the spacing handle. The two halves of the AD convergence thus MEET in one disorder, "
                   "the exact INVERSE of the addiction convergence: the threshold frame (B-i) names the "
                   "decay unreachable for instant levers, the plasticity-dynamics frame (B-ii) EXHIBITS "
                   "the decay (D1-D2), shows the levers do NOT rebuild it (D3), proves it is a "
                   "structural variable they cannot reach (D4), and shows the only handle is on the "
                   "progression axis (D5). ADDICTION CONSOLIDATES a trace the levers cannot erase (E0 "
                   "GAIN); ALZHEIMER'S LOSES a substrate the levers cannot rebuild (E0 DECAY) -- the "
                   "same E0 plasticity layer met from opposite directions. FIREWALL: the connectivity "
                   "loss is the neurodegenerative progression as a STRUCTURAL quantity, NEVER a claim "
                   "about the FELT quality of memory, loss, recognition or selfhood in dementia "
                   "(Axis-A; consciousness_claim=0; hard problem OPEN); A PERSON LIVING WITH DEMENTIA "
                   "REMAINS A PERSON -- the cumulative loss is a substrate-degeneration boundary, NOT a "
                   "subtraction of the person, and nothing licenses treating anyone as an empty shell "
                   "or a lost cause; real neurodegeneration is HETEROGENEOUS (amyloid-beta aggregation, "
                   "tau/neurofibrillary pathology, synaptic and neuronal loss, neuroinflammation/"
                   "microglial dysfunction, network failure, cerebrovascular contribution -- LOCKED), "
                   "only the SIGN of a cumulative structural loss is asserted; the loss SIGN is the "
                   "structural inverse of E0 GAIN (the engine has no degeneration signal) and every "
                   "MAGNITUDE (including the rate and the identity of the real degeneration mechanism) "
                   "is [O]; and NOTHING here is a cure, a reversal, a prevention, a halt or a slowing "
                   "of the progression, a treatment, or a recommendation. Registered in run_all_atlas.py "
                   "as the 17th atlas citizen (AD-T3b-D), reproducing bit-for-bit with the engine byte-"
                   "unchanged; reuses the E0 PlasticConnectome (imported, not re-derived). "
                   "efficacy_tested=0; not medical advice; no cure / reversal / prevention; hard "
                   "problem OPEN.",
        "canonical": "39-alzheimers-progression-dynamics",
        "check": None,
    },
    "ocd_stabilisation_dynamics": {
        "label": "the dominant compulsion-maintaining axis of OCD (the self-sustaining STUCK LOOP) modelled DIRECTLY on the E0 plasticity layer as the THIRD E0 MODE -- STABILISATION, after addiction's GAIN and Alzheimer's DECAY -- the OTHER HALF of the §40 convergence: §40 (B-i) NAMED the loop-lock out of reach for the instant symptomatic levers, this module (B-ii) MODELS it and shows the only handle lives on the consolidation (learning/plasticity) axis; the stabilisation SIGN is grounded as the SAME E0 consolidation family as §37's GAIN, distinguished by the self-sustaining-at-rest readout (the engine has NO stuck-loop signal -- the honest disanalogy with §37); five sign-only results, all CONFIRMED over eta and bias sweeps",
        "value": "the dominant OCD fault §40 (OCD-T3c-L, B-i) named OUT OF REACH for the instant symptomatic L1/L2/L3 levers -- the STABILISATION lock (the self-sustaining stuck loop / over-deep basin that makes a compulsion a compulsion) -- is modelled DIRECTLY here by REUSING the §26 E0 PlasticConnectome (the kernel W0, the coupling map, the order-parameter machinery -- imported, not re-derived) and driving that frozen kernel, through E0's potentiating Hebbian update at a negatively-reinforced coordinated operating point, into a self-sustaining locked loop -- the THIRD E0 mode (after addiction's GAIN and Alzheimer's DECAY, completing the trio). Like §39 and UNLIKE §37 -- whose reward SIGN came from an engine signal (M5 dopamine reward-prediction error) -- the engine has NO stuck-loop / compulsion signal (no over-stable basin or self-sustaining-loop variable; it is a healthy emergent atlas), so this module does NOT claim to ground the stabilisation sign in an engine pathology signal: it grounds the BASELINE the loop locks around (the frozen M9 anchor W0), the BASIN-DEPTH concept (the READ-ONLY R19 barrier B(g)=g^2/4=0.25, the cusp normal-form basin depth an over-stabilised loop deepens) and the GUARD read-only, and the stabilisation DIRECTION is grounded as the SAME E0 consolidation family as §37's GAIN (the same potentiating update writes a trace > 0), DISTINGUISHED from §37 by its READOUT -- the locked loop holds its own coordination above the anchor at rest with NO external cue. CRUCIAL HONESTY: the NETWORK exhibits NO clean bistability/hysteresis of its own under these couplings, so NO network-hysteresis is claimed (the proper over-deep-basin lock is an E2/R19-cusp phenomenon, grounded in the READ-ONLY R19 barrier); what the E0 layer ACTUALLY exhibits is the CONSOLIDATION of the connectome into a self-sustaining locked loop. Five pre-registered SIGN-only results, all CONFIRMED over eta and bias sweeps: S1 progressive stabilisation (consolidation monotonically writes structure, trace up over BOTH an eta and a bias sweep, and the locked state deepens, Rlock deeper >= shallower -- a basin-depth variable the instant levers cannot reach), S2 self-sustaining loop (a consolidated connectome started from a COORDINATED/locked IC holds its coordination at/above the frozen M9 anchor at rest, and at/above the cold-start/fresh branch, with NO external cue, for epochs >= 4 over an eta sweep; the excess Rlock-M9 grows -- the defining readout distinguishing STABILISATION from addiction's cue-reactivity and Alzheimer's decline), S3 levers-do-not-unstick (the symptomatic lever -- the B-i reachable instant axis -- leaves the retained structural trace EXACTLY unchanged, a read-time coupling writes no structure, and even the MAXIMUM lever cannot reduce the consolidated trace -- relief WITHOUT re-writing the loop, the convergence seam, the analogue of extinction-persistence; exactly why SSRIs and augmentation are symptomatic management and do not by themselves erase the loop), S4 the structural-variable guard (with consolidation off the connectome stays identical to the kernel, the order parameter read with the FAITHFUL integrator from the engine's own fixed incoherent-seed IC returns to the frozen M9 anchor bit-for-bit, and the trace is exactly zero -- stabilisation is a structural variable the instant levers cannot reach, pure add-on; mirror of the addiction/Alzheimer's plasticity-variable guard), S5 the dynamics handle (a LOWER consolidation rate writes STRICTLY LESS structure at equal consolidation time while the symptomatic lever has NO handle on the structural trajectory -- the handle lives ONLY on the consolidation / learning-plasticity axis where exposure-and-response-prevention re-writing acts; the analogue of the spacing / progression-rate handle). The two halves of the OCD convergence meet in one disorder, completing the E0 trio: addiction CONSOLIDATES a sensitised reward trace (E0 GAIN, mass up), Alzheimer's LOSES a substrate (E0 DECAY, mass down), OCD FREEZES a self-sustaining loop (E0 STABILISATION, a trace that holds itself at rest) -- the same E0 layer met three ways. Reuses the E0 layer, no new tuned constant, engine byte-unchanged; the retained trace is the loop as a STRUCTURAL quantity, never the felt quality of an intrusive thought, an urge or the distress of a compulsion (Axis-A; consciousness_claim=0; hard problem OPEN); OCD is a TREATABLE condition and an intrusive thought is a symptom, not a wish or a moral failing; efficacy=0; not medical advice; no cure, reversal, or prevention",
        "grade": "[V mech]",
        "meaning": "OCD's dominant defect -- the STABILISATION lock (the self-sustaining stuck "
                   "loop / over-deep basin that makes a compulsion a compulsion) -- was NAMED out of "
                   "reach for the instant symptomatic threshold levers in §40 (OCD-T3c-L, B-i), for "
                   "two reasons: it is a LOOP-STABILITY / BASIN-DEPTH property, not an instant "
                   "operating point (a plasticity/E0-layer variable -- the addiction lesson), AND it "
                   "is SELF-SUSTAINING (the loop holds ITSELF, so an instant lever that lowers the "
                   "drive does not erase the structure that keeps it going). §40 called it 'an E2 "
                   "phenomenon'. That naming was the honest HALF of a convergence; this module is the "
                   "OTHER half -- it MODELS the loop directly via the §26 E0 plasticity dynamics, "
                   "supplying the variable that actually MAINTAINS it (the rate of the consolidation "
                   "process, the learning/plasticity axis) and showing the symptomatic levers have no "
                   "handle on it. It REUSES the E0 PlasticConnectome (it does NOT re-derive the "
                   "kernel, the coupling-vs-bias map, or the order-parameter machinery -- handover "
                   "reuse discipline) and drives that frozen kernel through E0's potentiating Hebbian "
                   "update, at a negatively-reinforced coordinated operating point, into a self-"
                   "sustaining locked loop -- the THIRD E0 mode. Where §37 drove a reward bias to GROW "
                   "a sensitised trace that responds MORE to a reward CUE, and §39 drove attrition to "
                   "LOSE a substrate, this module drives consolidation to LOCK a loop that SELF-"
                   "SUSTAINS AT REST. STABILISATION shares §37's E0 consolidation FAMILY (the same "
                   "potentiating update writes a trace > 0); it is DISTINGUISHED from §37 not by a "
                   "different sign of the trace but by its READOUT -- the locked loop holds its own "
                   "coordination above the M9 anchor at rest with NO external cue, the mechanistic "
                   "signature of a stuck compulsion that runs itself. The GROUNDING is honestly "
                   "disanalogous to §37 (and like §39): the addiction reward SIGN was read out of an "
                   "ENGINE signal (M5 RPE), but the engine has NO stuck-loop signal -- it is a healthy "
                   "emergent atlas with no over-stable-basin or self-sustaining-loop variable (the "
                   "very reason E0 had to ADD plasticity, and why §40 named this axis out of reach) -- "
                   "so this module does NOT claim to ground the stabilisation sign in an engine "
                   "pathology signal; it grounds the BASELINE the loop locks around (the frozen M9 "
                   "anchor W0), the BASIN-DEPTH concept (the READ-ONLY R19 barrier B(g)=g^2/4=0.25, "
                   "the cusp-catastrophe normal-form basin depth) and the GUARD read-only, and the "
                   "stabilisation DIRECTION is grounded as the SAME E0 consolidation family as §37's "
                   "GAIN, distinguished by the self-sustaining-at-rest readout. CRUCIAL HONESTY: the "
                   "NETWORK exhibits NO clean bistability or hysteresis of its own under these "
                   "couplings (the order parameter never collapses to an incoherent branch), so NO "
                   "network-hysteresis is claimed -- the proper over-deep-basin / over-wide-hysteresis "
                   "lock named by §40 is an E2/R19-cusp phenomenon, grounded here in the READ-ONLY R19 "
                   "barrier, NOT a network read. Five pre-registered SIGN-only predictions are all "
                   "CONFIRMED and all hold over eta and bias sweeps (anti-tuning): S1 PROGRESSIVE "
                   "STABILISATION -- consolidation monotonically writes structure into the connectome "
                   "(the retained trace ||W-W0|| rises with epochs, 0->0.18->0.35->0.50 over 0-18) "
                   "over BOTH an eta and a bias sweep, and the locked state deepens (Rlock deeper >= "
                   "shallower) -- the loop deepening, a basin-depth variable the instant levers cannot "
                   "reach; S2 SELF-SUSTAINING LOOP (the defining readout) -- a consolidated connectome "
                   "started from a COORDINATED (locked) initial condition HOLDS its coordination at or "
                   "above the frozen M9 anchor at rest with NO external cue (Rlock >= M9), and at or "
                   "above what the SAME connectome reaches from a FRESH (incoherent) start (Rlock >= "
                   "Rfresh): an IC-hysteresis gap in which the locked branch sits above the cold-start "
                   "branch, the excess Rlock-M9 growing with consolidation (-0.001->0.009->0.014->"
                   "0.015 over 0-18) -- the mechanistic signature of a stuck compulsion that runs "
                   "ITSELF, distinct from addiction's cue-reactivity (a response to an external reward "
                   "cue) and Alzheimer's progressive decline; S3 LEVERS-DO-NOT-UNSTICK -- the "
                   "symptomatic lever (the B-i reachable instant axis) changes the instant operating "
                   "point but leaves the retained structural trace EXACTLY unchanged (a read-time "
                   "coupling writes no structure), and even the MAXIMUM lever cannot reduce the "
                   "consolidated trace -- relief WITHOUT re-writing the loop, the convergence seam, "
                   "exactly why SSRIs and augmentation manage symptoms and do not by themselves erase "
                   "the compulsion loop; the analogue of extinction-persistence (there the drive came "
                   "off but the trace stayed, here the lever moves the symptom but the loop stays); S4 "
                   "the STRUCTURAL-VARIABLE GUARD -- with consolidation off (eta=0 / zero epochs) the "
                   "connectome stays identical to the kernel, the order parameter read with the "
                   "FAITHFUL integrator from the engine's own fixed (incoherent-seed) initial "
                   "condition returns to the frozen M9 anchor BIT-FOR-BIT, the trace is EXACTLY zero, "
                   "and the engine's own _integrate(W0) == M9, so the loop DISAPPEARS without the "
                   "consolidation process, proving the stabilisation axis is a STRUCTURAL (plasticity-"
                   "layer) variable which is precisely why the instant levers cannot reach it (pure "
                   "add-on; mirror of the addiction/Alzheimer's plasticity-variable guard); and S5 "
                   "the DYNAMICS HANDLE -- a LOWER consolidation rate writes STRICTLY LESS structure "
                   "(a shallower loop) at equal consolidation time, while the symptomatic lever has NO "
                   "handle on the structural trajectory at all (it leaves the trace invariant, S3) -- "
                   "the handle lives ONLY on the CONSOLIDATION (learning/plasticity) axis, the "
                   "direction in which exposure-and-response-prevention (ERP) re-writing can weaken "
                   "the loop while a symptomatic agent manages the operating point; the analogue of "
                   "the spacing / progression-rate handle. The two halves of the OCD convergence thus "
                   "MEET in one disorder, completing the E0 trio: the threshold frame (B-i) names the "
                   "loop unreachable for instant levers, the plasticity-dynamics frame (B-ii) EXHIBITS "
                   "the loop (S1-S2), shows the levers do NOT unstick it (S3), proves it is a "
                   "structural variable they cannot reach (S4), and shows the only handle is on the "
                   "consolidation axis (S5). ADDICTION CONSOLIDATES a sensitised reward trace (E0 "
                   "GAIN, mass up); ALZHEIMER'S LOSES a substrate (E0 DECAY, mass down); OCD FREEZES a "
                   "self-sustaining loop (E0 STABILISATION, a trace that holds itself at rest) -- the "
                   "same E0 plasticity layer met three ways. FIREWALL: the retained trace is the loop "
                   "as a STRUCTURAL quantity, NEVER a claim about the FELT quality of an intrusive "
                   "thought, an urge, or the distress of a compulsion (Axis-A; consciousness_claim=0; "
                   "hard problem OPEN); OCD is a TREATABLE condition and an intrusive thought is a "
                   "SYMPTOM, not a wish, a character flaw, or a moral failing, and nothing licenses "
                   "treating anyone as their compulsion or as responsible for the loop; real OCD is "
                   "HETEROGENEOUS (CSTC circuit hyperconnectivity, serotonergic and glutamatergic "
                   "dysregulation, post-synaptic-density / SAPAP3-DLGAP3 pathology, SLITRK5, basal-"
                   "ganglia gating, error-monitoring abnormalities -- LOCKED), only the SIGN of a "
                   "self-sustaining stabilisation is asserted; the stabilisation SIGN is the SAME E0 "
                   "consolidation family as §37's gain (distinguished by the self-sustaining-at-rest "
                   "readout) and every MAGNITUDE (the rate eta, the locked-point bias, the identity of "
                   "the real compulsion mechanism) is [O]; and NOTHING here is a cure, a reversal, a "
                   "prevention, a treatment, or a recommendation. Registered in run_all_atlas.py as "
                   "the 19th atlas citizen (OCD-T3c-D), reproducing bit-for-bit with the engine byte-"
                   "unchanged; reuses the E0 PlasticConnectome (imported, not re-derived). "
                   "efficacy_tested=0; not medical advice; no cure / reversal / prevention; hard "
                   "problem OPEN.",
        "canonical": "41-ocd-stabilisation-dynamics",
        "check": None,
    },
    "e0_triad_synthesis": {
        "label": "the E0 triad synthesis (the v1.49 capstone): a META-SYNTHESIS -- zero new measurement, zero new machinery, zero new tuned constant -- that cross-reads the three now-frozen E0-dynamics modules (addiction GAIN §37, Alzheimer's DECAY §39, OCD STABILISATION §41) and certifies them as THREE READOUTS of the single §26 E0 plasticity layer; the three source results JSONs are the SSOT and their frozen SHA-256 are re-verified BIT-FOR-BIT before they are read, the engine is imported READ-ONLY and byte-unchanged; five certifications (T1 one shared layer, T2 three directions of mass, T3 three readouts, T4 same family / different readout, T5 one seam / one handle), all CONFIRMED",
        "value": "the three preceding chapters each modelled one named disorder DIRECTLY on the §26 E0 PlasticConnectome -- addiction as GAIN (a sensitised reward trace that responds MORE to a cue, §37), Alzheimer's as DECAY (the structural inverse, a substrate LOST, §39), OCD as STABILISATION (a self-sustaining trace that holds its own coordination AT REST with no cue, §41). With the third face frozen, the three-mode arc CLOSES, and this capstone steps back to certify the single structural statement they jointly make: ONE plasticity layer, read THREE ways. It is a META-SYNTHESIS, not a new model: zero new measurement, zero new machinery, zero new tuned constant. Discipline of a synthesis -- the three source results JSONs are the SSOT, and BEFORE reading a single number the verifier re-computes each one's SHA-256 and checks it BIT-FOR-BIT against the frozen value (GAIN 20dfb3e9..., DECAY 7a8e8513..., STABILISATION ef37d619...); only then are they read; the engine is emerged READ-ONLY for the invariant check and confirmed byte-unchanged (0fbf4988...). FIVE CERTIFICATIONS, all CONFIRMED: T1 ONE SHARED LAYER -- all three are applications of the SAME imported PlasticConnectome, and with the plasticity process off (addiction eta=0, Alzheimer's decay-rate=0, OCD consolidation=0) all three connectomes revert to the SAME frozen M9 anchor (R~0.38961) BIT-FOR-BIT (each module's own guard asserts it at full precision) -- one layer, one off-state: the structure the gain consolidates onto, the substrate the decay strips, the baseline the loop locks around are the same anchor. T2 THREE DIRECTIONS OF MASS -- the same update moves structure UP under reward (gain trace headline 0.227), DOWN under degeneration (decay connectivity lost 5.52, the inverse), and UP into a self-holding well under negatively-reinforced coordination (stabilisation deep trace 0.498, gain's direction not decay's); the three directions are DISTINCT (mass sorts gain+stabilisation together vs decay, and does NOT yet split gain from stabilisation). T3 THREE READOUTS -- cue-reactivity (gain responds MORE to the same cue), loss-of-responsiveness (decay responds LESS), self-sustenance at rest (stabilisation holds Rlock~0.405 above the anchor with NO cue, over the cold-start branch Rfresh~0.396); the readout is what distinguishes the three, and it lines up with the disorders exactly. T4 SAME FAMILY / DIFFERENT READOUT (the sharpest single fact) -- driven to the SAME operating point the gain and stabilisation traces are LITERALLY IDENTICAL (0.35285 == 0.35285, every digit), the same consolidation family, and OCD is distinguished NOT by a different trace but by the self-sustaining-at-rest readout (Rlock~0.403 above the anchor): exactly the honest disanalogy §41 declared -- §37's reward sign came from an engine signal (M5 RPE), §41 had none and so grounded stabilisation as the SAME family as the gain distinguished by readout; the synthesis shows that hedge is the LITERAL truth. T5 ONE SEAM / ONE HANDLE -- in EVERY one of the three the instant symptomatic lever leaves the retained STRUCTURAL quantity EXACTLY unchanged (relief WITHOUT re-writing, the convergence seam: gain's extinction persists, decay's levers do not rebuild, stabilisation's levers do not unstick), and the ONLY handle on the structural trajectory lives on the PLASTICITY axis (the schedule of exposure for the gain, the rate of progression for the decay, the rate of consolidation -- where ERP acts -- for the stabilisation): the framework-level statement of why a symptomatic route and a learning-based/disease-modifying route are CATEGORICALLY different (a different axis, not a degree). Registered as the 20th and FINAL atlas citizen (E0-SYNTH), placed LAST in the run order so the three source JSONs are freshly regenerated before their hashes are re-verified. FIREWALL inherited THREEFOLD and absolute: every trace, loss and locked coordination is a STRUCTURAL quantity, NEVER the felt quality of a craving, of memory or selfhood, or of an intrusive thought or compulsion (Axis-A; consciousness_claim=0; hard problem OPEN); addiction is a chronic relapsing medical condition, a person with dementia remains a person, OCD is treatable and an intrusive thought is a symptom not a moral failing; only structural SIGNS and RELATIONS are asserted, every MAGNITUDE is [O]; nothing is a cure, reversal, or prevention; efficacy=0; not medical advice",
        "grade": "[V synth]",
        "meaning": "the capstone of the three-mode E0-dynamics arc. The addiction (§37), "
                   "Alzheimer's (§39) and OCD (§41) chapters each modelled one named disorder "
                   "DIRECTLY on the SAME §26 E0 plasticity layer -- addiction as GAIN (a sensitised "
                   "reward trace that responds MORE to a cue), Alzheimer's as DECAY (the structural "
                   "inverse, a substrate LOST), OCD as STABILISATION (a self-sustaining trace that "
                   "holds its own coordination AT REST with no cue). With the third face frozen the "
                   "arc closes, and this chapter is a META-SYNTHESIS -- NOT a new model -- that steps "
                   "back to certify the single structural statement they jointly make: ONE plasticity "
                   "layer, read THREE ways. It runs ZERO new measurements, adds ZERO new machinery, "
                   "derives ZERO new tuned constants. Its discipline is the discipline of a synthesis: "
                   "the three source results JSONs are the SSOT, and BEFORE reading a single number it "
                   "re-computes each one's SHA-256 and checks it BIT-FOR-BIT against the frozen value "
                   "(GAIN 20dfb3e9..., DECAY 7a8e8513..., STABILISATION ef37d619...); only then are "
                   "they read; the engine is emerged READ-ONLY for the invariant check and confirmed "
                   "byte-unchanged (0fbf4988...), the M0-16 subtree identical. FIVE certifications "
                   "hold, all CONFIRMED. T1 ONE SHARED LAYER -- all three import the SAME "
                   "PlasticConnectome, and with the plasticity process switched off (addiction eta=0, "
                   "Alzheimer's decay-rate=0, OCD consolidation=0) all three connectomes revert to the "
                   "SAME frozen M9 anchor (R~0.38961) BIT-FOR-BIT, each module's own guard asserting "
                   "it at full precision: one layer, one off-state -- the structure the gain "
                   "consolidates onto, the substrate the decay strips from, and the baseline the loop "
                   "locks around are all the SAME anchor. T2 THREE DIRECTIONS OF MASS -- the same "
                   "update moves structure UP under reward (gain, retained trace headline 0.227), DOWN "
                   "under degeneration (decay, connectivity lost 5.52, the structural inverse), and UP "
                   "into a self-holding well under negatively-reinforced coordination (stabilisation, "
                   "deep trace 0.498, gain's direction not decay's); the three directions are DISTINCT, "
                   "the mass cut sorting gain+stabilisation together (both up) against decay (down) and "
                   "deliberately NOT yet splitting gain from stabilisation. T3 THREE READOUTS -- what "
                   "distinguishes the three is what the trace DOES: cue-reactivity (gain responds MORE "
                   "to the same cue), loss-of-responsiveness (decay responds LESS), self-sustenance at "
                   "rest (stabilisation holds Rlock~0.405 above the anchor with NO cue, over the cold-"
                   "start branch Rfresh~0.396) -- three readouts the one layer produces, lining up "
                   "with the disorders exactly (over-response to cues / progressive loss / a self-"
                   "sustaining loop). T4 SAME FAMILY, DIFFERENT READOUT (the sharpest single fact) -- "
                   "driven to the SAME operating point the gain and stabilisation traces are LITERALLY "
                   "IDENTICAL (0.35285 == 0.35285, to every digit), the same consolidation family, and "
                   "what makes OCD OCD is NOT a different trace but the self-sustaining-at-rest readout "
                   "(Rlock~0.403 above the anchor): this is EXACTLY the disanalogy §41 declared -- "
                   "§37 could ground its reward sign in an engine signal (the M5 dopamine reward-"
                   "prediction error), §41 had NO such signal and so grounded stabilisation as the "
                   "SAME family as the gain distinguished only by the readout, and the synthesis shows "
                   "that honest hedge is the LITERAL truth (identical trace, the readout the only "
                   "separator). T5 ONE SEAM, ONE HANDLE -- in EVERY one of the three the instant "
                   "symptomatic lever leaves the retained STRUCTURAL quantity EXACTLY unchanged (relief "
                   "WITHOUT re-writing, the convergence seam: gain's extinction persists, decay's "
                   "levers do not rebuild, stabilisation's levers do not unstick), and the ONLY handle "
                   "on the structural trajectory lives on the PLASTICITY axis (the schedule of exposure "
                   "for the gain, the rate of progression for the decay, the rate of consolidation -- "
                   "where exposure-and-response-prevention acts -- for the stabilisation): one seam, "
                   "one axis, the framework-level statement of why a symptomatic route and a learning-"
                   "based or disease-modifying route are CATEGORICALLY different -- different handles "
                   "on different variables, only one of which reaches the structure. The triad is, at "
                   "heart, a single contrast table (the three faces by direction / readout / sign "
                   "grounding / handle), set side by side. Registered in run_all_atlas.py as the 20th "
                   "and FINAL atlas citizen (E0-SYNTH), placed LAST so the three source JSONs are "
                   "freshly regenerated before their hashes are re-verified; reproduces bit-for-bit "
                   "with the engine byte-unchanged. FIREWALL inherited THREEFOLD and absolute: every "
                   "trace, loss and locked coordination is a STRUCTURAL quantity, NEVER the felt "
                   "quality of a craving, of memory or selfhood under dementia, or of an intrusive "
                   "thought or compulsion (Axis-A; consciousness_claim=0; hard problem OPEN); addiction "
                   "is a chronic, relapsing medical condition, a person living with dementia remains a "
                   "person of undiminished dignity, OCD is a treatable condition and an intrusive "
                   "thought is a SYMPTOM not a wish, a character flaw, or a moral failing; only "
                   "structural SIGNS and RELATIONS are asserted and every MAGNITUDE is [O]; there is no "
                   "new mechanism, no new measurement and no new tuned constant; NOTHING here is a "
                   "cure, a reversal, a prevention, a treatment, or a dose; efficacy_tested=0; not "
                   "medical advice; hard problem OPEN.",
        "canonical": "42-e0-triad-synthesis",
        "check": None,
    },
    "e1_spatial_localisation": {
        "label": "spatial localisation = the field-shaping layer; the per-node spatial drive the global-drive atlas never had",
        "value": "generalising the engine's scalar coupling Kglob to a per-node vector Kvec (a spatial drive profile) and reading a per-node local-coherence field makes focal-vs-diffuse drive representable; the field has a FIXED spatial structure (the kernel is local and normalised, exact), perturbation reach is heterogeneous with a drive-stable cerebellar hub, and each node's self-localising/relay class is drive-invariant — but there is NO universal focal>diffuse law, so disease built on this layer is region-specific",
        "grade": "[V mech]",
        "meaning": "every disorder module to date drove the brain GLOBALLY — one scalar Kglob raised or "
                   "lowered for the whole network at once (schizophrenia, epilepsy, the θ-cap) — so focal-vs-"
                   "diffuse stimulation, off-target spillover and region-specific disease could not even be "
                   "posed: the fault was always global and the drive had no spatial profile. This layer "
                   "generalises the scalar to a per-node coupling vector Kvec_i = k(b_i)·OMEGA0 set through the "
                   "SAME k=κ/(1−|b|)[excit]/κ/(1+|b|)[inhib] cap 2κ map as the SZ/epilepsy/E0 modules (no new "
                   "constant), and reads a per-node local-coherence field c_i = <Σ_j W₀_ij cos(θ_j−θ_i)> — a "
                   "READ-ONLY side computation that never perturbs the θ trajectory. The FORM is forced [F] "
                   "(the frozen ~1/r³ row-stochastic kernel W₀ plus the existing k(b) map); the spatial PROFILE "
                   "(driven node, depth b0) is [O] swept and every SIGN/STRUCTURE holds across a depth sweep "
                   "b0∈{0.3,0.5,0.7,0.9} (anti-tuning), so no number is fit. Four results: (E1.1) the frozen "
                   "kernel is LOCAL (every row's weight monotone-decreases with anatomical distance, all 12 "
                   "rows) and NORMALISED (every row sums to 1, deviation 2e-16) — exact geometric structure, "
                   "the substrate of every focal/region claim; (E1.2) driving one node at a time and reading "
                   "the change in the GLOBAL order, reach(i)=|R−R0| is strongly heterogeneous (max/min>100) and "
                   "the map is NOT an artefact of drive amplitude — the cerebellum is the rank-1 reach hub at "
                   "EVERY swept depth and the full ranking is invariant for moderate-to-high drive (Spearman=1.0 "
                   "among b0≥0.5), the hub structure a connectome invariant; (E1.3, the headline) each node's "
                   "focal footprint is SELF-LOCALISING (own |Δc|>mean off-target) or a RELAY (lands harder off-"
                   "target), and this binary classification is IDENTICAL across the entire depth sweep — the "
                   "relay set {hippocampus, midbrain} fixed at every drive amplitude, whether a site contains "
                   "or relays its drive a fixed property of where it sits in the field; (E1.4, the honest no-"
                   "tuning result) a clean hypothesis — 'focal drive always concentrates local gain at its "
                   "target more than the same dose spread diffusely' — is FALSE: delivering equal total dose "
                   "focally vs diffusely the sign of (focal−diffuse target-gain) VARIES across sites (9/12 "
                   "concentrate, others do not), so spatial OUTCOME is site-determined, not governed by a "
                   "global rule — exactly why disease modules built on this layer must be REGION-SPECIFIC, "
                   "never global; the refuted clean hypothesis is reported honestly rather than forced. A "
                   "uniform (zero-bias) drive reproduces the frozen M9 coordination anchor (R=0.38961455156) "
                   "BIT-FOR-BIT and the off-state field equals the baseline exactly — E1 is a pure ADD-ON. The "
                   "SpatialField class is the reusable layer the later region-specific modules (focal foci, "
                   "lesion fields, off-target neuromodulation) import; those applications are OWED. Engine "
                   "imported READ-ONLY and byte-unchanged (0fbf4988…), M0-16 subtree identical; no new tuned "
                   "constant. Axis-A firewall: a local-coherence field, a reach map and a self/relay class are "
                   "STRUCTURAL spatial quantities of the coupling model, NEVER the felt locus of an experience "
                   "and NOT a real electrode, current density or dose (consciousness_claim=0; hard problem "
                   "OPEN); efficacy=0; not medical advice.",
        "canonical": "43-spatial-localisation",
        "check": None,
    },
    "focal_epilepsy_spread": {
        "label": "focal epilepsy = containment vs secondary generalisation; the first region-specific application of the spatial layer",
        "value": "driving each region as a focal ictal focus on the frozen kernel, the 12 foci partition into CONTAINED (the seizure stays focal) and BROADCAST (it secondarily generalises), and this partition is DRIVE-INVARIANT — the broadcast set {hippocampus, midbrain} fixed at every ictal intensity; broadcast IS off-target dominance (the ictal change lands harder on distal circuits than on the focus); but off-target spread is NOT global hypersynchrony — the largest global recruiter is the CONTAINED cerebellum and the two broadcast foci move global synchrony in opposite directions, two decoupled axes — so secondary-generalisation propagation is site-determined, containment the structural default",
        "grade": "[V mech]",
        "meaning": "the FIRST region-specific application of the §43 spatial-localisation layer, and the "
                   "spatial refinement of the §25 (T2a) over-synchronisation epilepsy module. §25 certified "
                   "the seizure as the network crossing the over-sync threshold on the GLOBAL order R, but it "
                   "drove the brain GLOBALLY (one scalar Kglob), so it could not ask the central clinical "
                   "question about a FOCAL epilepsy: does a seizure that BEGINS at one focus STAY focal or "
                   "SECONDARILY GENERALISE? That is intrinsically SPATIAL, and §43 (E1) is the layer that makes "
                   "‘where’ representable. This module IMPORTS the SpatialField class (it does NOT re-derive the "
                   "ephaptic kernel or the k(b) coupling map) and reads a focal seizure focus as a strong focal "
                   "EXCITATORY ictal drive at one region (the rest baseline, same k=κ/(1−|b|) map, no new "
                   "constant), with the ictal intensity SWEPT over {0.3,0.5,0.7,0.9} and every sign required to "
                   "hold at every intensity. Four results. (F1) The containment/broadcast partition is DRIVE-"
                   "INVARIANT: each focus is CONTAINED (self-localising — the ictal change concentrates at the "
                   "focus, the seizure stays focal) or BROADCAST (relay — the change lands harder off-target, the "
                   "seizure secondarily generalises), and the broadcast set {hippocampus, midbrain} is fixed at "
                   "every intensity — whether a focal seizure stays focal or generalises is a property of focus "
                   "LOCATION, inheriting the E1.3 self/relay class. (F2) Broadcast IS off-target dominance: for a "
                   "broadcast focus the mean off-target local-coherence change exceeds its own (ratio>1) — the "
                   "structural content of a seizure recruiting circuits BEYOND its focus — for a contained focus "
                   "it concentrates at the focus (ratio<1), the equivalence holding at every intensity. (F3, the "
                   "honest no-tuning result) Off-target spread is NOT global hypersynchrony: the clean hypothesis "
                   "‘the broadcast foci are exactly the foci that drive the whole brain into the §25 over-sync "
                   "state’ is FALSE — the single largest global-reach focus is the CEREBELLUM, which is CONTAINED, "
                   "at every intensity, and the two broadcast foci move global synchrony in OPPOSITE directions "
                   "(the midbrain RAISES global R toward over-sync, the hippocampus LOWERS it) — so off-target "
                   "spread and the §25 over-sync axis are TWO DISTINCT, decoupled spatial properties and "
                   "secondary-generalisation propagation is site-determined; the refuted clean hypothesis is "
                   "reported honestly (the E1.4 lesson for epilepsy). (F4) The broadcast set is a COHERENT "
                   "MINORITY relay-hub class: {hippocampus, midbrain} is simultaneously the E1.3 relay set and the "
                   "off-target-dominant set, a strict minority (2 of 12 — containment the structural default), and "
                   "disjoint from the global-reach hub — secondary generalisation is structurally the EXCEPTION "
                   "carried by specific relay hubs; a [L] direction-only correspondence is noted (most focal "
                   "seizures stay focal, mesial-temporal/hippocampal foci are the paradigmatic secondarily-"
                   "generalising epilepsy), never a patient-level prediction. A zero ictal drive reproduces the "
                   "frozen M9 anchor (R=0.38961455156) BIT-FOR-BIT and the off-state field equals the baseline "
                   "exactly — a pure structural read on the frozen kernel; engine imported READ-ONLY and byte-"
                   "unchanged (0fbf4988…), no new tuned constant, SpatialField reused not re-derived. Axis-A "
                   "firewall: a containment/broadcast class is a STRUCTURAL spatial quantity of the coupling "
                   "model, NEVER the felt locus of a seizure, and NOT a real electrode, EEG/SEEG localisation, "
                   "current density, seizure-propagation map, a prediction of which seizures generalise, or "
                   "surgical guidance (consciousness_claim=0; hard problem OPEN); efficacy=0; not medical advice.",
        "canonical": "44-focal-epilepsy-spread",
        "check": None,
    },
    "lesion_field_diaschisis": {
        "label": "stroke/lesion field = local deficit vs remote diaschisis; the second region-specific application of the spatial layer",
        "value": "silencing each region as a focal lesion (an inhibitory bias on the frozen kernel, the node SILENCED not deleted) the 12 lesions partition into LOCAL-DEFICIT (the dysfunction stays local) and REMOTE-DIASCHISIS (the lesion disrupts distant circuits more than itself), and this partition is DRIVE-INVARIANT over the moderate-to-severe core — the diaschisis set {hippocampus, midbrain} fixed at every severity, = the E1.3 relay set; remote diaschisis IS off-target dominance (the change lands harder on distal circuits than on the lesion); but global-coordination disruption is NOT remote diaschisis — the single largest global disruptor is the LOCAL-deficit cerebellum and, unlike §44, the reach hub is NOT drive-invariant (cerebellum→midbrain at −0.9), two decoupled axes — so remote-dysfunction propagation is site-determined, local deficit the structural default",
        "grade": "[V mech]",
        "meaning": "the SECOND region-specific application of the §43 spatial-localisation layer, and the "
                   "destructive-lesion DUAL of the §44 focal-epilepsy module. §44 read the spatial map under an "
                   "EXCITATORY ictal drive (does a focal seizure stay focal or secondarily generalise?); this "
                   "module reads the SAME map under a SILENCING (inhibitory) bias — a focal lesion — and asks the "
                   "dual clinical question for a STROKE: does destroying one region produce a purely LOCAL deficit "
                   "or disrupt REMOTE, connected regions MORE than the lesion site itself (DIASCHISIS, von "
                   "Monakow's classical concept of remote dysfunction after focal injury). A lesion = a strong "
                   "focal INHIBITORY bias at one region (the rest baseline, same k=κ/(1+|b|) inhib map, no new "
                   "constant); the lesioned node is SILENCED, NOT deleted — deleting a node would break the frozen "
                   "W0 and forfeit kernel reuse (handover's explicit lesion-modelling directive) — so the lesion "
                   "is read on the INTACT frozen kernel, severity SWEPT over {−0.5,−0.7,−0.9} (the moderate-to-"
                   "severe floor inherited from E1.2), every sign required to hold at every severity. Four "
                   "results. (L1) The local-deficit/remote-diaschisis partition is DRIVE-INVARIANT: each lesion is "
                   "LOCAL-DEFICIT (the coordination change concentrates at the lesion, the dysfunction stays "
                   "local) or REMOTE-DIASCHISIS (the change lands harder off-target, the lesion disrupts distant "
                   "circuits more than itself), and the diaschisis set {hippocampus, midbrain} is fixed at every "
                   "severity — whether a lesion stays local or causes diaschisis is a property of lesion "
                   "LOCATION — and that set is EXACTLY the E1.3 relay set read under silencing. (Honest scope: at "
                   "a MILD sub-floor −0.3 the thalamus ALSO enters the diaschisis set; this is reported plainly "
                   "and is NOT part of the drive-invariant claim, asserted only over the moderate-to-severe core.) "
                   "(L2) Remote diaschisis IS off-target dominance: for a diaschisis lesion the mean off-target "
                   "local-coherence change exceeds its own (ratio>1 — midbrain ~3.0×, hippocampus ~1.2×) — the "
                   "structural content of remote dysfunction after focal injury — for a local-deficit lesion it "
                   "concentrates at the site (ratio≪1 — cerebellum ~0.06×), the equivalence holding at every "
                   "severity. (L3, the honest no-tuning result) Global disruption is NOT remote diaschisis: the "
                   "clean hypothesis 'the lesions that most disrupt GLOBAL coordination are exactly the remote-"
                   "diaschisis lesions' is FALSE — the single largest global disruptor is the CEREBELLUM, a "
                   "LOCAL-deficit lesion (off/own≪1, no diaschisis) that is rank-1 global disruptor at the "
                   "moderate severities and top-3 at every severity, i.e. a lesion can MAXIMISE global disruption "
                   "while being maximally LOCAL; and unlike §44 (where the reach hub was drive-invariant) the "
                   "reach hub here is NOT drive-invariant (cerebellum tops reach at −0.5/−0.7, midbrain overtakes "
                   "at −0.9) — so remote diaschisis and global-coordination disruption are TWO DISTINCT, decoupled "
                   "spatial axes and remote-dysfunction propagation is site-determined; the refuted clean "
                   "hypothesis is reported honestly (the E1.4 lesson for stroke). (L4) The diaschisis set is a "
                   "COHERENT MINORITY relay-hub class: {hippocampus, midbrain} is simultaneously the E1.3 relay "
                   "set and the off-target-dominant set, a strict minority (2 of 12 — local deficit the structural "
                   "default), and disjoint from the global-disruption hub — remote diaschisis is structurally the "
                   "EXCEPTION carried by specific relay hubs; a [L] direction-only correspondence is noted (most "
                   "focal lesions produce focal deficits; diaschisis — crossed cerebellar diaschisis, "
                   "thalamic/limbic remote effects, von Monakow's concept — is the recognised exception at "
                   "specific connected hubs), never a patient-level prediction. A zero lesion reproduces the "
                   "frozen M9 anchor (R=0.38961455156) BIT-FOR-BIT and the off-state field equals the baseline "
                   "exactly — a pure structural read on the frozen kernel; engine imported READ-ONLY and byte-"
                   "unchanged (0fbf4988…), no new tuned constant, SpatialField reused not re-derived. Axis-A "
                   "firewall: a local-deficit/diaschisis class is a STRUCTURAL spatial quantity of the coupling "
                   "model, NEVER the felt experience of a stroke, and NOT a real lesion, infarct/perfusion/"
                   "diffusion map, connectome-diaschisis measurement, stroke-outcome prediction, or rehabilitation/"
                   "clinical guidance (consciousness_claim=0; hard problem OPEN); efficacy=0; not medical advice.",
        "canonical": "45-lesion-field-diaschisis",
        "check": None,
    },
    "targeted_neuromodulation_offtarget": {
        "label": "targeted neuromodulation = clean delivery vs off-target leak; the third and final region-specific application of the spatial layer, closing the E1 trilogy",
        "value": "aiming a focal therapeutic stimulation (DBS/TMS/tDCS, modelled as the SAME excitatory bias §44 used, k=κ/(1+|b|), no new constant) at each region, the 12 targets partition into CLEAN-DELIVERY (the excitation concentrates where it is aimed) and OFF-TARGET-LEAK (the excitation bleeds to distal circuits), and this partition is DRIVE-INVARIANT at EVERY swept intensity INCLUDING the mildest (no sub-floor caveat, an honest contrast with §45's inhibitory case) — the leak set {hippocampus, midbrain} fixed at every intensity, = the E1.3 relay set; off-target leak IS off-target dominance (off/own>1 — hippocampus ~4.2×, midbrain ~1.6×; clean cerebellum ~0.04×); clean delivery and global reach are DECOUPLED — the cleanest target (cerebellum) is ALSO the largest-global-reach target at every intensity and the reach hub IS drive-invariant (inheriting §44, the honest contrast with §45), refuting 'focal=weak, leaky=strong', and the two leak targets push global R in OPPOSITE directions (hippocampus lowers, midbrain raises), so leak is not a controllable point-to-point relay — clean delivery the structural default; the spatial numbers COINCIDE with §44 (same excitatory drive, stated plainly), what is new is the therapeutic target-selection reading and the N3 decoupling",
        "grade": "[V mech]",
        "meaning": "the THIRD and FINAL region-specific application of the §43 spatial-localisation layer, and the "
                   "THERAPEUTIC re-reading of the §44 focal-epilepsy module, CLOSING the E1 application trilogy "
                   "(containment/broadcast for seizures §44 · local/diaschisis for stroke §45 · clean/leak for "
                   "neuromodulation §46). §44 read the spatial map under an EXCITATORY ictal drive (does a focal "
                   "seizure stay focal or generalise?); this module reads the SAME excitatory map under the SAME "
                   "k=κ/(1+|b|) coupling but RE-FRAMES the drive as a therapeutic focal stimulation (deep brain "
                   "stimulation, transcranial magnetic/direct-current stimulation) and asks the dual clinical "
                   "question of TARGET SELECTION: aim a focal stimulation at a region — does the excitation DELIVER "
                   "CLEANLY (self-localising, the stimulation concentrates where it is aimed) or LEAK OFF-TARGET "
                   "(relay, the stimulation bleeds to distal circuits)? Because this module reads the SAME "
                   "excitatory spatial map as §44, the footprint classes, reach map and off-target ratios COINCIDE "
                   "NUMERICALLY with §44 — STATED PLAINLY as the central no-overclaiming point (a focal excitatory "
                   "drive is a focal excitatory drive; the numbers are NOT a fresh measurement). What is NEW is (a) "
                   "the THERAPEUTIC target-selection reading (a relay target = off-target leak, a self-localising "
                   "target = clean delivery, distinct from §44's seizure-prognosis framing) and (b) the N3 honest-"
                   "negative DECOUPLING result. Intensity SWEPT over {0.3,0.5,0.7,0.9}, every sign required to hold "
                   "at every intensity. Four results. (N1) The clean-delivery/off-target-leak partition is DRIVE-"
                   "INVARIANT: each target is CLEAN-DELIVERY (the change concentrates at the target) or OFF-TARGET-"
                   "LEAK (the change lands harder off-target), and the leak set {hippocampus, midbrain} is fixed at "
                   "every intensity — whether aiming at a region delivers cleanly or leaks is a property of target "
                   "LOCATION — and that set is EXACTLY the E1.3 relay set. Unlike §45's inhibitory case (a marginal "
                   "node crossed in only at a mild sub-floor severity), the EXCITATORY partition is exactly stable "
                   "at EVERY intensity INCLUDING the mildest (0.3) — NO sub-floor caveat, inheriting §44's full-"
                   "sweep scope, an honest contrast with the destructive dual. (N2) Off-target leak IS off-target "
                   "dominance: for a leak target the mean off-target local-coherence change exceeds its own "
                   "(ratio>1 — hippocampus ~4.2×, midbrain ~1.6×) — a stimulation that bleeds away from where it is "
                   "aimed — for a clean target it concentrates at the site (ratio≪1 — cerebellum ~0.04×, the "
                   "cleanest delivery), the equivalence holding at every intensity (these are §44's ratios re-read "
                   "as delivery quality). (N3, the honest no-tuning result) Clean delivery and global reach are "
                   "DECOUPLED: the clean hypothesis 'to get a large GLOBAL effect you must accept off-target leak; "
                   "a clean target is necessarily a WEAK one' is FALSE — the single largest global-reach target is "
                   "the CEREBELLUM, a CLEAN-delivery target (off/own≪1, no leak) that is rank-1 at EVERY intensity, "
                   "i.e. a target can MAXIMISE global effect while delivering maximally CLEANLY, refuting "
                   "'focal=weak, leaky=strong'; and unlike §45 the reach hub IS drive-invariant (cerebellum at "
                   "every intensity, inheriting §44). Moreover the two leak targets push global R in OPPOSITE "
                   "directions (hippocampus LOWERS R, midbrain RAISES it, at every intensity) — leak is site-"
                   "determined in magnitude AND direction, NOT a controllable point-to-point relay a clinician "
                   "could aim through — so clean delivery and global reach are TWO DISTINCT, decoupled spatial axes; "
                   "the refuted clean hypothesis is reported honestly (the E1.4 lesson for neuromodulation). (N4) "
                   "The leak set is a COHERENT MINORITY relay-hub class: {hippocampus, midbrain} is simultaneously "
                   "the E1.3 relay set and the off-target-dominant set, a strict minority (2 of 12 — clean delivery "
                   "the structural default), and disjoint from the global-reach hub — off-target leak is "
                   "structurally the EXCEPTION carried by specific relay hubs; a [L] direction-only correspondence "
                   "is noted (off-target effects of focal neuromodulation — current spread beyond target, DBS "
                   "co-recruitment of adjacent/connected structures, TMS/tDCS network spread — are a recognised "
                   "concern at specific connected hubs), never a patient-level prediction. A zero stimulation "
                   "reproduces the frozen M9 anchor (R=0.38961455156) BIT-FOR-BIT and the off-state field equals "
                   "the baseline exactly — a pure structural read on the frozen kernel; engine imported READ-ONLY "
                   "and byte-unchanged (0fbf4988…), no new tuned constant, SpatialField reused not re-derived, the "
                   "spatial numbers are §44's own. Axis-A firewall: a clean-delivery/off-target-leak class is a "
                   "STRUCTURAL spatial quantity of the coupling model, NEVER a felt effect of stimulation, and NOT "
                   "a real electric-field/current-density map, lead-position/SAR map, real connectome, prediction "
                   "of which patient's stimulation leaks or which target is optimal, or device-programming/target-"
                   "selection guidance (consciousness_claim=0; hard problem OPEN); efficacy=0; not medical advice.",
        "canonical": "46-targeted-neuromodulation-offtarget",
        "check": None,
    },
    "spatial_plasticity_imprint": {
        "label": "spatial-plasticity imprint = local delivery vs relayed consolidation; the FIRST cross-axis coupling, marrying the E1 spatial layer (WHERE) to the E0 plasticity layer (LASTING)",
        "value": "driving a focal therapeutic stimulation (modelled as the SAME excitatory bias §44/§46 used, k=κ/(1+|b|), no new constant) at each region and then letting the E0 phase-Hebbian update consolidate the coincidences it provokes (new integrator stepping the per-node spatial drive on the EVOLVING connectome), the 12 targets partition into LOCAL-IMPRINT (the lasting synaptic trace concentrates where the drive is aimed) and RELAYED-IMPRINT (the trace lands harder on distal circuits), and this partition is DRIVE-INVARIANT across BOTH the intensity sweep {0.3,0.5,0.7,0.9} AND the consolidation-rate sweep {0.03,0.05,0.08} — exactly one partition over the whole grid — the local set {brainstem, cerebellum, pallidum, striatum} fixed throughout; relayed imprint IS off-target-dominant trace (off/own>1) at every intensity and rate; the genuinely-new coupling result — the trace-relay set STRICTLY CONTAINS the §46 field-relay set {hippocampus, midbrain}: plasticity DELOCALISES imprint, so clean DELIVERY does NOT imply clean IMPRINT — six witness sites (neocortex, thalamus, hypothalamus, basal_forebrain_chol, forebrain_gaba_in, olfactory_bulb) self-localise the instantaneous field yet imprint OFF-TARGET once consolidation runs; relayed imprint is the STRUCTURAL DEFAULT (strict majority 8 of 12, an honest contrast with §46's clean-default 10 of 12); and the honest negative — there is NO universal focal>diffuse trace law (only 3 of 12 imprint more under a focal than a diffuse drive); what is new is the COUPLING reading (a lasting trace, not an instantaneous field) and the delivery/imprint decoupling",
        "grade": "[V mech]",
        "meaning": "the FIRST cross-axis coupling in the atlas — every prior E1 module (§44 containment/broadcast, "
                   "§45 local/diaschisis, §46 clean/leak) re-read the SAME §43 spatial map on a SINGLE axis (space), "
                   "and every prior E0 module (§37/§39/§41) consolidated on the SINGLE axis of time; this module "
                   "MARRIES the two, importing BOTH the §43 SpatialField (per-node drive, NOT re-derived) and the "
                   "§26 PlasticConnectome (phase-correlation Hebbian update, NOT re-derived) and asking the question "
                   "neither axis can answer alone: a focal stimulation DELIVERS to a place (E1) and then the network "
                   "CONSOLIDATES what the drive provoked (E0) — so WHERE does a focal drive leave a LASTING synaptic "
                   "imprint, and is that place the same as where the instantaneous field landed? A new integrator "
                   "(_integrate_coupled) steps the per-node spatial drive vector on the EVOLVING connectome while "
                   "accumulating the pairwise phase-coincidence the E0 rule consolidates, re-seeding the engine's own "
                   "fixed incoherent IC each epoch (deterministic). Intensity SWEPT over {0.3,0.5,0.7,0.9} AND "
                   "consolidation rate over {0.03,0.05,0.08}; every sign required to hold across the WHOLE product "
                   "grid. Four results. (C1) The local-imprint/relayed-imprint partition is DRIVE-INVARIANT across "
                   "BOTH sweeps: each target's lasting trace either concentrates where the drive is aimed (LOCAL "
                   "IMPRINT) or lands harder off-target (RELAYED IMPRINT), and the local set {brainstem, cerebellum, "
                   "pallidum, striatum} is fixed at every (intensity, rate) — whether a focal drive imprints locally "
                   "is a property of target LOCATION, stable under both how hard and how fast you drive. (C2) Relayed "
                   "imprint IS off-target dominance: for a relayed target the mean off-target consolidated trace "
                   "exceeds its own (ratio>1), for a local target it concentrates at the site (ratio<1), the "
                   "equivalence holding across the whole grid — the consolidated read of the §46 leak quality. (C3, "
                   "the genuinely-new coupling result + the honest negative) DELIVERY and IMPRINT are DECOUPLED: the "
                   "trace-relay set STRICTLY CONTAINS the §46 instantaneous field-relay set {hippocampus, midbrain} "
                   "— plasticity DELOCALISES the imprint — so a target whose instantaneous field self-localises "
                   "CLEANLY (clean DELIVERY, §46) can still imprint OFF-TARGET once the trace consolidates (relayed "
                   "IMPRINT): six witness sites (neocortex, thalamus, hypothalamus, basal_forebrain_chol, "
                   "forebrain_gaba_in, olfactory_bulb) deliver cleanly yet imprint off-target, demonstrating that "
                   "clean delivery does NOT imply clean imprint; and the refuted clean hypothesis is reported "
                   "honestly — there is NO universal focal>diffuse trace law (only 3 of 12 imprint more under a "
                   "focal than a matched diffuse drive, heterogeneous not universal), the E0×E1 lesson that a "
                   "lasting trace is not a sharpened field. (C4) Relayed imprint is the STRUCTURAL DEFAULT: the "
                   "relayed-imprint set is a strict MAJORITY (8 of 12) — an honest CONTRAST with §46's clean-default "
                   "(10 of 12 delivered cleanly), the coupling INVERTS the majority because consolidation spreads "
                   "what delivery localised — it equals the off-target-dominant set and it CONTAINS the §46 field-"
                   "relay set; a [L] direction-only correspondence is noted (stimulation-induced plasticity from "
                   "rTMS/tDCS/DBS is network-distributed rather than confined to the stimulated site — a recognised "
                   "feature of therapeutic neuromodulation), never a patient-level prediction. A zero drive with "
                   "consolidation OFF (eta=0) reproduces the frozen M9 anchor (R=0.38961455156) BIT-FOR-BIT, eta=0 "
                   "leaves the connectome W identical to the kernel, and a focal excursion reverts EXACTLY when "
                   "consolidation is removed (inheriting the E0.3 guard) — a pure structural read on the frozen "
                   "kernel; engine imported READ-ONLY and byte-unchanged (0fbf4988…), no new tuned constant, BOTH "
                   "the SpatialField and the PlasticConnectome reused not re-derived. Axis-A firewall: a local-"
                   "imprint/relayed-imprint class is a STRUCTURAL spatial quantity of the coupled model, NEVER a "
                   "felt effect of stimulation or of learning, and NOT a real electric-field/current-density map, "
                   "lead-position/SAR map, real connectome or synaptic-weight matrix, prediction of which patient's "
                   "stimulation imprints where or which target consolidates optimally, or device-programming/"
                   "target-selection guidance (consciousness_claim=0; hard problem OPEN); efficacy=0; not medical "
                   "advice.",
        "canonical": "47-spatial-plasticity-imprint",
        "check": None,
    },
    "spatial_switch_leverage": {
        "label": "spatial switch leverage = which focal drive most easily FLIPS the collective state; the SECOND cross-axis coupling, marrying the E1 spatial layer (WHERE) to the E2 state-switching layer (the bistable flip)",
        "value": "driving the single collective R19 bistable state (the SAME §28/§29 BistableSwitch cell, imported) with a focal stimulation whose effective drive on that state is the driven node's frozen-kernel BROADCAST LEVERAGE (lev_j = colsum_j = Σ_i W0[i,j], the one-step ephaptic current node j injects into the network — a pure readout of the frozen kernel, no new constant), the 12 sites rank by how easily their focal drive flips the state (intensity threshold b0* = spinodal(g)/lev_j, inverse in leverage), and that flip-threshold rank EQUALS the broadcast-leverage rank and is BARRIER-INVARIANT across the well-depth sweep g∈{0.7,1.0,1.3} on the common finite-threshold set — the easiest-to-flip hub is basal_forebrain_chol, monotone in leverage down to a FIXED non-switching minority {thalamus, olfactory_bulb} that never flips at any swept intensity (b0≤1); ease-of-flip tracks leverage with CRITICAL SLOWING — both the threshold and the crossing latency at fixed supra-threshold drive are monotone-decreasing in leverage, the lowest-leverage finite-flip site (brainstem) showing the largest latency (the §28 ictal time-course given a spatial address); the genuinely-new coupling result — the switch-leverage axis is DECOUPLED from BOTH the §46 instantaneous-footprint axis (the field-relay set {hippocampus, midbrain} is MID-rank 5–6/12, the switch hub basal_forebrain_chol is §46 SELF-LOCALISING) AND the §43 reach axis, with the honest negative that there is NO universal reach→switchability law (the §43/§46 reach hub CEREBELLUM is switch-rank 10/12, one of the HARDEST to flip; the hard-to-switch set {thalamus, olfactory_bulb, cerebellum} all deliver CLEANLY in the instant yet cannot cheaply flip the state); and a coherent MAJORITY-SWITCHABLE structure (10 of 12) with the fixed non-switching minority — the honest contrast with §46's clean-delivery default; what is new is the COUPLING reading (which focal drive flips a bistable collective state, a question neither layer can pose alone) and the switchability/footprint/reach triple-decoupling",
        "grade": "[V mech]",
        "meaning": "the SECOND cross-axis coupling in the atlas and the spatial sibling of the §29 bipolar episode — "
                   "§29 imported the §28 BistableSwitch and asked WHEN the collective state flips under a TEMPORAL "
                   "drive; this module imports the SAME cell (NOT re-derived) together with the §43 SpatialField "
                   "(NOT re-derived) and asks the question neither axis can answer alone: a focal stimulation acts "
                   "at a PLACE (E1) and the collective state either FLIPS or holds (E2) — so WHICH region's focal "
                   "drive most easily flips the bistable state? The only new object is the §28 cell fed an effective "
                   "drive read straight off the frozen kernel: h_eff(j,b0) = b0·lev_j with lev_j = colsum_j of W0, "
                   "the total one-step ephaptic current node j broadcasts into the network (a pure frozen-kernel "
                   "readout — no new constant, no new rule); the state starts at the DOWN fixed point s0=−√g and "
                   "flips up iff h_eff crosses the fold spinodal(g) (E.spinodal, the SAME fold as M11/theta-cap/"
                   "epilepsy/E2). Stimulation intensity SWEPT over {0.3,0.5,0.7,0.9} AND barrier depth g over "
                   "{0.7,1.0,1.3}; every sign/order required to hold across BOTH sweeps. Four results. (C1) The "
                   "flip-threshold rank EQUALS the broadcast-leverage rank (b0*=spinodal/lev, inverse in leverage) "
                   "and is BARRIER-INVARIANT on the common finite-threshold set — the easiest-to-flip site is the "
                   "highest-leverage hub basal_forebrain_chol, monotone down to a FIXED non-switching minority "
                   "{thalamus, olfactory_bulb} whose leverage is too small for the strongest swept drive to cross "
                   "the fold; which focal drive most cheaply flips the state is a property of the frozen kernel's "
                   "broadcast structure, not of barrier depth nor stimulation intensity. (C2) Ease-of-flip tracks "
                   "leverage with CRITICAL SLOWING: the threshold and the crossing LATENCY at fixed supra-threshold "
                   "drive (b0=0.9) are both monotone-decreasing in leverage — a high-leverage hub flips the state "
                   "both more cheaply AND faster — and the lowest-leverage finite-flip site (brainstem) shows the "
                   "largest latency (the transition time diverging as the effective drive approaches the fold), the "
                   "§28 ictal time-course now given a spatial address. (C3, the genuinely-new coupling result + the "
                   "honest negative) switchability is DECOUPLED from BOTH the §46 instantaneous-footprint axis and "
                   "the §43 reach axis: the §46 field-relay set {hippocampus, midbrain} is MID-rank in switch "
                   "leverage (5–6 of 12, easily switchable, not special) and the switch hub basal_forebrain_chol is "
                   "§46 SELF-LOCALISING, so WHERE a focal drive's instantaneous effect lands and WHICH focal drive "
                   "flips the state are distinct axes; and the refuted clean hypothesis is reported honestly — the "
                   "§43/§46 reach hub CEREBELLUM (rank-1 reach at every depth, read from the E1 results) is switch-"
                   "rank 10 of 12, one of the HARDEST to flip, and the hard-to-switch set {thalamus, olfactory_bulb, "
                   "cerebellum} all self-localise (clean DELIVERY) yet cannot cheaply flip the state, so there is NO "
                   "universal reach→switchability law (reaching far, delivering cleanly, and flipping the collective "
                   "state are three distinct properties). (C4) A coherent MAJORITY-SWITCHABLE structure: a strict "
                   "MAJORITY (10 of 12) can have the collective state flipped by a swept drive, with the FIXED non-"
                   "switching minority {thalamus, olfactory_bulb} locked out — an honest CONTRAST with §46's clean-"
                   "delivery default (10 of 12 self-localising); a [L] direction-only correspondence is noted (the "
                   "highest-leverage hubs basal_forebrain_chol and hypothalamus are the classic global brain-state / "
                   "arousal control hubs, the locked-out/hard sites thalamic relay, olfactory bulb and cerebellum "
                   "are peripheral relay/motor-timing structures — direction-consistent with broadcast hubs gating "
                   "global brain-state switching), never a patient-level prediction. Removing the focal drive "
                   "(b0=0 → h_eff=0) settles the collective state via E.settle BIT-FOR-BIT (the static limit IS the "
                   "frozen engine, inheriting the E2.4 guard) and the fold is read from E.spinodal — a pure add-on "
                   "on the frozen kernel; engine imported READ-ONLY and byte-unchanged (0fbf4988…), no new tuned "
                   "constant, BOTH the SpatialField and the BistableSwitch reused not re-derived. Axis-A firewall: "
                   "the collective bistable state and its flip are STRUCTURAL quantities of the coupled model, NEVER "
                   "a felt state, an experienced arousal or a level of consciousness, and NOT a real electric-field/"
                   "current-density map, lead-position/SAR map, real connectome, prediction of which patient's "
                   "stimulation flips which brain state, or device-programming/target-selection guidance "
                   "(consciousness_claim=0; hard problem OPEN); efficacy=0; not medical advice.",
        "canonical": "48-spatial-switch-leverage",
        "check": None,
    },
    "e0e2_kindling": {
        "label": "kindling = do repeated state-flips become easier; the THIRD cross-axis coupling, marrying the E0 plasticity layer (the evolving connectome) to the E2 state-switching layer (the bistable flip), and the module that closes the trace→threshold link the §29 bipolar episode left OPEN",
        "value": "driving the single collective R19 bistable state (the SAME §28/§29 BistableSwitch cell, imported) through repeated FLIP EPISODES, letting each flip drive the §26 phase-Hebbian update so the connectome EVOLVES (the SAME §26 PlasticConnectome, imported), and reading the effective drive of an external push off the evolving connectome via its COORDINATION GAIN L(W) = R(W)/R_anchor (the order parameter at the measured coupling normalised by the frozen M9 anchor R(W0) = 0.38961455156044245 — a pure readout of the connectome, = 1 at W0, generalising the §48 broadcast leverage to the global coherence gain), the flip threshold in external push is p* = spinodal(g)/L(W), which DROPS as the connectome consolidates: repeated flips deepen the retained trace ‖dW‖ STRICTLY MONOTONICALLY and the threshold ends BELOW the un-kindled fold (KINDLING — repeated flips become easier), and the kindling is BARRIER-INVARIANT across the well-depth sweep g∈{0.7,1.0,1.3} (p* = spinodal(g)/L scales the fold by the same gain at every g) — this is the trace→threshold coupling the §29 bipolar episode (B3) named but left [O]; the push-space hysteresis loop 2·spinodal(g)/L NARROWS and the crossing latency at a fixed supra-threshold push SHORTENS (a learned change of the §28 hysteresis and a faster onset); the genuinely-new coupling result with the honest negative — kindling is CONSOLIDATIVE, NOT DEGRADATIVE: the clean hypothesis 'kindling erodes coordination, so easier-to-flip means less coordinated' is REFUTED, the connectome's coordination R(W) RISES (net, across the rate sweep) and the kindled connectome ends AT OR ABOVE the frozen anchor while the trace deepens, so easier-to-flip and erosion are DECOUPLED (the threshold falls through CONSOLIDATION, the connectome writing the repeated transition into its own structure, not through degradation); and a single coherent consolidative seam — the threshold is monotone-decreasing in the accumulated trace ‖dW‖ (the trace IS the kindling variable), with a [L] direction-only correspondence to clinical kindling (Goddard) and bipolar cycle acceleration; what is new is the COUPLING reading (whether repeated flips of a bistable state lower its own threshold, a question neither layer can pose alone — E0 has no flip, E2 has a frozen connectome) and the consolidative-not-degradative refutation",
        "grade": "[V mech]",
        "meaning": "the THIRD cross-axis coupling in the atlas and the module that CLOSES the trace→threshold "
                   "link the §29 bipolar episode left OPEN. The §26 plasticity layer built the evolving "
                   "connectome and its retained trace; the §28 state-switching layer built the bistable flip, "
                   "its fold and its hysteresis; §29 imported §28 and showed (B3) that alternating episodes "
                   "DEEPEN the connectome trace and separately noted a LOWER barrier flips more cheaply, but "
                   "left the actual trace→threshold COUPLING — whether and how the accumulated trace lowers the "
                   "threshold — explicitly [O]. This module supplies it. It imports BOTH layers (NOT re-derived) "
                   "and asks the question neither can pose alone: E0 has the plastic connectome but no bistable "
                   "flip, E2 has the flip but a frozen connectome so repetition cannot accumulate. The only new "
                   "object is the §28 cell driven through the §26 connectome: repeated FLIP EPISODES drive the "
                   "phase-Hebbian update so the connectome consolidates, and the effective drive of an external "
                   "push p on the collective state is scaled by the connectome's COORDINATION GAIN L(W) = "
                   "R(W)/R_anchor (a pure readout, = 1 at W0); the state flips iff h_eff = p·L crosses the fold "
                   "spinodal(g) (E.spinodal, the SAME fold as M11/theta-cap/epilepsy/E2), so the threshold p* = "
                   "spinodal(g)/L drops as L grows. Rate eta SWEPT {0.03,0.05,0.08} AND barrier g SWEPT "
                   "{0.7,1.0,1.3}; every sign required to hold across BOTH sweeps. Four results. (K1) Repeated "
                   "flips deepen the trace ‖dW‖ STRICTLY MONOTONICALLY and the flip threshold ends BELOW the "
                   "un-kindled fold — kindling, repeated flips become easier — and it is BARRIER-INVARIANT (at "
                   "every g the kindled threshold ends below that depth's own fold); the trace→threshold "
                   "coupling §29 (B3) left [O], now supplied. (K2) The push-space hysteresis loop 2·spinodal(g)/L "
                   "NARROWS (a learned change of the §28 hysteresis) and the crossing latency at a fixed "
                   "supra-threshold push SHORTENS (a faster §28 onset). (K3, the genuinely-new coupling result + "
                   "the honest negative) kindling is CONSOLIDATIVE, NOT DEGRADATIVE — the clean hypothesis "
                   "'kindling erodes coordination (R toward incoherence), so easier-to-flip means less "
                   "coordinated' is REFUTED: the threshold DROPS while R(W) RISES and the kindled connectome ends "
                   "AT OR ABOVE the frozen anchor (MORE coordinated, not less) as the trace deepens, so "
                   "easier-to-flip and erosion are DECOUPLED — the threshold falls through CONSOLIDATION, not "
                   "degradation; the refuted clean hypothesis is reported honestly (with a negligible "
                   "first-episode transient at the lowest rate disclosed). (K4) A single coherent consolidative "
                   "seam: the threshold is monotone-decreasing in the accumulated trace ‖dW‖ (the trace IS the "
                   "kindling variable — the explicit trace→threshold law §29 left open), with a [L] "
                   "direction-only correspondence (clinical kindling, Goddard; bipolar cycle acceleration — "
                   "repetition lowering the next transition's threshold), never a patient-level prediction. With "
                   "eta = 0 the connectome stays frozen, R = the frozen M9 anchor BIT-FOR-BIT so the gain L = 1 "
                   "and the threshold = the un-kindled fold exactly (E0.4), and with a zero push (h_eff = 0) the "
                   "collective state settles via E.settle BIT-FOR-BIT and the down state stays down (E2.4) — a "
                   "pure add-on; engine imported READ-ONLY and byte-unchanged (0fbf4988…), no new tuned "
                   "constant, no new rule, BOTH the PlasticConnectome and the BistableSwitch reused not "
                   "re-derived. Axis-A firewall: the collective bistable state, its flip threshold, the retained "
                   "trace and the coordination gain are STRUCTURAL quantities of the coupled model, NEVER a felt "
                   "state, an experienced mood, a level of consciousness or an experienced ease of relapse, and "
                   "NOT a real connectome, synaptic-weight matrix, measure of kindling/seizure threshold, or "
                   "prediction of whether any patient's episodes accelerate (consciousness_claim=0; hard problem "
                   "OPEN); efficacy=0; not medical advice.",
        "canonical": "49-kindling",
        "check": None,
    },
    "cross_axis_coupling_synthesis": {
        "label": "the cross-axis coupling synthesis (the v1.57 capstone): a META-SYNTHESIS -- zero new measurement, zero new machinery, zero new tuned constant -- that cross-reads the three now-frozen CROSS-AXIS COUPLING modules (spatial-plasticity imprint §47 E1×E0, spatial switch leverage §48 E1×E2, kindling §49 E0×E2) and certifies them as ONE FAMILY: the three pairwise EDGES of the same three layers E0 (plasticity), E1 (spatial localisation) and E2 (state switching), each layer appearing in exactly two couplings, sharing one shape -- the genuinely-new result each seam surfaces is a DECOUPLING of two quantities the single-axis intuition welds together; the three source results JSONs are the SSOT and their frozen SHA-256 are re-verified BIT-FOR-BIT before they are read, the engine is imported READ-ONLY and byte-unchanged; five certifications (T1 one family / the complete E0/E1/E2 triangle, T2 one new joining object per coupling, T3 three decouplings, T4 a common shape / a single-axis law breaks, T5 one coupling discipline), all CONFIRMED",
        "value": "the three preceding cross-axis couplings each married TWO of the atlas's three new layers -- the §47 imprint coupled the §43 spatial layer (E1, WHERE) to the §26 plasticity layer (E0, LASTING), the §48 leverage coupled E1 to the §28 state-switching layer (E2, the FLIP), the §49 kindling coupled E0 to E2 -- and with the third frozen, the trio of pairwise couplings CLOSES, and this capstone steps back to certify the single structural statement they jointly make: they are the complete set of PAIRWISE EDGES of three layers, read as ONE FAMILY with ONE SHAPE. It is a META-SYNTHESIS, not a new model: zero new measurement, zero new machinery, zero new tuned constant. Discipline of a synthesis -- the three source results JSONs are the SSOT, and BEFORE reading a single number the verifier re-computes each one's SHA-256 and checks it BIT-FOR-BIT against the frozen value (imprint cdb16230..., leverage bd3a9e23..., kindling 3880e63f...); only then are they read; the engine is emerged READ-ONLY for the invariant check and confirmed byte-unchanged (0fbf4988...). FIVE CERTIFICATIONS, all CONFIRMED: T1 ONE FAMILY / THE COMPLETE E0/E1/E2 TRIANGLE -- all three couple two of the layers (couples_E1_and_E0 / couples_E1_and_E2 / couples_E0_and_E2 = 1) and TOGETHER realise all three pairwise edges {E1,E0} {E1,E2} {E0,E2}, every layer-vertex appearing in EXACTLY TWO couplings (E0 in 47+49, E1 in 47+48, E2 in 48+49 -- degree two), and each reverts to the frozen engine BIT-FOR-BIT with its drive off (each module's own engine-invariance guard reproduced): one family, three edges, one off-state. T2 ONE NEW JOINING OBJECT PER COUPLING -- each marries its two layers with EXACTLY ONE new object and re-derives NEITHER (the imprint readout, a focal drive through the plastic connectome; the leverage switch, the bistable cell driven by a node's frozen-kernel broadcast leverage; the kindling switch, the bistable cell driven through the evolving connectome), each reusing BOTH its layers read-only, with NO new tuned constant in any (the broadcast leverage and the coordination gain are frozen/evolving-kernel READOUTS, not free weights). T3 THREE DECOUPLINGS -- the genuinely-new result each seam surfaces is a DECOUPLING, all three CONFIRMED: clean DELIVERY != clean IMPRINT (47 C3, the retained-trace relay set STRICTLY CONTAINS the instantaneous-field relay set, 8 ⊃ 2 -- plasticity delocalises the mark), SWITCHABILITY decoupled from both instantaneous FOOTPRINT and spatial REACH (48 C3, the reach hub cerebellum is among the HARDEST to flip, switch rank 10/12; the switch hub is basal_forebrain_chol), EASIER-TO-FLIP decoupled from EROSION (49 K3, the coordination R(W) RISES 0.3896→0.3964 as the threshold falls and the kindled connectome ends AT OR ABOVE the anchor -- consolidation, not degradation). T4 A COMMON SHAPE / A SINGLE-AXIS LAW BREAKS -- each decoupling REFUTES a tidy single-axis hypothesis the coupling was the natural place to test, reported HONESTLY (no universal focal>diffuse imprint law §47; no universal reach→switchability law §48; no clean kindling-erodes-coordination story §49), the no-tuning discipline producing the SAME honest-negative shape three times: when SPACE meets TIME the imprint decouples from delivery, when SPACE meets STATE the flip decouples from footprint and reach, when TIME meets STATE the kindling decouples from erosion. T5 ONE COUPLING DISCIPLINE, THREE TIMES -- every coupling SWEEPS BOTH coupled axes so every sign survives the product grid (anti-tuning: 47 intensity × plasticity rate, 48 intensity × barrier depth, 49 plasticity rate × barrier depth), REVERTS to the frozen engine BIT-FOR-BIT with the drive off (inheriting EACH layer's guard -- E1×E0 the M9 anchor, E1×E2 the E.settle relaxation, E0×E2 BOTH), and reports any decoupling HONESTLY, with NO new measurement or tuned constant in any: same seam discipline, three couplings. Registered as the 28th and FINAL atlas citizen (CROSS-SYNTH), placed LAST in the run order so the three source JSONs are freshly regenerated before their hashes are re-verified. FIREWALL inherited THREEFOLD and absolute: every imprint, leverage, flip threshold, retained trace and coordination gain is a STRUCTURAL quantity, NEVER a felt state, an experienced mood, a level of consciousness, an experienced ease of relapse, a real connectome, a real measure of where a drive leaves a mark, which target is most switchable, or whether any patient's episodes accelerate (Axis-A; consciousness_claim=0; hard problem OPEN); only structural SIGNS and RELATIONS are asserted, every MAGNITUDE is [O]; the [L] correspondences in the source chapters are direction-only; target selection, device programming, prognosis and treatment are external; nothing is a cure, reversal, or prevention; efficacy=0; not medical advice",
        "grade": "[V synth]",
        "meaning": "the capstone of the three cross-axis couplings. The §47 imprint (E1×E0), §48 leverage "
                   "(E1×E2) and §49 kindling (E0×E2) chapters each married TWO of the atlas's three new "
                   "layers -- E0 plasticity (the evolving connectome), E1 spatial localisation (where), E2 "
                   "state switching (the bistable flip). With the third frozen the trio of pairwise "
                   "couplings closes, and this chapter is a META-SYNTHESIS -- NOT a new model -- that steps "
                   "back to certify the single structural statement they jointly make: they are the "
                   "complete set of PAIRWISE EDGES of the three layers, read as one FAMILY with one SHAPE. "
                   "It runs ZERO new measurements, adds ZERO new machinery, derives ZERO new tuned "
                   "constants. Its discipline is the discipline of a synthesis: the three source results "
                   "JSONs are the SSOT, and BEFORE reading a single number it re-computes each one's "
                   "SHA-256 and checks it BIT-FOR-BIT against the frozen value (imprint cdb16230..., "
                   "leverage bd3a9e23..., kindling 3880e63f...); only then are they read; the engine is "
                   "emerged READ-ONLY for the invariant check and confirmed byte-unchanged (0fbf4988...), "
                   "the M0-16 subtree identical. FIVE certifications hold, all CONFIRMED. T1 ONE FAMILY / "
                   "THE COMPLETE E0/E1/E2 TRIANGLE -- all three couple two of the layers and together "
                   "realise all three pairwise edges {E1,E0} {E1,E2} {E0,E2}, every layer-vertex appearing "
                   "in EXACTLY TWO couplings (E0 in 47+49, E1 in 47+48, E2 in 48+49 -- degree two), and "
                   "each reverts to the frozen engine BIT-FOR-BIT with its drive off: one family, three "
                   "edges, one off-state. T2 ONE NEW JOINING OBJECT PER COUPLING -- the imprint readout (a "
                   "focal drive through the plastic connectome), the leverage switch (the bistable cell "
                   "driven by broadcast leverage) and the kindling switch (the bistable cell driven through "
                   "the evolving connectome), each reusing BOTH its layers read-only and adding NO new "
                   "tuned constant (the leverage and the coordination gain are frozen/evolving-kernel "
                   "readouts, not free weights). T3 THREE DECOUPLINGS -- the genuinely-new result each seam "
                   "surfaces is a decoupling, all three CONFIRMED: clean delivery != clean imprint (the "
                   "trace relay strictly contains the field relay, 8 ⊃ 2 -- plasticity delocalises the "
                   "mark), switchability decoupled from both footprint and reach (the reach hub cerebellum "
                   "is among the hardest to flip, rank 10/12), easier-to-flip decoupled from erosion (the "
                   "coordination rises 0.3896→0.3964 as the threshold falls -- consolidation, not "
                   "degradation). T4 A COMMON SHAPE / A SINGLE-AXIS LAW BREAKS -- each decoupling refutes a "
                   "tidy single-axis hypothesis the coupling was the natural place to test, reported "
                   "honestly (no universal focal>diffuse imprint law, no universal reach→switchability law, "
                   "no clean kindling-erodes-coordination story), the same honest-negative shape three "
                   "times: when space meets time the imprint decouples from delivery, when space meets "
                   "state the flip decouples from footprint and reach, when time meets state the kindling "
                   "decouples from erosion. T5 ONE COUPLING DISCIPLINE, THREE TIMES -- every coupling "
                   "sweeps BOTH coupled axes (anti-tuning), reverts to the frozen engine BIT-FOR-BIT with "
                   "the drive off (inheriting each layer's guard -- the M9 anchor, the E.settle "
                   "relaxation, or both), and reports any decoupling honestly, with NO new measurement or "
                   "tuned constant in any: same seam discipline, three couplings. Registered as the 28th "
                   "and FINAL atlas citizen (CROSS-SYNTH), placed LAST in the run order so the three "
                   "source JSONs are freshly regenerated before their hashes are re-verified. The family "
                   "mirrors the earlier §42 E0 triad synthesis, which closed the three READOUTS of one "
                   "plasticity layer; this chapter closes the three COUPLINGS of three layers. FIREWALL "
                   "inherited THREEFOLD and absolute: every imprint, leverage, flip threshold, retained "
                   "trace and coordination gain is a STRUCTURAL quantity, NEVER a felt state, an "
                   "experienced mood, a level of consciousness, an experienced ease of relapse, a real "
                   "connectome, a real measure of where a drive leaves a mark, which target is most "
                   "switchable, or whether any patient's episodes accelerate (Axis-A; consciousness_claim=0; "
                   "hard problem OPEN); only structural signs and relations are asserted, every magnitude "
                   "is [O]; the [L] correspondences in the source chapters are direction-only; target "
                   "selection, device programming, prognosis and treatment are external; nothing is a cure, "
                   "reversal, or prevention; efficacy=0; not medical advice",
        "canonical": "50-cross-axis-synthesis",
        "check": None,
    },
}

# ---------------------------------------------------------------------------
# CITES — which locks each chapter cites (-> one self-contained card each)
# ---------------------------------------------------------------------------
CITES = {
    "01-constitution-scope": ["mediator_discipline"],
    "02-not-a-field": ["mediator_discipline", "field_coherence"],
    "03-organ-emergence": ["commit_order"],
    "04-em-brainwave": ["front_speed_c", "theta_gamma", "field_coherence", "brain_wavelengths"],
    "05-memory-physics": ["theta_gamma", "pattern_completion", "phase_protect"],
    "06-parallel-eddies": ["theta_gamma", "mediator_discipline"],
    "07-selection-loop": ["mediator_discipline"],
    "08-learned-field": ["mediator_discipline"],
    "09-stream-of-thought": ["theta_gamma", "mediator_discipline"],
    "10-felt-loop": ["mediator_discipline"],
    "11-hemispheres-and-ai": ["mediator_discipline"],
    "12-open-problem": ["pci_negative", "hard_problem"],
    "13-em-coordination": ["coord_kappa", "coord_regime", "coord_field_contribution", "coord_efficacy_open"],
    "14-sensory-coupling": ["sens_coupling_kappa", "sens_crossmodal_field", "sens_regime_bounded", "sens_efficacy_open"],
    "15-light-to-memory": ["lm_angle_rectification", "lm_information_contrast", "lm_memory_write", "lm_reader_feels_field", "lm_efficacy_open"],
    "16-what-is-a-thought": ["thought_definition", "commit_order", "front_speed_c", "pattern_completion", "hard_problem"],
    "17-faculties-of-mind": ["thought_definition", "mediator_discipline", "hard_problem"],
    # --- Part II: disorders of the mind (autism / ADHD / theta-cap) ---
    "18-autism-three-axis": ["autism_three_axis", "coord_kappa", "mediator_discipline"],
    "19-autism-chemical-limits": ["autism_chemical_reach", "autism_three_axis"],
    "20-theta-cap-pacemaker": ["theta_cap_pacemaker", "theta_cap_removable", "theta_cap_molecular_safe"],
    "21-theta-cap-operating-principle": ["theta_cap_operating_principle", "theta_cap_feasibility", "theta_cap_removable"],
    "22-adhd-vs-autism": ["adhd_axis_specific", "autism_chemical_reach"],
    "23-virtual-trial": ["virtual_trial", "theta_cap_operating_principle"],
    "24-schizophrenia-mirror": ["schizophrenia_mirror", "schizophrenia_symptom_domains"],
    "25-epilepsy-oversync": ["epilepsy_oversync", "schizophrenia_mirror"],
    "26-plasticity-consolidation": ["plasticity_consolidation", "epilepsy_oversync"],
    "27-depression-chronification": ["depression_chronification", "plasticity_consolidation"],
    "28-state-switching": ["state_switching", "epilepsy_oversync"],
    "29-bipolar-state-switching": ["bipolar_state_switching", "state_switching"],
    "30-bipolar-threshold-levers": ["bipolar_threshold_levers", "bipolar_state_switching"],
    "31-epilepsy-threshold-levers": ["epilepsy_threshold_levers", "epilepsy_oversync"],
    "32-depression-threshold-levers": ["depression_threshold_levers", "depression_chronification"],
    "33-schizophrenia-threshold-levers": ["schizophrenia_threshold_levers", "schizophrenia_symptom_domains"],
    "34-autism-threshold-levers": ["autism_threshold_levers", "autism_three_axis", "autism_chemical_reach"],
    "35-adhd-threshold-levers": ["adhd_threshold_levers", "adhd_axis_specific", "autism_threshold_levers"],
    "36-addiction-threshold-levers": ["addiction_threshold_levers", "state_switching", "adhd_threshold_levers"],
    "37-addiction-sensitization-dynamics": ["addiction_sensitization_dynamics", "addiction_threshold_levers", "plasticity_consolidation"],
    "38-alzheimers-threshold-levers": ["alzheimers_threshold_levers", "addiction_threshold_levers", "plasticity_consolidation"],
    "39-alzheimers-progression-dynamics": ["alzheimers_progression_dynamics", "alzheimers_threshold_levers", "plasticity_consolidation"],
    "40-ocd-threshold-levers": ["ocd_threshold_levers", "addiction_threshold_levers", "alzheimers_threshold_levers"],
    "41-ocd-stabilisation-dynamics": ["ocd_stabilisation_dynamics", "ocd_threshold_levers", "plasticity_consolidation"],
    "42-e0-triad-synthesis": ["e0_triad_synthesis", "addiction_sensitization_dynamics", "alzheimers_progression_dynamics", "ocd_stabilisation_dynamics"],
    "43-spatial-localisation": ["e1_spatial_localisation", "coord_kappa", "plasticity_consolidation"],
    "44-focal-epilepsy-spread": ["focal_epilepsy_spread", "e1_spatial_localisation", "epilepsy_oversync"],
    "45-lesion-field-diaschisis": ["lesion_field_diaschisis", "e1_spatial_localisation", "focal_epilepsy_spread"],
    "46-targeted-neuromodulation-offtarget": ["targeted_neuromodulation_offtarget", "e1_spatial_localisation", "focal_epilepsy_spread", "lesion_field_diaschisis"],
    "47-spatial-plasticity-imprint": ["spatial_plasticity_imprint", "e1_spatial_localisation", "plasticity_consolidation", "targeted_neuromodulation_offtarget"],
    "48-spatial-switch-leverage": ["spatial_switch_leverage", "e1_spatial_localisation", "state_switching", "targeted_neuromodulation_offtarget"],
    "49-kindling": ["e0e2_kindling", "plasticity_consolidation", "state_switching", "bipolar_state_switching"],
    "50-cross-axis-synthesis": ["cross_axis_coupling_synthesis", "spatial_plasticity_imprint", "spatial_switch_leverage", "e0e2_kindling"],
}

# ---------------------------------------------------------------------------
# ANSWERS — answer-first direct answer per chapter (40-60 words; faithful to the body)
# ---------------------------------------------------------------------------
ANSWERS = {
    "01-constitution-scope":
        "Felt Cognition reads the stream of thought as a functional process built on the verified "
        "neuro chain, under one discipline: every claim names a physical mediator — ion spikes and "
        "synaptic currents — nothing is asserted without being emerged, the dependency on neuro is "
        "one-way, and the hard problem of experience is held open, not solved.",
    "02-not-a-field":
        "The EM-field-as-binding-medium is retired only in its quantum and radiative optical-fibre "
        "forms; what replaces it is a named mechanism — ion spikes and synaptic currents gated by "
        "classified low-frequency phase (communication-through-coherence). Because the classical "
        "near-field is coherent across the brain, its functional role is reopened as open, not denied.",
    "03-organ-emergence":
        "Brain organs are emerged from 4D-DNA, not assumed: each master gene sets a measured bistable "
        "gamma, and an ascending fold-threshold predicts the commit order hypothalamus < cerebellum < "
        "cerebrum < hippocampus [verified]. The substrate is emerged under drive; absolute organ size "
        "and neuron count remain open.",
    "04-em-brainwave":
        "The EM brainwave is emerged, not posited: excitatory and inhibitory populations make a "
        "theta–gamma local field that radiates through the wave equation, and the emitted front travels "
        "at the wave speed c [verified]. Across a brain-sized transect the classical field is coherent "
        "(≈0.998); whether it is the computational medium stays open.",
    "05-memory-physics":
        "Memory is a physical attractor: a Hebbian write deepens an engram-cell bistable well, a stored "
        "pattern completes from a 10% cue, and a theta-phase clock — writing and reading on opposite "
        "phases — measurably protects old memory [verified]. This timing drives the brainwave; absolute "
        "capacity in patterns and milliseconds remains open.",
    "06-parallel-eddies":
        "A thought begins as many parallel ionic eddies igniting in gamma, winner-take-most, with gamma "
        "setting ignitability [model]. The mediator is a local ionic gamma-assembly — spikes and synaptic "
        "currents — not a physical field. Absolute size and any link to consciousness remain open.",
    "07-selection-loop":
        "Selection is a closed loop: many eddies are laid down and one is selected through a "
        "field → race → carried → selection cycle [model]. The mediator is basal-ganglia selection acting "
        "on ionic assemblies, cited from the neuro chain, not a field. Absolute timing in milliseconds "
        "and dopamine levels remain open.",
    "08-learned-field":
        "The laid-down field is learned: selection drives a dopamine reward-prediction error that updates "
        "which eddies appear next [model], with gamma read-only. The mediator is the dopamine value signal, "
        "cited from neuro; recruitment and reversal behave directionally as predicted. The absolute "
        "learning rate remains open.",
    "09-stream-of-thought":
        "The stream of thought is serial selection among parallel gamma-eddies, with conflict detection, "
        "memory feedback, and global gamma binding within a theta frame [model]. The 'large field' is "
        "theta–gamma phase-coherence (communication-through-coherence), not a physical field. The wired "
        "mechanisms pass directionally; absolute hertz and units remain open.",
    "10-felt-loop":
        "The embodied feeling loop folds body and brain into one real-time process: interoceptive and "
        "autonomic signals enter the eddy loop, gated by ionic phase, not a field [model]. Felt cognition "
        "is proposed as this integrated, real-time eddy process stimulating memory cells; whether it is "
        "experience — the felt quality — stays open.",
    "11-hemispheres-and-ai":
        "Hemispheric asymmetry is graded, and a system can compute the stream of thought yet not feel it — "
        "an architectural hypothesis, not a proof about machine consciousness [model]. Cerebral sensing "
        "logic treats the outside as felt by sensory cells and thought by cerebral cells, on the same "
        "selection and binding over internal eddies.",
    "12-open-problem":
        "The open problem of experience is held open, not solved: the model specifies function — the "
        "stream of thought — but not its subjective character, the quale. The consciousness access marker "
        "(perturbational complexity, PCI) is an honest negative; it did not robustly reproduce. No link in "
        "the paper is claimed to be causal.",
    "13-em-coordination":
        "At the brain's measured ephaptic coupling — the local field sitting at its entrainment "
        "threshold — twelve central organs settle into partial, metastable coordination, neither "
        "drifting free nor seizing into global lock. Cancelling the field in silico drops global order "
        "measurably; the near-field opens communication windows and carries theta–gamma coupling "
        "[verified mechanism]. Whether cognition uses it stays open.",
    "14-sensory-coupling":
        "At the same measured ephaptic coupling, eight sensory streams couple to their central relays, "
        "carrying γ cited verbatim from the neuro chain. The central substrate is unchanged; sensory "
        "drive loads onto it without seizing. Cross-relay senses organise only through the shared field "
        "(cancel < measured < augment); co-relay senses stay locked regardless. Whether cognition uses "
        "this is open.",
    "15-light-to-memory":
        "On the same vacuum lattice a brainwave is emerged light; brainwave and sensory EM superpose, and "
        "geometric angle rectification (α = 2/π, δ = 1/π²) turns their signed phase overlap into a "
        "sign-surviving information bit. Bound input clears the engram fold and writes a persisting memory; "
        "a downstream neuron feels the rolled field. Whether biology uses this is open.",
    "16-what-is-a-thought":
        "A thought is defined as a union of faculties, not an abstract umbrella. It is serial selection "
        "among parallel ionic gamma-eddies, bound within a theta frame, running on a substrate emerged "
        "from 4D-DNA: organs, brainwave and memory generated, not assumed. The definition is closed on the "
        "mechanism axis; whether any of it is felt stays open.",
    "17-faculties-of-mind":
        "Thought decomposes into fourteen faculties: perception, attention, the serial stream, memory, "
        "learning, the affect mechanism, arousal and sleep, dreaming, large-scale binding, and pathology "
        "are built and reproducible (F1-F10 closed); language, volition, social cognition and metacognition "
        "are honestly owed with named external inputs (F11-F14 owed). The partition is checked against a "
        "standard taxonomy, not chosen to look complete.",

    # --- Part II: disorders of the mind ---
    "18-autism-three-axis":
        "Autism is modeled not as one lesion but as three separable faults on the emerged cerebrum: a "
        "threshold E-I fault, an output gain fault, and a long-range wiring fault. Each leaves a distinct, "
        "reproducible fingerprint in synchrony, theta-gamma coupling and ignition; which fault an "
        "individual's autism is stays open. efficacy=0; not medical advice.",
    "19-autism-chemical-limits":
        "A scalar threshold-lowering gain chemical, the mechanism of the catecholaminergic stimulant class, "
        "fully reverses autism's threshold fault, partly helps the output fault, and only masks the wiring "
        "fault by over-synchronisation, because scalar gain cannot re-route geometry. This is why a "
        "stimulant relieves some presentations and not others. efficacy=0; no drug-treats-autism claim is "
        "made.",
    "20-theta-cap-pacemaker":
        "A wearable theta carrier is the only handle on the wiring axis no chemical reaches, but only as an "
        "external pacemaker: it forces long-range coordination inside a narrow window, the benign extra-lane "
        "reading is refuted, it is cleanly removable with no dependence, and it is molecularly safe below "
        "the spinodal fold. efficacy=0.",
    "21-theta-cap-operating-principle":
        "If a theta-cap is to supply the wiring-axis function at all, the dynamics force one mode: "
        "minimum-effective amplitude, matched to the individual wiring deficit, applied continuously, since "
        "nothing is banked. Physically every component (theta-tACS, closed-loop phase-locking, "
        "multi-electrode long-range montages) exists, but the assembly does not, and feasibility is not "
        "benefit. efficacy=0.",
    "22-adhd-vs-autism":
        "An explicit gene-grounded ADHD substrate (gain and arousal axes, intact wiring) restores to health "
        "under a stimulant where the same stimulant only partly reaches autism; the theta-cap is redundant "
        "for ADHD but essential for autism's wiring, and on an AuDHD substrate the two compose. The ADHD "
        "model's validity is open. efficacy=0.",
    "23-virtual-trial":
        "Across a synthetic population of eighty emerged cerebra, stimulant responders are gain-dominated "
        "and non-responders are wiring-dominated and partly cap-rescuable. An honest refutation shows the "
        "cap-unrescued residual is a dose-cap and stiffness limit, not a severe-wiring tail, arguing for "
        "amplitude matched to the deficit. Every fraction is an in-silico coupling state. efficacy=0.",
    "24-schizophrenia-mirror":
        "Schizophrenia is the over-ignition mirror of autism-T on the same R19 ignitability axis: a "
        "disinhibitory bias lowers the fold so irrelevant assemblies ignite (aberrant salience). Its positive, "
        "negative and cognitive symptoms sit on the threshold, output and wiring axes; a gain-reducing "
        "antipsychotic reverses the positive domain only, which is why dopamine blockade spares the rest. efficacy=0.",
    "25-epilepsy-oversync":
        "Epilepsy is the over-synchronisation pole of the engine's synchrony axis: an excitatory bias drives "
        "the order parameter to the over-sync ceiling and the selective gate collapses, so every assembly "
        "ignites — the ictal state. An inhibitory anticonvulsant-class push reverses it and raises the seizure "
        "threshold. The ictal time-course is owed to a state-switching layer. efficacy=0.",
    "26-plasticity-consolidation":
        "The plasticity layer the structural atlas never had: a phase-correlation Hebbian update of the ephaptic "
        "kernel makes consolidation and after-effects representable, resolves the open continuous-versus-periodic "
        "dosing question (spaced leaves a larger retained trace, so the cap repairs and pacing beats holding), and "
        "builds the reversible-to-chronified switch later mood disorders need. With plasticity off it reproduces "
        "the frozen engine bit-for-bit. efficacy=0.",
    "27-depression-chronification":
        "Depression is read as the chronification of a low-coordination operating point. A sustained HPA-driven "
        "withdrawal lowers coordination below health (acute, reversible); under the plasticity layer the excursion "
        "writes a retained structural trace that does not revert — the reversible-to-chronified switch. "
        "Antidepressant delayed onset is a consolidation timescale; treatment resistance is the trace's depth. "
        "efficacy=0; not medical advice.",
    "28-state-switching":
        "The state-switching layer is the R19 bistable cell read over time, with no new machinery. Sweeping the "
        "field gives hysteresis — a state resists switching back; the transition latency diverges at the fold, "
        "which closes the epilepsy chapter's owed ictal time-course; and the barrier sets the switching threshold. "
        "Constant drive reproduces the engine bit-for-bit. efficacy=0.",
    "29-bipolar-state-switching":
        "Bipolar disorder is read as two operating poles on one valence axis: mania sits above the healthy operating "
        "point, depression below. An episode is a bistable switch that persists past its trigger; kindling is the "
        "plasticity trace accumulating across episodes, so each switch gets easier; and a mood stabiliser is "
        "barrier-raising. efficacy=0; not medical advice.",
    "30-bipolar-threshold-levers":
        "The previous chapter's mood-stabiliser barrier-raise is decomposed into a DNA-grounded three-lever target "
        "map: reduce the inward excitatory current (L1), increase the outward potassium current (L2), or remove the "
        "upstream circadian and HPA drive (L3). Sixteen bipolar genes are placed by their own promoter switch "
        "stiffness. Targets are ranked, never drugs or doses; efficacy=0; not medical advice.",
    "31-epilepsy-threshold-levers":
        "The previous chapter's over-synchronisation threshold-raise is decomposed into a DNA-grounded three-lever "
        "target map: reduce the inward excitatory current (L1), increase the outward potassium current (L2, the "
        "dominant M-current axis), or remove the upstream mTOR drive (L3). Sixteen epilepsy genes are placed by "
        "their own promoter switch stiffness. Targets are ranked, never drugs or doses; efficacy=0; not medical advice.",
    "32-depression-threshold-levers":
        "The previous chapter's operating-point restoration is decomposed into a DNA-grounded three-lever target "
        "map: modulate inward glutamatergic current (L1), increase outward potassium current (L2), or remove the "
        "upstream HPA drive and restore the deficient monoamine and neurotrophic drives (L3, dominant here). "
        "Eighteen depression genes are placed by their promoter switch stiffness; targets are ranked, never drugs "
        "or doses; not medical advice.",
    "33-schizophrenia-threshold-levers":
        "Chapter 24's over-ignition correction is decomposed into a DNA-grounded three-lever target map: modulate "
        "inward glutamatergic/NMDA current (L1) and remove the up-stream dopamine drive (L3), co-dominantly, with "
        "the outward GABA-A lever (L2) minor, over fourteen schizophrenia genes placed by their promoter switch "
        "stiffness. The first L1+L3 co-dominant and first domain-restricted case (positive domain only); targets "
        "ranked, never drugs; not medical advice.",
    "34-autism-threshold-levers":
        "Chapters 18-19's E/I over-excitation correction is decomposed into a DNA-grounded three-lever target map: "
        "reduce inward excitatory current (L1, dominant), increase outward K+/restore GABA-A inhibition (L2), with "
        "a sparse serotonergic lever (L3), over ten autism genes. The map reaches the excitability axis only; the "
        "named output and wiring axes stay out of reach; targets ranked, never drugs; not medical advice.",
    "35-adhd-threshold-levers":
        "Chapter 22's gain/arousal ADHD substrate (intact wiring) maps onto the threshold frame and loads entirely "
        "on the up-stream drive lever (L3): five drive-tone genes, with both ionic-current levers empty. It is the "
        "first partial fit -- the dominant gain-amplitude core is named but out of reach, the wiring axis absent. "
        "Targets ranked, never drugs; not medical advice.",
    "36-addiction-threshold-levers":
        "Addiction's incentive-sensitisation substrate maps onto the threshold frame, loading most on the reward "
        "drive (L3, five genes) but engaging the glutamate (L1) and inhibitory (L2) levers too. It is the second "
        "partial fit: the dominant fault, a consolidated learned sensitisation gain, is named but out of reach. "
        "Targets ranked, never drugs; addiction is a treatable medical condition.",
    "37-addiction-sensitization-dynamics":
        "The integrated sensitisation gain chapter 36 named out of reach is modelled here directly on the "
        "plasticity layer. Repeated reward exposure builds a retained trace, the sensitised circuit reacts more "
        "to cues, extinction does not erase it, and intermittent exposure sensitises more -- so the two "
        "convergence halves meet. Addiction is a treatable medical condition.",
    "38-alzheimers-threshold-levers":
        "Alzheimer's maps onto the threshold frame as the third and deepest partial fit. The reachable "
        "surface is purely symptomatic with a split sign: cholinergic drive restored, glutamate "
        "excitotoxicity reduced, inhibition restored. The dominant neurodegenerative-progression axis is an "
        "irreversible decay, named but out of reach. Symptomatic levers do not slow progression; a person "
        "with dementia remains a person.",
    "39-alzheimers-progression-dynamics":
        "The neurodegenerative-progression axis chapter 38 named out of reach is modelled here directly on "
        "the plasticity layer, as the structural inverse of addiction's gain. Progression accumulates "
        "irreversible structural loss, the degenerated circuit responds less, symptomatic levers relieve "
        "without rebuilding, and the only handle lives on the decay rate -- disease modification. A person "
        "with dementia remains a person.",
    "40-ocd-threshold-levers":
        "OCD is the fourth partial fit. The reachable surface is the instantaneous CSTC excitability, where "
        "the mainstay routes genuinely but partially help. The dominant loop-lock is a pathological "
        "stabilisation, out of reach. The levers do not unstick the loop; intrusive thoughts are a symptom, "
        "not a moral failing.",
    "41-ocd-stabilisation-dynamics":
        "The stuck loop chapter 40 named out of reach is modelled here as the third E0 mode -- stabilisation, "
        "after addiction's gain and Alzheimer's decay. Consolidation writes a self-sustaining loop that holds "
        "itself at rest; the symptomatic levers do not unstick it, the handle lives only on the consolidation "
        "axis. An intrusive thought is a symptom, not a moral failing.",
    "42-e0-triad-synthesis":
        "Three chapters built one thing. Addiction's gain, Alzheimer's decay and OCD's stabilisation are certified "
        "here as three readouts of one plasticity layer -- one shared off-state anchor, three directions of mass, "
        "three readouts, the gain and stabilisation traces literally identical, the same seam and one handle on the "
        "plasticity axis. Zero new measurement; these are structural quantities, never felt experience.",
    "43-spatial-localisation":
        "Every disorder so far drove the brain globally. Generalising the scalar coupling to a per-node spatial "
        "drive makes focal-versus-diffuse representable: the field is local and normalised, perturbation reach is "
        "heterogeneous with a drive-stable cerebellar hub, and each node's self-localising-or-relay class is "
        "drive-invariant. No universal focal-beats-diffuse law holds, so disease here is region-specific. "
        "Structural quantities, never felt experience.",
    "44-focal-epilepsy-spread":
        "Chapter 43's spatial map gets its first application. Driving each region as a focal seizure focus, the "
        "foci partition into contained (the seizure stays focal) and broadcast (it secondarily generalises), and "
        "this partition is fixed by focus location, not ictal intensity. But broadcast is not the same as global "
        "hypersynchrony — two decoupled axes. Structural quantities, never felt experience.",
    "45-lesion-field-diaschisis":
        "Chapter 44's spatial map gets its destructive dual. Silencing each region as a focal lesion, the lesions "
        "partition into local-deficit (the dysfunction stays local) and remote-diaschisis (it disrupts distant "
        "circuits more than the lesion itself), fixed by lesion location, not severity. But diaschisis is not the "
        "same as global disruption — two decoupled axes. Structural quantities, never felt experience.",
    "46-targeted-neuromodulation-offtarget":
        "Chapter 44's excitatory drive, re-read as therapy, closing the trilogy. Aiming a focal stimulation at "
        "each region, targets split into clean-delivery and off-target-leak, fixed by target location, not "
        "intensity. The spatial numbers coincide with chapter 44; what is new: clean delivery and global reach "
        "are decoupled, the cleanest target is the strongest. Structural quantities, never felt effect.",
    "47-spatial-plasticity-imprint":
        "The first cross-axis coupling: where a focal drive leaves a lasting synaptic trace. Marrying the "
        "spatial layer to plasticity, targets split into local-imprint and relayed-imprint, fixed by location "
        "across intensity and rate. The new result: clean delivery does not imply clean imprint — plasticity "
        "delocalises it. Relayed imprint is the structural default. Structural quantities, never felt effect.",
    "48-spatial-switch-leverage":
        "The second cross-axis coupling, the spatial sibling of the bipolar episode: which focal drive most "
        "easily flips the collective state. Driving the bistable cell with each region's frozen-kernel broadcast "
        "leverage, the flip-threshold rank equals the leverage rank, barrier-invariant. The new result: "
        "switchability decouples from both instantaneous footprint and reach — the reach hub is among the "
        "hardest to flip.",
    "49-kindling":
        "The third cross-axis coupling, closing the trace-to-threshold link the bipolar episode left open: do "
        "repeated state-flips become easier? Driving the bistable cell through the evolving plastic connectome, "
        "repeated flips deepen the trace and lower the flip threshold (kindling), barrier-invariant. The honest "
        "finding: kindling is consolidative, not degradative — coordination rises, it does not erode.",
    "50-cross-axis-synthesis":
        "The capstone of the three cross-axis couplings, certified as one family: the spatial-plasticity imprint, "
        "the spatial switch leverage and the kindling coupling are the three pairwise edges of the same three "
        "layers. Each marries two and decouples a single-axis law — delivery from imprint, switchability from "
        "reach, easier-flip from erosion. Zero new measurement; structural signs only.",
}

CHAPTERS = list(ANSWERS.keys())
BOTS = ["Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "PerplexityBot", "ClaudeBot", "Google-Extended"]


def _get(results, path):
    cur = results
    for part in path.split("/"):
        cur = cur[part]
    return cur


def validate():
    """Cross-check every LOCK value against the frozen engine results (drift 0)."""
    results = json.load(open(RESULTS, encoding="utf-8"))
    problems = []
    for lid, lk in LOCKS.items():
        chk = lk.get("check")
        if not chk:
            continue
        path, expect = chk
        try:
            got = _get(results, path)
        except Exception as e:
            problems.append(f"{lid}: results path {path} missing ({e})"); continue
        if isinstance(expect, str):
            if str(got) != expect:
                problems.append(f"{lid}: {path} = {got!r} != {expect!r}")
        else:
            if abs(float(got) - float(expect)) > 1e-6 * max(1.0, abs(float(expect))):
                problems.append(f"{lid}: {path} = {got} != {expect}")
    # answer/cite coverage
    for slug in CHAPTERS:
        if slug not in CITES:
            problems.append(f"{slug}: no CITES entry")
        for lid in CITES.get(slug, []):
            if lid not in LOCKS:
                problems.append(f"{slug}: cites unknown lock {lid}")
        words = len(ANSWERS[slug].split())
        if not (38 <= words <= 62):
            problems.append(f"{slug}: answer {words} words (need ~40-60)")
    return problems


if __name__ == "__main__":
    probs = validate()
    if probs:
        print("VALIDATION PROBLEMS:")
        for p in probs:
            print("  -", p)
        raise SystemExit(1)
    print(f"registry OK: {len(LOCKS)} locks, {len(CHAPTERS)} chapters, values match frozen results")
