#!/usr/bin/env python3
"""
contamination_arithmetic.py -- VP Recent-Sequence Cascade, Module 26 (part A).
Radiocarbon contamination mixing arithmetic. FIREWALL-NEUTRAL: this is instrument
physics (how dead/modern carbon mixing shifts apparent 14C age) and is TRUE UNDER
ANY CHRONOLOGY -- it imports no past-occurrence interpretation.

Model:  F_meas = (1-c)*F_true + c*F_contam ;  age = -TAU*ln(F)
  dead-carbon contaminant  F_contam = 0  -> always OLDER (shift independent of true age)
  modern-carbon contaminant F_contam = 1 -> always YOUNGER (OLD samples hypersensitive)

LOCK: TAU = 8033 yr (Libby mean-life). Nothing fitted. SEED=19 convention.
Determinism proven by double-SHA-256 self-gate.
"""
import math, hashlib
SEED = 19
TAU = 8033.0
def F(age):  return math.exp(-age/TAU)
def age(Fv): return -TAU*math.log(Fv) if Fv > 0 else float('inf')
def f1(x):   return f"{x:.1f}"

def ledger():
    L = ["MODULE=26A SEED=%d TAU=%.1f" % (SEED, TAU)]
    # dead carbon -> OLDER ; shift = -TAU*ln(1-c), independent of true age
    for c in (0.01, 0.05, 0.10, 0.30, 0.50, 0.58):
        L.append("DEAD c=%.2f added_older_yr=%s" % (c, f1(-TAU*math.log(1-c))))
    # modern carbon -> YOUNGER ; old samples hypersensitive
    for true in (4000, 10000, 20000, 40000):
        ft = F(true)
        for c in (0.01, 0.05):
            L.append("MODERN true=%d c=%.2f apparent_BP=%s" % (true, c, f1(age((1-c)*ft + c))))
    return "\n".join(L)

def dsha(s): return hashlib.sha256(hashlib.sha256(s.encode()).digest()).hexdigest()
EXPECTED = "faabe48d95a0ad9f432b388d51442fc7bd333f9cf1735c5fd7ab070ac283092b"
if __name__ == "__main__":
    body = ledger(); print(body)
    d = dsha(body); print("\n2xSHA256 = " + d)
    if EXPECTED != "__PENDING__":
        assert d == EXPECTED, "REPRO GATE FAILED: %s != %s" % (d, EXPECTED)
        print("REPRO GATE: PASS")
    else:
        print("REPRO GATE: (freeze EXPECTED)")
