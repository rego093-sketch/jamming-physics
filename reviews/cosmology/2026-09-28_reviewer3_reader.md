# Cosmology volume — Reviewer 3 of 3 (the reader's lens)

Date: 2026-09-28 · Scope: `docs/cosmology/index.html` + 42 topic pages · No files under `docs/` or `repro/` were edited.
Method: I read the hub, chapters 0, 1, 6, 6.1, 7 and 7.1 closely. I skimmed chapters 2–5 and 8–15 and appendices C, F, G and J, and read closely wherever a problem showed up. I checked the prev/next chain against the hub order, looked for unescaped `<` in the HTML, and searched every page for raw LaTeX left in the text.

Target reader: an ordinary AI or educated non-specialist reading once, top to bottom.

Severity scale: **critical** means a reader is misled or loses content. **major** means a reader cannot follow a step or gets two different answers. **minor** means friction or polish.

---

## A. The headline a₀ = cH₀/2π: motivation and status

### R3-01 · critical · 06-galactic-rotation-derivation-a0-ch0, 06-why-…, 16-open-problems-gathered, axf-…, axj-…: the 2π is called "derived", "closed", "forced" and "a modelling choice" at once
Evidence:
- Ch 6 step 4: "This 2π is the wave-cycle factor, and in this framework it is **derived**, not inserted." Later in the same step: "What remains **a modelling choice**, honestly flagged … is the identification of the relevant length as the full wavelength λ_bg rather than the reduced ƛ = R_H (which would give the bare cH₀); the wave picture and **the 90% empirical match** support the full-cycle reading."
- Ch 6.1: "the empirical scale independently places the coefficient in the consistent band k≈5–7".
- App J, reclassification row #3: "Origin of 2π | open | **closed**".
- App F scorecard: a₀ graded "\textsf{[F]}" (forced). The executive summary says "the inflow-circulation geometry **forces** the galactic acceleration scale".

A reader is given three different justifications for the same 2π:
1. one wave cycle (λ = 2π/κ);
2. the ratio of two "cosine-integral rectification constants", α/δ = (2/π)/(1/π²);
3. "inflow-circulation geometry" in App F.

The reader is also told that the choice between cH₀ and cH₀/2π was supported by which one matches the data better. That selection step is the one a sceptical reader will call a fit, and the volume's own rule ("why this and not that", Ch 0) is not applied to it.

Fix:
- State one reason for the 2π and keep it identical on every page.
- Grade the result consistently, e.g. `[F+O]`: "the structure a₀ ∝ cH₀ is forced; the factor 1/2π rests on the full-wavelength identification, which is not yet forced".
- Change App J #3 to "narrowed (identification flagged)", not "closed".
- Remove "the 90% empirical match supports it" as a justification, or relabel it plainly: "we note that the full-cycle choice is also the one closer to the data; this is not independent evidence for it."

### R3-02 · major · hub, Ch 6: a₀ is "derived", but H₀ goes in as a measured input
Evidence:
- Ch 7: "Status tag: κ_opt is **[INPUT]** — fixed from data by the low-z Hubble law, not derived."
- The hub and Ch 6 say a₀ is "set by the cosmic inflow rate rather than fitted" and that "MOND postulates a₀ whereas this framework derives it."

A reader will read "derives a₀" as "predicts the number 1.2×10⁻¹⁰ from nothing". The actual claim is a *relation*: a₀ is tied to a separately measured H₀, and that is what removes a free constant.

Fix: add to the hub and to the opening of Ch 6:
> "The claim is a relation, not a number from nothing: given the measured Hubble rate H₀ (an input, Ch 7), the galactic scale is fixed at a₀ = cH₀/2π with no further freedom. For H₀ = 67–73 km/s/Mpc this gives 1.04–1.13 × 10⁻¹⁰ m s⁻², i.e. 87–94 % of the empirical 1.2 × 10⁻¹⁰."

### R3-03 · major · 06-galactic-…, step 2–4: the physical "why" is skipped; the derivation is dimensional analysis
Evidence:
- Step 3: "A rate-per-length κ_opt combined with the medium's wave speed c defines an acceleration … (dimensionally [m²s⁻²][m⁻¹]=ms⁻²). This is the acceleration below which the background processing of the medium is no longer negligible."
- Step 4: "The acceleration set by one full background cycle is then a₀ = c²/λ_bg."

