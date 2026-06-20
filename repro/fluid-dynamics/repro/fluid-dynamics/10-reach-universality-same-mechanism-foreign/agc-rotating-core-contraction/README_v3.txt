AGC_DOI_v3 supplementary data note
----------------------------------

This v3 archive extends the previous AGC_DOI_v2 repository with two types of additional data:

1. Simple grid-convergence check for a rotating rigid cylinder in an ideal-gas Euler model
   (data/sensitivity/grid_convergence_water_M1p5_alpha1.csv, figures_v3/fig_gridconv_*.png).

   - Model: 2D compressible Euler equations, ideal gas (gamma = 1.4).
   - Numerical method: finite-volume scheme with a Rusanov (local Lax–Friedrichs) flux.
   - Setup: Mach number M_inf = 1.5, spin parameter alpha = 1.0, rigid cylinder of radius R = 1.
   - Grids: N = 50, 100, 200 uniform cells in each direction on a 20R x 20R domain.
   - Quantities reported: bow-shock standoff distance x_s/R, surface-averaged pressure p_bar,
     and maximum surface pressure p_max, as functions of grid resolution.

   These results are intended as a simple numerical sanity check and do not replace
   the main water/Tait-EOS simulations discussed in the manuscript.

2. Quasi-static 0D toy model for geometric contraction under shock-induced loading
   (data/toy_model/toy_contraction_R_vs_M.csv,
    data/toy_model/toy_contraction_R_vs_density_ratio.csv,
    figures_v3/fig_toy_contraction_*.png).

   - The toy model treats the core as a compressible rotating region with an internal pressure law
     p_int(R) = p0 (R0/R)^(2 gamma_core) and a centrifugal stress scale sigma_cent that competes with
     an external shock pressure P_shock(M_rot).
   - The equilibrium radius R_eq is defined by p_int(R_eq) + sigma_cent = P_shock, and we tabulate
     the non-dimensional ratio R_eq/R0 as functions of rotational Mach number M_rot and density ratio
     rho_inf / rho_core.

   These toy-model data are meant to illustrate the geometric-contraction tendency implied by the
   shock-induced negative centrifugal loading, rather than to provide a full fluid–structure interaction
   simulation.

Please refer to the revised manuscript and supplementary material for the precise definitions and
context in which these auxiliary datasets are used.
