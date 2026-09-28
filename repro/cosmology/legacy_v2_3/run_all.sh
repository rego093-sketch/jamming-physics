#!/usr/bin/env bash
# Run every reproducibility script for The Earth-Cosmos Volume, in order.
# Requirements: Python >= 3.8, numpy (matplotlib optional, only for figures).
# Each script is deterministic (no random seeds). See README_REPRODUCIBILITY_MAP.md.
set -u
export MPLBACKEND=Agg
cd "$(dirname "$0")"
scripts=(
  ch1_inflow_rates.py
  ch3_gravity.py ch3_gate.py
  ch4_solar_system.py
  ch5_spin_tidal.py ch_galactic_spin.py
  ch6_galaxy_rar.py
  ch7_lattice_optics.py
  ch8_deficit.py ch8_bullet.py
  ch9_lattice_cmb.py
  ch12_sunspot.py
  ch_accuracy_dashboard.py
  ch10_ledger.py
  ch2_light.py ch2_lightangle.py ch2_grb.py ch2_goldstone.py ch2_stiffness.py
  ch2_relativistic.py ch2_gammashot.py ch2_collision.py ch2_shake.py
  ch2_gammacontent.py ch2_burstprop.py ch2_jammed2d.py ch2_upconvert.py
)
pass=0; fail=0
for s in "${scripts[@]}"; do
  printf '=== %s ===\n' "$s"
  if python3 "$s"; then pass=$((pass+1)); else fail=$((fail+1)); echo "  [FAILED: $s]"; fi
done
echo "-----"; echo "Completed: $pass ok, $fail failed (of ${#scripts[@]})."
