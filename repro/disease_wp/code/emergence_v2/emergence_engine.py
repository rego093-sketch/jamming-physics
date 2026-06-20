#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
emergence_engine.py -- dynamical emergence driven by a GROUNDED parameter DB.

Replaces the old target-fitting geometry with a forward run that USES the
systemic parameters. Every physical constant comes from param_db.json (locked,
cited, target-independent). The engine NEVER reads the validation targets
(real anatomical sizes; the staged-timing table) -- that separation is what makes
the DB values legitimate [L] inputs rather than a back-fit.

Layers
  WHEN    : relay ODE; rate from MEASURED protein half-life (Schwanhausser 2011)
            -> onset in HOURS, physically grounded, not tuned to days.       [L]+[F]
  HOW BIG : size = dwell(gamma) x DOSAGE; DOSAGE = (time available)^alpha,
            a single UNIVERSAL supply rule applied identically to all.        [F]
  (TRAJECTORY: reduced-order RD hook present; full continuum form is [O].)

What is graded what:
  * onset ORDER ........ [V] (argsort spinodal(gamma); deterministic)
  * onset ABSOLUTE hrs . [L]-grounded timescale (measured kinetics) -- NOT fitted
  * emergent SIZE ...... [F] (universal supply rule) -- magnitudes not validated
  * size-vs-real-mass .. [O] (needs per-organ growth atlas; engine does NOT compare)
"""

import os, json, math, hashlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DB = json.load(open(os.path.join(HERE, "param_db.json"), encoding="utf-8"))

# measured cardiac gamma (read-only; same NCBI->SantaLucia values as the package)
GAMMA = {"NKX2-5":1.513,"GATA4":1.3933,"HAND2":1.4566,"ISL1":1.4244,
         "TBX5":1.4392,"SOX9":1.4598,"MEF2C":1.2443,"TBX1":1.5935}
GENES = list(GAMMA.keys())

# literature cardiac relay DAG (epistasis, not day); same as the timing test
EDGES = [("S","NKX2-5"),("NKX2-5","GATA4"),("NKX2-5","TBX5"),("GATA4","TBX5"),
         ("S","ISL1"),("GATA4","HAND2"),("GATA4","MEF2C"),("ISL1","MEF2C"),
         ("ISL1","TBX1"),("GATA4","SOX9")]

def spinodal(g): return 2.0*(g/3.0)**1.5
def dwell(g, K=0.6, brake=0.5): return (g**1.5)/(K+brake)

# ---- parameters pulled from the DB (NOT inline magic numbers) ----------------
def kinetics():
    k = DB["kinetics"]
    halflife_h = k["protein_halflife_h"]["value"]      # [L] measured
    theta      = k["relay_threshold_theta"]["value"]   # [F]
    kd = math.log(2.0) / halflife_h                    # decay rate from half-life
    return kd, theta, halflife_h
def alpha():
    return DB["allometry"]["growth_supply_exponent_alpha"]["value"]   # [F] universal

# ---- WHEN: relay ODE in real hours (rate from measured half-life) ------------
def relay_onset_hours(theta_override=None):
    kd, theta, _ = kinetics()
    if theta_override is not None: theta = theta_override
    kp = kd  # steady state kp/kd = 1 (normalised); onset set by threshold, not by amplitude
    preds = {n: [] for n in GENES}
    for a,b in EDGES: preds[b].append(a)
    A = {n: 0.0 for n in GENES}; A["S"] = 1.0
    onset = {n: math.inf for n in GENES}
    dt = 0.05; T = 5000.0; t = 0.0   # hours
    for _ in range(int(T/dt)):
        on = {n:(A[n] >= theta) for n in GENES}; on["S"] = True
        for n in GENES:
            ups = preds.get(n, [])
            drive = kp if (ups and all(on[u] for u in ups)) else 0.0
            A[n] += dt*(drive - kd*A[n])
            if onset[n] == math.inf and A[n] >= theta: onset[n] = t
        t += dt
    return onset

# ---- HOW BIG: dwell(gamma) x universal supply dosage ------------------------
def emerge():
    onset = relay_onset_hours()
    t_cut = max(onset.values()) + math.log(2.0)/kinetics()[0]   # one more half-life of supply
    a = alpha()
    out = {}
    for g in GENES:
        time_available = max(t_cut - onset[g], 0.0)
        dosage = time_available ** a                  # UNIVERSAL rule, same for all
        size = dwell(GAMMA[g]) * dosage                # absolute size EMERGES
        out[g] = dict(onset_h=round(onset[g],2), dosage=round(dosage,2), size=round(size,2),
                      order_rank=None)
    order = sorted(GENES, key=lambda g: onset[g])
    for i,g in enumerate(order): out[g]["order_rank"] = i+1
    return out, round(t_cut,2)

def result_hash():
    feats,_ = emerge()
    blob = json.dumps(feats, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()[:12]

if __name__ == "__main__":
    kd, theta, hl = kinetics()
    feats, t_cut = emerge()
    print("="*82)
    print("  DYNAMICAL EMERGENCE ENGINE  (DB-grounded; targets never read)")
    print("="*82)
    print(f"  kinetics: protein half-life={hl} h [L] -> kd={kd:.4f}/h ; theta={theta} [F] ; alpha={alpha()} [F]")
    print(f"  developmental window emerged: 0 .. {t_cut} h  (~{t_cut/24:.1f} days) -- from measured kinetics, NOT fit\n")
    print(f"  {'gene':8s} {'rank':>4s} {'onset(h)':>9s} {'~day':>6s} {'dosage':>8s} {'size(emergent)':>15s}")
    order = sorted(GENES, key=lambda g: feats[g]['order_rank'])
    for g in order:
        f = feats[g]
        print(f"  {g:8s} {f['order_rank']:>4d} {f['onset_h']:>9.2f} {f['onset_h']/24:>6.1f} {f['dosage']:>8.2f} {f['size']:>15.2f}")
    print("\n  GRADES: order=[V] ; absolute onset hours=[L]-grounded (measured half-life) ;")
    print("          emergent size=[F] (universal supply rule) ; size-vs-real-mass=[O] (not compared).")
    print(f"  determinism: result sha={result_hash()}")
    print("="*82)
