# MASTER MANUAL — Reproductive / Gonadal-Endocrine (`reproductive_endocrine_vp_site`) · v0.7.1-writing

> 이 문서는 패키지의 **운영 매뉴얼**이다. 무엇이 어디서 어떻게 돌아가는지, 어떤 물리가 잠겼는지, 어떻게 재현하는지를 한 곳에 모은다.
> 항해는 한국어, 기술 본문·코드·등급은 영어. `[V]` sim-verified · `[L]` measured-anchor · `[F]` forced · `[O]` open(장애물 명시 필수).

---

## 0. 정체 (one line)
Gonads, the HPG axis and the germline emerge on the jammed substrate. One sex-hormone drive `h`; **two** failure
modes — a too-little / wrong-pattern oscillator disease (HPG) and a barrier-lowering oncogenic switch (R19);
**one** temporal-pattern lever (pulsatile / cycling). Brain-facing HPA stays in `mind` (firewall); this package
owns the gonadal axis only.

## 1. 즉시 실행
```bash
python repro/run_all.py        # 연구 재현 (7 섹션 + writing-lock 상태)
python tools/build_docs.py     # 집필: docs/ 정본 HTML 사이트 생성 (PHASE==writing + 게이트 그린일 때만)
```
`run_all.py`는 일곱 섹션(장기 창발, 진동자 확인, T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6 판별 배터리, oncology, therapy, disease, research gate)과
writing-lock 상태를 출력한다. **현재 `PHASE==writing`이므로** `build_docs.py`는 거부하지 않고 사이트를 빌드한다
(v0.3.0까지는 `PHASE != writing`으로 거부됐다). 두 번 빌드하면 `docs/`는 **바이트 동일**.

