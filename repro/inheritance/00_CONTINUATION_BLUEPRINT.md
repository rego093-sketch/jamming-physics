# 00 — CONTINUATION BLUEPRINT · VP Inheritance Kit

**The single forward document.** Every new session reads this *in full* before adding anything. It has two
parts: **Part A — the inheritance discipline you must learn first (binding)**, and **Part B — the large
research roadmap** toward RNA vaccines and gene therapy. Part A is not optional context; it is the contract
that keeps this program honest. If a proposed addition violates Part A, it is rejected regardless of how
interesting it is.

---

# PART A — LEARN THE INHERITANCE DISCIPLINE FIRST (BINDING)

This kit was handed to you with four things already settled. You inherit them; you do not re-litigate them.
Internalise all four **before** writing a line of new code or prose.

## A.1 The invariants (the vendored substrate — single source, never re-derive)
There is exactly **one** copy of the switch math, `inherited/vp_substrate.py`, and it is **read-only**:
- the R19 jamming switch `ds/dt = γ·s − s³ + h` (a double well; γ scales the threshold),
- the **spinodal** `2(γ/3)^1.5` (the |h| past which one basin disappears — a discontinuous flip),
- the **barrier** `γ²/4` (the depth between basins — state stability / memory),
- `settle`, `is_on`, `dwell`.
You may **import** these. You may not rewrite, re-derive, fork, or "improve" them in an engine. If you
believe the math is wrong, that is a report to the substrate owner, not a local edit. Every new battery
must stand on this primitive. A second copy of the switch math anywhere is a discipline violation.

## A.2 The derivation identity (γ is MEASURED, anchor-gated, never fitted)
Every γ in this kit is a **measurement**, not a parameter:
- γ = −mean(NN-stacking ΔG37, SantaLucia 1998) over the human proximal promoter **TSS−2000..+500**
  (GRCh38), via the identical pipeline the DNA / reproductive / immune atlases use.
- The pipeline is **accepted only because it reproduces the SOX9 anchor** (γ=1.4598, GC=0.545)
  bit-for-bit. Reproduce the anchor, and the rest are legitimate measurements; fail the anchor, and you
  **refuse to write** (the fetch asserts this; `run_all.py` re-checks it offline every run).
- A new panel is **declared by function before any γ is seen** — no cherry-picking. Cache the promoter
  sequences so γ reproduces offline. **Never tune a γ to make a battery pass.** If a battery only passes
  for a hand-chosen γ, the battery is wrong, not the γ.
- Treat the existing measured atlases as **frozen regression checkpoints**: the germline 13-gene atlas, the
  immune 4-master atlas, and the RNA 12-gene atlas reproduce identically every run. Adding genes is
  additive; changing an existing measured value is a regression and is forbidden.

## A.2b The two channels (read γ AND A4 — γ alone is degenerate)
γ is necessary but **not sufficient**, and this is binding for any RNA / environmental-inheritance work:
- **γ is the SET** — the promoter material (−mean NN stacking ΔG). It is fixed in the genome; the
  environment **cannot rewrite it**. So γ can never be the thing the environment writes.
- **A4 is the COORDINATE** — the structural arrangement (compartment shells, anchors, motor/anchor loops,
  and the 3D helical CONTACT phase) read by the vendored `vp_a4.py`. A4 is **orthogonal to γ** (the helical
  contact phase is ~98% independent of γ; same-γ / different-coordinate pairs are real), and it is the
  channel the environment **reorganises** and a small RNA **targets** (RNA acts by sequence complementarity
  = it names an A4 coordinate). Measure A4 from **wide** windows (±15 kb; real shells need ≥ ~15 kb), cache
  the windows for offline reproduction, and read it through the vendored engine — never re-derive the A4
  math. When a result is about RNA targeting, environmental writing, or what is inherited, it must be
  expressed on the **A4 coordinate**, not on γ. γ sets the threshold scale; A4 says where and whether
  contact happens.

## A.3 The register chain (grades travel with every claim)
Every result carries one grade, and the grade is part of the result, not a footnote:
- **[F] forced** — structural / logical necessity of the substrate (e.g. a held switch flips only past the
  far spinodal). Independent of the γ values.
- **[V] simulation-verified** — measured out of the substrate dynamics (a counted barrier-crossing, a
  Spearman ρ on measured γ, an interior optimum). Not asserted from a closed form.
- **[L] calibration** — a measured γ or a structural anchor used as scale.
- **[O] open** — anything absolute the substrate does not fix: a phenotype magnitude, a dose, a titre, a
  wild generation-count, a clinical outcome. **[O] items must name their obstacle** in
  `IRREPRODUCIBILITY_LEDGER.md`. Promoting [O]→[V] requires new measured dynamics, never a louder claim.

