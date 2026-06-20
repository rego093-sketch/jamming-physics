# REPRODUCE

```
python repro/run_all.py               # research entry: emerge, circulate, stress [3] + disease battery [3b] + oncology [4], gate [5]
python repro/_engine/vp_msk_engine.py # emergence JSON (+ sha256)
python repro/_verify/stress_tests.py  # physiology suite (T1-T5) + disease battery (T6-T10, master-dosage) suites
python repro/_disease/vp_msk_disease.py  # disease engine alone (18 targets, run_disease_battery)
python repro/_oncology/carcinogen_dose_response.py  # 4-site carcinogen dose-response
python repro/_verify/gates.py         # research gate (physiology + disease + oncology) + writing-lock status
python tools/build_docs.py            # WRITING: emit docs/ HTML (refuses while writing is locked)
```

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; round-before-hash; sorted
JSON keys. Two engine runs yield an identical sha256. No hand-entered numbers. stdlib + numpy only.

Disease battery: cited-severity PERTURBATIONS of the passing physiology/master switches; PASS = reproduce the
DIRECTION/SHAPE of the documented clinical sign, never an absolute number (No-Tuning). The research gate requires
the disease battery green in addition to physiology + oncology before writing unlocks.
