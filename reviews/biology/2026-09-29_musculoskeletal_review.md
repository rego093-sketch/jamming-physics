# musculoskeletal — light review (2026-09-29)

## Summary
- R1 compared the hub and §1–§6 claims with the cited data. R2 ran `vp_msk_dynamics.py` (T1, T3, T5) from a scratch copy of `repro/musculoskeletal/` with `python3 -B`. `run_all.py` printed the emergence, stress, disease, treatment, analgesic and oncology batteries (all PASS), then hit the 120 s limit in the gates step.
- Every printed number matches the pages:
  - γ: RUNX2 1.2414, TBX5 1.4392, SOX9 1.4598, MYOD1 1.4933;
  - spinodal 0.5324;
  - fusion 25 Hz, and 50/25/13 Hz for 25/50/90 ms;
  - τ 59.75 s and recovery 0.9743.
- Magnitude firewall: clean. The treatment chapters name drugs by mechanism only. There is no dose, concentration or schedule.
- The volume used [F]/[V] on biological claims throughout: 46 section badges on the hub, and about 150 labels across the 28 chapters.

## Findings
1. **γ-order graded [V].** Severity: high.
   - Where: hub §5; `docs/musculoskeletal/05-growth-plate-ordering-gamma-rank/`; T4 in `repro/.../vp_msk_dynamics.py` lines 241–268.
   - "γ-rank reproduces limb→cartilage→muscle" was graded [V].
   - The pass is computed over 3 of the 4 genes. Bone (RUNX2), which ranks first, is excluded from the pass condition. A 3-gene match is 1 of 6 possible orders.
   - Observation conflict: the somitic myogenic programme starts before limb Sox9 condensation.
     - Myf5 from about E8 (Ott 1991).
     - Myogenin about E8.5 and MyoD about E10.5 (Sassoon 1989).
     - Sox9 in limb condensations about E10.5–11.5 (Wright 1995).
   - The order holds only within the limb bud.
   - §1 also derives "relative size ∝ γ^1.5".
2. **T1 fusion "25 Hz" is a grid and criterion artefact.** Severity: medium.
   - Where: hub §2; `02-force-frequency-.../`.
   - 25 Hz is the first grid point (…20, 25, 30…) where ripple < 0.10, at the 50 ms input contraction time.
   - On a 1 Hz grid the same code gives 22 Hz. A 0.05 or 0.20 criterion gives 32 or 15 Hz.
   - "Fusion tracks 1/τ" holds by construction: the kernel depends only on u/τ, so f·τ ≈ 1250 ms·Hz.
3. **T5 fatigue τ 59.75 s is the 60 s input recovered by a log-linear fit.** Severity: medium.
   - Where: `06-muscle-fatigue-.../`.
   - This is self-consistency, not a test.
   - The 52 % loss equals the depth input 0.55 × (1 − e⁻³).
   - The 97 % recovery holds for the 180 s rest window. The code gives 81 / 93 / 99.7 % after 60 / 120 / 300 s.
4. **T3 Wolff "[F]".** Severity: low.
   - The spinodal 0.5324 = 2(γ/3)^1.5 is algebra.
   - The threshold and hysteresis come from the cubic. Their reading as bone yield is interpretation. The Frost setpoint [L] stays.

## What I changed (docs/musculoskeletal only)
- **Hub.** Added the reading-rule note after `<h1>`, and rewrote these entries:
  - the intro now says "read from γ", with building marked [O] and a link to dna §RB;
  - §2 now states its input dependence and gives 1/τ as a consistency check;
  - §4 gives the spinodal as algebra;
  - §5 is now interpretation, with [O] and the embryology citations;
  - §6 now states its input dependence.
- **Chapter pages.**
  - §1: the spinodal and size columns are labelled consistency and interpretation, with [O] per dna §RB.
  - §2: the grid and criterion dependence of 25 Hz, and 1/τ as consistency.
  - §5: the ranking is labelled code output and interpretation; the observation paragraph was added; the post-hoc three-gene subset is noted.
  - §6: τ is labelled a round trip; the loss and recovery values are tied to their inputs.
- **All pages, relabelled outside the existing lt-note asides:**
  - [V] → code output;
  - [F] → consistency;
  - γ "[V] measured" → observation;
  - "sim-verified" → "simulated";
  - badges now use class `g-hypothesis`.
- No number or lt-note was removed.