Two things are asserted, not shown:
- why c²/λ is the acceleration that a galaxy's inflow is compared against;
- why the comparison produces the crossover ν-function.

Ch 6.1 also says "The interpolation function ν is taken in the standard RAR form rather than derived." A reader needs this said *before* the result, not in the status section.

Fix:
- Add one sentence of physical mechanism to step 3 (what physically competes with what at g_N ≈ a₀), or label steps 3–4 as "dimensional identification [F+O]".
- Move "the interpolation ν is borrowed from the empirical RAR/MOND form, not derived" into step 5 itself.

### R3-04 · major · 06-galactic-… (before 07-…): forward reference to the key input
Evidence: Ch 6 uses κ_opt = H₀/c "(Eq. (kopt))" and "(developed in Chapter 7)". Ch 7 opens with "This chapter supplies the background rate κ_opt=H₀/c that Chapter 6 used".

A top-to-bottom reader meets the load-bearing input one chapter before it is defined.

Fix: add a two-line boxed pre-definition at the start of Ch 6:
> "Preview of Ch 7: in this framework redshift is light losing energy to the medium at a constant rate per metre, κ_opt; matching Hubble's law cz = H₀d gives κ_opt = H₀/c. That rate is the only cosmological input used here."

### R3-05 · critical · 06-why-…, 16-three-falsifiable-predictions, axg-…: the headline falsification test is stated three incompatible ways and has no magnitude
Evidence:
- Ch 6.1: "its absence would **falsify** Eq. (a0)", and "a₀ should have evolved with cosmic time as **H(z)**".
- Ch 16.1: "A measured correlation … would favour this framework; its absence would **favour MOND**" (softened).
- App G criterion (1): "a₀ failing to track cH₀/2π across redshift" **kills** the framework.
- Ch 7.1: the local H₀ is a line-of-sight average that varies about 9 % with environment.

A reader cannot answer three questions from the text:
1. **What is H(z) in a non-expanding cosmology?** Ch 7 treats κ_opt as a constant rate.
2. **Which H₀ (67 or 73) sets "the" a₀?**
3. **By how much should a₀ differ, and in which data?** For example, rotation curves at z ≈ 1–2, or galaxies in voids versus clusters.

Fix: rewrite the prediction once, identically, on all three pages. For example:
> "Prediction P1: a galaxy's acceleration scale equals c·H_eff/2π, where H_eff is the Hubble rate inferred along its own line of sight (Ch 7.1). Environments whose local H₀ differs by X % must show a₀ differing by the same X %; [state the redshift dependence explicitly, or say none is predicted in a static medium]. Falsified if per-galaxy a₀ from [SPARC-like / high-z kinematic samples] is constant to better than Y % across environments where H_eff differs by more than Y %."

Also state what current RAR analyses already constrain; a universal a₀ is reported to a few percent.

### R3-06 · major · 16-three-falsifiable-predictions (prediction 3): both outcomes of the gamma-dispersion "prediction" are accommodated
Evidence: "if instead gamma propagates as the transverse branch, the framework predicts a quadratic vacuum dispersion at a scale ≤882 GeV—detection would confirm …, while **continued non-detection favours the quasi-longitudinal reading**."

The Ch 16 intro still calls this "its sharpest, most distinguishing claim … a parameter-free prediction of gamma-ray vacuum dispersion".

A reader will see a test that cannot fail.

Fix: either
- state the observation that *would* refute the quasi-longitudinal reading, or
- relabel item 3 as "open item, not yet a falsifiable prediction" and say that the volume currently has two falsifiable predictions (a₀–H₀, angular-size minimum), one of which is untestable in practice (Ch 7).

### R3-07 · major · 00-how-read-this-volume, 07-non-expanding-…, 16-honest-ledger-…: which result is the headline test?
Evidence:
- Ch 0 badge: a₀ is "**the one prediction unique to this framework**".
- Ch 7: "The cleaner near-term discriminator is therefore the galactic one".
- Ch 16 abstract: "Its **sharpest, most distinguishing claim is a parameter-free prediction of gamma-ray vacuum dispersion**".
- App F lists three distinguishing items (a₀, H₀–density correlation, γ=1 lensing).
- App G lists six "kill" criteria. Ch 0 announces "the six falsification criteria"; Ch 16.1 has "three falsifiable predictions".

