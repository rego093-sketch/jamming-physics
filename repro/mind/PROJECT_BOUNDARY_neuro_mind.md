# PROJECT_BOUNDARY — neuro ⟷ mind

**Status:** LOCKED · the authoritative definition of where the two tracks separate.
**Scope:** governs **both** deliverables — `neuro` (this package) and `mind` (its own
package). Consolidates rules that were previously scattered across VP-SPEC §1.6 (lanes),
§2 (registry derivation relations), the mind `CONVERSION_REPORT` §2 (IN/OUT), the
`WORK_HANDOVER`, and `EM_NEAR_FAR_THESIS.md`. Where those agree, this restates; where a
rule was implicit, this makes it explicit.
**Enforced by:** `verify_boundary.py` (neuro-side architectural lock) + `verify_em_thesis.py`
(content lock). Both deterministic; both kept outside `run_all.py` so `verify_all.py` stays 5/5.
**Author:** Young Jae Lee · governed by VP-SPEC C0–C4.

---

## 0. The one-line lock (read this first)

> **`neuro` is the verified substrate; `mind` is the frontier model built on top of it.**
> The dependency is **one-way**: `mind` cites `neuro`; **`neuro` never depends on `mind`.**
> They are **two files, two lanes** — never merged. The only things shared byte-identical are the
> small SSOT set: `EM_NEAR_FAR_THESIS.md`, `TERMINOLOGY_canonical.md`, and this boundary file (§6).

This single asymmetry is the whole boundary. Everything below is its consequence. The reason
the asymmetry is strict: `neuro` is independently citable *because* it is independently
verifiable. The moment `neuro` leaned on `mind` (a frontier paper with **no causal anchor**),
`neuro`'s verified status would inherit `mind`'s openness, and the chain's one clean citation
target would be lost.

---

## 1. The two objects (what each one IS)

| | **neuro** — Neural Emergence Chain | **mind** — Felt Cognition |
|---|---|---|
| registry role (VP-SPEC §2) | branch — **own chain** | frontier — **cites neuro, one-way** |
| epistemic shape | one **causal anchor** (capacity = θ/γ, by tACS) + model + bounded `[O]` | **model + a large OPEN register, NO causal anchor** |
| what it answers | the **computation** of encoding, memory, value, behaviour; the physics of the EM near-field, measured and bounded | the **functional / felt** account: the stream of thought, why computing thought ≠ feeling it, the hard problem |
| where it stops | **at the computation.** Subjective experience is explicitly OUT. | takes up exactly what neuro defers; does **not** re-derive the substrate |
| verification | `verify_all.py` → 5/5; `verify_em_thesis.py` → 6/6 | `repro/mind/_verify/run_regression.py` → mechanism + determinism PASS |
| deliverable | `neuro_emergence_chain_integrated_v*.zip` | `mind_vp_site_UPGRADED*.zip` |

**The seam in one sentence:** neuro ends at *"this is the computation of encoding, memory and
behaviour"*; mind begins at *"here is the functional/felt account that runs on that computation,
and here is the part that stays open."*

---

## 2. Ownership / scope boundary — IN / OUT (frozen)

**IN `neuro`** (the verified substrate; mind may cite, never re-derive):
ion channels → rhythm/bands/coupling → θ/γ working-memory code → memory write/retrieve/
consolidate → value/intuition binding → control/morality → motor output (recruitment, force,
CPG) → sensory transduction → sensorimotor loop → the EM thread (emission §13, link §15,
near-field circulation §18, ephaptic threshold §19), measured/derived and graded.

**IN `mind`** (the frontier model; built **on** neuro's substrate):
parallel micro-eddies → selection closed loop → the learned field → the stream of thought →
the embodied felt loop → hemispheres & why thought ≠ feeling → the open problem of experience
(access question + hard problem + quale, honest-negative).

**OUT of `neuro` → belongs to `mind`:**
- subjective experience / consciousness (both the **access** question and the **hard problem**);
- whether cognition **functionally uses** the measured at-threshold near-field (the §18/§19 OPEN);
- the **re-grounded functional parallel-eddy** reading of thought (mind distinguishes it
  explicitly from the retired field).

**OUT of `mind` → belongs elsewhere:** the substrate itself → `neuro`; the genome → `dna`.

**RETIRED in both (kept in neuro §9 and mind §2, never revived):** the radiative far-field /
optical-fibre (TIR) EM carrier; axon-as-optical-fibre; EEG-as-radiative-carrier;
energy = information; DNA phase memory; the "consciousness vortex field." (See
`EM_NEAR_FAR_THESIS.md` — "EM" is **never** retired wholesale; only the far-field carrier is.)

---

## 3. Dependency boundary — the direction is one-way

| direction | status | what it may contain |
|---|---|---|
| **mind → neuro** | **ALLOWED** | mind cites neuro's **results with their status tags** (e.g. "capacity = θ/γ `[V]`", "ΔVm ≈ 0.27 mV at threshold, neuro §19"). Citation only. |
| **neuro → mind** | **FORBIDDEN as a dependency** | neuro may carry only **forward-defer pointers** — prose naming where an open item goes ("deferred to Mind", `href="/mind/"`). Never a result imported from mind, never reliance on mind being correct. |

**A pointer is not a dependency.** neuro §9 saying *"the access question is carried to Mind"* and
linking `/mind/` is the **interface**, not a coupling — neuro states *where the open question
travels*, then stops. This is allowed and expected. What is forbidden is neuro **consuming** a
mind claim (citing a mind result as support, importing a mind module, gating on a mind number).

**At the verification level the rule is stronger than prose:** neither package's gates may import
the other's code. Each must verify from its **own single zip** with the sibling absent. (Current
state: neuro has **0** code-level mind imports; mind has **0** code-level neuro imports; each
passes its gates alone.)

