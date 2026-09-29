# sensory_organ — light review (2026-09-29)

Volume: `docs/sensory_organ/` (hub + 12 chapters), code `repro/sensory_organ/`, declaration `docs/sensory_organ/_decl.json`.
Reviewers: R1 (claims vs data), R2 (code & inheritance). No page or code was edited.

## Summary

1. The code runs cleanly and reproduces every number the pages print. Determinism holds (sha `6a68bc48…`), gates are all green, and `tools/check_integrity.py` passes with 0 broken links. The classical anchors are correct arithmetic: reduced eye 22.27 mm, 2.69 D/mm, Greenwood 19.8 Hz–20.7 kHz, Hofstetter.
2. Two headline numbers are artefacts of numerical choices, not physics. The "max slope 3.1–3.3 ≈ Hill 3" depends on the grid: it goes 2.4 → 3.3 → 4.5 → 6.1 as the grid is refined. The "gain 464 at µ=0" is exactly F_probe^(−2/3) for the chosen F = 1e‑4. Both are presented as [V] agreement with data.
3. The developmental-order [V] ("taste latest confirmed") still sits in the hub, §1 and §2 next to the 2026-09-29 banner that supersedes it. The relative Kramers rates in §10 depend on an arbitrarily chosen D, but the page says only the absolute rate needs D. No magnitude-firewall violation was found: the doses are literature citations under an explicit banner.

## R1 — claims vs data

| # | Page / exact sentence | Finding | Severity |
|---|---|---|---|
| R1-1 | `docs/sensory_organ/03-unified-molecular-transducer-r19-switch/index.html`: "Sigmoid maximum slopes cluster near 3.1–3.3 (cooperative gating), matching cited Hill coefficients ≈3." Also §4 ("maximum slope 3.32 — consistent with … Hill ≈3") and §9 ("slope 3.12"). | The number is not a Hill coefficient. It is `max(np.gradient(s*(h)))` on a 41-point grid over [−h_sp, h_sp] of the low branch, where ds/dh = 1/(3s²−g) diverges at the spinodal. Rerunning `transduction._steady_state` with RAX γ = 1.4541 gives 21 pts → 2.39, 41 → 3.32, 81 → 4.54, 161 → 6.07. The "match to Hill ≈3" comes from the choice of grid. It is presented as [V] evidence against data. | **blocker** (for this claim only) |
| R1-2 | `docs/sensory_organ/07-cochlear-hopf-amplifier-cube-root/index.html`: "Small-signal gain rises from 1 far below to ~464 at criticality." | In the normal form the small-signal gain at µ=0 is unbounded. The code (`cochlear_amplifier.py`, `F_probe = 1e-4`) returns R/F = F^(−2/3) = 10^(8/3) = 464.16 exactly, so 464 restates the probe amplitude. The values 1, 10, 99 are just 1/\|µ\|. The qualitative statement (gain rises toward µ=0) is fine; the number should be labelled probe-dependent. The 1/3 exponent itself is correct and forced by the normal form. It could be graded [F] rather than [V], and `_decl.json` lists `forced: 0`. | should-fix |
| R1-3 | `docs/sensory_organ/01-organ-emergence-from-measured-gamma/index.html`: "Sorting the five measured γ values yields an emergence order whose falsifiable prediction — taste specified latest — is confirmed [V]". Similar wording in the hub card "the falsifiable order (taste latest) is confirmed" and hub lede "their developmental order is a parameter-free read-out of those measured numbers", and in §2 "The developmental order, for instance, is simply argsort(γ)". | The page's own 2026-09-29 banner says γ-order is superseded (dna §AX-A null, §AX-I). The body and hub still assert the order as [V], so the grade contradicts the banner. On the substance, argsort puts EYA1 (cochlea) first and PAX6 (eye field) fourth. The PAX6 eye field is specified before the otic placode, so the ordering is contradicted beyond the "taste latest" point. TAS1R3 is a receptor gene, not a taste-bud developmental master gene; taste-bud development is SHH/SOX2-driven. The "taste latest" check is one bit on five values. | should-fix |
| R1-4 | `docs/sensory_organ/10-disease-setpoint-drift-basin-collapse/index.html`: relative crossing-rate column "1.00× … 20.09× … 52.46×" with "absolute incidence is [O] (needs the noise scale)". | The relative rates also depend on D. The code sets `D_ref = 0.25·B0` (`repro/sensory_organ/repro/_pathology/setpoint_failure.py:65`), so rate_rel = exp(4·(1−(1−d)²)) for every γ, and 52.46 = e^3.96. A different D changes every number in the column. Only the barrier-fraction column (1−d)² is D-free. | should-fix |
| R1-5 | §3 table "barrier 0.529 / 0.531 / 0.605" and "every channel … verified bistable". | These are γ²/4 of the master TF genes (RAX, SOX2, TAS1R3), not of the channel genes (which are declared "to-measure"). Bistability holds by construction for any g > 0. The [V] therefore verifies the R19 normal form, not the channels. The wording "each verified bistable" overstates what was tested. | should-fix |
| R1-6 | §5: "Hofstetter's formula, amplitude = 25 − 0.40·age". | This is Hofstetter's *maximum*-amplitude formula; the average is 18.5 − 0.30·age, which gives ≈0.5 D at 60. Name it as the maximum formula. The reduced-eye 22.27 mm is the reduced-eye focal length (n′/P), not a real axial length (≈23.5–24 mm); the page frames it correctly as a model value. | nit |
| R1-7 | §11 / §12: "low-dose atropine … 650 nm red light", "RCT-supported ≥50% slowing". | These are literature citations with a clear firewall banner. No dose, concentration or schedule is emitted, so there is **no firewall violation**. Optionally, add the reported retinal-safety concerns for repeated low-level red light next to "long-term safety still accruing". | nit |
| R1-8 | §6 Greenwood (19.8 Hz–20 677 Hz), §5 2.69 D/mm, §8 flatness 0.018 / VOR ≈1.0. | Correct and honestly graded [L]/[V-arith] as classical anchors that are not re-derived. | no action |

