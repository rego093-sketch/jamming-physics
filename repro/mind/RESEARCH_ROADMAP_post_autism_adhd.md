# Research roadmap — after autism + ADHD

**Program:** VP `mind` / Felt-Cognition disease line (D-series → VC → beyond)
**Frame:** what to build *after* the autism+ADHD consolidation, chosen so the output can **actually help people** while being **worth the effort**. Same discipline throughout: physics-derived, gene-grounded, LOCK→Derive→Gate, **no-tuning**, SEED=19, 2×sha256, READ-ONLY engine (tree `0fbf4988…`), pre-registered sign-only predictions, honest grading ([V]/[L]/[O]), **efficacy = 0**, NOT medical advice.
**Effort tags per target:** **[reuse]** = the autism engine does it with axis re-weighting + a new gene set (low marginal effort); **[new]** = needs a new machinery layer (high effort, built once, reused after).

---

## 0. The thesis — what the whole program is actually *for*

The genuinely useful, humanity-scale deliverable is **not a cure** (efficacy = 0). It is a **transdiagnostic mechanistic fault-axis atlas**: a way to re-cut psychiatric/neurological conditions by **mechanism** (the T / O / W axes, plus the temporal axes below) instead of by symptom checklist, and to **locate each condition — and each patient — by its fault signature.**

Why this is the right target, and not "simulate disease X to show we can":

- The global burden of mental disorders **has not fallen since 1990 despite effective interventions existing** (GBD 2021). The bottleneck is therefore not the *absence* of tools — it is **matching the right patient to the right tool.** Diagnosis is symptom-based; treatment is largely **trial-and-error** (e.g. treatment-resistant depression runs at roughly a third of cases — McIntyre et al. 2023).
- This framework's *demonstrated* move is exactly a **mechanistic discriminant** that tells apart fault subtypes that look alike (the autism T/O/W discriminant) and that **rules an intervention in or out by axis** (the θ-cap = W-only finding: stimulant→gain, cap→wiring, no chemical reaches W).

So the atlas produces three things that map onto real unmet need: **(1) stratification** (separate look-alike biotypes), **(2) intervention-axis matching** (which modality can touch which fault), and **(3) mechanistic ruling-out** (retire approaches that *cannot* work on a given axis, saving wasted trials and wasted patient-years). Autism + ADHD already proved the method on two conditions sharing the O/T axes and diverging on W. Everything below extends the same atlas.

## 1. The success criterion (so the effort is not wasted)

A target "actually helps" only if its module ends in one of:
- a **pre-registered, reproducible discriminant** whose axis-assignment **predicts differential intervention response** — i.e. it would change *which patient gets which modality*; or
- a **mechanistic null** that **retires a wasted approach** on a given fault axis (a refutation is a finding).

The framework supplies the **hypothesis and the stratification, gated for reproducibility**; clinical validation is external and **required before any human benefit**. Anything that cannot reach one of those two endpoints is research for its own sake and is deprioritised below.

## 2. Phase 0 — the foundational layers (the "temporal core" autism never exercised)

Autism built the **structural** engine (the three static axes + PAC + over-sync boundary + routing). It did **not** exercise **time**: learning, accumulation, switching. Several of the highest-payoff targets are *defined* by time and would come out **hollow** without these. Build once, reuse everywhere.

- **E0 — Plasticity / consolidation layer.** **[new]** An STDP-like slow, activity-dependent update of the connectivity `W` on top of the READ-ONLY engine. *Unlocks:* disease **progression**, **learning/memory** deficits, stimulation **after-effects**, **addiction** sensitisation, depression **chronification** — and it answers the open device question (continuous vs. periodic dosing). **Single highest-leverage investment in the whole roadmap.** Phase of the θ-cap operating-principle [O] resolves here.
- **E1 — Spatial localisation + field-shaping.** **[new]** Make the fault **regional** (some regions/edges broken, others healthy) instead of global, and give the drive a spatial profile. *Unlocks:* focal-vs-diffuse stimulation, off-target over-sync, region-specific disease, and a realistic device model (the targeting question we could not even pose while the fault was global).
- **E2 — Dynamic state-switching.** **[new]** Use the R19 bistable switch (`g·s − s³ + h`) **over time** — transitions *between* attractors, not a single faulted basin. *Unlocks:* every **episodic** disorder (mood-state switching, seizure onset, panic).

