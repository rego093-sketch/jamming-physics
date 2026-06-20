# 16-muscle-force-length

**Verifies:** the muscle force–length law is DERIVED from locked filament dimensions
(overlap geometry) and matches the Gordon–Huxley–Julian (1966) MEASURED landmarks —
GHJ is the validation target, never an input (VP-SPEC C1).

**Run:** `python3 run.py`
**Expected output:** `SLUG VERIFICATION: PASS` — gate(vs GHJ) PASS, deterministic
(2×sha256 identical), fidelity 27/27 to `expected/`, and the four `[O]` items declared
(see `IRREPRODUCIBILITY_LEDGER.md`).

**Engine:** `../_engine/vp_muscle_force_law.py` (stdlib+numpy, deterministic).