Fix:
- Choose one ranked list, e.g. "P1 a₀–H₀ (primary), P2 H₀–density correlation, P3 deficit lensing γ=1, P4 merger reattachment; open: gamma branch; untestable now: z_min".
- Use it verbatim in Ch 0, Ch 16, Ch 16.1, App F and App G.
- Reconcile "three" with "six".

### R3-08 · minor · 00-how-…, 06-why-…: the long-known a₀ ≈ cH₀/2π coincidence should be credited up front
Evidence: Ch 0 calls a₀ "the one prediction unique to this framework". Only Ch 6.1 concedes that "the long-noted numerical near-coincidence a₀≈cH₀/2π is, in MOND, a coincidence", and cites Verlinde as a cross-check.

Fix: in Ch 0 and on the hub, say:
> "The numerical closeness of a₀ to cH₀/2π has been noted since Milgrom (1983); what is new here is a mechanism that makes it a necessary relation."

---

## B. Contradictions between chapters (same item, different value, grade or status)

### R3-09 · major · 08-colliding-clusters-bullet-offset vs 16-honest-ledger-… and axf-…
- Ch 8.1: "does not reproduce the observed 0.2 Mpc offset of any specific system. The quantitative data gate … remains open", and "Label: degenerate".
- Ledger (Ch 16): "Dark matter = vacuum deficit | **distinguishing** | … **Bullet reproduced where MOND fails**".
- App F: "reproducing the Bullet-Cluster offset (0.2–0.6 Mpc)".

Fix: in the ledger and App F, write "Bullet-type offset produced by mechanism; magnitude 0.2–0.6 Mpc in a toy ram-pressure model; no χ² against real lensing/X-ray maps [O]; degenerate with collisionless DM".

### R3-10 · major · 09-microwave-background-… vs axf-…: CMB temperature
- Ch 9 status: "The absolute temperature 2.725 K is **not derived**".
- App F: "the microwave background is present lattice emission, with **the 2.725 K floor shown by simulation and balance**".
- Ch 9 abstract: "Its near-perfect 2.725 K blackbody spectrum follows from quantized …" This can be read as deriving the temperature.

Fix:
- App F: "the blackbody *shape* is reproduced; the value 2.725 K is not derived [O]".
- Ch 9 abstract: "its blackbody *shape* follows …; its temperature is an input".

### R3-11 · major · 07-non-expanding-…, 09-no-big-bang-…, 08-dark-matter-…: whether the volume rejects the hot Big Bang
- Ch 7 objections: "Chapter 9, where this framework **rejects the hot Big Bang** and reinterprets the CMB as **steady-state lattice emission**".
- Ch 8 closing: "the microwave background as **steady-state** lattice emission".
- Ch 9.2: "we … make no positive claim about what the universe was—**no 'steady state'**, no alternative history", and the Big Bang is a hypothesis "which we **neither assert nor refute**".
- Ch 7 also says ρ_eff "evolves over cosmic time" (the time-varying index that produces the (1+z) stretch). That is not "static" either, although Ch 12 calls the medium "static".

Fix:
- Replace "rejects the hot Big Bang" and "steady-state" in Ch 7 and Ch 8 with the Ch 9 wording: "reads the CMB as present emission; makes no claim about origins".
- Add one sentence in Ch 7 or Ch 12 reconciling "static medium" with "ρ_eff evolving in time". For example: "non-expanding (no metric expansion) but not unchanging (the medium's effective density drifts; why is open, E-COSMO)".

### R3-12 · major · 07-non-expanding-… vs 14-*, 15-large-scale-structure-bao, 16-*, axf-…: status of BAO and the acoustic peaks
- Ch 7: "the BAO and growth (fσ₈) data—which we fit with standard ΛCDM and therefore regard as **degenerate**", and "the acoustic-scale argument presupposes the Big Bang and is therefore **not binding** here".
- Ch 9.2: "neither claims the peaks as support".
- Ch 14 / 14.1: "genuinely hard … structurally hard", with the badge "**conflicting**".
- Ch 15: "open program (HYP)", with the badge "conflicting".
- Ledger (Ch 16) and Ch 16.2: "**mechanism closed** (HYP); absolute value **out-of-scope**".
- App F: "out of scope **by design, not unsolved**".

One item carries five statuses: degenerate, not binding, conflicting, open, and closed/out of scope.

