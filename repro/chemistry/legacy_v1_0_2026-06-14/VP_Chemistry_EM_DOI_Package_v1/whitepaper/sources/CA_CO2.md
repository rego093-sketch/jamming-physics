\newpage

# Application: CO$_2$ Electrocatalytic Reduction — the $d$-band CO-binding descriptor **[F]/[F?]**

*Numbers reproduced by `vp_co2_reduction.py` (deterministic, standard-library, 2× sha256). This
section re-grounds the carbon-dioxide problem on the verified $d$-band energy descriptor, replacing
the refuted electron-amplitude account (in which CO$_2$ "dissociated" when an amplitude exceeded
$\sim 300$ fm $>\sqrt2$). The amplitude figure had no measured basis; the controlling variable is
the $^*$CO adsorption energy, exactly as for the hydrogen and nitrogen volcanoes (Chapter CT, §CA).*

## The mechanism — selectivity is set by $^*$CO binding **[F?]**

Electrochemical CO$_2$ reduction (CO$_2$RR) proceeds through adsorbed intermediates, and its
*product selectivity* is governed by a single descriptor: the binding energy of adsorbed CO,
$\Delta E_{\mathrm{CO}}$ — the same $d$-band quantity that orders hydrogen ($\Delta G_H$, apex Pt)
and nitrogen ($E_N$, apex Fe/Ru). The rate-limiting first electron transfer to $^*$CO$_2^{-}$ /
$^*$COOH / $^*$OCHO is what a catalyst must stabilize; how well it does so tracks
$\Delta E_{\mathrm{CO}}$. The module finds $\Delta E_{\mathrm{CO}}$ correlated with the Hammer–
Nørskov $d$-band centre $\varepsilon_d$ at $r = -0.97$ — confirming the descriptor and reusing the
same engine, not a new one.

## Thermodynamics — equilibria near 0 V, onset far below **[F]**

The multi-electron product potentials (vs RHE) cluster near zero, yet the observed onset is much
more negative ($-0.8$ to $-1.1$ V) because the CO$_2^{\bullet-}$ radical anion lies near $-1.9$ V:

| Product | $n\,(e^-)$ | $E^\circ$ (V vs RHE) |
|---|---|---|
| CO | 2 | $-0.10$ |
| HCOOH (formate) | 2 | $-0.12$ |
| CH$_3$OH | 6 | $+0.03$ |
| C$_2$H$_4$ | 12 | $+0.08$ |
| CH$_4$ | 8 | $+0.17$ |
| (competing) H$_2$ | 2 | $0.00$ |

These equilibria are forced from formation free energies by $E^\circ = -\Delta G^\circ/(nF)$; the
numeric gate independently reproduces $E^\circ(\mathrm{CO}_2\!\to\!\mathrm{CO}) = -0.104$ V and
$E^\circ(\mathrm{CO}_2\!\to\!\mathrm{CH}_4) = +0.169$ V from $\Delta G_f$ data.

## Copper's uniqueness — the falsifiable headline **[F?]**

Sorting metals by $\Delta E_{\mathrm{CO}}$ reproduces Hori's four-group classification:

- **Strong binding** (Pt, Pd, Ni, Rh, Co, Ru): the surface is CO-poisoned and evolves H$_2$.
- **Intermediate binding** ($\Delta E_{\mathrm{CO}} \approx -0.5$ eV): CO stays long enough to be
  reduced further to **hydrocarbons and alcohols** — this is **copper, and copper alone** among
  pure metals.
- **Weak binding** (Au, Ag, Zn): CO desorbs and is the product (CO-selective).
- **$sp$-metals** (Sn, Pb, Bi, In, Cd): bind $^*$OCHO through oxygen and give **formate**.

That copper is the only pure metal producing significant C$_2$+ hydrocarbons is the central,
established experimental fact (Hori), reproduced here as a consequence of intermediate $^*$CO
binding — the CO$_2$RR analogue of "Pt is the HER apex."

## The scaling-relation ceiling **[F?]**

Because $^*$COOH, $^*$CO, and $^*$CHO all bind through carbon, their energies scale together with a
nearly constant offset $\Delta E_{\mathrm{CHO}} \approx \Delta E_{\mathrm{CO}} + 0.74$ eV. The
$^*$CO $\to$ $^*$CHO step is therefore potential-limiting, giving a methane limiting potential on
copper of $U_L \approx -0.74$ V (Peterson–Nørskov). This $0.74$ eV floor cannot be removed by
tuning $\varepsilon_d$ alone — a linear-scaling constraint that is the direct cousin of the OER
$0.37$ V overpotential floor in the water chapter. It is the reason CO$_2$RR is intrinsically
difficult, stated as forced geometry of the scaling lines, not as a fitted loss.

## Grade and falsification

**Forced [F]:** the equilibrium potentials and electron counts. **Candidate-forced [F?]:** the
$\varepsilon_d \leftrightarrow \Delta E_{\mathrm{CO}}$ descriptor, copper's uniqueness, the volcano,
and the scaling ceiling. **Calibration [CAL]:** $\Delta E_{\mathrm{CO}}$, $\varepsilon_d$, the
equilibrium potentials, and the scaling offset. **Open [O]:** absolute current densities and the
full C–C coupling microkinetics. **Falsifier:** copper is the apex for hydrocarbons and CO$_2$RR
selectivity follows the $^*$CO-binding order; if a pure non-copper metal produces more hydrocarbons
at the same overpotential, or the binding order is broken, the $d$-band CO descriptor is refuted.
