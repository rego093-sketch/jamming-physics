# Chapter 23 — Population picture (virtual trial)

**Status (v1.32):** in-silico mechanism on the READ-ONLY engine cerebrum. **efficacy = 0 ·
NOT medical advice.** Every "fraction" below is an in-silico coupling state, **not** a clinical
response rate.

## Claims verified (VC5)
A heterogeneous synthetic population (N = 80, 76 affected) of emerged cerebra, each with a
sampled fault mix (wiring/gain/threshold) and stiffness dispersion, bit-faithful to the D9
endpoints (w=0 → R_health, w=1 → R_W):
- **P-VC5a.** Stimulant-responder fraction falls monotonically across rising-wiring strata
  (0.76 → 0.42 → 0.00) and correlates negatively with wiring share (r = −0.60). Gain fixes gain.
- **P-VC5b.** Adverse (over-sync) fraction rises with cap amplitude (0.14 → 0.57 → 0.99 → 1.0
  → 1.0) and is **minimised at the window** — over-sync is an amplitude phenomenon.
- **P-VC5c (core).** Non-responders are wiring-dominated (w-share 0.42 > responders 0.21);
  the cap rescues **32%** by pacing the missing routing (removable, per VC2 — not repair).
- **FINDING-VC5c (refutation → discovery).** The cap-unrescued **residual** is NOT the
  severe-W tail (cap-rescued w-share 0.45 > residual 0.40); it is a **dose-cap / stiffness
  limit** plus a few high-w cases the fixed window amplitude over-synced — arguing for
  amplitude **matched to the deficit**, not held fixed.

## Reproduce
```
cd ../_verify && python3 run_all_vc.py
```
VC5 `527ee1df…`. See `_verify/vc5_virtual_trial.py`.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
