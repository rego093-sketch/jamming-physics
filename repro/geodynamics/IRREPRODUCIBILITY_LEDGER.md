# Irreproducibility Ledger — geodynamics (Constitution C3)

This paper contains **no [O]-graded (irreproducible) quantitative claims**. Every
quantitative result shown in `docs/geodynamics/` is deterministically reproducible
from the bundle engines in `src/geodynamics/atl_bundle/`
(`validate_all.py` → 39/39 PASS; fixed seeds; `SHA256SUMS.txt` verified).

## Reproducible headline results (NOT [O])

| Quantity | Value | Reproducing engine | Audited check |
|---|---|---|---|
| μ_eff (unjamming) | ≈ 2.2×10⁻³ (no melt) | `engine/vp_jamming_friction.py` | C1, C4–C5 |
| φ_jam | 0.840 (classical ≈ 0.842) | `engine/jamming_microderive.py` | C4 |
| z_iso (isostatic coordination) | 2d (= 6 in 3D) | `engine/jamming_microderive.py` | C4 |
| G_relaxed → 0 at isostaticity | Hessian, ∝ (z−z_iso) | `engine/jamming_shear_modulus.py` | C5 |
| V_crit (no slow-liquefied branch) | ≈ 10⁻²–1 m s⁻¹ | `engine/jamming_bistability.py` | C9a–C9c |
| Ω-NoGo floor | μ_eff hold-min = 10⁻² | `engine/omega_nogo_check.py` | Ω |

## Bounded HOLD items (insufficient evidence — distinct from [O] irreproducible)

These are **evidence gates**, not reproducibility obstacles. They reproduce as
*HOLD verdicts* (the engines run; the data needed to UNLOCK is not in hand):

- **Master-scale system extrapolation — HOLD** (§16). The material law reproduces;
  its application at continental scale awaits the master-scale constraint. This is a
  scientific evidence gate, not a calculation that the package cannot run.
- **Absolute break-up chronology — chronology firewall** (§20). The paper is
  chronology-agnostic: relative-time magnetic stripes reproduce, and the U–Pb
  absolute ages are conceded. No absolute-age number is claimed, so none is `[O]`.

## Statement

No `[O]` entries exist for this paper. If a future revision introduces a quantity
that is irreproducible inside the package (e.g., an HPC-gated absolute scale, as the
physics volume has for absolute *g* and α_em), it must be listed here with its
specific obstacle, and the corresponding figure must carry an `[O]` grade in the body.
