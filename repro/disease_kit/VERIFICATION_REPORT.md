# Verification Report — `vp_disease_site_evidence_complete`

**Subject:** From a Single Bistable Switch to a Falsifiable Corrective Direction — the VP Disease Emergence Kit (static evidence site)
**Package release:** `0.42.1-trackA.merged_3of3` · **register chain-head:** `fc8598ec13f74a9e94d405d1be25573f13e4c0b7f93d3c96e958de9cfc01f658`
**Date:** 2026-06-22 · **Author / verifier of record:** Young Jae Lee (ORCID 0009-0002-7535-8245) · **Licence:** CC BY 4.0

---

## 1. Verdict

The package is **evidence-complete and self-contained**. The site reproduces byte-for-byte from the four
pinned source JSONs; both integrity manifests verify in full; every on-page headline number was
independently recomputed from the source data and matches; there are no dangling references; the V1–V18
falsification record is complete and offline-reproducible; and the full provenance chain (`inputs/` →
`outputs/` → rendered pages) is intact. Nothing needed to be imported from the upstream kit
(`vp_disease_kit_0.42.1-trackA.merged_3of3`); the cross-check below confirms the curation decisions are
truthful and lossless.

## 2. Scope and method

Verification was performed against the package as shipped, plus a cross-check against the upstream kit.
Steps: (a) execute the deterministic builder and diff its output against the shipped `docs/`; (b) verify
both SHA-256 manifests per-file and recompute their tree-digests; (c) re-derive every headline statistic
directly from the source JSONs using the builder's own predicates; (d) resolve every internal link and
sitemap URL; (e) confirm the validation record is complete with pinned snapshots; (f) trace citation
provenance from rendered pages back to `inputs/`; (g) hash-compare the source data against the kit.

## 3. Reproducibility

`python3 tools/build_disease_site.py` regenerates the site from `outputs/` only (standard library;
no wall-clock timestamps; SEED-fixed). Result:

- Rebuilt `docs/` is **byte-for-byte identical** to the shipped tree (`diff -rq` reports no differences).
- Regenerated `SITE_BUILD_MANIFEST.sha256` and `SITE_README.md` are identical to the shipped copies.
- Site tree-digest matches: `f3b70e445fdd170bc29966c6f00a4edb1a6b8cc058c6ccb6bfb07d2493b18220`.

## 4. Integrity manifests

| Manifest | Covers | Files | Per-file hash | Tree-digest | Result |
|---|---|---|---|---|---|
| `SITE_BUILD_MANIFEST.sha256` | `docs/` | 877 | SHA-256 | `f3b70e44…3b18220` | **877/877 OK**, digest reproduced |
| `EVIDENCE_MANIFEST.sha256` | `outputs/` + `inputs/` + `validation/` | 149 | 2× SHA-256 (hex) | `1f630ba6…8966ed0` | **149/149 OK**, digest reproduced |

Both manifests now carry their hash and tree-digest **formulas in the header**, so the roll-up digests are
independently reproducible (see §7, observation 2).

## 5. Headline numbers — independently recomputed

All figures were recomputed from the source JSONs (not read from the rendered HTML) and match the site:

| Claim | Recomputed | Source |
|---|---|---|
| Disease pages | 839 | `actionability_index.json.diseases` |
| MATCH / NOVEL / HOLD | 322 / 29 / 488 (Σ = 839) | `classify_disease` over the source set |
| Surfaced candidate rows | 233 | `surfaced_candidates.json` |
| Rediscovery / novel split | 147 / 86 | `candidate_register.json.prior_art_split` |
| Distinct (disease, citation) pairs | 947 | `mapped_levers.json` |
| Candidates with `prior_art_source` | 228 / 233 | `surfaced_candidates.json` |
| Candidates with `prior_art_note` | 233 / 233 | `surfaced_candidates.json` |
| Magnitude-firewall leaks | 0 (`status: PASS`) | `firewall_log.json` |

## 6. Structural integrity, validation, and provenance

- **No dangling references.** The only local asset referenced across all 872 HTML pages is
  `assets/css/site.css`, which is present. **7,534** internal page links and **872** sitemap `<loc>`
  targets all resolve (0 broken, 0 missing).
