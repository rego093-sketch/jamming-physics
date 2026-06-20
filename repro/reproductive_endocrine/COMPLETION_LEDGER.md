# COMPLETION LEDGER — Reproductive / Gonadal-Endocrine (`reproductive_endocrine_vp_site`) · v0.7.1-writing

> 무엇을 완료했고, 무엇이 어떤 등급으로 잠겼으며, 무엇이 아직 열려 있는지의 단일 기록.
> 등급은 정직성 표기다: `[V]` sim-verified · `[L]` measured-anchor · `[F]` forced · `[O]` open(장애물 명시).

---

## 1. Gate status (machine-checked)
| check | result |
|---|---|
| determinism (2× sha256 identical) | **PASS** — `f849da7d13d233020b3f4051867307c7523c42f9ae485359113a33b55f6a94a4` |
| organ emergence (4/4 measured γ, none deferred) | **PASS** |
| γ reception offline reproduction (organ cache + SOX9 anchor) | **PASS** — `fetch_gamma.py verify()` all true |
| **germline γ reception** (gamete cache + SOX9 & DAZL anchors) | **PASS** — `fetch_germline_gamma.py verify()` all true |
| **embryo γ reception** (developmental cache + SOX9 & DAZL anchors) | **PASS** — `fetch_embryo_gamma.py verify()` all true |
| **sex-determination γ reception** (sexdet cache + SOX9 & FOXL2 anchors) | **PASS** — `fetch_sexratio_gamma.py verify()` all true |
| T1–T5 discriminant battery | **PASS** (all 5) |
| **G1–G6 gamete battery** | **PASS** (all 6) — `gametogenesis.py` |
| **E1–E6 embryo battery** (fertilisation→fetus) | **PASS** (all 6) — `embryogenesis.py` |
| **F1–F6 fertility battery** (infertility/subfertility) | **PASS** (all 6) — `infertility.py` |
| **S1–S6 sex-ratio battery** (sex determination + distortion) | **PASS** (all 6) — `sex_ratio.py` |
| oncology dose-response | **PASS** |
| therapy temporal-pattern | **PASS** |
| disease mechanism layer | **PASS** |
| **research_gate all_green** | **TRUE** (`emergence · stress(T+G+E+F+S) · germline · embryo · fertility · sexratio · oncology · therapy · disease`) |
| writing_locked | **FALSE** (`PHASE == writing`, research signed off — unlocked v0.4.0) |
| **writing_gate (VP-SPEC §6 conformance)** | **105 / 105 PASS** — `reports/writing_gate.json` |
| `docs/` two-build determinism | **PASS** — byte-identical |

`reports/research_complete.json` written with `all_green: true` (now incl. `germline_pass`, `embryo_pass`, `fertility_pass`, `sexratio_pass` — all true).
`reports/writing_gate.json` written with `all_pass: true`.

## 1·E. v0.6.0 — the embryo: fertilisation → fetus (E1–E6)
The gamete battery stopped at the gamete; v0.6.0 lets the two gametes **meet** and builds a **fetus**, each
step a discriminant on the same substrate, reusing G1–G6 and adding **measured developmental master-gene γ**
(17 genes) as the only new input. The hashed core is unchanged (`f849da7d…`). Human is treated **conceptually**
(a γ-based gene-clock, not whole-genome synthesis).

| deliverable | grade | note |
|---|---|---|
| `repro/_embryo/fetch_embryo_gamma.py` | [V]/[L] | 17-gene developmental γ reception (same NN-dG37 pipeline); panel declared by stage/HOX before γ seen; SOX9+DAZL anchors gate persistence; offline `verify()` bit-for-bit |
| `inherited/embryo_promoters.cache.json` + `embryo_gamma.json` | [L] | cached promoters (2501 bp) → offline reproduction; stage means rise 1.4310<1.4373<1.4916 |
| `repro/_embryo/embryogenesis.py` (E1–E6) | [V]/[L]/[O] | all 6 PASS; deterministic `bdf77110…`; syngamy/cleavage/ZGA/gene-clock/arc/scoreboard |
| `inherited/embryo_identity.md` | — | seam note: received-from-DNA read-only, γ usage, pre-registered tests, **firewall** |
| gate wiring (`stress_tests.py`, `gates.py`, `run_all.py`) | — | E1–E6 in `all_targets_pass`; `embryo_all_pass`/`embryo_pass` surfaced; run_all §[3] prints embryo + developmental atlas |
| HTML chapter §12 + hub headline + 5 eqs (`build_docs.py`) | [V] | `12-embryogenesis-fertilisation-to-fetus`; **12 ch · 7939 words · 18 eqs**; writing-gate **91/91**; 2-build byte-identical |
| PDF `sec_embryo` + 2 open rows (`build_paper.py`) | [V] | live numbers; **10→12 pp**; `.tex` byte-identical; 0 unresolved refs |

