#!/usr/bin/env python3
"""run_all.py -- reproduce the whole DNA-emergence spine from the frozen NCBI data.

   Order:
     1. extract_orthologs.py   data/mito/*.gb        -> results/orthologs.json
     2. bimodality.py          (H1 two-band partition)
     3. compare_channels.py    (H2 clock/material decoupling) -> results/channel_records.json
     4. state_face.py          (H3 STATE face, nuclear adaptive loci)
     5. length_effect.py       (window-length honesty)
     6. make_figure.py         -> figures/fig_dna_emergence.png

   Captures every console report into results/RESULTS.txt. No tuning, no network:
   all six steps run from the frozen GenBank records under data/. SEED convention = 19.
"""
import os, sys, io, contextlib, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

STEPS = [
    ("extract_orthologs", "1. EXTRACT ORTHOLOGS (13 mito protein-coding genes x 6 taxa)"),
    ("bimodality",        "2. H1  TWO-BAND MATERIAL PARTITION (Elephantidae vs Homo)"),
    ("compare_channels",  "3. H2  CLOCK / MATERIAL DECOUPLING (doubt the average theory)"),
    ("state_face",        "4. H3  STATE FACE (adaptive nuclear loci: cold Hb, coat switch)"),
    ("length_effect",     "5. WINDOW-LENGTH HONESTY (반증 = 발견)"),
    ("make_figure",       "6. FIGURE (figures/fig_dna_emergence.png)"),
]

def main():
    buf = io.StringIO()
    for mod_name, banner in STEPS:
        header = "\n" + "#"*92 + f"\n# {banner}\n" + "#"*92 + "\n"
        print(header)
        buf.write(header)
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            mod.main()
        text = out.getvalue()
        sys.stdout.write(text)
        buf.write(text)
    with open(os.path.join(RES, "RESULTS.txt"), "w") as f:
        f.write(buf.getvalue())
    print("\n" + "="*92)
    print("ALL STEPS COMPLETE -> results/RESULTS.txt ; figures/fig_dna_emergence.png")
    print("="*92)

if __name__ == "__main__":
    main()
