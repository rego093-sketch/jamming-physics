# Inherited technique — `analgesic_threshold_logic_v2_0` DISCIPLINE kernel

**Source technique:** `analgesic_threshold_logic_v2_0` · concept DOI **10.5281/zenodo.20733420** (CC BY 4.0).
**First applied in:** `immune_hematologic_vp_site` v0.12.0 (this package), under `repro/_discipline/`.
**Status:** inherited and ACTIVELY APPLIED here; package-agnostic template provided in `_inheritance_kit/` for
the rest of the physiological suite.

This file is the canonical spec of *what was inherited* and *how to drop it into another VP physiological
package*. It exists so the technique is no longer "missing from the roadmap" — it is a first-class, reusable
governance layer. Read together with `FUTURE_WORK.md` (v0.12.0 entry) and `IRREPRODUCIBILITY_LEDGER.md`
(the two declared `[O]` inputs the layer introduces).

---

## 1. What the analgesic technique actually is

The analgesic package is a **DNA-grounded threshold-engineering map with a hard discipline firewall**. Its
transferable core is NOT its nociceptor content — it is the *governance pattern* that keeps a
"how-to-intervene" volume honest:

- targets are ranked by **declared** clinical burden, never by the model's internal numbers;
- the DNA read (γ = −mean SantaLucia-1998 nearest-neighbour stacking ΔG37) is **re-derived offline, drift 0**;
- external mechanism efficacy is graded **cited-`[L]`**, never silently promoted to derived `[V]`/`[F]`;
- every load-bearing claim carries a **named, measurable falsifier**;
- a **fail-closed firewall** forbids dose/regimen/synthesis/novel-efficacy/safety language.

In the analgesic package these are modules M1, M10, M11, M6, M5; the harness `repro/run_all.py` runs them in
dependency order with the firewall last and freezes determinism hashes.

## 2. The five inherited gates (immune instantiation)

All under `repro/_discipline/`, run by `run_discipline.py` (D1→D5, firewall last), determinism-frozen in
`expected_sha256.json` (5 hashes, drift 0), wired into `repro/_verify/gates.py::research_gate()` and
`repro/run_all.py` §[7] so the research battery **fails closed** without them.

| gate | file | analgesic origin | what it asserts (fail-closed) |
|---|---|---|---|
| **D1** inherit-reverify | `inherit_reverify.py` | M1 | re-derive the master-gene γ offline + recompute the R19 spinodal/barrier; every value drift 0 vs the byte-exact NCBI-verified cache |
| **D2** burden-prioritisation | `burden_prioritisation.py` | M10 | rank **disease targets only** by DECLARED weights + ordinal tiers; γ/|h_sp| carried as context, NEVER scored; no drug/dose ever ranked |
| **D3** mechanism-honesty | `external_mechanism_honesty.py` | M11 | every therapy lever's clinical anchor is graded cited-`[L]`, never derived `[V]`/`[F]`; honest-limit/open-obstacle `[O]` + "does not invent" present |
| **D4** falsification | `falsification_register.py` | M6 | a named, measurable falsifier for every load-bearing claim + the framework |
| **D5** forbidden-claim firewall | `forbidden_claim_scan.py` | M5 | forbid numeric dose/regimen, synthesis routes, novel-VP-efficacy, safety claims; negation-guarded; require disclaimers; allow cited-`[L]` cures + dose-RESPONSE biology |

**Two declared `[O]` inputs** the layer introduces (logged in the ledger): the D2 weight set
`{burden 0.40, unmet_durability 0.40, tractability 0.20}` + ordinal tiers, and the D5 firewall pattern list.
Both are explicit governance policy, not substrate-derived; they change ordering/scope only, never any
`[V]`/`[F]` number.

## 3. Per-package tuning surface (what changes between packages)

The **gate logic is byte-identical** across packages. Only three things are re-tuned:

1. **D1 master map** — the package's own gene→organ anchors and its offline γ pipeline / verification cache
   (e.g. immune: FOXN1/PAX5/RUNX1/TLX1; circulatory: SIX2/HHEX…; each package already ships these in
   `inherited/`). D1 imports the package's existing `gamma_pipeline` + `vp_substrate`; no new derivation.
2. **D2 target table** — the package's disease-target list with **cited** ordinal burden/unmet tiers. Targets
   are diseases, never agents. Weights stay the declared default unless the package states a different policy.
3. **D5 firewall pattern list + allow-list** — the package's editorial boundary: which posology/synthesis/
   efficacy/safety strings are forbidden, and which domain-legitimate phrases (e.g. "dose-response" as
   Kramers biology, cited-`[L]` cures) are explicitly allowed via the negation guard + exclude keys.