## 2. 디렉터리 지도
```
reproductive_endocrine_vp_site/
├── START_HERE.md            # bootstrap (read first)
├── CHARTER.md               # scope, IN/OUT seams, T1–T5 definitions
├── VERSION                  # 0.7.1-writing
├── PHASE                    # "writing"  (research signed off + gate green → writing unlocked)
├── CHANGELOG.md MASTER_MANUAL.md COMPLETION_LEDGER.md HANDOVER.md   # 4-doc SSOT
├── IRREPRODUCIBILITY_LEDGER.md   # every [O] with its obstacle
├── VP_SPEC_v1_8.md          # full spec (for the writing phase)
├── inherited/
│   ├── vp_substrate.py      # VENDORED primitives (FHN/R19) — MUST NOT MODIFY
│   ├── organ_gamma.json     # SOX9/FOXL2/DAZL/WT1 γ all measured [V] (FOXL2/DAZL/WT1 received v0.3.0)
│   ├── organ_promoters.cache.json   # cached organ promoter seqs (2501 bp) → offline bit-for-bit γ
│   ├── organ_identity.md             # organ seam note (DNA-cited identity + order)
│   ├── germline_gamma.json           # 13 gamete-program genes γ all measured [V] (received v0.5.0)
│   ├── germline_promoters.cache.json # cached gamete-program promoter seqs → offline bit-for-bit γ
│   ├── germline_identity.md          # gamete seam note (DNA-received γ atlas, read-only, SSOT)
│   ├── embryo_gamma.json             # 17 developmental master genes γ all measured [V] (received v0.6.0)
│   ├── embryo_promoters.cache.json   # cached developmental promoter seqs → offline bit-for-bit γ
│   └── embryo_identity.md            # developmental seam note (DNA-received γ, read-only, firewall, SSOT)
├── repro/
│   ├── run_all.py           # research entry point (7 sections; §[3] now T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6 + γ atlases)
│   ├── _engine/vp_rep_engine.py        # emerge_organs / confirm_oscillators / circulate / emit (hashed core)
│   ├── _gamma/fetch_gamma.py           # organ-master γ reception (DNA fetch_morpho_gamma pipeline); verify()/--fetch
│   ├── _germline/fetch_germline_gamma.py  # GAMETE-program γ reception (same pipeline, 13 genes); verify()/--fetch  [v0.5.0]
│   ├── _germline/gametogenesis.py      # G1–G6 gamete discriminant battery (meiosis/motility/egg/duality)         [v0.5.0]
│   ├── _embryo/fetch_embryo_gamma.py   # DEVELOPMENTAL γ reception (same pipeline, 17 genes); verify()/--fetch     [v0.6.0]
│   ├── _embryo/embryogenesis.py        # E1–E6 embryo battery (syngamy/cleavage/ZGA/gene-clock/arc/scoreboard)     [v0.6.0]
│   ├── _fertility/infertility.py       # F1–F6 fertility battery (chain/categorical-vs-Kramers/male/female/Rx/scoreboard) [v0.7.0]
│   ├── _sexratio/fetch_sexratio_gamma.py # SEX-DETERMINATION γ reception (same pipeline, 6 genes); verify()/--fetch    [v0.7.0]
│   ├── _sexratio/sex_ratio.py          # S1–S6 sex-ratio battery (bistable/Mendel/drive/skew/Fisher/atlas)            [v0.7.0]
│   ├── _dynamics/hpg_axis.py           # T1 (pulse generator) + T5 (puberty spinodal)
│   ├── _dynamics/menstrual_cycle.py    # T2 (slow relaxation) + T3 (feedback switch)
│   ├── _dynamics/spermatogenesis.py    # T4 (intermediate clock)
│   ├── _oncology/carcinogen_dose_response.py   # exact-barrier RR(dose) for breast/cervical/prostate
│   ├── _therapy/temporal_pattern.py    # BAT/cycling selectivity + pulsatile-vs-continuous GnRH
│   ├── _disease/mechanisms.py          # 8 non-rare disorders + better-treatment hypotheses
│   └── _verify/
│       ├── stress_tests.py  # runs T1–T5 + G1–G6 + E1–E6 + F1–F6 + S1–S6 live → run_battery() (germline+embryo+fertility+sexratio folded in)
│       └── gates.py         # research_gate() folds ALL modules incl. germline + embryo; writing_locked(); write_research_complete()
├── reports/                 # emergence_results.json, research_complete.json, writing_gate.json (generated)
├── tools/
│   ├── build_docs.py        # WRITING-phase canonical HTML generator (14 chapters incl. §11 gamete, §12 embryo, §13 fertility, §14 sex)
│   └── build_paper.py       # WRITING-phase canonical LaTeX whitepaper generator (incl. sec_gamete, sec_embryo, sec_infertility, sec_sexratio)
├── paper/                   # DEPOSIT artefacts: reproductive_endocrine_vp.tex + .pdf (15 pp)
├── manifest/…csv            # per-chapter manifest (slug,title,section,status,grade,words,eq) — emitted by builder
└── docs/                    # CANONICAL SITE: index.html hub · 11× <slug>/index.html · eq/*.svg
                             #   · _meta.json · sitemap.xml · robots.txt · llms.txt · assets/css/site.css
```

## 3. 기질 프리미티브 (vendored — 절대 수정 금지)
`inherited/vp_substrate.py`: `sdot`, `spinodal(g)=2*(g/3)**1.5` (spinodal(1.0)=0.3849), `barrier(g)=g**2/4`,
`settle`, `is_on`, `dwell(g,brake,K=0.6)=g**1.5/(K+brake)`, class `Organ`, class
`Neuron(gamma, tau_f, tau_s=40, beta=0.5)` with `run(drive, E=1.0, I=1.0, …)` (drive scalar **or** array,
s clamped to ±12), `Neuron.spikes`, `rate_hz`, `dominant_freq`; `SEED=19`; `seed_everything()`.
**Note:** the attribute is `self.g` (not `self.gamma`); `E`/`I` are `run()` args, not attributes. At
γ=1, β=0.5, E=I=1 the FHN is an autonomous limit cycle at **all** bias `h` — the only silence lever is
depolarisation block at drive ≳ 2×spinodal. (This is why FHA is modelled as low-*frequency*, not as silence,
and menopause as latch-loss, not amplitude decay.)

## 4. 잠긴 물리 (what is locked, with numbers)

### 4.0 Organ emergence (measured master-gene γ — received v0.3.0)
All four organs emerge from MEASURED γ (NN-stacking ΔG37, SantaLucia 1998, promoter TSS-2000..+500, GRCh38);
none are deferred. γ is a measured input, never fitted — the pipeline (`repro/_gamma/fetch_gamma.py`) is
accepted only because it reproduces the vendored SOX9 anchor (γ=1.4598, GC=0.545) bit-for-bit, and the
promoter sequences are cached (`inherited/organ_promoters.cache.json`) for offline reproduction.

