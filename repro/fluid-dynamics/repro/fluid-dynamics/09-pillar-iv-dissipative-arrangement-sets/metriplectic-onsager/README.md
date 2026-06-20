# Reproducibility Package: Onsager Anomaly Dissipation Saturation

This archive accompanies the manuscript

> **"Vortex-Merger Thermodynamics in 2D Turbulence:  
>  A Metriplectic Scenario for the Onsager Anomaly"**

and provides a minimal, self-contained set of Python scripts and data
to regenerate

- the dissipation–saturation figure (viscous, event, and total
  dissipation vs effective Reynolds number), and
- the robustness diagnostics for different particle numbers and
  random seeds,

without requiring supercomputing resources.

The directory layout is

- `data/raw/epsilon_events_ensemble.csv` – pre-computed ensemble of
  metriplectic vortex runs (produced offline with the ADG solver
  described in the Letter);
- `data/processed/*.csv` – summary tables derived from the raw
  ensemble and used for plotting;
- `NS_reference/` – a lightweight pseudo-spectral Navier–Stokes solver
  and the corresponding viscous dissipation data;
- `src/` – small helper scripts for summarising the data and producing
  figures;
- `docs/` – short notes on the discrete vortex model and the
  simulation protocol.

All scripts depend only on `numpy`, `pandas`, and `matplotlib`
(see `requirements.txt`).

## 1. Quick reproduction of the main figure

From the top-level directory (`metriplectic-onsager-repro/`) run

```bash
python -m src.parameter_sweep
python NS_reference/generate_viscous_data.py   # optional; regenerates NS curve
python -m src.plot_dissipation_saturation
```

This will create

- `data/processed/dissipation_vs_Re_metriplectic.csv` – the compact
  `(Re_eff, eps_bind, eps_tot)` table distilled from the ensemble;
- `NS_reference/viscous_dissipation_vs_Re.csv` – the viscous
  dissipation versus effective Reynolds number (Navier–Stokes
  reference);
- `figures/dissipation_saturation.png` – the plot corresponding to
  Fig. 2 in the Letter.

The `parameter_sweep` script does **not** run new simulations; it
simply summarises the ensemble in `data/raw/epsilon_events_ensemble.csv`
into a form convenient for plotting.  The raw ensemble itself was
generated using a high-precision Average Discrete Gradient (ADG)
integrator that preserves the metriplectic structure to machine
precision.

## 2. Robustness plots

To visualise how the event-driven dissipation depends on particle
number `N`, merger radius `r_c`, and random seed, run

```bash
python -m src.plot_robustness
```

which produces

- `figures/robustness_Nscan.png` – mean ± one standard deviation of
  the event dissipation versus effective Reynolds number for several
  `N`, and
- `figures/robustness_seedscatter.png` – scatter of individual
  ensemble members in the `(Re_eff, eps_bind)` plane.

These diagnostics show that the non-zero saturation of
`eps_events` is stable under changes in `N` and initial conditions
within this class of metriplectic vortex models.

If you have regenerated the raw ensemble file with your own
implementation of the metriplectic point-vortex dynamics, you can
rebuild the processed summary via

```bash
python -m src.robustness_scans
```

before re-running the plotting scripts.

## 3. Relation to the metriplectic kinetic theory

The Python code in this archive is intentionally lightweight and
transparent.  It is meant as a *reference implementation* and data
post-processing pipeline, not as the production ADG solver itself.

- The **kinetic theory and H-theorem** are derived in the main text
  and Supplemental Material.
- The **concrete discrete vortex model** (degrees of freedom,
  Hamiltonian, merger rule, and definition of the internal reservoir
  `H_int`) is summarised in `docs/model_definition.md`.
- The **simulation protocol** and its relation to the Generalised
  Detailed Balance (GDB) closure are explained in
  `docs/simulation_protocol.md`.

In particular, the metriplectic closure with both mergers and splits
is an analytical construct; the numerical ensemble in this package
implements the strongly irreversible, forward-merger limit appropriate
to freely decaying turbulence, as discussed in the Letter.

## 4. Navier–Stokes reference and resolution

The file `NS_reference/viscous_dissipation_vs_Re.csv` contains a
$64^2$ pseudo-spectral Navier--Stokes reference, intended as a
laptop-friendly qualitative trend that can be regenerated quickly via

```bash
python NS_reference/generate_viscous_data.py
```

To demonstrate resolution independence, we additionally provide
precomputed high-resolution runs at $256^2$ and $512^2$, stored as

- `NS_reference/viscous_dissipation_vs_Re_highres_256.csv`
- `NS_reference/viscous_dissipation_vs_Re_highres_512.csv`.

The plotting script `src/plot_dissipation_saturation.py` overlays all
available resolutions in a single figure, showing that the viscous
dissipation--Re trend changes by less than order-one percent between
$64^2$ and $512^2$ in the overlapping viscosity range.

## 5. Optional universality diagnostic (+α)

For a compact numerical check of the saturation universality across
$N$ and $r_c$, you can run

```bash
python -m src.check_eps_saturation_universality
```

which prints basic statistics for `eps_tot_mean` and produces the
figure `figures/eps_saturation_universality.png`. In the bundled
ensemble, the saturation level clusters around
$\langle \varepsilon_{\mathrm{tot}} \rangle \approx 0.21$ with only
a few-percent spread across a factor-of-four in particle number and a
factor-of-five in merger radius.
