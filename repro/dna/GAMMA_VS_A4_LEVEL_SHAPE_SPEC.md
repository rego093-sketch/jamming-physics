# γ ↔ A4 — The Level/Shape Upgrade Manual

**Purpose.** Make the relationship between **γ (gamma)** and the **A4 coordinate** impossible to
misread — clear enough for a non-specialist on first contact — and bake that clarity into the
paper so the "γ ⊂ A4" confusion can never come back.

**Scope.** A clarification + a set of drop-in edits to *A Deterministic Two-Layer Interpretation
of DNA* (v1.12). **No body number, grade, or DOI changes.** This is a precision upgrade
(append-only): it sharpens wording and adds one retired-framing tombstone. Nothing in the
engines, tables, or measured values is touched.

**Backing.** Verified in session `vp_session_gamma_a4_verified` (4 phases, 2×SHA-256,
`prereg.sha256 ff04aa7b…3901`) and confirmed directly in the v1.12 engine code
(`key_pipeline_full.py::robust_z`).

---

## 0. The whole thing in one breath

> **One signal. Two facts about it. Neither fact is inside the other.**
>
> Slide a window along a stretch of DNA and measure its stiffness. You get a wiggly line.
>
> - **γ is the *average height* of that line** — one number: "how stiff is this stretch, overall?"
> - **A4 is the *shape* of that line once you subtract its average** — where it rises, where it
>   dips, where the cliffs (the *anchors*) are.
>
> You **make** A4 by **removing** γ. So γ cannot sit "inside" A4 — A4 is, by construction, the
> part that γ is **not**. They are the **level** and the **shape** of one stiffness field: two
> orthogonal projections, neither containing the other.

---

## 1. The picture (hold this and you can't get it wrong)

```
        stiffness signal along the locus
        s(x) = w_gc·GC + w_cpg·CpG + w_at·AT6        (one wiggly line over position x)

  stiff │          ╭─╮               ╭───╮
        │    ╭─╮   ╱   ╲    ╭╮      ╱     ╲           ← the raw signal s(x)
        │   ╱   ╲ ╱     ╲  ╱  ╲    ╱       ╲
   soft │  ╱     ╲╱      ╲ ╱    ╲__╱         ╲___
        └───────────────────────────────────────►  position x

  - - - - - - - - - - - - - - - - - - - - - - - -   ← the AVERAGE height  =  γ  (one scalar)


  SPLIT THE SIGNAL INTO ITS TWO HALVES:

     γ   =  mean( s )                       the LEVEL   →  one number, "how stiff overall"
     A4  =  shape of ( s − mean(s) )         the SHAPE   →  shells, anchors, where the cliffs are
                        └── robust_z subtracts the mean, i.e. the number that *is* γ ──┘

            s   =   γ    ⊕    A4
                   level     shape           ← two halves of ONE signal; neither inside the other
```

### The everyday analogy

Think of a **mountain range**.

- **γ = the average elevation** of the whole range — one number telling you "high country" vs
  "lowland."
- **A4 = the terrain map after you flatten out that average** — where the peaks and valleys sit
  relative to the local baseline.

Two hills of the **same shape** (same A4) can sit at **different average elevations** (different γ)
— a seaside dune and a mountain-top dune. And two plateaus at the **same average elevation**
(same γ) can be **flat or jagged** (different A4). The average and the shape are **independent
facts about one landscape**.

### The one line that kills the misconception

> The software computes A4 by taking the stiffness signal and **subtracting its own average**
> (`robust_z` subtracts the per-locus median; see `key_pipeline_full.py`). The number it subtracts
> **is γ**. Therefore **A4 = "the signal minus γ."** That is why **"γ ⊂ A4" is not merely
> wrong — it is impossible**: you cannot contain the very thing you removed.

---

## 2. The misconception, named and retired

> ❌ **RETIRED (irreversible):** "γ is one of the A4 coordinates" / "γ ⊂ A4" / "γ is a special
> case (a coarse version) of A4."
>
> ✅ **CORRECT:** "γ and A4 are the **level** and the **shape** of one stiffness field — two
> **orthogonal projections**. They share an input; neither contains the other's output."

