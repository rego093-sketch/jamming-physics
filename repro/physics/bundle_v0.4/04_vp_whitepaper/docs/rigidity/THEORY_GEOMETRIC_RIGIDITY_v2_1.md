# Theory of Geometric Rigidity (v2.1)

**Context:** Axiomatic Quantized Dynamics (Volume Particle Theory, VP)

**Author:** Young Jae Lee (Independent Researcher)

**Date:** 2025-12-15

## Abstract

We propose a unified view where the rigidity of matter and space is determined by the geometric arrangement (jamming/locking) of fundamental Volume Particles (VPs). Instead of treating elastic moduli and the speed of light as unrelated empirical constants, we parameterize “rigidity” by an Effective Coordination Number N.

By combining:

- a geometric “gap” delta = 4 - N,
- an inverse-gap barrier U_barrier proportional to 1/delta,
- and Boltzmann stability,

we obtain a universal rigidity form:

Psi(N) = Psi_base * exp[ kappa * ( 1/(4 - N) - 1 ) ].

This yields a divergence as N -> 4 (solid-like tetrahedral locking) and a finite base rigidity at N = 3 (liquid/vacuum fluid baseline).

> DOI note (reproducibility): the case-study table in this DOI is generated from a locked CSV using `04_vp_whitepaper/scripts/run_rigidity_theory_v2_1.py`.

## 1. Geometric axiom

- Space is filled with VPs.
- “Rigidity” Psi is the resistance formed when particles lock.
- The degree of locking is quantified by the Effective Coordination Number N.

## 2. Dimensional imperative

- N = 4: the minimum number of points to enclose a non-collapsible 3D volume (tetrahedron). This is treated as the geometric singularity of perfect locking.
- N = 3: three points define a plane; a system can maintain surface continuity but lacks volume bracing. This is treated as the liquid/vacuum-fluid baseline.

## 3. Derivation skeleton

1) Gap: delta = 4 - N.

2) Barrier scaling (model assumption): U_barrier = C_geo / (4 - N).

3) Escape probability: P_escape ~ exp( -U_barrier / E_thermal ).

4) Structural stability (rigidity proxy): Psi ~ 1/P_escape ~ exp( +U_barrier / E_thermal ).

5) Normalize at N = 3:

Psi(N) = Psi_base * exp[ kappa * ( 1/(4 - N) - 1 ) ], where kappa = C_geo / E_thermal.

## 4. Scaling statements (interpretation layer)

- Vacuum baseline: Psi_base(vac) ~ c^2 (hypothesis: the speed of light is the intrinsic rigidity scale of the VP vacuum fluid).
- Matter baseline: Psi_base(matter) ~ v_sound^2 (hypothesis: chemical bonds realize a reduced rigidity scale).
- A material efficiency factor eta may relate matter to vacuum: Psi_matter ~ eta * c^2 * (geometric factor).

## 5. Case studies

The DOI includes a small locked table of modulus ratios (solid/liquid) and the implied N_eff computed by the formula above, with kappa fixed for the table generation.

- Water (Ice Ih -> Water)
- Silica (Quartz -> Glass)
- Gallium Arsenide (solid -> liquid)

Silicon/Germanium are tracked as a “collapse class” where shear vanishes in the melt, so the simple ratio model is not applied.

