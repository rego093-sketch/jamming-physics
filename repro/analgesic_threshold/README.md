# analgesic_threshold_logic — v2.0

A free, falsifiable **target hypothesis** for non-opioid analgesia, built in the jamming-physics
idiom: a reproducible DNA read + a gated reproduction harness + an honest [V]/[F]/[O] ledger.

**Thesis.** The nociceptor's pain gate is a firing threshold; analgesia is a controlled upward
shift of it. From real promoter DNA this reads the threshold structure of the genes that build,
gate, and sensitise the pain fibre and proposes — *as a hypothesis only* — where and in which
direction to intervene. **No molecule, no dose, no efficacy claim, no medical responsibility.**
See `CONSTITUTION.md` and the disclaimer in `docs/analgesic/for-patients-and-public/`.

**What v2.0 adds over v1.0**
- Expands the read from **7 → 27 targets** on the identical locked pipeline (corr(γ,GC)=0.99898).
- A **three-lever frame**: L1 reduce the inward (excitatory) current · L2 increase the outward
  (K⁺) current · L3 remove the up-stream sensitising drive. Every target is placed in its lever.
- A **burden-weighted target prioritisation** (declared weights, cited 1–5 tiers; ranks targets,
  never drugs/doses/efficacy; γ-|h_sp| carried alongside but never folded into the score).
- An **L3-honesty gate** that fails the build closed unless every L3 (NGF/CGRP) mechanism link is
  graded `[O]` cited biology, never derived from the read.
- A **precision local-anaesthesia** map: nociceptor-selective entry port (TRPV1/TRPA1) × charged
  firing-threshold raiser → differential (pain-selective) block, anchored to Binshtok–Bean–Woolf
  (Nature 2007). All differential-block magnitudes remain `[O]`.

## Reproduce (one command, offline with the bundled cache)
```
python3 repro/run_all.py        # -> OVERALL: PASS (11/11 checks)
```
Runs the M1–M6 and M8–M12 gates and verifies determinism (drift 0). The 22 expanded-target reads
re-derive offline from `repro/02-read-nav-channels/nav_promoters.cache.json`; NCBI is contacted
only if that cache is absent.

## Layout
```
docs/analgesic/index.html               hub (answer-first overview + contents + cross-links)
docs/analgesic/{slug}/index.html        40 self-contained §6 pages: how-to-read · 5 lever pages ·
                                        27 per-target pages · prioritisation · precision · proposals ·
                                        falsification · grading · for-pharma · for-patients
docs/assets/css/site.css                canonical VP-SPEC stylesheet (+ analgesic grade badges)
docs/robots.txt · sitemap.xml · llms.txt   C4 access layer (7 bots, 41 URLs, <5KB summary)
docs/analgesic/_meta.json               summary card (§9): layout + 27 target reads
build_multipage_analgesic.py            deterministic generator (γ/|h_sp| byte-faithful → drift 0)
CHANGELOG_v2_0_multipage.md             single-file → multi-page conversion log
CONSTITUTION.md                         free / DOI / proposal-only / no medical responsibility
IRREPRODUCIBILITY_LEDGER.md             every [O] item (v2.0: 9 open classes)
VP_SPEC_v1_8.md                         governance spec (binding for this build)
repro/_engine/                          locked engines (dna_interpreter, vp_neuro_engine, deps)
repro/_inherited_data/                  inherited nociceptor γ + cached promoters
repro/01-inherit-reverify/              M1: re-verify inherited reads (drift 0)
repro/02-read-nav-channels/             M8: read the 22-target expanded set + gate (corr/drift/provenance)
repro/03-threshold-map/                 M9: the three-lever 27-target threshold map
repro/04-channelopathy-anchor/          M4: measured biology fixes the direction
repro/10-burden-prioritisation/         M10: burden/unmet/druggability-weighted target prioritisation
repro/11-l3-honesty/                    M11: fail-closed — every L3 mechanism link graded [O]
repro/12-precision-local-anaesthesia/   M12: nociceptor entry-port × charged-blocker differential-block map
repro/05-intervention-logic/            M5: the proposal (P1–P6) + fail-closed forbidden-claim scan
repro/06-falsification/                 M6: a named falsifier per proposal (incl. P6 precision)
repro/run_all.py + expected_sha256.json M7: harness + 10 frozen hashes
reports/                                gate snapshots
```

## Discipline (enforced by gates)
No tuning (every number measured or derived; prioritisation weights *declared*, not reverse-fit);
the forbidden-claim scanner fails the build closed if any proposal, module, or whitepaper section
drifts into a dose / efficacy / safety / treatment / synthesis claim (it scans the proposal, all
four new module outputs, and the precision whitepaper section, with a negation guard so firewall
text never false-positives); the L3-honesty gate forbids presenting any NGF/CGRP mechanism as
derived; γ stays blind to on/off (reads, not traits); every measured-biology statement is cited.
**The firewall is non-negotiable: γ reads promoter switch-threshold structure and is never equated
with a channel voltage, a potency, a dose, an in-vivo selectivity, or a clinical effect.**

**Scope:** analgesic *development logic* only — free, public-benefit, proposal-only. Disease
mechanism itself is out of scope. **No medical responsibility.**
