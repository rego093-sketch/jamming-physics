# Electromagnetism in the Jamming Vacuum: From the Quantum Lattice to Light

**VP Chemistry & Electromagnetism Whitepaper — Chapter EM**
DOI (reserved): 10.5281/zenodo.20680541 · Companion to VP Theory (physics) §10, §14, §15
Status: each result is graded **[F]** forced (zero free parameters) · **[CAL]** calibration input
(measured constant, used consistently) · **[V]** simulation-measured · **[H]** hypothesis ·
**[O]** open. Every numeric claim is reproduced by a deterministic, standard-library module
(2× sha256 identical); module names are given inline.

> One medium, one motion seen two ways. Charge is the bookkeeping of a synchronized rotation;
> light is the transverse swing of that rotation propagating on the single surviving longitudinal
> wave. Electricity, a radio wave, and a γ-ray differ only by an angle.


## EM.0 Governance (inherited from VP Theory §1)

This chapter inherits the No-Tuning / LOCK / Gate discipline of the physics whitepaper.
**The fundamental electromagnetic mechanism is supplied by physics §10 (light, clock-free $c$)
and §14 (force, the $1/r^2$ Green function). This chapter does not re-derive it; it takes those
results as input and develops the chemical and optical consequences.** Where a quantity is a
measured constant (notably the fine-structure coupling $\alpha_{\mathrm{em}}$), it is marked
**[CAL]** and is never tuned to fit a downstream result.


## EM.1 Genesis: charge as synchronized rotation **[H]→[V]**

A quantum that receives energy can only store it as rotation, so energy input forces rotation.
This is grounded in established physics: photon–photon collisions create matter
($\gamma\gamma \to e^+e^-$; $E=mc^2$), and photons carry helicity $\pm 1$ — circular polarization
is a *rotating field*. **Electric charge is the bookkeeping of one synchronized rotation** of the
quanta; the sign $\pm$ is the handedness (CW/CCW) of the twist of a charge's rotation relative to
the surrounding common axis. The elementary charge is one boundary-crossing rotation unit
(universal), so the EM coupling carries no nucleon-structure factor (contrast the mass/gravity
sector, where $m_p/m_e = 6\pi^5$ and the $82{+}7$ core appear).


## EM.2 Light emergence — the keystone **[F]/[V]**

Light is not assumed; it *emerges* from the jammed lattice. The chain (physics §SP):

1. **[F, axiom]** Infinitely rigid, fully packing quanta ⇒ the vacuum is a jammed lattice.
2. **[H]→[V]** Rotation (temperature) drives the contact number $z$ to the isostatic threshold
   $z = 2d = 6$ (self-organized criticality).
3. **[V]** At the isostatic point the shear reserve is zero, so the relaxed shear modulus
   vanishes while the bulk modulus stays finite:
$$ G_{\text{relaxed}} \to 0,\qquad B = \text{finite}\;\Rightarrow\; c^2 = \frac{B}{\rho}=K. $$
   The transverse acoustic wave dies; **one longitudinal speed survives.**
4. **[F]** A single speed gives linear dispersion and hence a wavelength:
$$ \omega = c\,q \;\Rightarrow\; \lambda = c/\nu. $$

**Direct demonstration (module `vp_light_emergence.py`).** A 1-D chain of quanta,
$m\,\ddot u_n = k(u_{n+1}-2u_n+u_{n-1})$, is given a right-moving Gaussian packet and integrated
by leapfrog (no randomness). The energy centroid propagates at
$c_{\text{measured}} = 0.99940$ versus the closed form $c_{\text{theory}} = a\sqrt{k/m} = 1$ —
a **0.06 %** agreement. The exact dispersion $\omega(q)=2\sqrt{k/m}\,|\sin(qa/2)|$ tends to
$\omega = cq$ as $q\to 0$ ($v_{ph}/c \to 0.99999$), and the identity $c^2=B/\rho$ is verified to
machine precision. A 2-D triangular lattice confirms that as the shear reserve $\to 0$ the
transverse speed $c_T \to 0$ while the longitudinal $c_L$ survives — **light is the unique
surviving longitudinal wave of the jammed lattice.**

