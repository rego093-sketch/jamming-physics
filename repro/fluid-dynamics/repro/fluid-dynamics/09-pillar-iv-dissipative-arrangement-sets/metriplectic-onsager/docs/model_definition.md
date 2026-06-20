# Discrete vortex metriplectic model (summary)

This note records the concrete model choices used in the reproducible
data package. It is intended to complement the algebraic description
in S1 of the Supplemental Material.

- **Degrees of freedom:** identical-sign point vortices at positions
  \(\{\mathbf{x}_i\}_{i=1}^N\) in a doubly periodic box of side
  \(L\). The state vector \(\Psi\) consists of all vortex
  positions together with an internal scalar reservoir \(H_\mathrm{int}\).
- **Flow energy:** the resolved Hamiltonian \(H_\mathrm{flow}\) is
  the Kirchhoff pair-interaction energy
  \[
    H_\mathrm{flow}
    = - \frac{1}{4\pi}
      \sum_{i \ne j} \Gamma_i \Gamma_j
      \ln \bigl| \mathbf{x}_i - \mathbf{x}_j \bigr|_P ,
  \]
  where \(|\cdot|_P\) denotes the periodic distance on the torus.
- **Internal energy:** the internal reservoir \(H_\mathrm{int}\)
  accumulates the binding energy released at merger events,
  \(H_\mathrm{int}(t) = \sum_\text{events} \Delta E\).
- **Event dissipation:** the instantaneous event-driven dissipation
  rate is defined as
  \(\varepsilon_{\mathrm{events}} = -\dot H_\mathrm{flow}\),
  computed from the change of \(H_\mathrm{flow}\) along the
  metriplectic trajectory.

The ensemble-averaged values of \(\varepsilon_{\mathrm{events}}\)
and the corresponding effective Reynolds numbers
\(Re_{\mathrm{eff}}\) for different \(N\), \(r_c\), and random
seeds are stored in the CSV files under `data/` and plotted by the
scripts in `src/plot_robustness.py`.

## Physical interpretation of the internal reservoir $H_{\mathrm{int}}$

In the freely decaying regime, vortex mergers proceed in a highly
anisotropic fashion: while the the cores coalesce into fewer, stronger
vortices, thin vorticity filaments are expelled to satisfy conservation
of circulation and angular momentum. These filaments become
progressively finer and more convoluted in time, eventually reaching
scales at which viscous or numerical dissipation becomes effective.

The internal reservoir $H_{\mathrm{int}}$ in this reproducible model
should be interpreted as a bookkeeping device for the interaction
energy that is transferred into these unresolved filamentary
structures. In other words, the metriplectic dynamics does not destroy
energy; it re-labels the portion of the flow energy that has been
pushed into increasingly fine vortex filaments as "internal" energy.

This picture is closely related to the Duchon--Robert formulation of
anomalous dissipation in rough velocity fields, where the energy flux
$D(u)$ measures the rate at which kinetic energy is transferred from
resolved to unresolved scales. In our setting, the growth rate
$\dot H_{\mathrm{int}}$ plays the role of such a flux: it quantifies
how quickly energy is pumped into the filamentary degrees of freedom
that would ultimately be damped by viscosity in a full Navier--Stokes
simulation.
