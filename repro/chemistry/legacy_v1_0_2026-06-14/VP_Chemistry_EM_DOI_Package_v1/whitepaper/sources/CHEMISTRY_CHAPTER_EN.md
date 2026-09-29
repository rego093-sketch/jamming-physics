# Chemistry from a Single Anchor: The Jamming Account

**VP Chemistry & Electromagnetism Whitepaper — Chapter CH**
DOI (reserved): 10.5281/zenodo.20680541 · Companion to VP Theory (physics) and to Chapter EM
Status grades: **[F]** forced (zero free parameters) · **[F?]** forced-candidate (model-dependent
or <1.5%) · **[CAL]** calibration input (measured constant, used consistently) · **[V]**
simulation-measured · **[O]** open (honestly unsolved). Every numeric claim is reproduced by a
deterministic, standard-library module (2× sha256 identical); module and case-ledger anchors are
given inline. Verified numbers quoted below are the actual module outputs.

> Everything starts locked, is derived, and is settled by a verdict. One table separates what is
> *forced* from what is *measured input* from what is *open*. Chemistry unfolds from the electron
> (a rotational dent) using only $\pi$-geometry and the electromagnetic $1/r^2$ — the same
> substrate from which light emerges (Chapter EM).


## CH.0 Governance and grading (inherited from VP Theory §1)

This chapter inherits No-Tuning / LOCK / Gate. **No-Tuning:** changing an input after seeing a
result to hit a target is forbidden. The clean final logic is presented here; the trial-and-error
of development lives, reproducibly, in the modules and the case ledger. Forced results **[F]** have
no adjustable parameter — they cannot be tuned, so they are *refuted* if they disagree with
measurement.


## CH.1 The anti-tuning chain — the central defense

A trained reviewer immediately suspects parameter-fitting. The rebuttal has three prongs.

**Prong A — forced results are dimensionless geometry with nothing to adjust.** The tetrahedral
angle $\arccos(-1/3)$, the ratio $\Delta_{\text{tet}}/\Delta_{\text{oct}} = 4/9$, the FCC packing
fraction $\pi/(3\sqrt2)$, the shell-filling integers $[2,8,8,18,18,32]$ — these are pure
geometry/integers with no knob.

**Prong B — calibration inputs are used as forward predictions.** Measured constants
(spectroscopic $B,\nu$; bond enthalpy $\Delta H$; $\mathrm pK_a$; standard potential $E^\circ$)
are each fixed *once* and used consistently. Quantities *derived* from them — standard entropy,
equilibrium constants, cell potentials — then match measurement; that is prediction, not fitting.

**Prong C — honest open items prove no tuning.** A tuner would have "solved" absolute
multi-electron ionization energies; instead the failure is recorded (mean ~22% for main group,
electron affinity wrong in sign 8/18 by the Slater method) and marked **[O]**.


## CH.2 Foundation: anchor → atomic scale **[F]**

The only observational input is the electron mass $m_e$ (the anchor). With the EM coupling
$\alpha_{\mathrm{em}}$ **[CAL]** and $\pi$ (using the *reduced* Compton wavelength
$\bar\lambda_{C,e} = \hbar/(m_e c) = \lambda_{C,e}/2\pi$):
$$ a_0 = \frac{\bar\lambda_{C,e}}{\alpha_{\mathrm{em}}} = \frac{\hbar}{m_e c\,\alpha_{\mathrm{em}}},
   \qquad \mathrm{Ry} = \frac{\alpha_{\mathrm{em}}^2 m_e c^2}{2}. $$
Module `vp_atomic.py` gives $a_0 = 0.529177$ Å (Δ +0.0000%) and $\mathrm{Ry} = 13.6057$ eV
(Δ −0.0001%); hydrogenic $\mathrm{IE} = \mathrm{Ry}\,Z^2$ to <0.06%. Shell structure follows from
the Aufbau degeneracy $2(2l+1)$, giving noble-gas closures $[2,10,18,36,54,86]$ and period lengths
$[2,8,8,18,18,32]$ exactly **[F]**. Absolute many-electron IE is only approximate (screening) and
is **[O]**.


## CH.3 Periodic structure: valence and oxidation **[F]/[F?]**

