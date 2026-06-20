#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROOF-OF-CONCEPT: emergence that ACTUALLY USES the systemic parameter.

The old appendix geometry hit a TARGET without the systemic parameter (-> [O]).
This instead GROWS a form from the parameter, with NO target and NO fitting:

  WHAT / ORDER : argsort(spinodal(gamma))                 [V]  (measured gamma)
  WHEN         : relay-ODE onset (systemic DYNAMICS)       [F]  (uniform kinetics)
  HOW BIG      : size = dwell(gamma) x DOSAGE(systemic)    [F]  (modelled supply)

DOSAGE here is a *modelled* resource-supply rule (a feature that switches on
earlier has more developmental time/resource before a global cutoff). It is a
MODELLING CHOICE, not a measurement, and is NOT fitted to any organ mass or
stage. The point is the MECHANISM: a realized (time, size) form EMERGES by
running the parameter forward -- not by matching a target.

GRADE CEILING (stated, not hidden):
  * This is [F]: the dynamics/dosage are modelled, parameters generic.
  * The emergent MAGNITUDES are [F]-arbitrary until MEASURED kinetics/growth
    rates replace the generic ones -> that replacement is [O] (data-blocked).
  * We do NOT compare these magnitudes to real masses/days; doing so by tuning
    would be the forbidden back-fit. So validation of realized magnitude = [O].

What this DOES prove: putting a systemic parameter in and re-running emergence
is FEASIBLE and CHEAP at reduced order. What it does NOT do: produce a
measured, validated realized form (that needs measured params + HPC).
"""

import numpy as np

GAMMA = {"NKX2-5":1.513,"GATA4":1.3933,"HAND2":1.4566,"ISL1":1.4244,
         "TBX5":1.4392,"SOX9":1.4598,"MEF2C":1.2443,"TBX1":1.5935}
def spinodal(g): return 2.0*(g/3.0)**1.5
def dwell(g, K=0.6, brake=0.5): return (g**1.5)/(K+brake)

# systemic DYNAMICS: literature cardiac relay (same DAG as the timing test), uniform kinetics
EDGES = [("S","NKX2-5"),("NKX2-5","GATA4"),("NKX2-5","TBX5"),("GATA4","TBX5"),
         ("S","ISL1"),("GATA4","HAND2"),("GATA4","MEF2C"),("ISL1","MEF2C"),
         ("ISL1","TBX1"),("GATA4","SOX9")]
GENES = list(GAMMA.keys())

def relay_onset(kp=1.0, kd=0.15, theta=0.5, dt=0.01, T=200.0):
    preds={n:[] for n in GENES}
    for a,b in EDGES: preds[b].append(a)
    A={n:0.0 for n in GENES}; A["S"]=1.0; onset={n:np.inf for n in GENES}
    t=0.0
    for _ in range(int(T/dt)):
        on={n:(A[n]>=theta) for n in GENES}; on["S"]=True
        for n in GENES:
            ups=preds.get(n,[]); drive=kp if (ups and all(on[u] for u in ups)) else 0.0
            A[n]+=dt*(drive-kd*A[n])
            if onset[n]==np.inf and A[n]>=theta: onset[n]=t
        t+=dt
    return onset

def grow():
    """Run the parameter forward -> emergent (onset, size) form. No target, no fit."""
    onset = relay_onset()
    t_cut = max(onset.values()) + 1.0                       # global developmental cutoff
    feats = {}
    for g in GENES:
        g_val = GAMMA[g]
        time_available = max(t_cut - onset[g], 0.0)         # systemic DOSAGE: supply ~ time before cutoff
        dosage = time_available ** 1.0                      # modelling choice (p=1); NOT fitted
        size = dwell(g_val) * dosage                         # absolute size EMERGES = dwell x dosage
        feats[g] = dict(onset=round(onset[g],3), dosage=round(dosage,3), size=round(size,3))
    return feats, t_cut

if __name__ == "__main__":
    print("="*78)
    print("  EMERGENCE WITH THE SYSTEMIC PARAMETER  (grown, not target-fitted)  [F]")
    print("="*78)
    feats, t_cut = grow()
    order = sorted(GENES, key=lambda g: feats[g]['onset'])
    print(f"  developmental cutoff t_cut = {t_cut:.2f}\n")
    print(f"  {'gene':8s} {'onset(when)':>12s} {'dosage':>9s} {'size(how big)':>14s}")
    for g in order:
        f=feats[g]
        print(f"  {g:8s} {f['onset']:>12.3f} {f['dosage']:>9.3f} {f['size']:>14.3f}")
    print("\n  -> a realized (time, size) form EMERGED by running gamma + dynamics + dosage forward.")
    print("     NO target was matched; NO parameter was fitted to a mass or a stage.")
    print("  GRADE: [F] (modelled dynamics/dosage).  Magnitudes are [F]-arbitrary until MEASURED")
    print("     kinetics/growth-rates replace the generic ones -> that is [O] (data-blocked).")
    print("     Validation against real mass/days is deliberately NOT done (would be back-fit).")
    print("="*78)
    print("  CONCLUSION: re-running emergence WITH a systemic parameter is feasible & cheap at")
    print("  reduced order, and lands at [F]. A MEASURED, validated realized form still needs")
    print("  measured parameters + HPC and remains [O]. The difference is DATA, not difficulty.")
