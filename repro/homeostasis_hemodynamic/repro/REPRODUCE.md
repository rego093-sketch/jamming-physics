# REPRODUCE

```
python repro/run_all.py                 # research entry: nodes, sensory layer, RP1-RP5 loops, interaction
                                        #   map, stress battery (26/26), pathology, therapy, comfort-logic, gate
python inherited/measure_gamma.py       # offline master-gene gamma: validates SIX2 (1.5556/0.6381 exact)
                                        #   then measures REN (1.3634) on the identical NN pipeline, from cache
python repro/_engine/vp_hmd_engine.py   # full circulate() JSON (+ sha256) -- one hash over everything
python repro/_engine/vp_hmd_loops.py    # RP1-RP5 closed-loop discriminants
python repro/_sensory/baroreceptor.py   # PIEZO1/2 baroreceptor transduction (+ shared-R19 spikes)
python repro/_sensory/macula_densa.py   # NKCC2 NaCl chemosensor (TGF + inverse renin; SGLT2i)
python repro/_therapy/fundamental_targets.py  # fundamental vs symptomatic therapy (hypertension, HF)
python repro/_pathology/hypotension_family.py  # hypotension node decomposition (RP6-RP9 + cardiogenic + T3)
python repro/_comparative/setpoint_emergence.py # universality: defended setpoint emergence by loop accretion (C1)
python repro/_pathology/setpoint_failure.py   # derived reset law + saddle-node collapse law
python repro/_intervention/intervention_logic.py    # comfort map: 3-lever technique on the defended setpoint (H1/H2/H3)
python repro/_intervention/burden_prioritisation.py # declared-weight target-AXIS ranking (never agents)
python repro/_intervention/counterreg_honesty.py    # per-axis mechanism [O] / lever placement [V] honesty gate
python repro/_intervention/falsification.py         # a named falsifier per HP1-HP7 + framework
python repro/_intervention/forbidden_claim_scan.py  # fail-closed firewall (no dosing/efficacy/safety-as-fact)
python repro/_verify/stress_tests.py    # the 26-suite battery (RP1-RP5, S1-S2, T1-T2, RP6-RP9, C1, CAL1-CAL7, IV1-IV5)
python repro/_verify/gates.py           # research gate (all_green) + writing-lock status
```

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed (SEED=19); round-before-hash;
sorted JSON keys. Two `circulate()` runs yield an identical sha256 covering the nodes, sensory layer, loops,
interaction map, therapy read, and the comfort-logic intervention layer (folded docs-independent). No
hand-entered numbers. stdlib + numpy only. Current research hash: `08a11846d481a849...`.

The comfort-logic layer (`repro/_intervention/`, v0.7.0) ports the three-lever intervention technique from
the non-opioid analgesic whitepaper (concept DOI `10.5281/zenodo.20733420`): it READS the proven RP4/T1/T2
loop directions and PLACES each axis on a lever (H1 reset-reference / H2 restore-buffer / H3 unload-effector
paired-only). The forbidden-claim firewall runs inside the battery (IV2, `scan_docs=False`) and again over
the built docs at write time (`scan_docs=True`); any dosing / efficacy / safety-as-fact phrasing fails the
build closed. The layer states a STRUCTURAL prediction only -- no molecule, regimen, efficacy, tolerability,
or safety result (`[O]`).

Writing stays LOCKED until `gates.research_gate()["all_green"]` is true AND `reports/research_complete.json`
is present AND `PHASE` is set to `writing`. Research is signed off (all_green=true), `PHASE=writing`, and the
canonical SEO HTML is published under `docs/` (rebuild is idempotent: `python tools/build_docs.py`).
