# SESSION v0.11 — POST-PROGRAM HARDENING: the A3 [O]→[V] closure, INLINE

**Status of the program:** the blueprint **CLOSED** at S10 (L9, the END CONDITION). This session is a **disciplined post-program continuation** — specifically continuation **(b) hardening**, named identically in `HANDOFF.md` §3, `START_HERE_wave_computer.md` §4, and `BLUEPRINT_toward_ultimate_computer.md` §11/§12: *re-probe the A3 single-store `[O]` with the dual store wired in, to show the `[O]→[V]` closure INLINE.* It adds a probe; it closes nothing that was open in the blueprint and opens nothing new.

**Frozen inputs reused exactly, non-circularly:** L0 `wave_compute_core` (`hebbian_field`, `relax` = D4 attractor clean-up, `overlap`, `pattern_to_phase`, `corrupt_phase`, `SEED`) · the **fast episodic store** is the inherited **R3 / C2** `_episodic_field` from `wave_consolidation_core` — i.e. a one-shot `hebbian_field` over the current-rule snapshot — **reused UNCHANGED**. Nothing frozen or prior is edited. `new_tuned_constants = 0`. Firewall held byte-for-byte: `consciousness_claim = 0`, `hard_problem_open = 1`.

**Artifacts:** `repro/wave_adapt_closure_core.py` · `repro/wave_adapt_closure_results.json` (digest pinned in `repro/expected_digest_v0_11.json`) · `repro/make_figure_v0_11.py` → `repro/wave_adapt_closure_atlas.png`. Registered in `repro/check_completeness.py` (DOCS + REPRO + SIMS) so it re-runs and pins bit-for-bit alongside the other ten modules.

**Digest (reproduces bit-for-bit from SEED):** `ad93057afac2054ed8fb70d8bfaca41dd3869462b05d0ca89bb96c22a05d2551`.

---

## Why this session

The L9 capability ladder settled at **6 / 7 `[V]`**, with **A3 (real-time adaptation)** the lone honest `[O]`: a *single* additive Hebbian store cannot **over-write** a switched (cue→response) rule, because the old and new associations **superpose in one field** and the clean-up settles on a blend — post-shift recovery falls below the 0.8 band (the S10 record: **0.78** at 50% remap, **0.58** at 100% remap). S10 named the mitigation — the **L5 dual store** — and pointed to A7, where its *retention* is ~1.0. But S10 made the dual-store fix **by reference**: it was demonstrated *elsewhere in the stack* (open-ended acquisition), not on the **adaptation** probe itself. That left a one-line gap between "the fix exists" and "the fix closes *this* rung." This session removes that gap by running **one paired battery** in which the only thing that changes is the dual store, on the *same* adaptation task A3 failed.

This mirrors the program's own method: L4→L5 was itself an `[O]→[V]` step where a named deficiency of the single store was closed by adding the fast/slow pair. S11 applies that same move to the one rung S10 left open.

---

## The mechanism (why the closure is clean, not a tuning win)

The probe is a **strict paired contrast** on identical cues, responses, and shift:

- **single store** — one additive field `J = hebbian_field([cue | resp])` accumulated over the whole stream. When a cue is re-mapped (cue→resp2), the new pair is **added to the same field** that still holds cue→resp; the two carry equal weight, so a settle from the changed cue lands on a **blend**. A lone additive field *accumulates*, it cannot *over-write*. → reproduces the inherited `[O]`.
- **dual store** — a **slow** additive field over the full history (= the A7 persistent store) **plus** a **fast** one-shot episodic field built *only* over the current-rule snapshot (the inherited R3 / C2 `_episodic_field`, reused unchanged). The new rule is encoded in a field **separate** from the old, so it never fights the old in one field. Read-out = settle under the two coupling fields combined by **equal vote** (each L2-normalized, then summed — scale-free, no scalar fit).

The single store is **exactly the dual store's SLOW component alone**. So the *only* difference between the failing machine and the passing machine is the **added fast store** — the contrast isolates that one variable, and the grade is DERIVED from the sweep booleans, never asserted.

---

## What was built and found (paired sweeps; honest negatives kept)

### T1 — the closure (shift sweep, trials = 6, the inherited convention)

