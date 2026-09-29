\newpage

# Appendix O: Open-Items Register (what is honestly unsolved)

This appendix consolidates every [O] / [H] item carried in this volume, with the specific physics
that would be required to close it. None is a defect to be fixed; each is open research. Closing any
of them would be *new physics*, not a correction — and forcing a closure would reintroduce exactly
the kind of overfitting (the retracted $\sqrt{2.5}$ rule, the refuted electron amplitude) that this
program has been careful to discard.

## O.1 Chemistry — peripheral quantitative opens (independently re-examined)

Each was re-examined by `vp_open_items_reexam.py`; all four correctly remain open because the
closing variable lies *outside* VP $\pi$-geometry.

| Open item | Module | Closing physics (outside VP geometry) |
|---|---|---|
| Absolute bond-dissociation energy | `vp_bond_energy.py` | the Morse range $\beta = a\,r_e$ (anharmonicity; lone-pair / polarity). A direct test found $\beta$ uncorrelated with bond order ($r = +0.18$), so $\sqrt2$ geometry alone cannot close it. |
| Defect knockdown (real vs ideal strength) | `vp_strength.py` | dislocation density $\rho_{\mathrm{disl}}$ (processing-dependent; Taylor $\tau=\alpha G b\sqrt{\rho}$) — intrinsically a calibration input. |
| Naïve shell correction | `vp_shell_correction.py` | the nuclear spin–orbit shell model (Mayer–Jensen); a uniform proximity bonus over-corrects because $\Delta B$ changes sign across magic numbers. |
| Electron affinity / absolute IE | `vp_dblock_chemistry.py` | electron screening constants (Clementi–Raimondi); Slater rules give only the correlation (sign correct $8/18$). |

## O.2 Electromagnetism — foundational opens (deeper than the chemistry set)

| Open item | Grade | Status |
|---|---|---|
| **Electromagnetic coupling $\alpha_{\mathrm{em}}$ (the "$1/137$")** | [CAL] | The *strength* of electromagnetism is a measured input; the framework derives the *form* ($1/r^2$, $c$, $E/B$, polarization, the angle law) but not the magnitude. Physics §14.5 states it is not derived. A topological / phase-winding route has been scaffolded but is computationally heavy and is **on hold**; there is no known low-cost shortcut. Closing it is new physics. |
| **Long-range / unscreened EM (global $U(1)$)** | [H] | Masslessness and infinite range rest on the breaking of a *global* (not gauged) $U(1)$, giving a Goldstone mode — a stated departure from gauge theory. The AQD dynamics supply causality (§EM.12) but not the gauge structure; this remains a hypothesis. |
| **Absolute vector (magnetic / radiative) sector** | [O] | The longitudinal (Coulomb / $E$) sector — including the dynamic equations, Poynting flow, and causality — is closed in §EM.12. The full vector $\mathbf E/\mathbf B$ curl structure (Faraday's $\nabla\times\mathbf E$ and Ampère–Maxwell's $\nabla\times\mathbf B$ in vector form, with the magnetic field as an independent transverse pseudovector and its absolute magnitude) is **not** supplied by the scalar/longitudinal treatment. This is the principal open structural item of the EM chapter. |
| **$\gamma\gamma$ genesis dynamics** | [O] | How charge is created from photon collisions ($\gamma\gamma\to e^+e^-$) at the level of lattice dynamics is open. |

## O.3 What is *closed* (for contrast)

The longitudinal electrodynamics is complete and reproducible: light emergence ($c^2=B/\rho$), the
static Coulomb $1/r^2$, the $|\mathbf B|=(v/c)|\mathbf E|$ ratio and $\nabla\!\cdot\mathbf B=0$,
polarization as helicity, the conduction–radiation angle, blackbody radiation, refraction, and — as
of this edition — the **dynamic field equations, Poynting's theorem, energy conservation,
uniqueness, and light-cone causality** (§EM.12). On the chemistry side the forced body is complete:
bonding geometry, coordination color, the metal $d$-shell fates, thermodynamics, equilibrium,
kinetics, solution and electrochemistry, materials geometry, and the nuclear skeleton; and the
applications are re-grounded on the verified $d$-band descriptor (catalysis, ammonia, water
electrolysis, energy storage, new materials, CO$_2$ reduction), with the non-working mechanisms
(magnetic desalination, amplitude-to-electricity ESS) honestly refuted and replaced by working
alternatives.