| master | organ | γ | GC | accession (GRCh38) |
|---|---|---|---|---|
| DAZL | germline | 1.3803 | 0.479 | NC_000003.12 − |
| SOX9 | gonad_testis | 1.4598 | 0.545 | NC_000017.11 + |
| FOXL2 | gonad_ovary | 1.4829 | 0.575 | NC_000003.12 − |
| WT1 | reproductive_tract | 1.5182 | 0.601 | NC_000011.10 − |

Developmental order = argsort(γ) = **germline → gonad_testis → gonad_ovary → reproductive_tract** [V] (germline-
first is consistent with PGC specification preceding gonadal differentiation — a sign sanity-check, not a fit).
The shared FHN oscillator still runs at γ=1 (rhythm depends on τ, not identity γ), so this promotion changes the
**emergence/order** claim only, not the dynamics.

### 4.1 Discriminant battery (T1–T5) — `_dynamics`, run live by `stress_tests`
| target | claim | key numbers | grade |
|---|---|---|---|
| **T1** | GnRH pulse generator = FHN relaxation oscillator; frequency-decoding | τ_s 20→155 pulses (LH fast) · 150→27 (FSH slow); rate monotone in τ_s | [V] mech / [L] rate |
| **T2** | menstrual cycle = slow relaxation oscillator (not sinusoid) | period 1133.65 arb; rise/fall **asymmetry 309.59** (sinusoid=1.0) | [V] mech / [L] ~28 d |
| **T3** | oestrogen feedback switch: negative → positive LH-surge flip | up-jump 1.634, hysteresis width 0.779; discontinuous | [V] switch |
| **T4** | seminiferous cycle = *intermediate* relaxation clock | τ_s 340 (=600×16/28, ratio anchor); pulse 132 < sperm 656 < menstrual 1134 | [V] order / [L] ~16 d |
| **T5** | puberty onset = discontinuous **spinodal crossing** | state −0.514 → +0.442; jump/spinodal **1.01**; localised at spinodal | [V] mech / [O] calendar age |

### 4.2 Oncology — `_oncology`, exact tilted double well `V(s) = −γs²/2 + s⁴/4 − hs`
- **γ-independence [F]:** `meta_barrier(γ,h)/barrier(γ)` vs `frac=h/spinodal(γ)` identical across γ (**max spread 0.0**):

  | frac | 0.0 | 0.2 | 0.4 | 0.6 | 0.8 | 0.95 |
  |---|---|---|---|---|---|---|
  | ratio | 1.0 | 0.71014 | 0.45804 | 0.24771 | 0.08705 | 0.01083 |
- **Site shapes** (Kramers `RR(dose)=rate(dose)/rate(0)`, noise `NOISE_D=0.15` [O], ratios D-robust):
  breast monotone (per-year 0.024 [L]); prostate concave + **plateau past the fold** (saturation model);
  cervical HPV×smoking **multiplicative at low**, **saturating at high** (falsifiable prediction).

### 4.3 Therapy — `_therapy` (resistance = amplified coupling κ, NOT deeper wells: κ_sens 1, κ_res 3)
| schedule | sensitive stress | resistant stress | res/sens |
|---|---|---|---|
| continuous high T | 0.0036 | 0.0304 | 8.35 |
| continuous low (ADT) | 0.0018 | 0.0043 | 2.36 |
| **cycling (BAT)** | 0.0633 | 0.4125 | 6.52 |

Cycling delivers the **resistant** clone **13.6×** its own continuous-high stress → retrodicts BAT (CRPC) and
LTED-pulse (breast). **GnRH same molecule, opposite effect:** continuous ≥2×spinodal → **0** pulses (suppress);
pulsatile → **41** pulses (activate).

### 4.4 Disease — `_disease` (one drive, two failure modes, one lever)
PCOS fast-τ LH-bias (0.0135 vs 0.00325) and FHA suppressed frequency (0.0025 vs normal 0.0075) are **opposite
ends of one pulse-frequency axis**. Menopause = bistable latch lost on depletion (ON 1.0 → 0.229), irreversible
[O]. 8 disorders total; retrodictions [V]/[L] vs novel hypotheses [O] (see COMPLETION_LEDGER §3).