### 2.5 The intervention layer — threshold-shift logic (cross-cutting) **[inherited, v1.37]**

> The layers above (E0/E1/E2) describe how a fault *forms and moves*. This layer describes how an intervention *reaches* it — and unlike the others it is **not built here**: it is inherited wholesale from the **analgesic reproducibility package** (Zenodo **10.5281/zenodo.20733420**) and registered as a **cross-cutting reusable layer** by `THRESHOLD_LOGIC_INHERITANCE.md`.

- **The frame.** A symptom is a **firing-threshold crossing**; an intervention is a **controlled upward shift** of that threshold. A threshold is set by a current balance, so there are exactly **three levers**: **L1** reduce inward (excitatory) current · **L2** increase outward (K⁺) current · **L3** remove the up-stream sensitising drive. It runs on the **same R19 substrate** the whole atlas rests on (`spinodal` fold = the switching barrier), so it attaches to **any** disorder module with **no new mechanism and no new tuned constant**.
- **DNA grounding.** Each candidate gene is placed by reading its **own promoter switch stiffness** — `γ = −mean` NN stacking ΔG (SantaLucia 1998) over its promoter window → `|h_sp| = spinodal(γ)`, engine **READ-ONLY** — the identical pipeline the analgesic package ran on the Na_V channels.
- **Fail-closed discipline (inherited).** An **L3-honesty gate** (every L3 link graded `[O]` cited biology, never derived), a **forbidden-claim scanner** (no dose/efficacy/safety/synthesis; self-test must fire), and a **burden-weighted prioritisation** that ranks **targets, never drugs or doses** (γ carried as context, **never** folded into the score). **Firewall:** promoter `|h_sp|` ≠ the network barrier `g` ≠ a channel voltage / potency / dose / clinical effect.
- **Applied (v1.37):** **T2b-L bipolar** (§30, module `bipolar_threshold_levers.py`, registered as the 8th atlas citizen `BIP-T2b-L`) — it **decomposes** the abstract mood-stabiliser barrier-raise of §29's B4 into a three-lever map over 16 bipolar excitability genes.
- **Applied (v1.38):** **T2a-L epilepsy** (§31, module `epilepsy_threshold_levers.py`, registered as the 9th atlas citizen `EPI-T2a-L`) — it **decomposes** §25's abstract over-sync-threshold-raise into a three-lever map over 16 epilepsy excitability genes, **L2-dominant** (KCNQ2/KCNQ3 M-current = the retigabine axis). Five γ reads (KCNQ2/KCNQ3/KCNB1/SCN2A/GRIN2A) reuse the bipolar cache verbatim. Two honest caveats recorded: KCNT1 sign-inverted, SCN1A Na-block contraindicated in Dravet — hence γ is [V] for promoter structure only, clinical direction [O].
- **Applied (v1.39):** **T1b-L depression** (§32, module `depression_threshold_levers.py`, registered as the 10th atlas citizen `DEP-T1b-L`) — it **decomposes** §27's abstract operating-point restoration into a three-lever map over 18 depression genes, and is the **first L3-dominant case** (12 of 18 on L3): HPA-removal (NR3C1/CRHR1/FKBP5), monoamine-restoration (SLC6A4/SLC6A2/MAOA/TPH2/HTR1A/HTR2A/COMT), and neurotrophic-restoration (BDNF/NTRK2, the convergence point). Seven γ reads (NR3C1/CRHR1/GRIN2A/CACNA1C/KCNQ2/KCNQ3 from the bipolar cache, GABRA1 from the epilepsy cache) reuse caches verbatim. The disorder-level **sign is flipped** (restore deficient, not reduce excess), stated openly. Two honest caveats recorded: the L1 glutamatergic direction is an NMDA antagonist (ketamine) acting via downstream BDNF — not excitation reduction (sign-subtle) — and HTR2A is non-monotone — hence γ is [V] for promoter structure only, clinical direction [O].
- **Planned for existing modules** (`THRESHOLD_LOGIC_INHERITANCE.md` §3): ✅ §25 epilepsy **DONE (v1.38)**; ✅ §27 depression **DONE (v1.39)**; **next — §24 schizophrenia (L1+L3 on the T-axis, domain-aware)**, §18–19 autism (unifies the existing multilever module under L1/L2/L3), §22 ADHD (L3/arousal, partial fit). The bipolar/epilepsy/depression gene sets **share genes** with these (SCN2A, GRIN2A, GRIN2B, KCNQ2/3, CACNA1C, NR3C1, CRHR1) — consistent with cross-disorder GWAS — so the γ cache is reusable across the atlas.


