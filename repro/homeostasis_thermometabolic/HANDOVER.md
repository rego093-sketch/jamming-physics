# HANDOVER — homeostasis_thermometabolic_vp_site (v0.6.0 → next)

State for the next session. Resume immediately; the package is self-contained.

## Where the package stands

v0.6.0 is **research-signed-off and site-landed**. The endotherm-vs-ectotherm foundation (the heart) is
complete and validated, **all 16 stress targets are green** (RT1–RD4 + RH8 + RH9), the disease and
restoration layers are built and gated, the new **precision-routing layer** is built and its firewall is
PROVEN, and the canonical multi-page VP-SPEC v1.8 site (**1 hub + 32 chapters**) regenerates with drift 0.
PHASE is `writing`; the writing gate is unlocked. The package ships as one zip.

Key hashes (recompute to verify nothing drifted): engine sha256 `08f50d6d…` (**byte-identical to v0.5.0** —
the engine did not change); site sha256 `3bb5657b…` (new, two chapters added); precision-routing sha256
`21021e79…` (new module's 2×sha256 self-check); vendored substrate sha256 prefix `5664800b…` (must stay
byte-identical); cross-species panel `crossspecies_thermo_panel.json` byte-identical (untouched).

## What changed this session (the precision-routing layer — HANDOVER #3, executed)

The v0.5.0 HANDOVER's named forward priority #3 (the **optional precision layer**) is now executed and
signed off — done **fully self-contained, with no external data, no panel mutation, no live fetch, and no
change to the engine**. It is the analgesic package's **local-anaesthesia mirror**: the analgesic work
separates a SYSTEMIC threshold-raiser (acts body-wide) from a PRECISION local block (confined to one nerve's
territory); the same distinction, re-read for the setpoint-restoration levers, asks WHERE each lever's node
acts — one tissue COMPARTMENT or many.

- **A cited compartment routing map.** Each restoration target is placed on a CITED anatomical compartment
  map and classed **PRECISION** (1 compartment), **REGIONAL** (2–3), or **SYSTEMIC** (≥4, or a distributed
  immune/stromal node with no single locus) by a **parameter-free** rule on the cited compartment count.
  **Result — nodes split 2 PRECISION / 5 REGIONAL / 2 SYSTEMIC.** The two clean precision routes are
  UCP1→brown fat (BAT) and MC4R→hypothalamus; INSR (the ubiquitous insulin receptor, 4 dominant
  compartments) and TNF (a distributed inflammatory program) are honestly SYSTEMIC — restoration cannot be
  confined to one place. Three NAMED routes span the spectrum: **BAT-targeted** (the cleanest precision),
  **central appetite-axis** (precision anatomy but a blood-brain-barrier [O] deliverability obstacle), and
  **hepatic glucose-disposal** (the honest distributed case — a body-wide receptor → a dominant-compartment
  route, not a single-compartment block).
- **Routability [F] vs deliverability [O].** The map keeps WHICH compartment (cited anatomy, [F]) distinct
  from whether an intervention can REACH it (an [O] obstacle: the blood-brain barrier, the small/variable
  BAT depot, the no-single-locus problem). No obstacle is silently dropped.
- **The firewall is PROVEN, not asserted.** Routing specificity is a parameter-free reciprocal of the cited
  compartment COUNT; γ is never an input, only carried alongside as the promoter switch-threshold context.
  `gamma_independence_gate()` recomputes the whole map under a drastically perturbed γ atlas and confirms
  every routing field (compartments / primary / specificity / tier) is **byte-identical** while **only** the
  carried γ-context column moves. (Visible in the rendered table: ordering is precision-first, and MC4R — the
  LOWEST-γ node — sits at the top because it is single-compartment, not because of γ.)
- **Code (science-neutral):** `repro/_pathology/precision_routing.py` (new) — the cited `COMPARTMENTS` /
  `ROUTING` maps, the three `NAMED_ROUTES`, the parameter-free `_tier`/`_breadth` classification, and four
  fail-closed gates: `gamma_independence_gate()` (the firewall proof), `anatomy_honesty_gate()`,
  `forbidden_claim_scan()` (the restoration scan EXTENDED with a DELIVERY class: no injection/implant/
  catheter/dose-as-fact; reuses the restoration scan machinery), and `falsification_register()` (PR1–PR3 +
  FRAMEWORK). It reads the γ atlas read-only and never touches the panel or the substrate. Surfaced like the
  three-lever module — in `repro/run_all.py` (new block **[5b] PRECISION ROUTING**), **not** folded into
  `circulate()` — so the 16-target battery and `research_gate.all_green` are untouched. Two chapters added to
  `build_docs.py` (**§R** concept + γ-independence proof, **§RM** the 9-node table + named routes + PR1–PR3);
  hub/llms/_meta gained a one-line precision note. Determinism: routing 2×sha256 identical (`21021e79…`);
  site drift 0; llms.txt 4424 bytes. **Engine sha256 is byte-identical (`08f50d6d…`)**; the panel and every
  read γ value are unchanged.

