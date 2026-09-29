# Conduction in Copper and Magnetism in Iron: Two Fates of the *d*-Shell

**VP Chemistry & Electromagnetism Whitepaper — Chapter CM**
DOI (reserved): 10.5281/zenodo.20680541 · Builds on Chapter EM (electromagnetism) and Chapter CH
(chemistry). Status grades as in Chapter EM. Numbers reproduced by `vp_copper_conduction.py` and
`vp_iron_magnetism.py` (deterministic, standard-library, self-checking).

> Copper conducts and iron magnetizes for the same root reason, read two ways. Copper's inner
> *d*-shell is **full**, freeing its outer electron into a conducting sea; iron's *d*-shell is
> **partly empty**, leaving unpaired rotations that align into a magnet. A filled shell makes a
> conductor; an unfilled shell makes a magnet.


## CM.0 The two questions

This chapter answers two concrete questions about metals using the electromagnetism of Chapter EM:

1. **Electricity is an electromagnetic wave — how does it pass *through the inside* of copper,**
   when copper (a metal) *reflects* ordinary light?
2. **What is the principle of iron's magnetism** — and in particular, why iron (and cobalt,
   nickel) but not copper, and not even manganese, which has *more* unpaired electrons than iron?
   (The physics whitepaper took the "why Fe and not Cu" criterion as an empirical input, §14; here
   it is derived.)


## CM.1 The paradox

Light is a transverse electromagnetic wave, and metals reflect it — that is why copper is shiny and
opaque. Yet electricity is *also* electromagnetic, and it travels straight through the body of a
copper wire. How can the same medium reflect one electromagnetic disturbance and transmit another?

The resolution is the propagation angle of Chapter EM (§EM.6). Electricity is the **extreme
longitudinal limit** ($\chi \to 0$) of the electromagnetic wave, while visible light is the
**transverse limit** ($\chi \to 90^\circ$). The same free-electron sea reflects the transverse wave
and transmits the longitudinal one. Same medium, opposite fates, set by angle.


## CM.2 Copper's free-electron sea **[F]/[CAL]**

Copper is $[\mathrm{Ar}]\,3d^{10}4s^1$: the inner $3d$ shell is **full**, and the single $4s$
electron is delocalized into a conducting sea. The free-electron density is
$$ n = \frac{\rho\,N_A\,Z_{\text{free}}}{M} = 8.49\times 10^{28}\ \mathrm{m^{-3}} $$
(one free electron per atom; $\rho, M$ measured **[CAL]**). This sea is the "internal quanta" through
which conduction propagates.


## CM.3 Why transverse light is reflected — the plasma frequency **[F]/[CAL]**

The free-electron sea has a natural oscillation frequency, the plasma frequency
$$ \omega_p = \sqrt{\frac{n e^2}{\varepsilon_0 m_e}} = 1.64\times 10^{16}\ \mathrm{rad/s}
   \;\;(f_p = 2.6\times 10^{15}\ \mathrm{Hz},\ \lambda_p = 115\ \mathrm{nm},\ \text{ultraviolet}). $$
Below $\omega_p$ — radio, infrared, **all of visible light** — an incident transverse wave drives the
free electrons, which re-radiate and **reflect** it: this is exactly why metals are shiny and opaque
(`vp_copper_conduction.py`, §1). Above $\omega_p$ (X-rays) the electrons cannot follow and the metal
becomes transparent. The transverse electromagnetic wave is turned back by the very sea that carries
the current.


## CM.4 Why longitudinal electricity is transmitted — conduction as $\chi \to 0$ **[F]**

The longitudinal mode is different. A longitudinal ($\chi \to 0$) electromagnetic disturbance is a
**density/pressure wave of the electron sea** that threads straight along the wire — straighter even
than a $\gamma$-ray. It is not reflected because it is not a transverse oscillation of the surface
electrons; it propagates *through* the internal quanta of the copper atoms, not through vacuum or
air (physics §14). This longitudinal disturbance is the current. The angle that makes light
reflect (transverse) is the angle that makes electricity transmit (longitudinal). Two physical facts
fix conduction at $\chi \to 0$: small amplitude (a low-amplitude disturbance threads straight; if the
amplitude grows the path tilts transverse and the signal *leaves* the copper as radiative loss) and
medium (it runs through the atomic-internal quanta).


## CM.5 The skin effect **[F]/[CAL]**

The transverse and longitudinal pictures are quantitatively distinct. A transverse wave that does
enter the metal decays within the skin depth
$$ \delta = \sqrt{\frac{2}{\mu_0\,\sigma\,\omega}}: \quad
   8.4\ \mathrm{mm}\ (60\ \mathrm{Hz}) \to 2.1\ \mu\mathrm{m}\ (1\ \mathrm{GHz}). $$
