# BC1 — Why black copper is black, and where its electrons go

Pre-registered in `PREREG.json` (committed before the run). The run is `python3 bc1_run.py`, which is deterministic (SEED = 19, about 12 s) and writes `RESULT.json`.

**Hypothesis under test (author's):** the black colour guides electrons in one direction, and heating the black layer should show this.

**Correction found before the run:** the black layer is **CuO**, a p-type semiconductor with a gap of about 1.35 eV. It is not copper metal. The earlier module `07-low-grade-waste-heat-electricity/vp_blackcu_absorber_not_generator.py` rejected conversion using the Seebeck coefficient of copper *metal* (1.8 µV/K). That argument does not apply to CuO. The literature Seebeck value for CuO is still to be checked, so it is flagged here and not used.

## Results

| # | Prediction | Result | Reading |
|---|---|---|---|
| P1 | Cu metal reflects, redder than blue; CuO absorbs >90 % of visible light | **PASS** | Cu: R̄ = 0.87, R(1.8 eV) = 0.98 > R(2.8 eV) = 0.76, so the colour is copper-red. CuO film: Ā = 0.99. |
| P2 | With no field, the electron flux is not directed (\|net\| < 0.02) | **FAIL** | 74 % of electrons return to the **lit face** because light is absorbed within 100 nm of it. Holes do exactly the same. The **charge** current is −0.0014 per photon, which is zero within noise. |
| P3 | More than 90 % of the absorbed energy ends as heat | **PASS** | 99.9 %. The excess energy above the gap is lost in about 0.3 ps, and the pairs then recombine. |
| P4 | A junction field directs the carriers | **PASS** | With 1e5 V/m, electrons and holes separate. The charge current is 0.19 per photon, about 140× the no-field case. |
| P5 | A temperature gradient (400 → 300 K across 1 µm) directs the carriers | **FAIL** | The gradient-induced flux is −0.012 and −0.0045 for the two gradient directions. Both have the same sign and sit at the noise level (≈ 0.007). The charge current is about 0. |

## What it means

1. **Why black.** Copper metal is not black. Its free-electron plasma reflects light, and interband absorption starting at 2.1 eV takes out the blue, which gives the red colour. Black copper is black because of its **CuO layer**. The gap of about 1.35 eV lies below every visible photon, so all visible light is absorbed within about 100 nm. The nanostructure removes the remaining surface reflection. This is the same rule as chemistry CC.7.
2. **Where the electrons go.** Absorbing light creates an electron **and** a hole at the same place. In a centrosymmetric absorber with no built-in field, both diffuse the same way: back toward the lit face, where they were created. That motion is directional, but it carries no **net charge**, so it produces no electricity. Heating does not change this: in the model, a 100 K gradient over 1 µm moves nothing beyond noise. Blackness decides *where* the energy is deposited, not *which way the charge flows*.
3. **What would make it one-way.** Something must break the symmetry between electrons and holes. Candidates are a junction (CuO/ZnO, Cu₂O/CuO, a Schottky contact to Cu), unequal electron and hole transport (a real p-type Seebeck effect, which is not modelled here because both carriers were given the same D), or a non-centrosymmetric crystal (bulk photovoltaic effect). CuO/Cu₂O on Cu already has an oxide/metal interface. Whether that interface gives a usable field is **data-pending [O]**.
4. **The light link (Kirchhoff).** A black surface is also the best thermal emitter (ε = α). When the store is hot, "light emergence" does happen, but it is thermal emission. Turning it into electricity needs a TPV cell, meaning a separate junction. See the ESS3 proposal.

These are model results with declared parameters, graded [V mech]. They are not measurements on real black copper.
