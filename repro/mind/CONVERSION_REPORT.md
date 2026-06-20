# CONVERSION REPORT — `mind` (Felt Cognition)

**Spec:** VP_SPEC v1.6 · **paper_id:** `mind` · **code:** `min` · **branch:** `jamming`
**Build:** code-driven. Source = the consciousness arc of `dna_4d_emergence_kit` (`INTEGRATED_WHITEPAPER` consciousness sections + `STATUS.md` **C18 + C34–C42** + the 8 arc result JSONs), ported to English with **no meaning or number change**.

**This is a FRONTIER paper.** Unlike `neuro` (one causal anchor, a clean citation target), `mind` is **model + a large OPEN register, with NO causal anchor** — the honest signature of the subject. Two disciplines are load-bearing and hold on every page:
1. **Physical-mediator obligation.** Every "eddy/field" names what carries it — the **ion spike + synaptic current** along real connections, gated by the **phase of classified low-frequency oscillations (δ/θ/γ)** = communication-through-coherence. *The oscillation does not carry the message; it sets when the message gets through.* Abstract "synchrony" with no named mediator is forbidden (it reads as fiction and invites confusion with the retired field).
2. **One-way dependency.** `mind` cites `neuro` results *with their status tags*; **`neuro` does not depend on `mind`.** This protects neuro's citability.

---

## 1. What was built

```
docs/mind/
  index.html                       (hub — frontier banner + mediator bright line)
  01-constitution-scope/index.html
  02-not-a-field/index.html            ← the guardrail: retired EM field vs the named mechanism
  03-parallel-eddies/index.html
  04-selection-loop/index.html
  05-learned-field/index.html
  06-stream-of-thought/index.html
  07-felt-loop/index.html              ← the hard problem is marked open here
  08-hemispheres-and-ai/index.html     ← "computing thought ≠ feeling it" (architectural hypothesis)
  09-open-problem/index.html
  _meta.json
docs/assets/css/site.css           (byte-identical shared asset)
manifest/mind.csv
manifest/mind_claimmap.csv         (Phase A: C18 + C34–C42 + quale + RETIRED → chapter / OPEN)
reports/phase2-mind-full.gate.json (GATE PASS — 120/120)
repro/mind/_verify/                (REGRESSION PASS — 16 mechanism checks, seed=7, offline)
repro/mind/{01..09}/README.md      (per-slug honest scope)
```

