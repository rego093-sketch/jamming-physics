# CHARTER — Reproductive and Gonadal-Endocrine Emergence: the HPG Oscillator, the Menstrual Cycle, and Hormone-Driven Cancer

**paper_id:** `reproductive_endocrine_vp_site`  ·  **code:** `rep`  ·  **branch:** jamming (hormonal-cycle / germline)  ·  **version:** 0.6.0-writing

## Scope (one line)
Gonads, the gonadal-endocrine (HPG) axis and the germline emerge on the substrate; the menstrual cycle is a slow relaxation oscillator, hormone feedback is a switch, and sex hormones act as the sustained drive in hormone-driven cancers. Brain-facing HPA stays in mind (firewall); this package owns the gonadal axis only.

## What this package emerges and circulates
Like the mind package, this package **emerges its organs by simulation and circulates their dynamics**
— at the level of physical MECHANISM, not felt experience. Organ *identity* and *developmental order*
are owned by the DNA morphogenesis gene-clock and CITED here (measured γ, never fitted). Organs whose
γ is not yet in the DNA atlas are listed as honest **to-measure** inputs (fetch via the same pipeline)
— deferred, not invented.

### Organs
- **gonad_testis** (`SOX9`) — γ=1.4598 (vendored, measured [V]) — testis determination (SRY->SOX9) + Sertoli/spermatogenesis support — *dyn:* germline-support — *rate anchor:* testis determination [V]
- **gonad_ovary** (`FOXL2`) — γ=1.4829 (received, measured [V]) — ovarian determination + folliculogenesis (menstrual oscillator) — *dyn:* oscillator — *rate anchor:* menstrual cycle ~28 d [L]
- **germline** (`DAZL`) — γ=1.3803 (received, measured [V]) — gametogenesis (meiotic program) — *dyn:* germline — *rate anchor:* spermatogenic cycle timing [L]
- **reproductive_tract** (`WT1`) — γ=1.5182 (received, measured [V]) — gonadal / tract scaffold — *dyn:* structural — *rate anchor:* scaffold

**γ reception (v0.3.0):** FOXL2 / DAZL / WT1 were formerly TO-MEASURE; they are now received via the identical
DNA `fetch_morpho_gamma` pipeline (`repro/_gamma/fetch_gamma.py`: NN-stacking ΔG37, SantaLucia 1998, on the
cited proximal promoter TSS-2000..+500, GRCh38). Sequences are cached (`inherited/organ_promoters.cache.json`)
so γ reproduces offline bit-for-bit; the pipeline is accepted only because it reproduces the vendored SOX9
anchor (γ=1.4598, GC=0.545). Measured input, never fitted. Developmental order (γ ascending): germline →
gonad_testis → gonad_ovary → reproductive_tract [V].

## Physical-class boundary (why these organs are one package)
Decomposition is by **physical regime / coupling topology**, not textbook organ-system labels. This
package is the **jamming (hormonal-cycle / germline)** class. Anything outside that class belongs to a sibling package and
is reached only through the cited seam variables — never re-emerged here (SSOT).

### Seams IN (inherited / cited)
- mind/neuro: GnRH pulse-generator neural edge (CITE, do NOT re-emerge; mind owns brain-facing HPA, this owns the gonadal HPG response)
- DNA: organ identity + emergence order [V]
- substrate: FHN/R19 (vendored)

### Seams OUT (this package is SSOT for these; siblings cite them)
- sex-hormone levels (systemic; this package is SSOT)

## Discriminant targets (must pass before writing)
- T1 HPG pulse: GnRH pulse -> LH/FSH (the gonadotropin pulse generator as an FHN oscillator) [V], rate [L]
- T2 menstrual cycle: follicular->luteal as a slow relaxation oscillator, ~28 d period [V], period [L]
- T3 hormone feedback switch: estrogen negative feedback + the mid-cycle LH-surge positive feedback (a switch) [V]
- T4 spermatogenic cycle: cycle timing / period from the substrate [V]
- T5 puberty onset: gonadotropin reactivation as a threshold crossing [V]