### 4.5 Germline / gamete battery (G1–G6) — `_germline`, run live by `stress_tests` (added v0.5.0)
The germ cell itself, on the same vendored substrate, with **measured gamete-program promoter γ** (13 genes) as
the only new input. `fetch_germline_gamma.py` receives γ through the identical DNA pipeline (NN-stacking ΔG37,
SantaLucia 1998, promoter TSS−2000..+500, GRCh38.p14); the panel is declared by function before γ is seen, and
is persisted only because **both** anchors reproduce (SOX9 1.4598 **and** DAZL 1.3803). γ is cached
(`inherited/germline_promoters.cache.json`) for offline reproduction.

| target | claim | key numbers | grade |
|---|---|---|---|
| **G1** | meiosis = one replication + **two ordered divisions** | ploidy 2N,2C→2N,4C→1N,2C→1N,1C; order forced by two-stage REC8 release (arm separase 0.684 → centromeric 1.085, shugoshin protection sign) | [V] / [L] / [O] separase kinetics |
| **G2** | gametes are **not identical** | assortment 2²³ = 8,388,608; interference = refractory thinning (Fano 0.108 vs Poisson 0.976; gap CV 0.26; obligate CO); floor 10⁴⁷ | [V] / [L] |
| **G3** | sperm flagellum = the **fast** relaxation oscillator; CatSper = gain switch | 4-clock ladder 26.2<132.45<674.95<1133.65; hyperactivation amp 2.21→2.83 **and** beat 77→57 | [V] / [L] ~20 Hz / [O] integer 9 |
| **G4** | egg = switch **held** at MII; fertilisation = one-way spinodal flip | arrested −1.088; sub-spinodal no-flip, supra-spinodal (>0.3849) flip; polyspermy = past-spinodal irreversibility | [V] / [L] |
| **G5** | γ atlas + **pre-registered** module-separation test | permutation **NULL** (F 0.109, p 0.617) reported honestly; core cluster CV 0.0028 vs panel 0.0253 (p 0.0014) | [V] narrow claim; null reported |
| **G6** | sperm/egg **duality**; symmetric (4) vs asymmetric (1) | oscillator vs held switch; 4 vs 1+3 polar bodies; anisogamy (egg:polar-body 49×, vol ~18,963×) | [V] / [L] size / [O] evolutionary "why" |

**Measured γ atlas (ascending):** TEKT1 1.3400 · NLRP5 1.3475 · MOS 1.3619 · DAZL 1.3803 · CATSPER1 1.4019 ·
DMC1 1.4056 · MLH1 1.4085 · SPO11 1.4105 · PRDM9 1.4165 · ZAR1 1.4226 · DNAH1 1.4469 · ZP3 1.4486 · REC8 1.4525.
γ enters the dynamics **only** where a measured master names a mechanism the substrate already owns
(REC8→cohesin spinodal, CATSPER1→hyperactivation gain, MOS→cytostatic hold); the structural G1–G6 results do
**not** depend on the γ values. The whole battery JSON is byte-identical across runs, and it is folded into
`research_gate()` **separately** from the hashed `circulate()` core (core sha unchanged).

### 4.6 Embryo battery (E1–E6) — `_embryo`, run live by `stress_tests` (added v0.6.0)
The two gametes **meet** and a **fetus** is built, each step a discriminant on the same substrate, reusing
G1–G6 and adding measured developmental master-gene γ (17 genes) as the only new input. Human is **conceptual**
(γ-based gene-clock, not whole-genome synthesis).

