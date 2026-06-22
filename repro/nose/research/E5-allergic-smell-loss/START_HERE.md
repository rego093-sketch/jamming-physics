# START HERE — increment E5  (the acquired disease layer)

The fifth emergence of the nose seed (see `BLUEPRINT.md` for the full plan). **BUILT (v0.6.2).**

> **Theoretical / NON-CLINICAL.** Mechanism-layer research only, **direction-only / proposal-only**
> (`FIREWALL.md` #4, #8): it does **not** diagnose, treat, screen, or prescribe; it designs no
> molecule and states no dose, potency, or efficacy. The felt experience is the mind volume's.

**Task:** the **acquired** disease layer — the sibling of E4's **congenital** anosmia, and the most
common real-world nose complaint: **allergic rhinitis** (Type-2 airway inflammation) and how it makes
you lose your **smell**. The honest point is that allergic rhinitis is **not** primarily an
olfactory-transduction or olfactory-development disease — it is an **immune** hypersensitivity. So the
VP discipline is to **consume** the allergy mechanism from the volume that owns it and derive **only**
the part that is genuinely olfactory.

**Consumed, not re-derived (one-way cite, `FIREWALL.md` #8):**
- the allergic **mechanism** — sensitization at the R19 spinodal, the dose×repetition threshold, the
  **latch**, and controlled **desensitization** (= allergen immunotherapy = basin-acting
  re-tolerization) — is the **immune/hematologic volume's §11** "Allergy: sensitization, the latch,
  and controlled desensitization", graded **[V]** there (**DOI 10.5281/zenodo.20755280**). E5 computes
  **none** of it (no priming, no tolerance accumulator, no crossover dose).
- the **absolute** airway aeroallergen load and mucosal scale are the **respiratory volume's [O]** (the
  immune volume itself defers the airway antigen scale to the surface owner). E5 owns **none** of it.

**Owned here — the olfactory-surface consequence (what no other volume can state).** Use the measured
reading in `inherited/organ_gamma.json` (the OR bank and the OSN-identity organisers) and the R19
switch + `Organ` in `inherited/vp_substrate.py`.

**Deliverable (done):** a deterministic module `research/E5-allergic-smell-loss/run.py` that shows
allergic rhinitis takes smell two ways, told apart by **one move — restore the drive**:
- **PART A — CONDUCTIVE** loss = a **drive suppression** (κ↓) on the **intact** E1/E2 switches: mucosal
  swelling reduces odorant flux, the OR panel flips OFF in spinodal(γ) order (E1's thermometer in
  reverse), and the percept fades to anosmia — but **restoring κ→1 recovers it EXACTLY**, because γ is
  untouched. **Reversible.** [F]/[V]
- **PART B — SENSORINEURAL** loss = an **organ degradation** on E2/E3: chronic inflammation drops the
  OSN compartment's master cis-drive below its γ-set R19 **presence** threshold (inherited `Organ`,
  "parts present ≠ trait"), so no receptor can carry a percept **regardless of κ** — the **same**
  organ-formation failure as E4, reached by inflammation instead of a Kallmann mutation. **Persistent.** [F]/[V]
- **PART C — the discriminator + the firewall in action:** restoring the drive (κ→1) recovers the
  conductive percept but **not** the sensorineural one; the substrate expresses the clinical
  conductive-vs-sensorineural split as **DRIVE (E1/E2) vs ORGAN (E2/E3)**. Direction-only restorative
  levers (sign only): conductive → κ↑ (restore access; the upstream allergic cause is the immune §11
  desensitization, cited); sensorineural → act on the **organ** (protect the epithelium), recovery not
  guaranteed. No dose/molecule/efficacy. The odorant key stays E1's [O]; the felt percept → mind volume.

It prints every number and self-hashes (2× run → identical sha256) and declares grades [F]/[V]/[L]/[O]
honestly. Plus `gate_E5.py` (`E5 GATE: PASS`), folded into the verifier's foundation list. The
inherited foundation stays **frozen** — E5 adds **no gene** (no new γ; the two DATA files are untouched,
no-regression).

**Firewall:** structure-only; γ is promoter structure, **never** a mucus/airflow value, a dose, or a
clinical effect; **κ (the conductive factor) and the organ degradation are abstract structural
representations** (κ is not a measured airway value — that scale is the respiratory volume's [O]; the
organ loss is the inherited Organ presence mechanism, not a measured cell count); the **allergy
mechanism is consumed from immune §11**, not re-derived; the disease layer is **proposal-only**; the
felt percept is the mind volume's.

**Next:** `BLUEPRINT.md` → grow the verified E0–E5 research base into the full multi-chapter **HTML
volume** (VP-SPEC v1.8 §6) — every displayed number reproduced deterministically, the disease layer
(congenital E4 + acquired E5) proposal-only, the odorant-identity [O] named throughout, the allergy
mechanism cited to immune §11 — delivered, as always, as **one zip**.
