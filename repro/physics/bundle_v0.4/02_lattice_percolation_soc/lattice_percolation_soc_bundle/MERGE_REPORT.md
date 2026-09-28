# Merge report (DOI_complete_v0.2.0 + jamming_rotation_485pm)

This bundle was produced by taking `lattice_percolation_soc_bundle_DOI_complete_v0.2.0.zip` as the base and
adding the `jamming_rotation_485pm` study materials from `lattice_percolation_soc_bundle_jamming_rotation_485pm.zip`.

## Added from 485pm bundle
- code/jamming_rotation_485pm_study.py
- docs/JAMMING_ROTATION_485pm.md
- images/jamming_rot_circ_vs_av.png
- images/jamming_rot_hist.png
- results/jamming_rotation_485pm.csv
- results/jamming_rotation_485pm_summary.json

## Updated/merged
- code/run_all.py (now runs: toy → 3D percolation → SOC → MST → visible wave → 4.85 pm rotation study)
- docs/RESULTS_SUMMARY.md (rotation section appended)
- docs/실행방법.md (combined instructions)
- docs/설명서.md (includes rotation section)
- requirements.txt (adds pandas for the rotation script)

## Integrity
- manifest_sha256.txt regenerated using code/make_manifest.py
