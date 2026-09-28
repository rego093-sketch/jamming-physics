#!/usr/bin/env python3
"""
ch1_inflow_rates.py  --  Reproduces Chapter 1 (The Single Input: the inflow rate).

CLAIM TESTED
------------
The inflow (vacuum-annihilation) rate is fixed by the pi-chain of the physics volume:
    nucleon  nu_p = 3*pi^4        ~ 292.227 s^-1   (forced; physics-volume LOCK-NU-N)
    electron nu_e = 1             =   1     s^-1   (n=1 of nu_n = n*pi^(2(n-1)))
    hydrogen nu_H = 3*pi^4 + 1     ~ 293.227 s^-1
For bulk matter the nucleon term dominates, so Q is proportional to mass with
    Q/M = nu_H / m_H = 1.7522e29  quanta s^-1 kg^-1   (hydrogen anchor).
Per-body inflow rate is then Q = M * (nu_H/m_H).

INPUTS  (no fitting; pure constants + textbook masses)
------
pi; atomic mass unit m_u = 1.66054e-27 kg; hydrogen-atom mass m_H = 1.6735e-27 kg;
body masses (kg) from standard references.

ALGORITHM
---------
Compute nu_p, nu_e, nu_H, m_p/m_e=6*pi^5; Q/M; then Q = M*(Q/M) and N_nuc = M/m_u per body.

EXPECTED OUTPUT  (verify against Chapter 1, Table 1)
---------------
nu_p=292.2273, nu_e=1, nu_H=293.2273, m_p/m_e=1836.118
Q/M = 1.7522e+29
Sun  Q=3.485e59 ; Earth Q=1.046e54 ; Moon Q=1.286e52 ; Jupiter Q=3.326e56  (etc.)
Ratio column equals M/M_Earth because Q ∝ M.
"""
import math

pi = math.pi
nu_p = 3*pi**4
nu_e = 1.0
nu_H = nu_p + nu_e
mp_me = 6*pi**5                      # = 2*pi*nu_p, internal consistency
m_u  = 1.66054e-27                   # atomic mass unit [kg]
m_H  = 1.6735e-27                    # hydrogen-atom mass [kg]
QperM = nu_H / m_H                   # quanta s^-1 kg^-1

bodies = [   # name, mass [kg]
    ("Sun",     1.98892e30), ("Mercury", 3.3011e23), ("Venus",   4.8675e24),
    ("Earth",   5.97237e24), ("Mars",    6.4171e23), ("Jupiter", 1.89819e27),
    ("Saturn",  5.6834e26),  ("Uranus",  8.6810e25), ("Neptune", 1.02413e26),
    ("Moon",    7.3420e22),
]
M_earth = 5.97237e24

if __name__ == "__main__":
    print("=== Forced pi-chain constants ===")
    print(f"nu_p = 3*pi^4   = {nu_p:.4f} s^-1")
    print(f"nu_e            = {nu_e:.0f} s^-1")
    print(f"nu_H = 3*pi^4+1 = {nu_H:.4f} s^-1")
    print(f"m_p/m_e = 6*pi^5 = {mp_me:.4f}  (= 2*pi*nu_p)")
    print(f"Q/M = nu_H/m_H  = {QperM:.4e} quanta s^-1 kg^-1\n")
    print(f"{'body':8s} {'M [kg]':>13} {'N_nucleons':>13} {'Q [s^-1]':>13} {'Q/Q_Earth':>11}")
    for name, M in bodies:
        Q = M*QperM; N = M/m_u
        print(f"{name:8s} {M:13.4e} {N:13.3e} {Q:13.4e} {M/M_earth:11.3e}")
    print("\nPASS if these match Chapter 1 Table 1 (ratios exact; absolutes use the hydrogen anchor).")
