# Cross-Volume Concept-DOI Registry

> VP-SPEC v1.7+ artifact (Constitution cross-reference layer). The nine jamming-physics.org
> whitepapers share one canonical site; each volume's hub links its siblings by **concept DOI**
> (the version-independent Zenodo identifier that always resolves to the latest version). This table
> is the single source for those links. Built **verbatim from VP-SPEC v1.8 Ch.2 registry** —
> no web re-research (Ch.2 / Ch.10 rule: a session uses only the registry row for its paper).
>
> Current volume: **fluid-dynamics** (`flu`) — *The Configured Continuum*.

## Registry

| paper_id | code | short | concept DOI | headline result | branch |
|----------|------|-------|-------------|-----------------|--------|
| physics | phy | VP Theory | [10.5281/zenodo.17932566](https://doi.org/10.5281/zenodo.17932566) | c² = B/ρ ; m_p/m_e = 6π⁵ (−19 ppm) | foundation |
| **fluid-dynamics** | **flu** | **Configured Continuum** | [**10.5281/zenodo.17972568**](https://doi.org/10.5281/zenodo.17972568) | ∂ρ/∂t + ∇·(ρu) = 0 ; ρ Du/Dt = ∇·T | **jamming ← this volume** |
| cosmology | cos | Vacuum-Inflow Cosmology | [10.5281/zenodo.20568874](https://doi.org/10.5281/zenodo.20568874) | a₀ = cH₀/2π ≈ 1.08×10⁻¹⁰ m s⁻² | inflow |
| geodynamics | geo | Jamming Geodynamics | [10.5281/zenodo.17978934](https://doi.org/10.5281/zenodo.17978934) | Ψ_eff > Ψ_y | convergence (jamming + geochronology) |
| dna | dna | 4D DNA Blueprint | [10.5281/zenodo.20471407](https://doi.org/10.5281/zenodo.20471407) | form ← γ (Layer 1) ; quantity ← φ (Layer 2) | jamming |
| geochronology | chr | Cross-Chronometer Limit | [10.5281/zenodo.20568673](https://doi.org/10.5281/zenodo.20568673) | foreign(old) incorporation ⇒ age old-biased | methods (convergence support) |
| chemistry | chm | VP Chemistry & EM | [10.5281/zenodo.20680540](https://doi.org/10.5281/zenodo.20680540) | c²=B/ρ (0.06% sim) ; arccos(−1/3) ; φ_RCP=0.7405 ; d-band catalysis | jamming (cites physics Vol I) |
| neuro | neu | Neural Emergence Chain | [10.5281/zenodo.17979015](https://doi.org/10.5281/zenodo.17979015) | working-memory capacity ≈ θ/γ (7±2) ; tACS causal | branch (own chain) |
| mind | mnd | Felt Cognition | [10.5281/zenodo.20694404](https://doi.org/10.5281/zenodo.20694404) | stream = θ-frame serial selection ; hard problem OPEN | frontier (cites neuro, one-way) |

## Latest-version resolutions (Zenodo, confirmed 2026-06-15 per Ch.2)

The concept DOI resolves to the most recent version. As recorded in the spec, the v1.7-added trio
resolve as: **chemistry → 10.5281/zenodo.20680541 (v1.0)**, **neuro → 10.5281/zenodo.20694299 (v2)**,
**mind → 10.5281/zenodo.20694405 (v1.0)**. Confirmed site slugs: `neuro=/neuro`, `mind=/mind`;
`chemistry` slug unconfirmed at spec time. The original six (physics, fluid-dynamics, cosmology,
geodynamics, dna, geochronology) use their paper_id as the site slug.

## Branch topology (how this volume relates to its siblings)

- **physics** is the foundation; **fluid-dynamics** sits on the **jamming** branch and shares the
  substrate anchor `c² = B/ρ` with physics (Vol I) and chemistry.
- **geodynamics** is a convergence volume linking the jamming branch and the geochronology method.
- **mind** is a one-way frontier citing **neuro**; **chemistry** cites **physics** Vol I.

The machine-readable form of this table is `registry/cross_volume_doi.csv` (10 columns, 9 rows),
which additionally carries `code`, `full_title`, `resolves_to_latest`, `site_slug`, and
`is_current_volume`.

_Generated for the VP-SPEC v1.8 upgrade of the fluid-dynamics distribution (2026-06-15)._