### Germline / gamete battery (G1–G6) — the germ cell itself (added v0.5.0)
The organs and rhythms above never opened the gamete. The `repro/_germline/` module answers the four germ-cell
questions on the same substrate (R19 switch + FHN oscillator), with **measured gamete-program promoter γ**
(13 genes, identical DNA pipeline, panel declared by function before γ seen, persisted only because SOX9 **and**
DAZL anchors reproduce) as the only new input. Folded into the research gate via `stress_tests`; the hashed core
is unchanged.
- G1 how a gamete is made: meiosis = one replication + two **ordered** divisions (reductional→equational), the
  order forced by two-stage REC8 cohesin release (shugoshin protection sign, not tuned) [V]
- G2 are gametes identical? **No** — independent assortment 2²³ + crossover interference modelled as the
  substrate refractory period mapped onto the chromosome axis (sub-Poisson, obligate CO); diversity floor 10⁴⁷ [V]
- G3 sperm motility: the flagellar beat is the **fast** end of the relaxation-oscillator ladder; CatSper Ca²⁺ is
  the gain switch driving hyperactivation (bigger **and** slower beat) [V]; the 9+2 axoneme integer [O]
- G4 egg logic: metaphase-II arrest = a switch **held** by cytostatic drive; fertilisation = a one-way
  supra-spinodal flip; the polyspermy block = past-spinodal irreversibility [V]
- G5 gamete-program γ atlas + a **pre-registered** module-separation test (reported as it falls, **null
  permitted**); only the tight recombination-core cluster is claimed [V on the narrow claim]
- G6 the sperm/egg **duality**: one substrate → a free oscillator (sperm) vs a held switch (egg); symmetric (4
  sperm) vs asymmetric (1 egg + 3 polar bodies) → anisogamy [V]/[L]; the evolutionary "why" [O]

### Embryo battery (E1–E6) — fertilisation → fetus (added v0.6.0)
The gamete battery made the two germ cells but stopped at the gamete. The `repro/_embryo/` module carries the
story to a fetus: the two gametes **meet**, a genome **emerges**, and a body plan is **built** — each step a
discriminant against the same substrate, reusing G1–G6 and adding **measured developmental master-gene γ**
(17 genes, identical DNA pipeline, panel declared by developmental stage/HOX position before γ seen, persisted
only because SOX9 **and** DAZL anchors reproduce) as the only new input. Folded into the research gate via
`stress_tests`; the hashed core is unchanged. (Human is treated **conceptually** — a γ-based gene-clock, not
whole-genome synthesis.)
- E1 syngamy + **DNA emergence**: the sperm (oscillator) delivers a supra-spinodal Ca²⁺ kick that flips the
  egg (held switch) one-way (polyspermy block holds); two haploid pronuclei fuse, restoring diploidy
  (1N+1N→2N), and the new genome is unique to a floor of 10⁹⁴ (the square of the gamete floor) [V]
- E2 cleavage: 2ⁿ **symmetric** divisions (vs oogenesis 1+3) with cytoplasmic mass **conserved** (cleavage ≠
  growth); the inner-cell-mass vs trophectoderm decision is one R19 bistable switch [V]
- E3 ZGA: the maternal-to-zygotic transition as a **one-step spinodal crossing** (genome OFF on maternal stores
  ZAR1/NLRP5 → ON past the spinodal); the handoff from the gamete program this package owns to the embryo's own
  genome [V]
- E4 the **gene-clock** builds the body: emergence order = argsort(spinodal(γ)); a **pre-registered** stage
  test (γ rises pluripotency<germ-layer<organ) is SUPPORTED (Spearman ρ≈0.55, p≈0.02); a HOX 3′→5′ colinearity
  test is reported as a partial result (null permitted). **Firewall:** the gene-clock law + the full-body atlas
  are the DNA 4D-Blueprint package's SSOT, cited here — this is a measured demonstration [V on the demonstration]
- E5 the whole arc: one specific sperm + one specific egg → syngamy → cleavage → ZGA → gene-clock body plan → a
  fetus (unique genome, ICM-derived), end-to-end and deterministic [V]
- E6 honest scoreboard + firewall restated: [V] events/order; [L] measured γ + structural anchors; [O] absolute
  gestational timing (as pubertal age) and the full-body atlas (DNA SSOT)