**Key E-series results:** E1 genome unique to 10⁹⁴ (gamete 10⁴⁷ squared), 1N+1N→2N exact, polyspermy block;
E3 ZGA one-step jump 1.6551 at drive 0.3913 ≈ spinodal 0.3849; **E4 pre-registered stage test ρ=0.5507,
p=0.0200 → SUPPORTED**; HOX colinearity partial (posterior-most highest, ρ=0.50) reported honestly; E5 fetus =
unique genome + 17 gene-clock-ordered structures, ICM-derived. Firewall: package owns fertilisation + early
embryo; full-body atlas + gene-clock law = DNA 4D-Blueprint SSOT (cited).

## 1·F. v0.7.0 — infertility/subfertility (F1–F6) + sex determination & sex-ratio distortion (S1–S6)

Two new **separate** HTML parts the user asked for: why conception **fails** (불임/난임), and how a gene biases
offspring toward one **sex** (성별 쏠림). Two new modules, each a discriminant battery on the same substrate,
reusing the gamete/embryo/therapy results and adding measured **sex-determination** master-gene γ (6 genes) as
the only new input. The hashed core is unchanged (`f849da7d…`).

**Two theses:** infertility = an operation **past a spinodal** (categorical, per-cycle p=0, immovable by a
sub-threshold drive) vs subfertility = an operation **near threshold** (a finite Kramers rate moved
exponentially by the same drive); and sex = the **SOX9↔FOXL2 R19 bistable**, Mendel = it untilted (fair coin),
meiotic drive = a tilt (fixing past the spinodal), sex-ratio distortion = the same tilt **with a sign**, Fisher
= a 1:1 population attractor.

| deliverable | grade | note |
|---|---|---|
| `repro/_fertility/infertility.py` (F1–F6) | [V]/[L]/[O] | all 6 PASS; chain-AND, the categorical/Kramers dissociation (1.56× vs 0), male oscillator-throughput, female surge-switch + REC8 cohesin fatigue (mis-segregation 0.121→0.752 age 25→45), treatment-as-a-drive, scoreboard; constants set once, never tuned |
| `repro/_sexratio/fetch_sexratio_gamma.py` | [V]/[L] | 6-gene sex-determination γ reception (same NN-dG37 pipeline); panel declared by axis before γ seen; SOX9+FOXL2 anchors gate persistence; offline `verify()` bit-for-bit |
| `inherited/sexdet_promoters.cache.json` + `sexdet_gamma.json` | [L] | cached promoters → offline reproduction; SRY 1.2550 (AT-rich outlier) … WNT4 1.5992; testis mean 1.3857 < ovary mean 1.5163 |
| `repro/_sexratio/sex_ratio.py` (S1–S6) | [V]/[L]/[O] | all 6 PASS; bistable sex switch, Mendel fair coin (0.4983), drive-as-tilt (→1.0 supra-spinodal), signed SSR skew (X-shredder 1.0 male / Y-killer 0.0 female), Fisher 1:1, γ atlas + **honest null** (axis-separation permutation p=0.10) |
| gate wiring (`stress_tests.py`, `gates.py`, `run_all.py`) | — | F1–F6 + S1–S6 in `all_targets_pass` (29 suites); `fertility_all_pass`/`sexratio_all_pass` + `fertility_pass`/`sexratio_pass` surfaced; run_all §[3] prints both batteries + sex-determination atlas |
| HTML chapters §13 + §14 + 2 hub headlines + 10 eqs (`build_docs.py`) | [V] | `13-infertility-and-subfertility`, `14-sex-determination-and-sex-ratio-distortion`; **14 ch · 10078 words · 28 eqs**; writing-gate **105/105**; 2-build byte-identical; `llms.txt` rewritten for 14 ch, <5 KB |

**Verification:** `research_gate()` ALL_GREEN, `result_sha256` = `f849da7d13d2…` **unchanged**, 29 suites PASS,
battery determinism identical; `build_docs.py` 14 pages / 28 eqs / 105-105.

