# Musculoskeletal Emergence

## Summary
This volume reads muscle, cartilage and bone, together with the mechanical loads they carry, from the R19 switch. The switch thresholds are read from measured master-gene promoter γ: RUNX2 1.2414, TBX5 1.4392, SOX9 1.4598 and MYOD1 1.4933. It inherits the γ ruler and node atlas from **dna**, the time layer from **circadian** and setpoint drift from **aging_senescence**. It adds one module: structure and mechanical load read from measured γ. The claims ledger records the headline as an **interpretation**. The γ values are deterministic code outputs on measured sequence. Mapping them to tissue structure and load is interpretation, and building the tissue (order, size, timing) is open [O] per dna §RB. Biology reading rule (2026-09-29): the volume accepts established observations and uses them. Each statement is an observation (cited), a code output (reproducible, with its dependence on inputs, grid or step stated), a consistency check or an interpretation. The former [F]/[V] grades are relabelled in place, and emergence is attempted only for simple tissue units.

## What changed in this version (2026-09-29)
**Corrections**
- §5 growth-plate ordering (hub and chapter): "γ-rank reproduces limb → cartilage → muscle" was graded [V]. It is now code output plus interpretation, with building [O]. The pass uses 3 of 4 genes, with RUNX2 excluded post hoc, so a match is 1 of 6 possible orders. It also conflicts with observation where the order is testable: somitic myogenesis (Myf5 ~E8, Ott 1991; MyoD ~E10.5, Sassoon 1989) precedes limb Sox9 condensation (~E10.5–11.5, Wright 1995).
- §1: "relative size ∝ γ^1.5" and developmental order from γ are superseded. The spinodal column is labelled consistency and the size column interpretation, with [O] per dna §RB / §AX-A / §AX-I.
- §2 force–frequency: tetanic fusion at "25 Hz" is a grid and criterion artefact (22 Hz on a 1 Hz grid; 32 / 15 Hz at a 0.05 / 0.20 ripple criterion). "Fusion tracks 1/τ" holds by construction, because the kernel depends on u/τ only, so it is relabelled consistency.
- §6 fatigue: τ 59.75 s is the 60 s input recovered by a log-linear fit, a round trip. The 52 % loss equals 0.55·(1 − e⁻³). The 97 % recovery depends on the 180 s rest window (81 / 93 / 99.7 % at 60 / 120 / 300 s).
- §4 Wolff / bone yield: the "[F]" spinodal 0.5324 = 2(γ/3)^1.5 is algebra of the cubic. Reading it as bone yield is interpretation, and the Frost setpoint stays [L].

**New experiments and results**
- None.

**Relabelled grades / reading rule**
- A reading-rule note was added to the hub. The intro now says "read from γ", with building [O] linked to dna §RB. On all pages outside the existing lt-note asides: [V] → code output, [F] → consistency, γ "[V] measured" → observation, "sim-verified" → "simulated". Badges use the hypothesis class. Manifest grade counts forced 6 / verified 45 → 0 / 0; open 6 is unchanged.
- Reading-versus-building notes were added to §1, §5 and the hub.

**Reproduction package changes**
- None. Code and data under `repro/musculoskeletal/` are unchanged since the previous version.

**Site/metadata**
- Biology reading-rule registry integration: `_decl.json`, page notes, hashes, lineage, homepage and sitemap were refreshed. The work-in-progress snapshot commits for the organ volumes and the sibling light reviews (circadian, aging_senescence, inheritance) were included.
- Highwire citation meta is regenerated from the manifest, with gate guards against escaped comments and raw LaTeX.
- Link audit (2026-09-28): stale repro and site links, including the `musculoskeletal_vp_site` slug, were repointed, leaving 0 broken links. The earlier untitled repository snapshot commits ("VP Theory site", "Final", "1111111") imported the volume.

## Claim status (claims ledger)
Counts: interpretation 2 · anchor-restatement 2 · identity 1 (5 rows).
- Structure and mechanical load read from measured promoter γ (RUNX2 1.2414, TBX5 1.4392, SOX9 1.4598, MYOD1 1.4933) — interpretation — the γ are deterministic code outputs; the mapping is interpretation.
- γ-rank reproduces limb → cartilage → muscle developmental order — interpretation — conflicts with observation (somitic myogenesis precedes limb Sox9). The pass uses 3 of 4 genes (1 of 6 orders). Was [V].
- Tetanic fusion at 25 Hz (tracks 1/τ) — anchor-restatement — 22 Hz on a 1 Hz grid; 32 / 15 Hz at 0.05 / 0.20 criterion. f·τ ≈ const is an identity.
- Fatigue τ 59.75 s, loss 52 %, recovery 0.9743 — anchor-restatement — τ recovers the 60 s input; recovery depends on the rest window.
- Wolff / bone-yield threshold = spinodal of the cubic (0.5324 = 2(γ/3)^1.5) — identity — algebra; reading it as bone yield is interpretation; the Frost setpoint remains [L].

## Open items
- Developmental order, size and timing of muscle, cartilage and bone: building is [O] (dna §RB). Bone ossification timing is drive-gated [O].
- Registered [O] scope items on the pages: material and signatureless diseases (§20: OI, EDS/Marfan, Paget), honest treatment limits (§24), and analgesic limits with the central-gain seam owned by neuro/mind (§28).
- Developmental cliffs, cartilage regeneration and established-tumour chemotherapy: [O]. Oncology incidence and fusion/metabolic aetiology: [O].
- Every clinical magnitude is withheld under the magnitude firewall. Treatment chapters name drug classes by mechanism only.

## Reproduction
The ZIP contains `docs/musculoskeletal/` (the published HTML pages), `repro/musculoskeletal/` (engine, inherited substrate, reports), `LEDGER.json` (this volume's claims-ledger rows) and `MANIFEST.sha256` (file hashes).
- Main harness: `cd repro/musculoskeletal && python3 repro/run_all.py`. It prints the emergence, stress, disease, treatment, analgesic and oncology batteries (all PASS in the review). The gates step takes longer than two minutes.
- Dynamics tests T1–T5 (fusion, spinodal, γ-rank, fatigue): `repro/musculoskeletal/repro/_engine/vp_msk_dynamics.py`.
- Gates: `repro/musculoskeletal/repro/_verify/gates.py`.
- SEED = 19. No network is needed.

## Citation and links
- Site: https://jamming-physics.org/musculoskeletal/
- Concept DOI: 10.5281/zenodo.20755760
- Author: Young Jae Lee, ORCID 0009-0002-7535-8245
- Licence: CC BY 4.0
- Corpus guide: https://jamming-physics.org/AGENTS.md
- Claims ledger: https://jamming-physics.org/claims-ledger/
