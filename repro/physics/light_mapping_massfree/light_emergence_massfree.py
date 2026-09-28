"""light_emergence_massfree.py — RECONSTRUCTED (2026-09-28).

The original module 06_light_mapping_massfree/ cited in §10.9.1 and W.0 is not in the
v0.4 bundle. This file re-implements the §10.9.1 table from its written specification so
that the committed light angles can be regenerated. It is deterministic and seed-free.

  sin(chi) = lambda / (m D),  m = ceil(lambda / D),  D = D_anch = 4.852620477 pm

What this checks and what it does not:
  * It regenerates chi(633) and chi(532) from D. That is a forward map, length -> angle.
  * The ratio (lambda/D)_633 / (lambda/D)_532 = 633/532 holds for ANY fixed D; it is
    arithmetic and is not evidence that the lattice wave is light. The test that can
    fail is E2 (repro/physics/experiments/E2): the wavelength-free lattice amplification A
    must connect independently measured lambda and D.
  * Sensitivity: over D +/- 0.03 % the angle moves by at most ~0.17 deg (it jumps with the
    integer m); the earlier text claim "> 1 deg" was an overstatement.
"""
import math

D = 4.852620477e-12
CHANNELS = {"633": 632.99e-9, "532": 532.0e-9}   # reporting-precision inputs sealed in §10.9.1


def angle(lam, d=D):
    m = math.ceil(lam / d)
    return m, math.degrees(math.asin(lam / (m * d)))


def main():
    print(f"{'ch':>4} {'lambda/D':>14} {'m':>8} {'chi(deg)':>10} {'m cos chi (D)':>14}")
    for ch, lam in CHANNELS.items():
        m, chi = angle(lam)
        print(f"{ch:>4} {lam / D:14.4f} {m:8d} {chi:10.4f} {m * math.cos(math.radians(chi)):14.2f}")
    for ch, lam in CHANNELS.items():
        base = angle(lam)[1]
        shift = max(abs(angle(lam, D * (1 + k * 1e-6))[1] - base) for k in range(-300, 301))
        print(f"sensitivity {ch}: max |d chi| over D +/-0.03% = {shift:.3f} deg")


if __name__ == "__main__":
    main()