High-frequency transverse fields are confined to a micron-thin surface layer, while the
direct/low-frequency longitudinal current fills the whole cross-section (`vp_copper_conduction.py`,
§3).


## CM.6 Three velocities — drift, signal, Fermi **[F]/[CAL]**

A common confusion is dissolved by separating three speeds (`vp_copper_conduction.py`, §4):

- **Drift velocity** $v_d = J/(ne)$: for $J = 10^6\ \mathrm{A/m^2}$, only $0.074\ \mathrm{mm/s}$ —
  the electrons themselves crawl.
- **Signal velocity** $\sim c$: the longitudinal field disturbance travels near light speed, so a
  lamp lights essentially instantly even though the electrons barely move.
- **Fermi velocity** $v_F = 1.57\times 10^6\ \mathrm{m/s}$: the electrons at the Fermi surface move
  fast, but their *net* drift is the slow $v_d$.

The predicted Fermi energy $E_F = \hbar^2(3\pi^2 n)^{2/3}/(2m_e) = 7.04\ \mathrm{eV}$ matches the
measured $\approx 7.0\ \mathrm{eV}$.


## CM.7 Why copper conducts so well **[F]/[CAL]**

The Drude relation $\sigma = ne^2\tau/m_e$ with $\sigma_{\mathrm{Cu}} = 5.96\times 10^7\ \mathrm{S/m}$
gives a relaxation time $\tau = 2.5\times 10^{-14}\ \mathrm{s}$ and a mean free path
$\ell = v_F\tau = 39\ \mathrm{nm}$. Copper's **filled** $3d^{10}$ shell hands its $4s^1$ electron to a
low-scattering sea — exactly the property that, in iron, is *absent*. This is the hinge of the whole
chapter: **a filled inner shell yields conduction; an unfilled one yields magnetism.**


## CM.8 The magnetic field of a current — and Joule loss **[F]**

A drifting charge tilts its rotation axis by $\sim v/c$ (§EM.4), shedding a small transverse twist
perpendicular to the drift; propagating sideways it wraps the wire azimuthally as the magnetic field
$B = \mu_0 I/(2\pi r)$, with circulation sense set by the rotation handedness (the right-hand rule).
The transverse twist has two fates: the **returned** part is the reactive $B$ field itself (present
even at zero loss, as in a superconductor), and the **un-returned** fraction is dissipation (Joule
loss). Thus $B$ and resistive loss share one origin — the transverse twist of moving charge — as its
returned versus un-returned parts; $B$ itself is not the loss.


## CM.9 Iron's magnetism — the principle **[F]/[CAL]/[O]**

Magnetism is aligned rotation. A magnetic moment is the rotation of an unpaired electron — the same
rotation that *is* electric charge (§EM.1) and helicity (§EM.5). For a material to be a permanent
(ferro)magnet, **two conditions must both hold**, and the pair derives exactly which elements
magnetize.


## CM.10 Criterion 1 — unpaired *d*-electrons (this is why **not copper**) **[F]**

