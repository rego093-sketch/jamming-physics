# Literature & Accession Registry — sensory_organ_vp_site

Every external anchor used by the research program, with its grade.
Grades: **[L]** locked & cited (measured input / established literature) · **[V]** verified in-sim ·
**[O]** open w/ stated obstacle · **contested** flagged where the literature disagrees.

This package **CITES** these; it does not re-derive organ optics/acoustics from R19, and it does not
compute transducer γ here (that is owned by the DNA package — see `inherited/organ_gamma.json _to_measure`).

---

## 1. Master genes (γ measured, vendored from DNA package) — [L]

γ = −mean(nearest-neighbour stacking ΔG37), SantaLucia 1998, human proximal promoter (TSS−2000..+500).
Never fitted. Cached so γ reproduces offline bit-for-bit.

| gene | γ | node | accession |
|---|---|---|---|
| PAX6 | 1.511 | eye_retina_optics | NCBI Gene 5080 |
| RAX | 1.4541 | eye_photoreceptor | NCBI Gene 30062 |
| EYA1 | 1.3638 | cochlea_frequency_map | NCBI Gene 2138 |
| SOX2 | 1.4573 | inner_ear_haircell | NCBI Gene 6657 |
| TAS1R3 | 1.5555 | taste_chemodetection | NCBI Gene 83756; UniProt Q7RTX0 |

- SantaLucia J Jr (1998). A unified view of polymer, dumbbell, and oligonucleotide DNA nearest-neighbor thermodynamics. *PNAS* 95(4):1460–1465.

## 2. Transducer effector genes (γ DEFERRED to DNA pipeline) — channel switch elements

Identity + accession cited here [L]; γ is an honest to-measure input (not invented).

| gene | accession | node | role |
|---|---|---|---|
| CNGA1 | NCBI Gene 1259; UniProt P29973 | photoreceptor | rod CNG channel α (cooperative gate) |
| CNGB1 | NCBI Gene 1258; UniProt Q14028 | photoreceptor | rod CNG channel β |
| TMC1 | NCBI Gene 117531; UniProt Q8TDI8 | hair cell | MET pore |
| PCDH15 | NCBI Gene 65217; UniProt Q96QU1 | hair cell | tip link (gating spring) |
| CDH23 | NCBI Gene 64072; UniProt Q9H251 | hair cell | tip link (gating spring) |
| SLC26A5 (prestin) | NCBI Gene 375611; UniProt P58743 | OHC | somatic motor = Hopf active force |
| TAS1R2 | NCBI Gene 80834; UniProt Q8TE23 | taste | sweet receptor subunit |
| TRPM5 | NCBI Gene 29850; UniProt Q9NZQ8 | taste | downstream cation channel |
| CNGA2 | NCBI Gene 1260; UniProt Q16280 | olfaction | olfactory CNG channel (same superfamily as CNGA1) |
| ADCY3 | NCBI Gene 109; UniProt O60266 | olfaction | adenylyl cyclase (cAMP generator) |

## 3. Cochlear place-map (tonotopy) — [L]

- Greenwood DD (1990). A cochlear frequency-position function for several species—29 years later. *J Acoust Soc Am* 87(6):2592–2605.
  - f = 165.4·(10^(2.1x) − 0.88), human, x∈[0 apex, 1 base] → ~20 Hz .. ~20 kHz. Reproduced in `organ_optics.py` [V].

## 4. Hair-cell mechanotransduction = two-state gating-spring switch — [L] structure → [V]

- Howard J, Hudspeth AJ (1988). Compliance of the hair bundle associated with gating of mechanoelectrical transduction channels. *Neuron* 1(3):189–199.
- Corey DP, Hudspeth AJ (1983). Kinetics of the receptor current in bullfrog saccular hair cells. *J Neurosci* 3(5):962–976.
- Markin VS, Hudspeth AJ (1995). Gating-spring models of mechanoelectrical transduction. *Annu Rev Biophys Biomol Struct* 24:59–83.
- Martin P, Mehta AD, Hudspeth AJ (2000). Negative hair-bundle stiffness betrays a mechanism for mechanical amplification. *PNAS* 97(22):12026–12031.

## 5. Cochlear active amplifier = Hopf critical oscillator — [L] → cube-root exponent 1/3 [V]

- Camalet S, Duke T, Jülicher F, Prost J (2000). Auditory sensitivity provided by self-tuned critical oscillations. *PNAS* 97(7):3183–3188.
- Eguíluz VM, Ospeck M, Choe Y, Hudspeth AJ, Magnasco MO (2000). Essential nonlinearities in hearing. *Phys Rev Lett* 84(22):5232–5235.
- Hudspeth AJ, Jülicher F, Martin P (2010). A critique of the critical cochlea: Hopf — a bifurcation — is better than none. *J Neurophysiol* 104(3):1219–1229.
  - Normal form dz/dt=(μ+iω₀)z−β|z|²z+Fe^{iω₀t}; at μ=0, R=(F/β)^{1/3}. Exponent **1/3 is parameter-free** [V]. Cited BM compression ~0.3–0.5 [L].

