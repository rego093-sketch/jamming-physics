# COMPLETION LEDGER — what "100%" means for the Felt-Cognition (mind) package

> **Latest (v1.36, 2026-06-19) — E2: the state-switching layer (§28) + T2b: bipolar disorder (§29).
> A foundational-layer advance (E2, add-only on the READ-ONLY engine) plus its first application (T2b),
> NOT a new-measurement advance.** Per §1 the package advances *scientifically* only by type (1)/(2)/(3);
> v1.36 changes no engine constant, frozen result, or claim. Where E0 gave the atlas a **slow** structural
> variable, **E2 gives the fast one** — a state that switches and stays switched. The key is **no new
> machinery**: the **R19 cell** `ṡ = g·s − s³ + h` (the supercritical pitchfork the whole framework rests
> on) is bistable for g>0; every earlier chapter read it at a single instant, this one reads it **over
> time** — g=1.0 universal scale, fold = the engine's own `spinodal(g)`, all grids swept stimulus probes
> (anti-tuning), no new equation or constant. **E2 (§28), four results:** **(E2.1)** sweeping the field up
> then down, the up/down transitions sit on opposite sides of zero (h=±0.39), a hysteresis loop of width
> `2·spinodal≈0.77` predicted as twice the fold — a state resists switching back; **(E2.2)** the transition
> latency **diverges at the fold** (critical slowing) and falls with overshoot (73.4→1.36), which **closes
> the §25 ictal time-course owed to E2** (closes-25=True); **(E2.3)** the spinodal rises monotonically with
> well depth (0.18→0.64), so the barrier handle is the switching threshold (shallow wells flip, deep wells
> hold; raising the barrier = the stabiliser sign); **(E2.4)** const-drive integration reproduces the
> engine's `settle` bit-for-bit with the fold read from the engine — a pure add-on. **T2b (§29), five
> results** (M17 valence axis: DA approach pole / M18 cortisol withdrawal pole; SAME coupling map as
> SZ/epilepsy/E0, no new constant): **(B1)** an approach bias raises R above health (0.422>0.390), a
> withdrawal bias lowers it below (0.367<0.390), ordering depressive<euthymic<manic monotone — not two
> diseases but two excursions on one axis; **(B2)** an episode is a bistable transition inheriting E2's
> hysteresis and latency, entered at one fold and only left at the other (it persists past its trigger);
> **(B3)** kindling is the E0 trace accumulating across alternating episodes (‖ΔW‖ 0.06→0.33), and a deeper
> trace lowers the barrier so each switch is easier; **(B4)** the mood-stabiliser sign is barrier-raising
> (flip threshold 0.38→0.64), making both manic and depressive switches harder to enter; **(B5)** η=0/no-bias
> reproduces the frozen M9 anchor R=0.38961455156044245 **bit-for-bit**, and the module **imports both
> `BistableSwitch` (E2) and `PlasticConnectome` (E0)** (reuses E2/E0=1.0/1.0) — bipolar is what the two
> layers do together, no third mechanism. **gate.py PASS 134/134** (answer-first 29/29, sitemap 30/30,
> llms.txt 4989B<5KB, SSOT drift 0, body word counts ±2%, build idempotent), registry **40 locks/29
> chapters**, `run_all_atlas.py` **ALL PASS 7/7** (14 CONFIRMED, E2=`47c35e06…`, BIP=`5c55c0e7…`),
> `run_all_d9.py` / `run_all_vc.py` ALL PASS; engine `e61083ae…`, tree `0fbf4988…`, and all six prior frozen
> result shas byte-unchanged. Added: two framing LOCKs (`state_switching`, `bipolar_state_switching`; the
> frozen `epilepsy_oversync` lock is **not** rewritten — the debt is announced by the new lock), their
> reproduce code (2× deterministic each), and the §28 (1111w) + §29 (1229w) canonical chapters.
> **efficacy=0; not medical advice; Axis-A firewall** (a bistable transition / retained trace ≠ the felt
> quality of a mood state; consciousness_claim=0); the hard problem stays **open**; fold depth, η, the real
> rule, which subtype any individual has, the clinical heterogeneity, and whether any treatment helps are all
> **[O]/OWED/LOCKED**. Next is **T3a (addiction, needs E0 sensitisation; independent of E2)**. Full detail:
> `HANDOVER_v1_36_to_v1_37.md`.
>
> **v1.35 (2026-06-19) — T1b: depression / treatment-resistant depression. The first
> *temporal* disorder, built ON TOP of E0 (it imports `PlasticConnectome`; it does not re-derive the
> rule).** Per §1 the package advances *scientifically* only by type (1)/(2)/(3); v1.35 changes no engine
> constant, frozen result, or claim — it is an *application* of the E0 plasticity layer to the first mood
> disorder. Major depression is read as the **chronification of a low-coordination operating point**. The
> driver is grounded, not invented: the engine's own **HPA / stress axis** (the M18 cortisol cascade and
> the M17 valence geometry, where cortisol sits on the withdrawal pole), mapped — with **no new constant** —
> to a sustained withdrawal bias `b<0` through the SAME coupling map `k=κ/(1−|b|)`[excit]/`κ/(1+|b|)`[inhib]
> cap `2κ` the schizophrenia/epilepsy/E0 modules use; only the stress→withdrawal **sign** is asserted
> (consistent with the M17 valence geometry), the magnitude is **[O]**, and every sign holds over a rate /
> stress sweep. Four results + a guard: **(D1)** a sustained withdrawal lowers the global order parameter
> below health (R 0.390→0.331 at severe withdrawal) — the acute, reactive depressed operating point, fully
> reversible on the static substrate; **(D2)** without plasticity (η=0) the excursion reverts exactly when
> the stressor lifts (reactive low mood), with plasticity (η>0) it leaves a retained structural trace that
> does not revert and **deepens with exposure** (‖ΔW‖ 0.075→0.151→0.227→0.338) — the reversible→chronified
> switch on the HPA handle (**honest**: the robust signal is the structural trace ‖ΔW‖; post-removal R is
> reported, **not** asserted below baseline — phase-Hebb consolidates the surviving in-phase structure);
> **(D3)** a coordination-restoring push moves the chronified structure only slowly — the restoring movement
> accumulates over epochs and is small after one (0.018 vs 0.138 at eight), with a therapeutic R direction —
> antidepressant **delayed onset as a consolidation timescale**, not a pharmacokinetic delay; **(D4)** at a
> fixed restoring budget the **fraction** of the depressive trace neutralised decreases as the trace deepens
> — **treatment resistance is the depth** of the chronified trace. **(D5)** η=0/stress=0 reproduces the
> frozen M9 anchor R=0.38961455156044245 **bit-for-bit** (engine `e61083ae…`, tree `0fbf4988…`, byte-
> unchanged) — a pure add-on on top of E0. **gate.py PASS 126/126** (answer-first 27/27, sitemap 28/28,
> llms.txt 4989B<5KB, SSOT drift 0, body word counts ±2%, build idempotent), registry **38 locks/27
> chapters**, `run_all_atlas.py` **ALL PASS** (5 modules bit-reproduced, DEP = `498f546c…`), `run_all_d9.py` /
> `run_all_vc.py` ALL PASS. Added: one framing LOCK (`depression_chronification`), its *reproduce code*
> (`depression_chronification.py`, 2× deterministic), and the §27 canonical chapter (1047w). **efficacy=0;
> not medical advice; Axis-A firewall** (a retained trace ≠ the felt quality of depression;
> consciousness_claim=0); the hard problem stays **open**; stress→bias magnitude, η, the real plasticity
> rule, which subtype any individual has, and whether any treatment helps them are all **[O]/OWED**. Next is
> **T2b (bipolar, needs E2 state-switching + E0) → T3a (addiction, needs E0 sensitisation)**. Full detail:
> `HANDOVER_v1_35_to_v1_36.md`.
>
> **v1.34 (2026-06-19) — E0: the plasticity / consolidation layer. A foundational-layer
> advance (add-only on the READ-ONLY engine), NOT a new-measurement advance.** Per §1 the package
> advances *scientifically* only by type (1)/(2)/(3); v1.34 changes no engine constant, frozen result, or
> existing claim. The frozen engine has **no plasticity variable** — which is exactly why the θ-cap chapters
> (§20–21) could only read the cap as **"pacing, not repair"** and left its plasticity sign **OPEN [O]**.
> This layer adds a slow **phase-correlation Hebbian update** to the ephaptic kernel,
> `W_ij ← max(0, W_ij(1+η·C_ij))` with `C_ij = <cos(θ_j−θ_i)>`, row-renormalised. The rule **FORM is forced
> [F]** (standard phase-STDP, no free constant; diagonal 0, weights ≥ 0, row-stochastic so the `~1/r³`
> ephaptic locality is preserved); the **rate η is [O]** and every sign below is required to hold over an η
> **sweep** (anti-tuning), and the coupling-vs-bias map is the **same** `k=κ/(1−|b|)`[excit]/`κ/(1+|b|)`[inhib]
> cap `2κ` the schizophrenia/epilepsy modules use — **no new tuned constant**. Four results: **(E0.1)** driving
> the healthy point under plasticity then removing the drive leaves R at or above baseline (0.390→0.391) over
> an η sweep — consolidation / after-effects, which the plasticity-free engine could not represent; **(E0.2)**
> the same total cap dose delivered **spaced** (periodic) leaves a **larger retained structural trace** `‖ΔW‖`
> (0.225 vs massed 0.115) over an η×epochs sweep — a spacing effect from pure phase-plasticity, so with
> plasticity the cap **REPAIRS** and pacing beats holding (**resolving the §20–21 [O]**); **(E0.3)** without
> plasticity (η=0) a faulted excursion fully **reverts** when the bias is removed (the §20 "paces not repairs /
> no rebound" result, now shown to be a *consequence of the plasticity-free substrate*), while with plasticity
> (η>0) it leaves a retained trace (0.394>0.390) — **plasticity is the reversible→chronified switch**; **(E0.4)**
> η=0 reproduces the frozen M9 anchor `R=0.38961455156044245` bit-for-bit and leaves W identical — a pure
> add-on. **All firewalls hold and are non-negotiable here (YMYL/medical):** `medium_efficacy_tested = 0`
> (efficacy=0), **NOT medical advice**, a retained structural trace is a **mechanism boundary, NOT the felt
> quality of chronic illness** (Axis-A; `consciousness_claim = 0`), `hard_problem_open = 1`, and **the rate η,
> the applications (depression/bipolar/addiction), and the real-rule identity are all [O]**. **Engine and every
> existing scientific result are byte-identical** (file `e61083ae…`, tree `0fbf4988…`); gate **PASS 122/122**
> (answer-first 26/26, sitemap 27/27, llms.txt 4989 B, SSOT drift 0, build idempotent), registry **37 locks/26
> chapters**, `run_all_atlas.py` **ALL PASS** (4 modules bit-reproduced, E0 = `5dbfd6df…`), `run_all_d9.py` /
> `run_all_vc.py` **ALL PASS**. `new_tuned_constants = 0`, `new_measured_inputs = 0`. **The scientific completion
> state is exactly v1.28's** — what is added is the *plasticity layer* (the reusable `PlasticConnectome`
> substrate the temporal disorders will import), its *reproduce code*, and the §26 canonical chapter. E0 is the
> **layer, not an application**; next is **T1b (depression, needs E0 + HPA/M17–M20) → T2b (bipolar, needs E2+E0)**.