**Open (tracked) → CLOSED in v0.7.1:** `paper/*.tex` (build_paper.py) is now extended to §13/§14 (see §1·F2
below). The genuine open quantities remain **[O]**: all absolute per-cycle probabilities, the semen/age→drive
map, the human sex-ratio residual's cause, azoospermia/POI gene→γ links, and whether the sex axis separates γ
at n=3/axis.

## 1·F2. v0.7.1 — distribution sync: whitepaper extended to §13 + §14 (paper catches up to the canonical HTML)

v0.7.0 left the PDF whitepaper at its v0.6.0 body (gamete + embryo only); the §13/§14 theses lived only in the
canonical HTML (C2). v0.7.1 closes that tracked item by extending `tools/build_paper.py` with two live-number
section generators, so the PDF mirrors the HTML and **cannot drift from the engine**. **No science changed** —
the hashed core is identical (`f849da7d…`); this is a writing/distribution-layer patch, the analogue of v0.4.1.

| deliverable | grade | note |
|---|---|---|
| `sec_infertility(D)` (`build_paper.py`) | [V]/[L]/[O] | live: chain-AND of 8 ops; the spinodal/Kramers dissociation **table** (subfertile 0.0391→0.0610, **1.56×**, year 0.381→0.530; sterile 0/0/—); male/female factor (51→7 beats; CatSper γ 1.4019; REC8 γ 1.4525; mis-seg 0.121→0.752); Rx-as-drive (41 vs 0 pulses) |
| `sec_sexratio(D)` (`build_paper.py`) | [V]/[L]/[O] | live: SOX9 1.4598↔FOXL2 1.4829 bistable + SRY hysteresis; Mendel untilted (20,000 meioses → 0.4983); drive-as-tilt 0.50→0.8623→1.0; signed SSR (X-shredder 1.0 / Y-killer 0.0 / partial 0.8223); Fisher 1:1 (0.5125 bounded; human 0.512); γ atlas **table** + **honest null** (axis-sep permutation p=0.10) |
| `sec_open(D)` +5 rows (`build_paper.py`) | [O] | per-cycle conception prob; per-age aneuploidy fraction; meiotic-drive/sex-ratio tilt magnitude; cause of human ~0.512 ratio; axis separation of sex-determination γ at n=3 — each with its obstacle (VP-SPEC C3); open table now 12 rows |
| abstract + keywords + bibliography | — | abstract gains one downstream-arc sentence; keywords extended; **Fisher 1930** added (`{9}`→`{10}`) |
| `paper/reproductive_endocrine_vp.tex` | [V] | **37,656 → 47,476 chars**; no `\today` → **byte-identical across two builds** (sha `3d5f5c64…`); title page Version **0.7.1-writing**, concept DOI unchanged |
| `paper/reproductive_endocrine_vp.pdf` | [V] | recompiled **clean** (`pdflatex`/`latexmk`, **0 unresolved refs/citations**), **12 → 15 pp**, A4; §13/§14 + Tables 11–13 render |

**Verification:** `python repro/run_all.py` → **ALL_GREEN: True**, `result_sha256` = `f849da7d13d2…` **unchanged**
(2× identical), WRITING UNLOCKED; γ offline `verify()` `ok: true`. `docs/` **untouched** (embeds no version
string) — §11–§14 chapters and the **105/105** writing-gate stand exactly as in v0.7.0. HTML remains canonical
(C2); the PDF is now a faithful, drift-proof mirror.

## 1a. Writing phase — completed (v0.4.0): canonical VP-SPEC v1.8 HTML site
The deliberate writing decision was taken (research green + `write_research_complete()` + `PHASE=writing`), and
`tools/build_docs.py` — the stub the research phase existed to unlock — was implemented and run. It emits a
per-title canonical site whose every number is pulled **live** from the research engine at build time, so the
site cannot drift from the code; two full builds are **byte-identical**. The hashed research core is unchanged.

