# E_NUMBERING — folder labels ⟷ BLUEPRINT-canonical numbers (RECONCILED, v0.11.0)

This document closes **open item #4** (the E-numbering reconciliation, flagged since v0.3.0). It is the
authoritative, human-readable companion to the machine-readable map `e_numbering.json`, which is
enforced by `tools/verify_seed.py` block **[5]** so the labels can never silently drift again.

## TL;DR
Research **folders** are numbered in **chronological build order** (`E1, E3, E4, E5, E6, E7, E8` — the
order they were built; `E2` was never used as a folder label because the first folder built took `E1`).
This coincides with the **BLUEPRINT-canonical** numbering for **E3/E4/E5/E7/E8**, and differs in
**exactly two** places, by design:

| folder (on disk) | folder label | BLUEPRINT-canonical | what it actually contains |
|---|---|---|---|
| `research/E1-place-and-traveling-wave/` | **E1** | **E2** | the MET tip-link switch (TMC1/PCDH15/CDH23) on the place map |
| `research/E6-traveling-wave-envelope/` | **E6** | **E1** | the traveling-wave **envelope** (the named [O], characterised in Q) |
| `research/E3-cochlear-amplifier/` | E3 | E3 | the cochlear amplifier (prestin), cube-root |
| `research/E4-congenital-deafness/` | E4 | E4 | congenital deafness — the four failure classes |
| `research/E5-readout-synapse/` | E5 | E5 | the otoferlin readout sensor |
| `research/E7-audible-band/` | E7 | E7 | the audible band (geometry-carved bandpass) |
| `research/E8-band-specific-loss/` | E8 | E8 | band-specific hearing loss (class × place) |

So the slip is a single **swap** at the folder level: **BLUEPRINT-E1 (envelope) lives in folder `E6`**,
and **BLUEPRINT-E2 (MET switch) lives in folder `E1`**. Nothing else is mislabelled.

## The BLUEPRINT-canonical numbering (the scientific spine)
- **E0** — inherited foundation: sound = √(B/ρ) longitudinal wave, the Greenwood place map, the R19
  substrate, the DNA reading γ(LEVEL)+A4(SHAPE). *(Lives in `inherited/`, not a research folder.)*
- **E1** — the fluid-loaded dispersive **traveling-wave envelope** — the named open obstacle the seed
  exists to take up. **Carried by folder `E6-traveling-wave-envelope`** (built v0.7.0; characterised as a
  one-parameter family in Q, Q the single irreducible [O]).
- **E2** — the hair-cell **mechanotransduction tip-link MET switch** (TMC1/PCDH15/CDH23/TMIE) = the R19
  switch on the place map. **Carried by folder `E1-place-and-traveling-wave`** (built v0.3.0).
- **E3** — the active **cochlear amplifier** (prestin/SLC26A5) = the R19 cubic at criticality. *(folder `E3`)*
- **E4** — congenital **DEAFNESS** (the goal) = the cubic's failure-mode decomposition. *(folder `E4`)*
- **E5** — the **READOUT** substrate (otoferlin/OTOF) = a rectified saturating Ca²⁺ sensor. *(folder `E5`)*
- **E7** — the **audible BAND** = a geometry-carved bandpass on the inherited wave law. *(folder `E7`)*
- **E8** — **band-specific** hearing loss = E4's class axis × E7's place axis. *(folder `E8`)*

> **There is no BLUEPRINT-canonical `E6`.** `E6` exists only as a folder label (the chronological slot
> after E5), and that folder carries BLUEPRINT-**E1** (the envelope). The canonical list runs
> E0, E1, E2, E3, E4, E5, E7, E8 — with no E6.

## Why the folders are NOT renamed
Renaming `E1-place-and-traveling-wave` → `E2-…` and `E6-traveling-wave-envelope` → `E1-…` would be the
"obvious" fix, but it is rejected for concrete reasons that outweigh the cosmetic gain:
1. **No-omission.** Every path is enumerated in `COMPLETENESS_MANIFEST.md` and `seed.json` `completeness`;
   a rename rewrites those paths and risks a missing-artifact gate failure if any reference is missed.
2. **Foundation paths.** `seed.json` `foundation_modules` and the volume SSOT loader
   (`volume/tools/vp_numeric_ssot.py`) import several `run.py` files **by path**; a rename must thread
   through all of them atomically.
3. **Deposited cross-links.** Sibling/site releases and the v0.10.0 HTML volume already reference these
   folder names; a late rename desynchronises external links for no scientific benefit.
4. **The chronological convention is itself coherent** — `E3/E4/E5/E7/E8` already match, and the
   build-order reading is honest. The only cost is two off-by-mapping labels, which this map fixes
   permanently and *checkably*.

The frozen-hash lineage is **not** the blocker (only the eight `inherited/` artifacts are hash-frozen, and
none of them is a research folder) — the blockers are no-omission, the foundation paths, and external
cross-links. The chosen reconciliation respects all three.

## How the reconciliation is enforced
`tools/verify_seed.py` block **[5] E-NUMBERING CONSISTENT** loads `e_numbering.json` and asserts, with no
network:
- every `research/E*/` folder on disk is listed in the map, and the map lists no phantom folder
  (set-equality, both directions);
- every mapped folder's `run.py` exists **and** is registered in `seed.json` `foundation_modules`;
- the `blueprint_E` assignment is an **injection** — no two folders claim the same canonical increment;
- the two recorded slip pairs (`E1`↔`E2`, `E6`↔`E1`) match the folders table exactly, so an accidental
  "silent fix" or any future drift trips the gate;
- each non-null `carrier_folder` in `blueprint_canonical` round-trips to a real folder entry.

If a future session **does** physically rename a folder to make the label match the BLUEPRINT, it must
update `e_numbering.json` in the same change — block [5] will fail until the map and the filesystem agree
(deliberate, never silent — the same discipline as the inherited re-freeze).

## Status
**Open item #4 is RECONCILED** — the labels are now unambiguous, documented, and machine-checked. No
inherited byte changed; no number changed; no folder renamed. The naming notes previously scattered across
`BLUEPRINT.md`, `WORK_HANDOVER.md`, and the chapter status blocks now defer to this file as the authority.
