# Applications: Catalysis, Fertilizer, Water, Energy, and Materials

**VP Chemistry & Electromagnetism Whitepaper — Chapter CA**
DOI (reserved): 10.5281/zenodo.20680541 · Companion to Chapters CH (chemistry), CM (metals),
CT (catalysis), EM (electromagnetism).
Status grades: **[F]** forced (zero free parameters) · **[F?]** forced-candidate · **[CAL]**
calibration input (measured constant) · **[V]** simulation-measured · **[H]** hypothesis · **[O]**
open / refuted. Every numeric claim is reproduced by a deterministic, standard-library module
(2× sha256 identical); module and case-ledger anchors are given inline.

> This chapter carries the metals account (CM/CT) into five practical domains: **catalysts,
> fertilizer, water purification, energy storage, and new materials**. Its method is the one that
> already succeeded for platinum (Chapter CT): where a speculative *amplitude/geometry* mechanism
> was proposed, it is tested; what does not survive is reported as refuted and **re-grounded on
> validated physics**; what does survive is kept and labelled. The result is a single thread — the
> **d-band energy resonance** — running through catalysis, fertilizer, and water electrolysis, with
> honest negative verdicts for two device claims that do not hold.


## CA.0 The central method: re-grounding, not decoration

The prior application materials built catalysis, desalination, and an energy device on an *electron
amplitude* variable (fm-scale). Chapter CT showed by direct simulation that this variable is the
wrong one: the geometric/amplitude resonance is a Bragg band edge (refuted), and platinum is
reproduced only by the **energy** resonance — the d-band center ($\varepsilon_d$) coupling to the
adsorbate level (Newns–Anderson / Hammer–Nørskov). This chapter applies that verdict everywhere:
each application is rebuilt on the validated mechanism, and any device claim whose mechanism fails
testing is reported as **refuted** or **[H]** with a working alternative supplied. Honesty about the
two negative results (magnetic desalination; the ESS "amplitude → electricity" generator) is not a
footnote — it is the chapter's spine.


## CA.1 The d-band engine — one variable for three reactions **[V]/[F?]**

Module `vp_dband_catalysis.py` generalises the platinum result into a reusable engine. A sharp
adsorbate level broadens on coupling to the metal d-band (Newns–Anderson) **[V]**; the d-band center
$\varepsilon_d$ then *predicts* binding. For hydrogen the correlation with measured adsorption is
$$ r(\varepsilon_d,\ \Delta G_H) = -0.915 \quad\text{(strong, non-circular)} \;[\mathbf{F?}], $$
and the Sabatier volcano (activity peaked at $\Delta G_H\approx 0$) reproduces the **Pt apex**. The
*same engine* applied to nitrogen adsorption gives a different optimum and the **Fe/Ru apex** of the
ammonia volcano. Crucially, the real tuning lever is the **energy**, not the lattice spacing: shifting
$\varepsilon_d$ by alloying or strain moves a metal along the volcano (`vp_dband_catalysis.py` §4).
This *replaces* the refuted geometric resonance with a design rule that is actually used for
electrodes. **Falsifiable:** HER apex at $\Delta G_H\approx0$ (Pt), ammonia apex at $E_N\approx-0.5$
eV (Fe/Ru); break either ordering and the d-band picture is discarded.


## CA.2 Fertilizer — ammonia synthesis **[F]/[F?]**

Nitrogen fixation $\mathrm{N_2 + 3H_2 \rightleftharpoons 2NH_3}$ underpins half the human food
supply. Module `vp_ammonia_synthesis.py` closes it with the two VP pillars — equilibrium (CH.8) and
the d-band catalyst engine (CA.1).

**Equilibrium forces the conditions [F].** With $\Delta H^\circ=-91.8$ kJ/mol (exothermic) and
$\Delta S^\circ=-198.1$ J/mol·K (gas moles $4\to2$), $\Delta G^\circ=\Delta H-T\Delta S$ gives the
crossover $T^{*} = \Delta H/\Delta S = 463$ K, where $K=1.000$. Below it the reaction is favoured but
$\mathrm{N_2}$ is kinetically inert; above it the equilibrium yield collapses. The module solves the
stoichiometric equilibrium and reproduces the **Le Chatelier compromise** quantitatively — e.g.
equilibrium $\mathrm{NH_3}$ rises with pressure ($\Delta n=-2$) and falls with temperature:

| condition | 1 atm | 100 atm | 200 atm | 400 atm |
|---|---|---|---|---|
| 500 K | 10.8% | 76.3% | 82.6% | 87.3% |
| 700 K | 0.6% | 29.1% | 40.7% | 52.4% |

This is exactly why industry runs ≈450 °C / 150–300 atm / Fe catalyst — a forced three-way
compromise, not a tuned choice.

**Catalysis selects the metal [F?].** The rate-limiting step is dissociation of $\mathrm{N\equiv N}$
(945 kJ/mol, among the strongest bonds; the bond-energy sum reproduces $\Delta H\approx-93$ kJ/mol,
sign and magnitude correct). The catalyst volcano in the nitrogen-binding descriptor peaks at
**Fe/Ru/Os** — the industrial Haber–Bosch catalysts — with Mo/W too strong (N trapped) and Ni/Pt too
weak (no dissociation). The volcano comes from the d-band energy of CA.1, one thread with catalysis
and water-splitting. Absolute rates, promoter ($\mathrm{K_2O}$/$\mathrm{Al_2O_3}$) effects, and
surface microkinetics remain **[O]**.


