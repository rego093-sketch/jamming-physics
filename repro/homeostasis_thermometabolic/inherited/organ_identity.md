# Node identity (CITED from DNA morphogenesis / energy gene-clock)

The DNA package already EMERGES organ/node identity and developmental order from measured master-gene
γ, grade **[V]** (visceral organ atlas + morphogenesis atlas + the energy/thermogenesis obesity atlas).
This package CITES that result; it does **not** re-derive node existence. γ values are MEASURED
(NN-stacking ΔG37, SantaLucia 1998), read-only, never fitted. Masters marked **TO-MEASURE** are named
but not yet in the atlas — an honest research input to fetch via the DNA `fetch_morpho_gamma` pipeline
(cross-species where comparative, e.g. the torpor/hibernation program) — not a fabricated number.

| master gene | node | measured γ | role (this package) |
|---|---|---|---|
| UCP1 | brown_adipose_thermogenesis | 1.4054 | uncoupled proton leak = heat, not ATP (the endotherm furnace) |
| ADRB3 | sympathetic_thermo_drive | 1.4462 | beta3-adrenergic activation of BAT (cold -> heat command) |
| PPARG | white_adipose_storage | 1.3902 | lipid storage + adipokine secretion (the lipostat storage node) |
| MC4R | melanocortin_appetite | 1.272 | hypothalamic energy-balance setpoint (intake control) |
| LEPR | leptin_feedback | 1.4554 | adiposity feedback signal (storage -> brain) |
| INSR | insulin_glucose_effector | 1.4956 | insulin-mediated glucose disposal (the euglycemia effector) |
| GHRL | ghrelin_hunger | 1.355 | gut hunger signal (drives intake; opposes leptin) |
| PDK4 | torpor_fuel_switch | 1.4112 | metabolic fuel-switch to lipid + glucose sparing (torpor-associated program) |
| (hypothalamic_thermostat) | preoptic_thermostat | —(diffuse) | preoptic setpoint comparator (the thermostat itself; circuit, no single master) |
| (torpor_arousal_cycle) | torpor_arousal_rhythm | —(diffuse) | periodic interbout arousal during hibernation (slow relaxation oscillator) |

> SSOT: identity + order live in DNA. γ changes there and propagates here by re-vendoring. To-measure
> entries are fetched, then vendored.
>
> **Update (v0.3.0):** PDK4 (torpor fuel-switch) promoted TO-MEASURE → **measured γ=1.4112** (NC_000007.14,
> TSS−2000..+500) via the identical DNA `fetch_morpho_gamma` pipeline (NN-stacking ΔG37, SantaLucia 1998).
> A 7-species furnace/torpor panel (UCP1/ADRB3/PDK4 across human, mouse, rat, pig, ground squirrel,
> zebrafish, frog) is vendored in `crossspecies_thermo_panel.json` and re-derives offline bit-for-bit. No
> named master remains unmeasured; the two diffuse nodes are circuits with no single master gene.

> **Update (v0.4.0):** the vendored `crossspecies_thermo_panel.json` is EXTENDED (never mutated) to an
> 8-gene × 14-species torpor/BAT panel — 107 measured cells. Genes added: PPARGC1A, DIO2, CIDEA, FGF21,
> SLC2A4/GLUT4 (joining UCP1/ADRB3/PDK4). Species added: Urocitellus parryii, Marmota marmota,
> Mesocricetus auratus, Microcebus murinus (a torpor-capable primate), Ursus americanus, Cavia porcellus
> (GC-matched rodent control), Oryctolagus cuniculus. The original 19 cache entries and all original read
> γ values stay byte-identical. Pre-registered NULL (RH8): across the 8-gene program, 0 genes' promoter γ
> separate hibernators from non-hibernators; every group γ gap IS a GC gap (cross-gene r(Δγ,ΔGC)=0.9957) —
> hibernation is regulatory gating of present genes, not a γ threshold (the firewall, at panel scale).