## 3. The prioritised targets

Ordered by **(fit to the framework) × (humanity payoff) × (effort leverage)**. Fit-grade in brackets.

### Tier 1 — do first

**T1a · Schizophrenia — the T/O/W⁺ discriminant.** **[reuse]** · fit **[V]**
The single most glaring omission and the cleanest application of the autism engine. Schizophrenia is the textbook convergence of **E-I imbalance** (NMDA hypofunction, parvalbumin/GABA interneuron deficit → **T**), **γ / PAC abnormality** (the engine's grounded observable), **dysconnectivity** (the disconnection hypothesis → **W**), and **dopamine** (→ **O**) — it maps onto **all three axes** the autism discriminant already separates, often *better* than autism. ~1% lifelong prevalence, a leading cause of global disability, high suicide and mortality. **Deliverable:** stratify the positive / negative / cognitive symptom domains by dominant axis-fault → a mechanistic account of *why dopamine blockade relieves positive symptoms but not negative/cognitive ones*, and which axis each non-responder is stuck on. **Why first:** lowest marginal effort (engine is built), high payoff, and it **proves the method generalises beyond autism** — the credibility keystone for the whole atlas.

**T1b · Depression biotypes, including treatment-resistant depression.** **[new]** (needs E0 + HPA) · fit **[L→V]**
The **largest single prize**: depressive disorders are the **2nd-highest cause of years-lived-with-disability worldwide**, rising, and treatment is **trial-and-error** with ~⅓ treatment-resistant. This is *exactly* the problem a mechanistic discriminant exists to solve. Fit spans **O** (monoamine gain), **T** (E-I), **W** (frontolimbic connectivity), plus **HPA / arousal** (the M17–M20 modules already in `mind`) and **chronification** (needs E0 plasticity). **Deliverable:** a biotype map that predicts **SSRI vs. NMDA/ketamine-type vs. TMS vs. behavioural** responders from the fault signature — turning weeks-to-months of sequential trial-and-error into an axis-matched first choice. **Highest humanity payoff; do it right after E0.**

### Tier 2 — high fit or high prevention value

**T2a · Epilepsy.** **[reuse]** (+ E2 for onset) · fit **[V]**
The most **direct dynamical fit of any condition**: hypersynchrony (R above the over-sync threshold) is *already* the framework's failure mode — it has been used as the seizure analogue throughout VC but **never made a primary module**. **Deliverable:** seizure susceptibility as a function of E-I state; which interventions raise the over-sync threshold and by how much; the ictal transition via E2. **Very low effort, real impact** — a natural early validation that can run alongside T1a.

**T2b · Bipolar disorder.** **[new]** (needs E2 + E0) · fit **[V]**
The R19 bistable switch is *literally* a two-attractor (manic ↔ depressive) system — tailor-made for **state-switching**, which is bipolar's defining feature. Adds HPA / circadian / sleep (episode triggers) and episode **accumulation** (E0). And because `mind` is a *Felt-Cognition* framework, it can speak to the **felt** quality of mood states, not just their oscillatory signature — a distinctive angle. **Deliverable:** characterise / predict episode transitions and the conditions that gate them (high suicide-prevention value).

### Tier 3 — strong fit, after the above

- **T3a · Addiction / substance use.** **[new]** (needs E0 reward + sensitisation) · fit **[L]** — enormous societal cost (esp. opioids); reward-circuit sensitisation is a plasticity phenomenon, so it follows E0.
- **T3b · Alzheimer's / dementia.** **[new]** (needs E0 progression) · fit **[L]** — γ entrainment (the real-world 40 Hz momentum) plus the existing DGENE gene atlas; the payoff is in modelling *progression*, which needs E0.
- **T3c · OCD.** **[reuse/new]** (needs E1 + E2) · fit **[L]** — cortico-striatal-thalamic loop as a pathological limit-cycle / "stuck" attractor; the engine has the striatal regions.

## 4. Honest exclusions — what *not* to force

The framework models conditions whose pathophysiology **is dynamical** (oscillation, E-I, connectivity, state-switching). It does **not** capture conditions dominated by **content, narrative, specific memory, or social cognition as such** — specific phobias, personality disorders, dissociative disorders, the body-image axis of eating disorders. The framework can render their dynamical substrate but **not their phenomenology**; building them would be **cosmetic**, and that violates the program's own honesty discipline. These stay **[O] / out of current scope** and are named here so the boundary is explicit, not accidental.

## 5. Recommended sequence (effort × payoff)

1. **T1a Schizophrenia discriminant** — cheap, reuses the engine, proves generalisation. *(credibility keystone)*
2. **T2a Epilepsy** — cheap, best dynamical fit, validates the over-sync→disease mapping. *(can run parallel to 1)*
3. **E0 Plasticity layer** — the one foundational investment; unlocks every temporal target *and* the device-feasibility verdict.
4. **T1b Depression / TRD biotypes** — the flagship payoff. *(needs E0)*
5. **T2b Bipolar** — *(needs E2 + E0)*; then **E1**, then **T3a/b/c** as the atlas fills in.

Structural (Tier-1/2 static) modules are mostly **applications** of the autism engine → fast, and they cash in your earlier read that "most are simulatable." The **temporal** prizes (depression chronification, bipolar, addiction) are **not** applications — they need E0/E2 — and that is where the remaining genuine difficulty (and the largest payoff) lives.

## 6. Discipline (unchanged, non-negotiable)

Every module: physics-derived, gene-grounded (NCBI RefSeq, γ from sequence), LOCK→Derive→Gate, **no-tuning**, SEED=19, stdlib+numpy, 2×sha256, four-document SSOT per version, READ-ONLY engine (file `e61083ae…`, tree `0fbf4988…`), pre-registered **sign-only** predictions, **refutations are findings**, **efficacy = 0**, Axis-A firewall, NOT medical advice, no self-deprecating language, honest grading retained. A target enters the build only when it can reach a **§1 endpoint** (a validated discriminant that changes treatment-matching, or a mechanistic null that retires a wasted approach).

---

*Sources for the burden framing: GBD 2021 mental-health analysis (Lancet Psychiatry, 2024) — depressive disorders 2nd-highest cause of YLDs, no global reduction in mental-illness burden since 1990 despite available interventions; schizophrenia among the leading causes of disability (~1% prevalence); treatment-resistant depression ~⅓ of cases (McIntyre et al., World Psychiatry 2023). These motivate the matching/stratification value proposition; they are not efficacy claims for any intervention.*
