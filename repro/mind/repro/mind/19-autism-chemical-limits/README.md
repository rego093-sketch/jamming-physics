# Chapter 19 — Chemical reach: mask vs correction

**Status (v1.32):** in-silico mechanism on the READ-ONLY engine cerebrum. **efficacy = 0 ·
NOT medical advice · no drug-treats-autism claim.**

## Claim verified
A scalar threshold-lowering (gain) operator — the mechanism by which the catecholaminergic
**stimulant** class raises excitability — acts **axis-specifically**:
- **T fault**: fully reversed (R back to health).
- **O fault**: partially helped (0.354 → 0.357).
- **W fault**: **not corrected**. Brute gain leaves the locality imbalance exactly invariant
  (0.842, mask) and reaches health only by pushing the network into over-synchronisation
  (κ×2.0). A selective tri-lever scheme buys a **safety margin** (off-target push 0.083 vs
  0.25), not new efficacy.

This is the engine's account of why a stimulant relieves some presentations and not others.

## Reproduce
```
cd ../_verify && python3 run_all_d9.py
```
Chemical reach = D9.3 `autism_multilever_threshold.py` and D9.4 `autism_candidate_limits.py`
(θ-supply window inj[0.08,0.10], R 0.393266; over-sync @ 0.15). Exit shows all D9 PASS,
engine byte-unchanged.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
