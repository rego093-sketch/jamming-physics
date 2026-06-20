# HANDOFF — v12 (cardiac single-organ deep dive) → next

This package is **self-verifying** from a clean extract. Start here.

## What v12 added (one paragraph)

The heart's own developmental program was resolved into 8 crisp sub-stage milestones, each tagged
with its canonical specifier master gene, each gene's **real γ** fetched by the **identical**
NCBI→SantaLucia pipeline, and the **same falsifiable gene-clock timing test** run on this one
coherent, textbook-staged system — the fair, single-system version of the v10 organ-timing test.
**Add-only, no engine edit.** Six new files (2 code, 1 fetch, 3 locked/cached data), one new gate
(11→12), source pin 63→69, `verify_all.py` **PASS 14/14**.

## The honest result (do not soften, do not overclaim)

`γ` (promoter thermodynamic stiffness) does **not** predict cardiac sub-stage timing:
**Spearman ρ=+0.071, exact permutation p=0.882 (n!=40320), Pearson r=−0.030 → grade [O].**
The cardiac master **NKX2-5** (first event in vivo, CS9) is ranked near-**last** by γ; **MEF2C**
(late septation) ranked **first** — γ gets the anchors backwards. Robust to ±1 CS jitter (max ρ=0.395
< ρ_crit=0.714 → 0% reach significance) and provably non-blind (synthetic-ordered γ → ρ=+1.000).
**This sharpens, on the best single system, the project's central finding: γ fixes the structure/order
of anatomy deterministically [V] but is orthogonal to developmental timing [O].** It is a
recognized-worthy *negative* (a falsifiable prediction, honestly reported as not confirmed), not a
positive claim.

## Invariants you must not break (the governance)

1. **No engine edit / no fork.** `organism/core.py` and every existing `code/*.py` are byte-identical
   across v10→v12 (integrity check proves drift 0). v12 only *adds* files.
2. **Every constant is measured-input or derived, never tuned.** γ is read-only (NCBI promoters);
   staging is locked/cited/γ-independent; the gate enforces **grade==evidence** (a [V] is earned only
   by a significant positive correlation, else [O]).
3. **Source pin = 69 files** (`expected_sha256.json`). **Fidelity = 12 baselines**
   (`repro/morpho/expected/*.json`), leaf drift 0. **Gate suite = 12 gates**, each 5/5.

## RUNTIME NOTE (important — read before running `verify_all.py`)

The full suite is **~330 s**, which **exceeds a single 300 s tool/shell call** (the
`verify_dev_timing_wide` gate alone is ~158 s). In a capped shell it will be killed mid-run — that is
a **timeout, not a failure**. Verify in two equivalent pieces (logically identical to `verify_all.py`):

```bash
# piece A — run each gate individually (each prints OVERALL: PASS (5/5) and regenerates its results/*.json)
for g in gene_clock morpho_plus adipose dev_timing timing_predictors dev_timing_wide \
         dev_timing_robust morpho_decomposition life_course organ_timing organ_anatomy heart_substages; do
  PYTHONPATH=code python3 code/verify_$g.py >/dev/null && echo "PASS $g" || echo "FAIL $g"
done

# piece B — verify_all.py's OWN integrity [2] + fidelity [3] layers
python3 - <<'PY'
import json,os,sys; sys.path.insert(0,os.getcwd()); import verify_all as V
frozen=json.load(open(V.SHA_FILE)); cur=V.compute_shas()
drift=(set(cur)^set(frozen))|{f for f in set(cur)&set(frozen) if cur[f]!=frozen[f]}
print("[2] integrity:",len(frozen),"files, drift",len(drift),"->","PASS" if not drift else "FAIL")
ok=all(not V.diff_json(json.load(open(os.path.join(V.EXPECTED_DIR,j))),
                       json.load(open(os.path.join(V.RESULTS,j)))) for _,j in V.GATES)
print("[3] fidelity:",len(V.GATES),"baselines ->","PASS" if ok else "FAIL")
PY
```

On an uncapped machine, `python3 verify_all.py` runs end-to-end and prints `OVERALL: PASS (14/14)`.

## Next levers (in priority order; same as v11, refined by the cardiac result)

1. **Different measured modality for timing — the ONLY path to a positive [O]→[V].** γ is promoter
   *thermodynamics*; timing is GRN/signaling *dynamics*, so the null is mechanistically expected. A
   timing-relevant observable — **expression-onset rank** (bulk/scRNA developmental atlas) or
   **chromatin-accessibility onset** (ATAC) per master gene — could actually correlate with staging.
   Status: **data-blocked** (no locked, citable, non-cherry-picked onset table in-package yet). Curate
   one the way `heart_substages.json` was curated (locked, cited, frozen, modality-independent) and run
   it through the *same* apparatus. **Do not** swap it in to chase significance — report whatever it says.
2. **Widen the crisp single-organ set** — repeat this exact fair test on another textbook-staged
   organ (e.g. limb, neural tube, somites/kidney). Each is power-limited (n small), but several
   independent single-system nulls would be a strong, clean meta-statement.
3. **Per-organ measured shape priors** — replace the rough ellipsoids in `organ_anatomy.py` with
   measured organ aspect ratios (polish/geometry; would lift absolute-size grade from [O], not a
   timing claim).
4. **`dna_vp` merge** — fold the morphogenesis γ-readout into the broader DNA→phenotype value-pipeline
   (integration/engineering, not new science).

## Files map (v12 delta)

```
code/heart_substages.py            # schedule=argsort(spinodal(γ)); calibrate() test; non-blindness; ±1 jitter band
code/verify_heart_substages.py     # gate PASS 5/5 (one switch · locked+identical-pipeline · grade==evidence+robust · falsifiable · deterministic)
code/data/fetch_heart_gamma.py     # identical NCBI→SantaLucia pipeline, 8 cardiac genes
code/data/heart_gamma.json         # real cardiac-gene γ (NKX2-5 == organ_gamma.json)
code/data/heart_promoters.cache.json  # cached promoter sequences → γ reproduces offline
code/data/heart_substages.json     # LOCKED + CITED cardiac Carnegie staging (γ-independent, frozen)
repro/morpho/expected/heart_substages_verify.json   # fidelity baseline
VERSION (→12.0) · CHANGELOG_v12_heart.md · LEDGER_heart.md · this file
expected_sha256.json (→69 files) · verify_all.py GATES (→12)
```
