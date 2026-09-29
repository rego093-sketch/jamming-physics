# ESS2: black copper inside a cavity in the hot sand

The absorber's front face also looks into the hot store. Light comes in through an aperture of area A_coll/CR, and the aperture is shut at night. The predictions were registered after ESS1 and before this run.

| Prediction | Result |
|---|---|
| P1: for CR ≥ 50 the store keeps accumulating (+50 K by day 30) | **FAIL**: +17 to +18 K. The store has approached its equilibrium. |
| P2: every CR ≥ 10 stores more than ESS1's best case (8.6 kWh) | PASS (15.5–18.4 kWh) |
| P3: the store's insulation, not the absorber, becomes the limit | PASS (aperture loss 0.9–3.4 kWh vs insulation loss 82–84 kWh) |
| P4: CR = 1 does not rescue the store | PASS |

**Reading**

- **The author's hypothesis holds on the absorber side.** When the whole interior is hot, heat no longer leaves through the absorber. Absorber-side loss falls from 68 kWh to 0.9 kWh, and the effective cavity absorptance is 0.998.
- **The limit moves to the store.** Energy balance gives the equilibrium rise ΔT_eq = η·α·Ḡ·A_coll / UA:
  - with 1 m² of collector on a 1 m³ store and τ = 5.4 days, this is 144 W / 3.0 W/K ≈ 48 K, and the simulation gives 47 K [F];
  - a 500 °C store needs about 10 m² of collector per m³ of sand, or proportionally better insulation.

  This is a sizing ratio, not a physical barrier.
- **What still stands.** Black copper remains an absorber, not a converter. Electricity needs a separate engine, whose Carnot limit rises with the store temperature.

**Grades.** Absorber-side loss suppression and the store limit are [V mech] in this lumped model. The equilibrium formula is [F]. Real hardware is data-pending.

Run: `python3 ess2_run.py` (about 1 s, deterministic).
