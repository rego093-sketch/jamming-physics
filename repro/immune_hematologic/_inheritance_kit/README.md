# `_inheritance_kit/` — portable analgesic discipline kernel

Reference implementation of the five fail-closed discipline gates inherited from
`analgesic_threshold_logic_v2_0` (DOI **10.5281/zenodo.20733420**). These are the **immune instantiation**
shipped as a template — copy `_discipline/` into a target package's `repro/` and re-tune the three surfaces
below. The gate logic, harness, determinism freeze, negation guard and self-tests are copied unchanged.

Full procedure: see `../ANALGESIC_TECHNIQUE_INHERITANCE.md` §3–§4.

## Three tuning surfaces (everything else stays byte-identical)

1. **D1 `inherit_reverify.py`** → `MASTER_ORGAN` = the target package's gene→organ anchors; it imports the
   package's existing `inherited/gamma_pipeline.py` + `vp_substrate.py`. No new γ derivation. Must report
   drift 0.
2. **D2 `burden_prioritisation.py`** → `TARGETS` = the package's **diseases** with **cited** ordinal
   burden/unmet tiers. Targets are diseases, never agents/doses. Weights stay the declared default unless the
   package states a new policy (log it in that package's ledger). γ/|h_sp| are context, NEVER scored.
3. **D5 `forbidden_claim_scan.py`** → `PATTERNS` (forbidden posology/synthesis/novel-efficacy/safety) +
   `EXCLUDE_KEY_RE`/allow-list for that package's corpus. **Pre-scan the docs before tuning.** Keep the
   negation guard + both self-tests.

D3 `external_mechanism_honesty.py` binds to the package's `therapy_report(...)` keys; D4
`falsification_register.py` lists the package's load-bearing claims + framework falsifier.

## After tuning

```
rm -f _discipline/expected_sha256.json            # drop the template's frozen hashes
python3 repro/_discipline/run_discipline.py        # writes fresh frozen hashes
python3 repro/_discipline/run_discipline.py        # drift 0
python3 repro/_discipline/run_discipline.py        # drift 0 (confirm twice)
```

Then wire `discipline_ok()` into the package's `research_gate()` (fold into `all_green`, fail-closed on import
error) and add a `[N] INHERITED DISCIPLINE` section to its `run_all.py`; re-sign `research_complete.json`.

> The template still contains immune content (master genes, immune disease targets, immune firewall patterns).
> It runs as-is **only** inside the immune package; in any other package the three surfaces above MUST be
> re-tuned or the gates will (correctly) fail closed.