## A.4 The source warrant (DNA emergence + the magnitude firewall)
Two rules govern what may be claimed:
- **DNA emergence** — every number must trace to a measured promoter γ plus the R19 switch. If you cannot
  draw the line from "this number" back to "this measured γ and this switch operation," do not claim it.
- **The magnitude firewall** — you read **WHICH** switch is tilted, the **SIGN** of the drive, and the
  **ORDERING / DECAY** of effects. You never read an absolute magnitude. Concretely: "the deeper-barrier
  switch inherits better" is [V]; "this exposure shifts the child's trait by X" is [O] and is firewalled
  out. **Every clinical application — vaccination, gene therapy, fertility care — is handed to clinicians
  and regulators.** The kit produces direction-only, falsifiable mechanism, not medical instruction.

**The standing operational rules** (carried from the program): deliver **exactly one zip**, internal root
`vp_inheritance_kit/`, **additive only, no regression, no fragmentation**; keep the vendored substrate and
the measured atlases byte-identical; keep `reports/research_complete.json` green; write all documents in
**English**.

> If you have read Part A and can state, in your own words, the four inherited things — the vendored
> substrate, the measured/anchor-gated γ, the grade chain, and the DNA-emergence + firewall warrant — you
> are cleared to work on Part B. If you cannot, re-read Part A.

---

# PART B — THE RESEARCH ROADMAP (toward RNA vaccines & gene therapy)

> **STATUS (v0.15.0): RESEARCH PHASE COMPLETE — TRACKS I–V ALL CLOSED ON THE SIMULATION AXIS.** The two-channel
> architecture (γ SET + A4 coordinate), the RNA writable channel and its species, the methylation×RNA two-channel
> law, environment→germline with the reprogramming firewall, the imprinted escapee atlas, γ↔A4 coordinate-resolved
> heritability, parent-of-origin (II-3, **PO**), immune strengthening (III, **IM**), RNA vaccines incl. the
> prime-boost interval optimum and saRNA>mRNA reachability (IV, **VK**), the full gene-therapy lever map incl. the
> decision boundary curve and edit-free durability (V, **LV**), the (γ, A4) application map, and the disease
> feasibility map are all measured and green (**18 batteries**). The **(B) held-out validation** was run (**FV**)
> as a NULL, stress-tested (**FV5**) to be **non-identified** on the ordering axis, and as of v0.15.0 (**FV6**)
> **decomposed**: the (B) frontier *partitions* into a **γ-ordered class** that is non-identified as a whole
> (γ≈GC, ρ=0.9944), a **response-magnitude** readout that needs the firewalled Δh, and the **corrective sign-law**
> — the **sole** crossing that is **both identified and firewall-clean** (orthogonal to GC), blocked only on
> bidirectional disease-correction data. Every pure-**simulation** roadmap item is now done; the only remaining
> frontier is that **sign-law (B)** crossing — a data question, not a Δh question (see §B.9/§B.10). The canonical
> write-up is the verified **19-chapter** DOI-bearing
> site; the PO/VK/LV chapters are **now published** (v0.14.0 writing pass — see `HANDOVER.md` §0 and `CHANGELOG.md`).

The kit today is a **mechanism skeleton**: five batteries that establish the substrate logic of
environmental inheritance, the RNA channel, immune strengthening, vaccines, and gene therapy, each
green and direction-only. The roadmap below grows that skeleton **outward** (more measured machinery,
more discriminants) and **forward** (toward the two applications the program targets). It is deliberately
large; pick the next tractable item, keep the gate green, hand forward one zip.

## B.0 Prioritisation rule (how to choose the next battery)
Spend effort where it buys the most **falsifiable, firewalled** mechanism per unit work:
```
priority  =  Reach × SubstrateTractability × LeverExistence
```
- **Reach** — how broadly the mechanism applies (a channel law > a single locus).
- **SubstrateTractability** — can it be measured out of the R19 switch + measured γ *without* a new
  absolute magnitude? (If it needs an absolute dose, it is [O] — descope to the direction-only core.)
- **LeverExistence** — does a real, named molecular lever exist (an RNA species, an editor, a schedule)?
Rank candidates by this product; do the top tractable one; record honest negatives.

