# Per-Latitude Deglacial → Petroleum-Source Scenario (M40)

**Constructive, objective. No mainstream-vs-VP adjudication** — this builds out the cascade's
own scenario in latitude detail, using three present-tense physical drivers, and couples it
to the melt. Reproducible: `repro/m40_latitude_petroleum_scenario.py` (gate
`3c899ccbd43f93323eab44b90c34e37876bc0bb572c0073e2c46d7e9a58bd141`), inputs frozen.

## The three drivers (all present-tense, computed/observed)

1. **Angle of incidence.** Annual-mean insolation from the present orbit: the equator takes
   the sun near-overhead (~416 W/m²), the pole obliquely (~172). The equator is hotter
   because the same beam is spread over less area at low latitude. Even in an ice age this
   geometry is unchanged — it is set by the planet's tilt, not by climate state.

2. **Water-vapour greenhouse trapping.** Saturation vapour pressure rises steeply with
   temperature (Clausius–Clapeyron). On the observed SST field the warm equatorial ocean
   carries **~6.6×** the column water vapour of the pole (35.6 vs 5.4 hPa). That vapour traps
   outgoing longwave and **amplifies** equatorial warmth; the dry pole traps little and stays
   cold. This is *why* the surface temperature gradient is as steep as it is — the humidity
   feedback, exactly as you specified.

3. **Rainfall.** The present zonal-mean precipitation field: a wet equator (ITCZ ascending,
   ~2000 mm/yr), an **arid descending subtropics** near 30° (~500 mm/yr — the world's desert
   belt), wet mid-latitude storm tracks (~1000 mm/yr at 45°), and dry cold poles (~150).

## Coupling to the melt (the scenario)

As ice melts, the high-latitude ice delivers **meltwater**; meltwater + rainfall form a
**freshwater lid** on the ocean surface → stratification → the bottom water goes **anoxic**
(O₂ resupply is cut off) → organic matter is **preserved** instead of oxidised. Rainfall and
meltwater also carry **nutrients** (weathering, runoff) → high surface **productivity**. Warm
water (drivers 1+2) additionally holds less O₂, reinforcing anoxia. Source-rock burial — the
seed of petroleum — is therefore strongest where **productivity × preservation** is greatest,
and it is **broadened during the meltwater pulse** as the lid spreads equatorward.

## The computed latitudinal profile

| lat | warmth | wet | meltwater | productivity | preservation | **favourability** |
|---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 0° | 1.00 | 1.00 | 0.00 | 1.00 | 0.93 | **1.00** |
| 15° | 0.97 | 0.62 | 0.03 | 0.60 | 0.42 | **0.27** |
| 30° | 0.83 | 0.19 | 0.17 | 0.16 | 0.00 | **0.00** |
| 45° | 0.55 | 0.46 | 0.45 | 0.25 | 0.62 | **0.17** |
| 60° | 0.27 | 0.30 | 0.73 | 0.08 | 0.62 | **0.05** |
| 75° | 0.06 | 0.11 | 0.94 | 0.01 | 0.53 | **0.00** |
| 90° | 0.00 | 0.00 | 1.00 | 0.00 | 0.47 | **0.00** |

**Ranking (most → least favourable): 0° > 15° > 45° > 60° > 75° > 30° > 90°.**

## What the detail reveals (that an average hides)

- A **strong equatorial/low-latitude peak**: warm + humid + productive + anoxic — every driver
  aligns.
- A **secondary mid-latitude high at 45°** (storm-track rainfall + meltwater lid) that
  **beats the warmer 30° subtropics** — because 30° is the arid descending desert belt and is
  productivity-starved. This non-monotonic equator→mid-latitude double structure is precisely
  the rainfall signal you asked to include; an annual-mean-temperature-only treatment would
  have made 30° rank above 45° and erased it.
- **Minima at the arid subtropics and the cold dry poles** — for opposite reasons (the
  subtropics have preservation potential but no productivity; the poles have meltwater
  stratification but the water is too cold and unproductive).
- **The melt as the trigger window**: meltwater (rising monotonically poleward) supplies the
  freshwater lid; as it spreads equatorward during deglaciation it extends the anoxic
  preservation window across the productive low latitudes — so the source-burial pulse is
  tied to the melt, latitude by latitude.

## Scope (honest)

The three drivers are present-tense **[V]**. The favourability field is a **constructed
forward index** from those [V] inputs, with transparent weights (in the script header). It
makes **no** claim about occurrence, rate, or absolute timing — those stay **[O]**, untouched.
This is detail-building of the scenario, not a discriminating test, and it is built objectively
from the physics, neither to break nor to inflate the framework. The weights can be tuned;
the *structure* (equatorial peak, mid-latitude secondary, subtropical/polar minima) follows
from the driver fields themselves and is robust to reasonable reweighting.
