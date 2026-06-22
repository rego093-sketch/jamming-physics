# START HERE — increment E4  (the goal)

The fourth emergence of the nose seed and its **goal layer** (see `BLUEPRINT.md`). **BUILT (v0.6.0).**

> **Theoretical / NON-CLINICAL.** Mechanism-layer research only. This increment is **direction-only /
> proposal-only** (`FIREWALL.md` #4): it does **not** diagnose, treat, screen, or prescribe; it designs
> no molecule and states no dose, potency, or efficacy. The felt experience of anosmia is the mind
> volume's.

**Task:** read congenital **anosmia** from the FROZEN substrate as the substrate's **two R19 failure
modes**. The congenital-anosmia genes split cleanly: **CNGA2, CNGB1** (CNG channelopathy →
transduction-switch failure) and **ANOS1, FGFR1, PROKR2, PROK2** (Kallmann → organ-formation failure).
Use the measured γ in `inherited/organ_gamma.json` (CNGA2/CNGB1/ANOS1/FGFR1 inherited; **PROKR2/PROK2
fetched from NCBI and folded in at v0.6.0**) and the R19 switch + `Organ` in `inherited/vp_substrate.py`.

**Deliverable (done):** a deterministic module `research/E4-congenital-anosmia/run.py` that
(A) reads the **two failure modes** — (1) a CNG loss-of-function removes the bistable switch so the
all-or-none transduction flip can never occur (the WT switch flips past h*; deleting it destroys the
flip, ≈229×); (2) a Kallmann loss-of-function leaves the master switch unable to clear its R19
presence threshold, so the OSN/bulb never emerges ("parts present ≠ trait"), with the anosmia +
hypogonadotropic-hypogonadism signature — each with a **direction-only** inverse-lever (the SIGN of a
hypothetical restorative move, no dose/molecule/efficacy); (B) the **cross-sense** result — CNGB1 γ is
byte-identical to rod vision, so a CNGB1 LOF is predicted to impair **both** smell and rod (dim-light)
vision, forced by the shared switch; (C) the **firewall in action** — restating that every line is
direction-only / proposal-only, the odorant key stays [O], and the felt percept is the mind volume's.
It prints every number and self-hashes (2× run → identical sha256) and declares grades [F]/[V]/[L]/[O]
honestly. Plus `gate_E4.py` (`E4 GATE: PASS`), folded into the verifier's foundation list. The
inherited foundation stays **frozen** (the two data files were re-frozen when PROKR2/PROK2 were added).

**Firewall:** structure-only; γ is promoter structure, **never** a channel current, dose, potency, or
clinical effect; the order-parameter s is the abstract R19 field; the `_linear_control` shows what
losing the switch costs (it does not fork the substrate); the disease layer is **proposal-only**; the
absolute restorative magnitude is an [O] this volume deliberately does **not** supply; the felt percept
is the mind volume's.

**Next:** `BLUEPRINT.md` → **E5 — allergic (acquired) smell loss** (built v0.6.2): allergic rhinitis's
effect on smell, with the allergy mechanism **cited to the immune §11** (not re-derived) and only the
olfactory consequence derived (conductive drive-suppression vs sensorineural `Organ` degradation). Then
grow the verified E0–E5 research base into the full multi-chapter **HTML volume** (VP-SPEC v1.8 §6) —
every displayed number reproduced deterministically, the disease layer proposal-only, the
odorant-identity [O] named throughout — delivered, as always, as **one zip**. (The OR panel is already
complete: **OR2W1** was measured from NCBI and folded in at v0.6.1, so `_to_measure` is empty; the felt
percept and the absolute odorant→Hz scale remain the mind volume's / a named [O].)