| target | claim | key numbers | grade |
|---|---|---|---|
| **E1** | syngamy + **DNA emergence** | sperm flips egg one-way (sub-spinodal does not; polyspermy block); 1N+1N→2N,2C; genome unique to **10⁹⁴** (gamete 10⁴⁷ squared) | [V] / [L] / [O] Ca²⁺ biophysics |
| **E2** | cleavage | 1→2→4→…→64 = 2ⁿ symmetric (vs oogenesis 1+3); mass conserved (cleavage ≠ growth); ICM/TE = R19 switch | [V] / [L] / [O] timing |
| **E3** | ZGA = maternal→zygotic, one-step | OFF on maternal (ZAR1/NLRP5/MOS) → jump 1.6551 @ drive 0.3913 ≈ spinodal 0.3849; handoff | [V] / [L] / [O] ZGA cleavage-stage |
| **E4** | **gene-clock** builds body | order = argsort(spinodal(γ)); **stage test ρ=0.5507, p=0.0200 SUPPORTED**; HOX colinearity partial (posterior-most highest) | [V] / [L] / [O] full atlas (DNA SSOT) |
| **E5** | whole arc → fetus | deterministic sperm+egg → arc all PASS; fetus = unique genome 10⁹⁴ + 17 gene-clock structures, ICM-derived | [V] / [L] / [O] gestational timing |
| **E6** | honest scoreboard + firewall | verified/anchored/open restated; package owns fertilisation + early embryo; atlas + clock law = DNA SSOT | [V] |

**Measured developmental γ atlas (ascending):** NANOG 1.3479 · SOX17 1.3821 · GATA4 1.3933 · HOXB4 1.4453 ·
PAX3 1.4479 · CDX2 1.4500 · SOX2 1.4576 · SOX9 1.4598 · PDX1 1.4732 · POU5F1 1.4874 · HOXA1 1.4923 ·
MYOD1 1.4937 · FOXA2 1.4986 · PAX6 1.5110 · NKX2-5 1.5130 · TBXT 1.5130 · HOXA13 1.5427. **Stage means rise**
(pre-registered): pluripotency 1.4310 < germ-layer 1.4373 < organ 1.4916. γ enters only as the body-plan
emergence order (argsort(spinodal(γ))) and relative size (DWELL); the syngamy/cleavage/ZGA results are
γ-independent. **Firewall:** the gene-clock law + full-body atlas are the DNA 4D-Blueprint package's SSOT
(cited). Battery JSON byte-identical (`bdf77110…`); folded into `research_gate()` separately from the hashed
core (core sha unchanged).

### 4.7 Fertility battery (F1–F6) — `_fertility`, run live by `stress_tests` (added v0.7.0)
Why conception **fails**, drawing the clinic's distinction in substrate terms: **infertility = an operation
past a spinodal** (categorical, per-cycle p=0, a sub-threshold drive does nothing); **subfertility = an
operation near its threshold** (a finite Kramers rate per cycle, moved exponentially by the same drive).
Reuses the same R19 spinodal + the oncology `exp(−ΔV/D)`, the measured gamete-machinery γ, and the §9 therapy
result; no new γ.

| target | claim | key numbers | grade |
|---|---|---|---|
| **F1** | conception = **AND** of substrate gates | 8-link chain; any single gate 0 ⇒ conception 0 (one broken link = sterility) | [V] / [F] / [O] per-link rates |
| **F2** | **infertility past a spinodal / subfertility near threshold** | subfertile 0.039→0.061 per fixed nudge (**1.56×**), p/yr 0.38→0.53; sterile (1.6·h_sp) p=**0**, same nudge → **0** | [V] dissociation / [L] / [O] absolutes |
| **F3** | male = oscillator **throughput** + CatSper gate | azoospermia = switch **off**; throughput 51→7 beats; CatSper γ 1.4019 a separate supra-spinodal gate | [V] / [L] WHO / [O] param→drive |
| **F4** | female = surge switch + **REC8 cohesin fatigue** | anovulation = surge off; mis-segregation **0.121→0.752** age 25→45 (barrier γ²/4·cohesin decays); POI = early latch loss | [V] / [L] REC8 γ + anchor / [O] absolute fraction |
| **F5** | treatment = a **drive** (kick/restart/bypass) | hCG = supra-spinodal kick; pulsatile GnRH 41 vs 0 (cited §9); ICSI/IVF = gate bypass | [V]/[L] / [O] schedules |
| **F6** | honest scoreboard + firewall | verified/anchored/open; clinical management firewalled | [V] |

Constants set once (D=0.25, fecundability=0.20, subfertile deficit 0.85·h_sp), never tuned. Folded into
`research_gate()` separately from the hashed core (core sha unchanged).

