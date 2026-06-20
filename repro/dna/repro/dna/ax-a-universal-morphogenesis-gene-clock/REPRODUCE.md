# REPRODUCE — verify the whole package with one command

This package is governed by the same VP-SPEC C3 no-tuning rule as
`neuro_emergence_chain_integrated v1.9`: **every constant is a measured input
(locked + cited) or a derived value — never a number chosen to hit a target.**
The single-entry, bit-for-bit verification backbone (`verify_all.py`) certifies
the whole package — the twelve morpho gates, the five folded-in emergence gates,
the source-integrity pin, and the cross-session fidelity baselines — in one run.

Current state: **v12.4** (post-Phase-7 morphogen length-scale cross-validation).
Earlier verify-count milestones (11/11 → 14/14 → 18/18 → 19/19 → 20/20) are
recorded in `VERSION`; this file always describes the *current* package.

## Verify everything (from this directory)

```
python3 verify_all.py
```

Expected: `OVERALL: PASS (20/20 checks)` —

```
[1] gate suite          12 morpho gates, each OVERALL: PASS (5/5)
    verify_gene_clock        one-switch <1e-12, order = argsort(spinodal(γ)), RMS→0.07, Chamfer→0
    verify_morpho_plus       4 organisms (head/bird/quadruped/fish), 42-γ superset bit-identical
    verify_adipose           one-switch, 59-γ superset, gene×env monotone, lean baseline bit-for-bit
    verify_dev_timing        honest NULL (ρ=−0.018, perm p=0.99), grade == evidence
    verify_timing_predictors 6-predictor composition battery, all [O], floor 7.9e-4 disclosed (n=7)
    verify_dev_timing_wide   n=10 widened test (7 locked + 3 new [V] masters), both tests [O];
                             DP exact-permutation engine validated vs brute force at n=7,8,9;
                             floor lifted to 2.2e-6 -> real null, not a power artifact
    verify_dev_timing_robust n=10 null hardened: stage +/-1 robustness (min perm p 0.119)
                             + leave-one-out jackknife (no fold flips, power retained);
                             MYF5->myotome investigated, too soft to lock (documented)
    verify_morpho_decomposition  CAPSTONE: how much of SHAPE does DNA fix? variance decomposition
                             of body shape -> genetic H2=0.51 (published twin BMI 0.48-0.63),
                             H2 falls to 0.10 as environment widens (population-dependence);
                             identical-twin DNA core bit-identical, surplus life +37% volume/+25% face
    verify_life_course       one continuous R19 fold (TIME×ENERGY), lean baseline bit-for-bit
    verify_organ_timing      per-organ emergence order from γ [V]; realized timing [O]
    verify_organ_anatomy     coarse-to-fine organ read-out, convergence + determinism
    verify_heart_substages   8 cardiac sub-stages, one-specifier-per-milestone [F] documented

[1b] emergence gate suite   5 folded-in gates (systemic-recovery fold-in; OVERALL: N/N -> PASS)
    verify_emergence            emergence_heart        7/7  (sha 939ae9924a6c)
    verify_emergence_organs     emergence_organs       6/6  (sha 40225433a67a)
    verify_emergence_trajectory emergence_trajectory   7/7  (sha b2b34a770f5a)  λ-scale [L], form [F], anatomy [O]
    verify_emergence_organs_wide emergence_organs_wide 8/8  (sha d82eeb925973)
    verify_emergence_morphogen  emergence_morphogen    8/8  (sha 01b0b6ea8b10 / band 4ea1c7b4111c)
                                first-principles band λ=√(D·τ)=[18.97,189.74] µm vs 6 measured
                                morphogen gradients; geom-mean factor 1.91, 5/6 in band, independent
                                set (Bicoid/Nodal/Shh) 3/3 in band -> REGIME-level [L]-grounded;
                                Wingless (~6 µm) named as a band miss, not excluded

[2] source integrity    sha256 pin over every governed module AND every measured
                        input (the γ tables + Carnegie stages), 87 files, drift 0.
[3] fidelity            gate-regenerated results/*_verify.json == frozen
                        repro/morpho/expected/*.json, leaf drift 0 (12 morpho baselines).
[3b] emergence fidelity each emergence gate's (PASS count + result-hash) fingerprint ==
                        frozen emergence_gate_baseline.json (5 fingerprints match).
```

The single-entry tally is **20 = 12 morpho gates + 5 emergence gates + 1 source
integrity + 1 morpho fidelity + 1 emergence fidelity**.

## What each layer buys (and why all are needed)

- **[1] / [1b]** is the science: the gates that prove the switch, the order law,
  the convergence, the honest timing null, the life-course coupling, and (Phase 7)
  that the model's first-principles length band matches real morphogen gradients
  with no fit.
- **[2]** is the integrity pin. The behavioural gates cannot see an edit that
  leaves *this input's* numbers unchanged (a comment, a refactor, a change that
  only bites on other inputs). The sha256 pin does. It is also the enforcement
  of the standing invariant **"the measured γ tables stay bit-for-bit, never
  tuned"** — touch a γ and `[2]` fails.
- **[3] / [3b]** is the cross-session anchor. A single run can be internally
  deterministic (2×sha, which each gate already checks) yet still have drifted
  from the released numbers. `[3]`/`[3b]` diff against a frozen baseline so a
  silent numeric drift is caught even when the run is self-consistent.

## Runtime note (honest, from VERSION §freeze)

The full `verify_all.py` does not complete in a single process inside a tight
runtime budget — `verify_dev_timing_wide` alone runs ~261 s. Every gate is
deterministic, so a baseline may be frozen **decomposed** (each gate run
individually to completion, its output cached, the canonical `freeze()` driven
on the cache); the pins produced are byte-identical to an inline `--freeze`.
This is a runtime accommodation, not a methodological shortcut.

## After an INTENTIONAL, gate-passing change — re-freeze deliberately

```
python3 verify_all.py --freeze     # refuses unless all gates pass, then
                                   # re-records expected_sha256.json + expected/
```

Freezing is always a deliberate act (mirrors neuro's "delete the key, run once
to record, run again to confirm"). Never freeze to make a red gate go green —
under VP-SPEC a green `verify_all` certifies that the *released* numbers were
reproduced and that nothing measured was silently edited, not that a new number
was made to look acceptable.

## Inspect the pinned set

```
python3 verify_all.py --list       # 87 governed files (engine + verify + data)
```
