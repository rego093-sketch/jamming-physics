# START HERE — increment A4 (the FULL A4 anchor / loop / anchor-relative-phase deferred read)

**One-line goal.** Turn the FIREWALL's one **NAMED, DEFERRED [O]** — *"the FULL A4 anchor/loop/anchor-
relative-phase needs the wider region + an NCBI feature table and is a named [O] deferred read"* — from a
flagged gap into a **MADE measurement**, by fetching the two named inputs for all 19 genes and running the
**INHERITED** grammar on them. No new machinery, no tuned number.

## Why this increment exists
The seed reads each master-gene promoter as **γ (LEVEL) + the promoter-scale A4 SHAPE**. The firewall
flagged exactly one thing as deferred: the **FULL** A4 coordinate — the wide-neighbourhood shell, the
nearest architectural anchor, the real motors/loops, and the anchor-relative helical phase — because it
needs a **wider genomic region** and an **NCBI feature table (rettype=ft)**. Two facts make it closable
**without tuning**: (1) the inherited grammar (`inherited/dna_interpreter.py` + `key_pipeline_full.py`)
ALREADY contains every function the full read uses — `run_key` (the wide-region stiffness-shell map),
`build_anchors`, `parse_ft_motors`, `build_loops`, `helix_coord`; and (2) what was missing was the
**MEASUREMENT** — the wider region and the feature table per gene. This increment fetches exactly those
two inputs and runs the existing grammar. **The [O] was a missing measurement, not missing machinery.**

## What it delivers (all in this folder)
- `run.py` — the deterministic module (self-hashing, 2×sha256). Imports the **inherited** grammar
  (`dna_interpreter`) + the frozen `vp_substrate` seed; recomputes the full A4 coordinate **offline** from
  the cached bytes; **edits no inherited byte** and triggers **no re-freeze** of the 8 inherited artifacts.
- `gate.py` — the standalone gate (G1–G7).
- `FINDINGS.md` — the results table + seven honest negatives (N1–N7).
- `START_HERE.md` — this card.

Two supporting artifacts live outside this folder (the package's measurement + fetch layer):
`tools/fetch_region_features.py` (the live NCBI fetcher) and `inherited/ear_regions.cache.json` (the
**raw measured** wide-region + feature-table bytes, added to `FROZEN_SHA256.json` as **one new frozen
key** — the 8 pre-existing inherited entries stay byte-identical).

## The result in one paragraph
The deferred read is now **MADE**. With a single, gene-independent genomic **FLANK = 20000 bp** each side
of the frozen promoter window, the cached promoter occupies a fixed offset inside the strand-corrected
wide region, so **`region[FLANK:FLANK+2501]` == the frozen promoter byte-for-byte for all 19 genes** — the
keystone: the wide A4 coordinate sits ON the unchanged γ layer with **zero drift**. Running the inherited
grammar on the measured inputs, **every** gene's TSS now carries a real **wide-neighbourhood stiffness
shell** (18/19 stiff — GC/CpG-island promoter neighbourhoods; TMC1 the AT-rich exception), a real
**nearest shell-boundary anchor** (strength = |Δmean_z|, with its distance), **real neighbouring-gene
motors** parsed from the NCBI feature table and joined as **loops (19/19 carry ≥1 real motor** — the core
promise of `dna_interpreter`, *anchors-only → real motors+loops*, now fulfilled on measured annotation),
and a real **anchor-relative B-DNA phase** (rise 3.4 Å, twist 34.29°/bp) that reads each TSS as
**contact-competent** (same rotational face, ≲60°) or not (3/19 competent: EYA1, PCDH15, SLC26A4 — the
grammar's verdict, not a tuned one). The read is **mostly window-stable**: under a 2× shrink to the
central sub-window of the **same fetch** (no new data), motor existence holds **19/19**, shell class
**15/19**, contact sign **16/19** — so it is **not a FLANK artifact** for the majority; the boundary-near
minority that flips is the named **window-relative [O]**. No clean numeric "closure" is claimed — that
would be tuning; the absolute FLANK / anchor distances / shell-motor-loop counts are window-relative
**[O]**, "anchor" is a mechanical stiffness-boundary **proxy** (not a measured CTCF/cohesin site), "loop"
is a geometric join (not a measured Hi-C contact), the phase uses **idealised** constant twist, and
Layer-2 stays flagged — each obstacle **named** (N1–N7), never invented.

## How to run / verify
```
python3 research/A4-anchor-loop-phase/run.py     # prints the full read; ends with 'sha256: …'
python3 research/A4-anchor-loop-phase/gate.py    # 'A4 GATE: PASS' iff all 7 hold
python3 tools/fetch_region_features.py verify inherited/ear_regions.cache.json   # re-audit the measured bytes
python3 tools/verify_seed.py                     # whole-seed gate; A4's run.py is in the foundation list
```

## Firewall (binding)
γ/A4 read promoter **STRUCTURE only** — never a channel voltage, a transduction gain, a drug potency, a
dose, an in-vivo selectivity, or a clinical effect. This increment reads the wide-neighbourhood A4
**COORDINATE** (shell / anchor / loop / phase), still structure-only; **Layer-2** (cascade sign / runtime
fill / wiring) stays flagged, never assigned; nothing is diagnosed, treated, or prescribed, and no
molecule is designed. The felt percept of hearing is the **mind** volume's. Every absolute magnitude is
**[O]** with its obstacle named. **No number is tuned**: the wide region and the feature table are
**NCBI-measured** (cached, byte-exact, re-auditable); FLANK is one gene-independent constant; the B-DNA
geometry is the inherited LOCK.
