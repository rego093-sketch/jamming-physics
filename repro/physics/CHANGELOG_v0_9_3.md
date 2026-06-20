# CHANGELOG v0.9.3 — Gravity §17.4: spatial reproduction merged, reproducibility guaranteed

## Summary
§17.4 is upgraded from a derived-mechanism-with-external-magnitude treatment to one whose **spatial
structure is reproduced against measurement**, with a sha256-frozen reproducibility pipeline and a
recorded residual map. The existing mechanism content (inflow, cap, four-wall theorem, Beverloo
height-independence, EP) is preserved verbatim; only integration points were revised.

## Changes
- **§17.4 title / claim-strip**: scope widened to inflow + cap + terrain field; spatial reproduction asserted.
- **§17.4.3**: revised — the framework now addresses BOTH the cap (surface magnitude) and the
  inverse-square kernel (spatial structure, validated in §17.4.7). Previously "addresses only the cap."
- **§17.4.6**: quantitative body scaling added — g_(*) ∝ ρ_eff·R gives Moon 1.62 m/s² (1/6, no coefficient);
  gas-giant multi-layer Σ g_cap·η.
- **§17.4.7 (NEW)**: "Spatial reproduction against measurement" — free-air −0.3079 mGal/m (+0.24%),
  latitude = Somigliana (rotation 65% + oblateness 35%), real-DEM terrain correction 0.00 mGal vs
  Newtonian (Pikes Peak TC = 21.46 mGal, 1089 SRTM points), ⟨cosθ⟩ scale-separation, direct-sim
  impossibility (3.6×10⁵⁴ samples), and the **residual map** (R-FA/R-TC/R-MN/R-ISO). Eqs phy-17-085..087.
- **§17.4.7→17.4.8**: old "Honest summary" renumbered and reframed (spatial structure reproduced;
  one external scalar); self-deprecating clause removed, honest [O] on absolute g retained.
- **W.0 scorecard**: gravity row → 5 rows (free-air, terrain, latitude, body-scale, cap+absolute).
- **W.6 provenance**: gravity row → 3 rows (G/S/M).
- **Reproducibility (NEW)**: tools/vp_gravity_ssot.py (canonical regenerator + drift gate),
  frozen DEM (tools/dem_Z.npy, sha256=bbe987307d5dcbb9…), tools/fetch_dem.py, tools/tc_compute.py,
  docs/GRAVITY_NUMERIC_LEDGER.md, reports/gravity.gate.json,
  verification_dossier/GRAVITY_REPRODUCIBILITY_MAP.md.
- **Equations**: phy-17-085..087 added to manifest/physics.eq_list.tsv and rendered to docs/eq/physics/.
- **manifest/physics.csv**: chapter 17 eq_display 85→88, word count updated.

## Reproduce
```
python3 tools/vp_gravity_ssot.py            # ledger + residual map
python3 tools/vp_gravity_ssot.py --check txt # drift gate over all chapters → PASS
python3 tools/tc_compute.py                  # real-DEM terrain correction + identity + ⟨cosθ⟩ test
```
No-Tuning preserved: no coefficient was migrated to close a residual. Absolute g remains [O]
(four-wall theorem, αₑₘ class); its boundary is proved, not hidden.