A localized moment requires an **unfilled** $d$-shell with unpaired electrons (Hund's rule). For
$3d^{n_d}$ the unpaired count is $n_d$ if $n_d\le 5$ else $10-n_d$, and the spin-only moment is
$\mu = \sqrt{n(n+2)}\,\mu_B$ (`vp_iron_magnetism.py`, condition 1):

| element | config | unpaired $d$ | $\mu_{\text{so}}\,[\mu_B]$ | moment? |
|---|---|---|---|---|
| Mn | $3d^54s^2$ | 5 | 5.92 | yes |
| Fe | $3d^64s^2$ | 4 | 4.90 | yes |
| Co | $3d^74s^2$ | 3 | 3.87 | yes |
| Ni | $3d^84s^2$ | 2 | 2.83 | yes |
| **Cu** | $3d^{10}4s^1$ | **0** | **0.00** | **no** |

Copper's $3d^{10}$ shell is full: zero unpaired $d$-electrons, no localized moment. Its $4s^1$ is a
free conduction electron, not a localized moment. **Copper fails condition 1 and cannot be magnetic
— the same filled shell that makes it a superb conductor.**


## CM.11 Criterion 2 — positive exchange (this is why **not manganese**) **[F]/[CAL]**

Having moments is not enough; neighbouring $d$-rotations must align **parallel** (ferromagnetic),
not antiparallel (antiferromagnetic). The Bethe–Slater criterion uses the ratio
$D/d$ = interatomic distance / $3d$-orbital diameter: above a critical value ($\approx 1.5$) the
exchange integral is positive (parallel, ferromagnetic); below it the exchange is negative
(antiparallel, antiferromagnetic) (`vp_iron_magnetism.py`, condition 2):

| element | $D/d$ | exchange | alignment |
|---|---|---|---|
| Cr | 1.18 | $J<0$ | antiparallel (antiferro) |
| Mn | 1.47 | $J<0$ | antiparallel (antiferro) |
| Fe | 1.63 | $J>0$ | parallel (ferro) |
| Co | 1.82 | $J>0$ | parallel (ferro) |
| Ni | 1.98 | $J>0$ | parallel (ferro) |

Manganese has **five** unpaired electrons — more than iron — yet $D/d = 1.47 < 1.5$ gives $J<0$, so
its moments align antiparallel and cancel: **manganese fails condition 2 and is antiferromagnetic.**
Cobalt ($D/d = 1.82$) sits near the exchange maximum.


## CM.12 The derivation — 7/7 classification **[F]**

Applying both conditions reproduces the observed magnetic class of the late $3d$ series with no
fitted magnetic parameter (`vp_iron_magnetism.py`, summary):

| element | unpaired $d$ | $D/d$ | derived | observed | ✓ |
|---|---|---|---|---|---|
| Cr | 5 | 1.18 | antiferro | antiferro | ✓ |
| Mn | 5 | 1.47 | antiferro | antiferro | ✓ |
| Fe | 4 | 1.63 | ferro | ferro | ✓ |
| Co | 3 | 1.82 | ferro | ferro | ✓ |
| Ni | 2 | 1.98 | ferro | ferro | ✓ |
| Cu | 0 | — | non-magnetic | non-magnetic | ✓ |
| Zn | 0 | — | non-magnetic | non-magnetic | ✓ |

**7/7.** Copper is non-magnetic by condition 1, manganese is antiferromagnetic by condition 2, and
only iron, cobalt, and nickel satisfy both — the "why Fe and not Cu" the physics whitepaper left as
input is here derived.


## CM.13 Curie temperature, domains, and $\nabla\!\cdot\mathbf B = 0$ **[F]/[CAL]**

Thermal rotation destroys alignment above the Curie temperature, where $k_BT_C$ is of order the
exchange energy: Fe 1043 K, Co 1388 K (highest, matching the strongest exchange), Ni 627 K
(`vp_iron_magnetism.py`). Below $T_C$, exchange aligns moments into **domains**; an external field
moves the domain walls. Because $\mathbf B$ *is* a rotation axis (§EM.4), it is divergence-free,
$\nabla\!\cdot\mathbf B = 0$: the poles are the two ends of one axis and cannot be separated — no
monopoles, and cutting a magnet yields two fresh N/S pairs. Hysteresis is the part of the alignment
that does not return — the permanent magnet — and heating above $T_C$ erases it. The
$\nabla\!\cdot\mathbf B = 0$ seen abstractly in Chapter EM becomes, in iron, the macroscopic fact of
domains and permanent magnets. (The metallic moments are non-integer — Fe 2.22, Co 1.72, Ni 0.62
$\mu_B$ — an itinerant/band effect marked **[O]**; the localized Hund count gives the correct
*ordering* and the magnetic *class*.)


## CM.14 The unifying picture

Copper and iron are the two fates of the $d$-shell:

- **Copper — filled $3d^{10}$ → free $4s$ electron → conduction.** Electricity passes through copper
  as the longitudinal ($\chi\to 0$) electromagnetic mode of that free sea, while light (transverse)
  is reflected by it.
- **Iron — unfilled $3d^6$ → unpaired moments → magnetism.** With positive exchange ($D/d>1.5$) the
  moments align into a ferromagnet; the aligned rotation is the magnetic field.

A filled inner shell makes a conductor; an unfilled one makes a magnet. Both are the same rotation —
the rotation that is charge, light, and helicity — expressed as a delocalized current in copper and
as an aligned moment in iron.


## CM.15 Falsification and reproducibility **[F]**

- If a metal's plasma frequency did not predict its reflectivity edge (shiny below $\omega_p$,
  transparent above), the plasma-reflection account of conduction-vs-light fails.
- If manganese (more unpaired electrons than iron) were ferromagnetic, or copper ($3d^{10}$) were
  ferromagnetic, the two-condition criterion fails.
- If the derived magnetic class disagreed with any late-$3d$ metal, the derivation fails (it is 7/7).

```
python3 code/foundation/vp_copper_conduction.py   # plasma freq, skin depth, drift/signal/Fermi
python3 code/foundation/vp_iron_magnetism.py      # two-condition ferromagnetic criterion (7/7)
```

Both modules are deterministic (stdout sha256 identical on re-run) and standard-library only.


*Copper and iron close the loop opened in Chapter EM: charge is rotation, and that one rotation
appears as a longitudinal current threading copper's filled-shell electron sea, and as an aligned
moment in iron's unfilled $d$-shell. The conductor and the magnet are the same physics, divided by
whether the inner shell is full.*