### Fertility battery (F1–F6) — infertility vs subfertility (added v0.7.0)
The embryo battery built a fetus when every operation succeeded. The `repro/_fertility/` module asks what
happens when one does **not**, and draws the clinic's distinction in substrate terms — no new γ (it reuses the
gamete-machinery γ and the oncology chapter's `exp(−ΔV/D)`):
- F1 conception is an **AND** of substrate operations (HPG pulse → … → gene-clock); one gate below threshold is
  sterility [V]
- F2 **the central claim**: **infertility = an operation past a spinodal** (categorical, per-cycle p=0, a
  sub-threshold drive does nothing) vs **subfertility = an operation near its threshold** (a finite Kramers
  crossing rate the same drive moves exponentially — 1.56× vs exactly 0) [V]
- F3 male factor = oscillator **throughput** (azoospermia = the switch off; count/motility = beat rate 51→7) +
  the CatSper hyperactivation gate [V]
- F4 female factor = the ovulation surge switch + **REC8 cohesin fatigue** (mis-segregation rises 0.121→0.752
  across maternal age 25→45 as the held barrier decays); POI = early latch loss [V]; absolute fraction [O]
- F5 treatment as a **drive**: the hCG trigger (a supra-spinodal kick), pulsatile GnRH (oscillator restart),
  ICSI/IVF (gate bypass) [V]/[L]
- F6 honest scoreboard + firewall: clinical management of a real couple belongs to clinicians

### Sex-ratio battery (S1–S6) — sex determination + sex-ratio distortion (added v0.7.0)
How a gene biases offspring toward one **sex**. The `repro/_sexratio/` module adds **measured sex-determination
master-gene γ** (6 genes, identical DNA pipeline, panel declared by axis before γ seen, persisted only because
SOX9 **and** FOXL2 anchors reproduce):
- S1 sex itself = the **SOX9↔FOXL2 mutual-antagonism R19 bistable** (SRY a transient supra-spinodal drive that
  then holds; adult transdifferentiates only supra-spinodal) [V]
- S2 Mendelian 50:50 = that switch **untilted** — a fair coin (ensemble 0.4983) [V]
- S3 meiotic drive = a **tilt** (graded distortion 0.86 below the spinodal → fixation 1.0 above; t-haplotype/SD
  limit) [V]
- S4 sex-ratio distortion = the same tilt **with a sign** — a sex-chromosome-linked gamete-killer (X-shredder →
  1.0 male; Y-killer → 0.0 female; one mechanism, two signs) [V]
- S5 Fisher's principle — the **population** sex ratio 1:1 is a stable attractor (human SSR ~0.512 is a small
  residual, not strong drive) [V]
- S6 sex-determination γ atlas (SRY 1.2550 outlier … WNT4 1.5992) + a **pre-registered** axis-separation test
  reported as it falls (**null**: permutation p=0.10, not significant at n=3/axis) [V on the test]

## Domain diseases + oncology scope (carcinogen → incidence)
Covers this physical class's diseases; the carcinogen-exposure mechanism (how much MORE cancer with
exposure) uses the shared R19 kernel (barrier-lowering → Kramers crossing → RR(dose)) with per-site
CITED epidemiological anchors. Grades: anchor [L] / dose-response shape [V] / absolute incidence [O].
- **breast carcinoma** ← cumulative estrogen exposure (HRT, early menarche); ionizing radiation
  - anchor/grade: estrogen-exposure RR (HRT cohorts) [L]; hormone as sustained drive [V]
- **cervical carcinoma** ← HPV infection x co-factors (smoking)
  - anchor/grade: HPV infection x carcinogen synergy RR (like H. pylori/gastric) [L]; synergy [V]
- **prostate carcinoma** ← androgen exposure; age
  - anchor/grade: androgen-driven; absolute RR less clean -> honest [O]; shape [V]

## Governance
- VP-SPEC v1.8 (full text in `VP_SPEC_v1_8.md`) governs the writing phase and C1/C3 in research.
  Constitution (C0) overrides any clause on conflict.
- **Research-first:** writing (`tools/build_docs.py`) locked until the stress battery is green and
  research signed off (START_HERE §5).
- **Canonical artifact:** per-title HTML in `docs/` (C2/C4). HTML is canonical. Body in English (C0).
- **Single deliverable + auto-handover:** one zip; START_HERE → CHARTER is the entire bootstrap; state
  passes by files only, next session resumes from the single zip (C0, §1, §5).