Valence equals the number of outer-shell electrons (1–8, main group) **[F]**. The octet rule fixes
ionic-compound stoichiometry: module `vp_valence.py` predicts 9/9 formulas (NaCl, MgCl₂, Al₂O₃,
CaO, …). Periodic trends (radius ↓, electronegativity ↑ across a period; radius ↑ down a group) are
**[F?]**. Transition metals have valence $4s+3d$ with variable oxidation states (Mn +2…+7) from the
partially filled $d$-shell; the half/fully-filled exceptions Cr ($3d^54s^1$), Cu ($3d^{10}4s^1$)
follow from sub-shell stability **[F]**.


## CH.4 Chemical bonding and VSEPR geometry **[F]**

Geometry is the electromagnetic $1/r^2$ repulsion of electron domains on a sphere (the Thomson
problem). Module `vp_molecular_geometry.py` *computes* (seed-independent) the angles:
$$ \text{linear } 180^\circ,\quad \text{trigonal } 120^\circ,\quad
   \boxed{\text{tetrahedral } \arccos(-\tfrac13) = 109.47^\circ},\quad \text{octahedral } 90^\circ. $$
All have zero free parameters **[F]**; the simulation reproduces the closed form
$\arccos(-1/3)=109.47^\circ$. Lone-pair compression (CH₄ → NH₃ → H₂O: $109.5^\circ \to 107^\circ
\to 104.5^\circ$) has the correct direction **[F?]**; the precise magnitude is **[O]**. Bond rupture
follows a scale-invariant $\sqrt2$ diagonal-stretch geometry shared with nuclear fission (Chapter EM
links the same $1/r^2$); absolute bond energy needs per-bond anharmonicity and is **[O]**.


## CH.5 Coordination chemistry: color and magnetism **[F]**

Ligand point charges (EM $1/r^2$) split the geometric $d$-orbitals (spherical harmonics). Module
`vp_crystal_field.py` gives the octahedral $e_g$↑ / $t_{2g}$↓ pattern (tetrahedral inverted) and the
analytic ratio
$$ \frac{\Delta_{\text{tet}}}{\Delta_{\text{oct}}} = \frac{4}{9} = 0.4444 \quad\text{(exact)}. $$
High/low-spin unpaired-electron counts give magnetic moments (Fe³⁺ 5/1 unpaired) **[F]**. Color is
the $d$–$d$ transition $\Delta \to \lambda$ (interpreted optically via Chapter EM); multi-band
precise color is **[O]**, the spectrochemical series is **[CAL]**.


## CH.6 Light, optics, color — see Chapter EM **[F]/[CAL]**

The optical consequences (propagation angle $\sin\chi = \lambda/(mD)$, Snell, rainbow $42.1^\circ$,
total-internal-reflection critical angle, blackbody, $d$–$d$ color) are developed in **Chapter EM**.
Chemistry *consumes* the electromagnetic mechanism from physics §10/§14; it does not re-derive it.
The boundary is explicit: fundamental EM (light as rotational transverse wave, $c^2=B/\rho$, the
$1/r^2$ Green function) is physics; the chemical/optical consequences are here.


## CH.7 Thermodynamics: rotational energy → temperature **[F]/[F?]**

Temperature is a rotational-energy scale; rotational levels $E_J = B\,hc\,J(J{+}1)$. Heat-capacity
degrees-of-freedom: monatomic $\tfrac32 R$, diatomic $\tfrac52 R$, solid Dulong–Petit $3R$ (<3%).
Module `vp_statistical_thermo.py` reproduces the H₂ heat-capacity **staircase**
($\tfrac32 R$ at 20 K → $\tfrac52 R$ at 298 K → $\tfrac72 R$ above ~6332 K) with activation
temperatures $T_{\text{rot}} = 88$ K, $T_{\text{vib}} = 6332$ K from $B,\nu$; $C_v$(H₂) 20.81 vs
20.4 (+2.0%) **[F]**. Standard molar entropy (Sackur–Tetrode + rotation + vibration + electronic)
is <0.3% for H₂·N₂·CO·O₂; O₂ includes the known triplet (paramagnetic) $R\ln 3$ **[F?]**. The
spectroscopic constants $B,\nu$ are per-molecule **[CAL]**.


## CH.8 Chemical equilibrium **[F]**

Direction is set by $\Delta G = \Delta H - T\Delta S$; dissociation occurs when $T\Delta S > \Delta H$.
The dissociation temperature is
$$ T^* = \frac{\Delta H}{\Delta S}. $$
Module `vp_equilibrium.py` gives $T^*$: N₂ 8214 K > H₂ 4400 K > O₂ 4210 K > Cl₂ 2272 K — the
**bond-strength order** **[F]**. Reaction entropies from partition functions are <0.4%. The van 't
Hoff $K(T)$ (H₂ ⇌ 2H, with $K=1$ at $T^*$) is **[F?]** ($\Delta H$ is **[CAL]**). Le Chatelier
directions (dissociation $\Delta S>0$ high-T driven; Haber $\Delta S<0$ high-T reversed) **[F]**.


