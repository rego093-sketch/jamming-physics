#!/usr/bin/env python3
# =============================================================================
#  gamma_lib_v10.py -- locked inputs + shared functions for the v10 size modules
# =============================================================================
#  PROVENANCE (DATA_LOCK style; genomes are EXTERNAL, referenced not bundled).
#  Growth-plate slices live in <ROOT>/data_small/{mouse_elephant,cat_tiger}_growthplate
#  (carried from v9; FASTA headers carry the genomic coordinate of each slice).
#  TSS coordinates below were extracted from each species' RefSeq genomic.gff
#  (the 'gene' feature: chrom, start, end, strand), streamed from the NCBI
#  datasets packages:
#     mouse    GCF_000001635.27 (GRCm39)
#     elephant GCF_030014295.1  (mLoxAfr1.hap2)
#     cat      GCF_018350175.1  (F.catus_Fca126_mat1.0)
#     tiger    GCF_018350195.1  (P.tigris_Pti1_mat1.1)
#  Each gene's coordinate was cross-checked to fall inside its slice's header range.
#
#  CORRECTION recorded (v10, kept visible -- the biggest_animals_v9 bug):
#  v9 biggest_animals mapped cat seq8=FGFR3/seq9=NPR2 and tiger seq13=FGFR3/seq14=NPR2.
#  The gff 'gene' feature shows the OPPOSITE: those chromosomes host
#  cat   seq8 (NC_058380.1)=NPR2, seq9 (NC_058371.1)=FGFR3 ;
#  tiger seq13(NC_056672.1)=NPR2, seq14(NC_056663.1)=FGFR3 .
#  => v9 SWAPPED FGFR3<->NPR2 for both felids (the brake and the strongest-signal gene).
#  v10 uses the gff-correct mapping below.
#
#  gamma = -mean(NN stacking dG, SantaLucia 1998) over called dinucleotide steps
#  (N-steps skipped). DETERMINISM: pure arithmetic, bit-for-bit.
# =============================================================================
import os

ROOT = os.environ.get("V10_ROOT",
                      os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DS = os.path.join(ROOT, "data_small")
GP = os.path.join(DS, "mouse_elephant_growthplate")
CT = os.path.join(DS, "cat_tiger_growthplate")

# SantaLucia 1998 unified NN dG37 (kcal/mol); stiffness = -dG (more stable = stiffer)
NN = {"AA":-1.00,"TT":-1.00,"AT":-0.88,"TA":-0.58,"CA":-1.45,"TG":-1.45,
      "GT":-1.44,"AC":-1.44,"CT":-1.28,"AG":-1.28,"GA":-1.30,"TC":-1.30,
      "CG":-2.17,"GC":-2.24,"GG":-1.84,"CC":-1.84}

MASS = {"mouse":0.025, "cat":4.0, "tiger":220.0, "elephant":5000.0}
SPECIES = ["mouse", "cat", "tiger", "elephant"]
GENES   = ["IHH", "FGFR3", "NPR2", "PTHLH", "SOX9"]

# (slice_path, slice_start, gene_start, gene_end, strand) -- gff-correct mapping
COORDS = {
 ("mouse","IHH"):  (f"{GP}/mouse_Ihh.fa",        74834474, 74984474, 74990831, "-"),
 ("mouse","FGFR3"):(f"{GP}/mouse_Fgfr3.fa",      33729068, 33879068, 33894412, "+"),
 ("mouse","NPR2"): (f"{GP}/mouse_Npr2_region.fa",43479015, 43629015, 43651437, "+"),
 ("mouse","PTHLH"):(f"{GP}/mouse_Pthlh.fa",     147003607,147153607,147165511, "-"),
 ("mouse","SOX9"): (f"{GP}/mouse_Sox9.fa",      112523036,112673036,112678583, "+"),
 ("elephant","IHH"):  (f"{GP}/elephant_IHH.fa",   27063609, 27213609, 27219009, "+"),
 ("elephant","FGFR3"):(f"{GP}/elephant_FGFR3.fa",157027386,157177386,157195810, "+"),
 ("elephant","NPR2"): (f"{GP}/elephant_NPR2.fa",  81835609, 81985609, 82004922, "-"),
 ("elephant","PTHLH"):(f"{GP}/elephant_PTHLH.fa",110478508,110628508,110640175, "+"),
 ("elephant","SOX9"): (f"{GP}/elephant_SOX9.fa",  20668948, 20818948, 20824738, "-"),
 # cat (gff-correct; v9 swapped 8/9): seq7=IHH seq8=NPR2 seq9=FGFR3 seq10=PTHLH seq11=SOX9
 ("cat","IHH"):  (f"{CT}/sequence__7_.fasta", 202824483,202924483,202930931, "-"),
 ("cat","NPR2"): (f"{CT}/sequence__8_.fasta",  57374786, 57474786, 57491542, "+"),
 ("cat","FGFR3"):(f"{CT}/sequence__9_.fasta", 204203604,204303604,204320499, "-"),
 ("cat","PTHLH"):(f"{CT}/sequence__10_.fasta", 61069608, 61169608, 61183905, "-"),
 ("cat","SOX9"): (f"{CT}/sequence__11_.fasta", 52970295, 53070295, 53075102, "+"),
 # tiger (gff-correct; v9 swapped 13/14): seq12=IHH seq13=NPR2 seq14=FGFR3 seq15=PTHLH seq16=SOX9
 ("tiger","IHH"):  (f"{CT}/sequence__12_.fasta",201230264,201330264,201336600, "-"),
 ("tiger","NPR2"): (f"{CT}/sequence__13_.fasta", 56983701, 57083701, 57100353, "+"),
 ("tiger","FGFR3"):(f"{CT}/sequence__14_.fasta",203082832,203182832,203198066, "-"),
 ("tiger","PTHLH"):(f"{CT}/sequence__15_.fasta", 60390915, 60490915, 60502776, "-"),
 ("tiger","SOX9"): (f"{CT}/sequence__16_.fasta", 52502210, 52602210, 52606987, "+"),
}

def read_seq(path):
    s = []
    with open(path) as fh:
        for ln in fh:
            if not ln.startswith(">"):
                s.append(ln.strip())
    return "".join(s).upper()

def gamma(seq):
    import numpy as np
    v = [-NN[seq[i:i+2]] for i in range(len(seq)-1) if seq[i:i+2] in NN]
    return float(np.mean(v)) if v else float("nan")

def windows(sp, gene):
    """Return (promoter_seq, genebody_seq, whole_seq) for one (species,gene).
       promoter = TSS-2000..+500 (strand-oriented); gamma is strand-symmetric."""
    path, sstart, gs, ge, strand = COORDS[(sp, gene)]
    seq = read_seq(path)
    tss = gs if strand == "+" else ge
    a, b = (tss-2000, tss+500) if strand == "+" else (tss-500, tss+2000)
    prom = seq[max(0, a-sstart):(b-sstart)+1]
    body = seq[gs-sstart:(ge-sstart)+1]
    return prom, body, seq