## CA.3 Water purification I — electrolysis electrodes **[F]/[F?]**

Module `vp_water_electrolysis.py` carries the d-band engine to clean hydrogen and electrochemical
water treatment. Water splitting $\mathrm{2H_2O\to2H_2+O_2}$ has a reversible minimum
$E^\circ_{\text{cell}}=1.229$ V ($\Delta G=237$ kJ/mol H$_2$) and a thermoneutral voltage
$V_{tn}=\Delta H/(nF)=1.481$ V; the difference $T\Delta S=48.6$ kJ/mol is supplied as heat **[F]**.
The real cell voltage decomposes as $V_{\text{cell}}=1.23+\eta_{\text{HER}}+\eta_{\text{OER}}+iR$,
and the single largest loss is the **anode (OER)**. The HER volcano (CA.1) places the cathode near
solved (Pt apex). The OER is bounded by a *fundamental* limit: the universal scaling relation
$\Delta G_{*\mathrm{OOH}}-\Delta G_{*\mathrm{OH}}\approx 3.2$ eV ties the intermediates, so the two
middle steps cannot both be 1.23 eV and the best achievable overpotential is
$$ \eta_{\text{OER}}^{\min} = 1.6 - 1.23 = 0.37\ \text{V} \quad[\mathbf{F?}], $$
with the apex at **RuO₂/IrO₂** (the industrial OER catalysts). This 0.37 V is *why water-splitting is
permanently expensive* on single-site catalysts — beating it requires breaking the scaling relation
(bifunctional / 3D sites), an honest **[O]**. Faraday's law gives 18.66 mmol H$_2$ per A·h **[F]** and
a thermoneutral voltage efficiency $V_{tn}/V_{\text{cell}}\approx 81\%$. Electrocoagulation,
electrodialysis, and capacitive deionization (CDI) extend the same electrode science to treatment and
desalination — all charge/membrane/potential based, **[F?]/[CAL]**.


## CA.4 Water purification II — magnetic desalination: an honest verdict **[F] · [O]/refuted**

The prior materials proposed separating $\mathrm{H_2O}$ from $\mathrm{Na^+/Cl^-}$ at 0.45 T by an
*amplitude* difference. Module `vp_magnet_desalination.py` replaces the prose with the actual
magnetic force. Water is weakly diamagnetic ($\chi_v\approx-9.05\times10^{-6}$); its magnetic energy
in a 0.45 T field is
$$ \frac{U_{\text{mag}}}{k_BT} \approx 5.3\times10^{-9} \quad[\mathbf{F}], $$
nine orders of magnitude below thermal energy — thermal motion overwhelms any magnetic ordering, so
**no separation occurs**. To reach $U_{\text{mag}}\approx k_BT$ would need $B\approx 6173$ T,
physically impossible for a purifier (cf. ~45 T continuous, ~1200 T pulsed-destructive). The Lorentz
force on flowing ions is real but $\sim10^{-2}\,k_BT$ across a channel: a field can stir (MHD) but
cannot *desalinate by amplitude*. **Verdict: the amplitude-separation device is refuted [O].** The
working alternatives are supplied with real numbers: reverse osmosis (seawater osmotic pressure
$\pi=i\,cRT\approx 30$ bar, matching the measured ~27 bar; thermodynamic minimum $\approx0.83$
kWh/m³), electrodialysis, and CDI. This is the platinum pattern again — refute the wrong mechanism,
keep the validated one.


## CA.5 Energy storage — black-copper solar ESS, split honestly **[F]/[F?] · [H]→alt**

Module `vp_ess_thermal.py` separates the device into a **real storage part** and a **hypothetical
generation part**.

**Storage is real and quantified.** A black-copper absorber ($\alpha\ge0.98$) at 800 W/m² collects
~4.7 kWh/day per m². High-heat-capacity media (alumina/sand) store it; the heat capacity is the
Dulong–Petit $3R$ per atom of Chapter CH.7 ($c_p\approx1223$ J/kg·K at the high-T limit; measured
880 J/kg·K at room temperature), so a 1 m³ store holds **~46 kWh** of heat over a 118 K rise **[F?]**.
Vacuum insulation gives a thermal time constant $\tau=mc/(UA)\approx 5.4$ days **[F?]** — ample for
overnight delivery.

**Generation is hypothesis, with a working alternative.** The claimed "rotation-amplitude →
electric field" generator has no validated mechanism and is marked **[H]**. Heat-to-electricity is
bounded by Carnot, $\eta=1-T_c/T_h=28.2\%$ at the storage temperature; realistic conversion uses a
thermoelectric (Seebeck, $ZT=1$ → ~5.5%, ~2.5 kWh) or a Stirling engine (~½ Carnot → ~14%, ~6.5 kWh)
**[F]**. The honest split — real thermodynamic storage, unproven generator replaced by a heat engine
— is the same discipline as CA.4.