| deliverable | grade | note |
|---|---|---|
| 10 chapter pages (`docs/<slug>/index.html`) | [V]/[F] | answer-first, JSON-LD ×2, canonical, claim-strip, vp-cards, prev/next; English body |
| hub (`docs/index.html`) | — | lede, one-drive/two-failures/one-lever thesis, 6 live headline results, graded TOC, `CreativeWorkSeries`+`BreadcrumbList` |
| 8 display equations (`docs/eq/*.svg`) | — | canonical rendered SVG, byte-stable (fixed hashsalt, no Date) |
| `_meta.json` · `sitemap.xml` · `robots.txt` (7 bots) · `llms.txt` (<5 KB) | — | retrieval-readiness (VP-SPEC §6/§9) |
| `site.css` · per-chapter manifest CSV | — | external stylesheet; manifest computed from emitted HTML (builder = SSOT) |

Totals: **10 chapters · ~5000 words · 8 equations**; per-page grades §1[F] §2–§7[V] §8[F] §9–§10[V].

## 1a-2. Zenodo deposit prep — completed (v0.4.1): DOI + LaTeX/PDF whitepaper
The Zenodo **concept DOI `10.5281/zenodo.20754657`** (version-independent, always resolving to the latest
version) is now baked in everywhere (clickable link in
claim-strip, footer, `_meta.json`, `llms.txt`); the honest `pending` marker is gone. A canonical **LaTeX
whitepaper** (`tools/build_paper.py`, live numbers, no `\today` → byte-identical `.tex`) was generated and
compiled to **PDF (9 pp, A4, `pdflatex`-clean, 0 unresolved refs)**. The three Zenodo upload files are the
`.tex`, the `.pdf`, and the reproducibility archive (the whole package). Core sha unchanged (`f849da7d…`).

| deposit file | grade | note |
|---|---|---|
| `paper/reproductive_endocrine_vp.tex` | — | LaTeX source, ~28.5 KB, deterministic (no build timestamp) |
| `paper/reproductive_endocrine_vp.pdf` | — | compiled whitepaper, 9 pp, colour grade badges, linked DOI/ORCID, 9-ref bibliography |
| reproducibility archive (`…_v0_4_1.zip`) | — | full package: engine + cache + both generators + docs + paper |

## 1b. Organ emergence — γ reception completed (v0.3.0)
FOXL2 / DAZL / WT1 received via the identical DNA `fetch_morpho_gamma` pipeline (NN-stacking ΔG37, SantaLucia
1998, promoter TSS-2000..+500, GRCh38); all four organs now emerge with measured γ. Measured input, never
fitted — accepted only because the pipeline reproduces the vendored SOX9 anchor (γ=1.4598, GC=0.545) bit-for-
bit; promoter sequences cached for offline reproduction.

| master | organ | γ | GC | grade |
|---|---|---|---|---|
| DAZL | germline | 1.3803 | 0.479 | [V] measured |
| SOX9 | gonad_testis | 1.4598 | 0.545 | [V] measured (anchor) |
| FOXL2 | gonad_ovary | 1.4829 | 0.575 | [V] measured |
| WT1 | reproductive_tract | 1.5182 | 0.601 | [V] measured |

Developmental order (γ ascending): germline → gonad_testis → gonad_ovary → reproductive_tract **[V]**.

## 2. Discriminant battery (T1–T5) — completed
| target | result | grade |
|---|---|---|
| T1 GnRH pulse generator + frequency-decoding (τ_s monotone) | PASS | [V] mech; [L] rate |
| T2 menstrual slow relaxation (asymmetry 309.59) — *PASS-criterion fixed (rise/fall asymmetry)* | PASS | [V] mech; [L] ~28 d |
| T3 oestrogen feedback switch (discontinuous flip + hysteresis 0.779) | PASS | [V] switch |
| T4 seminiferous intermediate clock (τ_s 340; pulse < sperm < menstrual) | PASS | [V] order; [L] ~16 d |
| T5 puberty spinodal crossing (state −0.514 → +0.442; jump/spinodal 1.01) | PASS | [V] mech; [O] calendar age |

## 2b. Germline / gamete battery (G1–G6) — completed (v0.5.0)
The germ cell itself, emerged on the same substrate. New module `repro/_germline/`: `fetch_germline_gamma.py`
(measured gamete-program promoter γ — 13 genes, identical NN-stacking ΔG37 pipeline, panel declared by function
before γ seen, persisted only because **both** anchors SOX9 1.4598 and DAZL 1.3803 reproduce; cached for offline
bit-for-bit) and `gametogenesis.py` (the G1–G6 discriminant battery, vendored substrate + measured γ only,
deterministic, each `[O]` carries its obstacle). Folded into `research_gate()` via `stress_tests`; the hashed
`circulate()` core is **unchanged**.

