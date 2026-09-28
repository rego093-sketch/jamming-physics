#!/usr/bin/env python3
"""exp10: run_2d_throat

Produces:
- outputs/2d_throat/gaps2d.csv
- outputs/2d_throat/gc2d.txt
- outputs/2d_throat/deltaeff2d.txt
- outputs/2d_throat/Gopen2d.edgelist
- outputs/2d_throat/backbone2d.edgelist
- outputs/2d_throat/report_perc2d.json

Toy deterministic implementation (no images).
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path


def read_nodes(path: Path):
    nodes = {}
    with path.open('r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for row in r:
            i = int(row['i'])
            nodes[i] = (float(row['x']), float(row['y']))
    return nodes


def read_edges(path: Path):
    edges = []
    for line in path.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        a,b = line.split()[:2]
        edges.append((int(a), int(b)))
    return edges


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    cfg = (root / 'configs' / 'thresholds.yaml').read_text(encoding='utf-8')
    # parse d0 simply
    d0 = 0.9
    for ln in cfg.splitlines():
        if ln.strip().startswith('d0:'):
            d0 = float(ln.split(':',1)[1].strip())

    nodes = read_nodes(root/'inputs'/'geometry'/'nodes2d.csv')
    edges = read_edges(root/'inputs'/'graphs'/'edges2d.edgelist')

    out = root/'outputs'/'2d_throat'
    out.mkdir(parents=True, exist_ok=True)

    gaps = []
    for (i,j) in edges:
        xi, yi = nodes[i]
        xj, yj = nodes[j]
        dij = math.hypot(xi-xj, yi-yj)
        gij = dij - d0
        gaps.append((i,j,dij,gij))

    # choose g_c as median positive gap
    pos = sorted([g for *_, g in gaps if g > 0])
    gc = pos[len(pos)//2] if pos else 0.0

    # write gaps2d.csv
    with (out/'gaps2d.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['i','j','d_ij','g_ij'])
        for row in gaps:
            w.writerow(row)

    (out/'gc2d.txt').write_text(f"{gc}\n", encoding='utf-8')
    (out/'deltaeff2d.txt').write_text(f"{gc}\n", encoding='utf-8')

    # open graph: edges with 0<g<=gc
    open_edges = [(i,j) for i,j,_,g in gaps if (g > 0 and g <= gc)]
    (out/'Gopen2d.edgelist').write_text("\n".join([f"{i} {j}" for i,j in open_edges]) + "\n", encoding='utf-8')

    # backbone (toy): reuse open edges
    (out/'backbone2d.edgelist').write_text("\n".join([f"{i} {j}" for i,j in open_edges]) + "\n", encoding='utf-8')

    report = {
        'experiment': '2d_throat',
        'status': 'PASS' if gc > 0 else 'INCONCLUSIVE',
        'd0': d0,
        'g_c': gc,
        'delta_eff': gc,
        'n_edges': len(edges),
        'n_open_edges': len(open_edges),
        'notes': ['toy deterministic exp10 package']
    }
    (out/'report_perc2d.json').write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding='utf-8')


if __name__ == '__main__':
    main()
