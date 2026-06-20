# REPRODUCE

```
python repro/run_all.py               # research entry: emerge, circulate, stress + oncology, gate report
python repro/_engine/vp_*_engine.py   # emergence JSON (+ sha256)
python repro/_verify/gates.py         # research gate + writing-lock status
```

Determinism (VP-SPEC C1): BLAS pinned single-thread before numpy; fixed seed; round-before-hash; sorted
JSON keys. Two engine runs yield an identical sha256. No hand-entered numbers. stdlib + numpy only.