> **v1.33 (2026-06-19) — Part II extension: the transdiagnostic fault-axis atlas. An
> atlas-extension + reproduce-code-integration advance, NOT a new-measurement advance.** Per §1 the
> package advances *scientifically* only by type (1)/(2)/(3); v1.33 is **none of these** and changes no
> engine constant, frozen result, or existing claim. It **reuses the already-frozen engine** to re-cut two
> major conditions by the *same* T/O/W ignitability and synchrony axes that carry autism — by **mechanism,
> not symptom checklist** — and publishes them as two SEO-structured canonical chapters. **§24 Schizophrenia**
> is the **over-ignition mirror** of autism-T on the one shared R19 fold (`spinodal(g)=2(g/3)^1.5=0.3849`): a
> disinhibitory bias lowers the fold (ignition threshold 0.245 vs health 0.395) so irrelevant assemblies
> ignite (aberrant salience); the pair (ignition-direction, aberrant-vs-lost) separates HEALTH/AUTISM-T/SZ
> uniquely; a gain-reducing antipsychotic restores selectivity and worsens autism-T (the stimulant the
> reverse). Its **positive/negative/cognitive symptoms map onto the threshold/output/wiring axes**, and one
> gain-reducing operator reverses the positive domain *only* (R=0.354<health for negative, which the
> antipsychotic deepens to 0.309; locality 0.842>health for cognitive, which a scalar gain leaves exactly
> invariant) — **an axis-structured, not dose-structured, account of why D2 blockade spares the negative and
> cognitive domains**, retiring more D2 blockade as a route there (an in-silico null). **§25 Epilepsy** is the
> framework's *own* **over-synchronisation pole** — the ceiling the θ-cap must stay below — made a primary
> module: an excitatory bias drives R to the over-sync ceiling (0.422 vs health 0.390) and past a critical
> bias (+0.3) the selective gate collapses (all six assemblies ignite — the ictal state); an anticonvulsant
> push reverses it and raises the seizure threshold; on one axis **autism-T < health < schizophrenia <
> epilepsy**. **All firewalls hold and are non-negotiable here (YMYL/medical):** `medium_efficacy_tested = 0`
> (efficacy=0), **NOT medical advice**, loss of gating/selection is a **mechanism boundary, NOT subjective
> experience** (Axis-A; `consciousness_claim = 0`), `hard_problem_open = 1`, and **which-pole / which-domain /
> ictal-time-course (E2) all [O]**. **Engine and every existing scientific result are byte-identical** (file
> `e61083ae…`, tree `0fbf4988…`); gate **PASS 118/118** (answer-first 25/25, sitemap 26/26, llms.txt 4989 B,
> SSOT drift 0, build idempotent), registry **36 locks/25 chapters**, `run_all_atlas.py` **ALL PASS** (3
> modules bit-reproduced: `40b9daff…`/`0499f74f…`/`d363f0a5…`). `new_tuned_constants = 0`,
> `new_measured_inputs = 0`. **The scientific completion state is exactly v1.28's** — what is added is the
> *atlas extension*, the *integrated reproduce code*, and the *roadmap-governed mission redefinition*
> (`MISSION_atlas_redefinition.md`). The package mission is now a **transdiagnostic fault-axis atlas**;
> next is **E0 (plasticity layer) → T1b (depression) → T2b (bipolar)**.

