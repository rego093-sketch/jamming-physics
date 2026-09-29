# analgesic_threshold — light two-reviewer review (2026-09-29)

Scope: the hub and 40 pages in `docs/analgesic_threshold/`, and the package in `repro/analgesic_threshold/`. The volume maps 27 nociception genes to a γ read and |h_sp|, sorts them into levers L1/L2/L3, and gives proposals P1–P6.

## R1 — claims against data, and the magnitude firewall
- **Firewall is clean.** There is no dose, concentration, regimen or effect size. Named agents (suzetrigine, QX-314, ziconotide, gefapixant) are cited observations only. The "≥"/"%" scan finds only the value "100%", which is not clinical.
- **[V] is used for the γ read.** "read [V]" appears 27 times on the hub and on every target page. The read is a deterministic code output from the promoter window and the SantaLucia table. It is not a test against external data. Relabel it "code output".
- **corr(γ,GC) = 0.99898 is presented as verification.** It is a property of the SantaLucia table itself (random sequence gives about 0.9996). It is a consistency check, not a finding.
- **[F] "forced by the reads" is used for three different kinds of claim:**
  - (a) Order by |h_sp|. This is a monotone function of γ, so it is a code output or consistency property.
  - (b) Lever placement and direction. These come from cited channel biology and agents, not from γ, so they are interpretation anchored to observation.
  - (c) The mechanism, for example the Binshtok 2007 differential block. This is an observation extended by interpretation.
- **Prioritisation is graded [F], but it depends on editorial weights.** The ranking uses declared weights (0.40/0.35/0.25) on cited 1–5 tiers. It is a code output that depends on those weights.
- **Falsification: untested hypotheses P1–P6 carry [F].** They are interpretations or hypotheses. The page's own framework falsifier, "does γ track expression-switch behaviour?", is correctly [O].
- **Lever pages overstate γ's role.** They say "the promoter reads place each gene in lever L1". In fact γ places the gene on the |h_sp| scale, and the lever comes from the channel's known physiology.

## R2 — code runs (python3 -B, scratch copy, timeout 120 s)
- `repro/run_all.py`: all 10 module gates PASS. The overall result is FAIL because of hash drift in `05-intervention-logic/expected/claim_scan.json`. The cause is that the forbidden-claim scanner no longer finds the `docs#proposal` and `docs#precision` sources after the move of `docs/`. The published pages are therefore not scanned by the volume's own scanner. This is the same pattern as the sensory volumes' gate paths.
- `03-threshold-map/expected/threshold_map.json`: all 27 γ and |h_sp| values match the hub exactly, with 0 mismatches. Spot checks of |h_sp| = (2/(3√3))γ^1.5 and barrier = γ²/4 hold by algebra (SCN9A 0.638545 / 0.49098; CACNA1H 0.8052 / 0.668879).
- `02 nav_gate.json`: corr = 0.998978 over 27 genes, drift 0.

## Edits made (docs only; no numeric change)
- Hub: added the reading-rule note. Changed "read [V]" to "read: code output" (27 times). Relabelled the grading contents line. Annotated corr(γ,GC) as table-intrinsic.
- target-scn9a, target-scn10a and target-ngf: read changed to code output; order changed to code output (consistency); lever changed to interpretation; mechanism changed to observation + interpretation; page badge changed. The other 24 target pages share this template and were not edited.
- grading-and-honesty and how-to-read-this-map: the grade legend is relabelled (code output / consistency / observation / interpretation / [O]).
- prioritisation: [F] changed to "code output (depends on declared weights)".
- precision-local-anaesthesia: [F] changed to observation (Binshtok 2007) + interpretation.
- falsification: [F] changed to interpretation.

## Open for the author
- Apply the same relabel to the remaining 24 target pages and the 5 lever pages, which use the same template.
- Repoint the claim scanner to `docs/analgesic_threshold/`.
- Run `tools/record_page_notes.py`.
