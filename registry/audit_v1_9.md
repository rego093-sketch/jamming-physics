# VP-SPEC v1.9 — Audit: Redundant Inheritance & Term Inconsistency (RESOLVED)

Reproducible: `python3 tools/audit_terms.py`. Structural items enforced by the gate
(REQUIRED + BODY, 30/30). Grade decisions below were taken by reading each term's
context across all 30 volumes (delegated), then applied; the dictionary is the SSOT.

## A. 중복상속 (redundant inheritance) — FIXED, CLEAN (A1–A4)

Owner *self-inheritance* (a volume "inheriting" a module it originates) was the real
bug: physics inherited `[kernel, light_emergence]`, dna inherited `[dna_interpretation]`.
Fix: added `owns_modules` (= module whose first-canonical volume is this paper);
**originate xor inherit**. Strips now render `Defines:` (owns) + `Inherits:` (consumed):
- physics → `Defines: R19 switch, Quantum light`
- dna → `Defines: DNA interpretation | Inherits: R19 switch`
- fluid-dynamics → `Defines: Rotor inflow | Inherits: R19 switch`; cosmology = pure consumer.

A1 self-inheritance · A2 dup ids · A3 owns∩uses · A4 owns∩inherits modules: **all CLEAN.**
Not bugs (noted): `event_quantum` distinctive to light+rotor (no misassignment in practice);
module + owner-volume co-inheritance (complementary axes).

## B. 용어 불일치 (term inconsistency)

### B1. Mislabels — FIXED (wrong aka over-capturing unrelated cards)
- `c2_brho ← "c"`: 4 neuro EM cards ("oscillating ionic charge → field") → aka removed; untagged.
- `r19_switch ← "kernel"`: 9 Kramers-rate cards → aka removed, **retagged to `kramers`** (link `/concepts/#kramers`).
- `node_atlas ← "node-decomp"`: 1 hemodynamic card ("MAP = CVP + CO × SVR") → aka removed; untagged.

### B2. Method/discipline terms carrying claim grades — RESOLVED
Earlier flags `grades`[F,L,O,V] and `magnitude_firewall`[O,V] were **false positives**
from the dictionary's own legend/definition page (now excluded) and from secondary
firewall brackets (audit now reads the PRIMARY grade only). Remaining `seam`[F] and
`A4`[O] are method/admissibility terms whose single context grade is legitimate; both
carry a `grade_note` recording this (seam wiring [F] = structural necessity; A4 [O] =
open magnitude of a specific coordinate, not the axis). **0 undocumented.**

### B3. Same claim concept graded differently across volumes — RESOLVED (decided by corpus read)
Real conflicts were normalized to the grade that matches each term's actual epistemic status:

| term | was | now | rationale | cards fixed |
|---|---|---|---|---|
| **gamma** | F / L / V | **[V]** | γ is a *measured* material constant (SantaLucia 1998, NCBI) — never forced or calibrated; this is the framework's "no-tuning" anchor | 6 (neuro×3, immune×2, nose×1) |
| **theta_gamma** | F / V | **[V]** | θ/γ is *computed* ≈6.1 and *verified* within the empirical 7±2 band — not forced to 7 | dict + 2 (neuro) |
| **fhn** | F / V | **[V]** | FitzHugh–Nagumo = R19 cubic **+ a recovery variable** (a modeling step); "forced" overclaims the bare kernel | 3 (cardioresp) |
| **mp_me** | F / O | **[F]** | mₚ/mₑ = 6π⁵ is π-forced (2π·ν_p); the −19 ppm is an honesty caveat, not an "open" downgrade | 1 (chemistry) |
| **node_atlas** | F / V | **[F]** | the [V] card was a hemodynamic mislabel (see B1) — atlas itself is the forced SSOT | (mislabel removed) |
| **c2_brho** | F / V | **[F] + note** | c²=B/ρ is *forced* by the elastic-wave kernel and *verified* to 0.06 % in chemistry §2 — a **legitimate context split**, documented via `grade_note`, both cards kept | kept (documented) |

After fixes each term is single-grade across volumes (gamma/theta_gamma/fhn = [V],
mp_me = [F]); c2_brho is the one intentional, documented [F]/[V] split. **0 undocumented conflicts.**

### B4. Formula-notation drift — REVIEWED (no scientific error)
- Cosmetic only (encoding/precision): `spinodal` `^1.5`≡`^{3/2}`; `nu_p`/`mp_me` numeric tails;
  `barrier` entities; `jammed_substrate` wording. `gamma_exemplars` 1.2414/1.4598/1.4933 is
  **correct** (RUNX2/SOX9/MYOD1 — a deliberate exemplar set, not one value).
- `r19_switch`: `g·s−s³+h` (general kernel; control `g`) vs `γ·s−s³+h` (1 biological-instantiation
  card where `γ` plays the control). Both legitimate; the general form `g` stays canonical.
- LHS symbol choices (`barrier` ΔV₀/ΔV/B; `spinodal` h\*/s\*/h_sp) are left as-is — every card
  links to the dictionary entry, which holds the canonical symbol. Not auto-edited (no error).

## What changed (this audit)
- `_decl.json` ×30 + strips regenerated with `owns_modules` (Defines/Inherits).
- `concepts.json`: removed misleading akas `c2_brho←"c"`, `r19_switch←"kernel"`, `node_atlas←"node-decomp"`;
  `theta_gamma` grade [F]→[V]; `grade_note` added to gamma, theta_gamma, c2_brho, seam, A4.
- Card regrades inside the relevant asides: gamma→[V] ×6, theta_gamma→[V] ×2, fhn→[V] ×3, mp_me→[F] ×1.
- Retag: 9 Kramers cards → `kramers`; untagged 4 neuro EM ("c") + 1 hemodynamic ("node-decomp").
- `retrofit_cards.py` authoritative (data-concept == canonical(data-locked); fixes stale/duplicate).
- `audit_terms.py` refined: PRIMARY-grade extraction, dictionary page excluded, `grade_note`-aware.
- **Final: audit A1–A4 CLEAN · B1 CLEAN · B2 0 · B3 0 undocumented · gate REQUIRED 30/30 + BODY 30/30.**
