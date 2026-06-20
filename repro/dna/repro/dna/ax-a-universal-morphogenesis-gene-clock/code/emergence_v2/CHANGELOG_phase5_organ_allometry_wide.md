# CHANGELOG — Phase 5 + continuation handover

## Phase 5 (this session): organ-allometry [O] → [L] promotion, add-only

**Goal (handover §7, 택1 Option 1):** promote the package's single most borderline result — the
organ-allometry validation, sitting at exact p=0.069 (just above 0.05) — from **[O]** to
**[L]-grounded**, by *widening the organ set with independently-cited exponents only*, with zero
tuning and zero modification of any pinned file.

**Outcome: achieved.** Pre-registered full set n=11 → ρ=+0.800, exact-perm p=0.0047 → **[L]-grounded**.
Gate `verify_emergence_organs_wide.py` → **8/8 PASS**.

### Files ADDED (all new; nothing pinned was touched)
- `param_db_wide.json` — 3 added interspecific exponents [L] (skeleton 1.08, blood 1.00, skeletal_muscle 1.10), each with per-tissue provenance; separate file so `param_db.json` sha256 stays intact.
- `validation_targets_wide.json` — ICRP-89 newborn/adult masses for the 3 tissues, same body span (73000/3500); read only by the gate.
- `emergence_organs_wide.py` — engine merging `param_db.json` (8) + `param_db_wide.json` (3) → 11 organs; never reads any target file; determinism sha `d82eeb925973`.
- `verify_emergence_organs_wide.py` — gate: DB-sourced · NON-FIT · determinism · body-anchor consistency · allometric **ladder A(8)→B(10)→C(11)** with exact-perm null · brain anchor · non-blind · robustness (±0.02 jitter) → 8/8 PASS.
- `LEDGER_organ_allometry_wide.md` — grade-of-record: the promotion, the full ladder, the pre-registration rule, the five-point anti-p-hacking defense, residual [O] = organ ABSOLUTE mass.

### Reproduce
```
cd emergence_v2
python3 emergence_organs_wide.py            # engine, sha d82eeb925973
python3 verify_emergence_organs_wide.py     # gate, 8/8 PASS (~1 min: exact n=11 null)
```

### Discipline honored
NON-FIT (engine never reads targets) · grade==evidence (rung A still honestly [O]) · add-only
(no pinned file changed; Phase-2 result reproduced byte-for-byte as the locked rung) · no
fabrication (every exponent and mass is primary-source cited) · no back-fit (exponents fixed in
comparative mammalian physiology, independent of the human masses; the 3 new tissues carry no γ
master, so the wider test is *more* independent of the gene-clock layer).

---

## Continuation handover — next deliberate step (NOT done here)

**Phase 6 fold-in / `--freeze` (separate, intentional):**
1. Fold the five Phase-5 files into the `integrated_v1_9_1/` snapshot tree.
2. Add `verify_emergence_organs_wide.py` to the snapshot's `verify_all.py` aggregator (new gate line; expected OVERALL count rises accordingly).
3. Re-pin sha256 across the snapshot and re-issue the zip + `.sha256`.
4. Update the Appendix-A / `dna_vp` main-body narrative wherever it states the organ-allometry grade: change **[O] (n=8, p=0.069)** → **[L]-grounded (n=11, ρ=0.800, p=0.0047)**, citing the pre-registered widening and the ladder. Keep the residual **[O] = absolute organ mass (g)** explicit.
5. Maintain DOI 10.5281/zenodo.20471407 lineage (new version note).

**Remaining Phase 5 menu options still open (handover §7), for future sessions:**
- Option 2 — timing absolute-clock verification axis.
- Option 3 — continuum trajectory [F] → measurement comparison.
- Option 4 — merge emergence layer into `dna_vp` main body.

**Integrity note:** the full `verify_all.py` (snapshot, expected OVERALL 18/18) had its morpho-gate
suite and emergence gates + integrity layer independently confirmed PASS earlier; the slow RD/exact-perm
layers were still finishing at last check. Re-run to completion is advised as part of the Phase-6 freeze,
since the wide gate will be added to that aggregator anyway.
