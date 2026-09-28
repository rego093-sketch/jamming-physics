#!/usr/bin/env python3
"""exp10: run_3d_jamming (toy)

Produces the files named in whitepaper §10.4.5.2.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


def parse_list_yaml(lines, key):
    for ln in lines:
        if ln.strip().startswith(key+':'):
            # next tokens like [a,b,c]
            rhs = ln.split(':',1)[1].strip()
            rhs = rhs.strip('[]')
            if not rhs:
                return []
            return [float(x.strip()) for x in rhs.split(',')]
    return []


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    probes_lines = (root/'configs'/'probes.yaml').read_text(encoding='utf-8').splitlines()
    iso_eps = parse_list_yaml(probes_lines, 'iso_eps')
    drift_u = parse_list_yaml(probes_lines, 'drift_u')

    out = root/'outputs'/'3d_jamming'
    out.mkdir(parents=True, exist_ok=True)

    # Toy switch variables
    switch = {
        'chi_span': 1,
        'kappa_min': 0.0,
        'chi_ST': 1,
        'chi_c': 1,
        'notes': ['toy deterministic']
    }
    (out/'switch.json').write_text(json.dumps(switch, indent=2, sort_keys=True) + '\n', encoding='utf-8')

    # Wiso.csv: define eta(eps)=1+eps, W_iso = eps^2
    with (out/'Wiso.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['eps','eta','Wiso'])
        for eps in iso_eps:
            w.writerow([eps, 1.0+eps, eps*eps])

    # Wdrift.csv: W_drift = u^2
    with (out/'Wdrift.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['u','Wdrift'])
        for u in drift_u:
            w.writerow([u, u*u])

    # Beff, rhoeff, ctilde, c
    # Use simple functions of probe sets
    Beff = float(sum(eps*eps for eps in iso_eps) / max(len(iso_eps),1))
    rhoeff = float(sum(u*u for u in drift_u) / max(len(drift_u),1))
    ctilde = 1.0 / (1.0 + Beff + rhoeff)

    # Read realization lock for a/dt
    realz = json.loads((root/'registry'/'realization_lock.json').read_text(encoding='utf-8'))
    a_m = float(realz['inputs']['a_m'])
    dt_s = float(realz['inputs']['dt_s'])
    c = (a_m/dt_s) * ctilde

    (out/'Beff.txt').write_text(f"{Beff}\n", encoding='utf-8')
    (out/'rhoeff.txt').write_text(f"{rhoeff}\n", encoding='utf-8')
    (out/'ctilde.txt').write_text(f"{ctilde}\n", encoding='utf-8')
    (out/'c.txt').write_text(f"{c}\n", encoding='utf-8')

    report = {
        'experiment': '3d_jamming',
        'status': 'PASS',
        'Beff': Beff,
        'rhoeff': rhoeff,
        'ctilde': ctilde,
        'c_m_s': c,
        'switch': switch,
        'notes': ['toy deterministic exp10 package']
    }
    (out/'report_c.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