Fix:
- Choose one status (suggested: "mechanism proposed [HYP]; absolute 150 Mpc length not derived [O]") and use it everywhere.
- Delete the Ch 7 sentence claiming BAO is "fit with standard ΛCDM" (the volume cannot both reject expansion and borrow ΛCDM's BAO fit), or explain it.

### R3-13 · major · 13-light-elements-without-hot-big vs 16-honest-ledger-…
- Ch 13: "big-bang nucleosynthesis does not operate". The freeze-out calculation there is labelled "standard freeze-out target (what any model must reproduce)".
- Ledger: "Yₚ≈0.25 **follows from** a freeze-out ratio n/p≈1/7". A reader will take this as the framework reproducing helium.

Fix: ledger row should read "Yₚ ≈ 0.25 is the standard-BBN target; this framework has no mechanism yet [O]/out of scope".

### R3-14 · major · 16-honest-ledger-… (dashboard caption): "the only free parameter" claim
Evidence: "The only free astrophysical parameter anywhere in the volume is the stellar mass-to-light ratio Υ".

The same table and other chapters list further free or empirical inputs:
- Mercury triaxiality "F (free)";
- Venus "accretion-swirl sign F (free input)";
- κ, fixed by matching GM_⊙ (Ch 1, Ch 3);
- κ_opt "[INPUT]" (Ch 7);
- η and δ_loc (Ch 7.1);
- the 150 Mpc "empirical normalisation" (Ch 14–16);
- the absolute CMB temperature.

Fix: replace the sentence with an explicit inputs list:
> "Empirical inputs: κ (≡G, from GM_⊙), κ_opt (≡H₀), Υ (per galaxy), and, in exploratory sectors only, η, δ_loc, triaxiality, the accretion-swirl sign, the 150 Mpc length."

Mirror that list on the hub (see R3-16).

### R3-15 · major · axf-…, 16-honest-ledger-…, 14-*, 00-how-…: several incompatible grade vocabularies, some differing from the corpus manual
Evidence:
- Ch 0 / App F: `[F]` forced, "`[O]` open (**external empirical input**)", `[F+O]`, `[HYP]`, `[SPEC]`, plus the empirical tokens deg/dist/conf.
- Ch 2.4: "grade **Fm**".
- Ch 7: "**[INPUT]**".
- The ledger uses labels outside the three-token vocabulary: "foundation", "reframed", "pattern", "mechanism (HYP)", "out-of-scope", "does not close", "degenerate (conditional)", "accommodated", "negligible".
- Ch 13, 14 and 15 each concede: "(The computed badge stays **conflicting**: the grade vocabulary has no 'open' token …)". The page badge therefore contradicts the text.
- AGENTS.md defines `[F]/[V]/[L]/[O]`, where `[O]` means an *open gap*, not "external input". `[V]` and `[L]` never appear in this volume.

Fix:
- Add an "open" token to the badge vocabulary so the badges on Ch 13–15 match their text.
- Map every label to the corpus `[F]/[V]/[L]/[O]` scheme in one legend table in Ch 0 (e.g. the Pantheon+ fit = `[V]` degenerate; κ_opt = `[L]` anchored to the Hubble law; `[INPUT]` → `[L]`).
- Define Fm or remove it.

### R3-16 · major · index.html (hub), 01-single-input-…: "one locked input" overstates
Evidence: hub: "From this one locked input it derives planetary orbits, the galactic scale a₀ …".

Ch 1 itself says that the absolute values depend on κ, "fixing κ once, by matching GM_⊙ = κQ_⊙ for the Sun". Ch 7 makes κ_opt = H₀/c an [INPUT].

Fix (hub):
> "One body-specific input (the per-nucleon rate, imported and geometric) plus two medium constants taken from measurement (κ, equivalent to G; κ_opt, equivalent to H₀)."

### R3-17 · major · 16-three-falsifiable-predictions: wrong formula (off by 2π)
Evidence: abstract: "882 GeV = √2·**ħ**c/πa".

Ch 2 (equation alt text) and App C use E_QG = √2·**h**c/(πℓ). With ħc/a = 311.7 GeV, √2·ħc/(πa) ≈ 140 GeV, not 882 GeV.

Fix: change ħ to h.

### R3-18 · minor · 01-single-input-inflow-rate: 0.3 % versus 0.2 %
Evidence: "the electron term is at most … ≈0.3% of the nucleon term". Later: "the true Q/M is lower … by the 0.2% noted above". Nothing "above" says 0.2 %.

Fix: say "≈0.17 % (half an electron per nucleon; the 0.3 % is the hydrogen upper bound)".

### R3-19 · minor · 01-single-input-…: mₚ/mₑ = 2πνₚ is dimensionally inconsistent as written
νₚ carries s⁻¹. Fix: "mₚ/mₑ = 2π·(νₚ/νₑ) = 6π⁵".

---

## C. Terms and symbols used before definition, and skipped steps

### R3-20 · major · hub, 00-how-…: the hub never tells the reader what a₀, H₀, the RAR or ΛCDM are, or why a₀ matters
The hub states "a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻²" three times without defining it.

- **H₀** is first defined in Ch 7.1 ("Hubble constant"), but is used from Ch 0 on.
- **ΛCDM** is used from Ch 6.1 on and never expanded; "cold dark matter" appears nowhere.
- **MOND** is expanded only in Ch 6.

Fix: add a four-line "Why this number" box to the hub:
> "Galaxies rotate too fast at their edges for their visible mass. Below one universal acceleration, a₀ ≈ 1.2×10⁻¹⁰ m/s², the extra pull appears (the radial-acceleration relation). Standard cosmology (ΛCDM = cosmological constant Λ + cold dark matter) explains it with invisible halos; MOND postulates a₀ as a new constant. This volume claims a₀ is not new: it is the speed of light times the Hubble rate H₀ (how fast redshift grows with distance), divided by 2π."

### R3-21 · major · index.html, 00-how-…, 01-…: foundational jargon is imported but not glossed
The following appear in the opening pages with no in-volume explanation:
- "n-fold rectification law" (the source of 3π⁴, the volume's only input);
- "π-chain";
- "cosine-integral rectification constants";
- "river identity";
- "four-wall theorem";
- "E-COSMO embargo";
- "κ-LOCK";
- "G-ISO";
- "G-CAP-DEPART";
- "handover v0.6.0";
- "AQD" (hub: "VP, also denoted AQD", used nowhere else).

The version-change note in Ch 0 is internal bookkeeping placed in the reader's first page.

Fix:
- Give each imported term a one-sentence plain gloss at first use, or a short glossary at the end of Ch 0. For example: "n-fold rectification law: the physics volume's rule νₙ = n·π^(2(n−1)) assigning each particle type n a fixed annihilation rate".
- Move the v2 change note to App J.
- Drop "AQD" or define it.

### R3-22 · major · index.html (hub): "Inherits: R19 switch" is misleading
The hub badge reads "Inherits: R19 switch · Quantum light · Rotor inflow". No page in the volume mentions R19 or the cubic switch. Per AGENTS.md the R19 normal form is first stated in `dna`, and cosmology inherits only `physics`.

Fix: "Inherits: physics (jammed substrate, c² = K/ρ, νₚ = 3π⁴)". Also note that the corpus manual writes c² = B/ρ while this volume writes K/ρ; add "(K = bulk stiffness, written B elsewhere in the corpus)".

### R3-23 · major · 01-…, 03-gravity-…: sink without source is not addressed
Ch 3 says the medium "admits no voids; the surrounding quanta therefore move inward to replace those annihilated", and the Sun annihilates about 3.5×10⁵⁹ quanta s⁻¹ forever in a medium Ch 12 calls static and without a finite age.

The first question a lay reader asks is: where does the medium come from, and why is it not used up? No page answers it or points to where the physics volume does.

Fix: add an "Anticipated objection: is the vacuum used up?" item to Ch 1 or Ch 3. Answer it, or cite the physics-volume section and grade it [O].

### R3-24 · minor · 02-* sub-pages: order and definitions
- Ch 2.1 (gamma burst) opens "The estimate above models a burst as a stream of independent high-k photon modes". That estimate is on the previous page.
- Ch 2.2 relies on "Goldstone" and quasi-longitudinal gamma, which are defined in Ch 2.3–2.4.
- FPU-β is used without expansion (Fermi–Pasta–Ulam–Tsingou).
- Ch 3.1 opens "Two of those imported results …" with no antecedent on the page.

Fix:
- Replace "above" with "(Ch 2, §…)".
- Either reorder to 2 → 2.3 (angle) → 2.4 (Goldstone) → 2.1 → 2.2, or add one-line forward definitions.
- Expand FPU-β.
- Restate the two imported results in the first sentence of Ch 3.1.

### R3-25 · minor · 02-*, 10-post-newtonian-sector, App C: γ is overloaded and two lattice lengths look alike
- γ means gamma rays (Ch 2), the PPN light-bending coefficient (Ch 8, 10), and the DNA stiffness elsewhere in the corpus.
- D = 4.85 pm and a = 6.33×10⁻¹⁹ m are both called the lattice or cell scale. Their difference changes E_QG by 8 orders, yet App C, which explains them, is at the back.

Fix:
- Write "γ_PPN" in Ch 8 and Ch 10.
- Define D versus a in one sentence at their first use in Ch 2, and link App C there.

---

## D. Claimed versus verified versus open

### R3-26 · major · 00-how-…, hub: the claimed / verified / open split exists but is scattered, and the mainstream contrast is never stated in one place
The volume is admirably candid chapter by chapter ("degenerate", "we claim no advantage"). A one-pass reader, however, never gets a single table of:
- what mainstream cosmology says;
- what this volume says instead;
- what data currently decides it;
- what observation would falsify it;

for the four big items: expansion, dark matter, dark energy, the Big Bang/CMB.

The closest things are App F and the Ch 16 ledger, and they contradict the chapters (B above).

Fix: put a 5-row table on the hub or at the end of Ch 0:

| Topic | Standard view | This volume | Status | Falsifier |
|---|---|---|---|---|
| Redshift | metric expansion | energy loss to the medium | degenerate on SNe | … |
| Dark energy | Λ | not needed | degenerate | … |
| Dark matter | particle halos | vacuum deficit | degenerate on curves; lensing γ=1 open | … |
| a₀ | coincidence / MOND constant | cH₀/2π | distinguishing | a₀ ∝ H_eff |
| CMB / BBN / BAO | hot Big Bang relics | present emission; peaks and BAO length not derived | open | … |

### R3-27 · minor · 07-hubble-tension-…, axg-…: a hypothesis-grade item is used as a framework kill criterion
Ch 7.1 grades the Hubble-tension mechanism HYP/SPEC ("not a parameter-free prediction"). App G criterion (2) makes the absence of the H₀–density correlation kill the whole framework.

Fix: state that it would kill the Ch 7.1 mechanism only, or promote the mechanism explicitly.

---

## E. Rendering and structure

### R3-28 · critical · unescaped `<` swallows text in the browser (5 places)
In each case the HTML parser opens a bogus tag and the following text disappears.

| Page | Raw HTML | What the reader loses |
|---|---|---|
| 06-galactic-rotation-derivation-a0-ch0 (line 51) | `g_N=GM_(bar)(<r)/r², with GM_(bar)=κQ_(bar) …` | Step 1 of the headline derivation up to the next `>` |
| 02-angle-account-quasi-longitudinal-gamma (line 49) | `for λ<D one has m=⌈λ/D⌉=1` | Text after `λ` |
| 02-gamma-burst-collective-disturbance (lines 41, 116) | `≈0.73c<c its components separate`; `v_g=ccos(ka/2)<c and` | Text after `c` (two places) |
| 07-non-expanding-lattice-optics-cosmology (line 102) | `over 0<z<2.3,` | The figure reference after it (my extraction shows "over 0 (cosmo), left)") |
| axf-executive-summary-one-page-result (line 64) | `(τ_(lock)<age);` | The spin-row note, possibly more of the scorecard table |

Fix: escape these as `&lt;` in the generator and add a build check for `<[A-Za-z]` outside known tags.

### R3-29 · major · raw LaTeX left in the visible text (about 30 pages)
- `\href{https://doi.org/…}{ 10.5281/… }`: 27 occurrences on 21 pages.
- `\textsf{[F]}` and similar: 99 occurrences on 18 pages, including every grade in the App F scorecard and the Ch 16 ledger.
- `[textsfO]` appears in App F prose. `textsf` also appears in the hub title and URL slug of App E: `axe-conjectures-solar-activity-exploratory-textsfhyp`, "(exploratory, textsfHYP/textsfSPEC)".
- `$a₀=cH₀/2π$`, `$D$`, `$a$` appear in hub link titles and the App C title.
- ` ``Dark Matter'' ` appears in the hub (TeX quotes).
- `emphmechanism`, `emphopen`, `emphnot` appear in the Ch 16 caption and App J.
- `l}{ Galactic scale — … }` appears as table-group header debris in the Ch 16 dashboard.
- `Spin \ tidal` and `Large-scale structure \ BAO` show a stray backslash.

Broken macros:
- `\gg`/`\ll` render as `292ggνₑ`, `g_Ngga₀`, `g_Nlla₀`, `εll1`, `ħωll k_BT` (Ch 1, 6, 7, 9).
- `\gtrsim`/`\lesssim` render as `gtrsim20%`, `|Δc/c|lesssim10⁻¹⁵` (Ch 7, 16).
- `\bar` renders as `barλ`, `barκ` (Ch 6, 6.1, 7.1).
- `\kappa`/`\odot` render as `kappaQ_(odot)` (Ch 1, 4).
- `\mathrm` renders as `m_(mathrm H)` (Ch 1) and `E_(rm QG,2)` (Ch 2).
- `\frac` renders as `fracΓ_(ad)Γ_(ad)-1 fracpρ c²` (Ch 9.1).
- `\langle` renders as `langleKE⟩/langlePE⟩` (Ch 9, 9.2).
- `quantas⁻¹` should read "quanta s⁻¹" (Ch 1, 3).

The underscore→subscript converter corrupts script names in the Ch 16 dashboard caption: `chₐccuracy_dashboard.py`, `ch4ₛolarₛystem.py`, `ch5ₛpinₜidal.py`, `ch_galacticₛpin.py`.

Fix: extend the generator's LaTeX→Unicode map (\gg ≫, \ll ≪, \gtrsim ≳, \lesssim ≲, \bar, \kappa κ, \odot ⊙, \langle ⟨, \frac, \textsf, \emph, \href, TeX quotes). Exempt `code`/filenames from subscript conversion. Add a CI grep for `\\[a-z]+\{|textsf|emph[a-z]|gg[νga]|mathrm`.

### R3-30 · major · unresolved cross-reference labels throughout
The reader sees LaTeX label keys instead of numbers:
- "Table (rawinferred)", "Table (Qbody)", "Table (a0)";
- "§ (bulk)", "§ (status)", "§ (gate)", "§ (galspin)", "§ (realmap)", "§ (angle-disp)", "§ (colliding)";
- "Equation (QperM)", "Eq. (a0)", "Eq. (dL)", "Eq. (kopt)";
- "(nuH)", "(nup)–(nue)";
- "Fig. (gal)", "Fig. (ledger)";
- "Appendix (scorecard)", "Appendix (governance)".

My extraction counts about 41 `§ (…)` references on 11 pages, 15 `Appendix (…)` on 5 pages and 11 `Table (…)` on 7 pages. Because equations are SVG images without visible numbers, "Eq. (a0)" cannot be located at all.

Fix: resolve labels to numbered links (e.g. "Eq. 6.2", "§1.3", "Appendix F"), and show equation numbers beside the SVGs.

### R3-31 · minor · Korean UI strings on English pages
"재현 코드 (GitHub)", "스냅샷", "용어", "백서 목차 §1 →" appear in each page's repro strip and footer nav. An English reader cannot tell what they are.

Fix: "Reproduction code", "Snapshot", "Glossary", "Contents".

### R3-32 · minor · structure checks that passed
- The hub lists all 42 topic pages.
- Prev/next links follow the hub order on every page.
- All 66 equation SVGs referenced exist.
- No stub pages; the shortest, App C at about 4.9 kB, is complete.
- The hub's "28 chapters" (= §0–16 plus 11 appendices) is consistent.

Only note: App D (imports index) is linked twice on the hub, at the top and in the appendix list. That is harmless.

---

## Priority order for fixes
1. R3-28: escape `<`. It silently deletes text, including the first step of the a₀ derivation.
2. R3-29 and R3-30: raw LaTeX and unresolved labels on about 30 pages.
3. R3-01, R3-02, R3-05, R3-06, R3-07: make the headline claim, its grade, and its falsifier single, consistent and quantitative.
4. R3-09 to R3-16: reconcile App F and the Ch 16 ledger with the chapters (Bullet, CMB temperature, Big Bang stance, BAO/acoustic, BBN, free parameters, grade vocabulary, "one input").
5. R3-20 to R3-23 and R3-26: reader on-ramp (why a₀, glossary, mainstream-contrast table, sink-without-source).
