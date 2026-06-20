# CHANGELOG — Reproductive / Gonadal-Endocrine (`reproductive_endocrine_vp_site`)

> 모든 버전 증가마다 4-문서 SSOT(CHANGELOG / MASTER_MANUAL / COMPLETION_LEDGER / HANDOVER)를 함께 갱신한다.
> 기술 내용은 영어, 항해(navigation)는 한국어. 등급 어휘([V]/[L]/[F]/[O])는 정직성 표기이며 자기비하가 아니다.

---

## v0.7.1-writing — distribution sync: the whitepaper now carries §13 (infertility/subfertility) and §14 (sex determination & sex-ratio distortion)

**One line:** v0.7.0 wrote the two new theses as canonical **HTML** chapters §13/§14 (C2) but left the PDF
whitepaper at its v0.6.0 body (gamete + embryo only) — a tracked open item. v0.7.1 closes it: `tools/build_paper.py`
is extended with two new LaTeX section generators that pull every number **live** from the `_fertility` and
`_sexratio` batteries, so the PDF can no longer drift from the engine. **No science changes** — the hashed
research core is identical (`f849da7d…`); this is a writing/distribution-layer increment only, exactly as v0.4.1
was for the initial Zenodo prep.

### Changed — `tools/build_paper.py` (registry extended to §13/§14)
- `gather()` now also imports `infertility` + `sex_ratio` and folds `run_fertility_battery()` /
  `run_sexratio_battery()` (+ the measured sex-determination γ atlas) into the build dict `D`.
- **`sec_infertility(D)`** (new) — the chain-AND of 8 verified operations; the central spinodal/Kramers
  dissociation as a table (subfertile `0.0391→0.0610`, **1.56×**, year `0.381→0.530`; sterile `0/0/—`, the same
  nudge moving one exponentially and the other not at all); male/female factor (azoospermia=switch OFF;
  `51→7` beats; CatSper γ `1.4019`; REC8 γ `1.4525`; age mis-segregation `0.121→0.752`); treatment-as-a-drive
  (`41` vs `0` pulses, hCG kick, ICSI/IVF bypass). All numbers live; grades [V]/[L]/[O] preserved.
- **`sec_sexratio(D)`** (new) — the SOX9 (`1.4598`)↔FOXL2 (`1.4829`) bistable, SRY-as-transient drive with
  hysteresis; Mendel as an untilted switch (`20,000` meioses → `0.4983`, analytic `0.5`); drive-as-tilt
  (`0.50→0.8623→1.0`); the **signed** sex-ratio skew (X-shredder `1.0` male, Y-killer `0.0` female, partial
  `0.8223`); Fisher's 1:1 attractor (`0.5125` bounded shift; human `0.512` residual); the measured γ atlas as a
  table (axis-labelled) + the **pre-registered axis-separation null** (ovary `1.5163` > testis `1.3857`, gap
  `0.1306`, permutation **p = 0.10**), reported honestly.
- **`sec_open(D)`** extended with five new [O] rows (each with its obstacle, VP-SPEC C3): absolute per-cycle
  conception probability; per-age aneuploidy fraction; meiotic-drive/sex-ratio tilt magnitude; cause of the
  human ~0.512 ratio; axis separation of sex-determination γ at n=3.
- Abstract extended with one downstream-arc sentence (gamete → embryo → infertility/subfertility → sex
  determination/sex-ratio); keywords extended; **Fisher 1930** added to the bibliography (`{9}`→`{10}`).

### Result
- `paper/reproductive_endocrine_vp.tex` **37,656 → 47,476 chars**; **`\today` still never used** → `.tex`
  **byte-identical across two builds** (sha `3d5f5c64…`). Title page reads **Version 0.7.1-writing**, concept
  DOI `10.5281/zenodo.20754657` unchanged.
- `paper/reproductive_endocrine_vp.pdf` recompiled **clean** (`pdflatex`/`latexmk`, **0 unresolved
  references/citations**), **12 → 15 pages**, A4. New §13/§14 and Tables 11–12 render; the extended open-quantities
  table (Table 13) carries all twelve [O] rows.
- Research gate unchanged: `python repro/run_all.py` → **ALL_GREEN: True**, determinism `f849da7d…` (2× identical),
  WRITING UNLOCKED. HTML site (`docs/`) is **untouched** — it embeds no package version string, so the §13/§14
  chapters and the 105/105 writing-gate stand exactly as in v0.7.0. HTML remains canonical (C2); the PDF is now
  a faithful, drift-proof mirror of it.

---

## v0.7.0-writing — infertility vs subfertility (F1–F6) + sex determination & sex-ratio distortion (S1–S6) + measured sex-determination γ + chapters §13, §14

**One line:** v0.6.0 built the **embryo** (E1–E6). The user asked for two new, **separate** HTML parts: why
conception **fails** (불임/난임), and how a gene makes offspring lean one **sex** (성별 쏠림). v0.7.0 adds two
new modules — `repro/_fertility/` and `repro/_sexratio/` — each a discriminant battery against the same
vendored R19 switch + FHN oscillator, **reusing** the gamete/embryo/therapy results and adding **measured
sex-determination master-gene promoter γ** (6 genes, received through the identical DNA pipeline) as the only
new input. Two six-target batteries (F1–F6, S1–S6) all **PASS**, are wired into the research gate, and are
written up as canonical HTML **chapters §13 and §14** with ten new display equations. The hashed research core
is **unchanged** (`f849da7d…`): both batteries are additional discriminant layers folded into
`research_gate()`, science-neutral to the `circulate()` core.

