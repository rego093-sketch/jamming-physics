# Chapter 22 — ADHD vs autism (separate, gene-grounded)

**Status (v1.32):** in-silico mechanism on the READ-ONLY engine cerebrum. ADHD **model
validity OPEN** (no separately-validated ADHD model). **efficacy = 0 · NOT medical advice.**

## Claims verified (VC4)
An **explicit** gene-grounded ADHD substrate (not a relabelled autism cohort): 8 ADHD genes —
O/gain (DRD4, SLC6A3, COMT, SNAP25, DBH, TH), T/arousal (ADRA2A, SLC6A4), **W = none**; 4 live
NCBI; FOXP2, ADGRL3 pre-registered excluded so "ADHD has intact W" is airtight.
- **P-VC4a.** On intact geometry the stimulant restores ADHD to health in **both R and PAC**
  (gain ×2.0); on broken geometry it restores autism's PAC but R stays **capped** below health.
- **P-VC4b.** The cap's far-pair benefit is **3.34×** larger where wiring is broken (autism
  Δfar 0.136 vs ADHD 0.041) — the cap is redundant for ADHD once gain is restored.
- **P-VC4c.** On an explicit **AuDHD** substrate the two **compose**: stimulant fixes gain
  (PAC → health), cap fixes routing (far 0.213), R 0.393 below the over-sync edge, no interference.

## Reproduce
```
cd ../_verify && python3 run_all_vc.py
```
VC4 `aed19bc2…`. See `_verify/vc4_adhd_coemergence.py`, `_verify/adhd_cohort_promoters.json`.

## Honesty ledger
medium_efficacy_tested 0 · consciousness_claim 0 · new_tuned_constants 0 · no_cure_claimed 1.