Total body words **2645** (tighter than neuro's 2933 — a focused frontier paper). Inline unicode math only; **zero display equations → no `/eq/` SVGs**.

---

## 2. Scope — IN / OUT (frozen)

**IN (this paper)** — the *functional* model of the stream of thought and felt cognition:
parallel micro-eddies (C34) → selection closed loop (C35) → the laid-down field is learned (C36) → the stream of thought (C37) → the embodied feeling loop (C38·C39·C40) → hemispheres & why thought ≠ feeling (C41·C42) → the open problem of experience (C18 honest-negative + quale).

**OUT → `neuro`** (published, the verified substrate): ions → rhythm → θ/γ code → memory → value → the basal-ganglia loop. `mind` **cites** these, never re-derives them.

**OUT → `dna`**: the genome.

**RETIRED (kept in §2 and §9, never revived):** the EM "vortex field" as a carrier — physically false (tissue coherence length short by ~10⁹×); axon=optical-fibre, EEG=EM-carrier, energy=information, DNA phase memory. The *functional* parallel-eddy reading is a structure **on** the ionic substrate, never a medium of its own.

---

## 3. Per-chapter grade (claim-strip badge = real status)

| § | chapter | grade (badge) |
|---|---|---|
| 1 | Constitution and scope | — (framing) |
| 2 | The retired field, and what replaces it | — (guardrail) |
| 3 | Parallel micro-eddies | model |
| 4 | Selection: the closed loop | model |
| 5 | The laid-down field is learned | model |
| 6 | The stream of thought | model |
| 7 | The embodied feeling loop | model (hard problem OPEN) |
| 8 | Hemispheres, and why thought is not feeling | model (hard problem OPEN) |
| 9 | The open problem of experience | **open** |

**No `causal` anywhere — model×6 → open.** That gradient IS the honest frontier signature. Citation rule: `mind` claims are citable only as *proposed mechanisms / open questions*, never as results; the wired components carry their *direction* support from `neuro` (cited), not from `mind`.

**Headline (`_meta.json`):** the stream = serial selection among parallel γ-eddies (functional model) · the "field" = band-structured phase-coherence on ionic spikes/synaptic currents (CTC), **NOT** the retired EM field · consciousness (PCI) = honest negative, hard problem OPEN · thinking ≠ feeling (architectural hypothesis).

---

## 4. Gate (VP_SPEC §8) — **PASS, 120/120, 0 fail**

Same §8 checks as dna/neuro (section count, single `<h1>`, title suffix + lengths, description 80–160, abstract with ≥1 unicode-math token, **anti-fabrication numbers-in-body**, no katex, ≤300 KB, DOM ≤3000, internal links resolve, hub orphans 0, **cross-branch ref** → links `/neuro/` and `/dna/`).

*Two real defects caught and fixed:* (a) five descriptions exceeded 160 chars → rewritten into range; (b) §8's abstract used `&rarr;` **entities**, so the unicode-math check saw zero → switched to a literal `→`. (Same class of subtlety the neuro build surfaced — entities are not glyphs.)

---

## 5. Repro (`repro/mind/`) — **REGRESSION PASS, 16 checks, seed=7, offline**

`_verify/run_regression.py` vendors the **real** arc artifacts (8 JSONs — no invented numbers), verifies them **bit-for-bit** (sha256), and re-derives the **mechanism** invariants from the frozen numbers: winner-take-MOST (losers retained 0.215 under soft vs 0 under hard), γ→ignitability (pearson ≈ 1.0, monotone), single-winner selection (nsel = 1, commit = 1; control = 0), and RPE learning toward reward (target 0.75 vs control 0.07).

**Honest scope (the critical line):** the regression demonstrates that the **mechanisms behave as claimed** — it does **NOT** confirm the functional theory of consciousness, and it reproduces **no marker of consciousness** (the PCI access marker is an **honest negative**, §9). Component circuits (basal-ganglia selection, dopamine RPE) inherit their *direction* support from the `neuro` paper, not from this harness. Per-slug READMEs state, chapter by chapter, what reproduces (mechanism demos: §3–§5) versus what is framing (§1, §2), composite-model (§6), or explicitly **not reproduced** because there is nothing to reproduce for the felt quality (§7, §8) and the honest negative (§9).

---

## 6. ⚠ AUTHOR-LOCK flags (resolve before publishing)

1. **DOI decision — RESOLVED.** Minted as a **new own concept DOI** (the recommended option, since `mind` is a distinct work from the applications/DNA lineage of `17979015`). Concept DOI = `10.5281/zenodo.20694404` (version-independent, embedded throughout); this version (v1) = `10.5281/zenodo.20694405`. The placeholder has been swapped across all pages, `_meta.json`, hub, PDF, and TeX.
2. **Registry row.** Add to `tools/split.py` `REG`:
   `"mind":dict(code="min",short="Felt Cognition",branch="jamming",doi="<DOI>",title="Felt Cognition: Parallel Micro-Eddies, the Stream of Thought, and the Open Problem of Experience")`
   `branch="jamming"` keeps it a sibling of dna/neuro; change only if you want a separate "frontier" arm.
3. **"Why a system can think without feeling" framing (§8) — confirm.** It is stated strictly as an **architectural hypothesis** (current AI appears to lack the embodied real-time loop), with the hard problem flagged OPEN and an explicit disclaimer that the model does **not** prove an artificial system cannot feel. Confirm this non-overclaiming framing is acceptable.
4. **Bright-line approval.** Confirm §2 ("Not a field") + the physical-mediator tagging draw a sufficient boundary against the retired EM field.

---

## 7. Cross-links (§10) & out-of-scope

**Cross-links built:** hub → `/neuro/` (the verified substrate; "every mechanism here rests on neuro") and → `/dna/`. The `neuro` paper's §9 and hub already forward-reference `/mind/`, which now **resolve**. The dependency is **one-way** by construction — mind→neuro, never neuro→mind.

**Out of scope (site-wide; needs the whole program):** `concepts/` glossary (CTC, ignitability, winner-take-most, felt loop, access vs phenomenal…), top-level `index.html` + `sitemap.xml`, Scholar `citation_*` tags + Zenodo back-links (after the DOI is minted).

---

## 8. Merge

1. Drop `docs/`, `manifest/`, `reports/`, `repro/` into the repo root (paths are repo-relative).
2. Confirm `reports/phase2-mind-full.gate.json` = PASS.
3. Resolve the four AUTHOR-LOCK flags (§6).
4. Commit → GitHub Pages serves `docs/mind/`; the neuro↔mind cross-links go live (one-way dependency preserved).
