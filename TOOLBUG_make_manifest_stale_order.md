# TOOL BUG — `tools/make_manifest.py` ORDER/REL is stale (blocks registry regen)

**Found** 2026-06-25 during the DNA v1.18.1 merge close-out · **Severity** high (silent data loss)
**Status** reported only — NOT fixed here (tool edits require an approval session, VP-SPEC §1)

## Symptom
Running `python3 tools/make_manifest.py` against the current site regenerates
`registry/vp.manifest.json` with **30 volumes**, silently dropping **`continental-genesis`**
and **`recent-sequence-cascade`** — the two volumes created by the 2026-06-24 un-merge
(`lineage.jsonl`: "un-merged continental-genesis-cascade … 31->32 volumes"). The live `docs/`
contains both (`docs/continental-genesis/`, `docs/recent-sequence-cascade/`), and the homepage,
sitemap, `_decl`, repro, and the 32-volume backup manifest all carry them.

## Root cause
`make_manifest.py` hard-codes the volume set in two places (`ORDER` list and `REL` dict, ~lines
18–63). Both list 30 volumes and were not updated when the cascade/genesis un-merge raised the
count to 32. The builder iterates `for vid in ORDER`, so any volume absent from `ORDER` is omitted
from the regenerated manifest entirely (and from the primitive-membership counts).

## Impact on this merge
The canonical path to refresh the registry — update `tools/master.json`, run `make_manifest.py`,
regenerate the homepage — **cannot be used as-is**: it would regress 32→30 volumes. Therefore the
DNA registry update was done **surgically** instead (DNA row only): `pages` 18→29 and both
`content_sha256`/`repro_sha256` recomputed with the tool's **own** `dir_content_hash` function,
plus a continued `lineage.jsonl` entry. Verified by `tools/gate.py`:
- 32/32 slug-sets PASS (no volume dropped), lineage chain valid (14 entries), manifest self-hash OK,
- `dna` is **no longer** in the `content_sha256` drift list; `repro_sha256` now 32/32.

## What remains (the one residual site-gate failure — pre-existing, not caused by this merge)
`tools/gate.py` reports `content_sha256 integrity — drift: [29 volumes]` (everything except
`dna`, `continental-genesis`, `recent-sequence-cascade`). This is **pre-existing in the base**:
running `gate.py` on the pre-merge backup shows the same drift for **30** volumes (the 29 + `dna`),
i.e. the base shipped with stale content hashes for 29/32 volumes before this merge. Fixing all 29
cleanly is a one-command job **once this bug is fixed**:

```
# after adding 'continental-genesis' and 'recent-sequence-cascade' to ORDER and REL:
python3 tools/make_manifest.py "refresh content_sha256 baseline for all 32 volumes"
python3 tools/build_index.py        # regenerate homepage from the refreshed manifest
```

The surgical DNA hashes above were computed with the same `dir_content_hash`, so a correct full
regen will reproduce them identically for `dna` — no conflict.

## Fix (for the approval session)
Add the two volumes to `ORDER` (in their lineage positions: continental-genesis #7,
recent-sequence-cascade #8) and add their `REL` entries (continental-genesis inherits per its
`_decl`; recent-sequence-cascade inherits `continental-genesis`, per the recorded un-merge edge).
Then re-run `make_manifest.py` + `build_index.py`.
