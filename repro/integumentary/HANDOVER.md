# HANDOVER — `integumentary_vp_site` v1.0.0

**Author:** Young Jae Lee (ORCID 0009-0002-7535-8245).
**Read order for a new session:** `START_HERE.md` → `CHARTER.md` → this file (then `MASTER_MANUAL.md` /
`COMPLETION_LEDGER.md` for depth). **State is carried by files only** (VP-SPEC §1); a single zip is the
unit of handoff.

---

## 1 · Where the package stands

**v1.0.0 — the in-lane (jamming barrier/interface + external-insult) research-and-writing program is
complete.** Ten targets (T1–T9 + oncology), twenty-three diseases, and the cross-package seam manifest are
delivered, verified, and published as fourteen canonical HTML sections. Seven determinism hashes are
frozen and green; `python repro/run_release_audit.py` re-checks all of them at once and writes
`reports/release_audit.json` (`all_ok = true`).

This is a **0.x → 1.0** transition: it marks that the package's physical class is fully covered and what
remains is cross-package integration that needs infrastructure not yet built. It is not a claim that skin
biology is finished — it is the honest statement that *this self-contained package's lane* is done.

## 2 · What v1.0.0 changed (small, on purpose)

The release is **label-only over v0.9.0's computation plus governance**. Concretely:

1. **Added one additive, read-only artifact:** `repro/run_release_audit.py` — a top-level consolidation
   gate that re-runs every canonical runner in its own subprocess and asserts each emitted sha equals its
   pinned value, then writes `reports/release_audit.json`. It imports nothing from the engine or the gates
   and computes no physics, so it cannot perturb any hash.
2. **Verified the cited `[L]` anchors against current literature** (network) and recorded them in
   `ANCHORS_VERIFIED.md`: the T4 turnover window is resolved (the CHARTER `TO-ANCHOR` flag is cleared);
   the melanoma-intermittent / SCC-cumulative dichotomy and the OCA → SCC hazard are confirmed; and the
   "melanoma burst RR ≈10.59×" figure is flagged as a **kernel-sensitivity quantity, not an OCA melanoma
   incidence** (OCA melanoma is clinically rare — consistent, because OCA removes the melanocytic
   substrate). No computation changed.
3. **Wrote the four-document SSOT:** `CHANGELOG.md` (v1.0.0 entry), `MASTER_MANUAL.md`,
   `COMPLETION_LEDGER.md`, this `HANDOVER.md` (plus `ANCHORS_VERIFIED.md`).
4. **Bumped the version label** to 1.0.0 and the build date to 2026-06-19, and re-stamped the HTML: the
   **only** change to the fourteen existing pages + hub is the version/date label (verified by diff). The
   seven determinism hashes are byte-identical to v0.9.0.

What v1.0.0 deliberately did **not** do: it added no new mechanism, no new constant, no new γ, and no new
disease. The in-lane roadmap was already exhausted at v0.9.0 ("the one remaining in-package, harness-free
next step").

## 3 · The frozen-hash contract (must stay byte-identical)

| layer | runner | sha256 (short) |
|---|---|---|
| core T1–T5 + oncology | `run_all.py` | `1fb59f556e01…` |
| pathology | `run_pathology.py` | `0a4404ccde65…` |
| hair-cycle | `run_cycle.py` | `d910fa5d2854…` |
| sebaceous | `run_seb.py` | `1e8a557d9a8d…` |
| adhesion | `run_adhesion.py` | `55dce8c267ea…` |
| vasomotor | `run_vasomotor.py` | `53a99f522ad6…` |
| seam | `run_seam.py` | `52b49a95a9ad…` |

Full hashes in `COMPLETION_LEDGER.md` §5. Re-confirm with `run_release_audit.py` before any package.

## 4 · What the next session CAN do

- **DOI minted and wired (done 2026-06-19).** Concept DOI **10.5281/zenodo.20754541** (per-version DOI for
  v1.0.0: **10.5281/zenodo.20754542**) is stamped into every chapter + hub claim-strip, the per-page
  JSON-LD (`sameAs`), `docs/_meta.json`, and `DEPOSIT_README.md`. This was a deposit-time action — no engine
  code changed — and the seven frozen hashes still re-verify 7/7 via `run_release_audit.py`.
- **Optional anchor/doc refinements** (recorded in `ANCHORS_VERIFIED.md`, non-blocking): widen the stated
  T4 turnover window toward the newer ~48–56 d literature; split BCC from SCC toward the
  intermittent/recreational pole. Both are documentation/anchor edits that would **not** touch any `[V]`
  shape or any hash. If done, they regenerate only via `build_docs.py` (and the relevant `[L]` text).
- **Add a genuinely new in-class mechanism** *if one is identified* — strictly via the §5 recipe in
  `MASTER_MANUAL.md` (new target + own gate + own hash, verified green, **then** the disease). Note: the
  obvious in-lane candidates are already delivered; a new one would need a newly identified jamming-class
  failure mode, not a re-labelling of an out-of-class disease.

## 5 · What the next session CANNOT do here (blocked, honestly)

- **Live-wire the DECLARED-OUT cross-package contracts** (HANDOFF §5.3 first bullet + §5.4): import the
  `disease_wp` gene-key parameters (XP / OCA / EDA / genetic ichthyosis), have the dynamics entries emit
  the systemic-trajectory side, and register each gene-lesion on the `disease_wp` side with a
  back-pointer. **This needs the integration harness, which does not exist.** It is a *cross-package*
  task; it cannot be completed inside this single self-contained package. It is recorded in the seam
  manifest as DECLARED-OUT, not faked.
- **Model out-of-class diseases in-lane** (urticaria/angioedema, lichen planus → immune-effector seams;
  cutaneous infections → out of physical class; secondary-Raynaud fixed ischemia → rheumatology seam).
  Forcing these onto an unrelated knob would violate no-tuning. They are named, not modelled.

## 6 · User-return convention

Return a **single zip** (internal paths = package-relative), never fragments. Merge any additions/edits
into the one zip and hand it to the next session. `START_HERE.md` → `CHARTER.md` remains the entire
bootstrap; this `HANDOVER.md` carries the rest.