### The two new theses
- **Infertility vs subfertility is a spinodal, not a slider.** The reproductive arc is an **AND** of substrate
  operations; **infertility (sterility)** is an operation on the **wrong side of a spinodal** — categorical,
  deterministic, per-cycle probability exactly **zero**, and a sub-threshold drive does nothing.
  **Subfertility** is an operation **near its threshold** — a small-but-finite **Kramers crossing rate** per
  cycle, so the **same drive** that does nothing across a spinodal moves it **exponentially**. Same physics
  (R19 spinodal + the oncology chapter's `exp(−ΔV/D)`), two failure classes.
- **Sex is a tilted switch; a drive gene tilts the coin.** Mammalian sex is the **SOX9↔FOXL2** mutual-
  antagonism **R19 bistable** (SRY the tipping drive, hysteresis the lifelong maintenance). **Mendelian 50:50**
  is that switch **untilted** — a fair coin. **Meiotic drive** is a **tilt**: transmission climbs from ½ and,
  **past the spinodal, fixes near 1**. **Sex-ratio distortion** is a sex-chromosome-linked gamete-killer — the
  **same tilt with a sign** (X-shredder → male-biased; Y-killer → female-biased). **Fisher's** restoring force
  keeps the **population** at 1:1.

### Added — `repro/_sexratio/fetch_sexratio_gamma.py` (measured sex-determination γ reception)
- Same NN-stacking ΔG37 pipeline (SantaLucia 1998, promoter TSS−2000..+500, GRCh38.p14) as the organ, gamete
  and developmental masters. The 6-gene panel was declared **by sex-determination axis before any γ was seen**
  (testis: SRY/SOX9/DMRT1; ovary: FOXL2/RSPO1/WNT4). No-tuning gate: refuses to persist unless **both** anchors
  reproduce — SOX9 (1.4598) and FOXL2 (1.4829). Writes `inherited/sexdet_promoters.cache.json` +
  `inherited/sexdet_gamma.json`; offline `verify()` recomputes γ from cache, network-free and bit-for-bit.
- **Measured sex-determination γ atlas (ascending):** SRY **1.2550** (AT-rich outlier) · DMRT1 1.4423 ·
  SOX9 1.4598 · RSPO1 1.4669 · FOXL2 1.4829 · WNT4 1.5992. Testis-axis mean 1.3857, ovary-axis mean 1.5163.

### Added — `repro/_fertility/infertility.py` (the F1–F6 fertility battery)
| target | claim | key numbers | grade |
|---|---|---|---|
| **F1** | conception is an **AND** of substrate operations; one broken link → sterility | 8-link chain (HPG pulse → … → gene-clock); any single gate at 0 ⇒ conception 0 | [V] / [F] / [O] per-link rates |
| **F2** | **infertility = past a spinodal (categorical); subfertility = near-threshold Kramers** | subfertile p/cycle 0.039 → 0.061 under a fixed nudge (**1.56×**), p/yr 0.38→0.53; sterile (deficit 1.6·h_sp) p=**0**, same nudge → still **0** | [V] dissociation / [L] fecundability+D / [O] absolutes |
| **F3** | male factor = oscillator **throughput** (off=sterile, weak=subfertile) + CatSper gate | azoospermia = R19 switch **off** (sub-spinodal); throughput 51 → 7 beats as recovery slows; CatSper (γ 1.4019) a separate supra-spinodal gate | [V] / [L] WHO count / [O] param→drive map |
| **F4** | female factor = ovulation **surge switch** + **REC8 cohesin fatigue** | anovulation = surge switch off; mis-segregation rises **0.121 → 0.752** across age 25→45 (held barrier γ²/4·cohesin decays); POI = early latch loss | [V] / [L] REC8 γ + age-aneuploidy anchor / [O] absolute fraction |
| **F5** | treatment = a **drive**: kick / restart / bypass | hCG = supra-spinodal kick; pulsatile GnRH restart (41 vs 0 pulses, cited from §9); ICSI/IVF = gate bypass | [V]/[L] retrodictions / [O] schedules |
| **F6** | honest scoreboard + firewall | verified logic / anchored magnitudes / open absolutes; clinical management firewalled | [V] |

- Constants set **once** (SELECTION_TEMP_D=0.25, FECUNDABILITY_MAX=0.20, SUBFERTILE_DEFICIT=0.85·h_sp), never
  tuned per target. Deterministic (SEED=19), byte-identical across runs.

### Added — `repro/_sexratio/sex_ratio.py` (the S1–S6 sex-ratio battery)
| target | claim | key numbers | grade |
|---|---|---|---|
| **S1** | sex = one **bistable** switch (SOX9↔FOXL2), SRY the drive | two equal basins at h=0; SRY a transient supra-spinodal flip that **holds**; adult transdifferentiates only supra-spinodal (FOXL2/DMRT1-KO) | [V] / [L] SOX9+FOXL2 γ |
| **S2** | Mendelian 50:50 = a **symmetric (untilted)** segregation switch | 20 000-meiosis ensemble splits **0.4983** (analytic **0.50**) — a fair coin | [V] |
| **S3** | segregation distortion = a **tilt** (graded, then supra-spinodal fix) | TR(0)=0.50 → sub-spinodal **0.86** → supra-spinodal **1.0** (t-haplotype/SD limit) | [V] / [L] drive anchor |
| **S4** | sex-ratio distortion = a **signed** sex-chromosome gamete-killer | X-shredder SSR **1.0** (male), Y-killer **0.0** (female), weak driver **0.82** (partial) — one mechanism, two signs | [V] / [L] X-shredder anchor |
| **S5** | **Fisher** — the population sex ratio 1:1 is a **stable attractor** | returns to 0.50 from 0.20/0.80; weak persistent drive shifts it only to **0.5125**; human SSR ~0.512 is this small residual | [V] / [L] human SSR |
| **S6** | sex-determination γ atlas + **pre-registered axis-separation test (honest null)** | ovary axis trends higher (1.5163 vs 1.4857… testis 1.3857), but with SRY a strong outlier and n=3/axis the **permutation p=0.10 → not significant**; reported as it falls | [V] test reported / [L] γ / [O] separation open at this n |

### Changed — pipeline wiring (both batteries folded into the research gate)
- `repro/_verify/stress_tests.py`: `run_battery()` now appends **F1–F6 and S1–S6** to the suites, so
  `all_targets_pass` spans **T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6** (29 suites); `fertility_all_pass` and
  `sexratio_all_pass` are surfaced.
- `repro/_verify/gates.py`: `research_gate()` now reports `fertility_pass` and `sexratio_pass`.
- `repro/run_all.py`: section [3] prints the fertility and sex-ratio targets and the measured sex-determination
  γ atlas separately; the gate summary line now includes `fertility=` and `sexratio=`.

### Changed — `tools/build_docs.py` (chapters §13, §14)
- 10 new display equations (rep-inf-001…005, rep-sxr-001…005), rendered to `docs/eq/*.svg`.
- `gather_data()` imports the fertility and sex-ratio modules and their γ atlas; five new data-table builders.
- Two new canonical chapters — **§13 infertility & subfertility** (page grade V) and **§14 sex determination &
  sex-ratio distortion** (page grade V) — with answer-first paragraphs, claim strips, vp-cards, JSON-LD ×2,
  every number pulled **live** from the modules. Hub + `_meta.json` headlines extended; `llms.txt` rewritten to
  cover all 14 chapters and kept **under 5 KB**. Writing self-check **105 / 105 PASS**.

### Verification
- `research_gate()` **ALL_GREEN**, `result_sha256` = `f849da7d13d2…` **UNCHANGED**, 29 suites all PASS,
  battery determinism identical. `build_docs.py`: **14 pages / 28 display eqs / 105-105 checks**, core sha
  unchanged.

### Open (tracked)
- `paper/reproductive_endocrine_vp.tex` (the `build_paper.py` registry) is **not yet extended** to §13/§14 —
  HTML is canonical (C2); the PDF regeneration is a next-session follow-up.
- All absolute per-cycle probabilities, the map from a real semen/age value to a drive, the cause of the human
  sex-ratio residual, the specific azoospermia/POI gene→γ links, and whether the sex axis separates γ at this
  sample size remain **[O]**, each with its obstacle stated.

---

## v0.6.0-writing — the embryo: fertilisation → fetus (E1–E6) + measured developmental γ + chapter §12

**One line:** v0.5.0 emerged the two **gametes** (G1–G6). The user's next question is the obvious one — the
gametes are made, so let them **meet**, let a genome **emerge**, and let a **fetus** actually be built.
v0.6.0 adds a new `repro/_embryo/` module that carries the story from syngamy to a fetus, each step a
discriminant against the same vendored R19 switch + FHN oscillator, **reusing the gamete results** and adding
**measured developmental master-gene promoter γ** (17 genes, received through the identical DNA pipeline) as
the only new input. A six-target battery (E1–E6) all **PASS**, is wired into the research gate, and is written
up as canonical HTML **chapter §12** and a new PDF section. The hashed research core is **unchanged**
(`f849da7d…`): the embryo battery is an additional discriminant layer folded into `research_gate()`,
science-neutral to the `circulate()` core. The user confirmed a **human conceptual** treatment is fine
(γ-based gene-clock, not whole-genome synthesis).

### Added — `repro/_embryo/fetch_embryo_gamma.py` (measured developmental γ reception, the embryo's DNA emergence)
- Same NN-stacking ΔG37 pipeline (SantaLucia 1998, promoter TSS−2000..+500, GRCh38.p14) as the organ and
  gamete masters. The 17-gene panel was declared **by developmental stage and HOX axis position before any γ
  was seen** (no cherry-picking); each gene carries its `stage_rank` (the pre-registered hypothesis order:
  pluripotency = 1 < germ-layer = 2 < organ-primordium = 3). No-tuning gate: refuses to persist unless **both**
  vendored anchors reproduce — SOX9 (1.4598) and DAZL (1.3803). Writes `inherited/embryo_promoters.cache.json`
  + `inherited/embryo_gamma.json`; offline `verify()` recomputes γ from cache (DAZL cross-checked from the
  germline cache), network-free and bit-for-bit.
- **Measured developmental γ atlas (ascending):** NANOG 1.3479 · SOX17 1.3821 · GATA4 1.3933 · HOXB4 1.4453 ·
  PAX3 1.4479 · CDX2 1.4500 · SOX2 1.4576 · SOX9 1.4598 · PDX1 1.4732 · POU5F1 1.4874 · HOXA1 1.4923 ·
  MYOD1 1.4937 · FOXA2 1.4986 · PAX6 1.5110 · NKX2-5 1.5130 · TBXT 1.5130 · HOXA13 1.5427.
  **Stage means rise** (the pre-registered hypothesis): pluripotency 1.4310 < germ-layer 1.4373 < organ 1.4916.

### Added — `repro/_embryo/embryogenesis.py` (the E1–E6 embryo battery)
| target | claim | key numbers | grade |
|---|---|---|---|
| **E1** | **syngamy + DNA emergence** — sperm (oscillator) flips egg (held switch) one-way; two haploids fuse | egg activated one-way (sub-spinodal does **not** flip; polyspermy block holds); 1N+1N→2N,2C (→2N,4C after S); new genome unique to **10⁹⁴** (= gamete 10⁴⁷ squared) | [V] / [L] / [O] Ca²⁺-wave biophysics |
| **E2** | **cleavage** — symmetric divisions, mass conserved, first fate switch | cell count 1→2→4→…→64 = 2ⁿ (vs oogenesis 1+3); cytoplasmic mass conserved (cleavage ≠ growth), each blastomere 1/2ⁿ; ICM/TE = one R19 bistable switch | [V] / [L] blastocyst count / [O] cleavage timing |
| **E3** | **ZGA** — maternal-to-zygotic transition as a one-step spinodal crossing | genome OFF on maternal-only (ZAR1 1.4226, NLRP5 1.3475, MOS 1.3619) → ON in one jump 1.6551 at drive 0.3913 ≈ spinodal 0.3849; maternal(oocyte)→zygotic(embryo) handoff | [V] / [L] / [O] absolute ZGA cleavage-stage |
| **E4** | **the gene-clock builds the body** — emergence order = argsort(spinodal(γ)) | order NANOG→…→HOXA13; **pre-registered stage test ρ=0.5507, p=0.0200 → SUPPORTED** (γ tracks developmental stage); HOX 3′→5′ colinearity ρ=0.50, p=0.50 → posterior-most highest, partial (reported honestly) | [V] order + tests reported / [L] panel γ / [O] full atlas (DNA SSOT) |
| **E5** | **the whole arc** — one sperm + one egg → a fetus | deterministic gamete draws → distinct zygote fingerprint; arc all PASS (syngamy→cleavage→ZGA→body plan); fetus = unique genome 10⁹⁴ + 17 gene-clock-ordered structures, ICM-derived | [V] / [L] / [O] absolute gestational timing |
| **E6** | **honest scoreboard + firewall** | verified / anchored / open(obstacle) restated; firewall: package owns fertilisation + early embryo; full-body atlas + gene-clock law = DNA SSOT | [V] |

- Uses only `inherited/vp_substrate.py` + `gametogenesis.py` (the gamete results) + the measured developmental
  panel. Deterministic (SEED=19); the whole battery JSON is byte-identical across runs (`bdf77110…`). Each
  target carries its honest grade and states its obstacle for every `[O]`.

### Added — `inherited/embryo_identity.md` (seam note)
- Documents the developmental genes as **received from DNA, then read-only** (SSOT): the measured γ table by
  stage, what γ is used for (the body-plan emergence order = `argsort(spinodal(γ))` and relative size via
  DWELL) and what it is **not** (the fertilisation/cleavage/ZGA results are structural, γ-independent), the
  two pre-registered tests (stage correlation; HOX colinearity, partial), and the **firewall**: this package
  owns the fertilisation event + early embryo, the full-body atlas + gene-clock law are the DNA 4D-Blueprint
  package's SSOT (cited, never re-owned).

### Changed — pipeline wiring (embryo folded into the research gate)
- `repro/_verify/stress_tests.py`: `run_battery()` now appends E1–E6 to the suites, so `all_targets_pass`
  spans **T1–T5 + G1–G6 + E1–E6**, and an `embryo_all_pass` summary is surfaced.
- `repro/_verify/gates.py`: `research_gate()` now reports `embryo_pass` (enforced via `all_targets_pass`).
- `repro/run_all.py`: section [3] prints the embryo targets and the measured developmental γ atlas separately;
  the gate readout line adds `embryo`.

### Added — canonical chapter §12 (HTML) + index headline + 5 display equations + PDF section
- `tools/build_docs.py`: new chapter **`12-embryogenesis-fertilisation-to-fetus`** (“The embryo: fertilisation
  to fetus”), answer-first, with the syngamy ploidy table, the developmental γ-by-stage gene-clock table, and
  the pre-registered stage/HOX test narrative; `gather_data()` pulls the live embryo battery + atlas; five new
  display equations (`rep-emb-001..005`). Hub gains an embryo headline result; `llms.txt` gains gamete + embryo
  core claims. → **12 chapters · 7939 words · 18 equations**, writing-gate **91/91**, two builds byte-identical.
- `tools/build_paper.py`: new `sec_embryo` section (live numbers); two new open-quantity rows (absolute
  gestational timing; full-body atlas as DNA SSOT). PDF **10→12 pp**, `.tex` byte-identical, 0 unresolved refs.

---

## v0.5.0-writing — the gamete itself (germline): meiosis, motility, the egg — G1–G6 + measured gamete-program γ + chapter §11

**One line:** the package emerged the reproductive **organs** and the HPG **rhythms** but had never opened the
**germ cell**. v0.5.0 adds a new `repro/_germline/` module that answers the four questions about the gamete —
*how* it is made, *whether* gametes are identical, the *sperm* motility logic, the *egg* logic — each as a
discriminant against the same vendored R19 switch + FHN oscillator, with **measured gamete-program promoter γ**
(13 genes, received through the identical DNA pipeline) as the only new input. A six-target battery (G1–G6) all
**PASS**, is wired into the research gate, and is written up as canonical HTML **chapter §11** and a new PDF
section. The hashed research core is **unchanged** (`f849da7d…`): the gamete battery is an additional
discriminant layer folded into `research_gate()`, science-neutral to the `circulate()` core.

### Added — `repro/_germline/fetch_germline_gamma.py` (measured gamete-machinery γ reception)
- Same NN-stacking ΔG37 pipeline (SantaLucia 1998, promoter TSS−2000..+500, GRCh38.p14 = GCF_000001405.40) as
  the organ masters, generalised to resolve coordinates online via the NCBI datasets v2 API, then efetch
  promoters. The 13-gene panel was declared **by function before any γ was seen** (no cherry-picking):
  meiosis {SPO11, PRDM9, DMC1, MLH1, REC8}, sperm {CATSPER1, DNAH1, TEKT1}, oocyte {ZP3, MOS, NLRP5, ZAR1},
  plus the germline anchor {DAZL}. No-tuning gate: refuses to persist unless **both** vendored anchors
  reproduce — SOX9 (1.4598) and DAZL (1.3803). Writes `inherited/germline_promoters.cache.json` +
  `inherited/germline_gamma.json`; offline `verify()` recomputes γ from cache (network-free, bit-for-bit).
- **Measured γ atlas (ascending):** TEKT1 1.3400 · NLRP5 1.3475 · MOS 1.3619 · DAZL 1.3803 · CATSPER1 1.4019 ·
  DMC1 1.4056 · MLH1 1.4085 · SPO11 1.4105 · PRDM9 1.4165 · ZAR1 1.4226 · DNAH1 1.4469 · ZP3 1.4486 · REC8 1.4525.
  The recombination core (SPO11/DMC1/MLH1/PRDM9) clusters tightly ≈1.406–1.417.

### Added — `repro/_germline/gametogenesis.py` (the G1–G6 discriminant battery)
| target | claim | key numbers | grade |
|---|---|---|---|
| **G1** | meiosis = one replication + **two ordered divisions** (reductional → equational) | ploidy 2N,2C→2N,4C→1N,2C→1N,1C; order forced by two-stage REC8 release (arm separase 0.684 → centromeric 1.085, shugoshin protection sign, not tuned) | [V] / [L] / [O] separase kinetics |
| **G2** | gametes are **NOT identical** | independent assortment exactly 2²³ = 8,388,608; crossover **interference = the substrate refractory period** mapped onto the chromosome (Fano 0.108 vs Poisson 0.976, gap CV 0.26, obligate CO); distinct-gamete floor 10⁴⁷ | [V] / [L] |
| **G3** | sperm flagellum = the **fast** relaxation oscillator; CatSper = the gain switch | four-clock ladder 26.2 < 132.45 < 674.95 < 1133.65 (flagellum<pulse<spermatogenic<menstrual); hyperactivation raises amplitude (2.21→2.83) **and** slows the beat (77→57) | [V] / [L] ~20 Hz / [O] integer 9 of the 9+2 axoneme |
| **G4** | egg = a switch **held** at metaphase II; fertilisation = a one-way spinodal flip | arrested state −1.088; sub-spinodal Ca²⁺ does **not** flip, supra-spinodal (>0.3849) does; polyspermy block = past-spinodal irreversibility | [V] / [L] |
| **G5** | gamete-program γ atlas + **pre-registered** module-separation test | permutation test **NULL** (F 0.109, p 0.617) reported as it falls; positive sub-test: recombination core is a tight cluster (CV 0.0028 vs panel 0.0253, p 0.0014) | [V] on the narrow claim; null reported honestly |
| **G6** | sperm/egg **duality**: oscillator vs held switch; symmetric (4) vs asymmetric (1) | one substrate → free oscillator (sperm) vs held switch (egg); 4 spermatids vs 1 egg + 3 polar bodies; anisogamy (egg:polar-body 49×, egg:sperm volume ~18,963×) | [V] / [L] size anchor / [O] evolutionary "why" |

- Uses only `inherited/vp_substrate.py` + the measured panel γ. Deterministic (SEED=19); the whole battery JSON
  is byte-identical across runs. Each target carries its honest grade and states its obstacle for every `[O]`.

### Added — `inherited/germline_identity.md` (seam note)
- Documents the gamete-program genes as **received from DNA, then read-only** (SSOT): the measured γ table, what
  γ is used for (only where a measured master names a mechanism the substrate already owns — REC8→cohesin
  spinodal, CATSPER1→hyperactivation gain, MOS→cytostatic hold) and what it is **not** (the structural results
  do not depend on γ), and the pre-registered test discipline (the null is reported; only the core cluster is claimed).

### Changed — pipeline wiring (germline folded into the research gate)
- `repro/_verify/stress_tests.py`: `run_battery()` now appends G1–G6 to the suites, so `all_targets_pass`
  spans **T1–T5 + G1–G6**, and a `germline_all_pass` summary is surfaced.
- `repro/_verify/gates.py`: `research_gate()` now reports `germline_pass` (enforced via `all_targets_pass`).
- `repro/run_all.py`: section [3] prints the HPG targets and the gamete targets separately, plus the measured
  γ atlas; the gate readout line adds `germline`.

### Added — canonical chapter §11 (HTML) + index headline + 5 display equations
- `tools/build_docs.py`: new chapter **`11-gametogenesis-the-gamete-itself`** ("The gamete itself: meiosis,
  motility and the egg"), answer-first, with the meiosis ploidy table, the measured γ-by-module table, and the
  honest-null narrative; `gather_data()` pulls the live germline battery + atlas; five new display equations
  (`rep-gmt-001..005`); a sixth headline result on the index page; the chapter-count self-check made
  count-agnostic. **Site now 11 chapters · 6417 words · 13 equations**; writing-gate **84/84 PASS**; `docs/` two
  builds **byte-identical**.

### Changed — LaTeX whitepaper grows a gamete section (PDF 9 → 10 pp)
- `tools/build_paper.py`: new `sec_gamete(D)` mirrors the HTML chapter (live numbers, the γ-by-module table, the
  reported null + core-cluster result); `gather()` pulls the germline battery + atlas. The `.tex` remains
  byte-identical across runs (no `\today`); the PDF recompiles to **10 pp**, `pdflatex`-clean, 0 unresolved refs.

### Unchanged — the frozen science core
- The deterministic `circulate()` core sha256 is still
  **`f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4`** (2× identical). The gamete battery runs
  **live** inside `research_gate()` (like every other research module) and does **not** enter the hashed core, so
  adding it does not perturb the hash. The measured-γ reception is a measurement (cached), not a fit.

---

## v0.4.1-writing — Zenodo deposit prep: concept DOI assigned; LaTeX/PDF whitepaper + reproducibility archive

**One line:** the writing-phase site was carried to a **Zenodo deposit**. The honest `pending` DOI marker was
replaced everywhere by the **Zenodo concept DOI `10.5281/zenodo.20754657`** (version-independent, always
resolving to the latest version), and a canonical **LaTeX whitepaper** was added via a new live-number generator
(`tools/build_paper.py`) and compiled to **PDF** (9 pp). Three deposit artefacts are produced: the `.tex`
source, the compiled `.pdf`, and the reproducibility archive (this whole package). The hashed research core is
**unchanged** (`f849da7d…`); only the DOI string and the new paper artefacts were added.

### Added — `tools/build_paper.py` (canonical LaTeX whitepaper generator)
- Mirrors `build_docs.py`: imports the same research modules and pulls **every** displayed number live at
  build time (`emerge_organs`, `run_T1..run_T5`, `run_oncology`, `run_therapy`, `run_disease`), so the PDF
  cannot drift from the engine (C1). Refuses while `gates.writing_locked()` is True.
- Emits `paper/reproductive_endocrine_vp.tex`: title page (author + ORCID + version + DOI + canonical), abstract,
  keywords, the full 10-section body (substrate, organ emergence, GnRH generator, menstrual cycle, oestrogen
  switch/LH surge, spermatogenic cycle, puberty, hormone-cancer dose–response, temporal-pattern therapy, disease
  map), a Methods/reproducibility section, an honest open-quantity table, data/code availability, and a
  9-entry bibliography (SantaLucia 1998; FitzHugh 1961; Nagumo 1962; Kramers 1940; Knobil 1980; WHI 2002;
  Denmeade–Isaacs BAT; the two VP sibling papers).
- **Deterministic:** `\today` is never used (the title page carries the fixed version + DOI), so the `.tex` is
  byte-identical across runs. All eight result tables and the inline numbers are generated from the live module
  returns.

### Built — `paper/` deposit artefacts
| file | content |
|---|---|
| `paper/reproductive_endocrine_vp.tex` | LaTeX source (~28.5 KB), `pdflatex`/`latexmk`-clean, 0 unresolved refs |
| `paper/reproductive_endocrine_vp.pdf` | compiled whitepaper, **9 pages**, A4, colour grade badges, linked DOI/ORCID |

### Changed — concept DOI assigned (was honestly pending)
- `tools/build_docs.py`: introduced `DOI = "10.5281/zenodo.20754657"` + `DOI_URL`; the claim-strip and footer
  now render a **clickable DOI link** (was a `pending` span), `_meta.json` `doi` is now
  `{value, url, type:"concept", note}`, and `llms.txt` carries the real DOI. A comment documents that this is
  the Zenodo **concept** DOI (version-independent, always latest), the only DOI used as the package identifier.
- Removed the now-dead `.doi-pending` CSS rule. The site was rebuilt; **no `pending` string remains** anywhere
  in `docs/`. Per-page word counts shifted trivially (DOI text replaced the placeholder).

### Governance / determinism
- `VERSION` 0.4.0-writing → **0.4.1-writing**. `PHASE` stays `writing`.
- Research core sha256 **unchanged** (`f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4`) —
  the DOI/paper layer sits on frozen science. `docs/` two-build determinism still byte-identical; writing-gate
  **77/77**. The `.tex` is byte-identical across runs; the `.pdf` is the `pdflatex` compile of that source.
- `inherited/` untouched; no research module edited. `IRREPRODUCIBILITY_LEDGER.md` open [O] set unchanged.

---

## v0.4.0-writing — WRITING phase entered: canonical 10-chapter VP-SPEC v1.8 HTML whitepaper built

**One line:** the deliberate writing decision was taken — `research_gate().all_green` confirmed True,
`gates.write_research_complete()` re-written, root `PHASE` flipped `research → writing` — and
`tools/build_docs.py` (the stub the whole research phase unlocked) was **implemented and run**, emitting the
full per-title canonical HTML site under `docs/`. Every published number is pulled **live** from the research
engine at build time (the site cannot drift from the code); two full builds are **byte-identical**. The hashed
research core is **unchanged** (`f849da7d…`): the writing phase reads the science, it does not alter it.

### The writing decision (3 conditions, all met)
- ① `research_gate()` `all_green == true` (7 sections green) · ② `gates.write_research_complete()` re-written
  (`reports/research_complete.json`, `all_green: true`) · ③ root `PHASE` set to `writing`.
- `gates.writing_locked()` now returns `(False, "writing unlocked")`; `build_docs.py` proceeds instead of refusing.

### Added — `tools/build_docs.py` implemented (was the locked stub)
- Per-title canonical generator, VP-SPEC v1.8 §6 conformant. Refuses while `gates.writing_locked()` is True;
  when unlocked, builds **10 chapter pages + hub + site artefacts**. English body (C0); HTML is canonical (C2);
  every displayed quantity pulled live from the modules (`emerge_organs`, `run_T1..run_T5`, `run_oncology`,
  `run_therapy`, `run_disease`) at build time (C1) — **no result is ever hard-coded**.
- **Answer-first** (`<p class="answer">` 40–60 words, self-contained) · `<p class="abstract">` · `claim-strip`
  (grade badge + LOCK→Derive→Gate + GitHub repro link + DOI) · one **vp-card** per cited locked quantity
  (`h_sp`, `ΔV₀`, DWELL, γ-method) with self-contained restatement + canonical-derivation link · two JSON-LD
  blocks per page (`ScholarlyArticle` + `BreadcrumbList`) · `<link rel="canonical">` · external `site.css`
  (no inline CSS/JS) · prev/next nav · honest grade badges throughout.
- **Display equations → canonical SVG** (matplotlib mathtext; `svg.hashsalt` fixed + Date metadata suppressed →
  byte-stable). 8 display equations rendered to `docs/eq/*.svg`, referenced by `<img>` with LaTeX `alt` text (C2).

### Built — `docs/` canonical site (24 files)
| artefact | content |
|---|---|
| `docs/index.html` | hub: title, lede, one-drive/two-failures/one-lever thesis, 6 live headline results, 10-chapter TOC with grade badges; JSON-LD `CreativeWorkSeries` + `BreadcrumbList` |
| `docs/<slug>/index.html` ×10 | §1 scope+substrate · §2 organ emergence (measured γ) · §3 GnRH pulse generator (T1) · §4 menstrual relaxation cycle (T2) · §5 oestrogen feedback switch + LH surge (T3) · §6 spermatogenic cycle (T4) · §7 puberty spinodal crossing (T5) · §8 hormone-cancer dose-response · §9 temporal-pattern therapy · §10 HPG disease mechanisms |
| `docs/eq/*.svg` ×8 | canonical rendered display equations (deterministic) |
| `docs/_meta.json` | VP-SPEC §9 summary card (paper_id, grades, per-chapter words + eq counts, totals, core sha256, DOI pending) |
| `docs/sitemap.xml` | 11 URLs (hub + 10 chapters) |
| `docs/robots.txt` | 7 named crawlers (Googlebot, Bingbot, OAI-SearchBot, GPTBot, PerplexityBot, ClaudeBot, Google-Extended) + Sitemap |
| `docs/llms.txt` | 4100 B authoritative retrieval summary (< 5 KB): blockquote + core claims + chapters + concepts + policies |
| `docs/assets/css/site.css` | external stylesheet (light + dark, system fonts, grade colours) |
| `manifest/reproductive_endocrine_vp_site.csv` | per-chapter slug,title,section_no,status,grade,words,eq_display — computed from the emitted HTML (builder is SSOT; was empty headers) |

- Totals (live): **10 chapters · 5010 words · 8 display equations**. Grades by page:
  §1 [F] · §2 [V] · §3 [V] · §4 [V] · §5 [V] · §6 [V] · §7 [V] · §8 [F] · §9 [V] · §10 [V].
- Internal nav / CSS / equation links are **relative** (`../`, `../assets/css/site.css`, `../eq/`) so the zip is
  locally browsable; absolute canonical URLs appear only in `<link rel=canonical>`, JSON-LD, sitemap, and footer.
- **DOI is honestly PENDING** ("pending Zenodo deposit") — never invented (C1/C3). Only the real sibling DOIs
  (VP Theory `10.5281/zenodo.17932566`, 4D DNA `10.5281/zenodo.20471407`) are cited, inside the vp-cards.

### Writing-phase conformance gate — `reports/writing_gate.json`
- Self-check **77 / 77 PASS**: every page has answer-first + 2× JSON-LD + canonical + claim-strip + external CSS
  + no-KaTeX; vp-card present where declared; hub has thesis + full TOC + 2× JSON-LD; robots has all 7 bots +
  Sitemap line; sitemap lists all 11 URLs; llms.txt < 5 KB; `_meta.json` parses with 10 chapters + core sha.

### Governance / determinism
- `VERSION` 0.3.0-research → **0.4.0-writing**. `PHASE` `research` → **`writing`**.
- **Reproducibility (C1):** `docs/` built twice from scratch → `diff -r` **clean (byte-identical)**. Equation SVGs
  carry no embedded timestamp. The research core sha256 is **unchanged** (`f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4`) —
  this is a writing-phase change layered on top of frozen science, not a science change.
- `inherited/vp_substrate.py` and `inherited/organ_promoters.cache.json` untouched. No research module edited.
- `IRREPRODUCIBILITY_LEDGER.md`: open [O] set unchanged (the site renders existing graded science); a
  writing-phase determinism line added under "What is NOT open".

---

## v0.3.0-research — γ reception: FOXL2 / DAZL / WT1 measured ([O]→[V]); writing still LOCKED

**One line:** the three TO-MEASURE reproductive master genes were **received** via the identical DNA
`fetch_morpho_gamma` pipeline (NN-stacking ΔG37, SantaLucia 1998, proximal promoter TSS-2000..+500, GRCh38),
promoting gonad_ovary / germline / reproductive_tract from deferred **[O]** to emerged **[V]** with real
measured γ. Measured input, never fitted; validated by reproducing the vendored SOX9 anchor bit-for-bit.
Writing remains a separate locked phase; `tools/build_docs.py` was **not** run.

### Added — γ reception pipeline (`repro/_gamma/fetch_gamma.py`)
- Self-contained reception of master-gene γ using the same method the DNA atlas uses:
  `γ = −mean(NN-stacking ΔG37, SantaLucia 1998)` over the human proximal promoter window **TSS-2000..+500**;
  `GC = (G+C)/ACGT`. TSS convention validated on SOX9 (plus → gene-range begin; minus → gene-range end).
- **Fidelity cross-check (no-tuning):** the pipeline is accepted only because it reproduces the vendored
  anchor **SOX9 γ=1.4598, GC=0.545** to 4 dp. Having reproduced the known anchor, the three unknowns measured
  by the identical code are legitimate measurements, not fits.
- Two modes: `verify()` (default, **offline** — recompute γ from the cache, cross-check SOX9, confirm
  agreement with `organ_gamma.json`); `--fetch` (**online** — pull promoters from NCBI E-utilities
  strand-aware, rebuild the cache, write measured γ back).

### Added — offline reproduction cache (`inherited/organ_promoters.cache.json`)
- Full promoter sequences (2501 bp each) + per-gene accession/strand/TSS/window/GC/γ/`seq_sha256`, so γ
  reproduces **offline bit-for-bit** without the network. Cross-checked by `fetch_gamma.py verify()`:
  `recompute_matches_cache`, `matches_gamma_json`, `seq_sha_ok`, `anchor_ok` all true.

### Measured values (GRCh38.p14, NCBI exact TSS)
| master | organ | accession / strand | TSS | γ (measured) | GC |
|---|---|---|---|---|---|
| FOXL2 | gonad_ovary | NC_000003.12 − | 138947137 | **1.4829** | 0.5754 |
| DAZL | germline | NC_000003.12 − | 16605423 | **1.3803** | 0.4790 |
| WT1 | reproductive_tract | NC_000011.10 − | 32435539 | **1.5182** | 0.6010 |
| SOX9 (anchor) | gonad_testis | NC_000017.11 + | 72121020 | 1.4598 | 0.5450 |

- **Developmental order (γ ascending, now over all four):** germline (1.3803) → gonad_testis (1.4598) →
  gonad_ovary (1.4829) → reproductive_tract (1.5182). Order is a γ readout over MEASURED organs **[V]**;
  germline-first is consistent with PGC specification preceding gonadal differentiation (sign sanity-check).

### Changed — engine + atlas
- **`repro/_engine/vp_rep_engine.py`** — `ORGAN_ROWS` `gamma_state` for FOXL2 / DAZL / WT1 flipped
  `to_measure → vendored`; all four organs now emerge with measured γ (functional spinodal + relative DWELL
  size computed), and `gamma_order_ascending` spans all four (was `['gonad_testis']`). The shared FHN
  oscillator still uses γ=1 (rhythm depends on τ, not identity γ) — the dynamics are unchanged; only the
  emergence/order claim is promoted.
- **`inherited/organ_gamma.json`** — FOXL2 / DAZL / WT1 moved out of `_to_measure` into `genes{}` with
  measured γ + GC + accession `src`; `_to_measure` now empty; `_reception_note` + `_measured_order_gamma_asc`
  added (top-level metadata; the engine reads only `genes`, so the hashed core is unaffected by these keys).

### Governance / determinism
- `VERSION` 0.2.0-research → **0.3.0-research**. `PHASE` stays `research` (writing intentionally locked;
  `build_docs.py` confirmed still REFUSED, reason `PHASE != writing`).
- All seven gate sections remain **green**; `research_gate().all_green == true`; `gates.write_research_complete()`
  re-written. Determinism `circulate()` 2× sha256 identical, byte-identical, process-stable. The hashed core
  **changed legitimately** (organ section now carries real γ for four organs and a four-element order) — this
  is a science change, not science-neutral infra:
  - old core (v0.2.0): `974effe2d6c2391f7b4b816d33f3aea684d3a22ef16b794d907741f370147899`
  - **new core (v0.3.0): `f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4`**
- `IRREPRODUCIBILITY_LEDGER.md`: the TO-MEASURE γ row retired from open (now reproduced **[V]**, offline from
  the cached promoters); determinism line updated to the new sha.



**One line:** the v0.1.0 skeleton was researched into a complete, deterministic, non-tuned research body —
HPG-axis dynamics (T1–T5), exact-barrier hormone-cancer dose-response, a temporal-pattern therapy capstone,
and a non-rare disease mechanism + better-treatment layer — with every module folded into one green research gate.
Writing (canonical HTML) remains a separate locked phase; `tools/build_docs.py` was **not** run.

### Added — dynamics (`repro/_dynamics/`)
- **`hpg_axis.py`** — **T1** GnRH pulse generator as an FHN relaxation oscillator, with frequency-decoding
  (slower τ_s → fewer, wider pulses: τ_s 20→155 pulses favour LH (fast); 150→27 pulses favour FSH (slow);
  rate monotone in τ_s). **T5** puberty onset as a discontinuous **spinodal crossing**
  (state −0.5136 → +0.4417, jump/spinodal = 1.01, localised at the spinodal). PASS.
- **`menstrual_cycle.py`** — **T2** menstrual cycle as a slow relaxation oscillator and **T3** the oestrogen
  feedback switch (negative → positive LH-surge flip with hysteresis). **T2 PASS-criterion fixed**: the earlier
  surge-fraction test was replaced by a **rise/fall asymmetry ratio** (a pure sinusoid = 1.0 by symmetry; a
  relaxation oscillator ≫ 1; boundary > 2.0). T2 now asymmetry = **309.59** PASS; T3 surge discontinuous
  (up-jump 1.634, hysteresis width 0.779) PASS.
- **`spermatogenesis.py`** — **T4** seminiferous cycle as an *intermediate* relaxation clock
  (τ_s = 600 × 16/28 → 340, a clinical-ratio **[L]** anchor, **not** tuned). Period ordering verified:
  pulse 132.45 < spermatogenic 656.5 < menstrual 1133.65 (arb). PASS.

### Added — oncology (`repro/_oncology/carcinogen_dose_response.py`, rewritten)
- Exact tilted double-well barrier via `np.roots` (no small-tilt approximation): `V(s) = −γs²/2 + s⁴/4 − hs`.
- **γ-independence [F]:** `meta_barrier(γ,h)/barrier(γ)` vs `frac = h/spinodal(γ)` is **identical across γ**
  (max spread **0.0**). Table: frac 0.0→1.0, 0.2→0.71014, 0.4→0.45804, 0.6→0.24771, 0.8→0.08705, 0.95→0.01083.
- Site dose-response **shapes** (Kramers RR): **breast** monotone in cumulative-oestrogen years (per-year 0.024 [L]);
  **prostate** concave + **plateau past the fold** (androgen saturation model); **cervical** HPV×smoking
  multiplicative at low joint exposure, **sub-multiplicative (saturating)** at high — a falsifiable prediction.
- `NOISE_D = 0.15` declared as the single open lattice constant **[O]**; every reported RR **ratio** is D-robust.
- `run_oncology()` status **PASS**.

### Added — therapy capstone (`repro/_therapy/temporal_pattern.py`)
- **Temporal pattern as a control axis separate from level.** BAT/cycling selectivity (resistance modelled as
  amplified coupling κ, **not** deeper wells: κ_sens 1, κ_res 3): continuous-high res/sens 8.35; continuous-low
  ADT 2.36; **cycling** res/sens 6.52, and cycling delivers the resistant clone **13.6×** its own continuous-high
  transition stress — retrodicts Bipolar Androgen Therapy (CRPC) and oestrogen-induced apoptosis in LTED breast.
- **GnRH same molecule, opposite effect:** continuous drive ≥ 2×spinodal → **0** pulses (depolarisation
  block = desensitisation/suppression); pulsatile (brief peaks) → **41** pulses (activation). Uses the vendored
  `Neuron.run()` with a drive array. `run_therapy()` status **PASS**.

### Added — disease layer (`repro/_disease/mechanisms.py`)
- 8 non-rare disorders mapped as *disease → substrate failure → current Rx as a substrate move → VP-derived
  better-treatment hypothesis*, each honestly graded ([V]/[L] retrodiction vs [O] novel). 5 computational
  substrate checks PASS using only **robust** verified levers:
  - **PCOS** fast-τ → LH-biased pulse (rate 0.0135 vs slow 0.00325); **FHA** suppressed low-frequency
    (0.0025 vs normal 0.0075) — *PCOS and FHA are opposite ends of one pulse-frequency axis*.
  - **Menopause** = loss of the bistable secretory **latch** on follicular depletion (intact holds ON = 1.0 at
    h = 0; depleted collapses to 0.229) — irreversible **[O]**.
  - **Puberty** = T5 spinodal (OFF below / ON above); **anovulation** = surge switch fails, hCG = a spinodal kick.

### Changed — verification & entry point
- **`repro/_verify/gates.py`** — `research_gate()` now folds **oncology + therapy + disease** module
  `status == PASS` into `all_green`, in addition to determinism + emergence + the T1–T5 battery. Each research
  module is invoked exactly once. The hashed deterministic core stays the light `circulate()` emit.
- **`repro/run_all.py`** — reports all seven sections: organ emergence, oscillator confirmation, T1–T5 battery,
  oncology, therapy, disease, and the research gate (+ writing-lock status).
- **`repro/_verify/stress_tests.py`** — imports `_dynamics` and runs T1–T5 live.

### Governance
- `VERSION` 0.1.0-research → **0.2.0-research**. `PHASE` stays `research` (writing intentionally locked).
- `IRREPRODUCIBILITY_LEDGER.md` extended with three new **[O]** items + stated obstacles: NOISE_D
  (absolute RR magnitude; all ratios D-robust), chronological pubertal age (T5; order [V], calendar age needs
  external calibration), menopause irreversibility (no in-package follicle regeneration).
- `reports/research_complete.json` written by `gates.write_research_complete()` with `all_green = true`.
- Determinism: `circulate()` emits identical sha256 on repeat (`974effe2d6c2391f7b4b816d33f3aea684d3a22ef16b794d907741f370147899`),
  unchanged from the v0.1.0 hashed core (research modules are aggregated separately, not in the hashed core).

---

## v0.1.0-research — Skeleton
- Bootstrap (`START_HERE.md`, `CHARTER.md`), substrate vendored (`inherited/vp_substrate.py`), VP-SPEC v1.8,
  organ identity γ (SOX9 = 1.4598; FOXL2/DAZL/WT1 declared TO-MEASURE). Engine `circulate()`/`emit()`,
  research/writing gate, `build_docs.py` refusing while locked. Baseline: only `gonad_testis` emerges (SOX9
  vendored); `gonad_ovary` oscillates (7 beats); T1–T5 defined but not yet implemented.