## R2 — code & inheritance

**Scripts run** (python3 -B, all < 120 s, no errors): `repro/_engine/vp_sns_engine.py`, `transduction.py`, `cochlear_amplifier.py`, `organ_optics.py`, `repro/_pathology/setpoint_failure.py`, `treatment.py`, `run_all.py`, `_verify/gates.py`, `_verify/stress_tests.py`.

| # | Finding | Evidence | Severity |
|---|---|---|---|
| R2-1 | Printed numbers match the pages. | exponent 0.3333; gains 1.0/9.9999/99.03/464.16; axial 22.267 mm; 2.695 D/mm; accommodation 19.0/1.0 D; Greenwood 19.8/20677; flatness 0.018; slopes 3.32/3.31/3.12; hysteresis 1.35–1.49; restoration 0.5708→0.0913→0.4420 (0.7314); sha `6a68bc48…` matches §2. | no action |
| R2-2 | The slope metric is grid-dependent (see R1-1). | `repro/sensory_organ/repro/_engine/transduction.py` lines ~108–111: `hs_grid = np.linspace(-hs, hs, 41)`; `steep = np.max(np.gradient(...))`. | blocker (for the claim) |
| R2-3 | The gain at µ=0 is set by the probe amplitude (see R1-2). | `cochlear_amplifier.py`: `F_probe = 1e-4`. | should-fix |
| R2-4 | The noise scale for the relative rate is a hidden choice (see R1-4). | `setpoint_failure.py:65` `D_ref = 0.25 * B0 + 1e-9`. | should-fix |
| R2-5 | Inheritance of γ is honoured. All five vendored γ in `repro/sensory_organ/inherited/organ_gamma.json` equal `repro/dna/repro/dna/ax-a-universal-morphogenesis-gene-clock/code/data/sensory_organ_gamma.json` exactly. `inherited/organ_identity.md` states that DNA owns identity and order, and the olfaction master is "to_measure" rather than invented. No DNA-atlas node is re-derived. | file comparison | no action |
| R2-6 | The source atlas is AX-A, the γ-order clock that DNA itself now reports as a null for order. The engine still computes and grades `order_grade="[V]"` and `broad_validated` (`vp_sns_engine.py:93–123`). This is the code side of R1-3. | `vp_sns_engine.py:95, 123` | should-fix |
| R2-7 | Cross-volume γ ambiguity, not a sensory bug: DNA's own "how to read a locus" page uses SOX2 γ = 1.287315 (302 kb locus), while the AX-A promoter value used here is 1.4573. The two windows differ and neither page says so. A one-line note in §1/§12 ("promoter window TSS−2000..+500; the locus-wide value differs") would prevent confusion. | `docs/dna/how-to-read-a-locus/index.html`; `docs/sensory_organ/12-…/index.html` | nit |
| R2-8 | Declared inheritance is incomplete in `seams.json`. `_decl.json` declares `inherits_volumes: ["dna","neuro"]` and the hub says the signal is "handed off to the Neural Emergence Chain", but `docs/sensory_organ/seams.json` has only an outgoing edge to `dna`, with no `neuro` edge and no physics/substrate edge (the hub says R19/FHN is "vendored from the jamming foundation"). | `docs/sensory_organ/seams.json` | nit |
| R2-9 | `_decl.json` grade counts (`forced: 0, verified: 21`) do not reflect that the cube-root exponent is forced by the normal form, or that the order claim is superseded. | `docs/sensory_organ/_decl.json` | nit |
| R2-10 | Integrity: `tools/check_integrity.py` reports links PASS (0 broken), scripts PASS (13 known gaps corpus-wide, 0 new), aggregates PASS. Pages link only to the repro folder root, not to individual scripts, which makes tracing a number to its script harder. | tool output | nit |