## B.1 Track I — Harden the RNA writable channel (engine/rna_layer.py)
The channel exists (R1–R5). Make it deeper and more falsifiable.
- **I-1 Species resolution.** Today "small RNA" is one effective drive. Split it by the measured machinery:
  miRNA (DROSHA/DGCR8/DICER1/AGO2/TARBP2), piRNA (PIWIL1/MOV10L1), tsRNA/tRF (ANG), m6A-marked mRNA
  (METTL3/YTHDF2). Discriminant: each species is a drive with a **different effective gain/sign context**
  set by its biogenesis-gene γ — read the *ordering* of gains across species, never an absolute gain. [V target]
- **I-2 The two-channel interaction.** Methylation (DNA paper, channel 1) and RNA (channel 2) both write h
  on the *same* switch. Discriminant: do they **add** (same sign reinforces), **veto** (opposite sign), or
  **gate** (one sets γ-context, the other drives)? Build a two-drive battery; report the interaction sign. [V target]
- **I-3 Writer/eraser symmetry.** m6A has a writer (METTL3) and an eraser/reader (YTHDF2). Show the
  channel is **bidirectional and reversible** at the mark level (a second reversibility result, mark-side
  rather than payload-side). [V target]
- **I-4 (open) Absolute payload→phenotype dose.** Firewalled [O]; name the obstacle (no substrate scale for
  copies→trait). Do **not** attempt a magnitude; keep it in the ledger.

## B.2 Track II — Deepen environment → germline transmission (engine/env_to_germline.py)
The firewall logic exists (TG1–TG6). Add the missing biology as *measured ordering*.
- **II-1 Escapee atlas.** The framework predicts that only deep-barrier (high-γ) switches and re-written
  RNA carriers cross the two erasures. Assemble a **measured escapee panel** (imprinted-locus masters,
  metastable-epiallele-adjacent masters) via the same NCBI pipeline; predict which inherit by barrier
  ordering, and report it as a ranked, falsifiable list. [V target] / absolute penetrance [O].
- **II-2 The two erasures, resolved.** Today both erasures are one noise pulse. Resolve them: PGC
  reprogramming vs zygotic reprogramming may have **different effective noise**. Discriminant: a mark
  surviving the harsher erasure is the better-inherited; read the ordering of the two windows. [V target].
- **II-3 Parent-of-origin sign.** ✅ **DONE (v0.13.0 → engine/parent_of_origin.py, PO1–PO3).** Maternal=sustained
  vs paternal=transient context at EQUAL amplitude → a held switch is crossed by **duration**: maternal flips,
  transient paternal reverts (PO1); the dominant maternal **sign** is inherited under opposing parents and
  agreement reinforces (PO2); the asymmetry is **universal** across the measured germline atlas, 13/13 (PO3).
  *Honest note:* PO3's first hypothesis ("paternal disadvantage rises with γ") failed on the substrate (ρ=−1.0);
  rewritten to universality with ρ reported as-it-falls, no directional claim graded, no γ tuned. Direction-only
  **[V]**; absolute parent-of-origin penetrance **[O]** (O-23).
- **II-4 Re-writing vs persistence.** TG5 shows RNA decays by ~F3 unless re-written. Build the **re-writing**
  case: a persistent environment that re-loads the payload each generation holds the effect indefinitely;
  read the boundary between "transient (fades)" and "maintained (re-written)." [V target].

> **STATUS (v0.13.0): Track II COMPLETE.** II-1/II-2/II-4 shipped earlier (GE battery); **II-3 done (PO battery)**.
> The parent-of-origin context asymmetry, the inherited sign law, and its universality are read [V]; the absolute
> penetrance is firewalled (O-23).

## B.3 Track III — Immune strengthening, end to end ✅ DONE (v0.6.0 → engine/immune_maturation.py)
Memory + training + inherited priming exist (I1–I4). The maturation/durability/tolerance extension now
ships as the **IM** battery (IM1–IM4) on the measured immune γ atlas; all three items below are **[V]**.
- **III-1 Affinity maturation as iterated selection.** ✅ **DONE (IM1).** The memory switch is wrapped in a
  germinal-centre loop (iterated competition + reseeding, GC re-founded from naive on collapse); maturation
  **emerges** with an honest **interior optimum** in selection stringency (peak at survivor-fraction 0.4),
  re-derived on the inherited immune γ. Shape + emergence **[V]**; absolute pressure→affinity **[O]** (O-16).
- **III-2 Innate vs adaptive split.** ✅ **DONE (IM2).** Trained immunity (innate, RUNX1, shallower barrier)
  vs adaptive memory (PAX5, deeper) read as a **two-timescale durability split** from a survival-based
  first-passage statistic (MFPT ratio ≈2.37, slow arm = deep barrier), tracking the measured γ ordering.
  Ordering + separation **[V]**; absolute lifetimes **[O]** (O-17).