---

## 4. File / lane boundary — two files, never merged

Per VP-SPEC §1.6 each paper owns a lane and a session never writes outside it; a cross-lane file
in a hand-off zip is **itself a gate FAIL**.

| | neuro lane | mind lane |
|---|---|---|
| canonical HTML | `docs/neuro/`, `docs/eq/neuro/` | `docs/mind/` |
| manifests | `manifest/neuro*.csv` | `manifest/mind*.csv` |
| reproduction | `repro/neuro/`, `content/`, neuro `tools/` | `repro/mind/` |
| gate reports | `reports/…neuro…` | `reports/…mind…` |

**One file per track.** neuro ships as `neuro_emergence_chain_integrated_v*.zip`; mind ships as
`mind_vp_site_UPGRADED*.zip`. **Do not** assemble a combined zip and **do not** drop mind files
into the neuro zip (or vice-versa). Each zip re-establishes its *entire* trusted state on its own:
extract → `cd` → run that package's verifier.

---

## 5. The hand-off interface — exactly what crosses

The boundary is crossed by **named OPEN items only**. neuro hands mind a short, explicit list;
nothing else transfers. Each crossing item carries three things so it is self-contained on arrival:

1. **the open question** (stated precisely),
2. **its status tag** (`[O]` / OPEN — *open because untested, not because false or weak*),
3. **the named decisive test** + a back-citation to the neuro section that bounds it.

The list (neuro → mind):

| open item | neuro origin | the decisive test mind inherits |
|---|---|---|
| Does cognition **functionally use** the measured at-threshold near-field / ephaptic coupling? | §18 (circulation) → §19 (at threshold) | behaviour-labelled intracranial recording, local field **cancelled vs. augmented** in real time |
| The **access** question (why some processing is reportable) | §9 register | robust bistable up/down dynamics + report-labelled data |
| The **hard problem** (why any of it is felt) | §9 register | none known — honest negative (mind §12 / quale) |
| The re-grounded **functional parallel-eddy** reading | §9 (retired-field carve-out) | mind builds it on the ionic substrate, explicitly *not* as a field of its own |

**mind takes these up; mind does not re-derive the substrate that produced them.** Conversely, if
mind ever resolves one (e.g. a positive functional-use result), that result does **not** flow back
into neuro — neuro cites no mind result. A confirmed finding would re-enter the chain only as a new
*measured input* under VP-SPEC C1, with its own citation, in a future neuro session — never as a
dependency on the mind paper.

---

## 6. Shared artifacts — the SSOT set held in common (byte-identical in both)

There is a small, **closed set** of shared single-source-of-truth files that live **byte-identical**
at the root of **both** packages. They are the files that pin a question *across* the two papers, so
it cannot be re-decided divergently. Everything else is lane-separated (§4).

| shared SSOT file | what it pins (read by) | guarded by |
|---|---|---|
| `EM_NEAR_FAR_THESIS.md` | the EM **regime** — near-field affirmed / far-field carrier retired; the A/B objects (§1.1); the two registers (§1.2) | `verify_em_thesis.py` (both) + byte-identity |
| `TERMINOLOGY_canonical.md` | the **controlled vocabulary** — the χ→0 objects, the three speeds, and the register/ownership split (§7: `neuro` owns objects, `mind` rides the brainwave abstraction) | `verify_terminology.py` (both) + byte-identity |
| `PROJECT_BOUNDARY_neuro_mind.md` | this **boundary** itself | `verify_boundary.py` (both) + byte-identity |

