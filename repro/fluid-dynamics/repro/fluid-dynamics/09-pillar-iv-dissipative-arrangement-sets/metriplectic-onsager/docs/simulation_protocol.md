# Simulation protocol and relation to GDB closure

This document explains how the numerical data in the reproducibility
package should be interpreted relative to the metriplectic kinetic
theory in the Letter.

## 1. GDB-based kinetic model (theory level)

In the main text and Supplemental Material the vortex gas is described
by a metriplectic kinetic equation with a collision operator
\(\mathcal{C}[f]\) that includes both forward (merger) and reverse
(split) processes,
\(v_1 + v_2 \rightleftharpoons v_3\). The corresponding transition
rates \(W_m, W_d\) are assumed to satisfy **Generalized Detailed
Balance (GDB)**, which guarantees an H-theorem for the coarse-grained
entropy and selects the maximum-entropy stationary state compatible
with the invariants. This should be read as an *effective closure*
at the level of the vortex gas, analogous to Boltzmann's molecular
chaos hypothesis, rather than as an exact microscopic symmetry of
Euler or Navier--Stokes flows.\footnote{See the discussion below
Eq.~(3) and Eq.~(4) in the main text.}

In this theoretical setting the H-theorem is a structural consequence
of the metriplectic brackets and GDB: it holds for any trajectory of
the coarse-grained kinetic equation, independent of the particular
numerical scheme.\footnote{The detailed algebra and proof are given
in S1--S2 of the Supplemental Material.}

## 2. Point-vortex simulations (data level)

The actual numerical data used for Fig.~2 and the robustness plots in
this package are obtained from **freely decaying point-vortex
simulations** that emulate the kinetic model but do not explicitly
resolve the full space of mergers and splits:

- The simulations track a set of identical-sign point vortices in a
  doubly periodic box, with an interaction energy equal to the usual
  Kirchhoff Hamiltonian.
- A merger event is triggered whenever two like-signed vortices
  approach within a cross-section radius \(r_c\). The two vortices
  are then replaced by a single vortex with combined circulation.
- The loss of interaction (binding) energy at each merger is
  accumulated in an internal reservoir \(H_\mathrm{int}\). The
  event-driven dissipation rate \(\varepsilon_{\mathrm{events}}\)
  is defined as the time rate of change of \(H_\mathrm{flow}\),
  i.e. the negative of the binding-energy release rate.

Crucially, in the **freely decaying regime** that we focus on, vortex
mergers strongly dominate over reverse split events. The numerical
implementation therefore samples only the *forward* merger channel.
This should be interpreted as the strongly irreversible, low-noise
limit \(J^- \ll J^+\) of the GDB kinetic closure. In this limit the
H-theorem derived in the theory section continues to act as an
upper bound on entropy production, but the simulations effectively
follow a one-way relaxation path towards higher entropy.

## 3. Practical interpretation

From the standpoint of reproducibility:

- The Letter's statements about the H-theorem and GDB refer to the
  **coarse-grained kinetic model** and are established analytically.
- The numerical scripts in this package implement a simplified
  **forward-merger dynamics** designed to mimic the decaying limit of
  that closure and to isolate the role of binding-energy release in
  sustaining anomalous dissipation.
- The robustness scans (multiple \(N\), \(r_c\), and random seeds)
  show that, within this class of models, the non-zero saturation of
  \(\varepsilon_{\mathrm{events}}\) is a persistent feature rather
  than a numerical artifact of a particular realization.

Users who wish to implement a fully GDB-symmetric merger--split
dynamics can treat the present scheme as the strongly irreversible
limit of such a model.

## 4. Additional remarks on dissipation and time scales

Even though the forward-merger simulations in this package do not
enforce Generalised Detailed Balance (GDB) at the microscopic level,
the metriplectic structure of the kinetic model still provides an
H-theorem at the coarse-grained level. In practice, the irreversible
merger limit corresponds to a non-equilibrium situation in which the
system explores states with enhanced entropy production. From this
perspective, the analytical H-theorem is best regarded as an upper
bound on the dissipation rate: breaking GDB does not switch off
dissipation, but rather allows for more irregular and potentially
stronger entropy production within the constraints of the invariants.

For readers interested in the mapping between discrete merger events
and a continuum time scale, Table S1 in the Supplemental Material
provides a "discrete--continuum dictionary". At fixed effective
Reynolds number $Re_{\mathrm{eff}}$, increasing the number of vortices
$N$ increases the frequency of merger events. In the freely decaying
limit this enhanced event rate compensates for the decrease of the
individual energy drops, leading to an approximately constant mean
event-driven dissipation rate $\langle \varepsilon_{\mathrm{events}}
\rangle$. The data in `data/processed/epsilon_events_summary.csv`
and the associated robustness plots provide a concrete numerical
realisation of this mechanism.