## CH.9 Reaction kinetics **[F]**

The activation energy is the threshold to reach the transition state (a $\sqrt2$ bond-stretch); the
fraction crossing is the Boltzmann tail $\exp(-E_a/RT)$. Module `vp_kinetics.py` reproduces the
Arrhenius temperature dependence, the room-temperature **10 K doubling rule** ($E_a\approx 50$
kJ/mol gives ×1.9 per 10 K), and recovery of $E_a$ from the Arrhenius slope $-E_a/R$. Mean molecular
speed $\sqrt{8k_BT/\pi m}$ (N₂ 298 K → 475 m/s) and the Eyring universal factor $k_BT/h =
6.2\times10^{12}$ s⁻¹ follow **[F]**. Absolute $E_a$ (transition-state structure) and tunneling are
**[O]**.


## CH.10 Solution chemistry: proton-transfer equilibrium **[F]**

With $K_w = 10^{-14}$, pure water has pH 7. The weak-acid pH solves $K_a = x^2/(C-x)$; module
`vp_solution_chemistry.py` gives acetic acid 0.1 M → pH 2.88 (measured 2.87). Henderson–Hasselbalch
buffering pH $= \mathrm pK_a + \log([A^-]/[HA])$ and titration equivalence-point jumps follow
**[F]**. Individual $\mathrm pK_a$ are **[CAL]**; absolute $\mathrm pK_a$ prediction (solvation) is
**[O]**.


## CH.11 Electrochemistry: electron (rotational dent) transfer **[F]**

Charge is rotation (Chapter EM); redox is rotational-dent transfer, symmetric with proton transfer
(CH.10). The cell potential is
$$ E^\circ_{\text{cell}} = E^\circ_{\text{cathode}} - E^\circ_{\text{anode}}, \qquad
   \Delta G^\circ = -nFE^\circ,\qquad E = E^\circ - \frac{RT}{nF}\ln Q. $$
Module `vp_electrochemistry.py` gives the Daniell cell $E^\circ_{\text{cell}} = 1.10$ V (matches
measured) and $\Delta G^\circ = -212$ kJ/mol **[F]**. The standard-potential series (Li −3.04 →
F₂ +2.87) links to IE and electronegativity; individual values are **[CAL]**.


## CH.12 Organic chemistry: carbon skeleton on EM geometry **[F]**

Carbon's tetravalence plus EM repulsion gives hybridization geometry (the same VSEPR engine as
CH.4): module `vp_organic_chemistry.py` gives sp³ tetrahedral $109.5^\circ$, sp² planar $120^\circ$,
sp linear $180^\circ$. Bond order–length–strength:
$$
\begin{array}{lccc}
 & \text{order} & \text{length} & \text{strength (kJ/mol)}\\
\text{C–C} & 1\ (1\sigma) & 154\ \text{pm} & 348\\
\text{C=C} & 2\ (1\sigma+1\pi) & 134\ \text{pm} & 614\\
\text{C≡C} & 3\ (1\sigma+2\pi) & 120\ \text{pm} & 839
\end{array}
$$
The degree of unsaturation $(2C+2+N-H-X)/2$ gives benzene 4 **[F]**. Functional-group reactivity
(acid–base, redox applied) is **[F?]**; absolute rates and stereoselectivity are **[O]**.


## CH.13 Materials and nuclear (summary) **[F]/[F?]**

Crystal packing fractions are pure geometry: FCC/HCP $\pi/(3\sqrt2) = 0.7405$, BCC 0.6802, SC 0.5236
(module `vp_crystal_packing.py`); FCC metal densities <2% **[F]/[F?]**. Nuclear magic-number skeleton
from Gauss-lattice point counts $N(R^2)+1$: module `vp_gauss_shells.py` gives **2, 8, 20, 28, 82**
(5/7 parameter-free); 50, 126 require spin–orbit **[CAL]**. SEMF fission/fusion gives the iron peak
$A=58$ and the critical $Z^2/A$ **[F?]**. Theoretical bounds ($\sigma_{th}$, $\gamma_s$) are bounds,
not predictions — honestly **[F]+[O]**.