Everything else — the harness, the determinism freeze, the `gates.py`/`run_all.py` wiring, the self-tests — is
copied unchanged.

## 4. Drop-in procedure for another physiological package

> Apply this to bring the discipline layer into `circulatory_vp_site`, `musculoskeletal_vp_site`, the
> hemodynamic/homeostasis package, the digestive/metabolic package, or any future volume.

1. `cp -r _inheritance_kit/_discipline <pkg>/repro/_discipline` (generic templates).
2. **D1**: point `MASTER_ORGAN` at the package's gene→organ anchors; confirm it imports the package's existing
   `inherited/gamma_pipeline.py` + `vp_substrate.py`. Run `python3 repro/_discipline/inherit_reverify.py` →
   must report drift 0.
3. **D2**: replace the `TARGETS` table with the package's diseases + **cited** ordinal tiers. Keep weights at
   the declared default (or state a new policy in the package ledger). Targets must be diseases only.
4. **D3/D4**: bind D3 to the package's `therapy_report(...)` keys (lever anchors, honest_limit, open_obstacle);
   list the package's load-bearing claims + framework falsifier in D4.
5. **D5**: tune `PATTERNS` (forbidden) + `EXCLUDE_KEY_RE`/allow-list to the package's corpus; **pre-scan the
   docs first** (the immune corpus was clean for numeric posology/synthesis/novel-efficacy/safety — verify the
   same before tuning). Keep the negation guard and the two self-tests.
6. Freeze: delete any stale `expected_sha256.json`, run `python3 repro/_discipline/run_discipline.py` once to
   write the frozen hashes, then run it **twice more** → drift 0 on both.
7. Wire: add `discipline_ok()` to the package's `research_gate()` (fold into `all_green`, fail-closed on import
   error) and a `[N] INHERITED DISCIPLINE` section to its `run_all.py`. Re-sign `research_complete.json`.
8. Record: add a "DELIVERED — inherited analgesic discipline" entry to the package's `FUTURE_WORK.md`, log the
   two declared `[O]` inputs in its ledger, bump VERSION, re-zip, fresh-extract test.

## 5. Cross-suite application plan (기존 연구사례 적용 계획)

Inherit, in this order (most therapy-content first, since the firewall earns the most there):

| package | version | priority | notes |
|---|---|---|---|
| `circulatory_vp_site` | v0.7 | **1** | DNA-grounded organ emergence already present (SIX2/HHEX); rich therapy surface → firewall high-value |
| `musculoskeletal_vp_site` | v0.4 | 2 | 18 hard disease targets (T1–T17) → D2 target table maps directly |
| hemodynamic / homeostasis | v0.2 | 3 | set `PHASE=writing` then inherit; smaller therapy surface |
| digestive / metabolic | (next) | 4 | apply at first writing build; D2 over the tiered GI disease roadmap |

Each inheritance is mechanical per §4; only the three tuning surfaces (§3) differ. The gate code and the
honesty guarantees are identical everywhere, which is the point — one audited discipline kernel, many volumes.

## 6. Cross-cutting: speed optimisation (✓ delivered in v0.13.0)

The two speed items are now implemented, byte-identical (no frozen hash changed, no gate relaxed):

- the five gates run **in-process** via `runpy.run_path(..., run_name="__main__")` instead of five subprocess
  interpreters — identical `__main__` code, so each `expected/*.json` is byte-for-byte the same, but the
  interpreter startups are gone and `gamma_pipeline`/`vp_substrate` load once and are reused across gates;
- `run_discipline.run()` **memoises its result for the process** and `gamma_pipeline.recompute_all()`
  **memoises the γ recompute** (deep-copy on return), so a battery that asks for the discipline result from
  both `run_all §[7]` and `research_gate` pays for one pass, not two.

Measured: discipline overhead ≈16 s → ≈10 s; full battery ≈131 s → ≈126 s. When porting to another package,
copy `run_discipline.py` as-is — the in-process harness is package-agnostic.

Hard constraint preserved for any future battery-level pass: **no frozen hash may change and no gate may be
relaxed.** The remaining large cost is the stochastic stress battery (≈115 s, already down from 295.6 s); reduce
it only by vectorising WITHOUT changing the RNG stream.

---

*Inherited from `analgesic_threshold_logic_v2_0` (DOI 10.5281/zenodo.20733420). This package:
`immune_hematologic_vp_site` (concept DOI 10.5281/zenodo.20755280), author Young Jae Lee
(ORCID 0009-0002-7535-8245), CC BY 4.0.*
