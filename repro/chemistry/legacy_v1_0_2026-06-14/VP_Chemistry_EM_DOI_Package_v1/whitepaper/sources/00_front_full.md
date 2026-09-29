---
title: "VP Chemistry & Electromagnetism"
subtitle: "Derived from a Single Anchor on the Jamming-Lattice Substrate — Foundations, Optics, and Applications"
author: "Young jae Lee (ORCID 0009-0002-7535-8245), Independent researcher, Daegu, Korea"
date: "2026-06-14 · DOI (reserved) 10.5281/zenodo.20680541"
---

# Abstract

This volume consolidates the Volume-Particle (VP) account of **electromagnetism, chemistry, and
their engineering applications** into a single reproducible whitepaper. Everything is derived from
one observational anchor — the electron, treated as a rotational dent in an infinitely rigid, fully
packing "jamming" lattice — using only $\pi$-geometry and the electromagnetic inverse-square law.
It is a companion to the VP Theory (physics) whitepaper, from which it takes the fundamental
electromagnetic mechanism (§10, §14) as input.

Three results anchor the account. First, **light is not assumed but emerges**: at the isostatic
point of the jammed lattice the relaxed shear modulus vanishes while the bulk modulus stays finite,
so a single longitudinal wave survives at $c^2 = B/\rho$; a deterministic lattice simulation
reproduces this to 0.06%. Second, on that substrate charge is synchronized rotation, the Coulomb
$1/r^2$ follows from three-dimensional flux conservation, the $E/B$ geometry and polarization are
rotation, and the same wave spans conduction and radiation by a single angle
$\sin\chi=\lambda/(mD)$; **and the dynamic field equations, the Poynting energy flow, and a strict
light-cone causality are supplied in longitudinal form** (Chapter EM, §EM.12, from the AQD
axiomatic field dynamics). Third, chemistry follows by sphere geometry and rotation — bonding
angles $\arccos(-1/3)$, the crystal-field ratio $4/9$, the close-packing fraction $0.7405$, the
nuclear magic skeleton, thermodynamics, equilibrium, kinetics, solution and electrochemistry — and
the engineering applications (catalysis, fertilizer, water, energy storage, new materials, and
**CO$_2$ reduction**) are re-grounded on the **verified $d$-band energy descriptor**, not on the
refuted electron-amplitude variable.

Every forced result has zero free parameters and is therefore falsifiable; measured constants are
labelled as calibration inputs and never tuned per result; open problems — most fundamentally the
electromagnetic coupling $\alpha_{\mathrm{em}}$ itself — are admitted rather than disguised. All
numbers are reproduced by deterministic, standard-library Python modules (a 38-module
chemistry/EM core with a 176-row case ledger, plus a 9-module / 46-row applications package) with
verification harnesses (core 38/38 pass; applications 9/9 pass) and numeric-drift gates that check
every displayed number against canonical recomputation and module output (both pass, zero drift).

**Keywords:** Volume-Particle theory, jamming lattice, light emergence, $c^2=B/\rho$,
electromagnetism, Poynting, causality, Coulomb $1/r^2$, propagation angle, VSEPR, crystal-field
$4/9$, $d$-band catalysis, CO$_2$ reduction, reproducibility, falsifiability.


# Introduction

## The program and this consolidation

The VP framework posits a vacuum built from infinitely rigid, fully packing particles — a jammed
lattice. From this single substrate the physics whitepaper derives the speed of light, the proton
radius, and a ladder of dimensionless constants. This whitepaper extends the program into
**electromagnetism, chemistry, and applications**, asking how much of each follows with *no
adjustable parameters* once light has emerged. This consolidated edition gathers what were
previously separate chapter files (EM, CH, CM, CC, CT) and the applications package (CA) into one
volume, and incorporates two completions made after the first release: the **dynamic-field /
Poynting / causality** addendum (§EM.12) and the **CO$_2$ electrocatalytic reduction** module
(§CA, re-grounded on the $d$-band descriptor).

## Why light first

The organizing principle is sequencing: **light must emerge before anything else follows.** Once
the lattice supports a single longitudinal wave at $c^2 = B/\rho$ with linear dispersion
$\omega = cq$, a wavelength exists; once a wavelength exists, the propagation angle, the quantum
diameter, refraction, and color follow; and once charge is identified as synchronized rotation, the
Coulomb law and the entire chemical edifice follow. Chapter EM begins with the emergence of light
and develops electromagnetism (now including its dynamic and causal structure); the chemistry
chapters build on that foundation; the applications chapters close the arc on verified physics.

## How claims are graded (the No-Tuning discipline)

- **[F] forced** results are dimensionless geometry or integers with nothing to adjust (the
  tetrahedral angle $\arccos(-1/3)$, the ratio $4/9$, the packing fraction $\pi/(3\sqrt2)$). They
  cannot be tuned, so they are *refuted* if measurement disagrees.
- **[CAL] calibration inputs** are measured constants (the fine-structure coupling, spectroscopic
  constants, standard potentials, $d$-band centers) fixed once and used consistently; quantities
  *derived* from them and then matching measurement are predictions, not fits.
- **[V] simulation-measured**, **[H] hypothesis**, and **[O] open** label what a deterministic
  simulation shows, what remains a working hypothesis, and what is honestly unsolved.

A central methodological result of this program is **negative**: the early "electron amplitude
(fm)" mechanism for catalysis, bond-angle deviations, magnetic desalination, and black-copper
power generation was tested and **refuted**, and is replaced — where a working mechanism exists —
by the correct variable (the $d$-band *energy*, equilibrium thermodynamics, real magnetostatics,
Carnot-bounded storage). Chapter CT records this refutation in full; the applications chapter is
built on the replacement. Letting the refuted mechanism go is what makes the surviving results
trustworthy to build on.

## Reproducibility as a first-class requirement

Every numeric claim is produced by a deterministic module using only the Python standard library;
determinism is verified by re-running and comparing output hashes. Verification harnesses check
execution, determinism, dependency, and case-ledger integrity (chemistry/EM core: 38/38;
applications: 9/9), and numeric-drift gates check that every displayed number matches both the
canonical closed-form recomputation and the module output (both pass, zero drift). Nothing here is
asserted that the reader cannot re-run.

## Boundary with the physics whitepaper

The *fundamental* electromagnetic mechanism — light as a rotational transverse wave, the single
surviving longitudinal speed, and the $1/r^2$ Green function — is established in the physics
whitepaper (§10, §14). This document consumes those results and develops the chemical, optical, and
dynamical consequences. The electromagnetic coupling strength $\alpha_{\mathrm{em}}$ is **not
derived** in this framework (physics §14.5); it is an honest open item, carried as [CAL].

\newpage