Why this is a *falsified* claim, not just an unfashionable one: the executed test partitioned the
possibilities (R1: shell/anchor are γ-redundant; R2/R3: distinct constructs) and **falsified all
of them**. Same field (Phase 1 + Phase 4) **and** no γ-redundant A4 axis (Phase 2). The data, not
taste, retire it. → Add it to the §8 retired register (text in §6.3 below).

---

## 3. The four things people confuse — and the fix for each

| If you find yourself thinking… | …you are confusing… | The fix |
|---|---|---|
| "A4 is just a more detailed γ, so γ is a coarse A4." | **level** with **shape** | A4 has the level *removed*. It is not a finer γ; it is a **different quantity** — the residual shape after γ is taken out. |
| "γ and A4 are separate, unrelated reads." | **orthogonal** with **independent** | They read the **same field** (ρ ≈ 0.94). A4 is built *from the very signal γ averages*. **Orthogonal outputs, shared input.** |
| "γ carries the structure / the position." | **level** with **shape** | Position, shell, anchor, loop = **A4 (the shape)**. γ is one scalar; it carries **no position** at all. |
| "The shell value is basically γ for that window." | **shell** with **level** | The shell label comes from the **mean-removed** z-signal (terciles of `robust_z`). Even the shell is **shape**, not level. |

---

## 4. The 10-second self-check (orthogonality you can feel)

Two knobs. Turn one, the other does not move. That is what "orthogonal projections of one field"
means, operationally:

1. **Raise the whole line** (add a constant stiffness across the window).
   → **γ changes. A4 is identical** — subtracting the new average removes the constant.
   → So **A4 cannot contain γ.**

2. **Rearrange the bumps, keeping the average fixed** (same area under the line, different shape).
   → **A4 changes. γ is identical** — the mean is unchanged.
   → So **γ cannot contain A4.**

Two independent knobs ⇒ neither quantity is nested in the other. Full stop.

---

## 5. The evidence (dead simple)

From `vp_session_gamma_a4_verified` — 37 loci (`sequences_v6` + cross-kingdom), deterministic,
2×SHA-256, `prereg.sha256 ff04aa7b…3901`:

| Question | Measurement | Result | Reading |
|---|---|---|---|
| Same field? | per-locus ρ(γ-signal, A4-signal) | **median ρ = 0.939** (0.896–0.986) | yes — ~94 % the same substrate |
| Same coarse skeleton? | γ-driven vs full-signal shells/anchors | **anchor offset 0.0 bp (37/37)**, label match 0.93 | identical coarse architecture |
| Does A4 carry γ? | max \|corr(any A4 axis, γ)\| | **0.327** (all axes ≤ 0.33) | **no** — `robust_z` removed the level γ is |

**Mechanism (why it must be so).** γ = `−mean(NN ΔG)` = the **mean** of the field. The A4 pipeline
applies `robust_z`, which **subtracts the per-locus median — i.e. deletes the level γ is** — and
keeps only the within-locus relative shape. **Shared input ≠ nested output.**

**One honest caveat for the rigor-minded** (keep it out of the fool-proof summary, keep it in the
ledger): γ uses the full SantaLucia NN table, while the A4 stiffness signal uses the
GC/CpG/AT6 proxy with locked weights. They are **not byte-identical signals** — they are the same
field "at ~94 %" because both are GC-dominated. The level/shape relationship is exact for the part
they share; the residual ~6 % is the dinucleotide-order term γ adds beyond the proxy. This does not
soften the conclusion — A4 still carries **zero** of the level (Phase 2).

---

## 6. Drop-in paper edits (paste-ready, append-only)

Each edit only **adds a clarifying sentence** or a reusable card. Existing wording stays; nothing
is deleted except where a sentence is explicitly *replaced* with a strictly clearer one carrying
the same numbers.