## 6. Phototransduction — rod CNG channel, cooperative all-or-none — [L] → [V]

- Fesenko EE, Kolesnikov SS, Lyubarsky AL (1985). Induction by cyclic GMP of cationic conductance in retinal rod outer segment. *Nature* 313:310–313.
- CNG Hill cooperativity ~3 (sharp switch); single-photon response discrete & reproducible. Olfaction shares the SAME CNG superfamily (CNGA2) — literal common transducer.

## 7. Vestibular semicircular canal = overdamped torsion pendulum — [L] → [V]

- Steinhausen W (1933). Über die Beobachtung der Cupula in den Bogengangsampullen.
- Van Egmond AAJ, Groen JJ, Jongkees LBW (1949). The mechanics of the semicircular canal. *J Physiol* 110(1–2):1–17.
- Jones GM, Milsum JH (1965). Spatial and dynamic aspects of visual fixation.
  - Peripheral afferent τ ~4–7 s; central velocity-storage ~15–25 s; VOR gain ~1 (healthy young). Canal integrates angular acceleration → encodes angular VELOCITY across 0.1–6 Hz [V].

## 8. Reduced eye / accommodation — classical optics — [L] → [V-arith]

- Gullstrand reduced/schematic eye: total power ~60 D (cornea ~40 + lens ~20), n′=1.336, emmetropic axial ~22.3–22.6 mm.
- Hofstetter HW (1965). Age–amplitude-of-accommodation formula: max amplitude(D) = 25 − 0.40·age → presbyopia ~1 D @ 60.
- Clinical axial→refraction ~2.7–3.0 D/mm; model gives 2.69 D/mm geometrically [V].

---

## 9. Root-cause treatment literature (2023–2026)

**Grades: [L] established/approved · contested where replication failed · partial where endpoint limited.**

- **AMD / geographic atrophy** — complement (alternative-pathway) positive-feedback loop.
  - Pegcetacoplan (C3 inhibitor, Syfovre), FDA Feb 2023; avacincaptad pegol (C5, Izervay), FDA Aug 2023. Slow lesion growth ~14–27%.
  - **HONEST CAVEAT (partial):** phase-3 showed **no functional visual-acuity benefit yet**; exudation/CNV risk ~7–12%.
- **Myopia** — emmetropization defocus-feedback loop; root = re-engage the error signal, not just optical correction.
  - Outdoor bright light (retinal dopamine) + low-dose atropine (0.01–0.05%) + peripheral-defocus lenses (DIMS) / ortho-K + repeated low-level red light (650 nm). RCT-supported ≥50% slowing; IMI consensus. Long-term safety still accruing.
- **Glaucoma** — TM outflow resistance ↑ → IOP setpoint drift.
  - ROCK inhibitors: netarsudil (US), ripasudil/fasudil (JP/CN) restore conventional outflow conductance (root tissue) + IOP-independent RGC neuroprotection (↑Bcl-2, ↓caspase-3). Approved (outflow); neuroprotection preclinical.
- **Presbycusis / SNHL** — transducer loss pushes the Hopf amplifier off criticality.
  - OTOF gene therapy (DFNB9) restored hearing in children (clinical, 2024). ATOH1 hair-cell regeneration — **contested for acquired SNHL** (regenerated cells remain immature; thresholds not restored). Synaptopathy repair (NT-3/BDNF) preclinical.
- **Cataract** — crystallins cross the aggregation spinodal (near-irreversible).
  - Pharmacological chaperones / oxysterols (lanosterol, 25-hydroxycholesterol, VP1-001) — **CONTESTED:** 2015 reports of reversal; **Daszynski et al. 2019 (Sci Rep) and others FAILED to replicate** disaggregation → efficacy unproven; surgery standard.
- **Diabetic retinopathy** — reset systemic metabolic setpoint (root); anti-VEGF blocks the downstream neovascular attractor.
- **BPPV** — canalith repositioning (Epley/Semont): mechanically returns otoconia → removes the false signal at its source (already a root-cause instrument-level fix).

---

*Citation discipline:* references are listed for attribution; quotations are avoided (paraphrase only).
Any item whose exact bibliographic coordinates need re-confirmation before HTML publication is marked in
`IRREPRODUCIBILITY_LEDGER.md`. The substrate claims ([V]) are reproduced by `repro/run_all.py`; the clinical
claims ([L]/contested) are literature anchors, not in-sim results.
