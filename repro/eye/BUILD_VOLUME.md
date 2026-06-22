# BUILD_VOLUME — the multi-chapter HTML volume (START HERE)

**What this is.** The publication layer that turns the finished down-conversion spine **E0→E8** into a
readable, machine-checkable, retrieval-ready website under `docs/eye/`. It adds **no physics and no
tuning** — it *publishes* the increments. The one rule it enforces, end to end: **every number you can
read on a page is the code's own output**, hash-pinned to the `run.py` that produced it, with HTML↔code
**drift 0**.

## Build it, then gate it
```
python3 tools/build_volume.py     # render docs/eye/ FROM each chapter's run.py   → BUILD VOLUME: DONE
python3 tools/gate_volume.py      # independent re-proof, HTML↔code drift 0       → VOLUME GATE: PASS
python3 tools/verify_seed.py      # the package's one-command gate (no-omission)  → SEED VERIFY: PASS
```
The build is deterministic: the `run.py` outputs are SEED-pinned with no RNG/clock, and the templating is
pure string ops, so re-running produces byte-identical files. `build_volume.py` clean-rebuilds `docs/eye/`
each time (no stale files survive).

## How "the numbers are the code's own" is actually enforced
1. **Single source.** `build_volume.py` *runs* each chapter's `run.py` and captures its **verbatim**
   stdout. That transcript is the chapter's single source of truth.
2. **The page shows the real run.** The transcript is embedded inside each page as
   `<pre class="transcript" data-run="…" data-sha="…">…</pre>` (inside a `<details>`), pinned to its
   sha256. Nothing is hand-transcribed.
3. **Prose numbers are gated at build time.** Any number that also appears in the prose is wrapped in
   `F("…")`, which **asserts** the exact string is a substring of that live transcript. A typo'd or
   invented number raises at build time — the volume will not build. Each surfaced number is also written
   to `docs/eye/facts/<slug>.json` (with the run shas) as the machine-readable ledger.
4. **The gate re-proves it from the shipped files** (so a later hand-edit of any HTML is caught), with
   seven independent checks:
   - **G1 determinism** — each `run.py`, run twice, is byte-identical.
   - **G2 code→facts** — the live transcript sha equals the sha recorded in `facts/*.json`.
   - **G3 page→code** — the embedded `<pre>`, un-escaped, is byte-identical to the live run (sha three
     ways). **This is the drift-0 check.**
   - **G4 fact drift-0** — every surfaced number is present verbatim in BOTH the live transcript AND the
     rendered HTML.
   - **G5 firewall** — the rendered **E4** disease chapter carries **none** of E4's own `MAGNITUDE_BLOCK`
     tokens and no `%`. Proposal-only holds in the prose, not just the transcript.
   - **G6 retrieval** — every page is static and machine-readable: `<h1>`, `<link rel=canonical>`, a
     JSON-LD block, and **every** `<script>` is `type=application/ld+json` (no executable JS).
   - **G7 no-omission** — every file in `expected_files()` exists.

The gate is **non-vacuous** (and that was checked): corrupt a prose number and **G4** fails; flip a single
byte inside an embedded transcript and **G3** fails.

## The firewall (E4 only)
The disease chapter stays **proposal-only**. E4's `run.py` already guarantees its *transcript* never prints
a clinical magnitude (the `MAGNITUDE_BLOCK` tuple in `research/E4-congenital-blindness/run.py`, quoted
verbatim by the tooling — never re-typed — plus no `%`). The builder adds no forbidden token to the E4
*prose*, and **G5** re-checks the *rendered* E4 chapter. The other chapters (E5/E7/E8) legitimately contain
`%` and are not firewalled. The shared page footer is worded to avoid magnitude vocabulary so it is safe on
every chapter, E4 included.

## The shared library
`tools/_volume_lib.py` is the single source for the builder and the gate: `run_capture` (subprocess, repo
root, verbatim stdout), `sha256_text`, `esc`/`unesc` (exact inverses over only `& < >`), `attr`, the
`VOLUME` chapter manifest (slug / number / title / one-liner / which `run.py` feeds the chapter),
`chapter_by_slug`, `expected_files`, `META`, and `load_magnitude_block()` (imports E4's `run.py` to read
its `MAGNITUDE_BLOCK` **verbatim**, so the firewall token list can never drift from the code it guards).

## Scope / lane
This package ships the **rendered volume as one zip**. The official live-site merge — the canonical
`paper_id`, the `301` redirects from old URLs, and registering the volume in the cross-volume DOI registry
— is a separate **VP-SPEC Phase 5** step done against the live site, and is deliberately **not** in this
package. Adding it here would couple the seed to site state it cannot verify offline.

## If a number ever changes
Don't edit HTML by hand. Edit the responsible `run.py` (it is the source), then re-run
`python3 tools/build_volume.py`. The new number flows into the transcript, the embedded `<pre>`, the prose
`F()`-gate, and `facts/*.json` together — there is no second place to update, so they cannot disagree.
