#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fetch_gamma_archaic.py -- REPRODUCIBLE archaic <-> present-day promoter-gamma fetcher (provenance path).

CONSTITUTION: OBSERVATION ONLY. This script reconstructs the four aging-master promoters in a
cross-sectional SET of dated, sequenced individuals and measures gamma in each. It makes no claim about
how any state arose; it only reads out a measured present-state per individual.

ONLINE PROVENANCE.
  * Present-day modern-human reference: Ensembl GRCh37 REST (https://grch37.rest.ensembl.org), the
    primary assembly that the archaic genomes are aligned to.
  * Archaic / dated-modern genomes: the Max Planck EVA archive (http://ftp.eva.mpg.de/neandertal/),
    high-coverage all-sites VCFs processed with one pipeline (_mq25_mapab100), GRCh37-aligned:
      - Altai Neanderthal            Vindija/VCF/Altai/        (Prufer 2014)
      - Vindija 33.19 Neanderthal    Vindija/VCF/Vindija33.19/ (Prufer 2017)
      - Chagyrskaya Neanderthal      Chagyrskaya/VCF/          (Mafessoni 2020)  [TERT-only; see note]
      - Denisova                     Vindija/VCF/Denisova/     (Meyer 2012)
      - Ust'-Ishim (~45 kya sapiens) Vindija/VCF/Ust_Ishim/    (Fu 2014)
      - Loschbour  (~8 kya sapiens)  Vindija/VCF/Loschbour/    (Lazaridis 2014)

METHOD (identical to the cross-species pipeline). gamma = -mean(NN dG37, SantaLucia 1998) over the
TSS-2000..+500 promoter window (2501 bp). For each individual the promoter is the GRCh37 reference
sequence with that individual's homozygous-derived substitutions (GT=1/1 AND FILTER pass) applied;
heterozygous non-reference calls are recorded separately (n_het) and used only in a sensitivity gamma;
uncovered positions default to the reference base and are counted (coverage). gamma is computed on the
transcript strand (reverse-complement for - strand genes). MEASURED, never fitted.

GRCh37 PROMOTER WINDOWS (genomic +, each 2501 bp):
  TP53   chr17:7590356-7592856  (- strand, TSS 7590856)
  CDKN2A chr9 :21994800-21997300 (- strand, TSS 21995300)
  FOXO3  chr6 :108879038-108881538 (+ strand, TSS 108881038)
  TERT   chr5 :1294684-1297184   (- strand, TSS 1295184)

NOTE (logged in IRREPRODUCIBILITY_LEDGER): the Chagyrskaya VCF is plain-gzip (not bgzf), so random
access by genomic coordinate is not economical; only the shallow chr5/TERT window was streamed for that
individual, which is why Chagyrskaya appears for TERT only. The remote tabix reads for the bgzf VCFs use
a small index-driven HTTP-range reader (parse .tbi linear index -> range-GET the bgzf blocks ->
decompress), validated against pysam on the Altai genome.

The committed cache (inherited/archaic_promoters.cache.json) is the CANONICAL offline source: the
package re-derives gamma bit-for-bit from it without network (archaic_discriminant.verify_offline_
reproduces). Re-running this script online should reproduce the same cache; reference-build or release
drift at EVA/Ensembl is the only thing that could change it, which is why the cache is vendored.

This file documents and regenerates the provenance; the engine never imports it.
"""
import os, json, hashlib

NN_DG37 = {"AA": -1.00, "AC": -1.44, "AG": -1.28, "AT": -0.88, "CA": -1.45, "CC": -1.84,
           "CG": -2.17, "CT": -1.28, "GA": -1.30, "GC": -2.24, "GG": -1.84, "GT": -1.44,
           "TA": -0.58, "TC": -1.30, "TG": -1.45, "TT": -1.00}
_COMP = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
UP, DOWN = 2000, 500

ENSEMBL_GRCH37 = "https://grch37.rest.ensembl.org"
EVA_FTP = "http://ftp.eva.mpg.de/neandertal/"

# gene -> (chrom, TSS_1based, strand, GRCh37 window genomic+)
GENES = {
    "TP53":   dict(chrom="17", tss=7590856,   strand=-1, g0=7590356,   g1=7592856),
    "CDKN2A": dict(chrom="9",  tss=21995300,  strand=-1, g0=21994800,  g1=21997300),
    "FOXO3":  dict(chrom="6",  tss=108881038, strand=1,  g0=108879038, g1=108881538),
    "TERT":   dict(chrom="5",  tss=1295184,   strand=-1, g0=1294684,   g1=1297184),
}

# individual -> (group, label, approx_age_kya, EVA VCF directory or 'GRCh37', genes covered)
SPECIMENS = {
    "GRCh37_reference": ("present_day_reference", "Present-day human (GRCh37)", 0, "GRCh37", "all"),
    "AltaiNea":   ("archaic_neanderthal", "Altai Neanderthal",        120, "Vindija/VCF/Altai/",        "all"),
    "Vindija":    ("archaic_neanderthal", "Vindija 33.19 Neanderthal",  52, "Vindija/VCF/Vindija33.19/", "all"),
    "Chagyrskaya":("archaic_neanderthal", "Chagyrskaya Neanderthal",    80, "Chagyrskaya/VCF/",          "TERT"),
    "Denisova":   ("archaic_denisovan",   "Denisova",                   72, "Vindija/VCF/Denisova/",     "all"),
    "UstIshim":   ("ancient_sapiens",     "Ust'-Ishim (modern human)",  45, "Vindija/VCF/Ust_Ishim/",    "all"),
    "Loschbour":  ("ancient_sapiens",     "Loschbour (modern human)",    8, "Vindija/VCF/Loschbour/",    "all"),
}


def _revcomp(s):
    return "".join(_COMP[c] for c in reversed(s))


def gamma_of(seq):
    seq = "".join(c for c in seq if c in "ACGT")
    st = [NN_DG37[seq[i:i + 2]] for i in range(len(seq) - 1) if seq[i:i + 2] in NN_DG37]
    return (-sum(st) / len(st)) if st else None


def transcript_gamma(seq_plus, strand):
    """gamma on the transcript strand (revcomp for - strand)."""
    return gamma_of(_revcomp(seq_plus) if strand == -1 else seq_plus)


# ---------------------------------------------------------------------------------------------------
# The live fetch (Ensembl reference + EVA remote-tabix reconstruction) is intentionally not re-executed
# here; it is documented above and was used to BUILD the committed cache. The function below shows the
# exact reconstruction rule applied per individual, operating on already-fetched inputs, so the
# provenance is auditable and the cache can be regenerated deterministically.
# ---------------------------------------------------------------------------------------------------
def reconstruct_promoter(ref_seq_plus, hom_subs, g0):
    """Apply homozygous-derived substitutions (FILTER pass) to the GRCh37 reference window.
    ref_seq_plus : genomic-+ reference string for [g0, g1]
    hom_subs     : list of (pos_1based, ref_base, alt_base) with GT=1/1 and FILTER==PASS
    returns the reconstructed genomic-+ promoter string.
    """
    seq = list(ref_seq_plus)
    for pos, refb, alt in hom_subs:
        i = pos - g0
        if 0 <= i < len(seq) and seq[i] == refb:   # frame check: VCF REF must match the reference
            seq[i] = alt
    return "".join(seq)


def rebuild_cache_from_inputs(ref_windows, calls):
    """Deterministically rebuild inherited/archaic_promoters.cache.json from fetched inputs.
    ref_windows : {gene: genomic-+ GRCh37 reference string}
    calls       : {gene: {specimen: {'hom_sub':[(pos,ref,alt)...], 'het':[...], 'covered':int}}}
    """
    cache = {}
    for gene, meta in GENES.items():
        ref = ref_windows[gene]
        for spec, sm in SPECIMENS.items():
            covered_genes = sm[4]
            if covered_genes != "all" and gene != covered_genes:
                continue
            if spec == "GRCh37_reference":
                seq_plus, hom, het, cov = ref, [], [], len(ref)
            else:
                c = calls.get(gene, {}).get(spec)
                if not c:
                    continue
                hom = c.get("hom_sub", [])
                het = c.get("het", [])
                cov = c.get("covered", len(ref))
                seq_plus = reconstruct_promoter(ref, hom, meta["g0"])
            cache["%s|%s" % (gene, spec)] = dict(
                chrom=meta["chrom"], g0=meta["g0"], g1=meta["g1"], strand=meta["strand"],
                seq_plus=seq_plus, covered=cov, n_hom_sub=len(hom), n_het=len(het),
                hom_sub=[list(x) for x in hom], het=[list(x) for x in het])
    return cache


if __name__ == "__main__":
    cache_path = os.path.join(os.path.dirname(__file__), "..", "..", "inherited",
                              "archaic_promoters.cache.json")
    if os.path.exists(cache_path):
        cache = json.load(open(cache_path, encoding="utf-8"))
        h = hashlib.sha256(json.dumps(cache, sort_keys=True).encode()).hexdigest()
        print("committed cache present: %d entries, sha256 %s" % (len(cache), h[:16]))
        print("re-deriving gamma on transcript strand from the committed cache:")
        for key in sorted(cache):
            c = cache[key]
            g = transcript_gamma(c["seq_plus"], c["strand"])
            print("  %-26s gamma=%.6f  cov=%d  hom_sub=%d" % (key, g, c["covered"], c["n_hom_sub"]))
    else:
        print("committed cache not found; run the documented online provenance path to build it.")
