# COMPLETION LEDGER — cardioresp_vp_site v0.5.0

Signed record of what is complete at this release. The release theme is the **inheritance and activation
of the reproducibility technology** from `analgesic_threshold_logic` v2.0 (`10.5281/zenodo.20733420`),
the binding of this package's concept DOI `10.5281/zenodo.20755371`, and the retroactive-application
plan for the sibling packages. The scientific content is byte-identical to v0.4.0.

---

## A. Task closure against the brief

| # | Brief item | Status |
|---|-----------|--------|
| 1 | Apply the analgesic v2.0 reproducibility technology to `cardioresp_vp_site` | **DONE** — full eight-point apparatus inherited and active |
| 2 | Roadmap was missing the technology → inherit now, apply, and plan retroactive application to existing packages | **DONE** — `FUTURE_WORK.md` §8 records the inheritance + per-sibling plan |
| 3 | Embed this package's concept DOI `10.5281/zenodo.20755371` | **DONE** — site-wide, gated by R10 |
| 4 | Single deliverable, English body | **DONE** — one zip, package-relative paths, English throughout |

## B. Reproducibility suite — gate-by-gate

`python repro/run_all.py` → **OVERALL: PASS (11/11 checks), drift 0**.

| gate | result | evidence |
|---|---|---|
| R1  engine determinism | PASS | two engine runs, identical sha `25900a90079a…` |
| R2  report drift-0 | PASS | whole result blob byte-identical across recomputation |
| R3  stress battery T1–T5 | PASS | 5/5 discriminants |
| R4  oncology forced shape | PASS | RR(0)=1, no-threshold (LNT), barrier matches R19 substrate |
| R5  disease battery | PASS | 6/6, all reuse R19+FHN, no new primitive |
| R6  file manifest (SHA256SUMS) | PASS at release | frozen as the last step; `sha256sum -c` clean |
| R7  forbidden-claim scan (fail-closed) | PASS | 16 patterns over 14 pages, 0 hits |
| R8  grade-token legality | PASS | only {[F],[V],[L],[O]} present |
| R9  [O] ↔ ledger cross-check | PASS | open sections 1, 8, 9, 11 each have an obstacle |
| R10 concept DOI consistency | PASS | `10.5281/zenodo.20755371` site-wide, no placeholder survives |
| R11 offline self-containment | PASS | engine + stress reproduce with the socket disabled |

## C. Deliverables present

- **Reproducibility apparatus** — `manifest/SHA256SUMS.txt` (frozen), `repro/_verify/repro_manifest.py`,
  `claim_scanner.py`, `doc_integrity.py`, drift-0 + offline gates in `gates.py`, suite section [7] in
  `repro/run_all.py` with a single `OVERALL` line and non-zero exit on failure.
- **Governance** — `CONSTITUTION.md` (A1–A7, C0); four-document SSOT (this ledger + `CHANGELOG.md` +
  `MASTER_MANUAL.md` + `HANDOVER.md`); `FUTURE_WORK.md` §8 inheritance + sibling plan.
- **Provenance** — concept DOI bound across every section page, the hub, JSON-LD (`identifier`+`sameAs`),
  `_meta.json`, `llms.txt`, and a `.doi` claim-strip pill; build made wall-clock-free
  (`RELEASE_DATE = 2026-06-18`), "pending archival" placeholders removed.
- **Canonical site** — VP-SPEC v1.8 retrieval-ready, **14 pages** (12 sections + hub + top index),
  engine sha `25900a90079a…`. The writing phase added §10 (DNA emergence chain), §11 (shared-substrate
  spectrum), and §12 (methods/reproducibility), foregrounded the DNA-emergence grounding, and
  strengthened the SEO/JSON-LD surface; every displayed number is still a regenerated engine value.
- **Archival deposit** — `zenodo/` whitepaper (PDF + TeX, scalable fonts, no Type-3) + `ZENODO_METADATA.md`
  (directory excluded from the file manifest).

## D. Honest limits carried forward (unchanged)

- Exactly **two [O] items**: absolute organ size (§1, §9) and absolute cancer relative-risk magnitude
  (§8, §9). Each has a stated obstacle in `IRREPRODUCIBILITY_LEDGER.md`. The forced/verified counterparts
  (size order; dose–response shape; the no-threshold endpoint) stand independently of the open scale.
- The package models **mechanism dynamics only**; no clinical, pharmacological, diagnostic, or treatment
  claim is made, and the fail-closed scanner (R7) keeps it that way.
- The reproducibility technology has been **inherited and applied here**; its application to the sibling
  packages is **planned** (FUTURE_WORK §8), not yet executed in those packages.

## E. Reproduce / re-pin

```
python repro/run_all.py                            # OVERALL: PASS (11/11), drift 0
python repro/_verify/repro_manifest.py freeze      # re-pin after any intentional edit (freeze last)
```

**Sign-off.** v0.5.0 closes the reproducibility-technology inheritance for `cardioresp_vp_site`. The
engine output is unchanged from v0.4.0; the change is the delivery-side guarantee layer and the DOI
binding. — Young Jae Lee, 2026-06-18.