### 6.1 — §I "How to read a locus", Step 2 (the first place γ and A4 meet)

**Insert** this lead sentence at the top of *Step 2 — Where does the element sit? The A4 coordinate*,
before the existing "The same read places the element…":

> **First, the relationship in one line.** γ and the A4 coordinate are the **level** and the
> **shape** of one stiffness signal: γ is its window-mean (a single number), and the A4 coordinate
> is the *same signal with that mean removed* — the shells and anchors are literally what is left
> after the average (γ) is subtracted out. So a locus has **one γ** (its overall stiffness) **and
> one A4 shape** (where it is stiff vs soft relative to its own average); neither contains the
> other.

### 6.2 — §2 "Material (γ): the threshold scale", "A scale, not a locus"

**Append** one clause to the existing paragraph that ends "…the scale of the threshold":

> — and it is the **level** of the stiffness signal, not its shape: where the element sits
> (shell, anchor, loop) is the **mean-removed** A4 read of §13, a separate projection of the same
> field.

### 6.3 — §8 "Bounds, open questions, retired claims", Retired register

**Add** this entry to the retired register, after the helical-periodicity tombstone:

> Also retired (irreversible): the framing **"γ ⊂ A4" / "γ is one of the A4 coordinates" / "γ is a
> coarse A4."** A direct measurement (37 loci, 2×SHA-256, `prereg.sha256 ff04aa7b…`) falsified
> every nesting hypothesis: γ and A4 read **one stiffness field** (per-locus ρ = 0.94; identical
> coarse anchors, 0.0 bp offset across all 37 loci) but the A4 coordinate carries **none of γ**
> (max \|corr(axis, γ)\| = 0.327, because the A4 pipeline's `robust_z` subtracts the per-locus
> median, which is exactly the level γ is). The correct, standing statement is: **γ = the level
> (window-mean) and A4 = the shape (mean-removed structure) of the same stiffness field — two
> orthogonal projections, neither nested in the other.** This framing must not revive under any
> name (e.g. "γ is the zeroth A4 channel").

**Also add** to the closure ("no fourth bucket") section a one-line clarifier:

> The four readable channels are not nested. In particular γ (§2) and the A4 coordinate (§13) are
> the **level** and the **shape** of one stiffness field — read together, never one inside the
> other.

### 6.4 — §13 "Unified deterministic interpreter", abstract

**Replace** the abstract's opening two sentences:

> *OLD:* "Earlier chapters split the read in two: the A4 grammar gave structure and position, while
> the cross-kingdom and clade chapters measured γ and methylation as global statistics without the
> coordinate. This chapter unites them into a single engine…"

> *NEW:* "Earlier chapters reported two projections of **one stiffness field** without naming their
> relationship: γ is its **level** (the window-mean scalar of §2), and the A4 coordinate is its
> **shape** (the *same* signal with that mean removed — shells, anchors, loops, anchor-relative
> phase). They are orthogonal, not nested: the A4 pipeline's `robust_z` subtracts the per-locus
> median, which is exactly the level γ is, so the coordinate carries none of γ while reading the
> same substrate. This chapter unites the level read and the shape read into a single engine…"

**Add**, in *The coordinate grammar, restored*, a sentence after "…restores that read":

> Mechanically, the coordinate is the **mean-removed** view of the same stiffness signal γ averages:
> `robust_z` deletes the per-locus level (= γ) and keeps the relative shape, which is why the shell
> and anchor reads are orthogonal to γ even though they are computed from the same field.

### 6.5 — Reusable vp-card ("γ vs A4: level vs shape")

Paste this self-contained card on any page that reports both γ and A4 (at minimum §I, §13):

