#!/usr/bin/env python3
"""Generate Core-82 storage artifacts (X82.csv, G82.edgelist, layers82.csv, params82.yaml).

This is a deterministic *reference instance* meant to satisfy the whitepaper's
§8.1.9 sealing requirement at the file-format level.

It does not claim to be the unique physical core; it provides a reproducible
concrete instance that is internally consistent (r=||x||, connected graph,
BFS layers from the smallest-radius roots).
"""

from __future__ import annotations

import csv
import json
import math
from collections import deque
from pathlib import Path


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding='utf-8')


def main() -> None:
    root = Path(__file__).resolve().parents[1]

    # build points
    coords = []
    spacing = 1.0
    for iz in range(4):
        for iy in range(4):
            for ix in range(5):
                coords.append((ix,iy,iz))
    coords.append((5,0,0))
    coords.append((5,1,0))
    coords = coords[:82]

    cx = (max(x for x,_,_ in coords) + min(x for x,_,_ in coords))/2
    cy = (max(y for _,y,_ in coords) + min(y for _,y,_ in coords))/2
    cz = (max(z for _,_,z in coords) + min(z for _,_,z in coords))/2

    X_rows = []
    for idx,(x,y,z) in enumerate(coords, start=1):
        x0 = (x - cx)*spacing
        y0 = (y - cy)*spacing
        z0 = (z - cz)*spacing
        r = math.sqrt(x0*x0 + y0*y0 + z0*z0)
        X_rows.append((idx, x0, y0, z0, r))

    with (root/'X82.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['i','x','y','z','r'])
        for row in X_rows:
            w.writerow(row)

    pts = {i:(x,y,z) for i,x,y,z,_ in X_rows}
    edges = []
    for i in range(1,83):
        xi,yi,zi = pts[i]
        for j in range(i+1,83):
            xj,yj,zj = pts[j]
            d = math.sqrt((xi-xj)**2+(yi-yj)**2+(zi-zj)**2)
            if d <= 1.01:
                edges.append((i,j))

    (root/'G82.edgelist').write_text("\n".join([f"{i} {j}" for i,j in edges]) + "\n", encoding='utf-8')

    # roots: N0=4 smallest radii
    sorted_by_r = sorted(X_rows, key=lambda t:(t[4], t[0]))
    N0 = 4
    roots = {i for i, *_ in sorted_by_r[:N0]}

    adj = {i:[] for i in range(1,83)}
    for i,j in edges:
        adj[i].append(j); adj[j].append(i)

    dist = {i: None for i in range(1,83)}
    q = deque()
    for r in roots:
        dist[r] = 0
        q.append(r)
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u] + 1
                q.append(v)

    with (root/'layers82.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['i','d'])
        for i in range(1,83):
            w.writerow([i, dist[i] if dist[i] is not None else -1])

    params = {
        'R_p': 1.0,
        'L_q': 1.0,
        'd_min': 1.0,
        'gamma_c': 1.01,
        'h_grid': spacing,
        'B': 0.0,
        'eps_pos': 0.0,
        'K_max': 0,
        'N0': N0,
        'K_b': 0,
        'Agg': 'GRID',
        'TB': 'index_ascending',
        'notes': ['toy deterministic Core-82 instance for file-format sealing (§8.1.9)']
    }

    lines = []
    for k,v in params.items():
        if isinstance(v, str):
            lines.append(f"{k}: {v}")
        elif isinstance(v, list):
            lines.append(f"{k}: {json.dumps(v)}")
        else:
            lines.append(f"{k}: {v}")

    write_text(root/'params82.yaml', "\n".join(lines)+"\n")

    print('[OK] wrote X82.csv, G82.edgelist, layers82.csv, params82.yaml')


if __name__ == '__main__':
    main()