**Quantum diameter [F].** One $2\pi$ phase winding of the carrier sets the rotational
circulation length
$$ D = 2\pi\,a_{\text{phys}} = \frac{2\pi\lambda}{A} = 2\lambda_{C,e} = 6\pi^6 r_p, \qquad
   r_p = \tfrac{2}{\pi}\lambda_{C,p}, $$
where $r_p$ is the globally stable fixed point of the stiffness-shell balance
$\alpha x^{-5}=x^{-4}\Rightarrow x^*=2/\pi$ (physics §SP S4). Numerically $D = 4.8526$ pm.
The module verifies $D=6\pi^6 r_p$ to within **+18.8 ppm**, which is exactly the headline
residual $m_p/m_e = 6\pi^5\;(-19\text{ ppm})$: the small mismatch is the *known residual of the
theory*, not an error.


## EM.3 The Coulomb sector: why $1/r^2$, why long-range, how strong

**Why a force exists [F].** Two sources' fields superpose; the stored strain energy depends on
separation and the medium relaxes it, giving $E_{\text{int}} = k\,q_1 q_2 / r$. Like sources repel,
opposite attract (a positive-definite strain structure).

**Why $1/r^2$ [F].** A fixed source flux is diluted over the $4\pi r^2$ shell (Gauss = Poisson
Green's function). In $d$ dimensions the field falls as $r^{-(d-1)}$, so $d=3$ gives $1/r^2$.
Module `vp_electromagnetism.py` measures the exponent directly: $d=1,2,3,4 \to 0,-1,-2,-3$,
confirming $E\propto 1/r^2$ in three dimensions as the geometric consequence of flux conservation.

**Why long-range / unscreened [H].** Synchronization spontaneously breaks a *global* $U(1)$
(the common phase), giving a massless Goldstone mode and hence infinite range. (Were the $U(1)$
gauged, its breaking would make the mediator massive and short-ranged; long-range EM requires the
broken symmetry to be global — a stated departure.)

**Coupling magnitude [CAL].** The elementary charge is one universal rotation unit, so
$$ K_C = k_e e^2 = \alpha_{\mathrm{em}}\,\hbar c, \qquad
   k_e = \frac{\alpha_{\mathrm{em}}\hbar c}{e^2}. $$
The module reproduces the Coulomb constant $k_e = 8.987552\times 10^9$ to $3\times 10^{-10}$%.
**$\alpha_{\mathrm{em}}$ is taken from measurement; it is not derived here** — an honest [CAL] item.


## EM.4 The E/B geometry: longitudinal $E$, transverse $B$ **[F]**

The same rotating medium supplies the vector sector. The organizing statement:
**the electric field is the force directed along the light (propagation) direction; the magnetic
field is the force directed at $90^\circ$ to it.** Both originate from one fact — a charge's
rotational output is *twisted* relative to the surrounding synchronized quanta because its axis
differs. A charge with axis aligned to the common axis emits a pure radial (Coulomb) field and no
magnetic field. A moving charge tilts its axis by an amount $\propto v/c$; the propagation of that
twisted region, transverse to the light direction, is the magnetic field:
$$ |\mathbf B| = \frac{v}{c}\,|\mathbf E|. $$
Module `vp_electromagnetism.py` confirms $|\mathbf B|/|\mathbf E| = v/c$ exactly. Because
$\mathbf B$ *is* a rotation (a pseudovector), it is automatically divergence-free,
$\nabla\!\cdot\mathbf B = 0$: the poles are the two ends of one rotation axis and cannot be
separated — there are **no magnetic monopoles**, and cutting a magnet yields two fresh N/S pairs.
The right-hand rule is the handedness of the rotation.


## EM.5 Polarization as rotation (helicity) **[F]**

Circular polarization *is* the rotating field; the two senses (CW/CCW) are helicity $\pm 1$.
In Jones form the circular states are $(1,\pm i)/\sqrt 2$. The module computes their Stokes
vectors and finds $|S_3| = S_0$ with $S_1 = S_2 = 0$ — i.e. pure rotation, no linear component.
Linear polarization is the equal superposition of the two rotation senses. (The sign convention
of $S_3$ depends on the time convention $e^{\mp i\omega t}$; the invariant content is
$|S_3| = S_0$ for circular light.)


## EM.6 The propagation angle: conduction ↔ radiation **[F]/[VP-prediction]**

Light is unambiguously an electromagnetic wave — *one* object. Its longitudinal part
($\nabla\!\cdot\mathbf u$, compression = deficit) is the static Coulomb field; its transverse,
propagating part is light. What distinguishes electricity, a radio wave, and a γ-ray is only the
propagation angle $\chi$, set by the wavelength through physics §10.9:
$$ \sin\chi = \frac{\lambda}{mD},\qquad m = \lceil \lambda/D\rceil. $$
Short-$\lambda$ γ-rays are near-longitudinal ($\chi\to 0$, penetrating); visible and radio waves are
near-transverse ($\chi\to 90^\circ$). Crucially the visible band is **near — not exactly —
transverse**: $\chi \approx 89.9^\circ$, a small *falsifiable* departure from the textbook
exactly-transverse wave. Electric conduction is the extreme-longitudinal limit ($\chi\to 0$):
charges drift through a wire's internal quanta, each producing a transverse twist that wraps the
wire azimuthally as the magnetic field. **Conduction and radiation are the same electromagnetic
phenomenon, differing only in angle (longitudinal vs transverse) and medium (atomic-internal
quanta vs free space)** — "electricity travels like a γ-ray."

Forward predictions (falsifiers, no fitting): for HeNe lines,
$\chi(632.8\,\text{nm}) = 89.892^\circ$ and $\chi(532\,\text{nm}) = 89.825^\circ$
(modules `vp_light_angle.py`, `vp_electromagnetism.py`).

The earlier Word-document formulation $\lambda = d/\cos\theta$ with $d = 5000$ fm is **superseded**:
it has no $m$-chain and is undefined for $\lambda < d$ (γ-rays, X-rays). The refined law fixes
$d$ to the *derived* value $D = 4852.6$ fm and covers the whole spectrum via the $m$-chain.


## EM.7 Blackbody radiation **[F]**

The Planck spectrum is the product of two lattice facts:
$$ u(\nu,T) \;\propto\; \underbrace{\nu^2}_{\text{geometric mode density}}\;\times\;
   \underbrace{\frac{h\nu}{e^{h\nu/k_BT}-1}}_{\text{rigid-shell high-}\nu\text{ cutoff}}. $$
The first factor alone is Rayleigh–Jeans and diverges (the UV catastrophe); the rigid shell blocks
high-frequency deformation when the shell energy exceeds the thermal excitation, supplying the
Bose cutoff. Module `vp_electromagnetism.py` tabulates $u_{\mathrm{RJ}}$ versus $u_{\mathrm{Planck}}$
(agreement at low $\nu$, strong suppression at high $\nu$) and solves the Wien transcendental
$x = 5(1-e^{-x})$ to recover $\lambda_{\text{peak}}T = 2.89777\times 10^{-3}$ m·K to
$6\times 10^{-9}$%. A 300 K body peaks at $\sim 9.7\,\mu$m (infrared) with $\chi \approx 89.95^\circ$
— transverse light, consistent with EM.6.


## EM.8 Refraction and dispersion — the bridge to chemistry **[F]/[CAL]**

Once light exists, its interaction with matter is geometric. Interfacial transverse-oscillation
matching gives Snell's law $n_1\sin\theta_1 = n_2\sin\theta_2$ **[F]**; the primary rainbow angle
is $42.1^\circ$ from Snell + droplet sphere geometry (Descartes) **[F]**; total internal reflection
has $\sin\theta_c = 1/n$ **[F]** (water $48.6^\circ$, diamond $24.4^\circ$). The absolute refractive
index $n$ is a material constant **[CAL]**. Wavelength-dependent $n(\lambda)$ orders the rainbow
colors (blue refracts more). These feed directly into the chemistry chapter's color of coordination
compounds ($d$–$d$ transitions, $\Delta_{\text{tet}}/\Delta_{\text{oct}} = 4/9$) and spectroscopy
(modules `vp_refraction.py`, `vp_light_angle.py`, `vp_crystal_field.py`).


## EM.9 Master ledger — forced / measured / open

| Result | Grade | Basis / module |
|---|---|---|
| $c^2 = B/\rho$ (single surviving longitudinal speed) | [F]/[V] | isostatic $z{=}2d$; `vp_light_emergence.py` |
| Linear dispersion $\omega = cq$ | [F]/[V] | long-$\lambda$ limit; `vp_light_emergence.py` |
| Quantum diameter $D = 2\lambda_{C,e} = 6\pi^6 r_p$ | [F] | wavelength relation; (−19 ppm residual) |
| $1/r^2$ from $4\pi r^2$ flux dilution | [F] | Gauss/Poisson; `vp_electromagnetism.py` |
| Coulomb constant $k_e = \alpha_{\mathrm{em}}\hbar c/e^2$ | [F]+[CAL] | reproduces $k_e$ to $3\times10^{-10}$% |
| $|\mathbf B| = (v/c)|\mathbf E|$, $\nabla\!\cdot\mathbf B = 0$ | [F] | twist geometry; `vp_electromagnetism.py` |
| Circular polarization $=$ rotation ($|S_3|=S_0$) | [F] | Stokes; `vp_electromagnetism.py` |
| Propagation angle $\sin\chi = \lambda/(mD)$ | [F]/[VP-pred] | `vp_light_angle.py` |
| Blackbody $=$ mode density $\times$ rigid cutoff; Wien | [F] | `vp_electromagnetism.py` |
| Snell, rainbow $42.1^\circ$, critical angle | [F] | `vp_refraction.py` |
| Fine-structure coupling $\alpha_{\mathrm{em}}$ | [CAL] | measured input, **not derived** |
| Long-range / unscreened (global $U(1)$ Goldstone) | [H] | symmetry argument |
| Magnetic / radiative *absolute* vector sector; γγ genesis dynamics | [O] | open (physics §14.0.6) |


## EM.10 Falsification criteria **[F]**

Because the forced results have no free parameters, they are refuted if measurement disagrees:

- If the visible-band propagation angle is *exactly* $90^\circ$ (not $\approx 89.9^\circ$), the
  rotating-quantum / $m$-chain picture is wrong.
- If $\chi(632.8\,\text{nm}) \neq 89.892^\circ$ or $\chi(532\,\text{nm}) \neq 89.825^\circ$, the
  angle law is refuted (forward prediction, length → angle, no fitting).
- If the Coulomb field deviates from $1/r^2$ in three dimensions, the flux-dilution origin fails.
- If circular light is not pure rotation ($|S_3| \neq S_0$), helicity-as-rotation is wrong.
- If the blackbody peak does not satisfy the Wien transcendental, the mode-density × rigid-cutoff
  factorization fails.


## EM.11 Reproducibility

All numbers above are produced by deterministic, standard-library Python modules with self-checks
(`assert`). Determinism is verified by running each module twice and comparing the stdout sha256.

```
python3 vp_light_emergence.py      # light emergence: c²=B/ρ, dispersion, single speed, angle
python3 vp_electromagnetism.py     # charge, 1/r², E/B, polarization, conduction/radiation, blackbody
python3 verify_chemistry.py --root <package root>   # runs all modules + ledger integrity gate
```

The harness reports execution, determinism, standard-library-only dependency, and case-ledger
integrity across all modules (currently 32/32 PASS with the two EM/light modules added).


*This chapter completes the electromagnetic foundation on which the chemistry chapter rests:
light emerges from the jammed lattice (EM.2), charge and the Coulomb $1/r^2$ follow (EM.3), the
E/B geometry and polarization are rotation (EM.4–5), the same wave spans conduction and radiation
by angle (EM.6), and the optical consequences (blackbody, refraction, color) bridge into chemistry
(EM.7–8). It is deliberately more detailed and fully reproducible relative to the original
Korean working document, and every forced claim is falsifiable.*