## CA.6 New materials — black copper and d-band design **[F]/[F?]**

Module `vp_new_materials.py` explains the black-copper absorber by *optics*, not amplitude, and ties
materials design to the d-band. Polished copper reflects ($R\approx0.97$, absorptance $\alpha=0.03$)
because of its free-electron plasma (Chapter CM); nanostructured/oxidised copper raises $\alpha$ to
~0.96 (a ~32× gain) by graded-index impedance matching, light-trapping, and intrinsic CuO absorption
**[F?]** — the same electromagnetic physics as the copper plasma/skin effect, not an fm-scale
amplitude. A **selective absorber** then needs *low* infrared emittance: the Stefan–Boltzmann
re-radiation $P=\varepsilon\sigma A(T^4-T_{\text{amb}}^4)$ at the storage temperature is +704 W net
for $\varepsilon=0.05$ but **−377 W for a blackbody surface** ($\varepsilon=0.90$) — the latter
*cannot even heat up* **[F]**. Thus low IR emittance is essential, a concrete falsifiable design
rule. Beyond coatings, the d-band of CA.1 is the materials lever (alloying/strain tunes catalytic,
electronic, and magnetic properties — the CM/CT trilogy), and crystal packing fractions remain pure
geometry (FCC/HCP $\pi/(3\sqrt2)=0.7405$, **[F]**, CH.13).


## CA.7 Master ledger — applications

**[F] forced (zero free parameters):** ammonia $T^{*}=\Delta H/\Delta S$, Le Chatelier directions,
bond-energy $\Delta H$ sign; water-splitting $1.23$/$1.48$ V and Faraday $18.66$ mmol/A·h; magnetic
energy $\ll k_BT$ and the infeasible $B$; seawater osmotic pressure and desalination minimum energy;
Dulong–Petit storage, thermal time constant, Carnot/Seebeck/Stirling efficiencies; Stefan–Boltzmann
selective-absorber balance; crystal packing fractions.

**[F?] forced-candidate:** $\varepsilon_d\leftrightarrow$ binding correlations and volcano apexes
(HER→Pt, NH₃→Fe/Ru, OER→RuO₂/IrO₂); d-band strain/alloy tuning; OER scaling-relation limit 0.37 V;
absorber enhancement and selectivity.

**[V] simulation-measured:** Newns–Anderson adsorbate-DOS broadening; volcano reconstructions.

**[CAL] calibration inputs:** $\varepsilon_d$, $\Delta G_H$, $E_N$, OER descriptors,
$\Delta H/\Delta S$, bond energies, $E^\circ$, susceptibility, emittance, insolation.

**[H] hypothesis → alternative:** the ESS "amplitude → electricity" generator (replaced by a heat
engine).

**[O] open / refuted:** magnetic amplitude-desalination (refuted); absolute reaction rates and
microkinetics; promoter effects; scaling-relation circumvention.


## CA.8 Falsification criteria **[F]**

- If the HER apex is not Pt ($\Delta G_H\approx0$) or the ammonia apex is not Fe/Ru
  ($E_N\approx-0.5$ eV), the d-band volcano account is discarded.
- If exothermic ammonia equilibrium does not fall with temperature and rise with pressure, the
  equilibrium account is discarded.
- If a single-site OER catalyst stably shows $\eta<0.3$ V, the scaling-relation limit needs revision.
- If a 0.45 T field measurably desalinates seawater, the magnetic-energy analysis is wrong (it is
  not: $U_{\text{mag}}/k_BT\sim10^{-9}$).
- If a non-selective (high-$\varepsilon$) black absorber maintains the storage temperature under the
  stated flux, the radiative-balance rule is wrong.


## CA.9 Reproducibility

Six deterministic, standard-library modules and three case ledgers (29 rows) reproduce this chapter;
`verify_applications.py` checks execution, determinism (2× sha256), standard-library-only dependency,
and ledger integrity in one pass (**6/6 PASS, 29 rows**).

```
python3 verify_applications.py        # all modules + ledgers
python3 vp_dband_catalysis.py         # HER→Pt, NH3→Fe/Ru, d-band tuning lever
python3 vp_ammonia_synthesis.py       # Haber compromise, T*, catalyst volcano
python3 vp_water_electrolysis.py      # 1.23/1.48 V, OER 0.37 V limit, Faraday
python3 vp_magnet_desalination.py     # magnetic separation refuted; RO/ED/CDI
python3 vp_ess_thermal.py             # thermal storage (CH.7); generation [H] + heat engine
python3 vp_new_materials.py           # black-copper optics; selective absorber; packing
```


*The five applications close on one idea carried from the metals trilogy: the **d-electron energy**
(not a lattice geometry, not an amplitude) governs catalysis, and the same energy thread reaches
fertilizer and water-splitting; thermodynamics governs equilibrium and storage; optics governs the
absorber. Where a device mechanism could not be validated it is refuted or marked hypothesis and a
working alternative is supplied. What is forced is falsifiable, what is measured is labelled, what is
open is admitted — and all of it is reproducible.*