### 4.8 Sex-ratio battery (S1–S6) — `_sexratio`, run live by `stress_tests` (added v0.7.0)
How a gene biases offspring toward one **sex**: sex itself is the **SOX9↔FOXL2 R19 bistable** (SRY the drive),
**Mendel** is that switch **untilted** (a fair coin), **meiotic drive** is a **tilt** (fixing past the
spinodal), **sex-ratio distortion** is the same tilt **with a sign** (X-shredder → male, Y-killer → female),
and **Fisher** holds the population at 1:1. Adds measured sex-determination master-gene γ (6 genes) as the only
new input.

| target | claim | key numbers | grade |
|---|---|---|---|
| **S1** | sex = one **bistable** switch (SOX9↔FOXL2), SRY the drive | equal basins at h=0; SRY transient supra-spinodal flip that **holds**; transdifferentiates only supra-spinodal | [V] / [L] SOX9+FOXL2 γ |
| **S2** | Mendel 50:50 = **untilted** segregation switch | 20 000-meiosis ensemble **0.4983** (analytic 0.50) — fair coin | [V] |
| **S3** | distortion = a **tilt** (graded → supra-spinodal fix) | TR 0.50 → 0.86 (sub) → **1.0** (supra; t-haplotype/SD limit) | [V] / [L] anchor |
| **S4** | sex-ratio distortion = **signed** sex-chromosome killer | X-shredder SSR **1.0** (male), Y-killer **0.0** (female), weak 0.82 (partial) | [V] / [L] anchor |
| **S5** | **Fisher** 1:1 = stable attractor | returns to 0.50 from 0.20/0.80; weak drive shifts to 0.5125; human SSR ~0.512 = small residual | [V] / [L] human SSR |
| **S6** | γ atlas + axis-separation test (**honest null**) | ovary > testis (1.5163 vs 1.3857) but SRY a strong outlier, n=3/axis, **permutation p=0.10 → not significant** | [V] test reported / [O] separation open at this n |

**Measured sex-determination γ atlas (ascending):** SRY **1.2550** (AT-rich outlier) · DMRT1 1.4423 ·
SOX9 1.4598 · RSPO1 1.4669 · FOXL2 1.4829 · WNT4 1.5992. Anchors SOX9+FOXL2 reproduce; cache offline-verified
bit-for-bit. The S6 null is reported **as it falls** — the chapter's verified claims do not depend on it.
Folded into `research_gate()` separately from the hashed core (core sha unchanged).

## 5. 재현 규약 (reproducibility — VP-SPEC C1)
- `SEED=19`; BLAS pinned single-thread at the top of every module; round-before-hash (8 dp); sorted JSON keys.
- `circulate()` is the hashed deterministic core → `emit()` returns identical sha256 on repeat (2×, byte-
  identical, process-stable):
  **`f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4`** (v0.3.0).
  - The core hash changed legitimately at v0.3.0: the organ-emergence section now carries measured γ for all
    four organs and a four-element developmental order (was one vendored organ + three deferred). This is a
    **science** change, not science-neutral infra. Prior core (v0.2.0): `974effe2…`.
- **γ reception is offline-reproducible:** `python repro/_gamma/fetch_gamma.py` (no flag) recomputes γ for all
  four masters from `inherited/organ_promoters.cache.json` and asserts agreement with `organ_gamma.json` plus
  the SOX9 anchor — no network needed. `--fetch` re-pulls from NCBI and rebuilds the cache (how it was built).
- Research-module statuses are aggregated in `gates.research_gate()` **separately** from the hashed core, so
  adding modules does not perturb the core hash.

## 6. 무튜닝 규율 (no-tuning — VP-SPEC, strict)
Every constant is a **measured input or a derived value, never chosen to hit a target**. τ_s sets a period, but
periods are **[L] anchors** — the package never claims to *derive* a clinical timing. `NOISE_D`, `per_year`, κ,
amplitude fractions are **stated inputs**, never fitted. All RR **ratios** are invariant to `NOISE_D` (declared
[O]). γ for FOXL2/DAZL/WT1 was **received** via the identical DNA `fetch_morpho_gamma` pipeline (NN-stacking
ΔG37 on the cited promoter, GRCh38) and cached — a measurement, accepted only because it reproduces the SOX9
anchor (1.4598/0.545) bit-for-bit; never fitted.