## How to verify in 30 seconds

```
python3 repro/run_all.py            # expect: 16/16 PASS, research all_green True, writing unlocked; [5b] precision tier split + γ-independence PROVEN printed
python3 tools/build_docs.py         # expect: drift 0, llms.txt < 5 KB (4424 bytes), 1 hub + 32 chapters
```

## Natural next steps (not required, in priority order)

1. **DOI — DONE.** Concept DOI [10.5281/zenodo.20756934](https://doi.org/10.5281/zenodo.20756934) is minted
   and finalized across the site. On any new Zenodo *version* deposit, update the version-specific DOI if you
   choose to cite it instead of the concept DOI, then regenerate.
2. **Precision-routing layer — DONE (this session).** The map is cited, parameter-free, and the firewall is
   PROVEN under a perturbed γ atlas. If pushed further, the honest extension is NOT a richer routing score
   (that risks importing magnitude) but a per-compartment **deliverability** object: attach the cited [O]
   reachability evidence (BBB penetrance class, BAT-depot quantity in adult humans, distributed-target
   selectivity) as a *separate* graded layer, never folded into the routing geometry.
3. **The DYNAMIC torpor contrast (RH9's standing [O] external step).** Still the deepest open item: ingest a
   real in-vivo torpor↔euthermia differential expression / methylation dataset (cited: hibernation expression
   atlases, e.g. *Ictidomys*; torpor hepatic methylation dynamics) and test whether the present-but-silenced
   gating is visible there. Logged [O] in the IRREPRODUCIBILITY_LEDGER; would require scoping the offline
   invariant (vendor a small cited processed contrast under the same provenance discipline) — keep it strictly
   firewalled (γ and CpG O/E still read structure only; the in-vivo read is a separate object).
4. **Apply the reusable patterns to the other living packages.** The PDK4 promotion, the panel-level γ NULL
   (RH8), the methylation-substrate NULL (RH9), and now the **compartment routing map with a proven
   γ-independence gate** are reusable templates — the `mind`/`disease`/`neuro` packages each have candidate
   to-measure masters, panel-/substrate-NULL opportunities, and restoration maps that could carry the same
   firewalled routing layer.
5. **Cross-package seam to `disease_wp`.** MODY currently enters as a declared imported parameter; wire the
   actual gene-lesion parameter from `disease_wp` if/when that package exposes it.

## Invariants to preserve (do not regress)

- `inherited/vp_substrate.py` stays **byte-identical** (`5664800b…`) — never re-derive the substrate math.
- `inherited/crossspecies_thermo_panel.json` stays **byte-identical** — the panel is only ever EXTENDED,
  never mutated; this version did not touch it at all.
- The engine result stays **byte-identical** unless engine code genuinely changes: the precision layer is
  surfaced in `run_all.py`, **not** in `circulate()`, so engine sha256 must stay `08f50d6d…`.
- No evolutionary / descent / selection language anywhere — observation only.
- The firewall is binding: γ (and CpG O/E) is never a clinical magnitude, never a routing input;
  disease/restoration/precision-routing are HYPOTHESES; the DYNAMIC torpor regulation is cited [O] external,
  never derived from a static read. The precision firewall is **PROVEN** by `gamma_independence_gate()` — keep
  the routing specificity a function of the cited compartment COUNT only; never fold γ into it.
- No tuning: every γ measured, spinodal/barrier locked, disease descriptors declared+cited. RH8/RH9
  separation tests are range-overlap (parameter-free); the tier rule is a parameter-free count threshold; the
  GC confound / γ-CpG-O/E dissociation is reported via cross-cell/cross-gene Pearson r, never used as a fitted
  gate.
- The original 19 cache entries and all original read γ values stay byte-identical.
- Honest grading vocabulary ([V]/[F]/[L]/[O]) is retained and is distinct from self-deprecating tone (which is
  not used). Every [O] states its obstacle (now including the precision deliverability obstacles).
- Four-document SSOT (CHANGELOG/MASTER_MANUAL/COMPLETION_LEDGER/HANDOVER) is regenerated at each version
  increment; the package ships as ONE zip (C0).