`neuro` §9 and `mind` §2/§4 are read under the EM thesis; both papers' EM prose is read under the
terminology canonical (§7 in particular tells each paper which words it owns). The "EM = brainwave =
low-frequency" abstraction is defined once, in the thesis §1.2 and the canonical §7, and inherited
by both — so the cognition register and the physics register cannot drift apart.

**Rule for the shared set:** any edit to any of the three must be **mirrored byte-identical** into
both packages, and each package's guards re-run (`verify_em_thesis.py` 6/6, `verify_terminology.py`,
`verify_boundary.py`). A cross-package drift in any of the three is a boundary FAIL. The helper
`sync_shared_ssot.py` (shipped at the root of both) copies the set one way and asserts byte-identity
when the two extracted packages sit side by side — run it after any shared-file edit.

---

## 7. What would break the boundary (and the gate that catches it)

| violation | caught by |
|---|---|
| neuro imports/cites a **mind result** (beyond a forward-defer pointer) | `verify_boundary.py` check (1) — no neuro→mind code import; review for cited mind claims |
| a **mind-lane file** ships inside the neuro zip (or vice-versa) | `verify_boundary.py` check (2) — lane purity; VP-SPEC §1.6 (cross-lane file = FAIL) |
| the two tracks **merged** into one zip | breaks "one file per track" (§4); each verifier expects its own root |
| `EM_NEAR_FAR_THESIS.md` **drifts** between the two copies | byte-identical check + `verify_em_thesis.py` in **both** packages |
| **"EM" retired wholesale** anywhere, or the far-field carrier revived | `verify_em_thesis.py` — both content boundaries pinned (6/6) |
| mind **re-derives** neuro's substrate instead of citing it | scope review against §2 IN/OUT (mind must cite the OUT→neuro items, not rebuild them) |
| neuro made to **depend on** mind to verify | `verify_boundary.py` check (5) — standalone contract intact; each gate runs with the sibling absent |

---

## 8. Enforcement — the two gates

**neuro side (checkable from this package alone):**
- `verify_boundary.py` (package root) → **5/5**, report `reports/lock-neuro-boundary.gate.json`.
  Pins: no neuro→mind code import · lane purity · shared SSOT present · EM lock holds · standalone
  contract intact.
- `verify_em_thesis.py` (`repro/neuro/09-bounds-open-retired/`) → **6/6**, report
  `reports/lock-neuro-09-em-thesis.gate.json`. Pins the EM content boundary.
- Both are **outside** `run_all.py`, so `verify_all.py` stays **5/5**. Run them after any edit that
  touches the EM question, the §9 register, cross-references to mind, or the package's file set.

**mind side (run these when the mind track is worked — its own session, its own zip):**
1. `repro/mind/02-not-a-field/verify_em_thesis.py` → 6/6 (mind's copy of the EM lock).
2. Confirm the mind copy of `EM_NEAR_FAR_THESIS.md` is **byte-identical** to neuro's.
3. Confirm **0** code-level `import` of any neuro module anywhere in `repro/mind/**`.
4. Confirm mind cites neuro results **with status tags**, and does **not** re-derive the substrate
   (§2 IN/OUT).
5. Confirm the mind zip carries **no** neuro-lane files.

*(A mirror `verify_boundary.py` can be added to the mind package to mechanize 2–5 in the same
style, when that track is next opened.)*

---

## 9. Current status (post EM-reconciliation — neuro v1.9.5 / mind v1.8.1)

- `verify_all.py` → **PASS 5/5** · `verify_em_thesis.py` → **PASS 6/6** ·
  `verify_boundary.py` → **PASS 5/5** · `verify_terminology.py` → **PASS**.
- neuro→mind: **0** code imports; **forward-defer pointers only** (6 HTML files) — the allowed
  interface.
- mind→neuro: citation in prose, **0** code imports — one-way cite holds.
- Shared SSOT set (§6): `EM_NEAR_FAR_THESIS.md`, `TERMINOLOGY_canonical.md`,
  `PROJECT_BOUNDARY_neuro_mind.md` — present in **both** packages, **byte-identical**; checked by
  `sync_shared_ssot.py`.
- Lanes: clean (no mind-lane files in the neuro package).

*(v1.9.5 EM-reconciliation pass: the thesis §1.2 and the canonical §7 add the "EM = brainwave =
low-frequency" abstraction and the object-vs-brainwave ownership split — `neuro` owns the objects,
`mind` rides the abstraction and cites. `mind` §2/§4 prose was brought into the cited register; the
`mind` package received the full shared SSOT set plus mirror `verify_boundary.py` /
`verify_terminology.py`.)*

**The boundary is in force and mechanically checked. The `mind` track proceeds as its own file
under §8's mind-side checklist; it is not folded into this package.**