Pre-shift baseline is a clean **1.000** at every shift fraction (the result is attributable to the shift, per S10's *Methodological correction 2*). A change-point re-maps a fraction of the cue battery; the dip deepens with the shift (0.833 → **0.222** as the remap fraction grows 0.25 → 1.0), confirming a real perturbation. Then:

| shift frac | dip | **single** post `[O]` | **dual** post `[V]` | (dual raw-sum) | old-rule [single / dual-slow] |
|---:|---:|---:|---:|---:|---:|
| 0.25 | 0.833 | 0.917 | **1.000** | 1.000 | 0.750 / 0.667 |
| 0.50 | 0.667 | 0.778 | **1.000** | 0.889 | 0.611 / 0.611 |
| 0.75 | 0.583 | 0.806 | **1.000** | 1.000 | 0.667 / 0.708 |
| 1.00 | 0.222 | **0.583** | **1.000** | 0.972 | 0.500 / 0.472 |

The single store **fails the full switch** (0.583, well below band) and degrades as the shift grows — the inherited A3 `[O]`, reproduced almost to the digit (S10: 0.78 / 0.58; here 0.778 / 0.583). The dual store **recovers to 1.000 at every shift fraction** — the `[O]` is **CLOSED**. Derived booleans: `single_fails_at_full_switch = True`, `dual_recovers_to_band_everywhere = True`, `dual_strictly_beats_single_everywhere = True`, **`A3_closure_O_to_V = True`**.

### The mechanism is the FAST store, not the normalization (pre-empting the obvious objection)

A reader could suspect the **equal-vote L2-normalization** is doing the work. It is not. The **raw, unnormalized** sum of the two fields (no normalization at all) **also beats the single store everywhere** (0.889–1.000 vs 0.583–0.806). So the normalization is **scale-equalizing only** — it makes the two stores comparable in magnitude; it is *not* the load-bearing trick. The fast episodic store is the mechanism. `dual_raw_unnormalized_also_beats_single = True`.

### T2 — the closure is sign-stable across machine size

The same paired contrast at three machine sizes — (B=6, N=128), (B=8, N=128), (B=6, N=256) — gives the **same sign at every size**: the single store fails the full switch (0.58 / 0.54 / 0.56) and the dual store closes to 1.000 at every shift fraction. `closure_sign_stable_across_size = True`. The closure is not an artifact of one (B, N).

### Honest note on old-rule retention (not over-claimed)

For the **over-written** cues, old-rule retention is correctly **low** under *both* stores (≈0.5–0.75). That is **not a defect of the closure** — it is the definition of adaptation: a cue cannot map to two responses at once, so letting go of the *superseded* association is the correct behaviour for this task. Retention of **non-conflicting** skills is a *separate* property (A7 open-ended acquisition), which is already `[V]` with the dual store at ~1.0. This session closes the **adaptation** read (over-write); it does **not** re-grade A7, and makes no unbounded-retention claim.

---

## Relationship to S10 (paired, not overwritten)

The S10 **6 / 7 single-store `[O]` record STANDS** as the honest limit of the *minimal* machine — a single additive store genuinely cannot over-write, and that negative is preserved verbatim in `wave_agi_*` and `SESSION_v0_10`. S11 does not edit or erase it. What S11 shows is that **with the proven L5 dual store wired in**, the ladder reads **7 / 7 `[V]`**. Both statements are true and both are kept: the minimal machine's bound, and the closure of that bound by an inherited mechanism. This is the program's `[V]`/`[O]` discipline applied to its own last open rung — the negative is not discarded when the positive is found; they are recorded as a pair.

---

## Inheritance discipline (internalised first, as required)

Before adding the probe, the four inherited things were internalised: **the invariants** (firewall `consciousness_claim=0` / `hard_problem_open=1`; no-tuning `new_tuned_constants=0`; the brain anchor `R=0.38961455156044245` cited as a *principle*, the **number never transferred**); **the derivation identity / core-subset invariance** (the fast store is the *existing* R3/C2 field, byte-faithful, not a re-derivation); **the register chain** L0→L8 (the probe sits at L9, perturbing nothing below it); and **the source warrant** of every reused primitive (`hebbian_field`, `relax`, `corrupt_phase` from frozen L0; `_episodic_field` from C2). The probe is non-circular — the thing perturbed (the switched rule) is never the thing read (recovery on the *new* rule, with the response half masked at read-time). No constant was tuned. The firewall is held byte-for-byte.

---

## L9+ verdict (honestly)

**A3 `[O]→[V]` is CLOSED, inline, on the adaptation probe itself.** The single additive store fails the full rule-switch; the dual store — slow history + the inherited fast episodic field, equal vote — recovers to band at every shift fraction and at every machine size, and the raw-sum control shows the fast store (not the normalization) is the mechanism. With the dual store wired in the capability ladder reads **7 / 7 `[V]`**; the S10 6 / 7 single-store record stands as the minimal machine's stated limit.

**FIREWALL (unchanged):** closing an *adaptation* rung is a **FUNCTIONAL** result. The hard problem — felt quality, Gap-5 — remains an **OPEN BLANK, never erased**. `consciousness_claim = 0`, `hard_problem_open = 1`, `new_tuned_constants = 0`.