## CH.14 Master ledger — forced / measured input / open

**[F] forced (zero free parameters — cannot be tuned):** shell filling and period lengths; valence,
oxidation, ionic formulas; all VSEPR angles ($\arccos(-1/3)$ etc.); $\Delta_{\text{tet}}/
\Delta_{\text{oct}}=4/9$; packing fractions; propagation angle $\sin\chi=\lambda/(mD)$; rainbow
$42^\circ$; Snell, critical angle; $C_v(T)$ staircase and activation temperatures; dissociation-
temperature order and Le Chatelier; Arrhenius, 10 K doubling, $k_BT/h$; pH, buffers, titration;
$E^\circ_{\text{cell}}$, $\Delta G=-nFE^\circ$, Nernst; hybridization, bond order, unsaturation;
Gauss magic-number skeleton.

**[CAL] calibration input (measured constants, used consistently — never tuned per case):**
spectroscopic $B,\nu$; bond enthalpy $\Delta H$; $\mathrm pK_a$; standard potential $E^\circ$;
spectrochemical series; absolute refractive index $n$; spin–orbit strength (magic 50, 126);
the fine-structure coupling $\alpha_{\mathrm{em}}$.

**[O] open (honest — not disguised as solved):** absolute multi-electron IE (screening); electron
affinity (Slater sign failure); absolute $\mathrm pK_a$, $E^\circ$ (solvation); multi-band precise
color; absolute bond energy (anharmonicity); $d$-block absolute IE; absolute rates and
stereoselectivity; nuclear shell-correction masses; pure-$\pi$ geometry of 50, 126.


## CH.15 Two unifications — sphere geometry and rotation

**Sphere geometry:** molecular shape = points *on* a sphere (Thomson/VSEPR) → $\arccos(-1/3)$;
nuclear shells = lattice points *inside* a sphere (Gauss) → magic-number skeleton; crystal density
= sphere *packing* (Kepler) → 0.7405; $d$-orbital splitting = spherical harmonics × ligand EM →
4/9.

**Rotation:** the electron is a rotational dent; charge is rotation handedness; light is the
rotational transverse wave (Chapter EM); temperature is rotational excitation; equilibrium, rate,
and electrochemistry all ride on rotational energy. The single anchor (electron = rotational dent)
opens, and the last sector (electrochemistry = rotational-dent transfer) closes the circle.


## CH.16 Falsification criteria **[F]**

Forced results cannot be re-fitted, so they are refuted on disagreement:

- If the tetrahedral angle is not $\arccos(-1/3)=109.47^\circ$, the VSEPR-EM derivation is discarded.
- If $\Delta_{\text{tet}}/\Delta_{\text{oct}} \neq 4/9$, the crystal-field geometry is discarded.
- If the rainbow angle is not $\approx 42^\circ$, the light-angle/refraction derivation is discarded.
- If H₂ heat capacity shows no $\tfrac32\to\tfrac52\to\tfrac72 R$ staircase, or the activation
  temperatures disagree with $B,\nu$, the partition-function account is discarded.
- If dissociation temperatures do not follow the bond-strength order, the equilibrium derivation is
  discarded.
- The committed light-angle predictions $\chi(632.8\,\text{nm})=89.892^\circ$,
  $\chi(532\,\text{nm})=89.825^\circ$ are falsifiable forward predictions (Chapter EM).


## CH.17 Reproducibility

Thirty deterministic, standard-library modules and a 114-row case ledger (`cases_fixed.csv`)
reproduce this logic; the light/EM additions add a 16-row ledger (`cases_em.csv`). Determinism is
verified by running each module twice and comparing the stdout sha256.

```
python3 research/foundation/vp_molecular_geometry.py   # tetrahedral 109.47°
python3 research/foundation/vp_crystal_field.py        # 4/9
python3 verify_chemistry.py --root <package root>      # all modules + ledger integrity gate
```

The harness reports execution, determinism, standard-library-only dependency, and case-ledger
integrity. With the light and electromagnetism modules included, **32/32 PASS**.


*Together with Chapter EM, this completes the program: light emerges from the jammed lattice and
the electromagnetic $1/r^2$ follows (Chapter EM); on that substrate, atoms, bonds, geometry, color,
heat, equilibrium, rate, solution, electrochemistry, and organic structure are forced by sphere
geometry and rotation (this chapter). What is forced is falsifiable; what is measured is labelled;
what is open is admitted — and all of it is reproducible.*
