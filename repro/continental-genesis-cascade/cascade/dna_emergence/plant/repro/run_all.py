#!/usr/bin/env python3
"""run_all.py -- reproduce the whole plant DNA-emergence spine from frozen NCBI records.

   1. plastid_partition.py   data/plastid/*.gb  -> results/plastid_orthologs.json   (H1')
   2. clock_decoupling.py    (H2)               -> results/plant_channel_records.json
   3. state_face_cold_uv.py  (H3, the cold-vs-UV hypothesis)
   4. length_composition.py  (gamma<->GC composition honesty)
   5. make_figure.py         -> figures/fig_plant_emergence.png

   No network, no tuning: runs from the frozen GenBank records. SEED convention = 19.
"""
import os, sys, io, contextlib, importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RES = os.path.join(HERE, "..", "results")
os.makedirs(RES, exist_ok=True)

STEPS = [
    ("plastid_partition",  "1. H1'  PLASTID material across kinds (grass vs nightshade)"),
    ("clock_decoupling",   "2. H2   CLOCK / MATERIAL decoupling (doubt the average theory)"),
    ("state_face_cold_uv", "3. H3   COLD vs UV STATE face (the user's hypothesis)"),
    ("length_composition", "4. COMPOSITION honesty (gamma <-> GC -> lineage property)"),
    ("make_figure",        "5. FIGURE (figures/fig_plant_emergence.png)"),
]

def main():
    buf = io.StringIO()
    for mod_name, banner in STEPS:
        header = "\n" + "#" * 88 + f"\n# {banner}\n" + "#" * 88 + "\n"
        print(header); buf.write(header)
        mod = importlib.import_module(mod_name); importlib.reload(mod)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            mod.main()
        text = out.getvalue()
        sys.stdout.write(text); buf.write(text)
    with open(os.path.join(RES, "RESULTS.txt"), "w") as f:
        f.write(buf.getvalue())
    print("\n" + "=" * 88)
    print("ALL STEPS COMPLETE -> results/RESULTS.txt ; figures/fig_plant_emergence.png")
    print("=" * 88)

if __name__ == "__main__":
    main()