| target | claim | result | grade |
|---|---|---|---|
| **G1** | meiosis = one replication + two **ordered** divisions (reductional→equational) | PASS — ploidy 2N,2C→1N,1C; order forced by two-stage REC8 release (arm sep. 0.684 → centromeric 1.085) | [V] mech; [L] REC8 γ / shugoshin magnitude; [O] separase kinetics |
| **G2** | gametes are **not** identical | PASS — assortment 2²³ = 8,388,608; interference = refractory thinning (Fano 0.108 vs Poisson 0.976, gap CV 0.26, obligate CO); floor 10⁴⁷ | [V]; [L] map-length anchors |
| **G3** | sperm flagellum = fast relaxation oscillator; CatSper = gain switch | PASS — ladder 26.2<132.45<674.95<1133.65; hyperactivation amp 2.21→2.83 **and** beat 77→57 | [V]; [L] ~20 Hz; [O] integer 9 of 9+2 axoneme |
| **G4** | egg = switch **held** at MII; fertilisation = one-way spinodal flip | PASS — arrested −1.088; sub-spinodal no-flip, supra-spinodal (>0.3849) flip; polyspermy = past-spinodal irreversibility | [V]; [L] drive magnitudes |
| **G5** | gamete-program γ atlas + **pre-registered** module-separation test | PASS (module) — permutation **NULL** (F 0.109, p 0.617) reported honestly; core cluster tight (CV 0.0028 vs 0.0253, p 0.0014) | [V] narrow claim; null reported |
| **G6** | sperm/egg duality; symmetric (4) vs asymmetric (1) | PASS — oscillator vs held switch; 4 vs 1+3 polar bodies; anisogamy (egg:polar-body 49×, vol ~18,963×) | [V]; [L] size anchor; [O] evolutionary "why" |

**The unifying gamete claim:** one substrate yields two opposite gametes — a free-running oscillator (motile
sperm) and a held switch (waiting egg); and crossover **interference is the substrate's refractory period**
mapped from time onto the chromosome axis (the same mechanism that regularises FHN spikes). The four user
questions — how gametes are made, whether they are identical, sperm motility, egg logic — are answered in order
as G1–G4, with G5 (measured γ + honest null) and G6 (the duality) closing the chapter.

## 2c. Gamete chapter §11 + paper section — completed (v0.5.0)
Canonical HTML chapter **`11-gametogenesis-the-gamete-itself`** ("The gamete itself: meiosis, motility and the
egg") added via `build_docs.py` (answer-first, meiosis ploidy table, γ-by-module table, honest-null narrative,
5 new display equations `rep-gmt-001..005`, a 6th index headline). Site now **11 chapters · 6417 words · 13
equations**, writing-gate **84/84**, two builds byte-identical. The LaTeX whitepaper grew a matching
`sec_gamete` (live numbers); PDF recompiled **9 → 10 pp**, `pdflatex`-clean, 0 unresolved refs; `.tex`
byte-identical across runs.


## 3. Disease mechanism + better-treatment layer — completed (8 disorders)
*Format: disorder → substrate failure → current Rx as a substrate move → VP-derived hypothesis (grade).*
Existing clinical approaches the framework **retrodicts** are flagged as validation; genuinely novel predictions
are graded **[O]** and explicitly need clinical validation. **None of this is clinical advice.**

| disorder | substrate failure | VP-derived better-treatment hypothesis | grade |
|---|---|---|---|
| PCOS (anovulatory) | GnRH pulse frequency too **high** → LH:FSH tips to LH; follicle stalls | restore a **slower** pulse pattern rather than only blunting androgen | **[O]** novel pattern-restoration; FSH-raising drugs are the [L]/[V] retrodiction |
| Functional hypothalamic amenorrhoea | pulse frequency suppressed **below** ovulatory threshold (generator intact) | **energy/tone restoration** is primary; pulsatile-GnRH pump as bridge | **[V]/[L]** retrodicts pulsatile-GnRH |
| Menopause / perimenopause | follicle-pool exhaustion removes the bistable secretory **latch** (irreversible) | HRT is **replacement, not restoration**; the secretory substrate is depleted | **[O]** irreversibility is the obstacle; HRT-as-replacement is [L] |
| Age-related male hypogonadism | sustained androgen drive low | **pulsed/cycled** TRT to avoid the suppression/desensitisation trade-off | **[O]** novel; the trade-off itself is the [V] structural prediction |
| Central precocious puberty | T5 spinodal crossed too early | **continuous** GnRH-agonist depot = depolarisation-block suppression | **[V]** retrodiction (continuous = suppression) |
| Delayed puberty (functional) | T5 crossing not yet reached | **pulsatile** GnRH = activation (opposite schedule to CPP) | **[V]** retrodiction (pulsatile = activation) |
| Anovulatory infertility (surge failure) | mid-cycle surge switch fails to flip | **hCG trigger = a spinodal kick** across the switch | **[V]/[L]** retrodicts the hCG trigger |
| Endometriosis (oestrogen-dependent) | oncogenic-analogue sustained oestrogenic drive | **continuous** GnRH-agonist suppression is correct for a suppression goal | **[V]** retrodiction (continuous suppression) |