- **III-3 Tolerance as the opposite sign.** ✅ **DONE (IM3).** The **sign** flips memory↔tolerance on the
  same switch — symmetric thresholds at the spinodal magnitude, **both** end-states held after the drive
  clears (hysteresis): the substrate of both vaccination and allergy desensitisation. Sign + held-basin
  **[V]**; absolute desensitisation dose/schedule **[O]**, clinical tolerance to clinicians (O-18).

## B.4 Track IV — RNA vaccines (engine/rna_vaccine.py → application)
The vaccine logic exists (V1–V5). Build the schedule science the application needs — all direction-only.
- **IV-1 Prime–boost interval, measured.** ✅ **DONE (v0.13.0 → engine/rna_vaccine_kinetics.py, VK1).** The
  prime–boost interval is swept in germinal-centre **rounds** (the IM1 GC loop reused unchanged) with decay at
  the **measured** escape rate: a genuine **interior optimum** (inverted-U in time) — too short under-matures,
  too long lets protection decay. Shape **[V]**; absolute days **[O]** (O-24).
- **IV-2 Durability-optimal re-boosting under a fixed budget.** Already sketched in V2/V3 — sharpen to a
  full **protected-fraction-over-horizon** sweep; the optimum interval ≈ measured protection half-life.
  Read the rule; absolute interval [O]. [V target].
- **IV-3 saRNA self-amplification vs mRNA.** ✅ **DONE (v0.13.0 → engine/rna_vaccine_kinetics.py, VK2).** saRNA's
  **longer same-amplitude drive window** crosses the protected (near-spinodal) basin **more reliably** than a
  shorter mRNA pulse (reachability ordering saRNA > mRNA), with the honest note that post-flip durability is the
  **identical** barrier — the advantage is in reaching, not holding. Ordering **[V]**; absolute titre **[O]** (O-25).
- **IV-4 Why a vaccine needs no edit.** Already V4 (payload transient, protection barrier-held). Generalise:
  contrast with a hypothetical SET-edit "vaccine" (irreversible, off-target risk) to motivate the drive
  route. [F/V].
- **IV-5 (open) Correlates of protection in absolute units.** Firewalled [O]; obstacle named (no
  substrate scale for titre→protection). Hand to clinicians/regulators.

> **STATUS (v0.13.0): Track IV COMPLETE on the simulation axis.** **IV-1 + IV-3 done (VK battery)**; IV-2/IV-4
> were already covered by V2/V3/V4; IV-5 is permanently firewalled. The interval-optimum shape and the
> saRNA>mRNA reachability ordering are read [V]; absolute days/titre are firewalled (O-24, O-25).

## B.5 Track V — Gene therapy (engine/gene_therapy.py → application)
The two levers + decision rule exist (GT1–GT4). Build out the lever map.
- **V-1 Lever A sub-types.** ✅ **DONE (v0.13.0 → engine/lever_map.py, LV1).** Knockout (γ→~0), base-edit (small
  δγ), prime-edit (larger δγ) all **move the threshold** (spinodal/barrier shift) and are not restorable by a
  drive (true SET edits); **CRISPRa** leaves γ untouched and is reversible, so the substrate **re-classifies it
  as Lever B**. SET-vs-drive + reversibility read **[V]**; absolute edit efficiency **[O]** (O-26).
- **V-2 Lever B sub-types.** ✅ **DONE (v0.13.0 → engine/lever_map.py, LV2).** siRNA (− drive), ASO splice-switch
  (an A4-**coordinate** change at fixed γ), saRNA (+ drive), miRNA-sponge (net + drive) all leave spinodal/barrier
  byte-identical and revert on withdrawal; the sign is read per sub-type. **[V]**; absolute dose **[O]** (O-26).
- **V-3 The decision boundary, measured.** ✅ **DONE (v0.13.0 → engine/lever_map.py, LV3).** With a declared
  absolute cap h_cap, the **boundary curve** h_path*(γ) = h_cap − spinodal(γ) **falls** with γ and crosses zero
  at a finite γ* = 3·(h_cap/2)^(2/3); beyond γ* even a zero-hold switch needs Lever A — confirmed by substrate
  settles on both sides and in the Lever-A-mandatory regime. Curve **[V]**; absolute cap **[O]** (reuses O-7).