## 7. 집필 잠금 (writing lock — research first) — **해제됨 (v0.4.0)**
`tools/build_docs.py` **refuses** while `gates.writing_locked()` is True. Unlock requires **all three**, and as
of v0.4.0 **all three are met**:
1. `research_gate()` → `all_green == true`  (**true**),
2. `gates.write_research_complete()` → `reports/research_complete.json` written (**done**),
3. root `PHASE` set to `writing`  (**done** — was `research`).

`gates.writing_locked()` now returns `(False, "writing unlocked")`. The lock is **mechanism, not ceremony**: the
research gate is still evaluated on every build, so if any module regressed the build would refuse again.

## 8. 집필 단계 (writing phase — VP-SPEC v1.8 canonical site)
```bash
python tools/build_docs.py        # → docs/ (idempotent; two builds are byte-identical)
```
**What it emits**: `docs/index.html` (hub) · 14× `docs/<slug>/index.html` (one page per section, incl. §11 the
gamete, §12 the embryo, §13 fertility, §14 sex) · 28× `docs/eq/*.svg` (canonical display equations) ·
`docs/_meta.json` (§9 summary card) ·
`docs/sitemap.xml` · `docs/robots.txt` (7 bots) · `docs/llms.txt` (<5 KB) · `docs/assets/css/site.css` · plus the
per-chapter `manifest/…csv`.

**Conformance (VP-SPEC §6) baked into every page:** answer-first 40–60-word `<p class="answer">`, abstract,
`claim-strip` (grade + LOCK→Derive→Gate + GitHub repro + DOI), one `vp-card` per cited locked quantity, two
JSON-LD blocks (`ScholarlyArticle` + `BreadcrumbList`), `<link rel=canonical>`, external CSS only, prev/next nav.

**Anti-drift (C1):** the builder imports the research modules and pulls **every** number live at build time —
nothing is transcribed by hand. Equations render to SVG with a fixed `svg.hashsalt` and suppressed Date metadata,
so the SVGs are byte-stable. A built-in self-check writes `reports/writing_gate.json` (currently **84/84 PASS**;
the chapter-count check is count-agnostic, so adding chapters does not require editing the gate).

**DOI honesty (C1/C3):** this package has no Zenodo deposit yet, so its own DOI is rendered as
`pending Zenodo deposit` everywhere — never invented. Only the real sibling DOIs (VP Theory, 4D DNA) are cited,
inside the vp-cards. The first deliberate next step after this phase is the Zenodo deposit + DOI mint.

**DOI (C1/C3):** the package DOI is the **Zenodo concept DOI `10.5281/zenodo.20754657`** — version-independent
and always resolving to the latest version, so it is the correct identifier to cite. It is rendered as a
clickable link everywhere (claim-strip, footer, `_meta.json`, `llms.txt`). Per-version DOIs are not used as the
package identifier. If the deposit is ever re-keyed, swap the one `DOI` constant in `build_docs.py` (and
`build_paper.py`) and rebuild — the whole site + paper follow. Only real sibling DOIs (VP Theory, 4D DNA) are
cited inside the vp-cards.

### 8b. LaTeX whitepaper + PDF (v0.4.1 body; §11–§14 added through v0.7.1)
```bash
python tools/build_paper.py                                   # → paper/reproductive_endocrine_vp.tex (live numbers)
cd paper && latexmk -pdf -interaction=nonstopmode reproductive_endocrine_vp.tex   # → .pdf (15 pp)
```
`build_paper.py` is the LaTeX twin of `build_docs.py`: it imports the same modules and interpolates every
number live, so the **PDF cannot drift from the engine**. The `.tex` uses no `\today` (the title page carries
the fixed version + DOI), so it is byte-identical across runs; the `.pdf` is the `pdflatex` compile. The three
Zenodo upload files are the `.tex`, the `.pdf`, and the reproducibility archive (this whole package). As of
**v0.7.1** the whitepaper carries all sixteen numbered sections — including §11 the gamete, §12 the embryo,
§13 infertility/subfertility, and §14 sex determination & sex-ratio distortion — so the PDF is a faithful,
drift-proof mirror of the canonical HTML site (C2); no chapter lags behind.

This remains a falsifiable, deterministic, honestly graded research artefact. **Not clinical advice.**