- **Falsification record complete.** `validation/` carries **V1–V18**, each with a pre-registration JSON,
  a test/holdout script, a `*_results.json` + `*_results.html`, a per-test firewall log, an
  `expected_sha256_*.json`, and — where external data is used — a pinned `*_snapshot.cache.json` plus a
  refetch-audit, so each test is reproducible offline.
- **Provenance chain intact.** `inputs/disease_inputs.json` and `inputs/kit_reads.json` each cover all
  **839** diseases; every disease rendered in `outputs/` is present in both inputs (0 missing); and all
  **939** distinct citation strings in `mapped_levers.json` are present in `disease_inputs.json`.

## 7. Cross-check against the upstream kit

- The five `outputs/` JSONs (`actionability_index`, `mapped_levers`, `surfaced_candidates`,
  `candidate_register`, `firewall_log`) and both `inputs/` JSONs are **byte-identical** (SHA-256 match)
  between this package and `vp_disease_kit_0.42.1-trackA.merged_3of3`.
- The eight Korean narrative summaries the package declares omitted
  (`V9..V16 *_INHERITANCE_CHECKPOINT*.md`) exist in the kit and were confirmed to be **narrative prose
  only**; their machine-readable content (hypotheses, criteria, hashes) lives in the corresponding
  `V9..V16 *_PREREGISTRATION.json` files, which are included. No machine-readable evidence was lost.

## 8. Observations from the prior verification — disposition in this build

**Observation 1 — two version labels.** The site and metadata display package release
`0.42.1-trackA.merged_3of3`, while `outputs/candidate_register.json.release` reads `0.40.0-repurposing.3`.
This is **not** a data inconsistency. The candidate register is append-only and hash-chained; its
`chain_head` (`fc8598ec13f74a9e…`) is computed as `sha256(prev + canonical(row))` over the genesis seed
and the 233 rows **only** — the `release` string is metadata and is not part of the hash pre-image
(verified in `pipeline/build_candidate_register.py`). The identical chain-head under both labels is the
cryptographic proof that the rows are unchanged across the relabelling. **Disposition:** the register's
`release` field is **preserved** as an honest mint-time record (overwriting a field in an append-only,
hash-chained artifact would violate that discipline); the relationship between the two labels is now
documented in `EVIDENCE_INDEX.md` (§ "Release labelling").

**Observation 2 — non-reproducible roll-up digest.** The prior `EVIDENCE_MANIFEST.sha256` tree-digest could
not be reproduced from standard formulas (per-file hashes verified, but the roll-up was opaque).
**Disposition:** `EVIDENCE_MANIFEST.sha256` was regenerated with the 149 per-file lines **byte-identical**
to the original (each re-verified) and a **documented, reproducible** tree-digest; both the per-file and
tree-digest formulas are now written into the manifest header. The new roll-up is
`1f630ba6aa7c9e22702a780754d0eb822d79b1a2fa130f17dd7e54f4a8966ed0`.

## 9. Key digests (this build)

```
register chain-genesis : f51f67f34c8659494a6ce5a8475b021b88878b1a7fd5d35444b9db0000fc3b01
register chain-head    : fc8598ec13f74a9e94d405d1be25573f13e4c0b7f93d3c96e958de9cfc01f658
site tree-digest       : f3b70e445fdd170bc29966c6f00a4edb1a6b8cc058c6ccb6bfb07d2493b18220   (877 files)
evidence tree-digest   : 1f630ba6aa7c9e22702a780754d0eb822d79b1a2fa130f17dd7e54f4a8966ed0   (149 files)
```

Per-file digests for every site and evidence file are listed in `SITE_BUILD_MANIFEST.sha256` and
`EVIDENCE_MANIFEST.sha256` respectively. To reproduce: `python3 tools/build_disease_site.py` (site) and the
formulas in the `EVIDENCE_MANIFEST.sha256` header (evidence roll-up).

---

*This report certifies a verification performed on the package contents as of the date above. It does not
assert clinical validity of any biological direction; all directions in the kit are direction-only [O]
hypotheses for expert evaluation under the stated safety firewall.*