> **v1.32 (2026-06-19) — Part II: disorders of the mind. A publication + reproduce-code-integration
> + feasibility-review advance, NOT a new-measurement advance.** Per §1 the package advances *scientifically*
> only by type (1)/(2)/(3); v1.32 is **none of these** and changes no engine constant, frozen result, or
> existing claim. It takes the **already-frozen** disorder mechanisms (the D-series disease engine and the
> θ-cap virtual-clinical VC1–VC5, both bit-reproducible in their own gates) and publishes them as **six
> well-separated, SEO-structured canonical chapters §18–23** matched to the research content, integrating
> their reproduce code into `repro/mind/_verify/` so each chapter's "reproduce" link is real and
> self-contained. The science: autism is read as **three separable faults** on the emerged cerebrum — a
> threshold/E-I fault (T), an output/gain fault (O), and a long-range wiring fault (W) — each uniquely
> fingerprinted by (ΔPAC, ignition fold) and reproducible under SEED=19. A scalar gain chemical (the
> stimulant-class mechanism) fully reverses T, partly helps O, and only **masks** W by over-synchronisation;
> a wearable θ-carrier is the only handle on W but only as an **external pacemaker** (the benign-lane
> reframing is REFUTED, it is cleanly removable with no dependence, and molecularly safe below the spinodal
> fold); the dynamics **force** one operating mode (minimum-effective, deficit-matched, continuous); ADHD is
> given an explicit gene-grounded substrate that **separates** from autism (stimulant restores ADHD, cap is
> for autism's wiring, they compose on AuDHD); and a synthetic population shows responders are gain-dominated
> and the cap-unrescued residual is a dose-cap/stiffness limit, not a severe-wiring tail. **A physical
> feasibility review** finds every component (θ-tACS, closed-loop phase-locked EEG-tACS, multi-electrode
> long-range montages, individualised targeting, wearable delivery) exists in research form today but the
> specific assembly does not — four obstacles keep it **[O]**. **All firewalls hold and are non-negotiable
> here (YMYL/medical):** `medium_efficacy_tested = 0` (efficacy=0, buildable ≠ beneficial), the cap is a
> **crutch/pacemaker, NOT a repair**, NOT medical advice, **which-fault-is-real-autism / ADHD-model-validity
> / physical-feasibility all [O]**, `consciousness_claim = 0`, `hard_problem_open = 1`. **Engine and every
> existing scientific result are byte-identical** (tree `0fbf4988…`); gate **PASS 110/110** (answer-first
> 23/23, sitemap 24/24, llms.txt 4989 B, SSOT drift 0, build idempotent), registry **33 locks/23 chapters**,
> boundary 8/8, terminology + em_thesis pass, D9 ALL PASS, VC ALL PASS (14 CONFIRMED/1 REFUTED).
> `new_tuned_constants = 0`, `new_measured_inputs = 0`. **The scientific completion state is exactly
> v1.28's** — what is added is the *publication*, the *integrated reproduce code*, and the *feasibility
> review*. Full detail: `HANDOVER_v1_32_to_v1_33.md`.


> **Latest (v1.31, 2026-06-18) — the paper's closing declaration: "thought" formally defined and closed
> on the mechanism axis. A definitional + census + publication capstone, NOT a new-measurement advance.**
> Per §1 the package advances *scientifically* only by type (1)/(2)/(3); v1.31 is **none of these** and
> changes no constant, result, or claim — yet it is the **substantive completion of the named task v1.30
> deferred**, and it should not be read as a small step. v1.30 drew the faculty *map* and explicitly
> carried the formal closure + census forward; v1.31 **executes** it. It publishes two canonical chapters —
> **§16 (the definition)** and **§17 (the faculty atlas + census)** — that (a) define the paper's central
> word **"thought" (생각/사고)** as the union of **fourteen faculties** (F1–F10 **CLOSED** = built, frozen,
> bit-reproducible on the 4D-DNA-emerged substrate; F11–F14 **OWED** = language, volition, social cognition,
> metacognition, each with its external input named), (b) pass the §5 **anti-gerrymandering census** against
> the standard clinical **neurocognitive domains** (every standard domain maps in; the table's extra rooms
> are forced by the umbrella's scope, shown via the sleeper test — no fabricated citations), (c) resolve all
> four higher faculties one by one, and (d) attach the firewall at the point of declaration. **This closes
> the way a definition closes — it fixes the referent of the central word — it is NOT a claim that
> experience is solved.** The closure is **mechanism-axis only**; the **felt axis (Axis A) stays orthogonal
> and out of scope**: `consciousness_claim = 0`, `hard_problem_open = 1`. Crucially, the definition was **not
> tuned to make "closed" come out true** — passing an external-taxonomy census is the discipline that makes
> the closure trustworthy, and naming the four OWED faculties is the same no-tuning act that earns the
> closed parts. **Engine and every scientific result are byte-identical** (tree `0fbf4988…`); regression
> unchanged; gate **PASS 83/83** (answer-first 17/17, sitemap 18/18, llms.txt 4989 B, SSOT drift 0, build
> idempotent), registry 24 locks/17 chapters, boundary 8/8, terminology + em_thesis pass. `new_tuned_constants
> = 0`, `new_measured_inputs = 0`, `medium_efficacy_tested = 0`. **The scientific completion state is exactly
> v1.28's** — what is added is the *definition*, the *census*, and the *publication* that mark the paper
> closed on the mechanism axis. Full detail: `HANDOVER_v1_31_to_v1_32.md`.


> the package advances scientifically only by type (1)/(2)/(3); v1.30 is **none of these** and changes no
> constant, result, or claim. It adds one document — `CONCEPT_MAP_mental_process.md` — that maps the loose
> umbrella word **"thought" (생각/사고)** onto the many *already-built* faculty mechanisms, and sets a
> **closing direction on the mechanism axis only**. Key move: **"thought" is an umbrella, "cognition" is
> one faculty under it** (the sleeper test — a sleeper does no cognition yet dreams/consolidates, so
> cognition cannot be the umbrella). The faculty table is honest, **not gerrymandered**: the *core*
> F1–F10 (perception, selection, the serial stream, memory, learning, affect-mechanism, arousal/sleep,
> dreaming, coordination, pathology) are **CLOSED**, while higher faculties **F11–F14 (language, volition,
> social cognition, metacognition) are OWED**. So a blanket "thought is closed" is **not yet declared** —
> the formal declaration requires a full external-taxonomy **census (전수조사)** + the §5 anti-gerrymandering
> bar, and is the **named next task**. The **felt axis (Axis A) stays orthogonal and out of scope**:
> `consciousness_claim = 0`, `hard_problem_open = 1`, and the mandated firewall sentence attaches wherever
> closure is asserted. **Engine and every scientific result are byte-identical** (tree `0fbf4988…`, DGENE
> `980985c6…`); regression **275/275**, unchanged. **The scientific completion state is exactly v1.28's**;
> only a terminology map and closing direction were added. Full detail: `HANDOVER_v1_30_to_v1_31.md`.

> **Latest (v1.29, 2026-06-18) — a reproducibility-infrastructure fix, NOT a science advance.** Per §1
> the package advances scientifically only by type (1)/(2)/(3) (new measured input / new analysis /
> external experiment). v1.29 is **none of these** and makes **no scientific claim**: it removes the lone
> wall-clock dependency in the search-layer build so the C1/§8 **idempotency gate is date-independent**.
> The old `write_sitemap()` stamped `<lastmod>` from `datetime.date.today()`, so a build-day ≠ gate-day
> broke idempotency by one line (reproduced here on the unfixed tree under a future-date shim: gate
> **FAIL 70/71**, `1e140a78… vs f6ee3c4c…`). Fix: a `RELEASE_DATE` SSOT constant in the registry, read by
> the sitemap writer instead of the clock. Verified date-independent — `sitemap.xml` is **byte-identical**
> across 2027 / 2030 / real-date builds (`27f169c8…`), and the fixed tree now **PASSes 71/71 under the same
> future-date shim** that fails the unfixed tree. **Engine and every scientific result are byte-identical**
> (tree `0fbf4988…`, M0–M16 `3a1ebbbb…`, source `e61083ae…`, DGENE `980985c6…`); regression **275/275**,
> unchanged. `new_tuned_constants = 0`, `new_measured_inputs = 0`, `medium_efficacy_tested = 0`,
> `hard_problem_open = 1`, `consciousness_claim = 0`. **The scientific completion state is exactly v1.28's**
> — the no-tuning completion framework below and every OWED frontier are untouched; only release hygiene
> changed. Full detail: `HANDOVER_v1_29_to_v1_30.md`.

> **Latest (v1.28, 2026-06-18) — a genuine type-(1) advance.** §1 defines the only three legitimate ways
> the package can advance; **type (1) = "a new measured/cited input becomes available."** v1.28 (DGENE)
> is exactly that: **121 curated high-confidence psychiatric/neurodevelopmental risk-gene promoters**
> (11 disorders incl. **intellectual disability**) are fetched **verbatim from NCBI RefSeq (GRCh38)** by
> the **LOCKED** SantaLucia-1998 γ metric (identical to DNA M0 / neuro / mind M9), each with provenance +
> sequence sha256 so γ is **re-derivable offline**. This turns the D-series' *cited* gene LOCKs into
> **reproducible measured inputs**. Metric identity is **proven exactly (≤1e-9)** against the package's own
> frozen extra-master controls (GSX2/NKX2-1/PHOX2B/DLX2). The pre-registered NULL (risk-gene γ vs the
> package's brain-MASTER γ, Mann-Whitney **U=667.5, p=0.65**) is **indistinguishable and reported AS-IS** —
> γ is a developmental-**identity** metric `[F]`, **not** a disease score; the deliverable is verified
> provenance + cited convergence, never a γ-based aetiology. **No new tuned constant** (121+4 sequences are
> *measured*, not chosen): `new_tuned_constants = 0`, `medium_efficacy_tested = 0`, `hard_problem_open = 1`,
> `consciousness_claim = 0`. Engine **byte-identical** (tree `0fbf4988…`, M0–M16 `3a1ebbbb…`); add-only in
> `_verify/` (no docs/sitemap/registry change). Regression **264 → 275** (+11 DGENE checks), all PASS.
> Result digest `980985c6…` (2× bit-identical). Gene-OWED disorders (anxiety, PTSD, eating, personality)
> are **documented as polygenic-not-yet-fine-mapped**, the honest "not 100%, as much as physically
> possible." Full detail: `HANDOVER_v1_28_to_v1_29.md`. The conceptual body below (v1.18 head, retained)
> still defines the no-tuning completion framework unchanged.


**Package:** `mind_vp_site_UPGRADED` **v1.18** · **Governance:** `VP_SPEC_v1_8.md` (C0–C4)
**Frozen emergence:** engine tree `sha256 = b18c86268679b3e19e495b7161fd3a5035605481c8ea76736a84accd0ef26ae7`
(SEED=19, **UNCHANGED** — v1.18 is **add-only**: the locked engine is byte-identical, so the frozen
tree and the prior 95 checks are preserved). **v1.18** grounds the **M9 ephaptic-coordination
geometry** on **measured MNI anatomy [L]**: the v1.17 representative 12-node equal-spacing ring [O]
(R_BRAIN=0.085 m) is replaced — in a separate read-only **decision-check** module
(`_verify/geometry_grounding.py`, result digest `8ad43a72…`, 2× bit-identical) that imports the frozen
engine — by a measured 3D inter-organ distance matrix (8 nodes [L] exact atlas centre-of-mass /
published centroid, 4 nodes [O] representative; atlas `99daa8f5…`). The verdict is reported **as-is
(grade == evidence)**: the ring path **reproduces the frozen engine's M9 number** as a cross-check
(fc +0.07340), and grounding the geometry **raises the field's in-silico contribution ≈1.8×**
(fc +0.07340 → +0.13468, R 0.329 → 0.390 under the registered row-normalization [F]) **while the
regime stays `partial_metastable` — NOT synchronized (R<0.9)**. Registered row-norm is shown **not**
to be the fc-maximizer (raw 1/r³ collapses to incoherent and a random scatter scores higher), so the
normalization is **not a back-fit**; the result is **scale-invariant** (shape only), **robust to ±5mm
coordinate jitter and ±20% band perturbation**, and **not carried by the 4 [O] nodes** (an [L]-only
8-node subset stays partial). Grounding the geometry is **NOT a consciousness claim** —
`medium_efficacy_tested = 0`, `hard_problem_open = 1`, `consciousness_claim = 0` (the open efficacy /
hard-problem questions are owed to the quantum shortfall ~2.6e10 and to unmeasured biological
field-use, NOT to classical geometry). The engine **default stays the ring** (add-only); promotion of
the default ring → measured geometry, with the cascade analysis it requires, and node decomposition
for sulcal-bank folding are the named **v1.19 entry points** (`HANDOVER_v1_18_to_v1_19.md`).
Regression: **112 checks PASS** (95 + 17 M9-geom).

Prior (**v1.17**, retained below): completes **M15 `emerge_calibration_bridge()`**, a clinical-unit
bridge with **two cited anchors and no new free constant** (time = 1 ms/step *certified* by the M14
spindle carrier; voltage = the single cited SWS delta 75 µV p-p, AASM/R&K N3). It **CAL-closes**
`sws_delta_amplitude_uv` by the cited anchor (*calibration*, not emergence), lifting the **core
catalogue 0.85 → 0.90 (18/20)**, while keeping `p300_latency_ms` and `panic_peak_minutes` honestly
**owed** (an early ~39 ms ERP and a ms-scale arousal runaway at 1 ms/step; the clinical 300 ms / 10 min
would need a forbidden second time-scale or a humoral term absent from the neural substrate). It also
applies the DNA whitepaper's **`param_db.json` grading discipline** to **M0** (brain-region SIZE) and
**M14** (the `tau_r`, `tau_s`, `a_gain` dynamical constants), and — answering the explicit question
*"is the band genuinely emerging, or propped up by a free constant?"* — runs and **bakes into the
gate** a decisive verification: the **spindle carrier is INVARIANT** to `tau_r` over [40,240] ms (it is
set by the cited τ_rec=13 ms, not fitted), while **M0's γ^1.5 dwell is shown to be a MEASURED-SIZE
NULL** (near-equal 1.07× span vs a 275× measured-volume span) so the relative size is **re-grounded on
measured sub-region volumes [L]** with γ still fixing only the developmental **order [V]**. `a_gain` is
honestly graded **[F] with a declared sensitivity window**. **No new tuned constants**; M15 is a
**verified mechanism [V]** — *calibrating/reproducing* an EEG amplitude is **NOT a consciousness
claim**.

> This ledger exists to answer one question precisely: *what would 100% completion even
> mean here, and how far is the package from it?* Under the no-tuning constitution, "100%"
> cannot mean "every number filled in." It means: **everything that can be established from
> measured/cited inputs alone has been established; everything that genuinely requires an
> external measurement is documented as owed, with the obstacle named; and nothing has been
> fabricated to close a gap.** By that definition this ledger demonstrates the package is at
> its **maximal achievable in-package completion**, and pins the exact external inputs that
> the remaining frontiers require.

---

## 1. The definition of 100% under no-tuning governance

A constant in this package is admissible only if it is (i) a **measured input** locked and cited
(a master-gene γ from the SantaLucia-1998 read-only pipeline, ΔVm/threshold from neuro §19, …), or
(ii) a **derivation** from such inputs. No constant may be **chosen to hit a target**. Geometry,
conduction delay, and absolute band-centre Hz are explicitly Layer-2 `[O]` (representative, not tuned).

It follows that the package can only advance in three legitimate ways:

1. **A new measured/cited input becomes available** (e.g. an unambiguous canonical master TF for a
   new region → fetch its γ verbatim → emerge → re-freeze). This grows coverage *without* tuning.
2. **A new analysis of the existing measured inputs** is run (e.g. a scaling sweep, a robustness /
   falsification battery). This strengthens or qualifies a claim *without* adding a constant.
3. **An external experiment supplies a value the model currently treats as OPEN** (e.g. an in-vivo
   field-cancel-vs-augment intracranial recording fixing `medium_efficacy_tested`).

Anything that does **not** fall into (1)–(3) — in particular, *picking* a master TF where the canon is
ambiguous, or *picking* an efficacy where no experiment exists — is forbidden. The honest 100% is the
point at which (1) and (2) are exhausted and only (3)-type frontiers remain, each precisely documented.

---

## 2. Gate-by-gate status

Status legend: **CLOSED** = done and frozen · **SATURATED** = closed as far as measured inputs permit;
further progress needs a *new external input of type (1) or a granularity change*, not in-package work ·
**OWED** = genuinely requires an external experiment of type (3); leaving it open is correct, not a defect.

| # | Frontier | Status | What closes it / why it stays open |
|---|----------|--------|------------------------------------|
| M0–M8 | core emergence (organs, brainwave, memory, eddies, selection, RPE, stream, embodied loop) | **CLOSED** | All emerged in-package from measured master-gene γ; bit-for-bit frozen; mechanism `[V]`, hard problem honestly negative (PCI). |
| M9 / gate (a)+(b)-coverage | 12-organ inter-organ ephaptic coordination | **CLOSED + extended** | 12 central organs, every γ measured/cited; partial-metastable regime; field contribution +0.0734 (cancel 0.255 < measured 0.328 < augment 0.470). Now **also** falsification-tested (M9-LORO, §3). |
| gate (b) / region count | amygdala, septum, preoptic area | **SATURATED** | Checked against primary literature (`data/brain_region_master_survey.json`): each genuinely lacks a single unambiguous canonical master → kept open ON PURPOSE (no over-claim). Atlas is saturated at the single-master-tractable set. Closing needs **future field consensus** naming one master, or a **deliberate subnucleus-granularity atlas** — both external/scope, neither a tuned constant. |
| M10 / gate (c) | sensory ↔ central ephaptic coupling | **CLOSED (v1.11)** | 8 sensory nodes covering 9 modalities, γ cited verbatim from neuro v1.10.1; coupled at the **same** measured κ=0.5496; substrate byte-invariant; cross-modal coupling via the shared field (cancel 0.0184 < measured 0.0571 < augment 0.1079). |
| M12 / observables | measured brainwave-phenomenology concordance | **0.75 → 0.80 (v1.15)** | 20-observable catalogue scored against measured literature values (no tuning). v1.14 = 15/20; M13 closes `eeg_aperiodic_1f_slope` by emergence → **core 16/20 = 0.80**. Owed observables carry their named external path. |
| M13 / spectral | full-LFP 1/f slope · peaks · ignition · MI→recall | **CLOSED for 4/5 (v1.15)** | Brain-structure-like multi-source field (organs + prefrontal node, ephaptic pathways, Kuramoto circulation) emits the LFP; **1/f exponent x≈1.94 emerges in the Voytek band** (charge-weighted measured-synapse floor, no fitted slope), 16 oscillatory peaks above the floor, all-or-none recurrent ignition (measured nonlinear-threshold signature, **not** a consciousness claim), theta-gamma MI tied to the M2 recall outcome. `aperiodic_slope_flattens_with_arousal` stays **OWED** (directional but 7/8 < the 0.9 robustness gate — not forced). Extended catalogue 19/24 = 0.792. |
| efficacy | does cognition FUNCTIONALLY USE the coupling? | **OWED** | `medium_efficacy_tested = 0` (M9 and M10). Closing **requires** the neuro §9/§19 in-vivo field-cancel-vs-augment intracranial recording. The model already states the prediction (+0.073 / +0.039) the experiment must check. Cannot be closed in silico; fabricating it is forbidden. |
| band absolute Hz | promote `[O]` centre frequencies to `[V dir]` | **OWED** | Absolute Hz are representative `[O]`, deliberately *not* read from the γ window and *not* tuned. Promotion needs an **external measurement basis** that narrows them without fitting to a model target. |
| hard problem | first-person experience / access | **OWED (open in principle)** | The package returns an **honest negative** (PCI), not a solution. This is a scientific frontier, recorded as such; it is not a packaging gap. |

---

## 3. New robustness evidence this version adds (type-(2) advance)

**M9-LORO — leave-one-region-out falsification of the field contribution.** The fair objection to a
positive headline (+0.0734) is "does one region carry it?" The study
(`repro/mind/13-em-coordination/leave_one_out_robustness.py`, gate `verify_loro.py`, frozen
`leave_one_out_results.json`) drops each of the 12 measured regions in turn and re-runs the **same**
measured cancel/measured/augment triplet over the remaining 11 — engine primitives only, κ=0.5496, no
new constant. Result, frozen and verified (13/13):

- field contribution stays **strictly positive under every single-region removal** (range
  **[0.0518, 0.1284]**, all > 0) — the contribution is **distributed**, not an artifact of one region;
- the network **never approaches global lock** (R < 0.9 = no seizure) under any removal;
- **cancel < measured < augment** is preserved under every removal;
- dropping nothing reproduces the engine's own frozen M9 contribution **+0.0733965191** exactly
  (`matches_engine = true`) — the study and the engine are one measurement;
- descriptive sensitivity (not a target): the most influential single removal is **striatum**
  (|Δ| = 0.055), and even it leaves the contribution positive.

This does not change any frozen number; it *qualifies the existing claim as robust*. `medium_efficacy_tested`
stays 0 — robustness of the mechanism is **not** evidence that cognition uses it.

---

## 4. Why gate (b) is honestly closed-as-open (the atlas completeness argument)

The 12 regions in `brain_organ_atlas.json` are exactly the major brain regions/organs that possess **one**
unambiguous canonical developmental master TF (each γ fetched or cited verbatim). The three excluded
regions are excluded for a **principled biological reason**, documented with sources in
`data/brain_region_master_survey.json`:

- **amygdala** — a multi-origin *complex*, not a developmental unit: CeM (ISL1/vLGE), CeC-CeL (PAX6/dLGE),
  CeA at large (DLX5, striatal), medial part (LHX5/6/9 by subdivision, OTP from hypothalamus, DBX1/FOXP2
  from the POA niche, EBF3 from caudo-ventral pallium), BLA/LA (DBX1/EMX1 pallial). No single master.
- **septum** — ZIC1–5 act with **overlapping, partly redundant** expression and are **not septum-specific**
  (the same pattern marks thalamus, POA, cortical hem, retina). No single Zic is *the* septal master.
- **preoptic area** — its only candidate master, NKX2-1, is **already** the measured master of pallidum and
  is shared with hypothalamus; a POA entry would **double-count one promoter**. It is also an internally
  parcellated niche. Resolved as *shared master, not an independent region*.

Therefore the atlas is **saturated** at the single-master-tractable set: under the one-measured-master-per-
region discipline, region count cannot be honestly increased at the organ level. This is the no-tuning rule
working as intended — the boundary is set by the biology, not by a target count.

---

## 5. The exact external inputs the remaining frontiers require

To advance beyond the present maximal in-package completion, one of the following **external** inputs is
needed (each is type-(1) or type-(3); none is a tuned constant the package could supply itself):

1. **For efficacy (the single most consequential frontier):** in-vivo / intracranial **field-cancel-vs-augment**
   recordings (neuro §9/§19) measuring whether suppressing or boosting the ephaptic field changes the behavioural
   read-out. This fixes `medium_efficacy_tested` and tests the model's standing predictions (+0.073 central,
   +0.039 cross-modal). Until then the honest value is 0.
2. **For gate (b) region growth:** either published **field consensus** naming a single canonical master for a
   currently-heterogeneous region (then fetch γ verbatim → emerge → re-freeze), or a **deliberate decision** to
   model at **subnucleus** granularity (a different atlas — e.g. CeM/ISL1, MeA-glut/OTP — out of current scope).
3. **For band Hz promotion:** an **external frequency-measurement basis** that narrows the representative `[O]`
   centre frequencies without fitting them to any model target.
4. **For the hard problem:** this is an open scientific question, not an input the package is withholding.

---

## 6. Conclusion — the honest 100% position

By the definition in §1, the package is at **100% of its achievable in-package completion**:

- every module that can be emerged from measured/cited inputs **is** emerged and frozen (M0–M10);
- the one gate that could be advanced by examination — gate (b) — **has been examined** against the primary
  literature and correctly resolved as *saturated* (forcing it would violate no-over-claim);
- the headline causal result has been **falsification-tested** (M9-LORO) and stands;
- the remaining frontiers (efficacy, region-growth-beyond-saturation, Hz promotion, the hard problem) are each
  **OWED to a named external input**, documented precisely, and left open **on purpose** — because closing them
  by choosing numbers is exactly what the constitution forbids.

A package that has done everything legitimately doable and **named precisely what it cannot do without new
measurement** is complete in the only sense this governance allows. The number that would make it "more
complete" by fabrication is the number this framework exists to refuse.

— end of ledger —