- **V-4 Durable correction without an edit.** ✅ **DONE (v0.13.0 → engine/lever_map.py, LV4).** Re-dosing a
  Lever-B drive each cycle (a_{n+1}=(1−loss)a_n+w, loss measured from the switch's own relaxation) holds the
  corrected state above a critical re-write rate w* and fades below it — durable correction with **no SET edit**,
  γ never touched (the GE3 boundary applied therapeutically). Persistence condition **[V]**; absolute re-dose
  schedule **[O]** (O-27).
- **V-5 (open) Clinical efficacy / safety in absolute units.** Firewalled [O]; obstacle named. Hand to
  clinicians/regulators.

> **STATUS (v0.13.0): Track V COMPLETE on the simulation axis.** **V-1…V-4 done (LV battery)**; V-5 permanently
> firewalled. The lever sub-type bins, the drive signs, reversibility, the lever-choice boundary curve, and
> edit-free durability are read [V]; absolute efficiencies/doses/schedules are firewalled (O-26, O-27).
>
> **With Tracks I–V all closed on the simulation axis, the only remaining frontier is the (B) held-out
> validation (§B.9/§B.10). FV6 decomposes it: the γ-ordering class is non-identified (γ≈GC), the
> response-magnitude readout needs the firewalled Δh, and the corrective sign-law is the sole identified +
> firewall-clean crossing — open on bidirectional disease-correction data, not on Δh.**

## B.6 Cross-track seams (keep them honest)
- **The unifying claim:** SET (γ, genome) vs DRIVE (h, environment/RNA) is the *same* decomposition behind
  inheritance, immunity, vaccines, and gene therapy. Every track is a different operation on one switch.
- **Two carriers, two decay laws:** methylation (deep-barrier, persistent) vs RNA (re-written, transient)
  — keep this contrast visible in every transgenerational result.
- **Reversibility is the through-line:** a drive (RNA, vaccine, Lever B) is reversible; a SET edit (Lever A)
  is not. This single fact organises the therapeutic map.

## B.7 When to write (research-first)
This kit is **research phase** (`PHASE` = `research`). Do **not** produce a canonical site or paper until
the chosen batteries are green and the research is signed off (the upstream VP-SPEC research-first rule).
When a track matures and `reports/research_complete.json` is green for it, writing may be opened
deliberately under VP-SPEC v1.8 — English body, per-title HTML, every quantitative result reproduced
(2×sha256), every [O] reasoned. Until then: measure, grade, keep the gate green, hand forward one zip.

## B.8 Definition of done (per increment)
An increment is done when: (1) the new battery is **measured out of the substrate** (not asserted), (2) it
carries a **grade** and any [O] is in the ledger with its obstacle, (3) the **anchor still reproduces** and
no measured γ changed, (4) `python repro/run_all.py` is **all_green**, (5) the docs are updated (CHANGELOG,
COMPLETION_LEDGER), and (6) it ships as **one additive zip**. No increment is done if it regressed a prior
result or introduced a magnitude past the firewall.

## B.9 Feasibility — the (A) map vs (B) validation split (and the autism / brain-cell extension)
**Status:** the map side ships as the **FM** battery (v0.7.0, `engine/rna_feasibility_map.py`); the
validation side (B) is the named open research direction below. This section governs every "does putting RNA
in actually change the cell?" question and must be inherited before any such work.

**The question and why a self-contained sim cannot answer it.** "Does RNA actually change the cell?" reduces
to the size of the drive the RNA supplies, Δh. But Δh (= dose/size) is exactly an **[O]** quantity behind the
magnitude firewall — the substrate fixes *which* switch and the *sign*, never the absolute drive. So the
yes/no rides on the one number we have pinned as unprovable, **and** the R19 dynamics is itself an assumption:
the answer is **doubly** undecidable self-contained. What a self-contained sim *can* deliver is a **map**: for
a given drive, **which** switch is reachable, the **ordering**, and whether it is **reversible**. Pushing a
drive past the spinodal flips the switch *by construction*, so a "flipped" screen is the **replay of the Δh
assumption, not a discovery**. (FM4 encodes this as a checkable invariant: a flip exists at k≥1 for every
measured switch and at no k<1, so the screen is a function of the assumed k alone and carries zero
discriminating information about a real cell.)

**The same engine becomes two completely different objects:**
- **(A) Map demo** — real promoter → γ emerges → R19 switches → inject RNA as a signed drive at the A4
  coordinate (siRNA → OFF / saRNA → ON) → integrate the dynamics → flip / ordering / reversibility. Direction,
  geometry, ordering, and reversibility come out legitimately **[V]**. Easy to build; it demonstrates the
  model's logic; it is **not** proof that "this cell changes." (This is FM1–FM3.)
- **(B) Validation test** — take **held-out** pre/post expression data from cells actually treated with
  siRNA/saRNA (data not used in construction) and **score** whether the model's predicted flipped-switch
  **set + ordering** matches the measured changed genes. Only this contrast (prediction vs measurement)
  crosses the line from "re-description" to "finding." **This is the open work.**

**The "make it as realistic as possible" trap.** The *inputs* can be made genuinely real (real γ, real RNA
targets, real cell promoters) and the circularity still does not break — only (B)'s scoring breaks it. And the
moment Δh or any parameter is **fitted to the target** to "match," the no-tuning invariant (A.2) is violated
and (B) becomes self-deception. The only honest path is **no-tuning prediction → score on held-out data**.
In short: (A) and (B) are nearly the same engine; the sole difference is **whether a scoring sheet (measured
data) exists.** Either way the target system (which promoter + which RNA) must be fixed first.

**The autism / brain-cell extension (FM2, measured).** The map transfers structurally to neurodevelopmental
biology: the autism-spectrum atlas `inherited/neuro_gamma.json` (MECP2, FMR1, SHANK3, CHD8, NRXN1, NLGN3,
PTEN, TSC2, SCN2A, SYNGAP1 — declared **by function** from SFARI monogenic ASD genes, measured through the
identical SOX9-anchor-gated pipeline) shows every ASD promoter is an **R19-bistable** switch and the
flip-drive ordering tracks the measured γ (SCN2A shallowest → PTEN deepest). So "would brain cells like autism
work?" → **in the (A)-map sense, yes**: the same reachability/ordering/reversibility structure holds on real
ASD promoters. Whether a given RNA dose changes a given neuron remains **[O]/(B)**.

**Next research (B), no-tuning:** pick one ASD target with public held-out perturbation data — e.g. an
ASO/siRNA knockdown or saRNA up-regulation series on a neuronal line for one of the FM2 genes — predict the
flipped-switch set + ordering from the **measured** γ (and A4 coordinate) with **no** parameter fitting, then
score precision/recall of the predicted changed-gene set and the rank-correlation of the ordering against the
measurement. Report it as it falls (honest negatives included). Until that score exists, FM stays a map, not
a claim.

> **STATUS (v0.12.0): the (B) ORDERING score is RUN (FV) and NULL, and is now STRESS-TESTED to be
> NON-IDENTIFIED (FV5).** Scored on **held-out** Replogle 2022 CRISPRi knockdown depth (DOI
> 10.1016/j.cell.2022.05.013), union-of-seven panel, primary K562 genome-wide n=43: sign-locked prediction
> ρ(γ, on-target `fold_expr`) > 0 came out **ρ = −0.0760, p = 0.6283** (slightly opposite, non-significant
> across every cutoff, sign disagrees on RPE1, SET-proxy AUC 0.389). γ was **re-read frozen** and
> hash-checked; nothing tuned. **FV5 then stress-tested the GC confound:** γ = −mean(NN ΔG37) tracks promoter
> GC **by construction** (ρ(γ,GC) = 0.99/0.98/0.96 on the three panels), and CRISPRi efficiency is itself a
> GC/accessibility phenomenon — so after partialling GC the γ effect is non-significant and sign-unstable
> (+0.13/−0.22/−0.43, all p ≥ 0.40). The knockdown-depth ordering score therefore **cannot separate barrier
> from GC** — the null is *non-identified*, not *signal-absent*. Per the promotion rule it **promotes
> nothing** — O-19/O-20 stay `[O]`, FM stays a map `[V]`; consistent with FM4. **Consequence for the
> neuronal (B):** γ↔GC collinearity is a promoter-DNA property (cell-type invariant), so repeating the same
> knockdown-depth observable on neuronal data (e.g. i³Neuron CRISPRi CROP-seq, Tian 2019, GEO `GSE124703`;
> CRISPRbrain — *the data exist; the test is degenerate*) inherits the identical non-identification and does
> **not** advance O-20. **Still genuinely open:** an **identified** neuronal (B) (a downstream
> RESPONSE-MAGNITUDE readout, which needs the firewalled Δh) and the **SET-membership precision/recall** (also
> needs an operating Δh). See `engine/feasibility_validation.py`, `bvalidation/`, and the ledger's "(B)
> validation" section. Any further (B) is additive; γ stays frozen; FV5 added only analysis (cache unchanged).
>
> **UPDATE (v0.15.0, FV6 — the (B) frontier PARTITIONS):** FV5's non-identification is now shown to be a
> *class* property, not a one-off. Measured on the disease panel, ρ(γ,GC)=0.9944 and R²(γ~GC)=0.9948 — so
> **every γ-ORDERED prediction** (reachability/knockdown-depth/durability/correction-difficulty ordering) is
> non-identified for the same reason, and re-running any of them as an ordering score adds nothing. The single
> exception is the **mechanism corrective-SIGN**: point-biserial(sign,GC)=+0.0153 (R²=0.0002 — a ≈4974×
> separation from the γ↔GC axis), so the sign is **orthogonal to the GC confound**, and because a sign test
> reads only WHICH sign corrects (never a dose) it is also **firewall-clean**. So within §B.9 the only (B) that
> is *both* identifiable and firewall-clean is the corrective sign-law (developed in §B.10); its obstacle is
> **bidirectional disease-correction DATA**, not the Δh. (Reproduces DM2's point-biserial(sign,γ)=−0.0148
> frozen; promotes nothing — O-19/O-20/O-22 stay `[O]`.)


## B.10 Disease-class feasibility — inheriting from the sibling vp-site program (DM, measured)
**Status:** ships as the **DM** battery (v0.8.0, `engine/disease_feasibility_map.py`) with two measured atlases
`inherited/onco_gamma.json` and `inherited/neurodegen_gamma.json`. This section governs every "could we correct
disease X with the RNA/edit lever?" question and extends §B.9 from the carrier/ASD class into the disease class.

**Inherit by re-measuring, never by importing.** The sibling `vp-site` program curates ~90 monogenic-disease
promoters (`repro/disease_kit/diseases/*/analysis.json`) measured through the **identical** TSS−2000..+500 /
SantaLucia-NN-ΔG37 / GRCh38 pipeline, each tagged with gene role (brake/driver), mechanism (GOF/LOF), and a
perturbation direction — under the same magnitude firewall. The discipline (A.2) forbids copying their γ.
Instead: re-declare the panel **by function**, re-measure through *this* kit's SOX9-anchor-gated fetcher, and
let the loci the two programs share become a **no-tuning cross-package check**. Four shared loci (PTEN, VHL,
SOD1, HTT) reproduce to 4 decimals — the strongest available evidence that the measurement is anchor-determined,
not program-determined. That agreement is **reported, never tuned to** (DM4 asserts it as an invariant).

**The disease-class content FM did not have — the corrective-sign law.** §B.9 mapped reachability/ordering/
reversibility but was sign-agnostic about *purpose*. Disease adds a forced correction direction, **orthogonal**
to γ:
- a **loss-of-function** lesion (tumour suppressor knocked out; recessive PD gene) → corrected by a **`+`**
  (restore / up-regulate) drive;
- a **gain-of-function** lesion (oncogene; dominant toxic-GOF PD gene; the proteinopathy bridge) → corrected by
  a **`−`** (knock-down / silence) drive.
The sign is set by **mechanism, not depth**: suppressors and oncogenes interleave along the γ-ordering
(point-biserial ≈ −0.015). DM2 verifies the mechanism-forced sign drives each gene out of its pathological
basin while the opposite sign from the *same* basin does not. This is **[V]** as a sign law; the absolute
corrective dose is **[O]** (O-21).

**The two-lever decision (DM3) is the firewall made operational.** A reversible **Lever-B** (RNA-style transient
drive at the A4 coordinate) is reachable for every measured promoter switch, and the required drive grows with
γ; **Lever-A** (a permanent edit) is reserved for **coding-SET** lesions — where the pathology is in material
the environment cannot write (the promoter γ itself), which is exactly the firewall boundary, not a therapeutic
recommendation. The rule (drive-reachable → Lever-B; SET-level lesion → hand to clinicians) is **[V]**; the
tolerability cap's absolute value stays **[O]** (O-7 logic).

**(B) — the open disease validation, no-tuning.** Identical shape to §B.9's (B): pick one disease gene with
public **held-out** perturbation data — an ASO/siRNA knockdown of an oncogene or toxic-GOF PD gene, or a
restore/saRNA up-regulation of a suppressor — predict the corrected-switch **set + ordering + sign** from the
**measured** γ (and A4 coordinate) with **no** parameter fitting, then score precision/recall of the predicted
corrected-gene set and the rank-correlation of the ordering against the measurement. Report as it falls (honest
negatives included). The per-patient corrected-yes/no (O-22) is promoted **only** by such a score; until it
exists, DM stays a map, not a claim, and all clinical translation is firewalled to clinicians and regulators.

> **STATUS (v0.12.0): the ORDERING axis is scored (FV), is NULL, and is NON-IDENTIFIED (FV5); the corrective
> SIGN-law is NOT yet scorable here.** The disease genes participate in FV's union-of-seven panel, and the
> γ-ordering vs held-out CRISPRi knockdown depth is the same recorded NULL (ρ=−0.08, p=0.63) — so **O-22 stays
> `[O]`** (promotes nothing) and DM stays a map `[V]`. **FV5 sharpens *why* the ordering axis is uninformative
> here too:** γ tracks promoter GC by construction (ρ(γ,GC)≈0.99) and knockdown depth is GC/accessibility-
> driven, so partialling GC leaves no identified γ signal — the disease-gene knockdown-depth ordering is
> *non-identified*, not merely under-powered, and a neuronal/other-line knockdown panel inherits the same
> degeneracy. **Why the sign-law (DM2) is still open (unchanged):** Replogle CRISPRi is a *knockdown* screen in
> a leukemia line — **not a disease-correction context** — so it cannot test LOF→`+`restore / GOF→`−`silence
> corrective signs. That needs **disease-vs-normal corrective** pre/post data (patient-derived cells, a restore
> arm) — a readout whose magnitude is the firewalled Δh. Such work is additive; γ stays frozen and re-read,
> never tuned.
>
> **UPDATE (v0.15.0, FV6 — corrects the obstacle for the sign-law (B)):** the clause above that the sign-law
> "needs a readout whose magnitude is the firewalled Δh" is **too strong** and is hereby corrected. A
> *corrective-sign* test reads only **WHICH** sign restores the healthy switch (LOF→`+`, GOF→`−`), never a dose
> or Δh, so it is **firewall-clean by construction**. FV6 also shows it is **identified**: on the disease panel
> the sign axis is orthogonal to the GC confound that sinks the ordering axis — point-biserial(sign,GC)=+0.0153,
> R²=0.0002, vs ρ(γ,GC)=0.9944 (a ≈4974× separation) — so a held-out sign-match could **not** be manufactured by
> GC. Therefore the corrective sign-law is the **unique (B) crossing that is both identifiable and
> firewall-clean**, and its **only** obstacle is **bidirectional disease-correction DATA**: an oncogene `−` arm
> *and* a suppressor/PD-gene `+` arm scored together (a single-arm screen like Replogle cannot exhibit the
> interleaving). This is a data question, **not** a Δh question. O-22 stays `[O]` (data-blocked); FV6 promotes
> nothing and tunes nothing (γ re-read frozen; reproduces DM2's point-biserial(sign,γ)=−0.0148).
>
> **UPDATE (v0.17.0–v0.18.0, FV7 + FV8 — the bidirectional data obstacle is now CLEARED, and O-22's obstacle
> moves from data to the firewall):** the "data question" above is now **answered on both arms**. FV7 (v0.17.0)
> scored the **`−` arm** on held-out DepMap CRISPR-**KO** (a knockout *is* the `−` operation; in a cancer line
> viability *is* a correction phenotype): GOF oncogenes are dependencies and LOF suppressors are not —
> point-biserial(GOF, −gene_effect)=+0.4940, exact p=0.0227 (n=16 onco), identified (point-biserial(sign,GC)=−0.1222,
> GC-partialled +0.4939 unchanged), firewall-clean. FV8 (v0.18.0) scored the **`+` RESTORE arm** on held-out
> Horlbeck 2016 **CRISPRa** (an activation *is* the `+` operation; cancer growth *is* its correction phenotype):
> LOF suppressors are growth-suppressive on activation and GOF oncogenes are not — point-biserial(LOF,
> −growth_phenotype)=+0.4852, exact p=0.0274 (n=16 onco), identified (point-biserial(sign,GC)=+0.1222,
> GC-partialled +0.4731 unchanged), firewall-clean. With **both arms** scored the corrective sign-law is now
> **bidirectionally `[V]`** (direction-only), which **removes in full** the bidirectional-DATA obstacle named
> above. **But O-22 STILL stays `[O]`**, and FV8 **corrects** FV7's "obstacle narrows to the `+` arm alone"
> framing: with both arms in, O-22's residual obstacle is **no longer data — it is the firewall itself**. The
> sign-law is **class-level + direction-only** (which way to push each disease class); O-22 is a **per-patient,
> absolute** outcome that needs the firewalled per-patient magnitude/penetrance — the absolute drive size being
> the separate item **O-21**. A direction-only law cannot certify a per-patient yes/no, and promoting O-22 would
> leak direction-only `[V]` into per-patient absolute `[V]` (a firewall breach). This is **not** a contradiction
> of FV6 (the sign-law needed bidirectional data, not Δh — both arms scored with **zero** Δh). γ untouched;
> nothing tuned. **No simulation-axis (B) item remains open; what remains for O-22/O-21 is the firewall, by
> design.**

**Scope note (deliberate sampling, not coverage).** ONCO (16) and NEURODEGEN (9) **sample** the disease classes
named for this increment; they are not an attempt to cover medicine. The fetcher's by-function declaration plus
the anchor gate make extension a matter of adding a function-declared panel and re-running — never of tuning.