## Action table

| Bucket | Item | File | Severity |
|---|---|---|---|
| **Fix now (small, safe)** | Relabel §7 "~464" as "probe-dependent (R/F = F^(−2/3) at F = 1e‑4)"; keep "gain rises toward µ=0". | `docs/sensory_organ/07-…/index.html` | should-fix |
| Fix now | §10: state that the relative-rate column uses D_ref = B0/4 and is illustrative. Only the barrier fraction is D-free. | `docs/sensory_organ/10-…/index.html` | should-fix |
| Fix now | Remove or downgrade the "taste latest confirmed [V]" and "order = argsort(γ)" wording in the hub, §1 and §2 so it agrees with the banner (reading only). | `docs/sensory_organ/index.html`, `01-…`, `02-…` | should-fix |
| Fix now | §5: "Hofstetter maximum-amplitude formula". | `05-…` | nit |
| Fix now | Add `neuro` (and substrate) edges to `seams.json`. | `docs/sensory_organ/seams.json` | nit |
| **Needs author** | Retract or replace the "max slope 3.1–3.3 ≈ Hill 3" match. Either compute an actual Hill coefficient from a declared model or drop the comparison. Current value is a grid artefact. | `03-…`, `04-…`, `09-…`, `transduction.py` | blocker |
| Needs author | Decide whether "every channel verified bistable" should read "the R19 normal form at the master-gene γ is bistable (by construction for g>0); channel γ to-measure". | `03-…` | should-fix |
| Needs author | Retire or regrade `order_grade`/`broad_validated` in the engine now that DNA §AX-A reports null; reconsider TAS1R3 as the taste "master gene". | `vp_sns_engine.py`, `01-…` | should-fix |
| Needs author | Regrade the cube-root exponent to [F] and update `_decl.json` counts. | `07-…`, `_decl.json` | nit |
| Needs author | Clarify the SOX2 promoter vs locus γ window across dna/sensory. | `12-…`, dna | nit |
| **No action** | Classical anchors (Greenwood, reduced eye, D/mm, canal, VOR) are correct and honestly graded. | `05-`, `06-`, `08-` | — |
| No action | Magnitude firewall is intact: clinical items are literature [L] under a banner, with no framework dose. | `11-`, `12-` | — |
| No action | Determinism, gates, stress tests and integrity all pass; the vendored γ equals the DNA source. | `repro/sensory_organ/` | — |