**Unifying thesis (the high-ambition payoff):** one drive `h`, moved two opposite ways. Lower the barrier → the
R19 oncogenic switch (every HRT/TRT carries a cancer-risk signature). Supply the wrong *pattern* → an HPG
oscillator disease (every anti-hormone cancer Rx carries hypogonadal effects). The single control axis the
framework exposes is **temporal pattern** (pulsatile / cycling), which retrodicts pulsatile-GnRH,
GnRH-agonist desensitisation, the hCG trigger, BAT, the LTED pulse, the saturation model, and HPV×smoking
multiplicativity.

## 4. Oncology — completed
- γ-independence of the barrier law **[F]** (max spread 0.0). Site shapes **[V]**: breast monotone, prostate
  concave + plateau, cervical multiplicative-low / saturating-high (**falsifiable**: synergies saturate at high
  exposure). Anchors **[L]**; absolute incidence **[O]**.

## 5. Therapy — completed
- Cycling selectivity (resistant fold 13.6×) and GnRH same-molecule-opposite-effect (41 vs 0 pulses).
  Principle **[V]**; clinical schedule **[O]**.

## 6. Open items (carried, each with obstacle in IRREPRODUCIBILITY_LEDGER)
| item | grade | next step |
|---|---|---|
| ~~FOXL2 / DAZL / WT1 γ~~ | **[V] DONE (v0.3.0)** | received via `fetch_morpho_gamma` pipeline (measured, cached, offline-reproducible); all four organs emerge with real γ — see §1b |
| absolute organ size / mass | [O] | external calibration (relative order is [F]) |
| absolute cancer incidence | [O] | epidemiological calibration (RR shape is [V]) |
| NOISE_D absolute RR magnitude | [O] | single lattice constant; all **ratios** already D-robust |
| chronological pubertal age (T5) | [O] | external endocrine calibration (discontinuous order is [V]) |
| menopause irreversibility | [O] | no in-package follicle regeneration; asserted from biology |
| novel hypotheses (low-freq pulsatile PCOS; pulsed/cycled TRT) | [O] | clinical validation — **not** clinical advice |

## 7. Done this phase / next phase
- **Germline / gamete emergence** (`repro/_germline/`, G1–G6 + measured gamete-program γ) — **DONE (v0.5.0)**.
  Six-target battery all PASS, folded into the research gate; canonical HTML chapter §11 + paper `sec_gamete`;
  core hash unchanged. See §2b/§2c. This answered the user's four germ-cell questions directly.
- **Writing** (canonical HTML via `tools/build_docs.py`) — **DONE (v0.4.0; extended v0.5.0 to 11 chapters,
  84/84)**. See §1a.
- **Zenodo deposit prep** — **DONE (v0.4.1)**. Zenodo **concept DOI `10.5281/zenodo.20754657`** (version-independent)
  baked in; LaTeX whitepaper + 9-page PDF generated; three upload files ready (`.tex`, `.pdf`, reproducibility
  archive). See §1a-2.
- **Next deliberate step — perform the actual Zenodo upload.** Upload the three files under the concept DOI
  `10.5281/zenodo.20754657`. The concept DOI is version-independent and already baked into every artefact, so no
  DOI swap is needed on publish. If the deposit is ever re-keyed, change the one `DOI` constant in
  `build_docs.py` and `build_paper.py` and rebuild both (site + paper follow automatically); never invent a DOI (C1/C3).
- **Optional research expansion** (unchanged, research-discipline): more carcinogen anchors, endometriosis
  progression dynamics, pulsed-TRT schedule sweeps — these re-enter the research gate, not the writing one.
