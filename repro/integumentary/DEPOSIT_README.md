# Integumentary VP — Reproducibility Archive (Zenodo deposit)

**Package** `integumentary_vp_site` (code: `skn`)
**Version** 1.0.0 — in-lane program complete — build 2026-06-19
**Author** Young Jae Lee · ORCID [0009-0002-7535-8245](https://orcid.org/0009-0002-7535-8245)
**Project** VP Theory — Jammed-Granular-Vacuum Emergence
**Canonical site** https://jamming-physics.org/integumentary/
**License** Creative Commons Attribution 4.0 International (CC BY 4.0)
**Governance** VP-SPEC v1.8 (constitution C0 overrides on conflict)

---

## DOI

- **Concept DOI (all versions, preferred citation handle):** `10.5281/zenodo.20754541`
  — minted on Zenodo, 2026-06-19. This is the canonical, version-independent identifier; it always
  resolves to the latest version of the record. Use this for general citation.
- **Per-version DOI (this v1.0.0 record):** `10.5281/zenodo.20754542`
  — resolves to this exact frozen snapshot.

The concept DOI is stamped into the package itself: every chapter and the hub carry it in the
claim-strip, in the per-page JSON-LD (`sameAs`), and in `docs/_meta.json` (`doi_concept` / `doi_version`).

Stamping the DOI was a **deposit-time action, not a code change** (per `COMPLETION_LEDGER §7.4`): it
touches only documentation and metadata surfaces, never the engine. The seven frozen result hashes below
are therefore preserved byte-for-byte, exactly as released, and re-verify 7/7 after the stamp.

---

## What this is

The integumentary system reconstructed as an **emergent** consequence of one
vendored bistable primitive — the R19 switch `ds/dt = g·s − s³ + h` — with the
control parameter `g` carried read-only as the measured master-gene order
parameter γ from the DNA gene-clock. No constant is chosen to hit a target
(strict no-tuning rule). Five organs switch on from their measured γ; ten
discriminant targets (T1–T9 + an oncology kernel) and twenty-three skin
diseases are reproduced as **signed perturbations of one existing knob**.

Full prose, derivations, tables, and the honesty ledger are in the companion
whitepaper bundled here under `paper/`.

---

## Archive layout

```
integumentary_vp_site/
├── DEPOSIT_README.md          ← this file
├── START_HERE.md              ← reader entry point
├── CHARTER.md                 ← scope + governing rules
├── CHANGELOG.md               ← full version history
├── MASTER_MANUAL.md           ← operating manual
├── COMPLETION_LEDGER.md       ← completion gate record
├── HANDOVER.md                ← session handover SSOT
├── ANCHORS_VERIFIED.md        ← cited-anchor verification
├── IRREPRODUCIBILITY_LEDGER.md← what is NOT bit-reproducible and why
├── VP_SPEC_v1_8.md            ← governing specification
├── VERSION  /  PHASE          ← 1.0.0 / writing
├── paper/                     ← NEW: human-readable whitepaper (added at deposit)
│   ├── integumentary_vp_site_v1.0.0_whitepaper.tex
│   └── integumentary_vp_site_v1.0.0_whitepaper.pdf
├── docs/                      ← canonical per-title HTML (14 sections + hub)
│   ├── _meta.json
│   └── 01../14../index.html
├── repro/                     ← reproducible engine + runners + audit
│   ├── run_release_audit.py   ← re-verifies all 7 hashes + gates
│   ├── run_all.py  run_pathology.py  run_cycle.py  run_seb.py
│   ├── run_adhesion.py  run_vasomotor.py  run_seam.py
│   ├── _engine/ _pathology/ _cycle/ _seb/ _adhesion/ _vasomotor/ _seam/ _oncology/ _verify/
│   └── REPRODUCE.md
├── reports/                   ← release_audit.json (machine verdict)
├── manifest/                  ← seam + target manifests
├── tools/                     ← build/validation helpers
└── inherited/                 ← read-only inputs vendored from sibling packages
```

The `paper/` directory is **additive only** — it is documentation. It touches no
engine file, so the seven frozen hashes are unchanged by its presence.

---

## How to reproduce (one command)

Requirements: Python 3 with NumPy (verified on NumPy 2.x; SEED is fixed in-engine).

```bash
cd integumentary_vp_site
python3 repro/run_release_audit.py
```

Expected verdict:

```
all frozen hashes match : True
all gates green         : True
RELEASE-READY           : True
```

The audit re-runs each canonical runner in its own subprocess and asserts that
the SHA-256 of its result matches the pinned value. Two independent runs produce
byte-identical output.

---

## Frozen determinism contract — 7 result hashes (SHA-256)

| Layer | Runner | SHA-256 |
|---|---|---|
| core T1–T5 + oncology | `repro/run_all.py` | `1fb59f556e01882916c0f4b4e72aa76ad47ef348bffb81fe4a7f3ce9093d3e92` |
| pathology (13 + 5-way) | `repro/run_pathology.py` | `0a4404ccde6559a7621249de90cd889f907619db48a4104329f3af2f74c51cd8` |
| hair-cycle (T6) | `repro/run_cycle.py` | `d910fa5d2854462236a5ef56b831490f1aca82ba37050b3f8bb751198b356822` |
| sebaceous (T7) | `repro/run_seb.py` | `1e8a557d9a8d7b05823259bb2fcac31e372b96272e47ef1f2f5d89b1b0246a84` |
| adhesion (T8) | `repro/run_adhesion.py` | `55dce8c267ea4c76d8d5b967535a4ee0876c4b67f605e6ae7d65bf38516f28ad` |
| vasomotor (T9) | `repro/run_vasomotor.py` | `53a99f522ad684a11bcc6d4d33c5e8123d1f4dff5a75836c0bbced6736a62003` |
| seam manifest | `repro/run_seam.py` | `52b49a95a9add070a05a02848b1a4cef0589f4a36791167232fda3fc1c1d58f7` |

Verdict of record: **7/7 hashes match, all gates green, release-ready.**

---

## Grading vocabulary (honest, retained)

- **[V]** simulation-verified shape on this substrate
- **[L]** cited literature anchor
- **[F]** substrate-forced regime scale
- **[O]** absolute magnitude open, with a stated obstacle

What is *not* bit-reproducible, and why, is logged in
`IRREPRODUCIBILITY_LEDGER.md` rather than hidden.

---

## How to cite

> Lee, Y. J. (2026). *Integumentary Emergence in the Jammed-Granular-Vacuum
> Framework: The Epidermal Barrier, Wound-Healing Unjamming, and the
> Ultraviolet-Carcinogenesis Showcase* (Version 1.0.0) [Computational science
> package]. Zenodo. https://doi.org/10.5281/zenodo.20754541

The DOI above is the concept DOI (version-independent). To cite this exact
snapshot, use the per-version DOI https://doi.org/10.5281/zenodo.20754542.
