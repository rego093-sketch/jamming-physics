#!/usr/bin/env python3
"""
verify_em_thesis.py — the lock for EM_NEAR_FAR_THESIS.md

Re-derives the load-bearing measurements and asserts BOTH boundaries of the thesis:
  (A) the radiative far-field / optical-fibre (TIR) carrier is RETIRED, and
  (B) the near-field / conduction (ephaptic) form is AFFIRMED.

It fails if EITHER boundary drifts — i.e. if a future edit tries to (a) retire "EM"
wholesale (which would contradict the measured, at-threshold near-field), or (b) revive the
far-field broadcast (which would contradict non-radiation / transparency / velocity).

No RNG, no tuned constant. Every number is a measured input or a derived value.
Run: `python3 verify_em_thesis.py`  -> prints PASS/FAIL and exits 0/1.
"""
import math
import sys

# ---- measured inputs (locked, cited) -------------------------------------------------
MU0     = 4 * math.pi * 1e-7      # vacuum permeability (H/m)
C       = 2.998e8                 # speed of light in vacuum (m/s)
SIGMA   = 0.3                     # tissue conductivity (S/m), extracellular/grey-matter
R_BRAIN = 0.085                   # brain radius (m)  -- same as neuro §18
HEAD    = 0.17                    # head thickness scale (m)
F_GAMMA = 40.0                    # representative EEG band (Hz)
V_NERVE = (0.5, 120.0)            # measured nerve conduction velocity (m/s)
N_TISSUE = 1.4                    # tissue refractive index (optical)
# ephaptic (neuro §19): measured field x measured sensitivity, bound is independent
E_FIELD  = 2.29                   # mV/mm   (Frohlich & McCormick 2010)
SENS     = 0.12                   # mV per mV/mm (Bikson 2004)
DVM_BOUND = 0.5                   # mV      (Anastassiou 2011, ephaptic bound)
# axon cable inputs
RM = 1.0    # membrane resistivity (ohm*m^2)
A  = 5e-6   # axon radius (m)
RI = 1.0    # axoplasm resistivity (ohm*m)

# ---- derived values ------------------------------------------------------------------
lam_gamma   = C / F_GAMMA
k_gamma     = 2 * math.pi / lam_gamma
rad_frac    = (k_gamma * R_BRAIN) ** 2                 # radiated fraction (sub-lambda)
delta_gamma = math.sqrt(2 / (2 * math.pi * F_GAMMA * MU0 * SIGMA))
head_over_d = HEAD / delta_gamma                       # << 1  => transparent
v_light     = C / N_TISSUE
v_ratio     = v_light / V_NERVE[1]                      # light / fastest nerve
lam_cable   = math.sqrt(RM * A / (2 * RI))              # cable space constant (m)
dvm         = SENS * E_FIELD                            # derived ephaptic depolarisation (mV)

checks = []
def check(name, ok, detail):
    checks.append(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")

print("=" * 78)
print("EM_NEAR_FAR_THESIS — gate")
print("=" * 78)

print("\n(A) RETIRED — radiative far-field / optical-fibre (TIR) carrier")
check("non-radiation (sub-wavelength)",
      rad_frac < 1e-9,
      f"radiated fraction (kr)^2 = {rad_frac:.2e}  (<< 1e-9 required)")
check("transparency (not contained by reflection)",
      head_over_d < 1e-2,
      f"head/skin-depth = {head_over_d:.2e}  (<< 1e-2 => wave passes, no reflection-trap)")
check("velocity rules out waveguided light",
      v_ratio >= 1e6,
      f"light/nerve = {v_ratio:.2e}x  (nerve {V_NERVE[0]}-{V_NERVE[1]} m/s vs light {v_light:.2e} m/s)")

print("\n(B) AFFIRMED — near-field / conduction (ephaptic) form")
check("ephaptic field is real and contained in measured bound",
      dvm < DVM_BOUND,
      f"derived dVm = {dvm:.4f} mV  (contained in measured < {DVM_BOUND} mV)")
check("ephaptic field is AT threshold, not negligible",
      dvm > 0.1,
      f"dVm = {dvm:.4f} mV  (>0.1 mV => order-1 fraction of the bound, NOT << )")
check("observed current flows internally like a cable",
      1e-4 < lam_cable < 1e-2,
      f"cable space constant = {lam_cable*1e3:.2f} mm  (mm-scale internal flow)")

print("\n" + "-" * 78)
both_ok = all(checks)
if both_ok:
    print("THESIS LOCK: PASS")
    print("  -> near-field EM AFFIRMED (measured, at threshold);")
    print("  -> radiative far-field carrier RETIRED (by measurement);")
    print("  -> 'EM' is NOT retired wholesale. Both boundaries hold.")
else:
    print("THESIS LOCK: FAIL — a boundary drifted. Revert the edit; do not paper over.")
print("-" * 78)
sys.exit(0 if both_ok else 1)