```html
<aside class="vp-card">
  <h4>γ and A4 are level vs shape of one field</h4>
  <p>γ is the <strong>average</strong> of the stiffness signal (one scalar). A4 is the
  <strong>shape</strong> of that same signal once the average is subtracted out (shells, anchors,
  loops). The engine builds A4 by removing the per-locus mean (<code>robust_z</code>), which is
  exactly γ — so A4 is "the signal minus γ", and "γ ⊂ A4" is impossible. Same field (ρ≈0.94),
  orthogonal projections; neither contains the other.</p>
  <p class="vp-grade">Grade: verified (level/shape decomposition, 2×SHA-256,
  prereg ff04aa7b…) — same field; A4 carries none of γ (max|corr|=0.327).</p>
</aside>
```

### 6.6 — Retrieval surfaces (`docs/llms.txt`, `_meta.json` one-liners)

Add one canonical read to `llms.txt` under "Canonical reads":

> - γ = LEVEL (window-mean of stiffness); A4 = SHAPE (same field, mean removed) — orthogonal
>   projections, neither nested [V]

Update the §13 `one_liner` in `_meta.json` to lead with the relationship:

> "γ and the A4 coordinate are the level and the shape of one stiffness field (A4 = the same signal
> with γ's mean removed); one engine reads both, restores the coordinate, and corrects the global
> helical claim to an anchor-relative contact read."

---

## 7. What is settled vs what is still open (so no one over-claims the *other* direction)

Making the relationship clear must not silently settle the open question it raises.

- **Settled [V]:** γ = level, A4 = shape, same field, orthogonal. (This manual.)
- **Settled [V]:** the **γ-level** is orthogonal to developmental **timing** (heart ρ = +0.071,
  p = 0.882). γ's level carries no fine timing — by information-theoretic necessity, a mean is a
  low-pass filter.
- **STILL OPEN [O]:** whether the **A4-shape** predicts order/timing that the **γ-level** cannot.
  This was **not** tested fairly — the one attempt (Phase 3b) ran on 2501 bp promoter fragments
  `< min_shell_bp (5000)`, so A4 was **degenerate** there. The single closing test: **re-run the
  heart/organ timing test with 25–50 kb windows** so the A4 coordinate has real shell/anchor
  resolution. Until then, "γ-level ⊥ timing" is earned, but "**sequence** ⊥ timing" is **not** —
  do not let the clarified level/shape language be read as closing it.

> Plain version: we have proven γ's **average** is blind to timing. We have **not** proven the
> **shape** is. Don't confuse "the average can't" with "nothing in the sequence can."

---

## 8. Governance

- **Append-only.** Every §6 edit adds a clarifying sentence or a reusable card; the only replaced
  text (§13 abstract opening) carries the same numbers, just sharper. No measured value, grade,
  table, equation, or DOI changes.
- **Grades.** The level/shape relationship is **[V]** (`vp_session_gamma_a4_verified`, 2×SHA-256,
  `prereg.sha256 ff04aa7b8b025bd19c6f06c7da253d66952acbe22a3f6804ade5b6cd5fac3901`). The "does
  shape carry timing" question stays **[O]** with its named closing input (25–50 kb windows).
- **Retired register is irreversible.** "γ ⊂ A4" joins the retired register and must not revive
  under any renaming.
- **Anti-작문.** Every number in this manual (ρ = 0.939, 0.0 bp / 37 loci, max|corr| = 0.327,
  ρ = +0.071 / p = 0.882) is from the executed session or the v1.12 engine; none is invented.

---

### One-paragraph summary

DNA has **one** stiffness signal. **γ is its average** (one number: how stiff overall). **A4 is its
shape** (where it's stiff vs soft, where the cliffs are) **after that average is subtracted out**.
The engine literally makes A4 by removing the mean — which is γ — so **A4 = "signal minus γ," and
"γ ⊂ A4" is impossible**. They are the **level** and the **shape** of one field: orthogonal,
neither inside the other (same field at ρ ≈ 0.94, yet A4 carries none of γ, max|corr| = 0.327). The
upgrade is to state this in plain words wherever γ and A4 meet (§I, §2, §8, §13), retire the
"γ ⊂ A4" framing in the §8 register, and **not** let the new clarity be misread as settling the
still-open question of whether the *shape* (unlike the *level*) can carry developmental timing.
